"""Trial widening the protected positive supply down the board."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());old=next(t for t in ts if str(t.m_Uuid.AsString())=='b75c3a29-9cd4-467f-ae80-d2c93a8e3d9b')
points=[(195.253,108.953),(195.253,114),(195.45,114.197),(195.45,118.5),(195.253,118.697),(195.253,135.196)]
for a,z,w in zip(points,points[1:],[1,.7,.7,.7,1]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(w));b.Add(t)
b.Remove(old);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
