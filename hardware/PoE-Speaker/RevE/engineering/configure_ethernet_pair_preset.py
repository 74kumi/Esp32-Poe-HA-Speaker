"""Save sourced Ethernet routing defaults in a project trial, not existing copper."""
from pathlib import Path
import json,copy,shutil,hashlib
D=Path('KiCad-RevE'); main=D/'PoE-Speaker-RevE.kicad_pro'
cfg=json.loads(main.read_text()); ns=cfg['net_settings']
assert not any(c['name']=='Ethernet100' for c in ns['classes'])
nc=copy.deepcopy(next(c for c in ns['classes'] if c['name']=='Default'))
nc.update(name='Ethernet100',priority=0,diff_pair_width=0.225806,diff_pair_gap=0.2032,track_width=0.225806)
ns['classes'].append(nc)
for net in ['ETH_TX_P','ETH_TX_N','ETH_RX_P','ETH_RX_N']:
 ns['netclass_patterns'].append({'netclass':'Ethernet100','pattern':net})
(D/'ethernet-trial.kicad_pro').write_text(json.dumps(cfg,indent=2)+'\n')
for ext in ['kicad_pcb','kicad_dru']: shutil.copy2(D/f'PoE-Speaker-RevE.{ext}',D/f'ethernet-trial.{ext}')
report={
 'source':'https://jlcpcb.com/pcb-impedance-calculator','observed_utc_date':'2026-09-15',
 'inputs':{'board_type':'Rigid','layers':4,'nominal_thickness_mm':1.6,'outer_copper_oz':1,'inner_copper_oz':0.5,'unit':'mil','target_ohms':100,'type':'Differential Pair (Non coplanar)','signal_layer':'L1','top_reference':None,'bottom_reference':'L2','trace_gap_mil':8,'width_spacing_complement':False},
 'result':{'stackup':'JLC04161H-7628','label':'Standard/Finished thickness1.59mm±10%','width_mil':8.89,'gap_mil':8,'width_mm':0.225806,'gap_mm':0.2032,'calculator_tolerance_percent':0.5},
 'interpretation':'The displayed 0.5% tolerance is a calculator setting, not a fabricator production guarantee. Masked noncoplanar model selected. Nearby same-layer copper must be kept sufficiently remote or evaluated with a coplanar model. Existing tracks are unchanged and are not impedance-qualified. These are routing defaults, not enforcing DRC width/gap constraints.',
 'project_before_sha256':hashlib.sha256(main.read_bytes()).hexdigest(),
 'pcb_sha256':hashlib.sha256((D/'PoE-Speaker-RevE.kicad_pcb').read_bytes()).hexdigest()}
(D/'reports/ethernet-impedance-calculator.json').write_text(json.dumps(report,indent=2))
print('Trial project has Ethernet100 routing defaults:',nc['diff_pair_width'],nc['diff_pair_gap'])
