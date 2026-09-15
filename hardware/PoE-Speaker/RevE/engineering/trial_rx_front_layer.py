"""Feasibility probe: expose obstacles to RX front-layer routing, not release."""
from pathlib import Path
import pcbnew as p, shutil,json,hashlib
D=Path('KiCad-RevE'); src=D/'PoE-Speaker-RevE.kicad_pcb'; b=p.LoadBoard(str(src)); changed=[]
tracks=list(b.GetTracks())
for t in tracks:
 if not isinstance(t,p.PCB_VIA) and t.GetNetname() in ['ETH_RX_P','ETH_RX_N'] and t.GetLayer()==p.In2_Cu:
  changed.append(t.m_Uuid.AsString()); t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(0.225806))
assert len(changed)==5
p.ZONE_FILLER(b).Fill(b.Zones()); p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
(D/'reports/rx-front-layer-probe.json').write_text(json.dumps({'status':'unaccepted feasibility probe; not coupled pair geometry','main_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'changed_segments':changed},indent=2))
