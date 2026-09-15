"""Widen the loaded 24V path around the 3V3 via without changing either net."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());remove=[]
starts={(198.1005,87.225),(198.1005,89.2249),(199.0976,90.222)}
for t in ts:
 if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='24V_AMP' and t.GetLayer()==p.In2_Cu and p.ToMM(t.GetStart()) in starts:remove.append(t)
assert len(remove)==3
points=[(198.1005,86.425),(197.6,86.9255),(197.6,88.7244),(199.0976,90.222)]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.In2_Cu);t.SetNet(b.FindNet('24V_AMP'));t.SetWidth(p.FromMM(.8));b.Add(t)
for t in remove:b.Remove(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
