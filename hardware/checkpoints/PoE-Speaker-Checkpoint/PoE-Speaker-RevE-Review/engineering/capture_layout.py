"""Persist reviewed placement so schematic rebuilds retain board placement choices."""
from pathlib import Path
import json,pcbnew as p
BASE=Path(__file__).resolve().parent.parent
b=p.LoadBoard(str(BASE/'KiCad-RevB/PoE-Speaker-RevB.kicad_pcb'))
placement={f.GetReference():{'position':[f.GetPosition().x/1e6,f.GetPosition().y/1e6],'angle':f.GetOrientationDegrees(),'side':'Bottom' if f.IsFlipped() else 'Top'} for f in b.GetFootprints()}
(BASE/'engineering/layout-overrides.json').write_text(json.dumps(placement,indent=2))
print('Saved',len(placement),'placement overrides; routing still requires separate preservation')
