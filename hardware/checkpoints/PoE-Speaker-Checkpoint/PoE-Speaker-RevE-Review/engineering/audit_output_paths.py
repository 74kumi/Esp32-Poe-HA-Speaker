"""Screen loaded amplifier/output-filter paths using direct copper adjacency."""
from pathlib import Path
import runpy,json
c=runpy.run_path('engineering/audit_supply_paths.py')
pairs=[(('U5','21'),('L2','1')),(('U5','23'),('L2','1')),(('U5','27'),('L1','1')),(('U5','29'),('L1','1')),(('L1','2'),('J3','1')),(('L2','2'),('J3','2'))]
rows=[c['trace'](a,z) for a,z in pairs]
for r in rows:
 r['whole_segment_length_mm']=round(sum(x['length_mm'] for x in r['path'] if x['kind']=='track'),3)
 r['via_count']=sum(x['kind']=='via' for x in r['path'])
Path('KiCad-RevE/reports/output-path-audit.json').write_text(json.dumps({'method':'Direct KiCad track/pad adjacency, widest path then whole-segment length. Pads and vias are excluded from minimum-width metric. This does not establish ampacity, switching-loop inductance, current sharing or thermal performance.','paths':rows},indent=2))
print([(r['source'],r['load'],r['widest_path_min_track_mm'],r['narrow_track_length_mm']) for r in rows])
