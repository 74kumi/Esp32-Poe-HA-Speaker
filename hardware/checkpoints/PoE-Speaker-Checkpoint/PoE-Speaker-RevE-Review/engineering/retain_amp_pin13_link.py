from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'power-trial.kicad_pcb'));ts=list(b.GetTracks())
for t in ts:
 if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND' and t.GetPosition()==p.VECTOR2I(p.FromMM(205.203),p.FromMM(106.125)):b.Remove(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
