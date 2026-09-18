# Procurement metadata audit

This repository includes a read-only audit for the generated RevE procurement report:

```bash
python3 scripts/audit_procurement_metadata.py \
  hardware/PoE-Speaker/RevE/KiCad-RevE/reports/procurement-audit.json
```

The command prints deterministic JSON containing the SHA-256 of the exact input report. Add `--strict` to return exit status `1` when any purchase-required component lacks a reference, manufacturer, manufacturer part number, or datasheet URL. Components explicitly marked `No purchase required` are excluded from those completeness gates.

Point-in-time snapshot checked on 2026-09-18 for procurement report SHA-256 `3dfe9d548ee20e9049ff3472cc6474819a961201d37c41526692fc432c798af5`:

- 209 total component records.
- 179 purchase-required component records.
- 30 records explicitly marked `No purchase required`.
- 18 purchase-required records lack manufacturer metadata.
- 19 purchase-required records lack a datasheet URL.
- No purchase-required record lacks an MPN.
- All 179 purchase-required records remain marked as candidates requiring further qualification.

The strict audit currently fails by design. The integration test pins both this input hash and these counts so a regenerated report requires deliberate review and snapshot refresh. This is evidence that issue #6 remains open, not a reason to weaken the check.

## Limits

Metadata completeness does **not** verify availability, lifecycle state, authorized distributors, electrical suitability, package/footprint compatibility, polarity, orientation, or approved alternates. It does not make the BOM order-ready and is not fabrication approval. Those items require manufacturer data, current supplier evidence, and engineering review.
