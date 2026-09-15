from pathlib import Path
import json,hashlib,shutil
D=Path('KiCad-RevE'); main=D/'PoE-Speaker-RevE.kicad_pro'
r=json.loads((D/'reports/ethernet-impedance-calculator.json').read_text())
assert hashlib.sha256(main.read_bytes()).hexdigest()==r['project_before_sha256']
assert hashlib.sha256((D/'PoE-Speaker-RevE.kicad_pcb').read_bytes()).hexdigest()==r['pcb_sha256']
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text()); assert not d['violations'] and not d['unconnected_items']
backup=D/'before-ethernet-pair-preset.kicad_pro'; assert not backup.exists()
shutil.copy2(main,backup); shutil.copy2(D/'ethernet-trial.kicad_pro',main)
f=Path('engineering/package_prototype_review.py'); s=f.read_text()
s=s.replace('Next: calculate and implement Ethernet differential geometry using the saved JLC04161H-7628 design baseline;', 'Next: reroute Ethernet using the sourced Ethernet100 preset (0.225806 mm width / 0.2032 mm gap), F.Cu over In1 GND on JLC04161H-7628;')
s=s.replace('pair widths/gaps still need calculation and fabricator confirmation.', 'the calculator-derived Ethernet100 routing preset is saved, but copper still needs rerouting and fabrication confirmation.')
f.write_text(s,encoding='utf-8')
f=Path('engineering/ETHERNET-STACKUP.md'); s=f.read_text()
start=s.index('Next implementation:'); end=s.index('\n\n',start)
s=s[:start]+'''Calculator result verified 2026-09-15: masked noncoplanar differential model, L1 over L2, 100 ohm target and 8 mil gap gives **8.89 mil width** on JLC04161H-7628. Exact conversions are 0.225806 mm width and 0.2032 mm edge gap. The source UI labels this standard stackup as finished thickness 1.59 mm +/-10%. The displayed impedance tolerance of 0.5% is a solver setting, not a manufacturing guarantee. Inputs/results are saved in reports/ethernet-impedance-calculator.json. Source: [fabricator calculator](https://jlcpcb.com/pcb-impedance-calculator).

The main KiCad project now assigns ETH_TX_P/N and ETH_RX_P/N to Ethernet100 with those differential routing defaults. Clearance and via defaults are retained. This changes no existing copper and does not add an enforcing width or pair-gap DRC rule; existing 0.2 mm tracks remain unqualified. Do not apply this noncoplanar result beside close same-layer ground copper without recalculating the coplanar geometry.

Next implementation: rework PHY/jack/ESD/termination placement and actual routes using the saved pair preset, preserving pin polarity. Inspect pair coupling, return corridors and jack isolation keepouts. Add enforcing rules only with the actual routing and explicit pad escape exceptions.''' + s[end:]
f.write_text(s,encoding='utf-8')
f=Path('engineering/ORDER-RELEASE-REVIEW.md'); s=f.read_text().replace('Choose stackup, calculate 100 ohm geometry, constrain and inspect pair routing.', 'The sourced Ethernet100 preset now supplies 100 ohm starting geometry: 0.225806 mm width / 0.2032 mm gap on F.Cu over In1 GND. Implement and inspect pair routing; these defaults do not constrain existing copper.')
f.write_text(s,encoding='utf-8')
f=Path('engineering/REVE-TRUNK-ROUTING.md')
with f.open('a',encoding='utf-8') as out: out.write('\n\n## 2026-09-15: sourced Ethernet routing preset\n\nVerified JLCPCB calculator output for JLC04161H-7628, masked noncoplanar L1/L2, 100 ohm, 8 mil gap: 8.89 mil width. Added Ethernet100 class with exact converted width 0.225806 mm and gap 0.2032 mm, assigned to the four MDI nets. Trial DRC zero/unconnected zero. Existing copper unchanged; this prepares actual rerouting and is not impedance qualification. Preserved before-ethernet-pair-preset.kicad_pro. The calculator tolerance setting is not a production guarantee.\n')
print('Accepted Ethernet100 defaults; main PCB unchanged.')
