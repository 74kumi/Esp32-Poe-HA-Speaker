"""Remove only DRC-identified dangling AMP_GVDD/GND copper in the C11 trial."""
from pathlib import Path
import pcbnew as p,json,subprocess
D=Path('KiCad-RevE');board=D/'power-trial.kicad_pcb';report=D/'reports/power-trial-drc.json'
cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe';removed=[]
b=p.LoadBoard(str(board));ts=list(b.GetTracks());lookup={t.m_Uuid.AsString():t for t in ts}
for iteration in range(30):
 subprocess.run([cli,'pcb','drc','--format','json','-o',str(report),str(board)],check=True,stdout=subprocess.DEVNULL)
 d=json.loads(report.read_text());assert not d['unconnected_items']
 if not d['violations']:break
 assert all(v['type'] in ['track_dangling','via_dangling'] for v in d['violations']),d['violations']
 for v in d['violations']:
  for item in v['items']:
   uid=item['uuid'];t=lookup[uid];assert t.GetNetname() in ['AMP_GVDD','GND']
   if uid not in removed:b.Remove(t);removed.append(uid)
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(board),b)
else:raise RuntimeError('Pruning did not converge')
(D/'reports/c11-spur-removal.json').write_text(json.dumps({'removed_uuids':removed,'drc_findings':len(d['violations']),'unconnected_items':len(d['unconnected_items'])},indent=2))
print('Removed',len(removed),'obsolete spur items; final DRC',len(d['violations']))
