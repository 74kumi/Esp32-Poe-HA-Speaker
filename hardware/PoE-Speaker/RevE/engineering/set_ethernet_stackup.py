"""Create a stackup-only trial; never overwrite the validated main board."""
from pathlib import Path
import hashlib, shutil, json
D=Path('KiCad-RevE'); main=D/'PoE-Speaker-RevE.kicad_pcb'
raw=main.read_text(); assert '(stackup' not in raw
block='''
		(stackup
			(layer "F.SilkS" (type "Top Silk Screen"))
			(layer "F.Paste" (type "Top Solder Paste"))
			(layer "F.Mask" (type "Top Solder Mask") (thickness 0.01524) (epsilon_r 3.8))
			(layer "F.Cu" (type "copper") (thickness 0.035))
			(layer "dielectric 1" (type "prepreg") (thickness 0.2104) (material "FR4 7628") (epsilon_r 4.4))
			(layer "In1.Cu" (type "copper") (thickness 0.0152))
			(layer "dielectric 2" (type "core") (thickness 1.065) (material "FR4") (epsilon_r 4.6))
			(layer "In2.Cu" (type "copper") (thickness 0.0152))
			(layer "dielectric 3" (type "prepreg") (thickness 0.2104) (material "FR4 7628") (epsilon_r 4.4))
			(layer "B.Cu" (type "copper") (thickness 0.035))
			(layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01524) (epsilon_r 3.8))
			(layer "B.Paste" (type "Bottom Solder Paste"))
			(layer "B.SilkS" (type "Bottom Silk Screen"))
			(dielectric_constraints yes)
		)'''
trial=D/'ethernet-trial.kicad_pcb'
trial.write_text(raw.replace('\t(setup','\t(setup'+block,1))
for ext in ['kicad_pro','kicad_dru']: shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
assert trial.read_text().replace(block,'',1)==raw
(D/'reports/stackup-baseline.json').write_text(json.dumps({
 'source':'https://jlcpcb.com/impedance','checked_date':'2026-09-14',
 'stackup':'JLC04161H-7628','status':'design baseline; not fabrication approval',
 'main_before_sha256':hashlib.sha256(main.read_bytes()).hexdigest(),
 'nominal_order_thickness_mm':1.6,'copper_dielectric_sum_mm':1.5862,
 'outer_copper_mm':0.035,'inner_copper_mm':0.0152,
 'outer_dielectric_mm':0.2104,'core_mm':1.065,
 'mask_above_trace_mm':0.01524,'mask_above_substrate_mm':0.03048,
 'mask_between_traces_mm':0.03048,
 'note':'KiCad mask thickness models above-trace value only. Do not flatten the nonuniform mask into the impedance calculator. No loss tangent was assumed. No trace geometry was qualified.',
 'copper_and_placements_unchanged':True},indent=2))
print('Created stackup-only ethernet trial; copper and placements unchanged.')
