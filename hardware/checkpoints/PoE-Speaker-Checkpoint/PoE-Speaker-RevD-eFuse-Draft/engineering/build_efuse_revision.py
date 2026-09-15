from pathlib import Path
import json,uuid,sys
E=Path(__file__).resolve().parent;B=E.parent;sys.path.insert(0,str(B))
from inspect_flux import parse,walk
m=json.loads((E/'revision-c-design.json').read_text());c=m['components']
def add(ref,value,pins,fp,pos):
 c[ref]={'ref':ref,'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'poe-revd:'+ref)),'value':value,'properties':{'Manufacturer Part Number':'TBD','Review status':'Development selection; thermal/transient checks pending'},'pins':[{'number':str(n),'name':str(n),'type':'passive','net':net} for n,net in pins.items()],'footprint':fp,'group':'Shared current protection','sheet':'Shared current protection','position':pos,'angle':0,'side':'Top','source':'RevD'}
# Put the eFuse after ORing, before every original 24V_AMP load.
for ref,pn in [('Q1','2'),('Q2','2'),('U9','6'),('U10','6')]:
 next(p for p in c[ref]['pins'] if p['number']==pn)['net']='24V_OR'
next(p for p in c['U11']['pins'] if p['number']=='4')['net']='AMP_ENABLE_CMD'
pins={1:'24V_OR',2:'24V_OR',3:None,4:None,5:'24V_OR',6:'EFUSE_UV',7:'EFUSE_OV',8:'GND',9:'EFUSE_DVDT',10:'EFUSE_ILIM',11:None,12:'EFUSE_SHDN',13:None,14:'EFUSE_FAULT_N',15:'EFUSE_PGTH',16:'AMP_SDZ',17:'24V_AMP',18:'24V_AMP',19:None,20:None,21:None,22:None,23:None,24:None,25:'GND'}
add('U16','TPS26630RGER',pins,'Package_DFN_QFN:Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm_ThermalVias',[252,77]);c['U16']['properties']['Manufacturer Part Number']='TPS26630RGER'
lib=parse(Path('C:/Program Files/KiCad/10.0/share/kicad/symbols/Power_Management.kicad_sym').read_text());sym=next(x for x in walk(lib,'symbol') if x[1]=='TPS26630RGE')
for x in walk(sym,'pin'):
 n=next(t[1] for t in x if isinstance(t,list) and t[0]=='number');p=next(p for p in c['U16']['pins'] if p['number']==n);p['name']=next(t[1] for t in x if isinstance(t,list) and t[0]=='name');p['type']='open_collector' if n=='16' else x[1]
R='Resistor_SMD:R_0805_2012Metric';C='Capacitor_SMD:C_0805_2012Metric'
for ref,v,a,b,pos in [('R130','6.04k','EFUSE_ILIM','GND',[246,82]),('R131','200k','24V_OR','EFUSE_OV',[241,73]),('R132','10k','EFUSE_OV','GND',[241,77]),('R133','158k','24V_OR','EFUSE_UV',[241,65]),('R134','10k','EFUSE_UV','GND',[241,69]),('R135','1k','AMP_ENABLE_CMD','AMP_SDZ',[263,70]),('R136','174k','24V_AMP','EFUSE_PGTH',[270,77]),('R137','10k','EFUSE_PGTH','GND',[270,81]),('R138','10k','EFUSE_FAULT_N','3V3',[252,65])]:
 add(ref,v,{1:a,2:b},R,pos)
 c[ref]['properties']['Tolerance']='0.1%' if ref in ['R131','R132'] else '1%'
 if ref in ['R131','R132']:c[ref]['properties']['Temperature coefficient']='10 ppm/C max'
for ref,v,net,pos in [('C121','100nF','EFUSE_DVDT',[253,84]),('C122','1uF','24V_OR',[251,71]),('C123','1uF','24V_AMP',[258,77])]:
 add(ref,v,{1:net,2:'GND'},C,pos);c[ref]['properties']['Voltage rating']='100 V' if ref=='C122' else '50 V'
for ref,net,pos in [('TP26','EFUSE_SHDN',[262,83]),('TP27','EFUSE_FAULT_N',[257,65])]:add(ref,net,{1:net},'TestPoint:TestPoint_Pad_D1.0mm',pos)
m['revision']='D-shared-efuse-development';m['changes'].append({'change':'Add shared eFuse after ORing; latch-off nominal 3 A; hardware power-good shutdown interlock','references':['U16','R130-R138','C121-C123','TP26-TP27']})
(E/'revision-d-design.json').write_text(json.dumps(m,indent=2))
s=(E/'build_revision.py').read_text().replace('revision-b-design.json','revision-d-design.json').replace("OUT=BASE/'KiCad-RevB'","OUT=BASE/'KiCad-RevD'").replace("PROJECT='PoE-Speaker-RevB'","PROJECT='PoE-Speaker-RevD'").replace('REV B - DEVELOPMENT','REV D - DEVELOPMENT').replace('((70,50),(230,50)),((230,50),(230,150)),((230,150),(70,150))','((70,50),(280,50)),((280,50),(280,150)),((280,150),(70,150))')
exec(compile(s,str(E/'build_revision.py'),'exec'))
