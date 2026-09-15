"""Reroute TX_N jack fanout while preserving its local termination tap."""
from pathlib import Path
import pcbnew as p,json,shutil,hashlib
D=Path('KiCad-RevE');src=D/'PoE-Speaker-RevE.kicad_pcb';b=p.LoadBoard(str(src));ts=list(b.GetTracks())
ids={'afbcb83b-8a30-447e-8eae-370f07a999e8','fb6f1fd4-4ae2-4fc5-8139-989e9359d856'}
old=[t for t in ts if t.m_Uuid.AsString() in ids];assert len(old)==2
old_length=sum(p.ToMM(t.GetLength()) for t in old)
for t in old:b.Remove(t)
rx_moved=[]
for t in ts:
 if t not in old and not isinstance(t,p.PCB_VIA) and t.GetNetname() in ['ETH_RX_P','ETH_RX_N'] and t.GetLayer()==p.In2_Cu:
  t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(.225806));rx_moved.append(t.m_Uuid.AsString())
pts=[(110.53,66.968),(114.288,66.968),(117.1,64.1563),(117.677,63.5793)]
length=0
for a,z in zip(pts,pts[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetWidth(p.FromMM(.225806));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('ETH_TX_N'));b.Add(t);length+=p.ToMM(t.GetLength())
power_ids={'a323a49a-b88c-4462-9bed-027f870c2c96','3da52bb8-048a-42ef-84bb-566052a83846','cd21218f-84bd-4ee8-8250-cc95de904e0a','7915e1da-6865-4e73-a2a9-14347f35443c'}
for t in ts:
 if t.m_Uuid.AsString() in power_ids:b.Remove(t)
power_pts=[(116.3,65.525),(116.3,74.6),(118.725,74.6)]
for a,z in zip(power_pts,power_pts[1:]):
 t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(*[p.FromMM(v) for v in a]));t.SetEnd(p.VECTOR2I(*[p.FromMM(v) for v in z]));t.SetWidth(p.FromMM(.3));t.SetLayer(p.B_Cu);t.SetNet(b.FindNet('ETH_3V3A'));b.Add(t)
v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(118.725),p.FromMM(74.6)));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('ETH_3V3A'));b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'ethernet-trial.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
(D/'reports/txn-fanout-trial.json').write_text(json.dumps({'main_before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'removed':sorted(ids),'old_length_mm':old_length,'new_length_mm':length,'points_mm':pts,'power_removed':sorted(power_ids),'power_points_mm':power_pts,'status':'trial; not matched-pair routing'},indent=2))

