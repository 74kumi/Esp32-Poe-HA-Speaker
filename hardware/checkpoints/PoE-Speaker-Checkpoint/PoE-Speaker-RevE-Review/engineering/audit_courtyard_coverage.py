from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));rows=[]
for f in b.GetFootprints():
 if not any(g.GetLayer() in [p.F_CrtYd,p.B_CrtYd] for g in f.GraphicalItems()):rows.append({'reference':f.GetReference(),'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibItemName()),'position_mm':p.ToMM(f.GetPosition()),'board_feature':f.GetReference().startswith(('H','TP'))})
(D/'reports/courtyard-coverage.json').write_text(json.dumps({'method':'Presence of courtyard graphics only; no body dimensions or overlap inference for absent courtyards. Existing DRC missing_courtyard check is disabled.','missing_courtyards':rows},indent=2));print('Missing courtyards:',len(rows),'including',sum(not x['board_feature'] for x in rows),'assembly components')
