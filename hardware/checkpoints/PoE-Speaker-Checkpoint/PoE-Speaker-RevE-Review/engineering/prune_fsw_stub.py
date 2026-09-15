import json,subprocess,pcbnew as p
path='KiCad-RevE/PoE-Speaker-RevE.kicad_pcb';report='KiCad-RevE/reports/board-drc.json'
for attempt in range(20):
 d=json.load(open(report));ids={i['uuid'] for v in d['violations'] if v['type'] in ['track_dangling','via_dangling'] for i in v['items'] if '[5V]' in i['description']}
 if not ids:break
 b=p.LoadBoard(path);tracks=list(b.GetTracks())
 for t in tracks:
  if str(t.m_Uuid.AsString()) in ids:b.Remove(t)
 p.SaveBoard(path,b)
 subprocess.run([r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe','pcb','drc','--format','json','-o',report,path],check=True)
else:raise RuntimeError('Review remaining stubs manually')
