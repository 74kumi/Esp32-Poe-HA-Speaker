"""Trial local U5 ground access: pin 1 via and pin 13 link to existing C11 ground via."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));pos=p.VECTOR2I(p.FromMM(205.203),p.FromMM(106.125))
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.25));assert not box.Contains(pos),(f.GetReference(),pad.GetNumber())
v=p.PCB_VIA(b);v.SetPosition(pos);v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
pts=[(204.19635,113.925),(205.025,113.925),(205.2,114.1)]
for a,z in zip(pts,pts[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(.35));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('GND'));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
