"""Compare the saved KiCad schematic and PCB against the explicit Rev B model."""
import collections,json,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as pcb
BASE=Path(__file__).resolve().parent.parent
R=BASE/'KiCad-RevB/reports'
m=json.loads((BASE/'engineering/revision-b-design.json').read_text(encoding='utf-8'))
expected={n:set(map(tuple,ps)) for n,ps in json.loads((R/'expected-nets.json').read_text()).items()}
tree=ET.parse(R/'schematic-netlist.xml')
actual={n.attrib['name']:{(p.attrib['ref'],p.attrib['pin']) for p in n.findall('node')} for n in tree.findall('.//nets/net')}
b=pcb.LoadBoard(str(BASE/'KiCad-RevB/PoE-Speaker-RevB.kicad_pcb'))
bp=collections.defaultdict(set)
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname():bp[p.GetNetname()].add((f.GetReference(),p.GetNumber()))
def diff(a):return {n:{'missing':sorted(ps-a.get(n,set())),'extra':sorted(a.get(n,set())-ps)} for n,ps in expected.items() if ps!=a.get(n,set())}
sd,bd=diff(actual),diff(bp)
nc={(ref,p['number']) for ref,c in m['components'].items() for p in c['pins'] if not p['net']}
extra={n:ps for n,ps in actual.items() if n not in expected}
assert not sd and not bd,(sd,bd)
assert {p for ps in extra.values() for p in ps}==nc
assert all(len(ps)==1 for ps in extra.values())
assert {f.GetReference() for f in b.GetFootprints()}==set(m['components'])
for pn,nm in [('13','POE_MODE_A_AC1'),('14','POE_MODE_A_AC2'),('15','POE_MODE_B_AC1'),('16','POE_MODE_B_AC2')]:assert ('J1',pn) in expected[nm]
for pn in ['28','29','30']:assert ('U2',pn) in nc # GPIO35/36/37 reserved by octal PSRAM
for ref in ['R6','R7','R8']:assert (ref,'2') in expected['3V3']
assert ('U6','3') in expected['BUCK5_SW']
report={'logical_mapping':'PASS','components':len(m['components']),'nets':len(expected),'connected_pins':sum(map(len,expected.values())),'no_connect_pins':len(nc),'schematic_differences':sd,'pcb_differences':bd,'tracks':len(list(b.GetTracks())),'fabrication_ready':False,'scope':'Verifies serialization and explicit design pin mapping, not circuit performance, ERC completeness, routing or physical operation.'}
(R/'net-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

