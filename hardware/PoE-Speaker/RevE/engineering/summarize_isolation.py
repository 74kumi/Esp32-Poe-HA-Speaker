"""Check the saved isolation-layout revision against KiCad's actual findings."""
import pcbnew as p,json,collections
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'KiCad-RevB';R=D/'reports'
b=p.LoadBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'))
drc=json.loads((R/'board-drc.json').read_text())
orientation={}
for f in b.GetFootprints():
 if f.GetReference() in ['U12','U13','U14']:
  pads={x.GetNumber():x for x in f.Pads()}
  assert max(pads[n].GetPosition().x for n in ['1','2'])<min(pads[n].GetPosition().x for n in ['3','4'])
  orientation[f.GetReference()]={'primary_pins':'left','secondary_pins':'right','angle_deg':f.GetOrientationDegrees()}
stats=collections.defaultdict(lambda:collections.defaultdict(float))
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA):stats[t.GetNetname()][str(round(t.GetWidth()/1e6,4))]+=t.GetLength()/1e6
violations=collections.Counter(v['type'] for v in drc['violations'])
isolation=[v for v in drc['violations'] if 'PoE primary to secondary review target' in v['description']]
report={'status':'Layout review in progress; not fabrication qualified','optocouplers':orientation,
 'isolation_target_mm':3,'isolation_clearance_findings':len(isolation),'unconnected_items':len(drc['unconnected_items']),
 'drc_findings':dict(violations),'track_length_mm_by_net_and_width':{n:dict(w) for n,w in stats.items()},
 'limits':['The 3 mm copper review rule is not a dielectric-strength or creepage certification.',
 'Wider routing targets do not qualify pin escapes, vias, return planes, temperature rise or protection circuitry.']}
(R/'isolation-layout-review.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='track_length_mm_by_net_and_width'},indent=2))
