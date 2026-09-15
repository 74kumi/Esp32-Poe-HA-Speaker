"""Move only DRC-flagged reference fields into nearby clear space."""
from pathlib import Path
import pcbnew as p,json,math,re
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb';b=p.LoadBoard(str(path))
d=json.loads((D/'reports/board-drc.json').read_text());refs=set()
for v in d['violations']:
 if v['type'] in ['silk_overlap','silk_over_copper']:
  for i in v['items']:
   match=re.fullmatch('Reference field of (.+)',i['description'])
   if match:refs.add(match[1]);break
def box(item,gap=0):
 r=item.GetBoundingBox();return (r.GetX()/1e6-gap,r.GetY()/1e6-gap,r.GetRight()/1e6+gap,r.GetBottom()/1e6+gap)
def overlap(a,c):return a[0]<c[2] and a[2]>c[0] and a[1]<c[3] and a[3]>c[1]
changed=[]
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 if f.GetReference() not in refs:continue
 obstacles=[]
 for g in b.GetFootprints():
  obstacles.extend(box(pad,.25) for pad in g.Pads())
  obstacles.extend(box(s,.2) for s in g.GraphicalItems() if s.GetLayer()==p.F_SilkS)
  if g.GetReference()!=f.GetReference():obstacles.append(box(g.Reference(),.2))
 t=f.Reference();original=t.GetPosition();origin=f.GetPosition();found=False
 for radius in range(2,22):
  for angle in range(0,360,10):
   t.SetPosition(p.VECTOR2I(origin.x+round(radius*math.cos(math.radians(angle))*1e6),origin.y+round(radius*math.sin(math.radians(angle))*1e6)))
   a=box(t,.15)
   if a[0]<70.5 or a[1]<50.5 or a[2]>279.5 or a[3]>149.5:continue
   if not any(overlap(a,c) for c in obstacles):found=True;break
  if found:break
 if found:changed.append(f.GetReference())
 else:t.SetPosition(original)
p.SaveBoard(str(path),b);(D/'reports/silk-repair.json').write_text(json.dumps({'moved':changed,'unresolved':sorted(refs-set(changed))},indent=2));print(changed)
