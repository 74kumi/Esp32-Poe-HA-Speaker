# Revision E — prototype review checkpoint

Open PoE-Speaker-RevE.kicad_pro in KiCad 10. This is the latest editable board. Earlier revisions remain preserved. NOT APPROVED FOR ORDERING OR POWER-UP.

Saved changes: C11 GVDD bypass is now local on B.Cu at (204.9,111.5), preserving the R15 PLIMIT branch; underside assembly clearance remains part of mechanical review. U7 FSW now connects to 3V3 per TI guidance; all previously missing passive/header order codes have documented candidates; C120/C121 use stable 100nF 100V C0G 1210 parts and C122 uses a 1uF 100V 1210 part. C17/C18 are a matched 2.2uF 25V pair. U5 is TPA3116D2DADR, U9/U10 are LM5050MK-2/NOPB, and Ag5800 is confirmed as the complete U1 code. Corrected 34 footprint assembly attributes and widened 51 power segments to 0.8mm where existing clearance permits.

Validation: zero DRC findings, zero unconnected items, zero ERC findings under the saved rule profile. All 616 connected model pins match schematic and PCB. U6/U7 electrical pin types are reviewed; the root sheet declares power sources after passive elements. These annotations do not prove circuit performance, and other imported pin types remain incomplete. See reports/power-source-review.json. Missing courtyard and some metadata checks remain disabled in the inherited profile; clean DRC does not substitute for physical review.

## Automated ERC/DRC checks

From the repository root, run:

```sh
KICAD_CLI=kicad-cli ./scripts/run-kicad-checks.sh artifacts/kicad
```

The wrapper writes `erc.rpt` and `drc.rpt`. GitHub Actions runs the same command for pull requests and pushes to `main`, retaining reports for 14 days. CI uses KiCad 10.0.5 from the immutable image `kicad/kicad:10.0.5@sha256:182c8005cb775a2c448a4c18681d489f1ff472a761885eba3e08b07e3c0564de`; use KiCad 10.0.5 for local runs when exact CI parity is required. The checks require zero KiCad ERC/DRC violations and do not run DRC after an ERC failure. Project-specific engineering/checkpoint scripts are intentionally excluded from CI because many are board-mutating, depend on checkpoint-local tools/data, or have not yet been proven read-only and reproducible in a clean CI environment.

Clean checks do not prove electrical correctness, PoE isolation, Ethernet signal integrity, thermal safety, manufacturability, or fabrication readiness.

Remaining work before a prototype order:

1. Reroute the remaining narrow loaded power paths, review via current capacity and local switching loops. reports/power-routing-audit.json contains exact positions and UUIDs; separate low-current sense branches from load trunks before modifying them. The two longest 24V_AMP sections (49.385mm and 39.837mm) have now been rerouted at 1.0mm width. A new continuous 1.0mm feed from C5 to the amplifier supply bypasses the congested narrow branch using two 0.5mm drilled vias. The original branch remains in parallel. See engineering/REVE-TRUNK-ROUTING.md; the whole path is not yet current-qualified.
2. Qualify Ethernet differential routing against the explicit JLC04161H-7628 design baseline and verify continuous return paths. See engineering/ETHERNET-STACKUP.md; the calculator-derived Ethernet100 routing preset is saved, but copper still needs rerouting and fabrication confirmation.
3. Review input fuse/transient coordination, capacitor effective capacitance and regulator stability, and amplifier supply tolerance. F1 DC interrupt ratings are now sourced; source/fault and time-current coordination remain open (engineering/FUSE-RATING-REVIEW.md).
4. Fit a top heatsink to the TPA3116D2 DAD package, check the Ag5800 thermal interface, body clearances, mounting support and connector access. H3/H4 now support the extended right edge at x=275; use insulating M2 standoffs. Thirteen assembly components still need verified courtyard/body review.
5. Produce and inspect Gerber, drill, assembly BOM and placement files only after those design checks; obtain fabricator stackup/via-treatment constraints. No manufacturing files or order submission are included in this checkpoint.

After assembly: staged current-limited bring-up, rail/startup/overload measurements, firmware and audio/Ethernet tests. Those are prototype validation activities, not prerequisites that can be completed without hardware. The eight-microphone ring remains a future separate board; this board is not a completed eight-microphone capture system.

Preserve routing: do not run build_revision.py or build_efuse_revision.py over this folder. For schematic-only updates run refresh_prototype_schematic.py, then annotate_prototype_power.py, export netlist/ERC and run validate_prototype.py. Editing model metadata alone does not update the schematic.
