"""Trial an inner-layer detour around the amplifier control vias."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());removed=[]
for t in ts:
 if isinstance(t,p.PCB_VIA) or t.GetNetname()!='24V_AMP' or t.GetLayer()!=p.B_Cu:continue
 if p.ToMM(t.GetStart()) in [(203.5827,106.4),(203.5827,107.865)] and p.ToMM(t.GetWidth())==.2:removed.append(t)
assert len(removed)==2
net=b.FindNet('24V_AMP');points=[(203.5827,106.4),(201.2,106.4),(201.2,109.0477),(201.8,109.6477)]
for a,z in zip(points,points[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.In2_Cu);t.SetNet(net);t.SetWidth(p.FromMM(1));b.Add(t)
for x,y in [points[0],points[-1]]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
for t in removed:b.Remove(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
