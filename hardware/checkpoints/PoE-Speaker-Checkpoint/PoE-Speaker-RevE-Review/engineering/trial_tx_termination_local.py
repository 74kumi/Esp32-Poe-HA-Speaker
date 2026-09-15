"""Local TX_P termination trial to free the receive routing corridor."""
from pathlib import Path
import pcbnew as p,shutil,json,hashlib
D=Path('KiCad-RevE');src=D/'PoE-Speaker-RevE.kicad_pcb';b=p.LoadBoard(str(src));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()}
remove={'28a58f13-d799-442e-afe4-1af09810781a','451f726b-0158-42ac-bb22-4f4385afaaec','b7b5de4d-c76b-4552-95a1-6ec970cd7c0d','101e52cd-0d9d-46a3-bfca-6bdff61b8e4d'}
for t in ts:
 if t.m_Uuid.AsString() in remove:b.Remove(t)
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
f=fs['R101'];f.Flip(f.GetPosition(),False);f.SetPosition(pt(120.5,64.8));f.SetOrientation(p.EDA_ANGLE(90,p.DEGREES_T));f.Reference().SetPosition(pt(123,64.8));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
print([(x.GetNumber(),p.ToMM(x.GetPosition())) for x in f.Pads()])
def route(net,points,layer):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(p.FromMM(.2));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t)
pads={x.GetNumber():p.ToMM(x.GetPosition()) for x in f.Pads()}
route('ETH_TX_P',[(119.497,66.7995),(120.5,65.7965),pads['1']],p.B_Cu)
route('ETH_3V3A',[pads['2'],(119.7,63.975)],p.B_Cu)
v=p.PCB_VIA(b);v.SetPosition(pt(119.7,63.975));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('ETH_3V3A'));b.Add(v)
route('ETH_3V3A',[(119.7,63.975),(119.7,63.8211)],p.In2_Cu)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
(D/'reports/tx-termination-trial.json').write_text(json.dumps({'main_before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'removed':sorted(remove),'R101_position':[120.5,64.8],'angle':90,'side':'Bottom','supply_via':[119.7,63.975],'status':'trial'},indent=2))

