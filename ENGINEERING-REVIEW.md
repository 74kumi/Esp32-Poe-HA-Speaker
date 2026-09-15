# Engineering review request

This project is approaching a first prototype and has not been fabricated, assembled or electrically validated. Please start with the latest Rev E sources, not an earlier revision or a trial file. Current release status is **HOLD**.

## Open the design

Open `KiCad-RevE/PoE-Speaker-RevE.kicad_pro` in KiCad 10. Keep the adjacent `SpeakerRevB.pretty` library, tables and custom design rules together. The library name is historical and intentional. The saved board has 209 components and 616 connected pins. The latest checked source hash is in `KiCad-RevE/reports/revision-status.json`.

Review the current board (`KiCad-RevE/PoE-Speaker-RevE.kicad_pcb` in the extracted source package), schematic (`KiCad-RevE/PoE-Speaker-RevE.kicad_sch` in the extracted source package), release review (`engineering/ORDER-RELEASE-REVIEW.md` in the extracted source package) and connector guide (`engineering/CONNECTOR-GUIDE.md` in the extracted source package). Candidate component data is in `KiCad-RevE/reports/procurement-audit.json`; availability and suitability are not procurement-approved.

## Highest-value questions

1. **Ethernet:** Verify W5500/2250506-1 jack wiring and polarity, magnetics center taps, ESD topology, termination taps, reference continuity and differential impedance. RX has a coupled front-layer trunk, but branch discontinuities remain. TX routing still needs work. See stackup and routing notes (`engineering/ETHERNET-STACKUP.md` in the extracted source package).
2. **Power and faults:** Review PoE/bench input arbitration, protection thresholds and tolerances, startup/inrush, fuse coordination, transient limits, conductor/via current capability and fault behavior. See eFuse review (`engineering/EFUSE-REVIEW.md` in the extracted source package) and fuse review (`engineering/FUSE-RATING-REVIEW.md` in the extracted source package).
3. **Audio and regulators:** Check PCM5122/TPA3116D2 configuration, output-filter values, bootstrap/GVDD paths, power/ground loops, regulator compensation and effective capacitor values. The 30 W / 4 ohm target needs measured validation.
4. **Assembly and thermal:** Check footprint pin maps, polarity/orientation, top heatsink, PoE module support, connector access, underside component clearance and the 13 assembly footprints still lacking verified courtyards. Resolve thermal via-in-pad treatment before fabrication.

## What the reports prove

Saved DRC and ERC reports are clean under the saved profile. Model/schematic/PCB connected-pin mappings agree. Missing courtyard checks and some inherited metadata checks are disabled; clean reports do not certify the circuit. Path-length, ground-contact and width scripts are geometry screens, not signal-integrity, ampacity or thermal solvers.

No manufacturing package is approved. Review ZIPs are source checkpoints, not order files. Firmware, the future microphone board, enclosure design and bench validation are incomplete.

## Useful review submissions

Use an issue with the checked PCB hash, KiCad version, reference/pin/net, coordinate or screenshot, expected behavior, observed problem and source evidence. Distinguish a definite defect from a question or suggested improvement. A proposed patch should retain DRC/connectivity checks and explain any rule exclusions. Do not submit supplier orders or claim a build has been tested unless it has.

## Reproducing local checks

The current scripts target a Windows KiCad 10 installation and contain local runtime paths. Adapt those paths before running elsewhere. `engineering/checkpoint_reve.py` runs board DRC, serialization checks, geometry audits and source packaging; the saved ERC report must also be regenerated after schematic edits. Historical acceptance/trial scripts are not a clean project generator and may require a particular previous board hash.
