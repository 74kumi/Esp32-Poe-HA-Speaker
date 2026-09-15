"""Replace the router's crossed LDO enable bridge with an inner-layer bridge.
Two via-in-pad locations are explicitly provisional assembly-review items.
"""
from pathlib import Path
import pcbnew as p,re
D=Path(__file__).resolve().parent.parent/'KiCad-RevB';path=D/'PoE-Speaker-RevB.kicad_pcb'
b=p.LoadBoard(str(path));ids=[]
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA) or t.GetNetname()!='5V':continue
 pts=[t.GetStart(),t.GetEnd()]
 if all(170.9<q.x/1e6<172.8 and 74.9<q.y/1e6<76.96 for q in pts) and any(q.y/1e6<76.9 for q in pts):ids.append(t.m_Uuid.AsString())
raw=path.read_text();spans=[]
for mat in re.finditer(r'\n\t\(segment\s',raw):
 start=mat.start();depth=0
 for end in range(raw.index('(',start),len(raw)):
  if raw[end]=='(':depth+=1
  elif raw[end]==')':
   depth-=1
   if depth==0:
    if any(i in raw[start:end+1] for i in ids):spans.append((start,end+1))
    break
for a,z in reversed(spans):raw=raw[:a]+raw[z:]
temp=D/'reports/ldo-bridge-input.kicad_pcb';temp.write_text(raw)
b=p.LoadBoard(str(temp));n=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='5V')
V=lambda x,y:p.VECTOR2I(round(x*1e6),round(y*1e6))
for y in [75.05,76.95]:
 v=p.PCB_VIA(b);v.SetPosition(V(171.9,y));v.SetWidth(600000);v.SetDrill(300000);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(n);b.Add(v)
t=p.PCB_TRACK(b);t.SetStart(V(171.9,75.05));t.SetEnd(V(171.9,76.95));t.SetWidth(200000);t.SetLayer(p.In2_Cu);t.SetNet(n);b.Add(t)
p.SaveBoard(str(path),b);print('Replaced',len(spans),'crossed bridge segments')
