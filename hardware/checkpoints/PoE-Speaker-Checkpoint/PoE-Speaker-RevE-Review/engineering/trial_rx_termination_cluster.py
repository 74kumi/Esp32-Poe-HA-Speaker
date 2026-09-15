"""Unaccepted Ethernet RX termination placement trial; always starts from saved board."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};ts=list(b.GetTracks())
for t in ts:
 if t.GetNetname()=='ETH_RX_TERM':b.Remove(t)
for ref,x,y,ang in [('R104',119.5,71.6622,0),('R105',120.5,69.2,270),('C102',120.5,74.1,270)]:
 f=fs[ref];f.Flip(f.GetPosition(),False);f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));f.SetOrientation(p.EDA_ANGLE(ang,p.DEGREES_T));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(123.5),p.FromMM(y)));print(ref,[(x.GetNumber(),p.ToMM(x.GetPosition())) for x in f.Pads()])
def route(net,pts):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(.2));t.SetLayer(p.B_Cu);t.SetNet(b.FindNet(net));b.Add(t)
route('ETH_RX_P',[(117.5,71.6622),(118.675,71.6622)])
route('ETH_RX_N',[(119.593,68.1826),(120.3076,68.1826),(120.5,68.375)])
route('ETH_RX_TERM',[(120.5,70.025),(120.325,70.2),(120.325,71.6622),(120.325,73.15),(120.5,73.325)])
route('GND',[(120.5,74.875),(121.5,74.875)])
v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(121.5),p.FromMM(74.875)));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)

