from pathlib import Path
import json,hashlib,shutil
D=Path('KiCad-RevE');E=Path('engineering');src=D/'PoE-Speaker-RevE.kicad_pcb'
r=json.loads((D/'reports/rx-coupled-trunk-trial.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['main_before_sha256']
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text());assert not d['violations'] and not d['unconnected_items']
backup=D/'before-rx-coupled-trunk.kicad_pcb';assert not backup.exists();shutil.copy2(src,backup);shutil.copy2(D/'ethernet-trial.kicad_pcb',src)
r.update(status='accepted; full Ethernet impedance qualification remains open',drc_findings=0,unconnected_items=0)
(D/'reports/rx-coupled-trunk.json').write_text(json.dumps(r,indent=2))
note='''

## 2026-09-15: accepted coupled RX trunk

Rebuilt RX_P jack-to-PHY approach on F.Cu, bypassing its former dip through (117.5,71.6622). The former route to that via remains only as the ESD/termination tap. RX_P and RX_N now run parallel at 0.225806 mm width / 0.2032 mm edge gap for x=110.221 through 118.6 (8.379 mm). Pad escapes, via/tap discontinuities, branch lengths and reference continuity remain unqualified. DRC and connectivity are clean. No component/model placement changed. Backup before-rx-coupled-trunk.kicad_pcb. Next inspect RX branch geometry and return reference, then complete TX_P layer and pair coupling.
'''
for name in ['REVE-TRUNK-ROUTING.md','ETHERNET-STACKUP.md']:
 with (E/name).open('a',encoding='utf-8') as out:out.write(note)
f=E/'package_prototype_review.py';s=f.read_text().replace('Next: finish RX pair coupling/spacing and PHY escape, then TX_P layer/coupling and ESD taps.', 'Next: inspect RX ESD/termination branches and reference continuity, then finish TX_P layer/coupling. The RX trunk now has 8.379 mm of parallel routing at the sourced 0.225806 mm width / 0.2032 mm gap and a direct PHY approach; see reports/rx-coupled-trunk.json.');f.write_text(s,encoding='utf-8')
print('Accepted RX coupled trunk.')
