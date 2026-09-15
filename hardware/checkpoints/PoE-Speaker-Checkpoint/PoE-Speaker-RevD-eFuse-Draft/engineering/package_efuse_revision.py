"""Save an honest, reproducible Revision D development checkpoint."""
from pathlib import Path
import pcbnew as p,json,collections,zipfile
D=Path('KiCad-RevD');E=Path('engineering');d=json.loads((D/'reports/board-drc.json').read_text());b=p.LoadBoard(str(D/'PoE-Speaker-RevD.kicad_pcb'))
counts=dict(collections.Counter(v['type'] for v in d['violations']))
erc=json.loads((D/'reports/schematic-erc.json').read_text())
report={'revision':'D shared eFuse development draft','components':len(list(b.GetFootprints())),'board_mm':[210,100],'track_segments':sum(not isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'vias':sum(isinstance(t,p.PCB_VIA) for t in b.GetTracks()),'ground_zones':len(list(b.Zones())),'unconnected_items':len(d['unconnected_items']),'drc':counts,'erc_findings':sum(len(s['violations']) for s in erc['sheets']),'poe_isolation_findings':sum('PoE primary' in v['description'] for v in d['violations']),'fabrication_ready':False}
(D/'reports/revision-status.json').write_text(json.dumps(report,indent=2))
readme='''# Revision D — shared current protection draft

Open PoE-Speaker-RevD.kicad_pro in KiCad 10. This editable development board is not approved for fabrication or power-up. Revisions B and C remain preserved.

Added TPS26630RGER after the bench/PoE ideal-diode junction, feeding all original 24V_AMP loads. The circuit targets a nominal 2.98 A current limit, latch-off behavior, controlled startup and power-good amplifier shutdown interlock. TP26 is the shutdown/reset point; TP27 exposes the fault output. See engineering/EFUSE-REVIEW.md for calculations and limitations. Eight microphones remain assigned to a future separate ring board.

The 210 x 100 mm provisional outline is unchanged from C. Retained routes were reused except the two nets split by this change. The secondary In1.Cu ground plane now extends under Ethernet while excluding the lower-left primary/module region. See reports/secondary-ground.png. The routing preview omits that plane so signal routing is visible.

Validation: all 616 connected model pins match both the schematic netlist and PCB pad nets. Specific checks confirm the eFuse supply split and amplifier interlock. Exact physical and electrical findings are below; an empty ratsnest does not establish electrical correctness. Most imported symbols still use boxed pin representations, and source electrical pin types need further review.

Release blockers: resolve remaining DRC and ERC findings; qualify high-current widths/vias and thermal copper; finish Ethernet impedance and return paths, switching loops, input transient/fuse coordination, hot-start and overload behavior, and exact passive order codes. U15 now uses the manufacturer-recommended 1.22 x 0.40 mm lands at 0.65 mm pitch. All narrow-track escapes have been repaired without relaxing rules. The 21 thermal vias are covered by a scoped 0.20 mm drill-process rule; see engineering/FABRICATION-PROCESS.md. DRC is clean under that documented profile, but assembly via treatment and final stackup require confirmation. The enclosure, mounting and final speaker are not fixed. No manufacturing release is included.

Do not rerun build_efuse_revision.py on this routed folder without first archiving it: generation recreates placement and removes later routing work.

## Saved validation counts

'''+ '\n'.join('- '+str(k)+': '+str(v) for k,v in report.items())+'\n'
(D/'README.md').write_text(readme,encoding='utf-8')
(E/'RESUME-HERE.md').write_text('# Resume checkpoint\n\nLatest: KiCad-RevD/PoE-Speaker-RevD.kicad_pro and PoE-Speaker-RevD-eFuse-Draft.zip. Shared eFuse/current-limit circuit and amplifier interlock are integrated. See KiCad-RevD/README.md and reports/revision-status.json for actual routing and rule-check status. B and C remain preserved.\n\nNext: DRC is clean with the scoped thermal-via rule and Ethernet ground extension. Review the five ERC power-source findings, U7 FSW selection, high-current/thermal layout, startup/transients, and 127 missing order codes (reports/procurement-audit.json). Read engineering/EFUSE-REVIEW.md. Do not regenerate over saved routing.\n',encoding='utf-8')
archive=Path('PoE-Speaker-RevD-eFuse-Draft.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in D.rglob('*'):
  if f.is_file() and ('reports' not in f.parts or f.suffix in ['.json','.png','.svg','.xml','.md']):z.write(f,str(f))
 for f in E.glob('*'):
  if f.is_file() and (f.name in ['revision-d-design.json','EFUSE-REVIEW.md','RESUME-HERE.md','FABRICATION-PROCESS.md','SECONDARY-RAIL-REVIEW.md'] or 'efuse' in f.name or f.name=='refine_revd_land_pattern.py'):z.write(f,str(f))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
with zipfile.ZipFile('PoE-Speaker-Checkpoint.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [Path('PoE-Speaker-First-Board-Draft.zip'),Path('PoE-Speaker-RevC-Integrated-Draft.zip'),archive]:
  if f.exists():z.write(f,str(f))
 for f in E.glob('*'):
  if f.is_file() and f.suffix in ['.py','.json','.md']:z.write(f,str(f))
with zipfile.ZipFile('PoE-Speaker-Checkpoint.zip') as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('Draft and checkpoint archives verified')
