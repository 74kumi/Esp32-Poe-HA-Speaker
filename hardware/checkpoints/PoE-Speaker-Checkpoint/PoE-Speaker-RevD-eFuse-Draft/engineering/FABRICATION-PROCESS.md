# Provisional fabrication process — not a production release

Reviewed 2026-09-12. The layout retains a 0.20 mm track/clearance default and 0.30 mm ordinary drill minimum. A scoped rule permits the existing grounded thermal vias in U2 and U16: 12 and 9 holes respectively, 0.20 mm drill, with 0.60 mm and 0.50 mm copper diameters. No hole geometry was changed and no DRC category was disabled.

JLCPCB is a capability reference, not a selected supplier or an order. Its rigid-board capability table lists 0.20 mm as a preferred minimum via drill. These thermal vias must be identified to CAM as vias rather than component insertion holes. Source: https://jlcpcb.com/capabilities/pcb-capabilities

Procurement must specify and confirm the treatment of exposed-pad vias, preferably filled and copper capped where they intersect solderable lands, plus stencil apertures, finish, stackup and copper weights. Simple open holes may wick solder and compromise the thermal joint. The present drill rule does not approve the assembly process, solder volume or thermal performance. Do not release fabrication until those requirements are included in the quote and accepted.

The U16 land pattern includes a 2.7 mm exposed pad and nine thermal vias; TI's RGE0024H drawing shows a typical 0.20 mm thermal drill. U2 thermal lands remain as supplied in the KiCad module footprint. Component sources:

- https://www.ti.com/lit/ds/symlink/tps2663.pdf
- https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf

Remaining release work includes power/ground thermal copper, switching loops, Ethernet return paths and impedance, fault/startup review, exact order codes, five schematic ERC findings, and mechanical fit. A clean DRC with this profile is a geometry milestone only.
