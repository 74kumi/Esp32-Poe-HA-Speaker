# ESP32 PoE Home Assistant Speaker

A PoE-powered network ceiling-speaker controller built around an **ESP32-S3**, **W5500 Ethernet**, **PCM5122 DAC**, and **TPA3116D2 amplifier**.

The long-term goal is a retrofit-friendly Home Assistant / voice-assistant speaker platform: reuse ordinary ceiling speakers, add network audio and control at the speaker, and optionally add a modular microphone-array ring hidden behind the existing grille.

## Project disclaimer

I'm not a hardware engineer — I'm an IT administrator who enjoys electronics, Home Assistant, and building things. I have a working understanding of many of the concepts involved, but this project has also been developed heavily with AI-assisted design, CAD scripting, and review.

I would genuinely welcome review or collaboration from experienced hardware engineers, especially as the project moves toward its first physical prototype.

The finalized engineering handoff is now archived in this repository, but the hardware has not yet been fabricated, assembled, or electrically validated. I cannot claim that the current design will work as intended. Please treat it as an engineering prototype and manufacturing handoff, not a proven product.

![Final RevF manufacturing-release board preview](board-revf.png)

> **RevF manufacturing release:** this is the finalized manufacturing handoff for the RevE PCB design. The electrical CAD revision remains RevE for traceability; RevF identifies the released manufacturing package.
>
> The supplied package was reviewed and verified by an engineer according to the project owner. That review evidence is preserved with the handoff, but it does not replace independent source-file review, fabrication, assembly, or prototype validation. PCBWay should confirm the final 4-layer stack-up and 100 Ω Ethernet impedance before production.

## Project status

| Area | Status |
| --- | --- |
| Main-board schematic / PCB | Rev E finalized engineered source archived |
| Main-board manufacturing release | RevF handoff archived with Gerbers, drills, BOM, CPL, STEP, and notes |
| KiCad source | Rev E source available directly in this repository |
| Main-board saved ERC / DRC | Supplied release reports included; profile-dependent and not a substitute for independent validation |
| Ethernet layout | Finalized: 0.2764 mm / 0.20 mm target geometry; fabricator stack-up confirmation remains |
| Power / protection | Finalized engineering handoff; bench startup, fault, current, and thermal validation remain |
| Audio / amplifier | Circuit, thermal, and acoustic validation still required |
| Firmware | Bring-up firmware not yet complete |
| Home Assistant integration | Planned, not yet validated |
| Microphone array | Six-microphone RGB ring engineered handoff archived; prototype and acoustic validation remain |
| Physical prototype | Not built yet; fabrication package prepared |

A clean ERC/DRC result is a regression check, not proof that the circuit is electrically correct, safe, acoustically suitable, or production-ready.

## Current hardware

The main board is intended to provide:

- ESP32-S3 controller
- wired Ethernet using W5500
- PoE-powered operation with bench-power support for development
- PCM5122 playback DAC
- TPA3116D2 speaker amplifier
- target of approximately **30 W into 4 ohms**, subject to real prototype validation
- programming / debug access
- expansion interfaces, including the reserved J4 microphone-ring connector

### Current Rev E board preview

![Current Rev E board preview](board-top.png)

The image above reflects the current Rev E board source more closely than the historical 3D render at the top of this README. The KiCad files remain the authoritative design reference.

### Open the Rev E design

The active source is tracked directly in Git:

- [Rev E KiCad project](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pro)
- [Rev E PCB](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pcb)
- [Rev E schematic](hardware/PoE-Speaker/RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_sch)
- [Rev E engineering notes](hardware/PoE-Speaker/RevE/engineering/)
- [RevF manufacturing package](hardware/PoE-Speaker/RevF/Manufacturing/README-PCBWay.md)
- [RevF board preview](board-revf.png)
- [Historical design checkpoints](hardware/checkpoints/)

Open the project in **KiCad 10**. Keep the adjacent project-local footprint library, symbol library, tables, design rules, BOM, and generated netlist together.

## Modular microphone rings

The project now includes a supplied, engineer-reviewed six-microphone RGB ring handoff. It is separate from the main PoE board and is intended to connect through the main-board J4 expansion interface. The ring package includes KiCad source, custom libraries, BOM, placement data, Gerbers, drills, STEP models, datasheets, design notes, and engineering reports.

