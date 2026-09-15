"""Trial inner-layer escape for the last draft soft-start connection."""
import pcbnew as p
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'KiCad-RevB'
b=p.LoadBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'))
V=lambda x,y:p.VECTOR2I(round(x*1e6),round(y*1e6))
net=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='BUCK3V3_SS')
def track(a,z,layer):
 t=p.PCB_TRACK(b);t.SetStart(V(*a));t.SetEnd(V(*z));t.SetWidth(200000);t.SetLayer(layer);t.SetNet(net);b.Add(t)
track((199.5,98.75),(200.6,98.75),p.F_Cu)
v=p.PCB_VIA(b);v.SetPosition(V(200.6,98.75));v.SetWidth(600000);v.SetDrill(300000);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
track((200.6,98.75),(200.6,94),p.In2_Cu)
track((200.6,94),(199.3224,92.7224),p.In2_Cu)
track((199.3224,92.7224),(193.7285,92.7224),p.In2_Cu)
p.SaveBoard(str(D/'reports/softstart-trial.kicad_pcb'),b)
