# F1 rating evidence and remaining coordination work

Reviewed 2026-09-14. F1 is the imported XC 24T 3.15A250V part. Manufacturer page: https://www.xcfuse.com/smd_fuses/24T_119.html

The manufacturer lists DC breaking capacities for the 250 mA–10 A range: UL 50 A at 125 VDC and 25 A at 250 VDC. It also lists VDE 100 A at 250 VDC through 6.3 A. Thus the earlier statement that F1 has no substantiated DC rating is superseded. Do not extrapolate a higher interrupt rating at 24 V without supporting evidence.

For 3.15 A the page gives nominal melting I²t of 25.78 A²s. Published operating bands allow at least one hour at 125%, 1–120 seconds at 200%, and 10–100 ms at 1000%. The page's approval-symbol legend is inconsistent; do not infer certification status from its circle symbols.

Decision: retain F1 as a candidate. Its voltage/interrupt evidence does not by itself establish coordination with the bench input, MOSFETs, wiring or eFuse. Determine prospective short current and temperature derating, check startup and time-current behavior, and compare fault let-through with the protected hardware. A current-limited bench source may never blow a 3.15 A fuse; staged bring-up must rely on its source limit and active protection rather than expecting fast fuse operation.
