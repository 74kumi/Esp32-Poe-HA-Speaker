# Revision E supply-trunk routing follow-up

The two longest 24V_AMP segments, originally 49.385mm and 39.837mm long at 0.2mm width, now use 1.0mm routes. The first moves to y=81.5mm to clear the EFUSE_ILIM via. The second uses local bends around the 3V3 and BUCK5_VCC vias. The minimum-clearance rule remains 0.20mm.

The amplifier's front supply connection below U5 now bends to y=117.1mm at 1.0mm width. The incoming internal diagonal is widened to 1.0mm with a 0.8mm-long, 0.3mm-wide escape at its existing endpoint. The rear upper diagonal is 1.0mm with a 1mm-long 0.3mm escape. Part of the rear capacitor supply route is now 1.0mm and part 0.6mm; the congested section around AMP_FAULTZ and AMP_PLIMIT vias remains 0.2mm and needs further review/rerouting. Do not describe these changes as complete ampacity qualification.

The 10.959mm front trace from C123 toward R136 is a power-good sensing branch and was not widened in this pass. Final via count/current sharing, copper thickness, allowable temperature rise, switching-loop geometry and loaded-path analysis remain open.

Each accepted change passed the project's unchanged DRC profile with zero violations and zero unconnected items. Model/schematic/PCB pin-net mapping also passed for all 616 connected pins. No schematic connectivity was changed. Trial files are excluded from the review ZIP; the saved project is PoE-Speaker-RevE.kicad_pro.

Scripts reroute_amp_trunk.py, reroute_buck_supply.py, reroute_amp_branches.py and reroute_amp_back_supply.py are one-time operations against the preceding board state, not a generator to rerun against the final board. Before-trunk backup is retained under KiCad-RevE/reports.

## Direct amplifier feed

A subsequent pass added a continuous 1.0mm supply path from C5 pad 1 at (203.5,100) to the existing widened amplifier feed at (207,117.1). The route uses F.Cu into (207,107), B.Cu to (207,116.5), then F.Cu into the existing feed. Its two through vias have 1.0mm copper diameter and 0.5mm drills. This bypasses the congested 0.2mm branch around AMP_FAULTZ and AMP_PLIMIT; that original branch is retained in parallel, not reported as removed or widened.

The AMP_SDZ via moved from (207.524,111.6874) to (208.05,111.6874), with its In2.Cu and B.Cu connections adjusted. No signal net assignment changed. The relocated via and new route pass the unchanged clearance rules. DRC has zero violations and zero unconnected items, and all 616 model-to-board connections pass. Current sharing, via plating/temperature rise and local decoupling loops still require review; a geometric bypass alone does not qualify amplifier output power.

The accepted implementation is add_amp_bulk_feed.py, a one-time operation against the before-amp-direct-feed backup. bypass_amp_supply_neck.py and move_amp_control_vias.py are unsuccessful exploratory trials and must not be applied to the saved project. Trial boards are excluded from the review ZIP.

## Bench supply lanes

The long In2.Cu BENCH_FUSED and 24V_BENCH_PROTECTED routes are separated into wider lanes through the less congested right-hand board area. Their long new sections are 1.0mm wide at y=105.6 and y=103.3 respectively; the original narrow routing is retained through the dense amplifier area to the left. This is a partial routing improvement, not an end-to-end current rating.

The 26.243mm protected positive supply run on B.Cu was also widened: most is now 1.0mm, with a short 0.7mm section at x=195.45 passing between a ground via and the 3V3 route. This is the positive protected supply, not a ground-return trace despite the historical script filename widen_bench_return_run.py. No ground-plane or clearance-rule relaxation was made.

Accepted one-time scripts: separate_bench_trunks.py followed by widen_bench_return_run.py. Before-bench-trunks backup is retained in reports. The final board passes DRC with zero violations and unconnected items; all 616 model connections still match. Remaining narrow necks, supply vias, copper thickness and loaded-branch current analysis still require review.

## ORing supply follow-up

