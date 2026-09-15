# Active PoE Speaker hardware source

This directory contains the **current active main-board design** for the ESP32 PoE Home Assistant Speaker project.

## Current revision

The canonical editable source is:

`RevE/KiCad-RevE/PoE-Speaker-RevE.kicad_pro`

Open it in **KiCad 10** and keep the project-local libraries, tables, design rules, and supporting files together.

The adjacent `RevE/engineering/` directory contains design-review notes, calculations, scripts, fabrication-process notes, connector documentation, and saved reports used during the Rev E engineering review.

## Source policy

- Active editable KiCad source belongs here.
- Historical board snapshots belong under `../checkpoints/`.
- Manufacturing-release outputs should be generated from a specific reviewed/tagged source revision and clearly identified as release artifacts rather than active design source.
- KiCad session/local-state files and editor backups should not be committed.

The current board remains an engineering prototype. A clean ERC/DRC result does not establish electrical performance, safety, signal integrity, thermal performance, or manufacturing readiness.
