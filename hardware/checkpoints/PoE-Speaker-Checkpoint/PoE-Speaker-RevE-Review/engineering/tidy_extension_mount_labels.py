from pathlib import Path
import pcbnew as p,shutil
D=Path('KiCad-RevE');path=D/'PoE-Speaker-RevE.kicad_pcb';b=p.LoadBoard(str(path));shutil.copy2(path,D/'before-mount-reference-tidy.kicad_pcb')
for f in b.GetFootprints():
 if f.GetReference() in ['H3','H4']:
  f.Reference().SetPosition(p.VECTOR2I(p.FromMM(275),p.FromMM(59 if f.GetReference()=='H3' else 141)));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
p.SaveBoard(str(path),b)
