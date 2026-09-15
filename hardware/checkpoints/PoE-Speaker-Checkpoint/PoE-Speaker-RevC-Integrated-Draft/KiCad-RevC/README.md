# Revision C — integrated prototype development

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
