"""Trial spreading the two long bench-power routes into wider lanes."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts}
routes={
 '4e87eb2a-85b5-4964-8790-a34f91de5080':[(247.14,104.385),(246.055,103.3),(215.5,103.3),(214.415,104.385),(196.855,104.385)],
 '40867b5a-e40e-4329-b8d1-3ba2b0e218cd':[(240.882,104.835),(240.117,105.6),(215.5,105.6),(214.735,104.835),(199.073,104.835)]}
for key,points in routes.items():
 old=lookup[key]
 for i,(a,z) in enumerate(zip(points,points[1:])):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(1 if i<2 else .2));b.Add(t)
 b.Remove(old)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
