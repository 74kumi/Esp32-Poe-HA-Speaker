"""Produce a clean constrained routing input after a stalled incremental attempt."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parent.parent/'KiCad-RevB/reports'
s=(R/'isolation.dsn').read_text()
def endscope(start):
 d=0
 for i in range(start,len(s)):
  if s[i]=='(':d+=1
  elif s[i]==')':
   d-=1
   if d==0:return i+1
 raise ValueError('unbalanced')
start=s.index('(wiring');end=endscope(start);s=s[:start]+'(wiring)'+s[end:]
primary=set(json.loads((R/'isolation-review-target.json').read_text())['primary_nets'])
expected=json.loads((R/'expected-nets.json').read_text());allnets=set(expected)
power={'24V_AMP','24V_POE','24V_BENCH_RAW','24V_BENCH_PROTECTED','POE_12V_MID','5V','3V3'}
speaker={'SPK_POS','SPK_NEG','AMP_SW_POS','AMP_SW_NEG'}
classes={'PoEPrimary':(primary,600),'Secondary':(allnets-primary-power-speaker,200),'Power':(power,600),'Speaker':(speaker,1000)}
start=s.index('(class PoEPrimary');pair=s.index('(class_class',start);end=endscope(pair)
text=''
for name,(nets,width) in classes.items():
 text+='(class '+name+' '+' '.join(json.dumps(n) for n in sorted(nets))+' (circuit (use_via "Via[0-3]_600:300_um")) (rule (width '+str(width)+') (clearance 200)))\n'
for secondary in ['Secondary','Power','Speaker']:text+='(class_class (classes PoEPrimary '+secondary+') (rule (clearance 3000)))\n'
s=s[:start]+text+s[end:];(R/'isolation-clean.dsn').write_text(s)
print('Prepared clean input with power widths and 3 mm isolation class pairs')
