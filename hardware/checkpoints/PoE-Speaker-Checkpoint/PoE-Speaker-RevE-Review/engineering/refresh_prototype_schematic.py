"""Regenerate schematic metadata only; keep routed PCB geometry intact."""
from pathlib import Path
import collections,json,math,re,sys,uuid,pcbnew as pcb,hashlib
BASE=Path(__file__).resolve().parent.parent;OUT=BASE/'KiCad-RevE';PROJECT='PoE-Speaker-RevE';ROOT=str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-revb-root'))
model=json.loads((BASE/'engineering/revision-e-design.json').read_text());pcbpath=OUT/(PROJECT+'.kicad_pcb');before=hashlib.sha256(pcbpath.read_bytes()).hexdigest()
b=pcb.LoadBoard(str(pcbpath));fplist={f.GetReference():f for f in b.GetFootprints()};footprint_names={r:str(f.GetFPID().GetLibItemName()) for r,f in fplist.items()};issues=[]
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-revb:'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def natural(s):return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)',s)]
s=(BASE/'engineering/build_revision.py').read_text();s=s[s.index('els={'):s.index('pcb.SaveBoard(',s.index('els={'))]
s=s.replace('REV B - DEVELOPMENT','REV E - DEVELOPMENT').replace('Rev B circuit draft','Rev E circuit draft')
exec(compile(s,'schematic-only','exec'))
s=(BASE/'engineering/fix_efuse_labels.py').read_text().replace("D=Path('KiCad-RevD')","D=OUT")
exec(compile(s,'labels','exec'))
assert hashlib.sha256(pcbpath.read_bytes()).hexdigest()==before
print('Schematic refreshed; routed PCB bytes unchanged')
