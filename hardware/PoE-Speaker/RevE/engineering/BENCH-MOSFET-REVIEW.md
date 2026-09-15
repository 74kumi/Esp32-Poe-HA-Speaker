# Bench pass-MOSFET screening

Decision: retain PSMN4R8-100BSE as the conditional draft candidate for two new opposing pass FETs. Keep Q1/Q2 in their existing ORing roles. No PCB substitution has been made.

The datasheet identifies a 100 V D2PAK device intended for hot-swap operation. Its tab is drain, pin 1 gate and pin 3 source. Figure 4 was visually inspected; a deliberately conservative 60 V / 1 A point lies below its 25 C mounting-base DC curve. [Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/PSMN4R8-100BSE.pdf).

Using voltage scaling, (175-100)/(175-25) = 0.5, moves that screening point to 30 V / 1 A at a 100 C mounting base. This is an approximation, particularly in thermally unstable regions, not a characterized hot-SOA guarantee. [Nexperia AN50006](https://assets.nexperia.com/documents/application-note/AN50006.pdf).

The calculated capacitor-only envelope, 24.48 V and 0.886 A for up to 224.4 ms, fits inside that conservative rectangle. Taking a DC point avoids using the 100 ms curve for a longer startup. Treat a single FET as bearing the entire stress; do not assume equal power sharing.

This passes a preliminary selection screen, not the completed circuit. The actual mounting-base temperature must remain below the assumed 100 C. Additional startup loads, gate-drive voltage, gate charge, current-limiting and repeated-fault heating still need checking. The published on-resistance test uses 10 V gate drive; the controller minimum enhancement is lower, so do not claim the headline resistance in this circuit.

Next bounded implementation: create an isolated protection schematic draft with the verified controller pin map, two candidate FETs, ramp network and explicit startup-disable requirement. Preserve the routed mainboard until pin mapping and fault-current handling have been reviewed. The original DMNH6012LK3 graph was also archived; it was not approved as the new linear pass device.
