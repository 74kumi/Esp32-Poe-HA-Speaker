"""Trial moving low-current signal vias to free the existing supply corridor."""
from pathlib import Path
import pcbnew as p
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));ts=list(b.GetTracks())
for key,x,y in [('ef71f386-8a57-4099-b0b6-c198845a9066',202.381,107.581),('261d5293-1bb5-4e4f-b17e-926878c47fe4',202.968,110.075)]:
 via=next(t for t in ts if str(t.m_Uuid.AsString())==key);old=via.GetPosition();new=p.VECTOR2I(p.FromMM(x),p.FromMM(y));via.SetPosition(new)
 for t in ts:
  if isinstance(t,p.PCB_VIA) or t.GetNetCode()!=via.GetNetCode():continue
  if t.GetStart()==old:t.SetStart(new)
  if t.GetEnd()==old:t.SetEnd(new)
for t in ts:
 if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='24V_AMP' and t.GetLayer()==p.B_Cu and p.ToMM(t.GetStart()) in [(203.5827,106.4),(203.5827,107.865)]:t.SetWidth(p.FromMM(1))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b)
