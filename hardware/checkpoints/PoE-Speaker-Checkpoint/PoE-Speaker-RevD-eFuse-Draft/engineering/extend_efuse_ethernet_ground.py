"""Extend the secondary ground plane under Ethernet, above the PoE primary region."""
from pathlib import Path
import pcbnew as p,shutil,json
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb';backup=D/'reports/before-ethernet-ground.kicad_pcb'
if not backup.exists():shutil.copy2(path,backup)
b=p.LoadBoard(str(path));zones=list(b.Zones());assert len(zones)==1
z=zones[0];assert z.GetNetname()=='GND' and z.GetLayer()==p.In1_Cu
points=[(103,51),(279,51),(279,149),(140,149),(140,86),(103,86)]
o=z.Outline();o.RemoveAllContours();o.NewOutline()
for x,y in points:o.Append(round(x*1e6),round(y*1e6))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
(D/'reports/ethernet-ground-extension.json').write_text(json.dumps({'layer':'In1.Cu','net':'GND','outline_mm':points,'purpose':'Add reference copper under Ethernet and local decoupling while excluding the primary/module region below y=86 mm on the left.','limits':'Preliminary 3 mm clearance rule remains active. This does not establish controlled impedance, uninterrupted return paths for all layers, creepage, or thermal approval.'},indent=2))
print('Extended the existing secondary plane beneath Ethernet')
