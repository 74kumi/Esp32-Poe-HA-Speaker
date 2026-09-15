# Bench-input overvoltage proposal

Status: selection and static calculation only; not yet added to the schematic or routed board.

The amplifier permits 26 V in normal operation and has a 30 V absolute maximum. The latter is not a design target. [TI amplifier datasheet](https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf).

Candidate: TPS26630 with adjustable overvoltage disconnect. Its OVP threshold is 1.176–1.224 V, input leakage is ±150 nA, and specified turnoff delay can reach 14 us under the datasheet test conditions. [TI eFuse datasheet](https://www.ti.com/lit/ds/symlink/tps2663.pdf).

Proposed divider: 200 kohm from protected input sensing node to OVP, 10 kohm from OVP to ground, both 0.1%. The calculation script enumerates threshold, resistor-tolerance and leakage corners:

- Nominal trip: 25.200 V.
- Static corner range: 24.619–25.783 V.
- Remaining static margin to 26 V: only 0.217 V.
- Working supply assumption: regulated 24 V ±2%. A +5% supply can nuisance-trip.

This is a candidate, not a validated protection solution. Temperature drift, aging and dynamic overshoot are excluded. Do not approve it solely on the static calculation.

Proposed insertion: J2 -> F1 -> input transient clamp -> reverse-polarity stage -> eFuse disconnect -> existing Q2/U10 ORing -> 24V_AMP. Rename the present fused node to BENCH_FUSED; reserve 24V_BENCH_PROTECTED for the disconnect output. D11 belongs upstream of the disconnect; it must not be represented as a 26 V rail clamp. The existing downstream ORing remains necessary until backfeed behavior is independently checked.

Next bounded step: select the reverse-polarity parts, current limit, startup ramp and temperature-stable divider; check the small voltage margin and dynamic response, then create the schematic change. Include the actual downstream bulk capacitance and PoE-powered backfeed condition. No changes to the routed PCB were made in this chunk.


## Temperature review checkpoint

The initial-tolerance calculation above is superseded for selection purposes by the temperature sweep in `bench-ovp-calculation.json`. Assuming independent worst-case TCR signs and resistor temperatures from -40 to 125 C (100 C maximum departure from 25 C):

| Each resistor TCR | Minimum trip | Maximum trip | Static window |
|---|---:|---:|---|
| 10 ppm/C | 24.572 V | 25.832 V | Pass, limited margin |
| 25 ppm/C | 24.502 V | 25.906 V | Pass, limited margin |
| 50 ppm/C | 24.386 V | 26.030 V | Fail |
| 100 ppm/C | 24.155 V | 26.279 V | Fail |

Decision: do not implement this candidate yet. At 25 ppm/C the lower trip is only 22 mV above the assumed supply maximum and the upper trip is only 94 mV below 26 V. Resistor aging and other effects are not included.

The JSON also contains an illustrative ramp calculation. At 10 V/ms, 14 us permits 0.14 V of additional rise if the rail follows the input. That alone exceeds the 94 mV margin. This is a sensitivity example, not a simulated waveform or a guaranteed protection bound; the datasheet delay applies at specified comparator overdrive.

Resume by comparing a more accurate/faster disconnect or a regulated/clamped amplifier supply architecture. Establish acceptable continuous supply range and transient envelope before choosing resistor values. Keep the existing routed draft as a review artifact until the replacement protection circuit is fully specified.
