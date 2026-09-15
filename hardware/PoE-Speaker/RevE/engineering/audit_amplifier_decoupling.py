"""Record supply-side amplifier bypass paths; does not model plane returns."""
from pathlib import Path
import runpy,json
c=runpy.run_path('engineering/audit_supply_paths.py')
pairs=[(('U5','32'),('C12','1')),(('U5','17'),('C13','1')),(('U5','17'),('C14','1')),(('U5','17'),('C15','1')),(('U5','7'),('C11','1')),(('U5','7'),('R15','1'))]
rows=[c['trace'](a,z) for a,z in pairs]
for r in rows:
 r['whole_segment_length_mm']=round(sum(x['length_mm'] for x in r['path'] if x['kind']=='track'),3)
 r['via_count']=sum(x['kind']=='via' for x in r['path'])
Path('KiCad-RevE/reports/amplifier-decoupling-audit.json').write_text(json.dumps({'method':'Direct copper adjacency, maximize minimum track width then minimize whole-segment length. This is not exact loop length, return-plane analysis, inductance or circuit qualification. GVDD also feeds R15, the PLIMIT divider resistor; preserve that branch when relocating C11.','paths':rows},indent=2))
print([(r['source'],r['load'],r['whole_segment_length_mm'],r['via_count']) for r in rows])
