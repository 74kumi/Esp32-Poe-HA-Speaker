"""Move the long 24V supply run around the eFuse sense via, then widen it."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
old=next(t for t in ts if str(t.m_Uuid.AsString())=='cbae4123-56c5-47cf-aea8-f275e9e752f2')
points=[p.ToMM(old.GetStart()),(205.1493,81.5),(253.2101,81.5),p.ToMM(old.GetEnd())]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(1));b.Add(t)
b.Remove(old);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
