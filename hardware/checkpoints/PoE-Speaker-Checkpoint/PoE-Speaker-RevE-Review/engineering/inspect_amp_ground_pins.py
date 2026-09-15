import pcbnew as p,json
b=p.LoadBoard('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');f=next(f for f in b.GetFootprints() if f.GetReference()=='U5');c=b.GetConnectivity();ts=list(b.GetTracks());lookup={t.m_Uuid.AsString():t for t in ts};rows=[]
for pad in f.Pads():
 if pad.GetNetname()!='GND':continue
 row={'pin':pad.GetNumber(),'position':p.ToMM(pad.GetPosition()),'connections':[]}
 for obj in c.GetConnectedTracks(pad):
  t=lookup[obj.m_Uuid.AsString()]
  if isinstance(t,p.PCB_VIA):row['connections'].append({'kind':'via','uuid':t.m_Uuid.AsString(),'pos':p.ToMM(t.GetPosition()),'drill':p.ToMM(t.GetDrillValue())})
  else:row['connections'].append({'kind':'track','uuid':t.m_Uuid.AsString(),'start':p.ToMM(t.GetStart()),'end':p.ToMM(t.GetEnd()),'width':p.ToMM(t.GetWidth()),'layer':b.GetLayerName(t.GetLayer())})
 rows.append(row)
print(json.dumps(rows,indent=2))
