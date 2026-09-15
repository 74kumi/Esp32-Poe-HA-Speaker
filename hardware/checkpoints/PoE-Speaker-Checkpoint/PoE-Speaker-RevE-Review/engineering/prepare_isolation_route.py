"""Reorient optocouplers and locally rip up their routes for isolation repair."""
import pcbnew as p,json,re,shutil
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'KiCad-RevB';R=D/'reports';path=D/'PoE-Speaker-RevB.kicad_pcb'
shutil.copy2(path,R/'before-isolation-repair.kicad_pcb')
b=p.LoadBoard(str(path));remove=[]
affected={'AT_LED_A','BT3_LED_A','BT4_LED_A','AT_DET_PRIMARY','BT3_DET_PRIMARY','BT4_DET_PRIMARY','POE_AT_DET','POE_BT3_DET','POE_BT4_DET'}
for t in b.GetTracks():
 inside=any(109<pt.x/1e6<123 and 88<pt.y/1e6<111 for pt in [t.GetStart(),t.GetEnd()])
 if t.GetNetname() in affected or t.GetNetname()=='GND' and inside:remove.append(t.m_Uuid.AsString())
raw=path.read_text();spans=[]
def endscope(s,start):
 depth=0
 for i in range(start,len(s)):
  if s[i]=='(':depth+=1
  elif s[i]==')':
   depth-=1
   if depth==0:return i+1
 raise ValueError('Unbalanced scope')
for mat in re.finditer(r'\n\t\((?:segment|via)\s',raw):
 start=mat.start();end=endscope(raw,raw.index('(',start))
 if any(u in raw[start:end] for u in remove):spans.append((start,end))
for start,end in reversed(spans):raw=raw[:start]+raw[end:]
temp=R/'isolation-placement.kicad_pcb';temp.write_text(raw)
b=p.LoadBoard(str(temp))
for f in b.GetFootprints():
 if f.GetReference() in ['U12','U13','U14']:
  f.SetOrientationDegrees(270)
  f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
p.SaveBoard(str(path),b)
dsn=R/'isolation.dsn';assert p.ExportSpecctraDSN(b,str(dsn))
s=dsn.read_text();start=s.index('(class kicad_default');end=endscope(s,start)
primary=set(json.loads((R/'isolation-review-target.json').read_text())['primary_nets'])
allnets={n.GetNetname() for n in b.GetNetsByNetcode().values() if n.GetNetname()}
def cls(name,nets):return '(class '+name+' '+' '.join(json.dumps(n) for n in sorted(nets))+' (circuit (use_via "Via[0-3]_600:300_um")) (rule (width 200) (clearance 200)))\n'
rules=cls('PoEPrimary',primary)+cls('Secondary',allnets-primary)+'(class_class (classes PoEPrimary Secondary) (rule (clearance 3000)))'
s=s[:start]+rules+s[end:];dsn.write_text(s)
(R/'isolation-repair.json').write_text(json.dumps({'rotated':['U12','U13','U14'],'removed_route_items':len(spans),'retained_route_items':len(list(b.GetTracks())),'interclass_target_mm':3,'status':'Routing trial'},indent=2))
print('Rotated three optocouplers; removed',len(spans),'route items; retained',len(list(b.GetTracks())))
