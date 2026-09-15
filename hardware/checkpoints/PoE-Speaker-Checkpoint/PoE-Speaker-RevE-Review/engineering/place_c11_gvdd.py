"""Trial local bottom-side C11 bypass; main board is unchanged."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE'); b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb')); fs={f.GetReference():f for f in b.GetFootprints()}
f=fs['C11']; f.Flip(f.GetPosition(),False); f.SetPosition(p.VECTOR2I(p.FromMM(204.9),p.FromMM(111.5))); f.SetOrientation(p.EDA_ANGLE(270,p.DEGREES_T)); f.Reference().SetPosition(p.VECTOR2I(p.FromMM(204.9),p.FromMM(114.9)))
print([(x.GetNumber(),p.ToMM(x.GetPosition().x),p.ToMM(x.GetPosition().y)) for x in f.Pads()])
def route(net,points):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b); t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a])); t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z])); t.SetWidth(p.FromMM(.2)); t.SetLayer(p.B_Cu); t.SetNet(b.FindNet(net)); b.Add(t)
route('AMP_GVDD',[(205.583,110.37),(204.9,110.725)])
route('GND',[(204.9,112.275),(204.75,112.425),(204.75,113.65),(205.2,114.1)])
v=p.PCB_VIA(b); v.SetPosition(p.VECTOR2I(p.FromMM(205.2),p.FromMM(114.1))); v.SetWidth(p.FromMM(.5)); v.SetDrill(p.FromMM(.3)); v.SetViaType(p.VIATYPE_THROUGH); v.SetLayerPair(p.F_Cu,p.B_Cu); v.SetNet(b.FindNet('GND')); b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones()); p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)


