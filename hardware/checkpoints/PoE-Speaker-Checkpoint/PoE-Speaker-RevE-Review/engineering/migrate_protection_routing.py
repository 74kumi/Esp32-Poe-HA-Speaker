import pcbnew as p,shutil,json
from pathlib import Path
D=Path('KiCad-RevC');b=p.LoadBoard(str(D/'PoE-Speaker-RevC.kicad_pcb'));old=p.LoadBoard('KiCad-RevB/PoE-Speaker-RevB.kicad_pcb');nets={n.GetNetname():n for n in b.GetNetsByNetcode().values()};count=0
for t in old.GetTracks():
 if t.GetNetname()=='24V_BENCH_PROTECTED':continue
 x=t.Duplicate();x.SetNet(nets[t.GetNetname()]);b.Add(x);count+=1
p.SaveBoard(str(D/'PoE-Speaker-RevC.kicad_pcb'),b)
shutil.copy2('KiCad-RevB/PoE-Speaker-RevB.kicad_dru',D/'PoE-Speaker-RevC.kicad_dru')
print('Preserved route items:',count)
assert p.ExportSpecctraDSN(b,str(D/'reports/protection.dsn'))
