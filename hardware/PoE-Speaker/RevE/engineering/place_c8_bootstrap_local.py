"""Trial a local C8 connection at the amplifier BSNR/OUTNR pins."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()}
for t in ts:
 if t.GetNetname()=='AMP_BSPL' or t.m_Uuid.AsString() in {'27e096ef-1780-49ab-90ee-de41dd29793f','3301a86a-bab9-421c-af70-62719dddec18','603eb6c9-0a95-47e8-9613-52c4a3cb8063','79880968-b819-4680-bb04-f6a7f3914713','f63fdc89-4cef-447b-8057-f5442fc96cd1'}:b.Remove(t)
def route(points,width,layer=p.F_Cu):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(width));t.SetLayer(layer);t.SetNet(b.FindNet('AMP_SW_NEG'));b.Add(t)
route([(216,102.764),(216,110)],1)
route([(216,110),(216,113.45)],1,p.In2_Cu)
route([(216,113.45),(216,113.2),(213.21,113.2),(213.21,112.2)],.6)
route([(213.21,112.2),(213.209,111.975)],.3)
for xy in [(216,110),(216,113.45)]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(*[p.FromMM(x) for x in xy]));v.SetWidth(p.FromMM(1));v.SetDrill(p.FromMM(.5));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('AMP_SW_NEG'));b.Add(v)
for a,z in zip([(216.01,94.0283),(216.01,108),(214.7,109.31),(214.7,111.55)],[(216.01,108),(214.7,109.31),(214.7,111.55),(216.01,111.55)]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(x) for x in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(x) for x in z]));t.SetWidth(p.FromMM(1));t.SetLayer(p.B_Cu);t.SetNet(b.FindNet('SPK_POS'));b.Add(t)
f=fs['C8'];f.SetPosition(p.VECTOR2I(p.FromMM(214.5),p.FromMM(112.2)));f.SetOrientation(p.EDA_ANGLE(180,p.DEGREES_T));f.Reference().SetPosition(p.VECTOR2I(p.FromMM(220),p.FromMM(104)))
f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
fs['C9'].Reference().SetPosition(p.VECTOR2I(p.FromMM(218),p.FromMM(104)))
pads={x.GetNumber():x for x in f.Pads()};up={x.GetNumber():x for x in fs['U5'].Pads()}
for cn,un in [('1','24'),('2','23')]:
 a=p.ToMM(up[un].GetPosition());z=p.ToMM(pads[cn].GetPosition());print(cn,a,z)
 points=[a,(z[0],a[1]),z]
 for start,end in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in start]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in end]));t.SetLayer(p.F_Cu);t.SetNet(pads[cn].GetNet());t.SetWidth(p.FromMM(.3));b.Add(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
