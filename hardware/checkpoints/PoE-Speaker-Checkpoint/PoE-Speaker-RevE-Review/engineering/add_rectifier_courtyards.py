from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'))
for f in b.GetFootprints():
 if f.GetReference() not in ['D'+str(i) for i in range(3,11)]:continue
 assert f.GetOrientationDegrees()==0 and f.GetValue()=='B5100C'
 pos=f.GetPosition();g=p.PCB_SHAPE(f);g.SetShape(p.SHAPE_T_RECT);g.SetStart(p.VECTOR2I(pos.x-p.FromMM(5.05),pos.y-p.FromMM(3.4)));g.SetEnd(p.VECTOR2I(pos.x+p.FromMM(5.05),pos.y+p.FromMM(3.4)));g.SetLayer(p.F_CrtYd);g.SetWidth(p.FromMM(.05));f.Add(g)
p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
