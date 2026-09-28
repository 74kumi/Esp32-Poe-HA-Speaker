# RevE procurement source review

Status: point-in-time source review for issue #6; no schematic, PCB, footprint, or generated procurement report was modified.

Input procurement report SHA-256: `3dfe9d548ee20e9049ff3472cc6474819a961201d37c41526692fc432c798af5`.

The Panasonic FR-A document contains all three electrolytic ordering stems used by C1–C6.[1]

Bourns lists `SRP1038A-100M` in the SRP1038A datasheet.[2]

Coilcraft lists both selected XAL variants in its manufacturer product table.[3]

Nexperia identifies `PSMN4R8-100BSE` as a D2PAK MOSFET.[4]

Analog Devices lists the exact `LTC4365HTS8#TRPBF` order code and TSOT-23 package.[5]

Texas Instruments lists `TPS26630RGER` as an active-production 24-pin RGE VQFN order code.[6]

Espressif lists the exact `ESP32-S3-WROOM-1U-N16R8` module variant.[7]

WIZnet identifies W5500 and its 48-pin LQFP package in the manufacturer datasheet.[8]

Murata's official product page lists the exact `BLM18PG121SN1D` packaging variant as an in-production 1608/0603 SMD ferrite bead with 120 ohm impedance at 100 MHz.[9]

Abracon's official ASE-series datasheet defines a 3.3 V, 3.2 x 2.5 mm SMD oscillator and separate ordering fields for operating-temperature code `L`, stability code `C`, and reel code `T`.[10] DigiKey catalogs the resulting 25 MHz manufacturer order code as `ASE-25.000MHZ-L-C-T`, not the repository's `ASE-25.000MHZ-LC-T` string.[11]

Together, these sources support manufacturer identity for all eighteen currently incomplete references, while exposing an order-code correction required for X2.[1][10][11]

The protection-device order codes and package families are directly present in manufacturer ordering data.[4][5][6]

The controller and Ethernet-device identities are likewise present in their manufacturer documents.[7][8]

## Manufacturer-source matches

| References | Current MPN | Manufacturer supported by primary source | Source-review result |
|---|---|---|---|
| C1, C2 | `EEUFR1E102` | Panasonic Industry | FR-A datasheet contains the ordering stem; lead/taping suffix and exact case dimensions still require confirmation.[1] |
| C3, C4 | `EEUFR1V102` | Panasonic Industry | FR-A datasheet contains the ordering stem; lead/taping suffix and exact case dimensions still require confirmation.[1] |
| C5, C6 | `EEUFR1H101` | Panasonic Industry | FR-A datasheet contains the ordering stem; lead/taping suffix and exact case dimensions still require confirmation.[1] |
| FB2 | `BLM18PG121SN1D` | Murata Manufacturing | Exact packaging variant and 1608/0603 size appear on the official product page.[9] |
| L1, L2 | `SRP1038A-100M` | Bourns | Exact MPN appears in the manufacturer datasheet.[2] |
| L3 | `XAL5050-822MEC` | Coilcraft | Exact MPN appears in the manufacturer product table.[3] |
| L4 | `XAL5030-222MEC` | Coilcraft | Exact MPN appears in the manufacturer product table.[3] |
| Q3, Q4 | `PSMN4R8-100BSE` | Nexperia | Exact MPN appears in the manufacturer datasheet as a D2PAK/SOT404 MOSFET.[4] |
| U15 | `LTC4365HTS8#TRPBF` | Analog Devices | Exact MPN appears in the manufacturer ordering table as an eight-lead TSOT-23 part.[5] |
| U16 | `TPS26630RGER` | Texas Instruments | Exact MPN appears in the manufacturer package information as a 24-pin RGE VQFN part.[6] |
| U2 | `ESP32-S3-WROOM-1U-N16R8` | Espressif Systems | Exact module variant appears in the manufacturer series table with 16 MB flash, 8 MB PSRAM, and the external-antenna `1U` form.[7] |
| U3 | `W5500` | WIZnet | Manufacturer datasheet identifies W5500 as a 48-pin LQFP Ethernet controller.[8] |
| X2 | `ASE-25.000MHZ-LC-T` | Abracon | ASE family and option codes are source-supported, but the current MPN omits the separator in the cataloged `ASE-25.000MHZ-L-C-T` order code.[10][11] |

These matches support proposed manufacturer names and primary-source URLs for all 18 references. They do **not** prove that the custom `*_RevB` footprints match the manufacturer land patterns, that polarity/orientation is correct, or that the components are available from authorized suppliers.

## X2 order-code blocker

The procurement report's `ASE-25.000MHZ-LC-T` value should not be treated as orderable. The official ordering grammar and the DigiKey manufacturer-product record support `ASE-25.000MHZ-L-C-T`; the schematic metadata should be corrected only after the exact X2 package, pinout, temperature range, and stability requirements are reviewed.[10][11]

