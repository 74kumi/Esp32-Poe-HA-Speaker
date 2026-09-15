"""Trial a local C9 connection at the amplifier BSNR/OUTNR pins."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()}
for t in ts:
 if t.GetNetname()=='AMP_BSNR':b.Remove(t)
f=fs['C9'];f.SetPosition(p.VECTOR2I(p.FromMM(212.7),p.FromMM(109.7)));f.Flip(f.GetPosition(),False);f.SetOrientation(p.EDA_ANGLE(90,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(212.7),p.FromMM(107.5)))
pads={x.GetNumber():x for x in f.Pads()};up={x.GetNumber():x for x in fs['U5'].Pads()}
for cn,un in [('1','26'),('2','27')]:
 a=p.ToMM(up[un].GetPosition());z=p.ToMM(pads[cn].GetPosition());print(cn,a,z)
 vpos=(212.3,a[1])
 if cn=='1':
  v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(*[p.FromMM(x) for x in vpos]));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetViaType(p.VIATYPE_THROUGH);v.SetNet(pads[cn].GetNet());b.Add(v)
  t=p.PCB_TRACK(b);t.SetStart(up[un].GetPosition());t.SetEnd(v.GetPosition());t.SetLayer(p.F_Cu);t.SetNet(pads[cn].GetNet());t.SetWidth(p.FromMM(.3));b.Add(t)
 else:vpos=(211.8,109.375)
 points=[vpos,(z[0],vpos[1]),z]
 for start,end in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in start]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in end]));t.SetLayer(p.B_Cu);t.SetNet(pads[cn].GetNet());t.SetWidth(p.FromMM(.3));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
