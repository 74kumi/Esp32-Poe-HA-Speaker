"""Trial a local C9 connection at the amplifier BSNR/OUTNR pins."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()}
removed={'58d7816d-6d65-407f-892a-a1e88eac73b4','7ff16400-bf14-4092-9669-8154faa0ba42','8aa69d45-f7c9-4f4f-97ef-f0d7189b0eb2','b5b920be-796b-45ec-a567-c3c59858ab4b','29c9c048-25da-4bd3-a4c9-7ecf90dffbc4'}
for t in ts:
 if t.GetNetname()=='AMP_BSNR' or t.m_Uuid.AsString() in removed:b.Remove(t)
def route(net,points,width):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));t.SetWidth(p.FromMM(width));b.Add(t)
for pos in [(212.81,110.675),(212.785,108.725)]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(*[p.FromMM(x) for x in pos]));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
route('AMP_SW_NEG',[(214.559,101.323),(216,102.764),(216,111.975),(213.209,111.975)],1.0)
fs['J3'].Reference().SetPosition(p.VECTOR2I(p.FromMM(220),p.FromMM(111)))
f=fs['C9'];f.SetPosition(p.VECTOR2I(p.FromMM(214.5),p.FromMM(109.7)));f.SetOrientation(p.EDA_ANGLE(90,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(214.5),p.FromMM(107.5)))
pads={x.GetNumber():x for x in f.Pads()};up={x.GetNumber():x for x in fs['U5'].Pads()}
for cn,un in [('1','26'),('2','27')]:
 a=p.ToMM(up[un].GetPosition());z=p.ToMM(pads[cn].GetPosition());print(cn,a,z)
 points=[a,(213.3,a[1]),(213.3+abs(z[1]-a[1]),z[1]),z]
 for start,end in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in start]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in end]));t.SetLayer(p.F_Cu);t.SetNet(pads[cn].GetNet());t.SetWidth(p.FromMM(.3));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
