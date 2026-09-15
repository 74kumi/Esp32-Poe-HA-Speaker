"""Widen draft power trunks; retain the pre-change board for DRC-guided rollback.
These are layout targets, not a certified current/temperature calculation.
"""
from pathlib import Path
import json,shutil,pcbnew as p
D=Path(__file__).resolve().parent.parent/'KiCad-RevB';path=D/'PoE-Speaker-RevB.kicad_pcb'
backup=D/'reports/before-power-widening.kicad_pcb'
shutil.copy2(path,backup)
b=p.LoadBoard(str(path));changes=[]
wide={'24V_AMP':1.0,'24V_POE':1.0,'24V_BENCH_RAW':1.0,'24V_BENCH_PROTECTED':1.0,'POE_12V_MID':1.0,
      'SPK_POS':1.5,'SPK_NEG':1.5,'AMP_SW_POS':1.5,'AMP_SW_NEG':1.5,'5V':.6,'3V3':.6,
      'POE_RECT_POS':.8,'POE_RECT_NEG':.8,'POE_MODE_A_AC1':.6,'POE_MODE_A_AC2':.6,'POE_MODE_B_AC1':.6,'POE_MODE_B_AC2':.6}
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):continue
 nm=t.GetNetname();target=wide.get(nm)
 if target and t.GetLength()>p.FromMM(2) and t.GetWidth()<p.FromMM(target):
  changes.append({'uuid':t.m_Uuid.AsString(),'net':nm,'old_width_mm':t.GetWidth()/1e6,'target_mm':target,'length_mm':t.GetLength()/1e6})
  t.SetWidth(p.FromMM(target))
p.SaveBoard(str(path),b)
(D/'reports/power-widening.json').write_text(json.dumps({'status':'Trial awaiting DRC','targets_mm':wide,'changes':changes},indent=2))
print('Trial widened',len(changes),'power trunk segments')
