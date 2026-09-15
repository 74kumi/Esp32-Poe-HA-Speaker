from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};rows=[]
for ref,y in [('H3',55),('H4',145)]:
 f=fs[ref];old=p.ToMM(f.GetPosition());f.SetPosition(p.VECTOR2I(p.FromMM(275),p.FromMM(y)));rows.append({'ref':ref,'old_position_mm':old,'new_position_mm':[275,y],'footprint':str(f.GetFPID().GetLibItemName())})
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b);(D/'reports/extension-mounting-review.json').write_text(json.dumps({'status':'trial','changes':rows,'hardware':'M2 insulating standoffs; enclosure and top heatsink design still pending'},indent=2))
