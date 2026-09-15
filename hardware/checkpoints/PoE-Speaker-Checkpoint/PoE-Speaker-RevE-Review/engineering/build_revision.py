"""Build the editable Rev B development schematic and unrouted placement board.

The recovery snapshot is read only. Connectivity comes from revision-b-design.json.
"""
import collections,json,math,re,sys,uuid,shutil
from pathlib import Path
import pcbnew as pcb
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE))
model=json.loads((BASE/'engineering/revision-b-design.json').read_text(encoding='utf-8'))
OUT=BASE/'KiCad-RevB';OUT.mkdir(exist_ok=True)
LIB=OUT/'SpeakerRevB.pretty';LIB.mkdir(exist_ok=True)
REPORT=OUT/'reports';REPORT.mkdir(exist_ok=True)
PROJECT='PoE-Speaker-RevB'
ROOT=str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-revb-root'))
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-revb:'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def natural(s):return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)',s)]
V=lambda x,y:pcb.VECTOR2I(round(x*1e6),round(y*1e6))
b=pcb.BOARD();b.SetCopperLayerCount(4)
old=pcb.LoadBoard(str(BASE/'KiCad-Recovered/PoE-Speaker.kicad_pcb'))
oldfps={fp.GetReference():fp for fp in old.GetFootprints()}
netnames=sorted({p['net'] for c in model['components'].values() for p in c['pins'] if p['net']})
nets={}
for nm in netnames:
    n=pcb.NETINFO_ITEM(b,nm);b.Add(n);nets[nm]=n
def rect(fp,x,y,layer):
    s=pcb.PCB_SHAPE(fp);s.SetShape(pcb.SHAPE_T_RECT);s.SetStart(V(-x,-y));s.SetEnd(V(x,y));s.SetLayer(layer);s.SetWidth(pcb.FromMM(.05 if layer==pcb.F_CrtYd else .1));fp.Add(s)
def inductor(name):
    fp=pcb.FOOTPRINT(b)
    if name=='SRP1038A':pitch,sx,sy,bodyx,bodyy=9.5,4.1,3.5,11.5,10.3
    else:pitch,sx,sy,bodyx,bodyy=3.31,1.18,4.7,5.48,5.68
    layers=pcb.LSET()
    for layer in [pcb.F_Cu,pcb.F_Paste,pcb.F_Mask]:layers.AddLayer(layer)
    for pn,x in [('1',-pitch/2),('2',pitch/2)]:
        p=pcb.PAD(fp);p.SetNumber(pn);p.SetAttribute(pcb.PAD_ATTRIB_SMD);p.SetShape(pcb.PAD_SHAPE_RECT);p.SetSize(V(sx,sy));p.SetPosition(V(x,0));p.SetLayerSet(layers);fp.Add(p)
    rect(fp,bodyx/2,bodyy/2,pcb.F_Fab)
    rect(fp,max(bodyx/2,(pitch+sx)/2)+.25,max(bodyy/2,sy/2)+.25,pcb.F_CrtYd)
    return fp
fplist={};footprint_names={};issues=[]
for ref,c in model['components'].items():
    target=c.get('footprint')
    if target:
        lib,name=target.split(':')
        fp=inductor(name) if lib=='SpeakerRevB' else pcb.FootprintLoad('C:/Program Files/KiCad/10.0/share/kicad/footprints/'+lib+'.pretty',name)
        assert fp,(ref,target)
    else:
        original=oldfps[ref]
        fn=str(original.GetFPID().GetLibItemName())
        fp=pcb.FootprintLoad(str(BASE/'KiCad-Recovered/FluxRecovered.pretty'),fn)
        assert fp,(ref,fn)
    # Remove degenerate source courtyard segments, preserving real outlines.
    for item in list(fp.GraphicalItems()):
        if isinstance(item,pcb.PCB_SHAPE) and item.GetShape()==pcb.SHAPE_T_SEGMENT and item.GetStart()==item.GetEnd():fp.Remove(item)
    fp.Models().clear();fp.SetReference(ref);fp.SetValue(c['value']);name=ref+'_RevB'
    footprint_names[ref]=name;fp.SetFPID(pcb.LIB_ID('SpeakerRevB',name));fp.Value().SetVisible(False)
    fp.Reference().SetPosition(V(0,-4));fp.Reference().SetTextSize(V(.8,.8));fp.Reference().SetTextThickness(pcb.FromMM(.12))
    pcb.PCB_IO_MGR.FindPlugin(pcb.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(LIB),fp);b.Add(fp)
    fp.SetPosition(V(*c['position']))
    if c['side']=='Bottom':fp.Flip(fp.GetPosition(),False)
    fp.SetOrientationDegrees(c['angle'])
    pnmap={p['number']:p['net'] for p in c['pins']}
    padnums={p.GetNumber() for p in fp.Pads() if p.GetNumber()}
    assert set(pnmap)<=padnums,(ref,'missing pads',set(pnmap)-padnums)
    for p in fp.Pads():
        nm=pnmap.get(p.GetNumber())
        if nm:p.SetNet(nets[nm])
    fplist[ref]=fp
