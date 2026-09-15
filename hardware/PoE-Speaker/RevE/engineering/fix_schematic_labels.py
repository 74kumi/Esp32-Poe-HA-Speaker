from pathlib import Path
import re
D=Path('KiCad-RevC')
for f in D.glob('*.kicad_sch'):
 s=f.read_text();count=[0]
 def change(m):
  t=m[0];t=re.sub(r'(\(at\s+[-\d.]+\s+[-\d.]+\s+)(0|180)(\))',lambda x:x[1]+('180' if x[2]=='0' else '0')+x[3],t,count=1)
  t=t.replace('(justify left)','(justify TEMP)').replace('(justify right)','(justify left)').replace('(justify TEMP)','(justify right)');count[0]+=1;return t
 s=re.sub(r'\(global_label\s+"[^"]*".*?\(uuid\s+[^)]+\)\)',change,s)
 s=s.replace('Rev B circuit draft','Rev C circuit draft');f.write_text(s)
print('Turned net labels outward from pin blocks.')
