"""Explicit ERC source annotations after passive power-path elements."""
from pathlib import Path
import json,uuid
D=Path('KiCad-RevE');path=D/'PoE-Speaker-RevE.kicad_sch';s=path.read_text();root=str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-revb-root'))
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'speaker-reve-power:'+v))
def q(v):return json.dumps(v)
def effects(hide=False):return '(effects (font (size 1.27 1.27))'+(' (hide yes)' if hide else '')+')'
def prop(name,value,x,y,hide=False):return f'(property {q(name)} {q(value)} (at {x} {y} 0) {effects(hide)})'
lid='SpeakerRevB:ReviewedPowerSource'
definition=f'(symbol {q(lid)} (power) (pin_names (offset 0)) (in_bom no) (on_board no) '+prop('Reference','#FLG',0,0,True)+prop('Value','PWR_FLAG',0,3.81)+ '(symbol "ReviewedPowerSource_0_1" (polyline (pts (xy 0 0) (xy -1.27 1.27) (xy 0 2.54) (xy 1.27 1.27) (xy 0 0)) (stroke (width 0) (type default)) (fill (type none)))) (symbol "ReviewedPowerSource_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))'
assert '(lib_symbols)' in s,'Run refresh_prototype_schematic.py first'
s=s.replace('(lib_symbols)','(lib_symbols '+definition+')')
sources={
 'BENCH_FUSED':'J2 external DC input through F1; source presence annotation only, not fuse qualification',
 'GND':'Secondary common return from J2 and isolated module output; never primary POE_RECT_NEG',
 '3V3':'U7 switch output through L4; VOS is a sense input, not an output pin',
 'ETH_3V3A':'3V3 through FB2; ferrite does not propagate ERC power drive',
 '24V_OR':'Q1/Q2 drains fed by protected bench and isolated PoE paths; U9/U10 OUT pins are sense inputs',
 '5V':'U6 switch output through L3; inductor does not propagate ERC power drive'}
items=''
for i,(net,reason) in enumerate(sources.items(),1):
 x=30.48+(i-1)%3*175.26;y=248.92+(i-1)//3*30.48;ref=f'#FLG0{i:02d}'
 items+=f'(symbol (lib_id {q(lid)}) (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid {uid(net)})'+prop('Reference',ref,x,y,True)+prop('Value','PWR_FLAG',x,y-5)+f'(instances (project "PoE-Speaker-RevE" (path "/{root}" (reference {q(ref)}) (unit 1)))))'
 items+=f'(global_label {q(net)} (shape passive) (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid(net+"label")}))'
items+=f'(text "ERC source declarations: see reports/power-source-review.json" (at 15 234 0) (effects (font (size 1.5 1.5)) (justify left)) (uuid {uid("note")}))'
path.write_text(s.rstrip()[:-1]+items+')',encoding='utf-8')
lib=D/'SpeakerRevB.kicad_sym';t=lib.read_text();lib.write_text(t.rstrip()[:-1]+definition.replace(q(lid),'"ReviewedPowerSource"',1)+')',encoding='utf-8')
(D/'reports/power-source-review.json').write_text(json.dumps({'source_annotations':sources,'limitations':'Flags declare verified topology across passive elements. They do not prove startup, regulation, protection or PCB current capacity. Imported pin types outside reviewed regulators remain incomplete.'},indent=2))
print('Annotated',len(sources),'power paths')
