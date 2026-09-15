from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts}
routes={
 '6a48652e-e33e-4fae-8244-327247d7e54f':([(210.2663,116.4059),(209.5722,117.1),(203.075,117.1),(202.3809,116.4059)],[1,1,1]),
 'd18fedca-7e09-4eac-9c8a-2e1d299e739d':([(198.1005,87.225),(198.1005,86.425),(203.6874,80.8381),(204.4874,80.8381)],[.3,1,1])}
for key,(points,widths) in routes.items():
 old=lookup[key]
 for a,z,w in zip(points,points[1:],widths):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(w));b.Add(t)
 b.Remove(old)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
