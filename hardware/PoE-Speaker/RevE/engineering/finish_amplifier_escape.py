import pcbnew as p,json,subprocess
from pathlib import Path
base=Path('KiCad-RevB/reports/before-amplifier-escape.kicad_pcb')
for x in [211.8,212.0,212.2]:
 b=p.LoadBoard(str(base));net=next(n for n in b.GetNetsByNetcode().values() if n.GetNetname()=='AMP_SW_POS')
 def v(x,y):return p.VECTOR2I(round(x*1e6),round(y*1e6))
 for a,z,l in [((211.80365,109.375),(x,109.375),p.F_Cu),((x,109.375),(211.598,109.375),p.B_Cu)]:
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*z));t.SetWidth(200000);t.SetLayer(l);t.SetNet(net);b.Add(t)
 t=p.PCB_VIA(b);t.SetPosition(v(x,109.375));t.SetWidth(500000);t.SetDrill(300000);t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(net);b.Add(t)
 path='KiCad-RevB/reports/amp-trial.kicad_pcb';p.SaveBoard(path,b)
 subprocess.run([r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe','pcb','drc','--format','json','--output','KiCad-RevB/reports/amp-trial.json',path],capture_output=True)
 d=json.loads(Path('KiCad-RevB/reports/amp-trial.json').read_text());bad=[a for a in d['violations'] if a['type'] in ['clearance','shorting_items','tracks_crossing']]
 print(x,len(bad),len(d['unconnected_items']),flush=True)
 if not bad and not d['unconnected_items']:
  p.SaveBoard('KiCad-RevB/PoE-Speaker-RevB.kicad_pcb',b);break
else:
 import shutil;shutil.copy2(base,'KiCad-RevB/PoE-Speaker-RevB.kicad_pcb')

