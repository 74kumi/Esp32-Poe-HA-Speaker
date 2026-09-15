"""Package the reviewable first-board draft, excluding tools and rejected trials."""
from pathlib import Path
import collections,json,zipfile,hashlib,pcbnew as p
BASE=Path(__file__).resolve().parent.parent;D=BASE/'KiCad-RevB';R=D/'reports'
design=json.loads((R/'first-board-draft.json').read_text())
b=p.LoadBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'))
design['track_segments']=sum(not isinstance(t,p.PCB_VIA) for t in b.GetTracks())
design['manual_escape']='U5 pin 27: 0.2 mm escape with 0.5/0.3 mm via in pad; assembly process and current capacity remain to be qualified.'
design['vias']=sum(isinstance(t,p.PCB_VIA) for t in b.GetTracks())
if (R/'power-widening.json').exists():
    power=json.loads((R/'power-widening.json').read_text())
    design['power_widening']={'accepted_segments':power['accepted_count'],'segments_requiring_reroute':power['blocked_count']}
    design['limitations'][0]='115 power trunk segments widened; remaining narrow trunks, escapes, vias and return paths are not current/temperature qualified.'
if (R/'isolation-review-target.json').exists():
    design['isolation_target_mm']=3
if (R/'isolation-layout-review.json').exists():
    iso=json.loads((R/'isolation-layout-review.json').read_text())
    design['isolation_clearance_findings']=iso['isolation_clearance_findings']
    design['optocoupler_orientation']=iso['optocouplers']
    design.pop('power_widening',None)
    design['limitations'][0]='Routing uses net-specific power-width targets, but narrow pin escapes, vias and complete return paths remain unqualified. See isolation-layout-review.json for actual widths.'
drc=json.loads((R/'board-drc.json').read_text())
net=json.loads((R/'net-validation.json').read_text())
counts=collections.Counter(v['type'] for v in drc['violations'])
design['kicad_drc']=dict(counts)
design['unconnected_items']=len(drc['unconnected_items'])
design['logical_mapping']=net['logical_mapping']
(R/'first-board-draft.json').write_text(json.dumps(design,indent=2))
lines=['# First board draft — review copy','',
'Open `PoE-Speaker-RevB.kicad_pro` in KiCad 10. **Not for fabrication or power-up.**','',
f"The 160 × 100 mm draft contains {design['footprints']} placed footprints, {design['track_segments']} track segments and {design['vias']} vias. KiCad reports {design['unconnected_items']} unconnected items. The saved schematic and PCB pad assignments match the revised electrical model.",'',
'The body-box placement check passes. This is an initial placement and routing study; it does not validate enclosure fit, circuit operation or manufacturability.','',
'## Current checks','',
'| KiCad finding | Count |','|---|---:|']
lines.extend(f'| {name} | {count} |' for name,count in sorted(counts.items()))
lines.extend(['','## Before a prototype order','',
'- Complete the PoE and bench-input protection changes described in `POWER-REVIEW.md`.',
'- Redesign high-current routes. Net-specific wider trunks still have narrow escapes and unqualified vias and return paths.',
'- Add and review ground planes, isolation boundaries and thermal copper. Check buck and amplifier switching loops.',
'- The explicit 3 mm primary-to-secondary copper review rule now has zero findings. This is a preliminary layout target, not an insulation certification.',
'- Qualify or replace the U5 pin 27 via-in-pad escape for assembly and current capacity.',
'- Route Ethernet pairs to the chosen stackup and impedance requirements.',
'- Complete pin-type/ERC review, silkscreen cleanup and footprint/manufacturing checks. The ESP32 module footprint includes 0.2 mm thermal holes against a current 0.3 mm board constraint; resolve the footprint/process choice.',
'- Verify all release checks, then generate fabrication outputs. No manufacturing Gerbers are included in this review package.','',
'The microphone ring remains a separate future board. The mainboard reserves its eight-microphone interface.',''])
(D/'FIRST-BOARD-DRAFT.md').write_text('\n'.join(lines),encoding='utf-8')
(D/'POWER-REVIEW.md').write_bytes((BASE/'engineering/POWER-REVIEW.md').read_bytes())
files=[f for f in D.iterdir() if f.suffix in ['.kicad_pro','.kicad_sch','.kicad_pcb','.kicad_sym','.kicad_dru','.md'] or f.name in ['fp-lib-table','sym-lib-table']]
files+=list((D/'SpeakerRevB.pretty').glob('*.kicad_mod'))
files+=[R/n for n in ['first-board-draft.json','net-validation.json','board-drc.json','schematic-erc.json','first-board-draft.png','first-board-draft.svg','placement.json'] if (R/n).exists()]
files+=[R/n for n in ['isolation-review-target.json'] if (R/n).exists()]
files+=[R/n for n in ['isolation-layout-review.json','isolation-repair.json','bridge-replacement.json'] if (R/n).exists()]
with zipfile.ZipFile(BASE/'PoE-Speaker-First-Board-Draft.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(f,'PoE-Speaker-First-Board-Draft/'+str(f.relative_to(D)))
print(json.dumps(design,indent=2));print('Packaged',len(files),'files')