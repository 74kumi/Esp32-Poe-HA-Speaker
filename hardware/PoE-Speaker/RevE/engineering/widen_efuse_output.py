"""Give both eFuse output pins short escapes into a wider shared supply route."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts};net=b.FindNet('24V_AMP')
for key,w in {'b0c486b9-392d-41b5-b512-8caab36531f3':.3,'b92f532f-e205-4dab-82ec-a7db57fdcd1d':.8,'935174f7-c4af-47fc-9721-e4f7c2b61b78':.8,'65f8d083-e1e9-44df-b012-8034f8c17810':.8}.items():lookup[key].SetWidth(p.FromMM(w))
routes=[([(253.9625,75.75),(254.7,75.75),(255.8,75.75)],[.3,.8]), ([(253.9625,76.25),(254.3,76.25),(254.3,75.75)],[.3,.3])]
for points,widths in routes:
 for a,z,w in zip(points,points[1:],widths):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.F_Cu);t.SetNet(net);t.SetWidth(p.FromMM(w));b.Add(t)
b.Remove(lookup['a2b597a5-5a08-4fe1-b74c-6fae102aa5f2']);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)

