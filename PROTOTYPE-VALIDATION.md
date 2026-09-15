# Prototype Validation Plan

This document defines the minimum validation sequence for the first fabricated prototype. Record actual measurements, equipment used, board revision, source commit/hash and ambient conditions. Do not replace measurements with expected values after the board exists.

## 1. Before power

- Confirm board revision and source commit/hash.
- Inspect orientation and polarity of connectors, diodes, electrolytics, ICs and polarized passives.
- Inspect for solder bridges, opens, tombstoning and questionable via-in-pad joints.
- Verify heatsink and mechanical clearances.
- Measure resistance from each primary rail to ground and record the result.
- Confirm current-limit and emergency power-removal method before energizing.

## 2. Current-limited bench bring-up

Begin with an isolated, current-limited bench supply rather than PoE.

Record:
- Input voltage and current at startup.
- 3.3 V rail.
- Other regulated rails and amplifier supply rails.
- ESP32 boot behavior and serial output.
- Regulator, amplifier and protection-device temperatures after initial idle operation.

Stop immediately for unexpected current draw, unstable rails, smoke, odor or rapid thermal rise.

## 3. Digital subsystem

Verify:
- ESP32 reliable boot/reset behavior.
- Serial diagnostic output.
- W5500 SPI communication.
- Ethernet PHY/link indication.
- DHCP and static-IP operation if supported by the test firmware.
- Sustained network traffic without unexplained packet loss or link renegotiation.

Record test duration, traffic method and any error counters available.

## 4. Audio path

Start with low output power.

Verify:
- DAC initialization.
- Controlled test-tone generation.
- Amplifier mute and enable behavior.
- Correct channel/output polarity.
- Idle current and idle noise.
- Output waveform into a known dummy load before attaching a speaker.

Characterize, as practical:
- Output power into 4 ohms.
- Supply current versus output level.
- Clipping threshold.
- Frequency response.
- Noise and distortion using available equipment.

The 30 W into 4 ohms target is not considered validated until measured.

## 5. Thermal test

Record ambient temperature and temperatures at key components at approximately:
- idle;
- moderate output;
- near intended sustained output;
- 1 minute;
- 5 minutes;
- 15 minutes;
- 30 minutes where safe.

Priority components include the amplifier, regulators, PoE/power conversion components, protection devices, high-current connectors and any visibly stressed copper/via regions.

## 6. PoE test

Only after bench-power bring-up succeeds:
- Verify expected PoE classification/negotiation behavior where applicable.
- Verify startup without repeated negotiation/reset cycles.
- Compare operating rails and temperatures with bench-power operation.
- Exercise Ethernet and audio simultaneously from PoE.
- Record switch/PSE telemetry if available.

## 7. Protection and fault behavior

Perform only tests that can be conducted safely with appropriate current limiting and sacrificial protection.

Review or test as practical:
- input overcurrent behavior;
- eFuse/protection shutdown and recovery;
- short-circuit response on accessible protected rails;
- amplifier fault/mute behavior;
- brownout / power interruption recovery;
- repeated startup behavior.

Do not intentionally exceed component absolute maximum ratings merely to prove a theoretical failure mode.

## 8. Pass / fail handling

Every unexpected result becomes a GitHub issue with:
- board revision and source hash;
- test step;
- expected result;
- observed result;
- measurement and test equipment;
- photos/screenshots/logs when useful;
- suspected cause, clearly labeled as hypothesis if unproven.

Prototype validation is complete only when all required tests have recorded results and unresolved failures are either corrected or explicitly accepted with rationale.
