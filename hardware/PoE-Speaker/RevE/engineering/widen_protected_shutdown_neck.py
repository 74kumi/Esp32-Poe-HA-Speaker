"""Widen the protected supply around the bench shutdown via."""
import pcbnew as p
b=p.LoadBoard('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');ts=list(b.GetTracks())
for t in ts:
 if t.m_Uuid.AsString()=='6bf2c967-f33f-4e3d-ab9c-46790acf1922':b.Remove(t)
points=[(251.426,100.218),(251.2,100.444),(251.2,106.934),(251.306,107.04)]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(.6));t.SetLayer(p.B_Cu);t.SetNet(b.FindNet('24V_BENCH_PROTECTED'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('KiCad-RevE/power-trial.kicad_pcb',b)
