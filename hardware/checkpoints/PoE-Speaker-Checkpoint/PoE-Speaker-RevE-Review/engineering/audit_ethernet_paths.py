from pathlib import Path
import json,runpy
c=runpy.run_path('engineering/audit_supply_paths.py');rows=[]
for a,z in [(('U3','1'),('J1','10')),(('U3','2'),('J1','11')),(('U3','5'),('J1','5')),(('U3','6'),('J1','4'))]:
 r=c['trace'](a,z);r['whole_segment_length_mm']=round(sum(x['length_mm'] for x in r['path'] if x['kind']=='track'),3);r['via_count']=sum(x['kind']=='via' for x in r['path']);rows.append(r)
Path('KiCad-RevE/reports/ethernet-path-review.json').write_text(json.dumps({'method':'Widest connected track/pad path then shortest whole-segment sum; includes full tracks overlapping pads. Screening only, not exact differential skew or impedance.','paths':rows},indent=2));print([(r['net'],r['whole_segment_length_mm'],r['via_count']) for r in rows])
