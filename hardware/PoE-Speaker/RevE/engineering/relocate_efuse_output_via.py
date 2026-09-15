"""Move the eFuse output transition away from its PGTH trace, then enlarge it."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());v=next(x for x in ts if x.m_Uuid.AsString()=='b983fee9-a187-486f-966c-0b0f0547dc19');old=v.GetPosition();new=p.VECTOR2I(old.x,old.y-p.FromMM(.08))
for t in ts:
 if isinstance(t,p.PCB_VIA):continue
 if t.GetNetCode()==v.GetNetCode() and t.GetLayer()!=p.In2_Cu:
  if t.GetStart()==old:t.SetStart(new)
  if t.GetEnd()==old:t.SetEnd(new)
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.3));assert not box.Contains(new),(f.GetReference(),pad.GetNumber())
t=p.PCB_TRACK(b);t.SetStart(old);t.SetEnd(new);t.SetWidth(p.FromMM(.6));t.SetLayer(p.In2_Cu);t.SetNet(v.GetNet());b.Add(t)
v.SetPosition(new);v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)


