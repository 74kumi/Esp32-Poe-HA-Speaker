"""Create a coupled RX trunk and bypass its long PHY-route detour."""
from pathlib import Path
import pcbnew as p,json,hashlib,shutil
D=Path('KiCad-RevE');src=D/'PoE-Speaker-RevE.kicad_pcb';b=p.LoadBoard(str(src));ts=list(b.GetTracks())
ids={'31e7f51d-b35f-4433-ae72-56079566dbdb','e44ea4ee-caec-4518-b79f-957d0853a189','fd3a6089-a6b6-4e13-9bf9-0a6a626d0356'}
removed=[t for t in ts if t.m_Uuid.AsString() in ids];assert len(removed)==3
for t in removed:b.Remove(t)
pts=[(107.99,67.984),(108.617606,68.611606),(118.6,68.611606),(118.787894,68.7995),(119.348,68.7995)]
for a,z in zip(pts,pts[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(.225806));t.SetNet(b.FindNet('ETH_RX_P'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
(D/'reports/rx-coupled-trunk-trial.json').write_text(json.dumps({'main_before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'removed':sorted(ids),'points_mm':pts,'parallel_overlap_x_mm':[110.221,118.6],'parallel_center_spacing_mm':.429006,'parallel_edge_gap_mm':.2032,'width_mm':.225806,'status':'trial; branch discontinuities and return-plane review remain'},indent=2))
