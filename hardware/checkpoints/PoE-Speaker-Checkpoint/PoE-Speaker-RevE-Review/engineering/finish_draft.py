"""Import a local routing trial and report what is actually complete."""
import pcbnew as p,json,collections,sys,shutil,re
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
D=BASE/'KiCad-RevB';path=D/'PoE-Speaker-RevB.kicad_pcb'
session=sys.argv[1] if len(sys.argv)>1 else 'draft.ses'
shutil.copy2(path,D/'reports/before-routing-import.kicad_pcb')
raw=path.read_text(encoding='utf-8')
spans=[]
for match in re.finditer(r'\n\t\((?:segment|via)\s',raw):
    start=match.start();i=raw.index('(',start);depth=0
    for end in range(i,len(raw)):
        if raw[end]=='(':depth+=1
        elif raw[end]==')':
            depth-=1
            if depth==0:spans.append((start,end+1));break
for start,end in reversed(spans):raw=raw[:start]+raw[end:]
clean=D/'reports/import-placement.kicad_pcb';clean.write_text(raw,encoding='utf-8')
b=p.LoadBoard(str(clean))
assert len(list(b.GetTracks()))==0
assert p.ImportSpecctraSES(b,str(D/'reports'/session))
for f in b.GetFootprints():
    f.Reference().SetTextSize(p.VECTOR2I(1000000,1000000))
    f.Reference().SetTextThickness(150000)
p.SaveBoard(str(path),b)
report={'status':'First routed board draft; not for fabrication','footprints':len(list(b.GetFootprints())),
 'track_segments':sum(not isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'vias':sum(isinstance(t,p.PCB_VIA) for t in b.GetTracks()),
 'routing_session':session,
 'signal_layers_used':sorted({b.GetLayerName(t.GetLayer()) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA)}),
 'layers':'Four-layer board; inner ground plane not yet implemented',
 'limitations':['Draft routing uses 0.2 mm default width, including power nets; high-current routing must be redesigned before manufacture.',
 'Ethernet pairs are not impedance or length qualified.',
 'No isolation-clearance qualification, planes, or thermal design approval.',
 'Power-protection review remains open; see engineering/POWER-REVIEW.md.',
 'Read board-drc.json for remaining physical errors and incomplete connections.']}
(D/'reports/first-board-draft.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
