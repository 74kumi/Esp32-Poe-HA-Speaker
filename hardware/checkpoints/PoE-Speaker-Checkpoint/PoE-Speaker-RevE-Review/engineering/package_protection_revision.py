from pathlib import Path
import json,collections,zipfile,hashlib,pcbnew as p
D=Path('KiCad-RevC');E=Path('engineering');d=json.loads((D/'reports/board-drc.json').read_text());b=p.LoadBoard(str(D/'PoE-Speaker-RevC.kicad_pcb'))
counts=dict(collections.Counter(v['type'] for v in d['violations']))
iso=[v for v in d['violations'] if 'PoE primary' in v['description']]
report={'revision':'C integrated protection draft','components':len(list(b.GetFootprints())),'board_mm':[210,100],'track_segments':sum(not isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'vias':sum(isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'ground_zones':len(list(b.Zones())),'unconnected_items':len(d['unconnected_items']),'drc':counts,'poe_isolation_findings':len(iso),'fabrication_ready':False}
assert report['unconnected_items']==0 and not iso and not counts.get('shorting_items',0)
(D/'reports/revision-status.json').write_text(json.dumps(report,indent=2))
readme='''# Revision C — integrated prototype development

Open PoE-Speaker-RevC.kicad_pro in KiCad 10. This is an editable engineering draft, not a board approved for manufacture or power-up. Revision B is preserved separately.

Implemented: bench-input LTC4365HTS8 disconnect, two PSMN4R8-100BSE pass MOSFETs, UV/OV dividers, controlled-startup candidate network, bidirectional input TVS selection, fault test point, and amplifier shutdown pulldown. The protection schematic is integrated into the project and its connections are routed. The provisional outline is expanded to 210 x 100 mm; mounting and enclosure fit are not final.

Added a partial secondary-side In1.Cu ground plane from x=140 to 279 mm, leaving the Ethernet area outside this plane. Widened 14 new power-route segments to 0.8 mm where DRC permitted. Improved reference placement and turned schematic net labels outward for readability. Source symbols remain boxed pin representations.

Verification: 194 footprints, 575 connected pins match the design model, zero unconnected items, no reported shorts or PoE isolation-rule findings. The preliminary 3 mm rule is not an insulation certification. See reports/revision-status.json and board-drc.json for exact counts. ERC retains four undriven power-input findings and many source pin types remain unreviewed.

Release blockers:

- Short-circuit current limiting, fuse coordination, and repetitive-fault heating are unresolved. The startup ramp is not a fault current limiter.
- Confirm gate-drive capability, MOSFET hot SOA, actual startup loads, amplifier-disable sequencing, and bench/PoE backfeed using the complete circuit.
- Finalize resistor/capacitor/TVS order codes, tolerances, voltage ratings, and transient envelope. Several new passive MPNs remain TBD.
- Six U15 pad-spacing findings reflect 0.15 mm footprint gaps against the 0.20 mm project constraint; qualify the fabrication process/land pattern. Do not simply suppress them.
- Resolve 57 narrow-track findings and 12 ESP32 footprint drill findings. Widths and via current capacity are not thermally qualified.
- Finish Ethernet impedance/return paths, switching-loop layout, ground/thermal copper, silkscreen, mechanical fit and remaining source circuit review.

No manufacturing Gerbers are included. The PNG is a routing preview with F.Cu, In2.Cu and B.Cu; the inner ground plane is intentionally not shown in that view.

Preservation: build_protection_revision.py regenerates the initial placement and will overwrite this layout if rerun. Copy/archive this project before regeneration. Subsequent routing, fill, width and label changes are in the saved PCB and separate engineering scripts.
'''
(D/'README.md').write_text(readme,encoding='utf-8')
(E/'RESUME-HERE.md').write_text('# Resume checkpoint\n\nLatest deliverable: KiCad-RevC/PoE-Speaker-RevC.kicad_pro and PoE-Speaker-RevC-Integrated-Draft.zip. Bench protection is now integrated and routed; partial secondary plane added; references cleaned; 14 power segments widened. Read KiCad-RevC/README.md for exact blockers. Revision B preserved.\n\nNext work: complete fault-current limiting and startup/gate-drive validation; resolve U15 pad spacing, narrow tracks, module drill constraints, remaining silk and source electrical review. Do not mistake zero unconnected items for fabrication approval. Preserve routed C before running generators.\n',encoding='utf-8')
with zipfile.ZipFile('PoE-Speaker-RevC-Integrated-Draft.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in D.rglob('*'):
  if f.is_file() and ('reports' not in f.parts or f.name in ['revision-status.json','board-drc.json','net-validation.json','schematic-erc.json','revision-c-board.png','revision-c-board.svg','bench-protection-detail.png','protection-widths.json','schematic-netlist.xml']):z.write(f,str(f))
 for f in [E/'revision-c-design.json',E/'RESUME-HERE.md',E/'build_protection_revision.py',E/'validate_protection.py']:z.write(f,str(f))
with zipfile.ZipFile('PoE-Speaker-RevC-Integrated-Draft.zip') as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('Archive verified')