Two B.Cu 24V_OR routes were rerouted around the BUCK3V3_SS and AMP_PLIMIT vias. The upper route is predominantly 1.0mm wide, with short 0.3mm endpoint sections retained for signal clearance; the lower route is 1.0mm wide. The geometric audit's total below-0.5mm length for 24V_OR fell from 50.85mm to 30.87mm. No clearance rules were changed. The accepted one-time script is widen_oring_routes.py; the preceding board is preserved as reports/before-oring-routes.kicad_pcb.

Next review should distinguish supply load branches from sensing branches using actual PCB connectivity, rather than continuing to widen all same-net segments indiscriminately. KiCad's connectivity object exposes GetConnectedTracks/GetConnectedPads/GetConnectedItems, which may help build a path-level audit. No such path/current analysis has yet been completed. Via plating, temperature rise and bottlenecks in the remaining power paths are still open.

## Source-to-load audit and 5V correction

The subsequent audit_supply_paths.py now uses KiCad's direct track/pad connectivity to trace ten actual source-to-load paths. Results are in reports/supply-path-audit.json. It maximizes the minimum track width and then minimizes a whole-segment length metric. Pads and vias are not given current ratings, and it does not model parallel current sharing, voltage drop or ground return. This supersedes the earlier note that no path-level audit exists; current/thermal analysis still remains undone.

The verified L3.2-to-U7.11 load path initially contained 35.739mm of tracks narrower than 0.5mm. Its long In2.Cu sections were rerouted around 5V_PG and BUCK3V3_SW vias and widened to 0.8mm. The final approach segments (UUIDs 044de3e7-c3b7-45a4-9740-430398edd39b, a71c8389-bc65-4b39-af65-2e91e130130f and 8406323a-3925-4c5c-ad4a-98a370fb3ed6) were widened to 0.6mm. The 613a3492-9a19-4af0-a3a0-fbece343fb45 pin connection is 0.3mm wide and 0.702mm long. The audited path now has a minimum track width of 0.3mm and only 0.702mm below 0.5mm. DRC and all 616 pin-net checks pass.

The long-route operation is widen_5v_load_path.py; final approach changes are recorded above and in the board. The preceding board is reports/before-5v-load-path.kicad_pcb. Next priority candidates from the audit: F1.2-to-Q3.2, Q4.2-to-Q2.3, eFuse input/output approaches, and L4.2-to-U2.2 (the latter still has a 17.729mm 0.2mm segment near the top edge). Distinguish unavoidable short IC pin escapes from long load-carrying bottlenecks.

## 3V3 header feed

The later reroute_3v3_header_feed.py replaces the six narrow sections on the L4.2-to-U2.2 path near J4 with a continuous 0.8mm route at y=51.7 and around the left end of the header at x=154.5. The neighboring BOOT_GPIO0 trace was moved to y=50.63 with bends retaining its original endpoints. It remains inside the unchanged copper-to-edge clearance rule. No net assignments, connector pinouts or source electrical behavior changed.

The candidate passed DRC with zero findings and zero unconnected items; pin-net validation also passes. The prior board is reports/before-3v3-header-feed.kicad_pcb. Consult the refreshed source-to-load audit for the resulting whole-path bottleneck; width improvements are still not a thermal/current rating.

## eFuse approaches

The eFuse input approach (8160d7ac-d120-490a-b50f-c89914d5ad20) is widened from 0.2mm to 0.6mm. The output route now uses short 0.3mm connections from both OUT pins into a 0.8mm route toward C123 and the existing supply via. The short pin-17 branch joins at x=254.3 to avoid the AMP_SDZ via. This preserves pin spacing clearance while widening the shared current path; package and copper current sharing are not yet thermally qualified.

The accepted output change is widen_efuse_output.py. The pre-change board is reports/before-efuse-approaches.kicad_pcb. Run checkpoint_reve.py after any accepted board edit to regenerate DRC, pin-net checks, power audits, preview, and the verified review/checkpoint archives. It refuses to package a board with DRC findings.

## Latest amplifier and bench improvements

