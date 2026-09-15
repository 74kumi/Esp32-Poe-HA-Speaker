from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevC');b=p.LoadBoard(str(D/'PoE-Speaker-RevC.kicad_pcb'))
net=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='GND')
z=p.ZONE(b);z.SetLayer(p.In1_Cu);z.SetNet(net);z.SetLocalClearance(300000);z.SetThermalReliefGap(300000);z.SetThermalReliefSpokeWidth(300000)
o=z.Outline();o.NewOutline()
for x,y in [(140,51),(279,51),(279,149),(140,149)]:o.Append(round(x*1e6),round(y*1e6))
b.Add(z);f=p.ZONE_FILLER(b);f.Fill(b.Zones());p.SaveBoard(str(D/'PoE-Speaker-RevC.kicad_pcb'),b)
print('Added conservative secondary-only inner ground zone, x=140..279 mm. Ethernet region remains outside this plane.')
