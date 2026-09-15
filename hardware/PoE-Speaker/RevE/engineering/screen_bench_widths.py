"""Try widening loaded bench-path segments; accept only zero-finding trials.

This geometry screen does not establish current capacity. Run on the saved board;
every accepted edit is saved immediately and recorded for review.
"""
from pathlib import Path
import pcbnew as p
import json, subprocess, shutil
D=Path('KiCad-RevE'); main=D/'PoE-Speaker-RevE.kicad_pcb'
trial=D/'power-trial.kicad_pcb'; report=D/'reports/bench-width-screen.json'
cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
backup=D/'reports/before-bench-width-screen.kicad_pcb'
assert not backup.exists(), 'One-time screen already started; inspect its saved results'
shutil.copy2(main,backup)
rows=json.loads((D/'reports/supply-path-audit.json').read_text())['paths'][:2]
targets={v['uuid']:v for row in rows for v in row['narrow_tracks']}
results=[]
for uid,source in targets.items():
 b=p.LoadBoard(str(main)); tracks=list(b.GetTracks()); t=next(x for x in tracks if x.m_Uuid.AsString()==uid)
 t.SetWidth(p.FromMM(.6));p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(trial),b)
 subprocess.run([cli,'pcb','drc','--format','json','-o',str(D/'reports/power-trial-drc.json'),str(trial)],check=True,stdout=subprocess.DEVNULL)
 d=json.loads((D/'reports/power-trial-drc.json').read_text());ok=not d['violations'] and not d['unconnected_items']
 if ok:shutil.copy2(trial,main)
 results.append(dict(source,trial_width_mm=.6,accepted=ok,findings=[{'type':v['type'],'description':v['description']} for v in d['violations']]))
 report.write_text(json.dumps(results,indent=2));print(uid,'accepted' if ok else 'blocked',len(d['violations']),flush=True)
print('Accepted',sum(r['accepted'] for r in results),'of',len(results),flush=True)
