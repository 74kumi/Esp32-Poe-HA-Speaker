"""Trial larger barrels on audited power vias; exclude holes near any component pad."""
from pathlib import Path
import json,pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));d=json.loads((D/'reports/supply-path-audit.json').read_text());ids={t['uuid'] for r in d['paths'] for t in r['path'] if t['kind']=='via' and t['drill_mm']<.5};pads=[x for f in b.GetFootprints() for x in f.Pads()];rows=[]
for v in b.GetTracks():
 if not isinstance(v,p.PCB_VIA) or v.m_Uuid.AsString() not in ids:continue
 pos=v.GetPosition();near=[]
 for pad in pads:
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.35))
  if box.Contains(pos):near.append(pad.GetParentFootprint().GetReference()+'.'+pad.GetNumber())
 row={'uuid':v.m_Uuid.AsString(),'net':v.GetNetname(),'position_mm':p.ToMM(pos),'old_diameter_mm':p.ToMM(v.GetWidth(p.F_Cu)),'old_drill_mm':p.ToMM(v.GetDrillValue()),'near_pads':near,'trial':not near};rows.append(row)
 if not near:v.SetWidth(p.FromMM(1));v.SetDrill(p.FromMM(.5))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b);(D/'reports/power-via-review.json').write_text(json.dumps({'method':'Audited load-path vias only. Proposed 1.0 mm copper / 0.5 mm drill; conservatively exclude holes within pad bounding box plus 0.35 mm. Clearance checked separately. No current or thermal rating inferred; plating/stackup pending.','vias':rows},indent=2));print('Trial',sum(r['trial'] for r in rows),'excluded',sum(not r['trial'] for r in rows))
