"""Trial widening the remaining fused supply entry near the ORing FET."""
import pcbnew as p
b=p.LoadBoard('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');ts=list(b.GetTracks())
ids={'9746db39-c072-4b7b-bf02-b28400d17146','66a89fd1-e052-4310-916f-44f7a70a4b6a','64660bc2-fe34-4a02-91bc-d74779fb3a95','cde0e6a5-e18d-404f-82e9-1b91cab4d5a4','02ce300c-cd03-4b12-95ea-8eaf63460eb2'}
for t in ts:
 if t.m_Uuid.AsString() in ids:b.Remove(t)
points=[(189.756,107.024),(189.932,107.2),(197.473,107.2),(199.073,105.6)]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(.6));t.SetLayer(p.In2_Cu);t.SetNet(b.FindNet('BENCH_FUSED'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('KiCad-RevE/power-trial.kicad_pcb',b)