### Read-only X2 package and pin review

- Abracon's recommended land pattern uses 2.10 mm horizontal and 1.65 mm vertical pad-center spacing with 1.30 mm x 1.10 mm pads.[10]
- `X2_RevB` uses centers at x = +/-1.05 mm and y = +/-0.825 mm with 1.30 mm x 1.10 mm pads, matching those dimensions.
- Abracon defines pin 1 as tri-state/standby, pin 2 as ground/case, pin 3 as output, and pin 4 as VDD.[10] The PCB maps those pins to `3V3`, `GND`, `ETH_25MHZ`, and `3V3`, respectively; tying pin 1 high selects normal oscillation.

The X2 package geometry, orientation, and PCB net mapping therefore match the ASE-series drawing. This does not qualify clock signal integrity, supply decoupling, oscillator startup, lifecycle, or sourcing. The metadata was not changed because the canonical schematic/report refresh path requires KiCad's unavailable `pcbnew` Python module; hand-editing generated artifacts would create an unverified source/report split.

## Remaining unresolved reference

- `F1` / `24T 3.15A250V`: no official manufacturer datasheet was found for the recorded `xcfuse(旭程)` entry. The string is too generic to treat as an approved orderable part.[unverified]

## Required follow-up before BOM approval

1. Confirm Panasonic ordering suffixes, lead spacing, diameter, height, voltage rating, and polarity against the assigned custom footprints.
2. Compare each official package drawing with its `*_RevB` footprint; this document only confirms source identity and package-family claims.
3. Correct X2's exact MPN through the canonical model/schematic/report regeneration path when `pcbnew` is available, and retrieve a primary source for `F1` or replace it with an explicitly approved orderable MPN.
4. Record authorized supplier evidence, lifecycle state, stock risk, and approved alternates separately.
5. Regenerate `procurement-audit.json`, rerun `scripts/audit_procurement_metadata.py --strict`, and update the pinned snapshot only after source metadata changes are reviewed.

This review is not an approved BOM, electrical qualification, package-fit signoff, or fabrication approval.

## Sources

[1] https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1259.pdf
    > "EEUFR1E102( ) 200 2180"
    > "EEUFR1V102( ) 200 500"
    > "EEUFR1H101( ) 200 8000"
[2] https://bourns.com/docs/product-datasheets/srp1038a.pdf
    > "SRP1038A-100M 10 20 20 10 27 30 7.5 12"
[3] https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal50xx
    > "XAL5030-222MEC | 2.2 | 13.2 | 14.5"
    > "XAL5050-822MEC | 8.2 | 31.8 | 35.0"
[4] https://assets.nexperia.com/documents/data-sheet/PSMN4R8-100BSE.pdf
    > "PSMN4R8-100BSE N-channel 100 V 4.8 mΩ standard level MOSFET in D2PAK"
[5] https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4365.pdf
    > "LTC4365HTS8#TRPBF LTFKT 8-Lead Plastic TSOT-23"
[6] https://www.ti.com/lit/ds/symlink/tps2663.pdf
    > "TPS26630RGER Active Production VQFN (RGE)"
[7] https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
    > "ESP32-S3-WROOM-1U-N16R8 16 MB (Quad SPI) 8 MB (Octal SPI)"
[8] https://docs.wiznet.io/img/products/w5500/W5500_ds_v110e.pdf
    > "The W5500 chip is a Hardwired TCP/IP embedded Ethernet controller"
[9] https://pim.murata.com/en-global/pim/details/?partNum=BLM18PG121SN1D
    > "BLM18PG121SN1B,BLM18PG121SN1D,BLM18PG121SN1J Applications Appearance & Shape"
    > "Size code in mm(inch) 1608/0603 Shape SMD"
    > "Impedance (at 100MHz) 120Ω ±25%"
[10] https://abracon.com/Oscillators/ASEseries.pdf
    > "3.3V CMOS Compatible 3.2 x 2.5mm SMD Crystal Oscillator ASE Series"
    > "Operating Temp. I: 0°C ~ +50°C D: -10°C ~ +60°C E: -20°C ~ +70°C F: -30°C ~ +70°C N: -30°C ~ +85°C L: -40°C ~ +85°C"
    > "Overall Freq. Stability J(*): ±20ppm R: ±25ppm K: ±30ppm H: ±35ppm B: ±40ppm C: ±50ppm"
    > "Packaging Blank: Bulk T: 1000pcs/Reel T2: 250pcs/Reel T3: 3000pcs/Reel"
[11] https://www.digikey.com/en/products/detail/abracon-llc/ASE-25-000MHZ-L-C-T/1236885
    > "Manufacturer Product Number | ASE-25.000MHZ-L-C-T"
    > "Detailed Description | 25 MHz XO (Standard) CMOS Oscillator 3.3V Enable/Disable 4-SMD, No Lead"
