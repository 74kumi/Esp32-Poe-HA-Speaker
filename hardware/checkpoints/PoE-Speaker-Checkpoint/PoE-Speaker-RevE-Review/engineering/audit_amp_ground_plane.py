"""Shortest direct copper paths from U5 ground pins to filled-plane-contact vias."""
from pathlib import Path
import pcbnew as p,json,heapq
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));c=b.GetConnectivity();ts=list(b.GetTracks());pads=[x for f in b.GetFootprints() for x in f.Pads()];lookup={x.m_Uuid.AsString():x for x in ts+pads};zones=[z for z in b.Zones() if z.GetNetname()=='GND'];rows=[]
def contacts(x):return any(x.IsOnLayer(z.GetLayer()) and z.HitTestFilledArea(z.GetLayer(),x.GetPosition()) for z in zones)
for pad in pads:
 if pad.GetParentFootprint().GetReference()!='U5' or pad.GetNetname()!='GND':continue
 start=pad.m_Uuid.AsString();best={start:0};prev={};q=[(0,start)];end=None
 while q:
  cost,k=heapq.heappop(q)
  if cost!=best[k]:continue
  x=lookup[k]
  if (isinstance(x,p.PCB_VIA) or isinstance(x,p.PAD) and x.GetAttribute()==p.PAD_ATTRIB_PTH) and contacts(x):end=k;break
  for obj in list(c.GetConnectedTracks(x))+list(c.GetConnectedPads(x)):
   uid=obj.m_Uuid.AsString()
   if uid not in lookup:continue
   y=lookup[uid]
   if y.GetNetname()!='GND':continue
   weight=p.ToMM(y.GetLength()) if isinstance(y,p.PCB_TRACK) and not isinstance(y,p.PCB_VIA) else 0
   n=cost+weight
   if n<best.get(uid,float('inf')):best[uid]=n;prev[uid]=k;heapq.heappush(q,(n,uid))
 path=[]
 if end:
  k=end
  while k!=start:
   x=lookup[k];item={'uuid':k}
   if isinstance(x,p.PCB_VIA):item.update(kind='via',position_mm=p.ToMM(x.GetPosition()),drill_mm=p.ToMM(x.GetDrillValue()))
   elif isinstance(x,p.PAD):item.update(kind='pad',reference=x.GetParentFootprint().GetReference(),pin=x.GetNumber())
   else:item.update(kind='track',width_mm=p.ToMM(x.GetWidth()),length_mm=round(p.ToMM(x.GetLength()),4),start_mm=p.ToMM(x.GetStart()),end_mm=p.ToMM(x.GetEnd()),layer=b.GetLayerName(x.GetLayer()))
   path.append(item);k=prev[k]
  path.reverse()
 rows.append({'pin':pad.GetNumber(),'plane_contact_found':end is not None,'whole_segment_length_mm':round(best[end],3) if end else None,'path':path})
r={'method':'Shortest sum of whole track lengths through KiCad direct track/pad adjacency to a GND via or plated pad whose center lies in filled GND copper. Does not establish continuous return-current corridor, impedance or thermal performance. Includes pad bridges and excludes zone traversal.','pins':rows};(D/'reports/amp-ground-plane-paths.json').write_text(json.dumps(r,indent=2));print([(x['pin'],x['plane_contact_found'],x['whole_segment_length_mm']) for x in rows])
