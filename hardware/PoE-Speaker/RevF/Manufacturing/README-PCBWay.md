# PoE-Speaker RevE — PCBWay Manufacturing Package

Use this package for PCB fabrication and PCBA assembly. It intentionally excludes historical KiCad checkpoints and development files.

## Fabrication
- Upload every file in `Gerbers/` to PCBWay.
- The package contains four copper layers, solder mask, paste, silkscreen, Edge.Cuts, the Gerber job file, and separate PTH/NPTH drill files.

## Assembly
- Use `Assembly/PoE-Speaker-RevE.csv` as the BOM.
- Use `Assembly/PoE-Speaker-RevE-all.pos` as the pick-and-place/CPL file.
- TP25, TP26, and TP27 are bare SMD test-point pads and are not placement components.

## Mechanical/build
- `Mechanical/PoE-Speaker-RevE-assembly.step` is the final assembly STEP reference.
- U5, TPA3116D2DADR, requires an external top-side heatsink. See the PDF in `Notes/`.

## Validation
- Fresh KiCad PCB DRC: 0 violations, 0 unconnected pads, 0 footprint errors.
- Fresh KiCad ERC: 0 errors, 0 warnings.
- Board: 4 layers, approximately 200.40 x 80.07 mm, 1.58468 mm nominal CAD thickness.
- Ethernet final geometry: 0.2764 mm width / 0.20 mm pair gap.

See `MANIFEST.json` for file sizes and SHA-256 hashes.

## Final engineered handoff provenance

The RevE source and RevF manufacturing outputs in this directory were imported from the supplied `Final Engineered Files` package. The user reports that the PCB package was reviewed and verified by an engineer. The included report, DRC image, and impedance-reference images are preserved in `Notes/` as supplied evidence; they are not a substitute for independent source-file review or physical prototype validation.

Traceability:

- Editable CAD remains RevE: `../../RevE/KiCad-RevE/`.
- RevF identifies this manufacturing release package.
- The final package was imported without embedded `.history`, `.git`, lock, or KiCad session artifacts.
