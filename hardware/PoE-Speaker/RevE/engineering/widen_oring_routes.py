"""Trial wider ORing supply routes around existing control vias."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts}
routes=[('3cc26ebb-4d59-4e01-ac1b-10e25f1fa24b',[(194.4645,81.7758),(194.4645,82.5758),(194.25,82.7903),(194.25,96.2841),(194.25,97.2841),(194.4645,97.4986)],[.3,1,1,.3,.3]),('8967b4ed-bbe5-4e1a-b198-2b84544e5feb',[(201.7391,126.4573),(202.2,125.9964),(202.2,120.5614),(201.7391,120.1005)],[1,1,1])]
for key,points,widths in routes:
 old=lookup[key]
 for a,z,w in zip(points,points[1:],widths):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(w));b.Add(t)
 b.Remove(old)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)


