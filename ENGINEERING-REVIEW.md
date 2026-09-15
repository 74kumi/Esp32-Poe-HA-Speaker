# Engineering review request

This project is approaching a first prototype and has **not** been fabricated, assembled, or electrically validated. Please review the current Rev E source rather than an earlier checkpoint or trial file. Current release status is **HOLD**.

## Open the design

Open [`hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pro`](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pro) in **KiCad 10**.

Keep the adjacent `SpeakerRevB.pretty` footprint library, `SpeakerRevB.kicad_sym` symbol library, library tables, and custom design rules together. The `SpeakerRevB` library name is historical and intentional.

The saved Rev E board contains 209 components and 616 connected pins. The latest checked source hash is recorded in `hardware/PoE-Speaker/RevE/KiCad-RevE/reports/revision-status.json`.

Useful starting points:

- [Current PCB](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pcb)
- [Current schematic](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_sch)
- [Rev E engineering notes](hardware/PoE-Speaker/RevE/engineering/)
- [Order / release review](ORDER-RELEASE-REVIEW.md)
- [Connector guide](hardware/PoE-Speaker/RevE/engineering/CONNECTOR-GUIDE.md)
- [Ethernet stackup / routing notes](hardware/PoE-Speaker/RevE/engineering/ETHERNET-STACKUP.md)

Candidate component data is recorded in `hardware/PoE-Speaker/RevE/KiCad-RevE/reports/procurement-audit.json`; availability and suitability are not procurement-approved.

## Highest-value review questions

1. **Ethernet** — Verify W5500 / 2250506-1 jack wiring and polarity, magnetics center taps, ESD topology, termination taps, reference continuity, and differential impedance. RX has a coupled front-layer trunk, but branch discontinuities remain. TX routing still needs work. See [ETHERNET-STACKUP.md](hardware/PoE-Speaker/RevE/engineering/ETHERNET-STACKUP.md).
2. **Power and faults** — Review PoE / bench-input arbitration, protection thresholds and tolerances, startup / inrush, fuse coordination, transient limits, conductor / via current capability, and fault behavior. See [EFUSE-REVIEW.md](hardware/PoE-Speaker/RevE/engineering/EFUSE-REVIEW.md) and [FUSE-RATING-REVIEW.md](hardware/PoE-Speaker/RevE/engineering/FUSE-RATING-REVIEW.md).
3. **Audio and regulators** — Check PCM5122 / TPA3116D2 configuration, output-filter values, bootstrap / GVDD paths, power / ground loops, regulator compensation, and effective capacitor values. The 30 W / 4 ohm target requires physical measurement.
4. **Assembly and thermal** — Check footprint pin maps, polarity / orientation, top heatsink, PoE-module support, connector access, underside clearance, remaining courtyard gaps, and thermal via-in-pad treatment.

## What the saved reports prove

Saved DRC and ERC reports are clean under the saved profile, and model / schematic / PCB connected-pin mappings agree.

They do **not** certify the circuit. Missing-courtyard checks and some inherited metadata checks are disabled, and the project-specific path-length, ground-contact, and width scripts are geometry screens rather than signal-integrity, ampacity, or thermal solvers.

No manufacturing package is currently approved. Firmware, the microphone-ring hardware, enclosure work, and bench validation remain incomplete.

## Useful review submissions

Please open a GitHub issue and include, where applicable:

- checked PCB hash / source revision;
- KiCad version;
- component, pin, and net;
- coordinate or screenshot;
- expected behavior;
- observed concern; and
- datasheet section, calculation, or other supporting evidence.

Distinguish a confirmed defect from a question or suggested improvement. Proposed patches should retain DRC / connectivity checks and explain any rule exclusions.

## Reproducing local checks

The current engineering scripts target a Windows KiCad 10 installation and some still contain local runtime paths. Adapt those paths before running them elsewhere.

`hardware/PoE-Speaker/RevE/engineering/checkpoint_reve.py` runs board DRC, serialization checks, geometry audits, and source packaging. The saved ERC report must also be regenerated after schematic edits.

Historical acceptance / trial scripts are preserved for traceability and may depend on a particular previous board hash; they are not a clean project generator.
