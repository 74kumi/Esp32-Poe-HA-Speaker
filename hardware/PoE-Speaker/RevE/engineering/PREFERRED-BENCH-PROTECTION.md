# Preferred bench protection candidate

Status: calculated candidate, not implemented in the schematic or PCB.

Use LTC4365 as the next design candidate with two opposing N-channel MOSFETs for disconnect and reverse-input protection. The device's full-temperature OV threshold is 0.4925–0.5075 V and input leakage is bounded at ±10 nA. Its specified fault delay is at most 2 us at 50 mV comparator overdrive and 12 V; this is not a universal 24 V switching-time guarantee. [Manufacturer datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4365.pdf).

Proposed OV divider: 198 kohm top, 4.02 kohm bottom, 0.1% initial tolerance, 10 ppm/C or better. Exact orderable resistor and controller grades remain to be chosen. Under the conservative independent-TCR assumptions in compare_ovp_candidate.py, the trip window is 24.651–25.606 V over -40 to 125 C resistor temperatures. This leaves 171 mV above the assumed 24 V +2% supply and 394 mV below the amplifier's 26 V operating ceiling. Aging and voltage coefficient remain unmodeled.

This is a better static candidate than the earlier TPS26630 divider; it is not proof of surge protection. Preserve Q2/U10 downstream ORing until reverse-current behavior is checked. LTC4365 does not replace current limiting. Select the external FETs against startup SOA, actual bulk capacitance, available fault current, and turnoff energy. Do not treat the 3.15 A fuse as a semiconductor current limiter.

Next implementation chunk: verify the complete reference topology and package pin map, select FETs and current/inrush handling, then build a separate schematic revision. Keep the existing routed PCB intact. The remaining 235 DRC findings and other documented electrical review items are unchanged.