reroute_amp_near_3v3.py replaces the narrow In2.Cu detour near the 3V3 via with a 0.8mm route through x=197.6. The U5 supply approaches a7552990-f27c-4d45-807f-a1e4426dea3a, 265774f1-129e-4ed8-a0aa-32a2c26f2972 and a858f2b0-a324-4e91-86d8-2db20ad48114 are now 0.8mm. The upper power pin bridge 8a2dc632-7769-4734-9b2d-34b75ff1148e and pin-31 approach be6888ca-9eb7-443c-b8d0-eaadce5606e2 are 0.5mm. The short B.Cu neck 44438f23-f561-457f-b997-fb3abbad93c0 is 0.4mm. These changes passed DRC without rule changes.

The F1 output approach c10ca537-3517-4ffc-a2eb-3b6b120c567d and 13.8975mm BENCH_FUSED diagonal 09e5af79-6607-4f10-9e78-aa9b6704e562 are widened to 1.0mm. A subsequent one-time screen_bench_widths.py tested fourteen remaining narrow loaded segments at 0.6mm. Three passed and were accepted: 80049751-3370-469e-a09d-af30adfec276, acc9d389-638c-40f3-aa0f-94b5fbe48b2d and f28f03ed-3f95-4cd8-8dbc-7535d3cf855b. The other eleven trials were rejected for clearance findings. Their original widths remain. Detailed results are reports/bench-width-screen.json; the pre-screen board is preserved locally.

The current F1.2-to-Q3.2 path still has 26.968mm below 0.5mm, and Q4.2-to-Q2.3 has 30.438mm. Both remain limited to 0.2mm at some locations and require rerouting. The 3V3 L4-to-U2 path is now at least 0.6mm throughout. eFuse-to-amplifier paths have only 1.0–1.5mm below 0.5mm in the selected graph paths, but their vias and thermal performance are not qualified.

## Bootstrap placement: open priority

audit_bootstrap_paths.py records both capacitor-to-IC connections for C7–C10. The combined whole-segment screening lengths are C7 58.703mm, C8 52.641mm, C9 67.963mm and C10 29.889mm. These are not exact loop lengths: shared tracks can extend beyond a junction. They nevertheless identify a substantial placement issue. TI's TPA3116D2 layout guidance calls for close local decoupling and small switching loops: https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf . A clean connectivity report does not qualify these loops.

Neither place_c9_bootstrap.py nor place_c9_bootstrap_bottom.py is accepted. The top trial conflicts with SW_NEG and ground tracks. The revised bottom trial places C9 at (212.7,109.7) and reuses the SW_POS via, but its new BSNR via conflicts with the 1.0mm B.Cu SW_POS trunk at x=211.598 and the F.Cu ground link at x=212.81. It also leaves the old SW_POS capacitor spur dangling. Main C9 remains at its original location. Do not copy power-trial.kicad_pcb into the main project. Plan a coordinated local reroute of bootstrap capacitors, switched-output copper and ground connections; preserve current capacity, drill/clearance limits and the return plane.

## Accepted C9 local placement — supersedes original-location note above

The later coordinated trial place_c9_bootstrap_local.py, followed by prune_c9_old_spur.py, is accepted. C9 is now on F.Cu at (214.5,109.7), oriented 90 degrees. Two 0.3mm connections run directly from U5 pins 26/27 to its pads, with bends starting at x=213.3. The combined audited connection length is 5.766mm, down from the previous 67.963mm whole-segment metric. The original long BSNR route and five DRC-identified dangling SW_POS spur items are removed. The two older trial scripts remain rejected.

The crossing F.Cu ground link between pins 25 and 28 is replaced with 0.6mm diameter / 0.3mm drilled ground vias at (212.81,110.675) and (212.785,108.725), connected to the filled ground plane. SW_NEG retains its 1.0mm width and detours via x=216 to clear C9; this adds approximately 2.829mm to the audited C7/C8 output paths, which still need local placement work. J3's reference is moved clear of C9. No clearance or drill constraints were relaxed.

