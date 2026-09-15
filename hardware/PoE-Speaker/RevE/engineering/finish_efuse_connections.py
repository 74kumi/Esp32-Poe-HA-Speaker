"""Restore proven local buck supply geometry and add the fault pullup feed."""
from pathlib import Path
import pcbnew as p,shutil
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb';shutil.copy2(path,D/'reports/before-local-repair.kicad_pcb')
b=p.LoadBoard(str(path));old=p.LoadBoard('KiCad-RevC/PoE-Speaker-RevC.kicad_pcb');nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}
count=0
for t in old.GetTracks():
 if t.GetNetname()=='24V_AMP' and all(162<pt.x/1e6<170 and 95<pt.y/1e6<101.4 for pt in [t.GetStart(),t.GetEnd()]):
  x=t.Duplicate();x.SetNet(nets['24V_AMP']);b.Add(x);count+=1
def point(x,y):return p.VECTOR2I(round(x*1e6),round(y*1e6))
def trace(a,c,layer):
 t=p.PCB_TRACK(b);t.SetStart(point(*a));t.SetEnd(point(*c));t.SetWidth(200000);t.SetLayer(layer);t.SetNet(nets['3V3']);b.Add(t)
def via(x,y):
 t=p.PCB_VIA(b);t.SetPosition(point(x,y));t.SetWidth(600000);t.SetDrill(300000);t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(nets['3V3']);b.Add(t)
trace((252.9125,65),(253.9,65),p.F_Cu);via(253.9,65)
trace((253.9,65),(254.2,65.3),p.B_Cu)
trace((254.2,65.3),(254.2,87.2),p.B_Cu)
trace((254.2,87.2),(253.9,87.5),p.B_Cu);via(253.9,87.5)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b);print('Restored',count,'local buck route items and connected fault pullup')
