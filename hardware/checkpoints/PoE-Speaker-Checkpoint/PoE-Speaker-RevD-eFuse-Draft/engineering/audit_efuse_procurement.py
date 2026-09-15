"""Inventory unfinished ordering information without inventing purchasable parts."""
from pathlib import Path
import json,pcbnew as p
D=Path('KiCad-RevD');m=json.loads(Path('engineering/revision-d-design.json').read_text())['components'];b=p.LoadBoard(str(D/'PoE-Speaker-RevD.kicad_pcb'))
footprints={f.GetReference():str(f.GetFPID().GetLibItemName()) for f in b.GetFootprints()};rows=[]
for ref,c in sorted(m.items()):
 props=c.get('properties',{});mpn=str(props.get('Manufacturer Part Number','')).strip()
 if ref.startswith(('TP','H')):status='PCB feature; no assembly purchase assigned'
 elif not mpn or mpn.upper() in ['TBD','N/A','NONE']:status='Missing exact order code'
 elif ref in ['U1','U5','U9','U10']:status='Family/base code; exact suffix or variant requires review'
 else:status='Order code present; ratings/footprint/availability not fully approved'
 rows.append({'reference':ref,'value':c['value'],'mpn':mpn,'footprint':footprints[ref],'status':status})
counts={s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})}
(D/'reports/procurement-audit.json').write_text(json.dumps({'counts':counts,'components':rows,'scope':'Presence and known family-code screening only; not a validated purchasing BOM.'},indent=2))
text='# Procurement readiness audit\n\nNo parts have been ordered. An order code being present does not establish electrical or mechanical suitability.\n\n'
text+='\n'.join('- '+s+': '+str(n) for s,n in counts.items())+'\n\n'
text+='Priority: finalize U1 module variant, U5 amplifier package/order suffix, U9/U10 order suffixes, F1 fuse and protection passives. Check C1-C6 package metadata against their actual radial footprints; older source descriptions may still say SMD.\n\n'
text+='| Reference | Value | Issue |\n|---|---|---|\n'
for r in rows:
 if r['status'].startswith(('Missing','Family')):text+='| '+r['reference']+' | '+r['value'].replace('|','/')+' | '+r['status']+' |\n'
(D/'reports/procurement-audit.md').write_text(text,encoding='utf-8');print(counts)