The rendered top copper was visually inspected, DRC has zero findings and zero unconnected items, and all 616 model-to-schematic-to-PCB connections pass. The pre-change board is reports/before-c9-local-placement.kicad_pcb. The model's C9 placement is synchronized. This is a layout improvement, not measured switching performance. Next: coordinated C7, C8 and C10 placement, with HF decoupling and output-loop review.

## Accepted C10 and C7 local placement

C10 is now at (214.5,106.5), oriented 270 degrees on F.Cu. Its 0.3mm connections run to U5 pins 30 and 29 with separate bend positions to maintain clearance. The combined audited connection metric fell from 29.889mm to 6.328mm. One obsolete SW_POS spur was removed. Accepted one-time scripts: place_c10_bootstrap_local.py and prune_c10_old_spur.py. The preceding board is reports/before-c10-local-placement.kicad_pcb.

C7 is now at (214.5,115.0), oriented 90 degrees on F.Cu. Its 0.3mm connections run locally to U5 pins 20 and 21. Four obsolete SW_NEG spur items were removed, including the long top-side run formerly reaching C7. The combined audited connection metric fell from 61.532mm to 5.156mm. Accepted one-time scripts: place_c7_bootstrap_local.py and prune_c7_old_spur.py. The preceding board is reports/before-c7-local-placement.kicad_pcb.

The affected references were repositioned to clear copper apertures and one another. Each candidate was rendered and visually inspected before acceptance. Both accepted boards passed DRC with zero findings and zero unconnected items; all 616 pin-net comparisons pass. C7 and C10 model placements are synchronized, and review/checkpoint archives are refreshed. Scripts operate on their respective earlier baselines and should not be reapplied blindly.

C8 remains at its original location, with a 55.470mm combined whole-segment screening metric. It needs a coordinated placement pass; avoid crowding the already placed capacitor courtyards or the J3 connector. Local HF decoupling, output-current paths, and ground-return review remain necessary after bootstrap placement. No manufacturing release is implied by these geometry checks.

## Accepted C8 local placement — completes the bootstrap placement pass

C8 is now on F.Cu at (214.5,112.2), oriented 180 degrees, between C9 and C7. Its two local connections to U5 pins 24 and 23 reduce the combined audited metric from 55.470mm to 5.751mm. The old BSPL routing and eight DRC-identified obsolete SW_NEG spur items were removed. Accepted one-time scripts are place_c8_bootstrap_local.py and prune_c8_old_spur.py, against the preceding board preserved as reports/before-c8-local-placement.kicad_pcb. The C8 model placement is synchronized.

To clear C8, SW_NEG transitions from F.Cu at (216,110) to In2.Cu and back at (216,113.45), using 1.0mm diameter / 0.5mm drilled through vias. The inner segment remains 1.0mm wide. The short lower F.Cu approach is 0.6mm to clear the C7 bootstrap connection, and the short connection near pin 23 is 0.3mm; current sharing, temperature rise and switching performance still need qualification. The B.Cu SPK_POS route retains 1.0mm width and detours left through (214.7,109.31) and (214.7,111.55) to clear the upper output via without approaching the wrong connector pad. No clearance or drill rules were relaxed.

The top copper rendering was inspected before acceptance. Final DRC reports zero findings and zero unconnected items, and all 616 pin-net checks pass. The four combined bootstrap routing metrics are C7 5.156mm, C8 5.751mm, C9 5.766mm and C10 6.328mm. These are geometric screening values, not measured loop inductance or circuit qualification. Checkpoint archives and resume notes are updated. Next: amplifier high-frequency decoupling placement, output-current and ground-return paths, then the remaining release checks.

## Accepted supply decoupler placement: C13 and C12

C13 moved from (196,91) to (213.5,119), oriented 270 degrees on F.Cu. A 0.8mm connection joins the lower amplifier supply near pin 17. Its ground pad connects to a 0.8mm diameter / 0.4mm drilled ground via at (213.5,121.9). The old crossing ground trace was replaced by local returns at (209.225,119.1) for C11 and (216.3,118.4) for the downstream ground branch, using 0.6mm / 0.3mm vias. Two obsolete supply-spur items were removed. Accepted scripts: place_c13_decoupling.py and prune_c13_old_spur.py. Backup: reports/before-c13-decoupling.kicad_pcb.

