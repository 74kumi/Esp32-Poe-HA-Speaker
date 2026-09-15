"""Explicit electrical redesign model for the eight-microphone speaker main board.

This does not rerun or overwrite the Flux recovery. The net changes below are
intentional design changes; the resulting netlist must not be compared to the
unmodified Flux EDIF as if it were still a format-only conversion.
"""
import collections,copy,json,re,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from inspect_flux import parse,walk

BASE=Path(__file__).resolve().parent.parent
SOURCE=json.loads((BASE/'74kumi-poe-esp32-network-audio-endpoint.flx').read_text(encoding='utf-8'))
KICAD=Path('C:/Program Files/KiCad/10.0/share/kicad')
def ident(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'poe-speaker-revb:'+s))
def properties(e):return {p['name']:p.get('value','') for p in e.get('properties',{}).values()}
def scalar(s):return float(str(s).replace('mm','').replace('deg',''))
components={}
netmap={tuple(pin):n for n,ps in json.loads((BASE/'KiCad-Recovered/reports/expected-nets.json').read_text()).items() for pin in ps}
changes=[]
for e in SOURCE['elements'].values():
    ref=e['label']; pr=properties(e)
    nr=SOURCE['pcbLayoutNodes'][e['uid']]['pcbNodeRuleSet']
    xy=[scalar(v) for v in nr['position']['value'].split()[:2]]
    terms=[]
    for tid,t in e['part_version_data_cache'].get('terminals',{}).items():
        pn=str(t.get('pin_number') or SOURCE['pcbLayoutNodes'][e['uid']+'__'+tid]['terminalId'])
        terms.append({'number':pn,'name':t.get('name',pn),'type':'passive','net':netmap.get((ref,pn))})
    value=next((str(pr[k]) for k in ['Resistance','Capacitance','Inductance','Manufacturer Part Number'] if pr.get(k) not in (None,'')),e['part_version_data_cache'].get('name',ref))
    components[ref]={'ref':ref,'uuid':e['uid'],'value':value,'properties':pr,'pins':terms,
      'position':[150+xy[0],100-xy[1]],'angle':scalar(nr.get('rotationZ',nr.get('rotation',{})).get('value',0)),
      'side':nr.get('layer',{}).get('value','Top'),'source':'Flux','group':pr.get('Functional Group','Other')}

def connect(ref,pin,net):
    p=next(p for p in components[ref]['pins'] if p['number']==str(pin)); p['net']=net
def set_value(ref,value):components[ref]['value']=value
def part(ref,mpn,footprint,description=None):
    c=components[ref]; c['properties']['Manufacturer Part Number']=mpn; c['footprint']=footprint
    if description:c['properties']['Role Details']=description
def add(ref,value,pins,footprint,group,pos,mpn='',kind='passive'):
    components[ref]={'ref':ref,'uuid':ident(ref),'value':value,'properties':{'Manufacturer Part Number':mpn},
       'pins':[{'number':str(p),'name':str(p),'type':kind,'net':n} for p,n in pins.items()],
       'footprint':footprint,'group':group,'position':list(pos),'angle':0,'side':'Top','source':'RevB'}
def official(ref,lib,sym,mpn,group,pos,fp=None):
    tree=parse((KICAD/'symbols'/(lib+'.kicad_sym')).read_text(encoding='utf-8'))
    node=next(n for n in tree if isinstance(n,list) and n[:2]==['symbol',sym])
    pins={next(walk(p,'number'))[1]:{'number':next(walk(p,'number'))[1],'name':next(walk(p,'name'))[1],'type':p[1],'net':None} for p in walk(node,'pin')}
    footprint=fp or next(n[2] for n in node if isinstance(n,list) and n[:2]==['property','Footprint'])
    components[ref]={'ref':ref,'uuid':ident(ref),'value':mpn,'properties':{'Manufacturer Part Number':mpn},
        'pins':list(pins.values()),'footprint':footprint,'group':group,'position':list(pos),
        'angle':0,'side':'Top','source':'RevB','official_symbol':lib+':'+sym}

# Replace the incompatible controller and the RMII-only PHY plus its support parts.
removed=[]
for ref,c in list(components.items()):
    if c['group'] in ['Ethernet PHY','Ethernet PHY Clock','RMII Clock'] or ref in ['U2','R10','R40']:
        removed.append(ref); del components[ref]
