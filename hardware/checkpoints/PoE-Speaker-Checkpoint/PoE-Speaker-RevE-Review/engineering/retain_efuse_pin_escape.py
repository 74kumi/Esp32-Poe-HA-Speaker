from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'power-trial.kicad_pcb'))
for t in b.GetTracks():
 if t.m_Uuid.AsString()=='de68fccd-d0fa-4041-801a-9a1035c22098':t.SetWidth(p.FromMM(.3))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
f=D/'reports/load-neck-width-trial.json';d=json.loads(f.read_text());d=[x for x in d if x['uuid']!='de68fccd-d0fa-4041-801a-9a1035c22098'];f.write_text(json.dumps({'accepted_changes':d,'retained_neck':'U16 pin escape de68fccd remains 0.3 mm for 0.5 mm length; 0.6 mm conflicts with adjacent AMP_SDZ pad. Current qualification remains.'},indent=2))