C12 moved from (200,107.5) to (207.4,104), oriented 90 degrees on B.Cu. It connects through the existing supply via at (207,107), with a 0.8mm backside connection and a 0.6mm local front connection to the upper supply pins. Its ground return uses a 0.8mm / 0.4mm ground via at (207.4,101). The capacitor pads are clear of the open via holes; the trial's new via in the supply pad was rejected. The AMP_SDZ signal remains on B.Cu, detouring around C12 through x=209.25 without crossing the inner power lanes. One obsolete supply spur was removed. Accepted scripts: place_c12_decoupling.py and prune_c12_old_spur.py. Backup: reports/before-c12-decoupling.kicad_pcb.

Both placements were rendered and visually inspected and passed DRC with zero findings/unconnected items. All 616 pin-net comparisons pass. Model placement and side are synchronized. C12 introduces an underside component at this location; assembly planning and enclosure standoff clearance must account for it. C14/C15 and overall supply/ground loops still require review; no capacitance-under-bias, thermal or EMC qualification is implied. TI guidance used: https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf , sections 8.2.2.4 and 10.1. The purpose is to shorten decoupling connections to supply and ground, not merely clear DRC.

## Output-pin width follow-up

The actual output-current paths are now recorded by audit_output_paths.py in reports/output-path-audit.json and regenerated by checkpoint_reve.py. Three short amplifier pin connections were widened from 0.3554mm to 0.5mm: 6a066147-0a58-4241-b33e-d64c5af9ea57 (pin 21), 114bc68d-c06b-49f8-92b9-769f02e570c5 (pin 23), and ff07bc79-1b99-440c-af24-ed57d7520758 (pin 29). Their lengths are 1.405mm, 1.405mm and 1.208mm. Backup: reports/before-output-pin-widths.kicad_pcb.

All four selected amplifier-to-inductor paths now have minimum track widths of at least 0.5mm; the pin-27 path has a 1.0mm minimum. Both inductor-to-speaker-connector paths have a 1.0mm minimum. No selected path includes a track below 0.5mm. This excludes pads/vias from the width metric and does not establish ampacity, current sharing, temperature rise or output-loop inductance. Other narrower tracks on these nets include bootstrap branches; they should not be widened indiscriminately.

DRC remains at zero findings/unconnected items, all 616 pin-net comparisons pass, and checkpoint archives are verified. Remaining priorities include amplifier local returns and internal GVDD decoupling, the still-narrow bench supply trunks, and stackup/current/thermal qualification.

## Extended bench supply lanes

extend_bench_fused_lane.py replaces the long 0.2mm section and its eastern bend with a 1.0mm In2.Cu lane at y=105.6 from x=199.073 to 215.5. A short 0.2mm entry remains from (199.073,104.835). Backup: reports/before-fused-lane-extension.kicad_pcb.

extend_bench_protected_lane.py replaces the neighboring long 0.2mm route with a 1.0mm In2.Cu lane at y=102.4 from x=197.2 to 215.5, joining the existing lane at y=103.3. The narrow entry bends through (197.2,104.04) to clear the nearby 3V3 via. Backup: reports/before-protected-lane-extension.kicad_pcb.

widen_protected_shutdown_neck.py replaces the 6.8231mm-long 0.2mm B.Cu segment near the bench controller with a 0.6mm route through x=251.2, maintaining clearance from BENCH_SHDN at (252.115,100.975). Backup: reports/before-protected-shutdown-neck.kicad_pcb.

The audited F1.2-to-Q3.2 path now has 10.224mm below 0.5mm, down from 26.968mm. Q4.2-to-Q2.3 now has 6.649mm below 0.5mm, down from 30.438mm. Both still contain 0.2mm sections and are not current-qualified. No clearance constraints were changed. Final DRC is zero findings/unconnected items, all 616 pin-net checks pass, and checkpoint archives are verified. Continue with the remaining short necks identified by supply-path-audit.json and then current/via/return-path qualification.

