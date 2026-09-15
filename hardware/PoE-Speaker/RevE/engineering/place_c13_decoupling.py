"""Trial a local lower amplifier supply decoupler; use the main board baseline."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
ts=list(b.GetTracks())
for t in ts:
 if t.m_Uuid.AsString() in {'4475f7c9-7e65-458e-b833-3fd8cbe3120c','c793cffc-9030-47ee-b352-12bb0357def8'}:b.Remove(t)
f=fs['C13'];f.SetPosition(p.VECTOR2I(p.FromMM(213.5),p.FromMM(119)));f.SetOrientation(p.EDA_ANGLE(270,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(213.5),p.FromMM(119)));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
pads={x.GetNumber():x for x in f.Pads()};up={x.GetNumber():x for x in fs['U5'].Pads()}
def route(net,points,width):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(width));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));b.Add(t)
route('24V_AMP',[p.ToMM(up['17'].GetPosition()),(211.80365,117.525),p.ToMM(pads['1'].GetPosition())],.8)
route('GND',[p.ToMM(pads['2'].GetPosition()),(213.5,121.9)],.8)
v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(213.5),p.FromMM(121.9)));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
fs['C7'].Reference().SetPosition(p.VECTOR2I(p.FromMM(222),p.FromMM(102.5)))
route('GND',[(217.454,117.954),(216.3,118.4)],.4)
route('GND',[(209.225,120),(209.225,119.1)],.4)
for xy in [(209.225,119.1),(216.3,118.4)]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(*[p.FromMM(x) for x in xy]));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
