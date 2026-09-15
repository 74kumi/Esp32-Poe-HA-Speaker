# Secondary rail review checkpoint

U7 is TPS62132RGTR, the fixed 3.3 V member of the TPS6213x family. The model connects FB and DEF to GND, VOS to 3V3, AVIN/PVIN and EN to 5V, all switch pins to L4, and AGND/PGND/EP to GND. These match the intended fixed-output topology. FSW is tied to 5V; the datasheet pin-table note recommends VOUT or PG for low-frequency selection, so this connection remains a follow-up item rather than being silently accepted. L4 is 2.2 uH and C53 is 3.3 nF; verify the full output-capacitance/stability envelope and startup loading before release.

Source: TI TPS6213x Rev F, Table 5 (device comparison), pin functions and application guidance: https://www.ti.com/lit/ds/symlink/tps62130.pdf

Five ERC findings remain: undriven power-input nets BENCH_FUSED, GND, 3V3, ETH_3V3A, and 24V_OR. The source symbols for several regulators and power-path devices use passive pin types. Do not simply place power flags to make this report green: verify those stages and correct symbol types/source annotations first. ERC cannot currently establish that every imported circuit has a valid power source.

Next physical review: buck input-capacitor loops, U7 VOS sensing route, inductor/output-capacitor loop, and the amplifier's power and heat-removal paths. The extended In1.Cu ground plane gives Ethernet additional reference copper, but signal-layer transitions and differential pair impedance/length still require review.