## Bench entry bottlenecks removed

widen_fused_entry.py replaces the remaining narrow fused entry and obsolete stub with a 0.6mm In2.Cu route through (189.932,107.2), (197.473,107.2) and (199.073,105.6), retaining the original western endpoint (189.756,107.024). The y=107.2 lane clears the protected-supply via that blocked the initial trial. Backup: reports/before-fused-entry.kicad_pcb.

Four protected-supply entry segments are widened to 0.6mm: 331895c1-e12e-4f85-8351-170377cc3197, 73ad2d41-2e02-485d-971e-8b832a88669b, 5ca90b07-e6b7-401f-b20a-8837c8e69503 and 060da957-5bed-452d-b66b-8ee326c8651e. Backup: reports/before-protected-entry-widths.kicad_pcb.

The saved F1.2-to-Q3.2 and Q4.2-to-Q2.3 graph paths now each have minimum track width 0.6mm and zero whole-segment length below 0.5mm. This supersedes the preceding narrow-entry counts. Other same-net sensing branches remain narrow intentionally; the audit does not establish current capacity, via plating requirements or thermal performance. DRC is zero findings/unconnected items and all 616 pin-net comparisons pass. Next: current and return-path qualification, outstanding local decoupling, Ethernet and release checks. Connector roles and exact J4/J5/J6 pin numbers are recorded in engineering/CONNECTOR-GUIDE.md.

## C11 investigation — trials NOT accepted

audit_amplifier_decoupling.py now records six supply-side bypass/PLIMIT paths in reports/amplifier-decoupling-audit.json and is included in checkpoint validation. It uses the existing widest-path, whole-segment screening metric, not an exact loop-length calculation. The saved U5.7-to-C11.1 path reports 18.339mm and two vias; U5.7-to-R15.1 reports 13.743mm and two vias. R15 feeds AMP_PLIMIT, not AMP_GAIN. An early commentary description of it as a gain-setting resistor was incorrect.

No C11 relocation has been accepted. The saved C11 remains at (210,120) on F.Cu. place_c11_gvdd.py and prune_c11_old_spur.py are experimental and must not be applied to the main project or used as a release candidate without completing checks. The current power-trial board has conflicts and is excluded from review archives.

The investigation found several constraints: the F.Cu AMP_SDZ vertical at x=202.3527 blocks a direct route into the space vacated by C12; the inner layer has crossing audio/control routes, and the back layer is crowded with FAULTZ, GAIN and PLIMIT. Removing all GVDD tracks also disconnects R15, so preserve its branch. The latest trial at (203.6,120.5) conflicts with the PLIMIT via at (203.822,119.832) and has label issues. Other nearby positions conflict with the 24V_AMP route at y=117.1 or x=202.3809. Do not repeat blind coordinate trials; first map the local copper and plan a coordinated placement/routing change that preserves R15 and avoids open holes in solder pads. Main-board geometry remains at the last verified bench-entry checkpoint.


## Accepted C11 local GVDD bypass — 2026-09-14

Mapped the actual bottom-layer corridor before placement. C11 moved from top (210,120), 180 degrees, to bottom (204.9,111.5), 270 degrees. Its GVDD pad connects locally to the existing GVDD via at (205.583,110.37); ground bends left around the MUTE via, then reaches a new 0.5 mm diameter / 0.3 mm drill ground via at (205.2,114.1). Retained the full R15 PLIMIT branch. Removed five DRC-identified obsolete C11 spur items. Trial DRC: zero findings and zero unconnected items. Bottom copper/silkscreen render inspected. Main pre-change backup: before-c11-local-gvdd.kicad_pcb. This supersedes earlier rejected C11 trials. Current/return-plane and assembly qualification remain pending; no fabrication release.


## Accepted remaining load-neck widening — 2026-09-14

