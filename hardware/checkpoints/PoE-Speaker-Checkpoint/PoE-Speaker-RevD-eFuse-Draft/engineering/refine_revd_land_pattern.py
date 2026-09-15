"""Use the LTC4365 TS8 recommended land dimensions, preserving pad numbering."""
import pcbnew as p,json
from pathlib import Path
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb';b=p.LoadBoard(str(path))
f=next(f for f in b.GetFootprints() if f.GetReference()=='U15');center=f.GetPosition()
assert f.GetOrientationDegrees()==0
for pad in f.Pads():
 old=pad.GetPosition();pad.SetSize(p.VECTOR2I(1220000,400000))
 pad.SetPosition(p.VECTOR2I(center.x+(-1310000 if old.x<center.x else 1310000),old.y))
p.FootprintSave(str(D/'SpeakerRevB.pretty'),f)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
(D/'reports/land-pattern-review.json').write_text(json.dumps({'U15':{'source':'LTC4365 TS8 drawing 05-08-1637 Rev A; datasheet Rev B page 18','pad_mm':[1.22,.4],'row_centers_mm':2.62,'pitch_mm':.65,'pad_gap_mm':.25,'note':'Matches recommended solder-pad layout; previous generic pads were wider and shorter.'},'thermal_drills':{'U2':12,'U16':9,'diameter_mm':.2,'status':'Retained pending documented fabrication/assembly process. Not enlarged merely to satisfy generic 0.3 mm rule.'}},indent=2))
print('Updated U15 PCB and local footprint library to the TS8 recommended land dimensions')
