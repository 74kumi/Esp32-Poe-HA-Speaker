from pathlib import Path
import re,json,shutil,pcbnew as p
D=Path('KiCad-RevB'); refs={f'D{i}' for i in range(3,11)}
props={'Manufacturer Part Number':'B5100C','Manufacturer Name':'Diodes Incorporated','Datasheet URL':'https://www.diodes.com/datasheet/download/B5100C.pdf','Reverse Voltage':'100','Forward Voltage':'0.85 V max at 5 A','Package or Case Code':'SMC (DO-214AB)','LCSC Part Number':'','JLCPCB Part Class':'','Role Details':'PoE bridge: 100 V draft replacement; thermal and transient qualification pending'}
model=Path('engineering/design_revision.py');s=model.read_text()
marker='# Consolidate sheets by circuit function; retain the finer functional group as metadata.'
block="\n# PoE bridge voltage-margin revision; retain recovered SMC geometry and pin numbering.\nfor ref in [f'D{i}' for i in range(3,11)]:\n    components[ref]['value']='B5100C'\n    components[ref]['properties'].update("+repr(props)+")\nchanges.append({'change':'Replace 60 V SS56 bridges with 100 V B5100C; thermal/transient qualification pending','references':[f'D{i}' for i in range(3,11)]})\n\n"
if '# PoE bridge voltage-margin revision' not in s:model.write_text(s.replace(marker,block+marker))
# Patch only actual schematic instances, preserving their graphics and every connection.
q=lambda x:json.dumps(x,ensure_ascii=False)
f=D/'07_PoE_input_and_isolation.kicad_sch';raw=f.read_text();shutil.copy2(f,D/'reports/before-bridge-replacement.kicad_sch')
spans=[]
for m in re.finditer(r'\(symbol\s+\(lib_id\s+"SpeakerRevB:(D[3-9]|D10)"',raw):
 depth=0;quoted=False;esc=False
 for i in range(m.start(),len(raw)):
  c=raw[i]
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:spans.append((m.start(),i+1));break
assert len(spans)==8,len(spans)
for a,z in reversed(spans):
 t=raw[a:z]
 for k,v in dict(props,Value='B5100C').items():
  t=re.sub(r'(\(property\s+'+re.escape(q(k))+r'\s+)"(?:\\.|[^"\\])*"',lambda m:m[1]+q(v),t)
 raw=raw[:a]+t+raw[z:]
f.write_text(raw)
# Embedded library default values and standalone library values.
for f in [D/'07_PoE_input_and_isolation.kicad_sch',D/'SpeakerRevB.kicad_sym']:
 f.write_text(f.read_text().replace('"SS56"','"B5100C"'))
path=D/'PoE-Speaker-RevB.kicad_pcb';shutil.copy2(path,D/'reports/before-bridge-replacement.kicad_pcb');b=p.LoadBoard(str(path))
for f in b.GetFootprints():
 if f.GetReference() in refs:
  f.SetValue('B5100C')
  # Procurement properties live in the schematic and design model.
  for pad in f.Pads():assert tuple(pad.GetSize())==(2160000,3240000)
p.SaveBoard(str(path),b)
for ref in refs:
 f=D/'SpeakerRevB.pretty'/f'{ref}_RevB.kicad_mod';f.write_text(f.read_text().replace('"SS56"','"B5100C"'))
print('Updated 8 bridge diodes; preserved all copper and pad geometry.')

