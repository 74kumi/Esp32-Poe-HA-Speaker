# Power review — 2026-09-11

Status: in progress, not a release approval.

## Layout pass after the first draft

115 power trunk segments longer than 2 mm were widened to preliminary targets of 0.6–1.5 mm according to net function. Ninety-two other attempted changes conflicted with existing copper and were reverted. Short escapes, vias and return paths remain unqualified; this does not establish the current capacity of a complete path. The final standard-clearance check retained zero unconnected items and no shorts/crossings.

An explicit 3 mm primary-to-secondary copper review rule now identifies 16 spacing findings. This target is a conservative layout assumption, not a certified creepage/clearance requirement. The optocoupler placement and routing need particular attention: some primary pins face toward the secondary circuitry, and the router passed secondary tracks near primary through-hole pads. Reorient the optocouplers and reroute their paths while preserving the electrical pin map. Also review the Ag5800 underside barrier against the manufacturer's drawing. The module's dielectric rating alone does not qualify the carrier PCB.

The active KiCad DRC report includes the stricter rule; the earlier ordinary 0.2 mm clearance result is retained separately as `reports/standard-clearance-drc.json`.

## Corrected in the design model

**PoE class detection:** R6, R7 and R8 were connected from the PC817 collectors to GND. The emitters are also grounded, so that arrangement cannot generate the intended high logic level when the optocouplers are off. Resistor pin 2 now connects to 3V3. Detection is active low. Firmware must use that polarity.

**5 V buck:** U6 is LMR33630AQRNXRQ1, RNX VQFN. Pin 3 was marked NC and left open. TI's pin-function table explicitly requires this package's NC pad to connect to SW. Pin 3 now joins BUCK5_SW with pin 12. The bootstrap loop must be kept short in layout. [TI datasheet, section 5](https://www.ti.com/lit/ds/symlink/lmr33630-q1.pdf)

## Connections checked, retained

- Ag5800: output 1 is between POE_12V_MID and GND; output 2 is between 24V_POE and POE_12V_MID. C1 and C2 each span their respective output with positive polarity toward the higher voltage. This is the intended series-output arrangement. [Silvertel datasheet, sections 4 and 5.11](https://productinfo.silvertel.com/products/POE/PD/Ag5800/Ag5800v1-4.pdf)
- LM5050-2: IN and the external MOSFET source are on each incoming supply; OUT and drain are on the shared 24V_AMP rail; OFF is grounded. This is the basic forward ORing arrangement. It is not a complete reverse-input or overvoltage protection circuit. [TI LM5050-2 datasheet](https://www.ti.com/lit/ds/symlink/lm5050-2.pdf)
- The 5 V feedback divider is 100k/24.9k. With a nominal 1 V reference, its calculated output is 5.016 V. This calculation does not include reference/resistor tolerances or load regulation.

## Unresolved release blockers

**Bench-input surge protection:** D11 is SMBJ26A. Its 26 V standoff rating must not be interpreted as a 26 V clamp. The amplifier rail is fed through an ideal-diode controller, which does not regulate overvoltage. The regulator is rated for 36 V operation and 38 V absolute maximum; the amplifier's supply limit must also be respected. Coordinate an actual overvoltage-disconnect/clamping design with the input transient specification. Do not select a lower-standoff TVS blindly: it must also tolerate the normal supply. [Vishay SMBJ data](https://www.vishay.com/docs/88392/smbj.pdf), [TI amplifier data](https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf)

**PoE bridges:** D3–D10 now select B5100C, 100 V, in SMC. Thermal design and TVS coordination remain open.

**Remaining review:** detector LED current/resistor dissipation over the PoE voltage range; TVS coordination at the Ag5800 input; regulator passives and soft start; amplifier PBTL/gain/PLIMIT/startup behavior; fuse coordination and reverse bench-input protection; isolation and thermal layout. The schematic and PCB still contain other unreviewed source components.


## Isolation layout update — 2026-09-12

U12–U14 now place their primary pins to the left and secondary pins to the right. The rerouted board passes the preliminary 3 mm primary-to-secondary copper clearance rule with zero findings, zero unconnected items, and no copper shorts or ordinary clearance findings. This supersedes earlier isolation-layout findings; it does not certify insulation or resolve the outstanding protection and thermal design. U5 pin 27 uses a provisional 0.5 mm diameter / 0.3 mm drill via-in-pad escape; qualify assembly and current capacity or redesign it.


## Bridge selection update — 2026-09-12

D3–D10 changed from 60 V SS56 to Diodes Incorporated B5100C (100 V). Its 5 A rating requires the specified case/lead temperature; it is not a free-air board rating. Maximum forward drop is 0.85 V at 5 A. [Manufacturer datasheet](https://www.diodes.com/datasheet/download/B5100C.pdf).

The SMC drawing was compared with the recovered pads: 2.16 × 3.24 mm pads at 7.38 mm pitch. Terminal width up to 3.18 mm and overall span up to 8.13 mm fit those pads; solder-process tolerances still require review. Custom numbering remains pin 1 anode, pin 2 cathode. Old supplier identifiers were cleared.

This increases normal reverse-voltage headroom; it does not establish surge immunity. Confirm TVS coordination and bridge temperature for the selected PoE load before release. Next small chunk: bench-input overvoltage disconnect.
