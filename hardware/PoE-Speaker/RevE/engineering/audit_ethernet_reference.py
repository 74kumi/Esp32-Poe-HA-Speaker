"""Sample filled In1 ground under Ethernet copper; not a field solver."""
from pathlib import Path
import pcbnew as p, json, math, hashlib
D=Path('KiCad-RevE'); src=D/'PoE-Speaker-RevE.kicad_pcb'; b=p.LoadBoard(str(src))
zones=[z for z in b.Zones() if z.GetNetname()=='GND' and z.GetLayerSet().Contains(p.In1_Cu)]
rows=[]
tracks=list(b.GetTracks())
for t in tracks:
 if t.GetNetname() not in ['ETH_TX_P','ETH_TX_N','ETH_RX_P','ETH_RX_N'] or isinstance(t,p.PCB_VIA): continue
 a=t.GetStart(); v=t.GetEnd(); length=p.ToMM(t.GetLength()); n=max(1,math.ceil(length/0.1))
 missing=[]
 for i in range(n+1):
  q=p.VECTOR2I(round(a.x+(v.x-a.x)*i/n),round(a.y+(v.y-a.y)*i/n))
  if not any(z.HitTestFilledArea(p.In1_Cu,q) for z in zones): missing.append([round(p.ToMM(q.x),4),round(p.ToMM(q.y),4)])
 rows.append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':b.GetLayerName(t.GetLayer()),'length_mm':round(length,4),'sample_count':n+1,'missing_ground_samples':missing})
report={'pcb_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'method':'Track centerline samples at <=0.1 mm spacing projected onto saved filled In1.Cu GND. Pad antipads can legitimately produce missing samples. This does not check lateral return-current corridors, pair coupling, impedance, or the appropriateness of referencing In1 from B/In2.',
 'segments':rows,'segments_with_missing_samples':sum(bool(x['missing_ground_samples']) for x in rows)}
(D/'reports/ethernet-reference-review.json').write_text(json.dumps(report,indent=2))
print('Ethernet segments with missing projected In1 ground:',report['segments_with_missing_samples'],'of',len(rows))
