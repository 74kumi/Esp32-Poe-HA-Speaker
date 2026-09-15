# PoE speaker — Revision B development

Open `PoE-Speaker-RevB.kicad_pro` in KiCad 10. This revision is **not ready for fabrication**. The original migration is preserved separately in `../KiCad-Recovered`.

## Changes implemented

- ESP32-S3-WROOM-1U-N16R8 and W5500 replace the original ESP32/RMII architecture. Four PDM data lines reserve support for eight microphones on a future separate ring. GPIO35–37 remain unused because the module uses octal PSRAM.
- J1 cable-side PoE pickup uses pins 13–16. PHY-side center taps 12 and 6 now belong to the W5500 interface. Pins 1 and 7 are unused.
- W5500 analog supply filtering, termination, reference resistor, reset delay, SPI damping and 25 MHz oscillator are included.
- C1–C6 now use physical radial capacitor footprints and specified Panasonic FR parts. L1–L4 use rated inductors and footprints constructed from manufacturer land patterns.
- TP10 and TP11 now expose SPI clock and MOSI.
- Local symbol and footprint libraries travel with the project. Thirteen editable schematic pages and 179 footprints are generated.

## Validation and limits

`reports/net-validation.json` compares the KiCad-exported schematic netlist and saved PCB pad assignments to the explicit revised model. This checks file generation and pin mapping; it does not prove that the circuit works. `reports/schematic-svg` contains KiCad-rendered sheets.

The board has a proposed 160 × 100 mm outline around the existing mounting holes. All 179 parts have been placed without expanded body-box overlaps. A local routing pass has produced actual editable copper; see `reports/first-board-draft.json` and `reports/board-drc.json` for the current counts and remaining findings. This is a **first layout draft**, not a production routing solution. Existing recovery copper was not copied because it does not implement the revised circuit.

The initial router uses 0.2 mm traces and 0.15 mm fine-pitch escapes. Those widths are **not a validated power-distribution design**. High-current paths, ground planes, Ethernet differential-pair geometry, isolation and heat flow still require dedicated routing work. Do not order this draft.

Most recovered components still use generic pin-block symbols with passive electrical pin types. ERC is therefore incomplete as a circuit check. Power-source pin modeling remains outstanding; do not suppress those errors as a substitute for reviewing the power circuit.

## Work remaining before release

1. Complete power and protection audit: PoE bridge reverse-voltage margin, Ag5800 series outputs, ORing, regulator compensation/layout, amplifier PBTL configuration and thermal limits.
2. Review remaining source component pin types, actual part numbers, voltage ratings and footprint pin mappings. Replace generic schematic graphics with conventional symbols where practical.
3. Refine placement for switching loops, isolation and audio performance. Verify mechanical clearances, mounting hardware and connector access.
4. Replace provisional power and Ethernet routes with qualified geometry; add appropriate planes/thermal vias and isolation clearances, choose a fabrication stackup and verify Ethernet impedance.
5. Resolve electrical and board checks without hiding findings. Produce fabrication and assembly outputs only after those checks pass.
6. Implement and bench-test firmware for simultaneous four-line PDM capture, DAC playback, SPI Ethernet and PoE power limiting. Speaker selection and microphone-ring geometry remain future inputs.

## Reproducibility

Run `engineering/design_revision.py`, then `engineering/build_revision.py` with KiCad's Python from the project root. Export a KiCad XML netlist to `reports/schematic-netlist.xml`, then run `engineering/validate_revision.py`. `engineering/place_draft.py` creates the placement and Specctra input; `engineering/finish_draft.py` imports the locally generated routing session. **The builder discards later placement and routing when rerun. Preserve the routed board before rebuilding.**

## Reference documents

- [ESP32-S3 module datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- [ESP32-S3 peripheral capability definitions](https://raw.githubusercontent.com/espressif/esp-idf/master/components/soc/esp32s3/include/soc/soc_caps.h)
- [W5500 datasheet](https://docs.wiznet.io/img/products/w5500/W5500_ds_v110e.pdf) and [reference circuit](https://docs.wiznet.io/img/products/w5500/w5500_sch_v110_use_mag_.pdf)
- [Bel 2250506 connector drawing](https://www.belfuse.com/media/drawings/products/magjack%20ICMs/dr-mag-2250506.pdf)
- [Bourns SRP1038A](https://www.bourns.com/docs/product-datasheets/srp1038a.pdf): 13.6 mm overall land span, 5.4 mm inner gap, 3.5 mm land height.
- [Coilcraft XAL50xx](https://www.coilcraft.com/getmedia/49bc46c8-4b2c-45b9-9b6c-2eaa235ea698/xal50xx.pdf): 3.31 mm pad-center pitch, 1.18 × 4.70 mm lands.
- [Abracon ASE oscillator](https://abracon.com/Oscillators/ASEseries.pdf)
- Panasonic [EEUFR1E102](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1E102), [EEUFR1V102](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1V102), [EEUFR1H101](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1H101).
