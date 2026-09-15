"""Move the remaining long fused bench segment into the existing wide lane."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
for t in ts:
 if t.m_Uuid.AsString() in {'239e0d29-fd1c-4d59-bd74-cabbd244cd22','7e850267-ac0f-4dda-9778-2a9aed3ad394'}:b.Remove(t)
for a,z,w in [((199.073,104.835),(199.073,105.6),.2),((199.073,105.6),(215.5,105.6),1.0)]:
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(w));t.SetLayer(p.In2_Cu);t.SetNet(b.FindNet('BENCH_FUSED'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
