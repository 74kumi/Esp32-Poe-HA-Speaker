"""Trial widening only the five narrow segments identified on audited load paths."""
from pathlib import Path
import json,pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));d=json.loads((D/'reports/supply-path-audit.json').read_text()); ids={t['uuid'] for r in d['paths'] for t in r['narrow_tracks']}; changed=[]
for t in b.GetTracks():
 if t.m_Uuid.AsString() in ids:
  changed.append({'uuid':t.m_Uuid.AsString(),'old_width_mm':p.ToMM(t.GetWidth()),'new_width_mm':.6});t.SetWidth(p.FromMM(.6))
assert len(changed)==5
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
(D/'reports/load-neck-width-trial.json').write_text(json.dumps(changed,indent=2))
