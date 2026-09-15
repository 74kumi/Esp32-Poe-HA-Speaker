# Project Roadmap

This roadmap turns the engineering review into explicit release gates. The project should move forward only when the exit criteria for the current gate are met and documented.

## Gate 0 — Rev E engineering review

**Status:** HOLD

Goal: turn the current Rev E checkpoint into a defensible fabrication candidate.

Exit criteria:
- Ethernet MDI routing reviewed and reworked as true differential pairs with documented reference continuity and stackup assumptions.
- PoE / bench input protection, fuse behavior, eFuse limits, startup/inrush and transient assumptions reviewed with calculations.
- Regulator and audio power paths reviewed, including effective capacitance, compensation, amplifier bootstrap/GVDD paths, output filter and grounding.
- Remaining footprint, polarity, orientation and courtyard gaps resolved or explicitly waived with rationale.
- Via-in-pad and thermal requirements resolved for the intended assembler.
- KiCad DRC/ERC clean under the documented ruleset.
- No unresolved blocker-class GitHub issues.

## Gate 1 — Rev F fabrication candidate

Goal: freeze a board revision that can be sent for prototype manufacture.

Exit criteria:
- Exact source commit/hash recorded.
- BOM reviewed for manufacturer part numbers, lifecycle, availability and approved substitutes where practical.
- Gerber, drill, BOM and placement outputs generated from the exact checked source.
- Manufacturing outputs independently inspected against the PCB source.
- Stackup and impedance assumptions confirmed with the selected fabricator.
- Assembly notes include via-in-pad, stencil, heatsink, connector and polarity/orientation requirements.
- Prototype validation plan reviewed before ordering.

## Gate 2 — Prototype assembly and smoke test

Goal: prove that the board can be powered safely and that all basic subsystems come alive.

Exit criteria:
- Visual inspection passed before power.
- Resistance-to-ground / short checks passed on primary rails.
- Current-limited isolated bench bring-up completed.
- Main rails measured and recorded.
- ESP32 boots and exposes serial diagnostics.
- Ethernet PHY/link state is functional.
- DAC produces a controlled test signal.
- Amplifier enable/mute and idle-current behavior are verified.
- No abnormal thermal rise or fault behavior during smoke testing.

## Gate 3 — Functional validation

Goal: demonstrate that Rev F meets the intended electrical function.

Exit criteria:
- Ethernet reliability tested under sustained traffic.
- Audio output power characterized into the intended load.
- Noise, clipping and distortion behavior measured to the practical limits of available equipment.
- Thermal behavior recorded at multiple power levels and durations.
- Protection/fault behavior tested where safe and practical.
- PoE operation verified separately from bench-power operation.
- All failures and deviations are captured as issues.

## Gate 4 — Firmware / Home Assistant integration

Goal: layer product behavior onto proven hardware.

Exit criteria:
- Stable Ethernet/network stack.
- Deterministic amplifier mute/enable behavior.
- Audio playback path validated.
- OTA/update recovery strategy tested.
- Home Assistant integration demonstrated.
- Diagnostics expose useful rail, link and fault information where hardware permits.

## Gate 5 — Rev 1.0 candidate

Goal: produce a repeatable design suitable for documented small-run builds.

Exit criteria:
- All prototype findings resolved or accepted in writing.
- Source, BOM, fabrication outputs, firmware and validation results are versioned together.
- Known limitations documented.
- Licensing and third-party notices reviewed.
- Release package reproducible from the tagged commit.

## Parallel future track — modular microphone rings

The microphone-array ring is a separate accessory PCB family and should not block fabrication or validation of the main PoE speaker board.

Concept: provide multiple ring diameters that share the same electrical interface. An installer removes a ceiling-speaker grille, selects a ring that fits the usable grille area without obstructing the driver, routes a small cable to the main board, and reinstalls the grille. The main electronics remain common across speaker sizes.

Development goals:
- measure representative ceiling speakers and define useful ring-size families;
- validate an eight-microphone PDM topology against the reserved J4 interface;
- prove one ring electrically and acoustically before cloning the design into additional diameters;
- develop reversible mounting methods and safe cable-routing options;
- characterize grille attenuation, speaker-induced vibration, microphone saturation, beamforming behavior and echo-cancellation requirements;
- keep ring variants electrically interchangeable wherever practical.

See [`hardware/microphone-rings/README.md`](hardware/microphone-rings/README.md) for the concept and proposed development sequence.

## Working rule

Every engineering change should answer three questions:
1. What problem does this change solve?
2. What evidence or calculation justifies it?
3. How will we verify that it worked?

A clean DRC/ERC result is necessary but is not evidence of electrical performance or manufacturing readiness.
