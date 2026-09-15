"""Finish candidate selections and fit stable timing capacitors in Rev E."""
from pathlib import Path
import json,pcbnew as p
D=Path('KiCad-RevE');mp=Path('engineering/revision-e-design.json');m=json.loads(mp.read_text());cs=m['components']
b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
def choose(ref,code,mfg,url,**props):
 cs[ref]['properties'].update({'Manufacturer Part Number':code,'Manufacturer Name':mfg,'Datasheet':url,'Selection status':'Documented prototype candidate; circuit qualification pending',**props})
for refs,code,v,tol in [(['C49','C31'],'GRM21BR61C226ME44L',16,'20%'),(['C24','C23','C22','C48','C25','C111','C113'],'GRM21BR61C106KE15L',16,'10%'),(['C50'],'GRM32ER61C476KE15L',16,'10%')]:
 for ref in refs:choose(ref,code,'Murata','https://www.murata.com/en-global/products/productdetail?partno='+code,**{'Voltage Rating':f'{v} V','Dielectric':'X5R','Tolerance':tol})
for ref,code in [('J5','TSW-106-07-G-S'),('J6','TSW-106-07-G-S'),('J4','TSW-107-07-G-D')]:choose(ref,code,'Samtec','https://www.samtec.com/products/'+code)
choose('FB1','BLM18AG601SN1D','Murata','https://www.murata.com/en-us/products/productdata/8796738650142/ENFA0003.pdf',**{'Current rating':'500 mA','DCR maximum':'0.48 ohm'})
for ref in ['C17','C18']:
 cs[ref]['value']='2.2uF';cs[ref]['properties']['Capacitance']='2.2uF';fs[ref].SetValue('2.2uF')
 choose(ref,'C0805C225K3RACTU','KEMET','https://search.kemet.com/component-documentation/download/specsheet/C0805C225K3RACTU',**{'Voltage Rating':'25 V','Tolerance':'10%','Dielectric':'X7R','Design note':'Matched AC coupling pair; changed from 1.5uF to 2.2uF. Hold amplifier shutdown until DAC settles.'})
for ref,code in [('C120','C1210C104J1GACTU'),('C121','C1210C104J1GACTU'),('C122','C1210C105K1RACTU')]:
 assert Path('engineering/sources/prototype-capacitors',code+'.txt').exists()
 choose(ref,code,'KEMET','https://search.kemet.com/component-documentation/download/specsheet/'+code,**{'Voltage Rating':'100 V','Tolerance':'5%' if ref!='C122' else '10%','Dielectric':'C0G' if ref!='C122' else 'X7R'})
 name='C_1210_3225Metric';cs[ref]['footprint']='Capacitor_SMD:'+name
 old=fs[ref]
 if str(old.GetFPID().GetLibItemName())==name:continue
 new=p.FootprintLoad(r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty',name)
 new.SetUuid(old.m_Uuid);b.Remove(old);b.Add(new);new.SetPosition(old.GetPosition());new.SetOrientation(old.GetOrientation());new.SetReference(ref);new.SetValue(old.GetValue());new.SetPath(old.GetPath())
 new.SetFPID(p.LIB_ID('Capacitor_SMD',name))
 for a,z in [(new.Reference(),old.Reference()),(new.Value(),old.Value())]:
  a.SetPosition(z.GetPosition());a.SetTextAngle(z.GetTextAngle());a.SetTextSize(z.GetTextSize());a.SetTextThickness(z.GetTextThickness());a.SetVisible(z.IsVisible())
 pads={x.GetNumber():x for x in old.Pads()}
 for pad in new.Pads():
  op=pads[pad.GetNumber()];pad.SetNet(op.GetNet())
  if pad.GetPosition()!=op.GetPosition():
   t=p.PCB_TRACK(b);t.SetStart(op.GetPosition());t.SetEnd(pad.GetPosition());t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(op.GetNet());b.Add(t)
for t in list(b.GetTracks()):
 if str(t.m_Uuid.AsString())=='ae183f8b-5eec-464c-8ac0-1480b51040ea':b.Remove(t)
for ref in ['C1','C2','C3','C4','C5','C6']:cs[ref]['properties']['Package']='Radial through-hole; see assigned PCB footprint'
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'),b)
mp.write_text(json.dumps(m,indent=2));print('Remaining passive candidates selected; C120/C121/C122 enlarged to 1210')
