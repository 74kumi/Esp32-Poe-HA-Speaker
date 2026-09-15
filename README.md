# ESP32 PoE HA Speaker

PoE network speaker main-board prototype using ESP32-S3, W5500 Ethernet, PCM5122 DAC and TPA3116D2 amplifier. The target is 30 W into 4 ohms. Home Assistant integration, firmware and measured performance are not yet validated. A modular eight-microphone ring family is planned as a separate future board; see [microphone-ring concept](hardware/microphone-rings/README.md).

**Engineering prototype — not ready to manufacture or power up.**

![Rev E board preview](board-top.png)

## Get the editable design

- [Latest KiCad Rev E source and engineering reports](PoE-Speaker-RevE-Review.zip)
- [Checkpoint package with earlier design revisions](PoE-Speaker-Checkpoint.zip)
- [Engineering review guide](ENGINEERING-REVIEW.md)
- [Current release blockers](ORDER-RELEASE-REVIEW.md)

Extract the Rev E ZIP before opening `KiCad-RevE/PoE-Speaker-RevE.kicad_pro` in KiCad 10. Keep its adjacent libraries and design rules together. The repository currently distributes complete source packages; paths in engineering notes refer to files inside the extracted package. Review ZIPs are not fabrication packages.

The review checkpoint contains 209 components and 616 connected pins. Saved DRC/ERC reports have zero findings under the saved rule profile, and model/schematic/PCB connected-pin mappings agree. Missing courtyard checks and some inherited metadata checks are disabled. These checks do not establish circuit performance or manufacturing readiness.

Recent work moved both receive main routes to the front layer and added an 8.379 mm parallel trunk at calculator-derived geometry. Transmit coupling, ESD/termination branches, reference continuity, protection/current/thermal calculations and assembly checks remain open.

## Engineering help welcome

Please open an issue with the PCB hash from `KiCad-RevE/reports/revision-status.json`, component/pin/net references, coordinates, a clear finding and supporting datasheet or calculation. Review priorities are Ethernet integrity, input protection and fault behavior, regulator/audio circuits, footprint correctness and manufacturing/thermal constraints.

This design was developed with AI-assisted CAD scripting. Independent engineering review and prototype measurements are needed. No assembled-board test results are claimed.

## License

Original hardware design materials in this repository are available for personal, educational, research, and other noncommercial use under the terms in [LICENSE](LICENSE). Commercial manufacture, sale, OEM use, paid integration, or other commercial exploitation requires a separate written commercial license from the copyright holder.

Software, firmware, scripts, and third-party material may be subject to separate terms. Included vendor references, library material, trademarks, and datasheets retain their respective owners' notices and are not relicensed by this project.
