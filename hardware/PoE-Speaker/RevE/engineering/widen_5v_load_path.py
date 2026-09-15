"""Reroute the verified L3-to-U7 load path around two signal/switch vias."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts}
lookup['cb2fe424-0c6f-497e-86c8-22677824b44e'].SetWidth(p.FromMM(.8))
routes={
 '25e17d49-9611-4d9f-96d5-53856756519e':[(173.757,90.4941),(174.1511,90.1),(196.7489,90.1),(197.143,90.4941)],
 '209810c4-e769-4e03-8a05-fffe793d47b4':[(197.143,90.4941),(197.8,90.4941),(202.062,94.7561),(202.062,95.4128)]}
for key,points in routes.items():
 old=lookup[key]
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(.8));b.Add(t)
 b.Remove(old)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
