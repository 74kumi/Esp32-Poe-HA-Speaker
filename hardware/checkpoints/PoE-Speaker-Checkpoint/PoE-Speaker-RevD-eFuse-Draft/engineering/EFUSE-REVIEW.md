# Revision D shared supply protection

Development circuit: TPS26630RGER sits between the joined ideal-diode outputs (24V_OR) and every original 24V_AMP load. Bench reverse/overvoltage protection remains upstream. B_GATE and DRV are unused: reverse blocking is assigned to the existing upstream circuits, not to this eFuse alone.

Calculated settings: 18/6.04 = 2.98 A nominal current limit; 1.2*(1+158/10) = 20.16 V UVLO; 1.2*(1+200/10) = 25.2 V OV cutoff; 1.2*(1+174/10) = 22.08 V power-good threshold. These are nominal values, not guaranteed switching points. MODE floats for latch-off. TP26 permits shutdown/reset by grounding SHDN; its internal pullup avoids depending on downstream 3V3 to start.

The PGOOD open-drain output clamps AMP_SDZ. U11 drives it through R135 (1 kohm), with R129 (10 kohm) to ground. At a 3.3 V command, released level is about 3.0 V; a 130 ohm clamp gives about 0.38 V and less than 3.3 mA. This is a static screening calculation; validate actual IO-expander levels, startup and brownout behavior on the assembled circuit.

C121 = 100 nF gives about 500 V/s and 48 ms to 24 V. Estimated downstream capacitance is 2215.22 uF including new C123: about 1.11 A nominal capacitor charging, or 1.71 A using 20% added bulk capacitance, 90 nF ramp capacitance, 2.225 uA and gain 26. DC-bias/tolerance-qualified capacitor selections and other startup loads remain open. Thermal regulation can change the startup waveform. Approximate nominal stored energy is 0.64 J at 24 V; this is not a thermal qualification.

Source: Texas Instruments TPS2663 Rev G, pin table, electrical characteristics, sections 8.3.2 and 8.3.7, Equation 5: https://www.ti.com/lit/ds/symlink/tps2663.pdf

Remaining work: qualify transient overshoot against the amplifier's 26 V operating ceiling, current-limit tolerances, fuse coordination, input wiring inductance, sustained overload heating, return copper, hot restart, and component order codes. A nominal 3 A limit is not an instantaneous 3 A hard-short ceiling. The first PCB must not be released on this calculation alone.
