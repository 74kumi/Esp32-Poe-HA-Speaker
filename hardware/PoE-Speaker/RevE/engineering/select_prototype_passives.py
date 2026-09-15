"""Populate documented passive candidates; keep qualification status explicit."""
from pathlib import Path
import json,re
path=Path('engineering/revision-e-design.json');m=json.loads(path.read_text());cs=m['components'];selected=[]
def choose(ref,mpn,mfg,url,**props):
 c=cs[ref];c['properties'].update({'Manufacturer Part Number':mpn,'Manufacturer Name':mfg,'Datasheet':url,'Selection status':'Datasheet-selected prototype candidate; availability and circuit qualification pending',**props});selected.append(ref)
for ref,c in cs.items():
 if not ref.startswith('R'):continue
 size=re.search(r'R_(\d{4})_',c['footprint'])[1];v=c['value'].replace('Ω','').upper();match=re.fullmatch(r'([\d.]+)(K?)',v);assert match,v
 n=float(match[1]);unit='K' if match[2] else 'R';code=(f'{n:g}'.replace('.',unit) if '.' in f'{n:g}' else f'{n:g}'+unit)
 code=code.ljust(4,'0');assert len(code)==4,code
 precise=ref in ['R120','R121','R131','R132'];suffix='BYEA' if precise else 'FHEA'
 choose(ref,'TNPW'+size+code+suffix,'Vishay','https://www.vishay.com/docs/28758/tnpw_e3.pdf',Tolerance='0.1%' if precise else '1%',**{'Temperature coefficient':'10 ppm/C maximum' if precise else '50 ppm/C maximum','Power rating':'0.10 W conservative' if size=='0603' else '0.125 W conservative' if size=='0805' else '0.25 W conservative'})
mapping={('0603','100nF'):'C0603C104K5RACTU',('0603','220nF'):'C0603C224K5RACTU',('0603','1uF'):'C0603C105K4RACTU',('0805','4.7uF'):'C0805C475K4RACTU',('1210','22uF'):'C1210C226K3RACTU',('1210','1uF'):'C1210C105K1RACTU',('1210','10uF'):'C1210C106K5RACTU',('0805','2.2uF'):'C0805C225K3RACTU',('0603','3.3nF'):'C0603C332J5GACTU',('0603','2.2nF'):'C0603C222J5GACTU',('0603','22nF'):'C0603C223K5RACTU',('0603','6.8nF'):'C0603C682J5GACTU',('0603','10nF'):'C0603C103K5RACTU',('0805','1uF'):'C0805C105K5RACTU'}
for ref,c in cs.items():
 if not ref.startswith('C') or ref in ['C120','C121','C122']:continue
 match=re.search(r'C_(\d{4})_',c.get('footprint',''))
 if not match:continue
 mpn=mapping.get((match[1],c['value']))
 if not mpn:continue
 assert Path('engineering/sources/prototype-capacitors',mpn+'.txt').exists()
 voltage={'1':100,'3':25,'4':16,'5':50}[mpn[10]]
 choose(ref,mpn,'KEMET','https://search.kemet.com/component-documentation/download/specsheet/'+mpn,**{'Voltage Rating':str(voltage)+' V','Dielectric':'C0G' if mpn[11]=='G' else 'X7R','Tolerance':'5%' if mpn[9]=='J' else '10%'})
path.write_text(json.dumps(m,indent=2));Path('KiCad-RevE/reports/passive-selections.json').write_text(json.dumps({'selected_references':selected,'count':len(selected),'status':'Candidate selections, not procurement approval'},indent=2));print('Selected',len(selected),'passive order codes')
