"""Place readable references outside solderable pads and other silkscreen shapes."""
from pathlib import Path
import pcbnew as p,json,math
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb';b=p.LoadBoard(str(path))
def box(item,pad=0):
 r=item.GetBoundingBox();return (r.GetX()/1e6-pad,r.GetY()/1e6-pad,r.GetRight()/1e6+pad,r.GetBottom()/1e6+pad)
def overlap(a,z):return a[0]<z[2] and a[2]>z[0] and a[1]<z[3] and a[3]>z[1]
obstacles=[]
for f in b.GetFootprints():
 for a in f.Pads():obstacles.append(box(a,.25))
 for a in f.GraphicalItems():
  if a.GetLayer()==p.F_SilkS:obstacles.append(box(a,.15))
placed=[];unresolved=[];moved=0
for f in sorted(b.GetFootprints(),key=lambda f:(-len(f.GetReference()),f.GetReference())):
 t=f.Reference();t.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));t.SetTextSize(p.VECTOR2I(1000000,1000000));t.SetTextThickness(150000)
 origin=f.GetPosition();best=None
 candidates=[(0,-4),(0,4),(-4,0),(4,0)]+[(rad*math.cos(k*math.pi/8),rad*math.sin(k*math.pi/8)) for rad in [3,5,6,7,8,10] for k in range(16)]
 for dx,dy in candidates:
  t.SetPosition(p.VECTOR2I(origin.x+round(dx*1e6),origin.y+round(dy*1e6)));a=box(t,.12)
  if a[0]<70.5 or a[1]<50.5 or a[2]>279.5 or a[3]>149.5:continue
  hits=sum(overlap(a,z) for z in obstacles+placed)
  score=(hits,math.hypot(dx,dy))
  if best is None or score<best[0]:best=(score,t.GetPosition(),a)
  if hits==0:break
 if best:
  t.SetPosition(best[1]);placed.append(best[2]);moved+=1
  if best[0][0]:unresolved.append(f.GetReference())
 else:unresolved.append(f.GetReference())
p.SaveBoard(str(path),b)
(D/'reports/reference-placement.json').write_text(json.dumps({'processed':moved,'references_with_remaining_bbox_conflicts':unresolved,'scope':'Reference positions only; actual silk DRC remains authoritative'},indent=2));print(moved,'references processed;',len(unresolved),'bbox conflicts')
