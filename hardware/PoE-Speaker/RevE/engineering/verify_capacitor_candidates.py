"""Retrieve manufacturer specification sheets for proposed capacitor order codes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,io
from pypdf import PdfReader
codes=['C0603C104K5RACTU','C0603C224K5RACTU','C0603C105K4RACTU','C0805C106K3PACTU','C0805C475K4RACTU','C0805C226M8PACTU','C1210C476M4PACTU','C1210C226K3RACTU','C1210C105K1RACTU','C1210C106K5RACTU','C0805C225K3RACTU','C0805C155K3RACTU','C0603C332J5GACTU','C0603C222J5GACTU','C0603C223K5RACTU','C0603C682J5GACTU','C0603C103K5RACTU','C0805C104J1GACTU','C0805C104J5GACTU','C0805C105K1RACTU','C0805C105K5RACTU']
out=Path('engineering/sources/prototype-capacitors');out.mkdir(exist_ok=True,parents=True)
def get(code):
 url='https://search.kemet.com/component-documentation/download/specsheet/'+code
 try:
  f=out/(code+'.pdf')
  if not f.exists():
   with urllib.request.urlopen(url,timeout=25) as r:data=r.read()
   assert data.startswith(b'%PDF');f.write_bytes(data)
  text='\n'.join(p.extract_text() or '' for p in PdfReader(str(f)).pages)
  assert code in text
  (out/(code+'.txt')).write_text(text,encoding='utf-8')
  return {'mpn':code,'status':'manufacturer sheet retrieved','url':url,'excerpt':text[:400]}
 except Exception as e:return {'mpn':code,'status':'unverified','error':str(e),'url':url}
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(get,codes))
(out/'verification.json').write_text(json.dumps(rows,indent=2))
for r in rows:print(r['mpn'],r['status'],r.get('excerpt','')[:180].replace('\n',' '))
