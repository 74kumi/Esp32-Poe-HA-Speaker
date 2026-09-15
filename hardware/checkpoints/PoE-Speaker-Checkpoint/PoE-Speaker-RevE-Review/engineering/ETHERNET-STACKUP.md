# Ethernet physical design baseline

2026-09-14: The PCB now contains an explicit JLC04161H-7628 stackup as the design baseline. This is a reversible engineering selection, not a fabrication order or an impedance qualification. The accepted change affects stackup metadata only; tracks, zones, pads and placements are unchanged. Backup: before-explicit-stackup.kicad_pcb.

| Layer | Thickness mm | Dielectric constant |
|---|---:|---:|
| F.Cu | 0.035 | — |
| 7628 prepreg | 0.21040 | 4.4 |
| In1.Cu | 0.0152 | — |
| FR4 core | 1.065 | 4.6 |
| In2.Cu | 0.0152 | — |
| 7628 prepreg | 0.21040 | 4.4 |
| B.Cu | 0.035 | — |

Source: [JLCPCB published stackup](https://jlcpcb.com/impedance), checked 2026-09-14. The listed copper/dielectric dimensions sum to 1.5862 mm; retain the nominal 1.6 mm board specification rather than silently rescaling dielectric heights. Mask is nonuniform: 0.01524 mm above copper and 0.03048 mm above substrate/between traces, Er 3.8. KiCad's single mask thickness stores the above-copper value; it cannot represent that full cross section. The sum including two above-copper mask films is 1.61668 mm. Confirm finished thickness tolerance and copper interpretation with fabrication. No loss tangent or hole plating thickness is assumed.

F.Cu over In1 GND is the intended Ethernet transmission-line geometry. The existing B.Cu and In2 signal segments do not have an equivalent nearby GND plane and must not reuse a top-layer width calculation. No bottom GND plane has been added by this change.

Calculator result verified 2026-09-15: masked noncoplanar differential model, L1 over L2, 100 ohm target and 8 mil gap gives **8.89 mil width** on JLC04161H-7628. Exact conversions are 0.225806 mm width and 0.2032 mm edge gap. The source UI labels this standard stackup as finished thickness 1.59 mm +/-10%. The displayed impedance tolerance of 0.5% is a solver setting, not a manufacturing guarantee. Inputs/results are saved in reports/ethernet-impedance-calculator.json. Source: [fabricator calculator](https://jlcpcb.com/pcb-impedance-calculator).

The main KiCad project now assigns ETH_TX_P/N and ETH_RX_P/N to Ethernet100 with those differential routing defaults. Clearance and via defaults are retained. This changes no existing copper and does not add an enforcing width or pair-gap DRC rule; existing 0.2 mm tracks remain unqualified. Do not apply this noncoplanar result beside close same-layer ground copper without recalculating the coplanar geometry.

Next implementation: rework PHY/jack/ESD/termination placement and actual routes using the saved pair preset, preserving pin polarity. Inspect pair coupling, return corridors and jack isolation keepouts. Add enforcing rules only with the actual routing and explicit pad escape exceptions.

The new ethernet-reference-review.json samples projected ground under track centerlines. Missing samples near pads can be normal antipads; continuous samples do not prove sufficient return width or a usable reference for inner/bottom routes. It is an inspection aid only. WIZnet's [hardware guide](https://docs.wiznet.io/Design-Guide/hardware_design_guide) remains the layout reference.


## 2026-09-15: front-layer RX feasibility probe

Promoted the five existing In2 RX segments to F.Cu at the sourced width in a separate trial. DRC found eight errors, zero unconnected items. Rejected; main copper remains unchanged. Detailed UUIDs/positions are in reports/rx-front-layer-probe.json. The trial is not a coupled pair and is excluded from release archives.

Obstacles are concentrated in the Ethernet circuit: TX_N routing at the jack and toward U3, TX_P routing to R101, R101 pad 1, and ETH_3V3A feeding the transmit termination. A layer-only conversion cannot solve these crossings. Do not repeat this same probe as the next chunk.

Next: coordinate all four MDI routes and R101/R102 supply branches, rather than routing RX in isolation. Preserve jack/PHY pin polarity. Plan the jack fanout first, then main coupled corridors, followed by short ESD/termination taps. R101/R102 placement and analog-supply access must be included in the same trial. RX bottom termination and ESD paths also remain part of final qualification. Keep the main unchanged until the full proposal has clean DRC and pin mapping.


## 2026-09-15: accepted local R101 transmit termination

R101 moved to B.Cu (120.5,64.8), angle 90. Its TX_P branch now uses the existing signal via at (119.497,66.7995) and about 1.59 mm of bottom track instead of about 5.37 mm of front track. ETH_3V3A uses a new 0.6/0.3 mm via at (119.7,63.975), linked to the existing In2 supply track. Via-to-pad bounding-box guard passes at 0.25 mm. DRC zero, unconnected zero; bottom placement visually inspected. Main backup before-r101-local.kicad_pcb; design model synchronized. No footprint library change is needed for a placement-only edit.

Rejected supply via trials at (120.5,62.9) and (121.6,63.975) conflicted with existing ground/RX copper. An additional RX_N top-layer probe still crossed TX_N fanout and ETH_3V3A in three places; that change was removed. See rxn-after-r101-trial-findings.json. This accepted change clears the TX_P termination branch, but does not complete the coordinated MDI reroute. Next address TX_N/R102 and R103 supply corridor together with both pair fanouts.


## 2026-09-15: accepted local R102 termination

Moved R102 to B.Cu (116.3,64.7), angle 270. Its TX_N tap uses a new 0.6/0.3 mm via at (117.1,64.1563) on the existing front signal track and about 0.917 mm of bottom track, replacing about 6.92 mm of front branch. The supply pad connects to the existing analog-supply via (117.5,65.3196). Via-to-component-pad bounding-box guard passes at 0.25 mm. Main PHY-to-jack routes are unchanged. This removes a long termination branch but adds a signal-tap via and does not qualify impedance or pair coupling. DRC and unconnected counts zero; underside placement visually inspected. Model synchronized; backup before-r102-local.kicad_pcb.

Rejected earlier position/orientation introduced nine DRC errors. Testing removal of the four-track R103 supply path produced one disconnected analog-supply island: it is NOT redundant. Restored all four tracks. Next rerouting must provide a replacement supply connection before removing that path. TX_N jack fanout remains another crossing obstacle. No footprint library geometry changed.


## 2026-09-15: accepted Ethernet front routing corridor

Replaced the TX_N jack detour with a shorter F.Cu route at 0.225806 mm width, preserving the R102 tap. Replaced segment length 10.107 mm becomes 8.551 mm. The first proposal crossed J1 unused pad 19; revised geometry goes below that pad and passes DRC. This is not yet a matched transmit pair.

Replaced the required four-track R103 analog-supply path through the receive corridor with 0.3 mm B.Cu routing from R102 power pad (116.3,65.525) via (116.3,74.6) to a new 0.6/0.3 mm supply via at (118.725,74.6), connecting the existing front analog-supply trunk. This longer replacement restores the complete analog supply rather than deleting a required connection. Current/return-loop review remains open. Via-to-component-pad guard passes at 0.25 mm.

With both obstacles cleared, moved all five In2 receive main-route segments to F.Cu at 0.225806 mm width. Both receive nets now use F/B only; bottom ESD/termination branches and their vias remain. Top-layer visual inspection and DRC pass with zero unconnected items. No component or footprint geometry changed, so no model/library placement update is needed. Backup: before-ethernet-front-corridor.kicad_pcb.

Next: improve actual RX coupling and spacing (long parallel sections still have about 0.768 mm center spacing, not the 0.429006 mm target), address RX_P PHY escape detour and termination taps, then TX_P layer/coupling and ESD branch geometry. The former layer-only probe conflicts are resolved by this coordinated change; do not rerun the old probe/acceptance scripts on the new main. Clean DRC does not establish impedance or return continuity.


## 2026-09-15: accepted coupled RX trunk

Rebuilt RX_P jack-to-PHY approach on F.Cu, bypassing its former dip through (117.5,71.6622). The former route to that via remains only as the ESD/termination tap. RX_P and RX_N now run parallel at 0.225806 mm width / 0.2032 mm edge gap for x=110.221 through 118.6 (8.379 mm). Pad escapes, via/tap discontinuities, branch lengths and reference continuity remain unqualified. DRC and connectivity are clean. No component/model placement changed. Backup before-rx-coupled-trunk.kicad_pcb. Next inspect RX branch geometry and return reference, then complete TX_P layer and pair coupling.
