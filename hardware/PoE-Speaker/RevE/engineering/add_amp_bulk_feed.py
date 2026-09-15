"""Trial direct inner-layer bulk-capacitor supply connection."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));net=b.FindNet('24V_AMP')
points=[(203.5,100),(203.5,101.3),(204.7,102.5),(207,102.5),(207,107),(207,116.5),(207,117.1)]
for i,(a,z) in enumerate(zip(points,points[1:])):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.B_Cu if i==4 else p.F_Cu);t.SetNet(net);t.SetWidth(p.FromMM(1));b.Add(t)
v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(207),p.FromMM(107)));v.SetWidth(p.FromMM(1));v.SetDrill(p.FromMM(.5));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(207),p.FromMM(116.5)));v.SetWidth(p.FromMM(1));v.SetDrill(p.FromMM(.5));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
ts=list(b.GetTracks());sv=next(t for t in ts if str(t.m_Uuid.AsString())=='2cfc1fb1-e722-435a-b7c6-c375bc0e3a7f');old=sv.GetPosition();new=p.VECTOR2I(p.FromMM(208.05),p.FromMM(111.6874));sv.SetPosition(new)
for t in ts:
 if isinstance(t,p.PCB_VIA) or t.GetNetname()!='AMP_SDZ':continue
 if t.GetStart()==old:t.SetStart(new)
 if t.GetEnd()==old:t.SetEnd(new)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)




