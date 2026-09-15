"""Revert only width changes that collide with existing copper; record bottlenecks."""
from pathlib import Path
import json,pcbnew as p
D=Path(__file__).resolve().parent.parent/'KiCad-RevB';R=D/'reports'
r=json.loads((R/'power-widening.json').read_text());d=json.loads((R/'power-width-trial-drc.json').read_text())
bad={i['uuid'] for v in d['violations'] if v['type'] in ['clearance','shorting_items','tracks_crossing','edge_clearance','hole_clearance'] for i in v['items']}
b=p.LoadBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'));tracks={t.m_Uuid.AsString():t for t in b.GetTracks()}
for c in r['changes']:
 c['accepted']=c.get('accepted',True) and c['uuid'] not in bad
 if not c['accepted']:tracks[c['uuid']].SetWidth(p.FromMM(c['old_width_mm']))
p.SaveBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'),b)
r['status']='Accepted collision-free widening candidates; final DRC pending'
r['accepted_count']=sum(c['accepted'] for c in r['changes']);r['blocked_count']=len(r['changes'])-r['accepted_count']
r['limitations']='Unchanged short escapes and blocked trunks remain current bottlenecks. Via arrays, planes, current sharing and temperature rise are not qualified.'
(R/'power-widening.json').write_text(json.dumps(r,indent=2));print(r['accepted_count'],'accepted,',r['blocked_count'],'require rerouting')