- [Microphone-ring concept and status](hardware/microphone-rings/README.md)
- [Final six-microphone RGB ring handoff](hardware/microphone-rings/ESP32-S3-Microphone-RGB-Ring/)
- [Listening / status-light plan](hardware/microphone-rings/LED-STATUS-LIGHT-PLAN.md)
- [Main-board J4 connector definition](hardware/PoE-Speaker/RevE/engineering/CONNECTOR-GUIDE.md)

The archived ring is a six-microphone engineered design; it should not be described as an already validated eight-microphone production system. Electrical bring-up, cable/interface validation, mechanical fit, microphone performance, vibration behavior, and acoustic/echo testing remain outstanding.

## Engineering status and roadmap

The current release state is **final engineered PCB handoffs archived**:

- Main board: RevE editable CAD with a RevF manufacturing release package.
- Microphone ring: six-microphone RGB engineered handoff with manufacturing outputs.
- Provenance: supplied final files, reports, and supporting evidence are preserved; embedded history repositories, lock files, and editor session artifacts were excluded.

Remaining work before production approval includes:

1. Confirm the PCBWay 4-layer stack-up, finished thickness, copper assumptions, and 100 Ω Ethernet impedance.
2. Fabricate and assemble a prototype from the RevF handoff.
3. Execute controlled PoE, bench-power, startup, protection, Ethernet, regulator, DAC, amplifier, thermal, and fault testing.
4. Bring up the six-microphone ring through J4 and validate its power, clock/data, I2C/RGB control, cable behavior, and connector pinout.
5. Measure microphone response, vibration coupling, grille fit, acoustic shadowing, simultaneous playback behavior, and echo-cancellation requirements.
6. Complete firmware bring-up and Home Assistant integration after the hardware interfaces are validated.

Project documents:

- [Roadmap](ROADMAP.md)
- [Engineering review guide](ENGINEERING-REVIEW.md)
- [Order / release review](ORDER-RELEASE-REVIEW.md)
- [Prototype validation plan](PROTOTYPE-VALIDATION.md)
- [Contribution guidance](CONTRIBUTING.md)
- [GitHub issues](https://github.com/74kumi/Esp32-Poe-HA-Speaker/issues)

## Repository layout

```text
.
├── docs/
│   ├── HISTORY.md
│   └── images/
│       └── early-board-render.png
├── hardware/
│   ├── PoE-Speaker/
│   │   ├── RevE/
│   │   │   ├── KiCad-RevE/        # current editable board source
│   │   │   └── engineering/       # design reviews, calculations and scripts
│   │   └── RevF/Manufacturing/    # fabrication and assembly release outputs
│   ├── microphone-rings/
│   │   ├── ESP32-S3-Microphone-RGB-Ring/ # engineered ring handoff
│   │   └── README.md              # concept, interface, and validation status
│   └── checkpoints/               # historical board revisions
├── ENGINEERING-REVIEW.md
├── ORDER-RELEASE-REVIEW.md
├── PROTOTYPE-VALIDATION.md
├── ROADMAP.md
└── board-top.png
```

## Contributing / reviewing

Engineering review is welcome, especially around Ethernet signal integrity, protection / fault behavior, power conversion, amplifier implementation, thermal design, footprints, acoustic performance, and manufacturability.

When reporting a hardware finding, please include the affected revision, component / pin / net, location where practical, expected behavior, observed concern, and supporting datasheet section or calculation. Clearly distinguish confirmed defects from questions or suggested improvements.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the current review priorities and main-board change policy.

This project has used AI-assisted CAD scripting and review workflows. AI output is not treated as engineering validation; independent review and physical prototype measurements are still required.

## License

Original hardware design materials are available for personal, educational, research, and other noncommercial use under the terms in [LICENSE](LICENSE).

Commercial manufacture, sale, OEM use, paid integration, or other commercial exploitation requires a separate written commercial license from the copyright holder.

Software, firmware, scripts, and third-party material may be subject to separate terms. Vendor references, library content, trademarks, and datasheets retain their respective owners' rights and notices.
