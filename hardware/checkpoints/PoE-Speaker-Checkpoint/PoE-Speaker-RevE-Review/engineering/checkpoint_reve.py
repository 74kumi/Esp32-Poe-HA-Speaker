"""Validate the saved Rev E board, refresh audits/preview and verify archives."""
from pathlib import Path
import subprocess,sys,json
D=Path('KiCad-RevE');cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe';board=str(D/'PoE-Speaker-RevE.kicad_pcb')
def run(args):subprocess.run(args,check=True)
run([cli,'pcb','drc','--format','json','-o',str(D/'reports/board-drc.json'),board])
d=json.loads((D/'reports/board-drc.json').read_text());assert not d['violations'] and not d['unconnected_items'],'Board findings require review before packaging'
for script in ['validate_prototype.py','audit_bootstrap_paths.py','audit_output_paths.py','audit_amplifier_decoupling.py','audit_amplifier_ground.py','audit_amp_ground_plane.py','audit_ethernet_routing.py','audit_ethernet_paths.py','audit_ethernet_reference.py','audit_courtyard_coverage.py','audit_prototype_layout.py']:run([sys.executable,str(Path('engineering')/script)])
run([cli,'pcb','export','svg','--layers','F.Cu,F.Silkscreen,Edge.Cuts','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-o',str(D/'reports/board-top.svg'),board])
run([r'C:\Users\Takumi\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe','-e',"require('C:/Users/Takumi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp')('KiCad-RevE/reports/board-top.svg').resize(1800).png().toFile('KiCad-RevE/reports/board-top.png')"])
run([sys.executable,'engineering/package_prototype_review.py'])
