"""Capacitor-only startup estimate, not a MOSFET qualification or simulation."""
import json,re
from pathlib import Path
E=Path(__file__).resolve().parent;m=json.loads((E/'revision-b-design.json').read_text())
caps={}
for ref,c in m['components'].items():
 if ref.startswith('C') and {p['net'] for p in c['pins']}=={'24V_AMP','GND'}:
  q=re.fullmatch(r'([0-9.]+)(u|n)F',c['value']);assert q,(ref,c['value'])
  caps[ref]=float(q[1])*({'u':1e-6,'n':1e-9}[q[2]])
cap=sum(caps.values()); cmax=cap*1.2; vin=24.48
# +20% aggregate capacitance is a screening assumption pending individual part tolerances.
cgate=100e-9; igate_max=30e-6; cgate_min=cgate*.9
slew=igate_max/cgate_min; current=cmax*slew
r={'status':'Proposed ramp only; no parts approved or CAD edits','capacitors_f':caps,'nominal_total_uf':cap*1e6,'screening_max_total_uf':cmax*1e6,'candidate_gate_cap_nf':100,'assumed_gate_cap_tolerance':.1,'nominal_inrush_a':cap*20e-6/cgate,'screening_max_inrush_a':current,'screening_fast_ramp_ms':vin/slew*1000,'nominal_24v_ramp_ms':24/(20e-6/cgate)*1000,'capacitor_only_pass_path_loss_j':.5*cmax*vin**2,'screening_initial_pass_power_w':vin*current,'source':'https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4365.pdf','requirements':['Use the Figure 14 gate-ramp topology; do not add 100 nF directly to the controller GATE and assume fast fault turnoff is preserved.','Treat one pass FET as carrying the whole linear stress until sharing is established. Screen SOA conservatively at 24.48 V, maximum calculated current, for 100 ms at the intended hot initial temperature, then check the entire slower-ramp family through 225 ms; this single point alone is insufficient.','Keep amplifier disabled during charging; regulators and other loads need a separate startup-current model.','Current source bounds are specified at 12 V; verify ramp over the actual voltage trajectory.','100 nF effective capacitance, voltage rating, dielectric behavior, gate resistance and stability require component selection and transient verification.','A prolonged output short is not limited by this ramp. Separate current-limiting/fuse coordination remains required.']}
(E/'bench-inrush-calculation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
