# Bench startup checkpoint

Calculated from the actual design model: 2214.22 uF directly on 24V_AMP. A screening +20% capacitance assumption gives 2657.064 uF.

A proposed 100 nF gate-ramp capacitor gives approximately 0.443 A capacitor-only inrush and 120 ms charging at 24 V nominal. Using 30 uA gate drive, -10% ramp capacitance and +20% load capacitance gives 0.886 A and 73.44 ms at 24.48 V. The opposite gate-drive/capacitance corner extends charging to about 224.4 ms. The current-source bounds are specified under the manufacturer's 12 V test conditions; these are screening estimates, not guaranteed startup limits.

Capacitor charging alone dissipates about 0.796 J in the series pass path at the screening maximum, with initial dissipation near 21.7 W in the fast-ramp case. Do not approve a low-RDS(on) switching MOSFET by current rating or avalanche energy alone. Check linear SOA at hot initial temperature over the full ramp trajectory and repetition rate, assigning the full stress to one FET unless sharing is established.

Use the manufacturer's Figure 14 ramp network so its added capacitance does not defeat fast turnoff. [LTC4365 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4365.pdf). The network values and physical layout require validation with the selected MOSFETs.

No MOSFET is approved in this checkpoint. Remaining loads during startup, amplifier disable sequencing, output-short protection and PoE backfeed must be included. The proposed ramp controls capacitor charging; it is not a current limiter during a fault.

Next: select a linear-SOA-qualified FET pair and check these trajectories, or choose an integrated hot-swap/current-limit architecture if the discrete path becomes larger. No schematic or PCB changes were made.
