"""Quantitative review queue, not a current/impedance qualification."""
import pcbnew as p,json,collections
from pathlib import Path
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'))
nets=['24V_AMP','24V_OR','24V_POE','24V_BENCH_PROTECTED','BENCH_FUSED','5V','3V3','AMP_SW_POS','AMP_SW_NEG','SPK_POS','SPK_NEG','BUCK5_SW','BUCK3V3_SW']
rows=[]
for net in nets:
 ts=[t for t in b.GetTracks() if t.GetNetname()==net and not isinstance(t,p.PCB_VIA)]
 if not ts:continue
 narrow=sorted([t for t in ts if p.ToMM(t.GetWidth())<.5],key=lambda t:t.GetLength(),reverse=True)
 rows.append({'net':net,'total_track_length_mm':round(sum(p.ToMM(t.GetLength()) for t in ts),2),'under_0_5mm_length_mm':round(sum(p.ToMM(t.GetLength()) for t in narrow),2),'longest_narrow_sections':[{'width_mm':p.ToMM(t.GetWidth()),'length_mm':round(p.ToMM(t.GetLength()),3),'start_mm':p.ToMM(t.GetStart()),'end_mm':p.ToMM(t.GetEnd()),'layer':b.GetLayerName(t.GetLayer()),'uuid':str(t.m_Uuid.AsString())} for t in narrow[:5]]})
(D/'reports/power-routing-audit.json').write_text(json.dumps({'scope':'Geometric screening only. 0.5mm is a review trigger, not an ampacity rule. Parallel branches and current sharing not inferred.','nets':rows},indent=2))
print([(r['net'],r['under_0_5mm_length_mm']) for r in rows])
