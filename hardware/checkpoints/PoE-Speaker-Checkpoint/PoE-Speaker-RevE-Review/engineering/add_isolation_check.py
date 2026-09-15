"""Add an explicit preliminary primary/secondary copper clearance review rule.
3 mm is a layout review target, not a claim of compliance or dielectric strength.
"""
from pathlib import Path
import json
D=Path(__file__).resolve().parent.parent/'KiCad-RevB'
primary=['POE_RECT_POS','POE_RECT_NEG','POE_MODE_A_AC1','POE_MODE_A_AC2','POE_MODE_B_AC1','POE_MODE_B_AC2','AT_DET_PRIMARY','BT3_DET_PRIMARY','BT4_DET_PRIMARY','AT_LED_A','BT3_LED_A','BT4_LED_A']
a='('+' || '.join("A.NetName == '"+n+"'" for n in primary)+')'
b=a.replace('A.NetName','B.NetName')
condition="A.NetName != '' && B.NetName != '' && (("+a+' && !'+b+') || ('+b+' && !'+a+'))'
text='(version 1)\n# Preliminary 3 mm review target; not an insulation certification.\n(rule "PoE primary to secondary review target"\n (condition '+json.dumps(condition)+')\n (constraint clearance (min 3mm))\n)\n'
(D/'PoE-Speaker-RevB.kicad_dru').write_text(text)
(D/'reports/isolation-review-target.json').write_text(json.dumps({'target_mm':3,'primary_nets':primary,'status':'Preliminary layout review target only','limitations':'Does not establish creepage, cross-layer dielectric isolation, module underside keepout, chassis clearance, surge survival or compliance.'},indent=2))
