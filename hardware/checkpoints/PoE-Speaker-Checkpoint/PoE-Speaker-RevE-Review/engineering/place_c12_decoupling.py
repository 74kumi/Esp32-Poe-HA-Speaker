"""Trial the upper amplifier supply decoupler near PVCC pins 31/32."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
f=fs['C12'];f.SetPosition(p.VECTOR2I(p.FromMM(207.4),p.FromMM(104.0)));f.Flip(f.GetPosition(),False);f.SetOrientation(p.EDA_ANGLE(90,p.DEGREES_T));f.Reference().SetPosition(f.GetPosition());f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
def route(net,points,width,layer=p.F_Cu):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(width));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t)
route('24V_AMP',[(211.80365,106.125001),(207,106.125001),(207,107)],.6)
route('24V_AMP',[(207.4,105.475),(207,105.875),(207,107)],.8,p.B_Cu)
route('GND',[(207.4,102.525),(207.4,101.0)],.8,p.B_Cu)
for xy,net in [((207.4,101.0),'GND')]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(*[p.FromMM(x) for x in xy]));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v)
ts=list(b.GetTracks())
for t in ts:
 if t.m_Uuid.AsString()=='04974730-7ba4-454e-861a-c7418105572a':b.Remove(t)
route('AMP_SDZ',[(208.1348,111.0766),(208.1348,108.5),(209.25,107.3848),(209.25,100.3),(208.1348,99.1848),(208.1348,79.0939)],.2,p.B_Cu)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