# Proposed envelope around the existing four mounting holes.
for a,z in [((70,50),(230,50)),((230,50),(230,150)),((230,150),(70,150)),((70,150),(70,50))]:
    s=pcb.PCB_SHAPE(b);s.SetShape(pcb.SHAPE_T_SEGMENT);s.SetStart(V(*a));s.SetEnd(V(*z));s.SetLayer(pcb.Edge_Cuts);s.SetWidth(pcb.FromMM(.05));b.Add(s)

# Reuse the tested native schematic serializer, with the revised explicit model.
els={c['uuid']:{'uid':c['uuid'],'label':ref,'c':c} for ref,c in model['components'].items()}
def props(e):return dict(e['c']['properties'],**{'Functional Group':e['c']['sheet']})
def value(e):return e['c']['value']
terminals={ref:{p['number']:dict(p,pin_number=p['number'],uid=p['number']) for p in c['pins']} for ref,c in model['components'].items()}
pin_net={(ref,p['number']):p['net'] for ref,c in model['components'].items() for p in c['pins'] if p['net']}
d={'noConnects':{c['uuid']+'__'+p['number']:True for c in model['components'].values() for p in c['pins'] if not p['net']}}
src=(BASE/'convert_flux.py').read_text(encoding='utf-8')
src=src[src.index('grouped=collections.defaultdict(list)'):src.index('notice=pcb.PCB_TEXT(b)')]
src=src.replace('FluxRecovered','SpeakerRevB').replace('RECOVERED - REVIEW','REV B - DEVELOPMENT').replace('flux_recovery','speaker_revision')
src=src.replace('pin passive line','pin {t.get("type","passive")} line')
src=src.replace('Recovered pin blocks | Global labels preserve EDIF connectivity | Pin electrical types require review','Rev B circuit draft | Global labels connect sheets | Source component pin types still require review')
src=src.replace('Recovered from Flux exports - editable migration draft','Eight-microphone main board - electrical redesign in progress')
src=src.replace('Read reports/RECOVERY.md before board work.','Read README.md for validation and outstanding work.')
src=src.replace('Recovered Flux pin blocks','Revision B pin blocks').replace('Recovered Flux footprints','Revision B local footprints')
# Split larger groups into readable continuation sheets before the packing loop.
needle='pages=[]; symbol_defs={}; paths={}'
src=src.replace(needle,"expanded=collections.defaultdict(list)\nfor group,items in grouped.items():\n    for i,e in enumerate(sorted(items,key=lambda e:natural(e['label']))):\n        expanded[group+(' '+str(i//21+1) if len(items)>21 else '')].append(e)\ngrouped=expanded\n"+needle)
exec(compile(src,'revision_schematic_serializer','exec'))
pcb.SaveBoard(str(OUT/(PROJECT+'.kicad_pcb')),b)
(OUT/(PROJECT+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':PROJECT+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.2,'min_track_width':.2,'min_via_diameter':.6,'min_through_hole_diameter':.3}}}},indent=2))
expected=collections.defaultdict(list)
for (ref,pn),nm in pin_net.items():expected[nm].append([ref,pn])
(REPORT/'expected-nets.json').write_text(json.dumps(expected,indent=2))
(REPORT/'build.json').write_text(json.dumps({'components':len(fplist),'nets':len(nets),'sheets':len(pages)+1,'tracks':0,'status':'Unrouted development placement; not fabrication ready','issues':issues},indent=2))
print('Built',len(fplist),'components,',len(nets),'nets,',len(pages)+1,'schematic pages in',OUT)
