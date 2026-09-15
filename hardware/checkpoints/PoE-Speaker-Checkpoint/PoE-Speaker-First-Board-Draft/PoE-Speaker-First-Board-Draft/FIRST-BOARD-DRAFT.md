# First board draft — review copy

Open `PoE-Speaker-RevB.kicad_pro` in KiCad 10. **Not for fabrication or power-up.**

The 160 × 100 mm draft contains 179 placed footprints, 1814 track segments and 222 vias. KiCad reports 0 unconnected items. The saved schematic and PCB pad assignments match the revised electrical model.

The body-box placement check passes. This is an initial placement and routing study; it does not validate enclosure fit, circuit operation or manufacturability.

## Current checks

| KiCad finding | Count |
|---|---:|
| drill_out_of_range | 12 |
| silk_edge_clearance | 1 |
| silk_over_copper | 84 |
| silk_overlap | 81 |
| track_width | 57 |

## Before a prototype order

- Complete the PoE and bench-input protection changes described in `POWER-REVIEW.md`.
- Redesign high-current routes. Net-specific wider trunks still have narrow escapes and unqualified vias and return paths.
- Add and review ground planes, isolation boundaries and thermal copper. Check buck and amplifier switching loops.
- The explicit 3 mm primary-to-secondary copper review rule now has zero findings. This is a preliminary layout target, not an insulation certification.
- Qualify or replace the U5 pin 27 via-in-pad escape for assembly and current capacity.
- Route Ethernet pairs to the chosen stackup and impedance requirements.
- Complete pin-type/ERC review, silkscreen cleanup and footprint/manufacturing checks. The ESP32 module footprint includes 0.2 mm thermal holes against a current 0.3 mm board constraint; resolve the footprint/process choice.
- Verify all release checks, then generate fabrication outputs. No manufacturing Gerbers are included in this review package.

The microphone ring remains a separate future board. The mainboard reserves its eight-microphone interface.
