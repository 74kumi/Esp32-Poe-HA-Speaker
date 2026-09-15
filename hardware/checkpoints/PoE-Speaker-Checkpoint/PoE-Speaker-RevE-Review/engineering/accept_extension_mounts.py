from pathlib import Path
import pcbnew as p,json,shutil
D=Path('KiCad-RevE');E=Path('engineering');b=p.LoadBoard(str(D/'power-trial.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
for ref in ['H3','H4']:
 pos=fs[ref].GetPosition()
 for f in b.GetFootprints():
  if f.GetReference()==ref:continue
  for pad in f.Pads():
   box=pad.GetBoundingBox();box.Inflate(p.FromMM(2.5));assert not box.Contains(pos),(ref,f.GetReference(),pad.GetNumber())
d=json.loads((D/'reports/power-trial-drc.json').read_text());assert not d['violations'] and not d['unconnected_items'];backup=D/'before-extension-mounts.kicad_pcb';assert not backup.exists();shutil.copy2(D/'PoE-Speaker-RevE.kicad_pcb',backup);shutil.copy2(D/'power-trial.kicad_pcb',D/'PoE-Speaker-RevE.kicad_pcb');f=E/'revision-e-design.json';m=json.loads(f.read_text());m['components']['H3']['position']=[275.,55.];m['components']['H4']['position']=[275.,145.];f.write_text(json.dumps(m,indent=2)+'\n');f=D/'reports/extension-mounting-review.json';r=json.loads(f.read_text());r.update(status='accepted',pad_keepout_check='No other component pad bounding box within 2.5 mm of each mounting center',drc_findings=0,unconnected_items=0);f.write_text(json.dumps(r,indent=2))
with (E/'REVE-TRUNK-ROUTING.md').open('a',encoding='utf-8') as f:f.write('\n\n## Accepted extension mounting support — 2026-09-14\n\nMoved existing right mounting holes H3/H4 from x=225 to x=275 at y=55/145. The mounting centers are now 5 mm from the extended right board edge, matching left-side edge offsets. Retained M2 footprints; use insulating standoffs. No other component pad bounding boxes within 2.5 mm of these centers. DRC zero and no unconnected items. Placement model synchronized; schematic connections unchanged. Backup before-extension-mounts.kicad_pcb. Enclosure, heatsink and module support remain separate mechanical checks.\n')
