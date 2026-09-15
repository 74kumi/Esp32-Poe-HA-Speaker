"""Route the verified 3V3 load feed around the outside of J4's ground pad."""
from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
audit=json.loads((D/'reports/supply-path-audit.json').read_text());row=next(r for r in audit['paths'] if r['source']=='L4.2');ids={t['uuid'] for t in row['narrow_tracks']}
assert len(ids)==6
points=[(173.32,51.9712),(173.32,51.7),(154.5,51.7),(154.5,54.2501),(156,55.7501)]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.In2_Cu);t.SetNet(b.FindNet('3V3'));t.SetWidth(p.FromMM(.8));b.Add(t)
for t in ts:
 if str(t.m_Uuid.AsString()) in ids:b.Remove(t)
boot=next(t for t in ts if str(t.m_Uuid.AsString())=='692c73b7-454d-45bd-b6c5-f9cae6424fb5')
start=p.ToMM(boot.GetStart());end=p.ToMM(boot.GetEnd());points=[start,(start[0]+.6037,50.63),(end[0]-.6037,50.63),end]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(boot.GetLayer());t.SetNet(boot.GetNet());t.SetWidth(boot.GetWidth());b.Add(t)
b.Remove(boot)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
