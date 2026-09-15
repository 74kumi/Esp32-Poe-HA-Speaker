"""Move the remaining long protected bench segment into the existing wide lane."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
for t in ts:
 if t.m_Uuid.AsString() in {'c5291573-33f4-49cd-a8b3-3127060a2ee0','abcfc146-f162-4004-af75-3cc525df2238'}:b.Remove(t)
for a,z,w in [((196.855,104.385),(197.2,104.04),.2),((197.2,104.04),(197.2,102.4),.2),((197.2,102.4),(215.5,102.4),1.0),((215.5,102.4),(215.5,103.3),1.0)]:
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(w));t.SetLayer(p.In2_Cu);t.SetNet(b.FindNet('24V_BENCH_PROTECTED'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
