from pathlib import Path
import json
path=Path('engineering/revision-e-design.json');m=json.loads(path.read_text())
types={
 'U6':{'1':'power_in','2':'power_in','3':'passive','4':'passive','5':'power_out','6':'power_in','7':'input','8':'open_collector','9':'input','10':'power_in','11':'power_in','12':'power_out'},
 'U7':{'1':'power_out','2':'passive','3':'passive','4':'open_collector','5':'input','6':'power_in','7':'input','8':'input','9':'input','10':'power_in','11':'power_in','12':'power_in','13':'input','14':'input','15':'power_in','16':'power_in','17':'power_in'}}
for ref,mapping in types.items():
 for pin in m['components'][ref]['pins']:pin['type']=mapping[pin['number']]
 m['components'][ref]['properties']['Pin type review']='TI pin table; duplicate internally common switch pins remain passive to avoid false output contention'
path.write_text(json.dumps(m,indent=2))