Four audited load-path segments widened to 0.6 mm: 24V_OR 4ad3da69 and 5075d3e5; 24V_AMP 44438f23; 5V 613a3492 (full UUIDs and original widths in reports/load-neck-width-trial.json). Trial has zero DRC findings and zero unconnected items. The 0.5 mm-long U16 output escape de68fccd remains 0.3 mm: widening to 0.6 mm reduced clearance to AMP_SDZ pin 16 to 0.075 mm, so that change was reverted. No component or netlist changes. These widths do not establish via ampacity, temperature rise, or return-path quality. Backup: before-load-neck-widths.kicad_pcb.


## Accepted power-via enlargement — 2026-09-14

Reviewed 18 audited load-path vias with 0.3 mm drills. Eleven now use larger copper/drill geometry (1.0/0.5 mm or 0.8/0.4 mm); seven retain original geometry because of neighboring copper. Full per-via positions, UUIDs and before/after dimensions: reports/power-via-review.json. Proposed drills were screened against all component pad bounding boxes with 0.35 mm margin to avoid moving holes into solder pads. Final filled-board DRC zero, unconnected zero. Original board preserved in before-load-via-enlargement.kicad_pcb. This is a geometry improvement, not a current rating: plating thickness, thermal behavior and ground-return review remain pending.


## Accepted eFuse output via relocation — 2026-09-14

Via b983fee9 moved from (256.4755,78.2346) to (256.4755,78.1546), enlarged from 0.6/0.3 mm copper/drill to 0.8/0.4 mm. Preserved the original long In2 route to clear EFUSE_FAULT_N; added a 0.08 mm long, 0.6 mm wide connecting segment. F.Cu endpoint follows the shifted via. Checked new hole against all pad bounding boxes with 0.30 mm center margin. Larger displacements approached C123 and were rejected. Final DRC zero and unconnected zero. This brings the preceding power-via review to twelve improvements and six original constrained vias. Backup: before-efuse-via-relocation.kicad_pcb. No via ampacity claim; plating and thermal assumptions remain unresolved.


## Ground-access review checkpoint — 2026-09-14

Added audit_amplifier_ground.py to the checkpoint workflow. Inventory follows ground tracks to vias and explicitly identifies plated through-hole pads; it does not model zone current or return inductance. C11/C12/C13 have nearby track-connected ground vias. C14/C15 merit local ground-access review; nearest reachable vias have straight-line separations around 3.98/5.97 mm, which are screening distances, not routed loop lengths. C5/C6 through-hole pads can access the ground plane directly, so separate-via distance is not evidence of a defect. Only one saved GND zone is present, on In1.Cu. Next inspect C14/C15 and U5 ground-plane continuity before changing routing. No PCB change in this chunk.


## Accepted C14/C15 local ground vias — 2026-09-14

Added 0.8 mm copper / 0.4 mm drill GND vias at (197.425,115.5) and (197.425,111.5), each with a 1.1 mm long, 0.6 mm wide F.Cu link from its capacitor ground pad. Hole-to-pad guard checked. Initial x=197.325 conflicted with the bottom 3V3 trunk and was rejected; x=197.425 passes. Both via centers hit the saved filled In1.Cu GND zone. Final DRC zero, unconnected zero. Existing ground routes retained. See reports/c14-c15-ground-vias.json. Backup before-c14-c15-ground-vias.kicad_pcb. Ground return distribution and amplifier pin/plane access remain for review.


## Accepted amplifier ground-pin track widths — 2026-09-14

Widened 21 directly connected U5 GND segments from 0.2 mm: seventeen to 0.4 mm, three to 0.35 mm, one to 0.25 mm. This count includes tiny imported pin stubs; it does not represent 21 independent return paths. Four full-width candidates conflicted with MUTE/SW_POS/SDZ/GAIN vias and were reduced to preserve clearance. Zero final DRC and unconnected findings. No route or via relocation. Full UUIDs/dimensions in reports/amp-ground-pin-widths.json. Backup before-amp-ground-pin-widths.kicad_pcb. Remaining: ground pin-to-plane access and return continuity, including downstream 0.2 mm tracks.


