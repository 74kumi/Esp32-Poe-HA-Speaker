from pathlib import Path
import json,uuid
E=Path(__file__).resolve().parent;B=E.parent
m=json.loads((E/'revision-b-design.json').read_text());c=m['components']
def add(ref,value,pins,fp,pos,types=None):
 c[ref]={'ref':ref,'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'poe-revc:'+ref)),'value':value,'properties':{'Manufacturer Part Number':value,'Review status':'Prototype candidate; not release qualified'},'pins':[{'number':str(n),'name':str(n),'type':(types or {}).get(str(n),'passive'),'net':net} for n,net in pins.items()],'footprint':fp,'group':'Bench protection','sheet':'Bench protection','position':pos,'angle':0,'side':'Top','source':'RevC'}
R='Resistor_SMD:R_0805_2012Metric';C='Capacitor_SMD:C_0805_2012Metric'
add('U15','LTC4365HTS8#TRPBF',{1:'BENCH_FUSED',2:'BENCH_UV',3:'BENCH_OV',4:'GND',5:'BENCH_SHDN',6:'BENCH_FAULT_N',7:'24V_BENCH_PROTECTED',8:'BENCH_PASS_GATE'},'Package_TO_SOT_SMD:TSOT-23-8',[249,100],{'1':'power_in','2':'input','3':'input','4':'power_in','5':'input','6':'open_collector','7':'input','8':'output'})
names=['VIN','UV','OV','GND','SHDN','FAULT_N','VOUT','GATE']
for p,n in zip(c['U15']['pins'],names):p['name']=n
for ref,drain,gate,pos in [('Q3','BENCH_FUSED','BENCH_GATE_A',[244,117]),('Q4','24V_BENCH_PROTECTED','BENCH_GATE_B',[265,117])]:
 add(ref,'PSMN4R8-100BSE',{1:gate,2:drain,3:'BENCH_COMMON_SOURCE'},'Package_TO_SOT_SMD:TO-263-2',pos)
 for p,n in zip(c[ref]['pins'],['G','D','S']):p['name']=n
res=[('R120','198k','BENCH_FUSED','BENCH_OV',[240,91]),('R121','4.02k','BENCH_OV','GND',[240,95]),('R122','392k','BENCH_FUSED','BENCH_UV',[246,91]),('R123','10k','BENCH_UV','GND',[246,95]),('R124','100k','BENCH_FUSED','BENCH_SHDN',[255,95]),('R125','10','BENCH_PASS_GATE','BENCH_GATE_A',[244,107]),('R126','10','BENCH_PASS_GATE','BENCH_GATE_B',[265,107]),('R127','5.1k','BENCH_PASS_GATE','BENCH_RAMP',[256,103]),('R128','10k','BENCH_FAULT_N','3V3',[260,91]),('R129','10k','AMP_SDZ','GND',[263,65])]
for ref,val,a,b,pos in res:
 add(ref,val,{1:a,2:b},R,pos)
 c[ref]['properties']['Manufacturer Part Number']='TBD'
 if ref in ['R120','R121']:c[ref]['properties'].update({'Tolerance':'0.1%','Temperature coefficient':'10 ppm/C maximum'})
add('C120','100nF',{1:'BENCH_RAMP',2:'GND'},C,[263,103]);c['C120']['properties'].update({'Manufacturer Part Number':'TBD','Voltage rating':'100 V','Tolerance':'10% effective capacitance including bias'})
add('TP25','BENCH_FAULT_N',{1:'BENCH_FAULT_N'},'TestPoint:TestPoint_Pad_D1.0mm',[266,95])
for p in c['F1']['pins']:
 if p['number']=='2':p['net']='BENCH_FUSED'
for p in c['D11']['pins']:
 if p['net']=='24V_BENCH_PROTECTED':p['net']='BENCH_FUSED'
c['D11']['value']='SMBJ26CA';c['D11']['properties'].update({'Manufacturer Part Number':'SMBJ26CA','Role Details':'Bidirectional input clamp; pulse coordination remains open','Manufacturer Name':'TBD','LCSC Part Number':''})
m['revision']='C-protection-development';m['status']='Protection integrated in draft schematic; not fabrication ready';m['intent']['board_outline_proposal_mm']=[210,100]
m['changes'].append({'change':'Add LTC4365 bench UV/OV/reverse-input disconnect with candidate pass FETs and ramp network; add amplifier shutdown pulldown','references':['U15','Q3','Q4','R120-R129','C120','TP25']})
(E/'revision-c-design.json').write_text(json.dumps(m,indent=2))
# Execute the established serializer against a separate output and model.
s=(E/'build_revision.py').read_text().replace('revision-b-design.json','revision-c-design.json').replace("OUT=BASE/'KiCad-RevB'","OUT=BASE/'KiCad-RevC'")
s=s.replace("PROJECT='PoE-Speaker-RevB'","PROJECT='PoE-Speaker-RevC'").replace('REV B - DEVELOPMENT','REV C - DEVELOPMENT')
s=s.replace('((70,50),(230,50)),((230,50),(230,150)),((230,150),(70,150))','((70,50),(280,50)),((280,50),(280,150)),((280,150),(70,150))')
exec(compile(s,str(E/'build_revision.py'),'exec'))
