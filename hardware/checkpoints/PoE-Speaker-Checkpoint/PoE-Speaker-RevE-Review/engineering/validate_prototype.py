from pathlib import Path
import json,xml.etree.ElementTree as X,collections
D=Path('KiCad-RevE');m=json.loads(Path('engineering/revision-e-design.json').read_text());tree=X.parse(D/'reports/schematic-netlist.xml');actual={}
for n in tree.findall('.//nets/net'):
 for p in n.findall('node'):actual[(p.attrib['ref'],p.attrib['pin'])]=n.attrib['name']
errors=[]
for ref,c in m['components'].items():
 for p in c['pins']:
  if p['net'] and actual.get((ref,p['number']))!=p['net']:errors.append([ref,p['number'],p['net'],actual.get((ref,p['number']))])
assert not errors,errors
assert actual['F1','2']=='BENCH_FUSED'
assert actual['Q3','2']=='BENCH_FUSED' and actual['Q4','2']=='24V_BENCH_PROTECTED'
assert actual['Q3','3']==actual['Q4','3']=='BENCH_COMMON_SOURCE'
assert actual['R129','1']=='AMP_SDZ' and actual['R129','2']=='GND'
for ref,pin in [('Q1','2'),('Q2','2'),('U9','6'),('U10','6'),('U16','1'),('U16','2'),('U16','5')]:assert actual[ref,pin]=='24V_OR'
for pin in ['17','18']:assert actual['U16',pin]=='24V_AMP'
assert actual['U11','4']==actual['R135','1']=='AMP_ENABLE_CMD'
assert actual['U16','16']==actual['R135','2']==actual['U5','2']=='AMP_SDZ'
for pin in ['3','4','11','13','19','20','21','22','23','24']:assert not next(p['net'] for p in m['components']['U16']['pins'] if p['number']==pin)
import pcbnew as pcb
b=pcb.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'))
bp={(f.GetReference(),pad.GetNumber()):pad.GetNetname() for f in b.GetFootprints() for pad in f.Pads() if pad.GetNumber()}
for ref,c in m['components'].items():
 for pin in c['pins']:
  if pin['net']:assert bp.get((ref,pin['number']))==pin['net'],(ref,pin)
report={'pcb_pad_mapping':'PASS','logical_mapping':'PASS','components':len(m['components']),'connected_pins':sum(bool(p['net']) for c in m['components'].values() for p in c['pins']),'new_protection_reference_checks':'PASS','limits':'Electrical serialization only; not fault protection or circuit performance approval'}
(D/'reports/net-validation.json').write_text(json.dumps(report,indent=2));print(report)