changes.append({'change':'Replace ESP32-WROVER/RMII subsystem with ESP32-S3 and W5500','removed':sorted(removed)})
official('U2','RF_Module','ESP32-S3-WROOM-1','ESP32-S3-WROOM-1U-N16R8','Controller',(143,70),'RF_Module:ESP32-S3-WROOM-1U')
official('U3','Interface_Ethernet','W5500','W5500','Ethernet',(118,69))
# Pin 36 INT is output according to W5500 Table 2; correct the installed library.
next(p for p in components['U3']['pins'] if p['number']=='36')['type']='output'
# Module pin numbers, not GPIO numbers. Avoid Octal PSRAM GPIO35/36/37.
s3={1:'GND',2:'3V3',3:'ESP_EN',4:'PDM_CLK_MCU',5:'PDM_DATA0',6:'PDM_DATA1',7:'PDM_DATA2',12:'PDM_DATA3',
    17:'I2S_BCLK',18:'I2S_LRCLK',19:'I2S_DATA',20:'ETH_SPI_SCLK_MCU',21:'ETH_SPI_MOSI_MCU',22:'ETH_SPI_MISO',
    8:'ETH_SPI_CS_N',9:'ETH_INT_N',11:'I2C_SDA',23:'I2C_SCL',39:'RING_GPIO_SPARE',38:'IOX_INT_N',
    31:'IOX_nRESET',27:'BOOT_GPIO0',36:'UART0_RX',37:'UART0_TX',40:'GND',41:'GND'}
for p,n in s3.items():connect('U2',p,n)
# Hardware-mode/reset interface remains on the existing GPIO expander.
connect('U11',1,'IOX_INT_N')
for ref,c in components.items():
    if ref=='U2':continue
    for p in c['pins']:
        if p['net']=='RMII_REF_CLK':p['net']='BOOT_GPIO0' # SW2/J5 boot access
        elif p['net']=='RMII_REF_CLK_SRC':p['net']=None
        elif p['net']=='RMII_CLK_EN':p['net']=None

eth={1:'ETH_TX_N',2:'ETH_TX_P',3:'GND',4:'ETH_3V3A',5:'ETH_RX_N',6:'ETH_RX_P',8:'ETH_3V3A',9:'GND',10:'ETH_EXRES',
     11:'ETH_3V3A',14:'GND',15:'ETH_3V3A',16:'GND',17:'ETH_3V3A',19:'GND',20:'ETH_TOCAP',21:'ETH_3V3A',
     22:'ETH_1V2',23:'GND',24:'PHY_SPEED_LED',25:'PHY_LINK_LED',28:'3V3',29:'GND',30:'ETH_25MHZ',
     32:'ETH_SPI_CS_N',33:'ETH_SPI_SCLK',34:'ETH_SPI_MISO',35:'ETH_SPI_MOSI',36:'ETH_INT_N',37:'PHY_nRESET',
     43:'3V3',44:'3V3',45:'3V3',48:'GND'}
for p,n in eth.items():connect('U3',p,n)

# The original export used PHY-side center taps for PoE: correct to cable-side taps.
for p,n in {1:None,7:None,12:'ETH_TX_CT',6:'ETH_RX_CT',13:'POE_MODE_A_AC1',14:'POE_MODE_A_AC2',15:'POE_MODE_B_AC1',16:'POE_MODE_B_AC2'}.items():
    connect('J1',p,n)
changes.append({'change':'PoE pickup moved from PHY-side CT pins to cable-side CT pins','old_pins':[12,6,1,7],'new_pins':[13,14,15,16]})

# Ethernet analog supply/termination and MCU boot support.
RFP='Resistor_SMD:R_0603_1608Metric'
CFP='Capacitor_SMD:C_0603_1608Metric'
def resistor(ref,value,a,b,pos,group='Ethernet',mpn=''):
    add(ref,value,{'1':a,'2':b},RFP,group,pos,mpn)
def capacitor(ref,value,a,b,pos,group='Ethernet',footprint=CFP):
    add(ref,value,{'1':a,'2':b},footprint,group,pos)
    components[ref]['properties'].update({'Voltage Rating':'16V','Dielectric':'X7R'})
