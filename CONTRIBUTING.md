# Contributing

Thanks for taking a look at the project. This is still a pre-prototype hardware design, so focused engineering review is more useful than broad redesign proposals.

## Start with the active source

Use the current Rev E design under:

`hardware/PoE-Speaker/RevE/`

The material under `hardware/checkpoints/` is historical and should not be used as the starting point for new changes.

## High-value review areas

The most useful review work right now is:

- Ethernet MDI routing, impedance assumptions, reference continuity, termination, and ESD layout;
- PoE / bench-power protection, startup, inrush, fuse coordination, and fault behavior;
- regulator, DAC, amplifier, grounding, thermal, and current-path review;
- footprints, pin mapping, courtyard / assembly envelopes, connector access, and manufacturability;
- prototype bring-up and validation planning.

See `ENGINEERING-REVIEW.md`, `ORDER-RELEASE-REVIEW.md`, and the open GitHub issues before starting substantial work.

## Main-board change rule

The main board is intentionally being stabilized for a first prototype. Optional features should use the existing expansion interfaces whenever practical.

A proposed main-board change should explain:

1. what problem it solves;
2. what evidence, datasheet guidance, or calculation supports it;
3. why the existing interfaces cannot solve the problem; and
4. how the change will be verified.

Convenience alone is not sufficient reason to reopen the core board design.

## Reporting an engineering finding

Please include as much of the following as practical:

- source revision / PCB hash;
- KiCad version;
- component, pin, and net;
- coordinate or screenshot;
- expected behavior;
- observed concern; and
- supporting datasheet section, calculation, or other evidence.

Clearly distinguish confirmed defects from questions, preferences, and suggested improvements.

## Validation expectations

A clean ERC / DRC result is necessary but does not prove electrical performance, signal integrity, thermal performance, safety, or manufacturability.

Do not describe the design as tested, production-ready, or fabrication-approved unless that claim is supported by the corresponding physical validation or release documentation.

AI-assisted CAD / code changes are welcome as tools, but generated output should be independently reviewed and verified like any other engineering work.
