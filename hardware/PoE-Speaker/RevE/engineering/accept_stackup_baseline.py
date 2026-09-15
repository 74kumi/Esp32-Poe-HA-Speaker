from pathlib import Path
import hashlib,json,shutil
D=Path('KiCad-RevE'); main=D/'PoE-Speaker-RevE.kicad_pcb'; trial=D/'ethernet-trial.kicad_pcb'
r=json.loads((D/'reports/stackup-baseline.json').read_text())
assert hashlib.sha256(main.read_bytes()).hexdigest()==r['main_before_sha256'],'Main changed; rebase required'
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text()); assert not d['violations'] and not d['unconnected_items']
backup=D/'before-explicit-stackup.kicad_pcb'; assert not backup.exists()
shutil.copy2(main,backup); shutil.copy2(trial,main)
f=Path('engineering/package_prototype_review.py'); s=f.read_text()
s=s.replace('Next: continue Ethernet differential routing/stackup.','Next: calculate and implement Ethernet differential geometry using the saved JLC04161H-7628 design baseline; see engineering/ETHERNET-STACKUP.md. The main board now has explicit dielectric/copper settings, but impedance is not qualified.')
s=s.replace('2. Qualify Ethernet differential routing against a chosen four-layer stackup and verify continuous return paths.','2. Qualify Ethernet differential routing against the explicit JLC04161H-7628 design baseline and verify continuous return paths. See engineering/ETHERNET-STACKUP.md; pair widths/gaps still need calculation and fabricator confirmation.')
f.write_text(s)
f=Path('engineering/ORDER-RELEASE-REVIEW.md'); s=f.read_text().replace('PCB specifies 1.6 mm overall but contains no explicit dielectric stackup.','Explicit JLC04161H-7628 copper/dielectric baseline is now saved in the PCB; see ETHERNET-STACKUP.md.').replace('Freeze fabricator stackup and copper weights before impedance/current calculations. JLC04161H-7628 is a documented candidate, not an order selection.','Use this baseline for impedance/current calculations. Confirm the stackup, finished copper, plating and impedance geometry with fabrication before order; the saved baseline is not an order approval.')
f.write_text(s)
f=Path('engineering/checkpoint_reve.py'); s=f.read_text().replace("'audit_ethernet_paths.py',","'audit_ethernet_paths.py','audit_ethernet_reference.py',"); f.write_text(s)
print('Accepted stackup-only trial; preserved prior main.')
