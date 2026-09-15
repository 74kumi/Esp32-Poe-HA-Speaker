# Prototype order release review

**Updated:** 2026-09-14  
**Status:** **HOLD — not ready to order.**

The current board is [`hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pcb`](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pcb). No manufacturing package is approved by this document.

## Release priorities

| Area | Evidence / current state | Work required before order |
| --- | --- | --- |
| **Ethernet layout** | Saved routing reviews show TX and RX still include layer changes, branch taps, and signal vias. RX main-route work has improved the front-layer corridor and shortened / localized termination branches, but the current metrics are geometry screens rather than exact differential-pair skew or SI validation. | Rework PHY, termination, ESD, and jack routing as intentional differential pairs. The current Ethernet100 starting geometry is 0.225806 mm width / 0.2032 mm gap on F.Cu over In1 GND. Prefer no signal vias. Verify reference continuity, isolation keepouts, and actual fabrication stackup. |
| **Physical stackup** | JLC04161H-7628 is saved as the current planning baseline. See [ETHERNET-STACKUP.md](hardware/PoE-Speaker/RevE/engineering/ETHERNET-STACKUP.md). | Use the baseline for planning calculations, then confirm finished copper, dielectric thickness, plating, and impedance geometry with the selected fabricator before ordering. |
| **Mechanical coverage** | Eight B5100C courtyards have been added and checked. Thirteen non-feature footprints still lack verified courtyard graphics in the saved review. | Add / verify remaining body and assembly envelopes. Inspect underside components, connector access, PoE-module support, and amplifier heatsink clearance. |
| **Mounting** | H3 / H4 moved to `(275,55)` / `(275,145)`, 5 mm from the extended edge. Existing left holes are at `(75,55)` / `(75,145)`. | Use insulating M2 standoffs for the prototype. Enclosure fit remains unconfirmed. |
| **Power paths / ground** | Recent track, via, and decoupling improvements pass the saved DRC. Remaining constrained vias and amplifier-ground paths are documented. | Calculate current capability using actual copper / plating assumptions. Review regulator input / output loops and remaining amplifier ground access. Geometry audits do not provide a current rating. |
| **Fuse / protection** | F1's manufacturer publishes DC interrupt ratings. [EFUSE-REVIEW.md](hardware/PoE-Speaker/RevE/engineering/EFUSE-REVIEW.md) contains nominal settings and startup estimates. | Check source fault-current bounds, fuse timing / let-through, protection tolerances, and transient behavior. The 3.15 A fuse is not an instantaneous current clamp. |
| **Assembly process** | U2 / U16 currently use thermal vias in solderable pads. | Specify filled / capped via-in-pad treatment and stencil / process requirements, or revise the land treatment. Confirm BOM / placement orientation and component supply. |
| **Electrical consistency** | Saved DRC / ERC are zero under the current profile, and 616 model / schematic / PCB connected pins match. | Preserve these checks after changes and complete circuit / footprint review beyond serialization. |
| **Manufacturing outputs** | No order-ready fabrication package has been generated. | After design checks, export and inspect Gerber, drill, BOM, and placement files from the exact reviewed source revision. Include fabrication notes and source hash. |

## Scope of the first prototype

This release is for the **network speaker main board**. Microphone-ring development remains a separate parallel track and should not block first-prototype validation of Ethernet, power, DAC, and amplifier functions.

Hardware measurements, firmware validation, and full-power thermal / audio testing happen after assembly; they cannot be completed from CAD alone. Bench bring-up should begin with a current-limited isolated supply and staged rail checks.

See the [prototype validation plan](PROTOTYPE-VALIDATION.md) for the intended bring-up sequence.

## Source guidance

Key external references used by the existing review work include:

- WIZnet hardware design guide — 100 ohm differential routing, short matched MDI paths, no signal-layer changes, and placement / reference guidance.
- W5500 reference schematic.
- JLCPCB documented 4-layer stackups; JLC04161H-7628 is currently used only as a planning baseline.
- F1 manufacturer DC interrupt / fuse data; see [FUSE-RATING-REVIEW.md](hardware/PoE-Speaker/RevE/engineering/FUSE-RATING-REVIEW.md).

The existing engineering notes preserve the original source URLs and detailed calculations where applicable.

## Next implementation sequence

1. Ethernet placement / differential-pair routing / reference continuity.
2. Remaining mechanical envelopes and assembly constraints.
3. Power / protection calculations and fault-case review.
4. Circuit / footprint review for DAC, amplifier, regulators, and connectors.
5. Generate and inspect a reproducible fabrication package from a frozen source revision.

Do not treat another isolated clean DRC result as a release decision. The order gate remains **HOLD** until the engineering blockers are resolved or explicitly accepted.
