from pathlib import Path
s=Path('engineering/finish_draft.py').read_text().replace("D=BASE/'KiCad-RevB'","D=BASE/'KiCad-RevD'").replace('PoE-Speaker-RevB.kicad_pcb','PoE-Speaker-RevD.kicad_pcb')
s=s[:s.index("report={'status'")]
exec(compile(s,'import-protection','exec'))
