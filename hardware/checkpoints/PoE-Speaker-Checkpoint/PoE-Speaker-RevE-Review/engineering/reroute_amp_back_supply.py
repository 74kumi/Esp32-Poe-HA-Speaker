from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());lookup={str(t.m_Uuid.AsString()):t for t in ts}
routes=[
 (['415ebbf4-25f5-409c-b68d-9c301a13a767'],[(203.5,94.6244),(199.8047,90.9291),(199.0976,90.222)],[1,.3]),
 (['06a33431-7511-4ea3-a8fc-bbdc91c4e608','e933c023-5419-4a22-9b7a-be5e9cc6879e'],[(203.5827,100.0827),(203.5827,106.4),(203.5827,107.865),(201.8,109.6477),(200.086,111.3617)],[1,.2,.2,.6])]
for keys,points,widths in routes:
 old=lookup[keys[0]]
 for a,z,w in zip(points,points[1:],widths):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(old.GetLayer());t.SetNet(old.GetNet());t.SetWidth(p.FromMM(w));b.Add(t)
 for key in keys:b.Remove(lookup[key])
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
