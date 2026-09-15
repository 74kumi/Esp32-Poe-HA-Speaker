import json,pcbnew as p
from pathlib import Path
mp=Path('engineering/revision-e-design.json');m=json.loads(mp.read_text());cs=m['components'];path=Path('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');b=p.LoadBoard(str(path))
for ref,code,url,note in [
 ('U1','Ag5800','https://www.silvertel.com/images/datasheets/Ag5800-datasheet-%20IEEE802_3bt-Power-over-Ethernet-4-pair-PD.pdf','Complete code in Table 1; outputs in series for 24V; not Ag5824'),
 ('U5','TPA3116D2DADR','https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf','DAD0032A top thermal pad; existing 32-lead 0.65mm pitch footprint; external top heatsink required'),
 ('U9','LM5050MK-2/NOPB','https://www.ti.com/lit/gpn/LM5050-2','DDC 6-lead thin SOT23; 0.95mm pitch'),
 ('U10','LM5050MK-2/NOPB','https://www.ti.com/lit/gpn/LM5050-2','DDC 6-lead thin SOT23; 0.95mm pitch')]:
  cs[ref]['properties'].update({'Manufacturer Part Number':code,'Datasheet':url,'Order code review':note})
cs['U8']['properties']['Manufacturer Part Number']='RT9013-33GB';cs['U8']['value']='RT9013-33GB'
changes=[]
for f in b.GetFootprints():
 pads=list(f.Pads());attrs=f.GetAttributes()
 if pads and all(x.GetAttribute()==p.PAD_ATTRIB_SMD for x in pads):
  f.SetAttributes((attrs & ~p.FP_THROUGH_HOLE)|p.FP_SMD)
  if attrs!=f.GetAttributes():changes.append(f.GetReference())
  p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(path.parent/'SpeakerRevB.pretty'),f)
mp.write_text(json.dumps(m,indent=2));p.SaveBoard(str(path),b)
(path.parent/'reports/assembly-metadata.json').write_text(json.dumps({'corrected_smd_attributes':changes,'note':'Classified from actual pad attributes; no pad geometry changed'},indent=2))
print('Corrected SMD classification:',len(changes))
