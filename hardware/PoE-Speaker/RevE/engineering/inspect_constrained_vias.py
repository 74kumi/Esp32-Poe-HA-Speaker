import pcbnew as p,json
b=p.LoadBoard('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');c=b.GetConnectivity();out=[]
ids=['280e574d-c161-4143-b892-0b2586aa0d65','b1f97f19-06f9-4a93-ad55-9ca5424f212e','b983fee9-a187-486f-966c-0b0f0547dc19']
for v in b.GetTracks():
 if v.m_Uuid.AsString() not in ids:continue
 row={'via':v.m_Uuid.AsString(),'tracks':[]}
 for t in c.GetConnectedTracks(v):
  if isinstance(t,p.PCB_VIA):continue
  row['tracks'].append({'uuid':t.m_Uuid.AsString(),'layer':b.GetLayerName(t.GetLayer()),'start':p.ToMM(t.GetStart()),'end':p.ToMM(t.GetEnd()),'width':p.ToMM(t.GetWidth())})
 out.append(row)
print(json.dumps(out,indent=2))
