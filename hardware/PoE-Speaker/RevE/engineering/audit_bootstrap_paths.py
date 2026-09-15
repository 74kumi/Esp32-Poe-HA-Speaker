"""Record amplifier bootstrap routing geometry for the next local layout pass."""
import runpy,json,math
from pathlib import Path
ctx=runpy.run_path('engineering/audit_supply_paths.py')
rows=[]
for cap,bs,out in [('C7','20','21'),('C8','24','23'),('C9','26','27'),('C10','30','29')]:
 legs=[ctx['trace'](('U5',bs),(cap,'1')),ctx['trace'](('U5',out),(cap,'2'))]
 for leg in legs:
  tracks=[x for x in leg['path'] if x['kind']=='track']
  leg['whole_segment_length_mm']=round(sum(x['length_mm'] for x in tracks),3)
  leg['via_count']=sum(x['kind']=='via' for x in leg['path'])
  ends=[x['position_mm'] for x in leg['path'] if x['kind']=='pad']
  leg['endpoint_distance_mm']=round(math.dist(ends[0],ends[-1]),3)
 rows.append({'capacitor':cap,'legs':legs,'combined_whole_segment_length_mm':round(sum(x['whole_segment_length_mm'] for x in legs),3)})
Path('KiCad-RevE/reports/bootstrap-routing-audit.json').write_text(json.dumps({'scope':'Saved main board only. Widest-path topology and sum of whole track lengths; shared segments may extend beyond branch junctions. This is a layout screening metric, not exact loop length, inductance or electrical qualification.','reference':'https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf','capacitors':rows},indent=2))
print([(r['capacitor'],r['combined_whole_segment_length_mm']) for r in rows])
