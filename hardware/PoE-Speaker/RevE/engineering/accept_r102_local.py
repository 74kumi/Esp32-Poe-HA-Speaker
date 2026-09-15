from pathlib import Path
import pcbnew as p,json,hashlib,shutil
D=Path('KiCad-RevE');E=Path('engineering');src=D/'PoE-Speaker-RevE.kicad_pcb'
r=json.loads((D/'reports/r102-placement-trial.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['main_before_sha256']
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text());assert not d['violations'] and not d['unconnected_items']
b=p.LoadBoard(str(D/'ethernet-trial.kicad_pcb'));point=p.VECTOR2I(p.FromMM(117.1),p.FromMM(64.1563))
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.25));assert not box.Contains(point),(f.GetReference(),pad.GetNumber())
backup=D/'before-r102-local.kicad_pcb';assert not backup.exists();shutil.copy2(src,backup);shutil.copy2(D/'ethernet-trial.kicad_pcb',src)
f=E/'revision-e-design.json';m=json.loads(f.read_text());m['components']['R102'].update(position=[116.3,64.7],angle=270,side='Bottom');f.write_text(json.dumps(m,indent=2)+'\n')
r.update(status='accepted',drc_findings=0,unconnected_items=0,signal_branch_before_mm=6.92,signal_branch_after_mm=.917,limits='Branch lengths approximate. New signal tap via is a remaining discontinuity, not impedance qualification. Required R103 analog-supply branch retained.')
(D/'reports/r102-local-placement.json').write_text(json.dumps(r,indent=2))
note='''

## 2026-09-15: accepted local R102 termination

Moved R102 to B.Cu (116.3,64.7), angle 270. Its TX_N tap uses a new 0.6/0.3 mm via at (117.1,64.1563) on the existing front signal track and about 0.917 mm of bottom track, replacing about 6.92 mm of front branch. The supply pad connects to the existing analog-supply via (117.5,65.3196). Via-to-component-pad bounding-box guard passes at 0.25 mm. Main PHY-to-jack routes are unchanged. This removes a long termination branch but adds a signal-tap via and does not qualify impedance or pair coupling. DRC and unconnected counts zero; underside placement visually inspected. Model synchronized; backup before-r102-local.kicad_pcb.

Rejected earlier position/orientation introduced nine DRC errors. Testing removal of the four-track R103 supply path produced one disconnected analog-supply island: it is NOT redundant. Restored all four tracks. Next rerouting must provide a replacement supply connection before removing that path. TX_N jack fanout remains another crossing obstacle. No footprint library geometry changed.
'''
for name in ['REVE-TRUNK-ROUTING.md','ETHERNET-STACKUP.md']:
 with (E/name).open('a',encoding='utf-8') as out:out.write(note)
f=E/'package_prototype_review.py';s=f.read_text().replace('Next: coordinate Ethernet TX_N/R102 and R103 supply corridor with both pair fanouts.', 'Next: reroute the TX_N jack fanout and replace the required R103 analog-supply corridor while planning both differential pairs. R102 is now local on B.Cu (116.3,64.7), with a 0.917 mm branch and a new signal-tap via; see reports/r102-local-placement.json. Removing the four-track R103 supply path alone disconnected one analog-supply island, so it was restored.')
f.write_text(s,encoding='utf-8')
print('Accepted R102 placement; model synchronized and via/pad guard passed.')
