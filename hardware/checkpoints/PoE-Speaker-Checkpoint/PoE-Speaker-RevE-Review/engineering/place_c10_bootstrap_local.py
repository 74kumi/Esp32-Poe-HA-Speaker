"""Trial a local C10 connection at the amplifier BSNR/OUTNR pins."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()}
for t in ts:
 if t.GetNetname()=='AMP_BSPR':b.Remove(t)
f=fs['C10'];f.SetPosition(p.VECTOR2I(p.FromMM(214.5),p.FromMM(106.5)));f.SetOrientation(p.EDA_ANGLE(270,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(218),p.FromMM(102.5)))
fs['C9'].Reference().SetPosition(p.VECTOR2I(p.FromMM(214.2),p.FromMM(113.5)))
fs['C9'].Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
fs['U5'].Reference().SetPosition(p.VECTOR2I(p.FromMM(210),p.FromMM(111)))
pads={x.GetNumber():x for x in f.Pads()};up={x.GetNumber():x for x in fs['U5'].Pads()}
for cn,un in [('1','30'),('2','29')]:
 a=p.ToMM(up[un].GetPosition());z=p.ToMM(pads[cn].GetPosition());print(cn,a,z)
 bend=212.7 if cn=='1' else 213.0
 points=[a,(bend,a[1]),(bend+abs(z[1]-a[1]),z[1]),z]
 for start,end in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in start]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in end]));t.SetLayer(p.F_Cu);t.SetNet(pads[cn].GetNet());t.SetWidth(p.FromMM(.3));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)

