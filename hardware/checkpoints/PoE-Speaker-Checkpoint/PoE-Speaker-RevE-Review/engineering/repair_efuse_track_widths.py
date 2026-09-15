"""Widen sub-minimum tracks when existing copper permits; retain blocked escapes."""
from pathlib import Path
import pcbnew as p,json,subprocess,shutil
D=Path('KiCad-RevD');path=D/'PoE-Speaker-RevD.kicad_pcb'
shutil.copy2(path,D/'reports/before-minimum-widths.kicad_pcb')
b=p.LoadBoard(str(path));changed={};blocked=[]
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA) and t.GetWidth()<200000:
  changed[t.m_Uuid.AsString()]={'old_width':t.GetWidth(),'net':t.GetNetname()};t.SetWidth(200000)
for iteration in range(8):
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 subprocess.run([r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe','pcb','drc','--format','json','--output',str(D/'reports/board-drc.json'),str(path)],capture_output=True,check=True)
 d=json.loads((D/'reports/board-drc.json').read_text())
 bad={i['uuid'] for v in d['violations'] if v['type'] in ['clearance','shorting_items','tracks_crossing','edge_clearance','hole_clearance'] for i in v['items']}&set(changed)
 if not bad:break
 for t in b.GetTracks():
  uid=t.m_Uuid.AsString()
  if uid in bad:
   info=changed.pop(uid);t.SetWidth(info['old_width']);blocked.append({'uuid':uid,**info})
else:raise RuntimeError('Width repair not converged')
(D/'reports/minimum-width-repair.json').write_text(json.dumps({'widened_to_mm':.2,'accepted':len(changed),'blocked':blocked,'scope':'Geometric widening only; remaining narrow escapes require rerouting or fabrication-rule review.'},indent=2))
print('Widened',len(changed),'tracks;',len(blocked),'blocked by existing geometry')