resistor('R100','12.4k','ETH_EXRES','GND',(112,75))
resistor('R101','49.9','ETH_TX_P','ETH_3V3A',(108,64))
resistor('R102','49.9','ETH_TX_N','ETH_3V3A',(108,67))
resistor('R103','10','ETH_3V3A','ETH_TX_CT',(106,60))
resistor('R104','49.9','ETH_RX_P','ETH_RX_TERM',(108,71))
resistor('R105','49.9','ETH_RX_N','ETH_RX_TERM',(108,74))
capacitor('C100','22nF','ETH_TX_CT','GND',(106,57))
capacitor('C101','6.8nF','ETH_RX_CT','GND',(102,74))
capacitor('C102','10nF','ETH_RX_TERM','GND',(108,77))
capacitor('C103','4.7uF','ETH_TOCAP','GND',(119,76),footprint='Capacitor_SMD:C_0805_2012Metric')
capacitor('C104','10nF','ETH_1V2','GND',(123,76))
for i,pos in enumerate([(111,69),(112,72),(115,76),(118,61),(122,62),(125,66)]):
    capacitor('C'+str(105+i),'100nF','ETH_3V3A','GND',pos)
capacitor('C111','10uF','ETH_3V3A','GND',(110,80),footprint='Capacitor_SMD:C_0805_2012Metric')
capacitor('C112','100nF','3V3','GND',(125,73))
capacitor('C113','10uF','3V3','GND',(126,77),footprint='Capacitor_SMD:C_0805_2012Metric')
add('FB2','120R@100MHz',{'1':'3V3','2':'ETH_3V3A'},RFP,'Ethernet',(113,81),'BLM18PG121SN1D')
resistor('R106','10k','3V3','PHY_nRESET',(126,66))
capacitor('C114','1uF','PHY_nRESET','GND',(129,66))
resistor('R107','10k','3V3','ETH_SPI_CS_N',(130,70))
resistor('R108','33','ETH_SPI_SCLK_MCU','ETH_SPI_SCLK',(132,74))
resistor('R109','33','ETH_SPI_MOSI_MCU','ETH_SPI_MOSI',(132,77))
# 25 MHz LVCMOS oscillator permits a grounded supply and a simple four-pad footprint.
add('X2','25MHz',{'1':'3V3','2':'GND','3':'ETH_25MHZ','4':'3V3'},'Oscillator:Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm','Ethernet',(125,81),'ASE-25.000MHZ-LC-T')
capacitor('C115','100nF','3V3','GND',(130,81))
resistor('R110','10k','3V3','BOOT_GPIO0',(135,55),'Controller')
resistor('R111','10k','3V3','IOX_INT_N',(152,76),'Controller')
# Keep strapping GPIO3/45/46 unused. Their default pulls/eFuse settings are authoritative.
changes.append({'change':'GPIO allocation and native four-line PDM RX moved to ESP32-S3','pin_map':s3})
connect('TP10','1','ETH_SPI_SCLK')
connect('TP11','1','ETH_SPI_MOSI')
changes.append({'change':'Repurpose obsolete RMII management test points for SPI clock and MOSI','references':['TP10','TP11']})

# Power review: PC817 collectors require a pull-up to produce a logic high
# while the optocoupler is off. The source accidentally grounded both ends
# of the collector/pull-resistor circuit when the transistor was on.
for ref in ['R6','R7','R8']:
    connect(ref,'2','3V3')
    components[ref]['properties']['Role Details']='10k pull-up to 3.3 V; class detection asserted low by PC817 collector'
changes.append({'change':'Correct PoE detector collector pull-ups from GND to 3V3','references':['R6','R7','R8']})
# TI LMR33630-Q1 datasheet section 5 explicitly requires pin 3 (NC) to
# connect to SW on the RNX VQFN package, for the bootstrap capacitor path.
connect('U6','3','BUCK5_SW')
changes.append({'change':'Connect LMR33630 RNX pin 3 to SW as required by TI','references':['U6']})

# Fix footprint/value mismatches from the source's generic capacitor assets.
for ref,c in components.items():
    if c['source']!='Flux':continue
    pkg=c['properties'].get('Package','')
    if ref.startswith('C') and re.fullmatch(r'SMD_\d{4}_\d{4}Metric',pkg):
        c['footprint']='Capacitor_SMD:C_'+pkg.removeprefix('SMD_')
    elif ref.startswith('R') and re.fullmatch(r'SMD_\d{4}_\d{4}Metric',pkg):
        c['footprint']='Resistor_SMD:R_'+pkg.removeprefix('SMD_')
