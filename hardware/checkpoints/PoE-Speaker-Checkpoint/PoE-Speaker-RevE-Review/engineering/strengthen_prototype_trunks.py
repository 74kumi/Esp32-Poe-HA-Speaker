"""Widen long power tracks where existing clearance permits; no rule relaxation."""
from pathlib import Path
import pcbnew as p,json,subprocess
D=Path('KiCad-RevE');path=D/'PoE-Speaker-RevE.kicad_pcb';backup=D/'reports/before-power-widths.kicad_pcb';backup.write_bytes(path.read_bytes())
b=p.LoadBoard(str(path));changes={};nets={'24V_AMP','24V_OR','24V_BENCH_PROTECTED','BENCH_FUSED','5V','3V3','BUCK5_SW','BUCK3V3_SW'}
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA) or t.GetNetname() not in nets:continue
 if p.ToMM(t.GetWidth())<.8 and p.ToMM(t.GetLength())>=2:
  changes[str(t.m_Uuid.AsString())]={'old_width':t.GetWidth(),'net':t.GetNetname(),'length_mm':p.ToMM(t.GetLength())};t.SetWidth(p.FromMM(.8))
rejected=[]
for attempt in range(4):
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 subprocess.run([r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe','pcb','drc','--format','json','-o',str(D/'reports/board-drc.json'),str(path)],check=True,stdout=subprocess.DEVNULL)
 d=json.loads((D/'reports/board-drc.json').read_text())
 if not d['violations'] and not d['unconnected_items']:break
 ids={i['uuid'] for v in d['violations']+d['unconnected_items'] for i in v['items']} & set(changes)
 if not ids:raise RuntimeError('Unexpected finding; restore before-power-widths checkpoint')
 for t in b.GetTracks():
  key=str(t.m_Uuid.AsString())
  if key in ids:t.SetWidth(changes[key]['old_width']);rejected.append(key)
 for key in ids:del changes[key]
else:raise RuntimeError('Widening did not converge')
(D/'reports/power-width-improvements.json').write_text(json.dumps({'accepted':changes,'rejected_count':len(rejected),'status':'Clearance-checked geometric improvement; vias, remaining necks and current/thermal capacity still need review'},indent=2))
print('Widened',len(changes),'segments,',round(sum(c['length_mm'] for c in changes.values()),1),'mm total; rejected',len(rejected),'conflicting segments')
