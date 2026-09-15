from pathlib import Path
import pcbnew as p,json,hashlib,shutil
D=Path('KiCad-RevE');E=Path('engineering');src=D/'PoE-Speaker-RevE.kicad_pcb'
r=json.loads((D/'reports/tx-termination-trial.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['main_before_sha256']
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text());assert not d['violations'] and not d['unconnected_items']
b=p.LoadBoard(str(D/'ethernet-trial.kicad_pcb'));point=p.VECTOR2I(p.FromMM(119.7),p.FromMM(63.975))
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.25));assert not box.Contains(point),(f.GetReference(),pad.GetNumber())
backup=D/'before-r101-local.kicad_pcb';assert not backup.exists();shutil.copy2(src,backup);shutil.copy2(D/'ethernet-trial.kicad_pcb',src)
f=E/'revision-e-design.json';m=json.loads(f.read_text());m['components']['R101'].update(position=[120.5,64.8],angle=90,side='Bottom');f.write_text(json.dumps(m,indent=2)+'\n')
r.update(status='accepted',drc_findings=0,unconnected_items=0,signal_branch_before_mm=5.3695,signal_branch_after_mm=1.59,limits='Approximate whole-segment branch lengths. Main differential routing remains unqualified. RX_N top-layer extension rejected for three crossings; RX_N is unchanged.')
(D/'reports/r101-local-placement.json').write_text(json.dumps(r,indent=2))
note='''

## 2026-09-15: accepted local R101 transmit termination

R101 moved to B.Cu (120.5,64.8), angle 90. Its TX_P branch now uses the existing signal via at (119.497,66.7995) and about 1.59 mm of bottom track instead of about 5.37 mm of front track. ETH_3V3A uses a new 0.6/0.3 mm via at (119.7,63.975), linked to the existing In2 supply track. Via-to-pad bounding-box guard passes at 0.25 mm. DRC zero, unconnected zero; bottom placement visually inspected. Main backup before-r101-local.kicad_pcb; design model synchronized. No footprint library change is needed for a placement-only edit.

Rejected supply via trials at (120.5,62.9) and (121.6,63.975) conflicted with existing ground/RX copper. An additional RX_N top-layer probe still crossed TX_N fanout and ETH_3V3A in three places; that change was removed. See rxn-after-r101-trial-findings.json. This accepted change clears the TX_P termination branch, but does not complete the coordinated MDI reroute. Next address TX_N/R102 and R103 supply corridor together with both pair fanouts.
'''
for name in ['REVE-TRUNK-ROUTING.md','ETHERNET-STACKUP.md']:
 with (E/name).open('a',encoding='utf-8') as out:out.write(note)
f=E/'package_prototype_review.py';s=f.read_text();s=s.replace('Next: coordinate all four Ethernet MDI routes plus R101/R102 placement and supply branches;', 'Next: coordinate Ethernet TX_N/R102 and R103 supply corridor with both pair fanouts. R101 is now accepted locally on B.Cu (120.5,64.8), reducing its TX_P branch from about 5.37 to 1.59 mm; see reports/r101-local-placement.json. RX_N-only front-layer follow-up still had three crossings and was removed;')
f.write_text(s,encoding='utf-8')
print('Accepted R101 placement; model synchronized and via/pad guard passed.')
