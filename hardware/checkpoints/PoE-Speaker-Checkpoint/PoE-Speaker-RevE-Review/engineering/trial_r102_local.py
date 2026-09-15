"""Relocate R102 and its supply branch in a trial; main must stay intact."""
from pathlib import Path
import pcbnew as p,json,shutil,hashlib
D=Path('KiCad-RevE');src=D/'PoE-Speaker-RevE.kicad_pcb';b=p.LoadBoard(str(src));ts=list(b.GetTracks());fs={f.GetReference():f for f in b.GetFootprints()};assert fs['R102'].GetLayer()==p.F_Cu
removed={'55de4897-b7a9-407f-81b9-a8123207f53a','e14890bb-ccbf-4afb-9246-4f0fae845a06','5966a231-d30e-4e07-bed8-96c0f2291235'}
for t in ts:
 if t.m_Uuid.AsString() in removed:b.Remove(t)
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def route(net,pts,layer):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(p.FromMM(.2));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t)
def via(net,x,y):
 v=p.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v)
f=fs['R102'];f.Flip(f.GetPosition(),False);f.SetPosition(pt(116.3,64.7));f.SetOrientation(p.EDA_ANGLE(270,p.DEGREES_T));f.Reference().SetPosition(pt(115,64.7));f.Reference().SetTextAngle(p.EDA_ANGLE(90,p.DEGREES_T))
pads={x.GetNumber():p.ToMM(x.GetPosition()) for x in f.Pads()};print(pads)
via('ETH_TX_N',117.1,64.1563)
route('ETH_TX_N',[(117.1,64.1563),(116.8187,63.875),pads['1']],p.B_Cu)
# Reuse the existing analog supply via.
route('ETH_3V3A',[pads['2'],(117.5,65.3196)],p.B_Cu)

p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
(D/'reports/r102-placement-trial.json').write_text(json.dumps({'main_before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'removed':sorted(removed),'position':[116.3,64.7],'angle':270,'side':'Bottom','new_vias':{'ETH_TX_N':[117.1,64.1563]},'status':'trial'},indent=2))

