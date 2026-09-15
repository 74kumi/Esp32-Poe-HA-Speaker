from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));pos=p.VECTOR2I(p.FromMM(209.88),p.FromMM(112.453))
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.25));assert not box.Contains(pos),(f.GetReference(),pad.GetNumber())
v=p.PCB_VIA(b);v.SetPosition(pos);v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)

