from pathlib import Path
import pcbnew as p,json,hashlib,shutil
D=Path('KiCad-RevE');E=Path('engineering');src=D/'PoE-Speaker-RevE.kicad_pcb'
r=json.loads((D/'reports/txn-fanout-trial.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['main_before_sha256']
d=json.loads((D/'reports/ethernet-trial-drc.json').read_text());assert not d['violations'] and not d['unconnected_items']
b=p.LoadBoard(str(D/'ethernet-trial.kicad_pcb'));q=p.VECTOR2I(p.FromMM(118.725),p.FromMM(74.6))
for f in b.GetFootprints():
 for pad in f.Pads():
  box=pad.GetBoundingBox();box.Inflate(p.FromMM(.25));assert not box.Contains(q),(f.GetReference(),pad.GetNumber())
rx=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname() in ['ETH_RX_N','ETH_RX_P']]
assert not any(t.GetLayer()==p.In2_Cu for t in rx)
backup=D/'before-ethernet-front-corridor.kicad_pcb';assert not backup.exists();shutil.copy2(src,backup);shutil.copy2(D/'ethernet-trial.kicad_pcb',src)
r.update(status='accepted; differential-pair qualification still open',receive_segments_moved_to_front=5,drc_findings=0,unconnected_items=0,new_supply_via_mm=[118.725,74.6],supply_route_width_mm=.3)
(D/'reports/ethernet-front-corridor.json').write_text(json.dumps(r,indent=2))
note='''

## 2026-09-15: accepted Ethernet front routing corridor

Replaced the TX_N jack detour with a shorter F.Cu route at 0.225806 mm width, preserving the R102 tap. Replaced segment length 10.107 mm becomes 8.551 mm. The first proposal crossed J1 unused pad 19; revised geometry goes below that pad and passes DRC. This is not yet a matched transmit pair.

Replaced the required four-track R103 analog-supply path through the receive corridor with 0.3 mm B.Cu routing from R102 power pad (116.3,65.525) via (116.3,74.6) to a new 0.6/0.3 mm supply via at (118.725,74.6), connecting the existing front analog-supply trunk. This longer replacement restores the complete analog supply rather than deleting a required connection. Current/return-loop review remains open. Via-to-component-pad guard passes at 0.25 mm.

With both obstacles cleared, moved all five In2 receive main-route segments to F.Cu at 0.225806 mm width. Both receive nets now use F/B only; bottom ESD/termination branches and their vias remain. Top-layer visual inspection and DRC pass with zero unconnected items. No component or footprint geometry changed, so no model/library placement update is needed. Backup: before-ethernet-front-corridor.kicad_pcb.

Next: improve actual RX coupling and spacing (long parallel sections still have about 0.768 mm center spacing, not the 0.429006 mm target), address RX_P PHY escape detour and termination taps, then TX_P layer/coupling and ESD branch geometry. The former layer-only probe conflicts are resolved by this coordinated change; do not rerun the old probe/acceptance scripts on the new main. Clean DRC does not establish impedance or return continuity.
'''
for name in ['REVE-TRUNK-ROUTING.md','ETHERNET-STACKUP.md']:
 with (E/name).open('a',encoding='utf-8') as out:out.write(note)
f=E/'package_prototype_review.py';s=f.read_text();start=s.index('Next: reroute the TX_N jack fanout');end=s.index('Reroute using the sourced Ethernet100 preset',start)
s=s[:start]+'Next: finish RX pair coupling/spacing and PHY escape, then TX_P layer/coupling and ESD taps. The coordinated TX_N fanout and replacement B.Cu analog-supply path now allow all five receive In2 segments onto F.Cu; accepted with clean DRC and connectivity. See reports/ethernet-front-corridor.json. Existing bottom termination/ESD branches remain. '+s[end:];f.write_text(s,encoding='utf-8')
f=E/'ORDER-RELEASE-REVIEW.md';s=f.read_text();s=s.replace('TX_P uses F/In2, RX_P and RX_N use F/B/In2; six vias across the four signal nets, including branches.', 'TX_P uses F/B/In2, TX_N uses F/B, and RX_P/RX_N now use F/B; seven signal vias remain including branch taps. Five receive main-route segments have moved from In2 to F.Cu after coordinated TX_N and analog-supply rerouting. R101/R102 termination branches are now local; see ethernet-front-corridor.json.').replace('PHY-to-jack screening paths are 10.994/14.374 mm TX and 16.091/13.705 mm RX.', 'Current PHY-to-jack screening paths are regenerated in ethernet-path-review.json; TX_N main route was shortened by about 1.557 mm.')
f.write_text(s,encoding='utf-8')
print('Accepted coordinated front corridor; new supply-via pad guard passed.')
