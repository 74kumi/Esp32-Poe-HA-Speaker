from pathlib import Path
import pcbnew as p,json,subprocess,shutil
D=Path('KiCad-RevC');path=D/'PoE-Speaker-RevC.kicad_pcb';shutil.copy2(path,D/'reports/before-protection-widths.kicad_pcb')
b=p.LoadBoard(str(path));changed={}
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA) and t.GetNetname() in ['BENCH_FUSED','BENCH_COMMON_SOURCE','24V_BENCH_PROTECTED'] and t.GetLength()>2000000 and t.GetWidth()<800000:
  changed[t.m_Uuid.AsString()]=t.GetWidth();t.SetWidth(800000)
for iteration in range(4):
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 subprocess.run([r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe','pcb','drc','--format','json','--output',str(D/'reports/board-drc.json'),str(path)],capture_output=True,check=True)
 d=json.loads((D/'reports/board-drc.json').read_text());bad={i['uuid'] for v in d['violations'] if v['type'] in ['clearance','shorting_items','tracks_crossing'] for i in v['items']}&set(changed)
 if not bad:break
 for t in b.GetTracks():
  if t.m_Uuid.AsString() in bad:t.SetWidth(changed.pop(t.m_Uuid.AsString()))
else:raise RuntimeError('Width review not converged')
(D/'reports/protection-widths.json').write_text(json.dumps({'widened_to_mm':.8,'accepted_segments':len(changed),'scope':'Longer new bench-power segments only. Pin escapes, vias, thermal/current capacity still unqualified.'},indent=2));print('Accepted',len(changed),'widened power segments; unconnected:',len(d['unconnected_items']))
