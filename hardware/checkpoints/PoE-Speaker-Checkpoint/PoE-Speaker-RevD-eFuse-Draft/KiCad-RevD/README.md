# Revision D — shared current protection draft

Open PoE-Speaker-RevD.kicad_pro in KiCad 10. This editable development board is not approved for fabrication or power-up. Revisions B and C remain preserved.

Added TPS26630RGER after the bench/PoE ideal-diode junction, feeding all original 24V_AMP loads. The circuit targets a nominal 2.98 A current limit, latch-off behavior, controlled startup and power-good amplifier shutdown interlock. TP26 is the shutdown/reset point; TP27 exposes the fault output. See engineering/EFUSE-REVIEW.md for calculations and limitations. Eight microphones remain assigned to a future separate ring board.

The 210 x 100 mm provisional outline is unchanged from C. Retained routes were reused except the two nets split by this change. The secondary In1.Cu ground plane now extends under Ethernet while excluding the lower-left primary/module region. See reports/secondary-ground.png. The routing preview omits that plane so signal routing is visible.

Validation: all 616 connected model pins match both the schematic netlist and PCB pad nets. Specific checks confirm the eFuse supply split and amplifier interlock. Exact physical and electrical findings are below; an empty ratsnest does not establish electrical correctness. Most imported symbols still use boxed pin representations, and source electrical pin types need further review.

Release blockers: resolve remaining DRC and ERC findings; qualify high-current widths/vias and thermal copper; finish Ethernet impedance and return paths, switching loops, input transient/fuse coordination, hot-start and overload behavior, and exact passive order codes. U15 now uses the manufacturer-recommended 1.22 x 0.40 mm lands at 0.65 mm pitch. All narrow-track escapes have been repaired without relaxing rules. The 21 thermal vias are covered by a scoped 0.20 mm drill-process rule; see engineering/FABRICATION-PROCESS.md. DRC is clean under that documented profile, but assembly via treatment and final stackup require confirmation. The enclosure, mounting and final speaker are not fixed. No manufacturing release is included.

Do not rerun build_efuse_revision.py on this routed folder without first archiving it: generation recreates placement and removes later routing work.

## Saved validation counts

- revision: D shared eFuse development draft
- components: 209
- board_mm: [210, 100]
- track_segments: 2101
- vias: 264
- ground_zones: 1
- unconnected_items: 0
- drc: {}
- erc_findings: 5
- poe_isolation_findings: 0
- fabrication_ready: False
