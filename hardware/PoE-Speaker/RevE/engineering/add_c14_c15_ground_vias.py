"""Trial dedicated ground vias beside C14/C15, outside solder pads."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
for ref in ['C14','C15']:
 pad=next(x for x in fs[ref].Pads() if x.GetNetname()=='GND');a=pad.GetPosition();z=p.VECTOR2I(a.x-p.FromMM(1.1),a.y)
 for f in b.GetFootprints():
  for x in f.Pads():
   box=x.GetBoundingBox();box.Inflate(p.FromMM(.3));assert not box.Contains(z),(ref,f.GetReference(),x.GetNumber())
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.6));t.SetLayer(p.F_Cu);t.SetNet(pad.GetNet());b.Add(t)
 v=p.PCB_VIA(b);v.SetPosition(z);v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(pad.GetNet());b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)

