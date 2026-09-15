from pathlib import Path
import json,hashlib,shutil
D=Path('KiCad-RevE'); E=Path('engineering')
f=D/'reports/rx-front-layer-probe.json';r=json.loads(f.read_text());d=json.loads((D/'reports/ethernet-trial-drc.json').read_text())
assert hashlib.sha256((D/'PoE-Speaker-RevE.kicad_pcb').read_bytes()).hexdigest()==r['main_sha256']
assert len(d['violations'])==8 and not d['unconnected_items']
r.update(status='rejected; validated main unchanged',drc_findings=8,unconnected_items=0,findings=d['violations'])
f.write_text(json.dumps(r,indent=2))
note='''

## 2026-09-15: front-layer RX feasibility probe

Promoted the five existing In2 RX segments to F.Cu at the sourced width in a separate trial. DRC found eight errors, zero unconnected items. Rejected; main copper remains unchanged. Detailed UUIDs/positions are in reports/rx-front-layer-probe.json. The trial is not a coupled pair and is excluded from release archives.

Obstacles are concentrated in the Ethernet circuit: TX_N routing at the jack and toward U3, TX_P routing to R101, R101 pad 1, and ETH_3V3A feeding the transmit termination. A layer-only conversion cannot solve these crossings. Do not repeat this same probe as the next chunk.

Next: coordinate all four MDI routes and R101/R102 supply branches, rather than routing RX in isolation. Preserve jack/PHY pin polarity. Plan the jack fanout first, then main coupled corridors, followed by short ESD/termination taps. R101/R102 placement and analog-supply access must be included in the same trial. RX bottom termination and ESD paths also remain part of final qualification. Keep the main unchanged until the full proposal has clean DRC and pin mapping.
'''
with (E/'ETHERNET-STACKUP.md').open('a',encoding='utf-8') as out:out.write(note)
with (E/'REVE-TRUNK-ROUTING.md').open('a',encoding='utf-8') as out:out.write(note)
f=E/'package_prototype_review.py';s=f.read_text();s=s.replace('Next: reroute Ethernet using the sourced Ethernet100 preset', 'Next: coordinate all four Ethernet MDI routes plus R101/R102 placement and supply branches; the RX-only front-layer probe was rejected with eight crossing/short/mask errors (reports/rx-front-layer-probe.json), main unchanged. Do not repeat that layer-only probe. Reroute using the sourced Ethernet100 preset');f.write_text(s,encoding='utf-8')
print('Rejected probe documented; main hash verified unchanged.')