## Accepted U5 pin 22 ground-plane access — 2026-09-14

Added a 0.6 mm copper / 0.3 mm drill GND via at (209.88,112.453) on the existing ground track. Via center contacts filled In1.Cu GND; pad-hole clearance screened with a 0.25 mm center margin. First trial at (210.822,112.625) conflicted with AMP_SW_POS on B.Cu and was rejected. Accepted position has zero DRC and unconnected findings. No old ground routes removed. Backup before-pin22-ground-via.kicad_pcb. Added audit_amp_ground_plane.py to locate shortest whole-segment copper paths from all ten ground pins to filled-plane-contact vias or plated pads; this does not qualify return impedance or uninterrupted current corridors.


## Accepted lower amplifier ground-group link — 2026-09-14

Added 0.35 mm F.Cu ground tracks from U5 pin 13 (204.19635,113.925) through (205.025,113.925) to the existing C11 GND via at (205.2,114.1). Confirmed that via contacts filled In1.Cu ground. Original ground routes retained. Trial via for pin 1 at (205.203,106.125) conflicted with AMP_MUTE on B.Cu and BENCH_FUSED on In2.Cu and was removed before acceptance. Final DRC zero and unconnected zero. Backup before-pin13-ground-link.kicad_pcb. Pin 1 remains unchanged; next inspect a different local ground access point for pin 1 and pins 9-11.


## Accepted extension mounting support — 2026-09-14

Moved existing right mounting holes H3/H4 from x=225 to x=275 at y=55/145. The mounting centers are now 5 mm from the extended right board edge, matching left-side edge offsets. Retained M2 footprints; use insulating standoffs. No other component pad bounding boxes within 2.5 mm of these centers. DRC zero and no unconnected items. Placement model synchronized; schematic connections unchanged. Backup before-extension-mounts.kicad_pcb. Enclosure, heatsink and module support remain separate mechanical checks.


## Accepted B5100C mechanical courtyards — 2026-09-14

Added 10.1 x 6.8 mm F.CrtYd rectangles to D3-D10 and their local library copies. Basis: saved B5100C package drawing, maximum body width 6.22 mm and overall lead span 8.13 mm; existing pads reach +/-4.77 mm in X. Courtyard allows at least 0.25 mm beyond pad/body extents, rounded outward. No copper or pad changes. Zero final DRC/overlap findings. Board and original library copies backed up. Other imported components without courtyards remain in reports/courtyard-coverage.json.


## Accepted Ethernet receive termination cluster — 2026-09-14

Moved R104/R105/C102 to B.Cu near U3, coordinates in reports/rx-termination-placement.json. New short B.Cu links use existing RX signal vias. Rebuilt the RX termination common node and added a 0.6/0.3 mm ground via at (121.5,74.875), confirmed in filled In1 GND and outside component pads. Removed twelve DRC-identified obsolete RX spur items, including one obsolete signal via. Final DRC zero, unconnected zero; bottom render visually inspected. Original main saved as before-rx-termination-cluster.kicad_pcb. This reduces excess termination routing; main pair coupling, impedance, layer transitions and skew remain open. Trial uses a copy of the main project/rules. Trial files must stay out of release archives.

Post-change Ethernet inventory: RX_P total copper 41.116 to 28.831 mm; RX_N 40.564 to 26.903 mm, including branches. Main PHY-to-jack screening paths unchanged. This is a termination-branch improvement, not completion of pair routing.


## 2026-09-15: sourced Ethernet routing preset

Verified JLCPCB calculator output for JLC04161H-7628, masked noncoplanar L1/L2, 100 ohm, 8 mil gap: 8.89 mil width. Added Ethernet100 class with exact converted width 0.225806 mm and gap 0.2032 mm, assigned to the four MDI nets. Trial DRC zero/unconnected zero. Existing copper unchanged; this prepares actual rerouting and is not impedance qualification. Preserved before-ethernet-pair-preset.kicad_pro. The calculator tolerance setting is not a production guarantee.


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
