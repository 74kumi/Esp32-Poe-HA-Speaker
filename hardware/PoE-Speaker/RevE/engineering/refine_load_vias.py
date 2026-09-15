from pathlib import Path
import json,pcbnew as p
D=Path('KiCad-RevE');f=D/'reports/power-via-review.json';r=json.loads(f.read_text());d=json.loads((D/'reports/power-trial-drc.json').read_text());assert not d['unconnected_items'];assert all(x['type']=='clearance' for x in d['violations']); rows={x['uuid']:x for x in r['vias']};bad={}
import re
for v in d['violations']:
 gap=float(re.search(r'actual ([0-9.]+) mm',v['description']).group(1))
 for i in v['items']:
  if i['uuid'] in rows:bad[i['uuid']]=min(gap,bad.get(i['uuid'],99))
b=p.LoadBoard(str(D/'power-trial.kicad_pcb'))
for v in b.GetTracks():
 uid=v.m_Uuid.AsString()
 if uid not in rows:continue
 row=rows[uid];dia,drill=(1,.5) if uid not in bad else ((.8,.4) if bad[uid]>=.105 else (row['old_diameter_mm'],row['old_drill_mm']))
 v.SetWidth(p.FromMM(dia));v.SetDrill(p.FromMM(drill));row.update(final_diameter_mm=dia,final_drill_mm=drill,changed=drill!=row['old_drill_mm']);row['reason']='Clearance-compatible candidate' if row['changed'] else 'Retained original due to neighboring copper'
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b);f.write_text(json.dumps(r,indent=2));print('Changed',sum(x['changed'] for x in rows.values()))
