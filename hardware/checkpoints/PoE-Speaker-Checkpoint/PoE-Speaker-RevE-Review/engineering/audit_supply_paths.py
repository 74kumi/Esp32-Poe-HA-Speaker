"""Trace actual copper adjacency; rank paths by their narrowest track.

This is a topology/width screen, not an ampacity or voltage-drop solver.
"""
from pathlib import Path
import pcbnew as p,json,heapq,math
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));conn=b.GetConnectivity()
fs={f.GetReference():f for f in b.GetFootprints()};items=list(b.GetTracks())+[x for f in fs.values() for x in f.Pads()]
def key(x):return str(x.m_Uuid.AsString())
lookup={key(x):x for x in items};adj={}
def neighbors(k):
 if k not in adj:
  x=lookup[k];adj[k]={key(y) for y in list(conn.GetConnectedTracks(x))+list(conn.GetConnectedPads(x)) if y.GetNetCode()==x.GetNetCode() and key(y) in lookup}
 return adj[k]
def cap(x):return p.ToMM(x.GetWidth()) if isinstance(x,p.PCB_TRACK) and not isinstance(x,p.PCB_VIA) else math.inf
def length(x):return p.ToMM(x.GetLength()) if isinstance(x,p.PCB_TRACK) and not isinstance(x,p.PCB_VIA) else 0
def describe(x):
 row={'uuid':key(x),'net':x.GetNetname()}
 if isinstance(x,p.PAD):row.update(kind='pad',reference=x.GetParentFootprint().GetReference(),pin=x.GetNumber(),position_mm=p.ToMM(x.GetPosition()))
 elif isinstance(x,p.PCB_VIA):row.update(kind='via',position_mm=p.ToMM(x.GetPosition()),drill_mm=p.ToMM(x.GetDrillValue()))
 else:row.update(kind='track',width_mm=cap(x),length_mm=round(length(x),4),start_mm=p.ToMM(x.GetStart()),end_mm=p.ToMM(x.GetEnd()),layer=b.GetLayerName(x.GetLayer()))
 return row
def trace(source,target):
 starts=[key(x) for x in fs[source[0]].Pads() if x.GetNumber()==source[1]];ends={key(x) for x in fs[target[0]].Pads() if x.GetNumber()==target[1]}
 assert starts and ends
 assert lookup[starts[0]].GetNetCode()==lookup[next(iter(ends))].GetNetCode(),(source,target)
 best={s:(math.inf,0) for s in starts};prev={};queue=[(-math.inf,0,s) for s in starts];heapq.heapify(queue);end=None
 while queue:
  nw,l,k=heapq.heappop(queue);w=-nw
  if best.get(k)!=(w,l):continue
  if k in ends:end=k;break
  for n in neighbors(k):
   score=(min(w,cap(lookup[n])),l+length(lookup[n]));old=best.get(n,(-1,math.inf))
   if score[0]>old[0] or (score[0]==old[0] and score[1]<old[1]):best[n]=score;prev[n]=k;heapq.heappush(queue,(-score[0],score[1],n))
 assert end is not None,('No adjacency path',source,target)
 path=[];k=end
 while True:
  path.append(describe(lookup[k]))
  if k not in prev:break
  k=prev[k]
 path.reverse();narrow=[v for v in path if v['kind']=='track' and v['width_mm']<.5]
 return {'source':'.'.join(source),'load':'.'.join(target),'net':lookup[end].GetNetname(),'widest_path_min_track_mm':best[end][0],'narrow_track_length_mm':round(sum(v['length_mm'] for v in narrow),3),'narrow_tracks':narrow,'path':path}
pairs=[(('F1','2'),('Q3','2')),(('Q4','2'),('Q2','3')),(('U1','9'),('Q1','3')),(('Q1','2'),('U16','1')),(('Q2','2'),('U16','1')),(('U16','17'),('U5','17')),(('U16','18'),('U5','31')),(('U16','17'),('U6','2')),(('L3','2'),('U7','11')),(('L4','2'),('U2','2'))]
rows=[trace(a,z) for a,z in pairs]
(D/'reports/supply-path-audit.json').write_text(json.dumps({'method':'KiCad direct track/pad adjacency; maximize minimum track width, then minimize sum of whole-segment lengths. Vias/pads excluded from width metric; no current sharing, thermal model or return-path analysis. Length is a screening metric, not an exact electrical path length.','paths':rows},indent=2))
print([(r['source'],r['load'],r['widest_path_min_track_mm'],r['narrow_track_length_mm']) for r in rows])
