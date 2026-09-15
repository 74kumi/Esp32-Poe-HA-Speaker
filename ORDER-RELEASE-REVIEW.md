# Prototype order release review

Updated 2026-09-14. **HOLD: not ready to order.** The latest board remains KiCad-RevE/PoE-Speaker-RevE.kicad_pcb. No manufacturing ZIP is approved by this document.

## Release priorities

| Area | Evidence / current state | Work required before order |
|---|---|---|
| Ethernet layout | ethernet-routing-review.json and ethernet-path-review.json: TX_P uses F/B/In2, TX_N uses F/B, and RX_P/RX_N now use F/B; seven signal vias remain including branch taps. Five receive main-route segments have moved from In2 to F.Cu after coordinated TX_N and analog-supply rerouting. R101/R102 termination branches are now local; see ethernet-front-corridor.json. RX termination R104/R105/C102 is now a local bottom-side cluster; twelve obsolete branch items were removed, reducing total RX-net copper from 81.680 mm to 55.734 mm. These totals include branches, not just pair lengths. Current PHY-to-jack screening paths are regenerated in ethernet-path-review.json; TX_N main route was shortened by about 1.557 mm. These are whole-segment metrics, not exact skew. | Rework PHY, termination, ESD and jack routing as differential pairs. The sourced Ethernet100 preset now supplies 100 ohm starting geometry: 0.225806 mm width / 0.2032 mm gap on F.Cu over In1 GND. Implement and inspect pair routing; these defaults do not constrain existing copper. Prefer no signal vias. Check reference continuity and jack isolation keepouts. |
| Physical stackup | Explicit JLC04161H-7628 copper/dielectric baseline is now saved in the PCB; see ETHERNET-STACKUP.md. | Use this baseline for impedance/current calculations. Confirm the stackup, finished copper, plating and impedance geometry with fabrication before order; the saved baseline is not an order approval. |
| Mechanical coverage | Eight B5100C courtyards added and checked. Thirteen non-feature footprints still lack courtyard graphics; see courtyard-coverage.json. | Add verified body/assembly envelopes for the remaining components; inspect underside parts, connector access, Ag5800 support and amplifier top heatsink. |
| Mounting | H3/H4 moved to (275,55)/(275,145), 5 mm from extended edge. Existing left holes at (75,55)/(75,145). | Use insulating M2 standoffs for the prototype. Enclosure fit remains unconfirmed. |
| Power paths / ground | Recent track/via/decoupling improvements pass saved DRC. Remaining constrained vias and amplifier ground paths are documented. | Calculate with actual copper/plating assumptions; review regulator input/output loops and remaining amplifier ground access. Geometric path audits do not provide a current rating. |
| Fuse and protection | F1 manufacturer now confirmed to publish DC interrupt ratings. EFUSE-REVIEW.md contains nominal settings and startup estimates. | Check source fault-current bounds, fuse timing/let-through, protection tolerances and transients. The 3.15 A fuse is not an instantaneous current clamp. |
| Assembly process | U2/U16 have thermal vias in solderable pads. | Specify filled/capped via-in-pad treatment and stencil/process requirements or revise the land treatment. Confirm BOM/placement orientation and component supply. |
| Electrical consistency | Saved DRC/ERC zero and 616 model/schematic/PCB connected pins match. | Preserve these checks after changes; finish circuit/footprint review beyond serialization. |
| Manufacturing outputs | Not generated for ordering. | After design checks, export and inspect Gerber/drill/BOM/placement files from the exact checked board; include fab notes and source hash. |

## Scope of first prototype

This is the network speaker main board. Eight-microphone capture/ring development remains separate, as requested. Hardware measurements, firmware validation and full-power thermal/audio testing happen after assembly; they are not tests that can be completed without prototype hardware. Bench bring-up should begin with a current-limited isolated supply and staged rail checks. A clean CAD report alone does not establish functional performance.

## Sources and review interpretation

- WIZnet hardware design guide: https://docs.wiznet.io/Design-Guide/hardware_design_guide — 100 ohm differential routing, short matched MDI paths, no signal layer changes, and placement/reference guidance. Current Ethernet layer changes depart from this guidance and require rework or substantiated qualification.
- W5500 reference schematic: https://docs.wiznet.io/assets/files/w5500_sch_v110_use_trans_-18b3297138bdf20fafd0f95e4c19358d.pdf
- JLCPCB documented stackups: https://jlcpcb.com/impedance — candidate 1.6 mm JLC04161H-7628 lists 0.035 mm outer copper, 0.21040 mm outer dielectrics, 0.0152 mm inner copper and 1.065 mm core. These numbers are planning inputs until a fabrication process is selected; solder mask and fabrication tolerances also affect impedance.
- F1 manufacturer: https://www.xcfuse.com/smd_fuses/24T_119.html — details in FUSE-RATING-REVIEW.md.

Next implementation: Ethernet placement/routing and stackup, then remaining mechanical envelopes and power/protection calculations. Do not spend the next chunk treating another isolated clean DRC result as a release decision.