for ref,mpn,diam,pitch in [('C1','EEUFR1E102',10,5),('C2','EEUFR1E102',10,5),('C3','EEUFR1V102',12.5,5),('C4','EEUFR1V102',12.5,5),('C5','EEUFR1H101',8,3.5),('C6','EEUFR1H101',8,3.5)]:
    part(ref,mpn,f'Capacitor_THT:CP_Radial_D{diam:.1f}mm_P{pitch:.2f}mm')
    components[ref]['properties']['Polarity']='Pin 1 positive, pin 2 negative'
    components[ref]['side']='Top'
changes.append({'change':'Replace six 100/1000 uF capacitors on generic 0603 pads with specified Panasonic radial parts','references':['C1','C2','C3','C4','C5','C6']})
for ref in ['L1','L2']:
    part(ref,'SRP1038A-100M','SpeakerRevB:SRP1038A','10 uH shielded, 7.5 A Irms, 12 A Isat; verify thermal performance')
part('L3','XAL5050-822MEC','SpeakerRevB:XAL50xx','8.2 uH shielded buck inductor');set_value('L3','8.2uH')
part('L4','XAL5030-222MEC','SpeakerRevB:XAL50xx','2.2 uH shielded buck inductor')
changes.append({'change':'Replace generic 1210 power-inductor pads with rated shielded inductors','references':['L1','L2','L3','L4']})


# PoE bridge voltage-margin revision; retain recovered SMC geometry and pin numbering.
for ref in [f'D{i}' for i in range(3,11)]:
    components[ref]['value']='B5100C'
    components[ref]['properties'].update({'Manufacturer Part Number': 'B5100C', 'Manufacturer Name': 'Diodes Incorporated', 'Datasheet URL': 'https://www.diodes.com/datasheet/download/B5100C.pdf', 'Reverse Voltage': '100', 'Forward Voltage': '0.85 V max at 5 A', 'Package or Case Code': 'SMC (DO-214AB)', 'LCSC Part Number': '', 'JLCPCB Part Class': '', 'Role Details': 'PoE bridge: 100 V draft replacement; thermal and transient qualification pending'})
changes.append({'change':'Replace 60 V SS56 bridges with 100 V B5100C; thermal/transient qualification pending','references':[f'D{i}' for i in range(3,11)]})

# Consolidate sheets by circuit function; retain the finer functional group as metadata.
def sheet(c):
    g=c['group']
    if g in ['Controller','MCU Support','Debug','MCU and Ethernet MAC']:return 'Controller and programming'
    if g=='Ethernet' or g in ['Ethernet and PoE Primary','Ethernet Protection','Status LEDs']:return 'Ethernet interface'
    if 'PoE' in g:return 'PoE input and isolation'
    if g in ['Secondary Regulators','5 V Buck','3.3 V Buck','3.3 V Rail','Power Good','24 V Power ORing','Bench Power Input','24 V Amplifier Rail']:return 'Power conversion'
    if 'Playback' in g or g in ['DAC LDO','I2S']:return 'Playback DAC'
    if 'Class-D' in g or g=='Speaker Output':return 'Speaker amplifier'
    if g in ['Microphone Ring Interface','PDM and I2S Damping','I2C','I2C Expansion','GPIO Expander','Clock and GPIO Expander','Control and Power Policy']:return 'Microphone and control'
    return 'Test points and mounting'
for c in components.values():c['sheet']=sheet(c)
layout_file=BASE/'engineering/layout-overrides.json'
if layout_file.exists():
    for ref,placement in json.loads(layout_file.read_text()).items():
        if ref in components:
            for key in ['position','angle','side']:components[ref][key]=placement[key]

model={'revision':'B-development','status':'Electrical redesign in progress; not released for fabrication',
       'intent':{'speaker':'30 W into 4 ohms, source target pending actual driver selection','microphones':8,'ring':'separate future PCB','controller':'ESP32-S3-WROOM-1U-N16R8','ethernet':'W5500 SPI 10/100','board_outline_proposal_mm':[160,100],'mounting_hole_spacing_mm':[150,90]},
       'components':components,'changes':changes}
if __name__=='__main__':
    out=BASE/'engineering/revision-b-design.json'; out.write_text(json.dumps(model,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Saved',out,'with',len(components),'components')

