from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
old=next(t for t in ts if str(t.m_Uuid.AsString())=='a210d4e1-9e19-4c89-8df1-290267f57565')
points=[p.ToMM(old.GetStart()),(200,100),(199.6,99.6),(197,99.6),(196.6,100),(169,100),(168.5,100.5),(165.5,100.5),(165,100),p.ToMM(old.GetEnd())]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(1));b.Add(t)
b.Remove(old);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
