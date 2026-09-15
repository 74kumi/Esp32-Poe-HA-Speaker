"""Carry Rev C routes forward, discarding nets split by the new eFuse."""
import pcbnew as p, shutil, json
from pathlib import Path
D=Path('KiCad-RevD'); path=D/'PoE-Speaker-RevD.kicad_pcb'
b=p.LoadBoard(str(path)); old=p.LoadBoard('KiCad-RevC/PoE-Speaker-RevC.kicad_pcb')
assert not list(b.GetTracks()), 'Run only on a freshly generated D board'
nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()}; count=0
for t in old.GetTracks():
 if t.GetNetname() in {'24V_AMP','AMP_SDZ'}:continue
 x=t.Duplicate();x.SetNet(nets[t.GetNetname()]);b.Add(x);count+=1
refs={f.GetReference():f for f in old.GetFootprints()}
for f in b.GetFootprints():
 if f.GetReference() in refs:
  t=refs[f.GetReference()].Reference();f.Reference().SetPosition(t.GetPosition());f.Reference().SetTextSize(t.GetTextSize());f.Reference().SetTextThickness(t.GetTextThickness())
p.SaveBoard(str(path),b)
shutil.copy2('KiCad-RevC/PoE-Speaker-RevC.kicad_dru',D/'PoE-Speaker-RevD.kicad_dru')
assert p.ExportSpecctraDSN(b,str(D/'reports/efuse.dsn'))
file=D/'reports/efuse.dsn';s=file.read_text();start=s.index('(class kicad_default');depth=0
for end in range(start,len(s)):
 if s[end]=='(':depth+=1
 elif s[end]==')':
  depth-=1
  if depth==0:break
primary=set(json.loads(Path('KiCad-RevB/reports/isolation-review-target.json').read_text())['primary_nets'])
def cls(name,nn):
 return '(class '+name+' '+' '.join('"'+n+'"' for n in sorted(nn))+' (circuit (use_via "Via[0-3]_600:300_um")) (rule (width 200) (clearance 200)))\n'
s=s[:start]+cls('PoEPrimary',primary)+cls('Secondary',set(nets)-primary-{''})+'(class_class (classes PoEPrimary Secondary) (rule (clearance 3000)))'+s[end+1:]
file.write_text(s);print('Preserved',count,'routing items; exported isolation-constrained eFuse input')
