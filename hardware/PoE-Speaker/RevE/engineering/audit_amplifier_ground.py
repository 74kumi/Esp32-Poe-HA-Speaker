"""Inventory amplifier capacitor ground access; not a return-current or impedance solver."""
from pathlib import Path
import pcbnew as p,json,math
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));c=b.GetConnectivity();fs={f.GetReference():f for f in b.GetFootprints()};ts=list(b.GetTracks());vias=[t for t in ts if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND'];rows=[]
for ref in ['C5','C6','C11','C12','C13','C14','C15']:
 pad=next(x for x in fs[ref].Pads() if x.GetNetname()=='GND');pos=pad.GetPosition();seen=set();pending=[pad];connected=[];tracks=[]
 while pending:
  x=pending.pop();uid=x.m_Uuid.AsString()
  if uid in seen:continue
  seen.add(uid)
  if isinstance(x,p.PCB_VIA):connected.append(x);continue
  if isinstance(x,p.PCB_TRACK):tracks.append(x)
  lookup={t.m_Uuid.AsString():t for t in ts}; pending.extend(lookup[y.m_Uuid.AsString()] for y in c.GetConnectedTracks(x) if y.GetNetname()=='GND' and y.m_Uuid.AsString() not in seen and y.m_Uuid.AsString() in lookup)
 def dist(v):return math.hypot(p.ToMM(v.GetPosition().x-pos.x),p.ToMM(v.GetPosition().y-pos.y))
 def describe(v):return {'uuid':v.m_Uuid.AsString(),'position_mm':p.ToMM(v.GetPosition()),'drill_mm':p.ToMM(v.GetDrillValue()),'straight_line_distance_mm':round(dist(v),3)}
 rows.append({'capacitor':ref,'ground_pad':pad.GetNumber(),'through_hole_pad':pad.GetAttribute()==p.PAD_ATTRIB_PTH,'pad_drill_mm':p.ToMM(pad.GetDrillSize()),'position_mm':p.ToMM(pos),'side':b.GetLayerName(fs[ref].GetLayer()),'direct_copper_access_vias': [describe(v) for v in sorted(connected,key=dist)],'nearest_ground_via_geometric_only':describe(min(vias,key=dist)),'ground_track_segments':[{'uuid':t.m_Uuid.AsString(),'width_mm':p.ToMM(t.GetWidth()),'length_mm':round(p.ToMM(t.GetLength()),3),'layer':b.GetLayerName(t.GetLayer())} for t in tracks]})
report={'method':'Follow connected ground tracks from each capacitor pad, stopping at vias. Zone and pad-mediated paths are not traversed. Plated through-hole pads may access the plane directly; a separate via is not required merely because this inventory reports a distant via. Distances are straight-line geometry, not return-loop length. Nearest via alone does not establish electrical access. No impedance, plane continuity, current sharing or thermal qualification.','capacitors':rows,'zones':[{'net':z.GetNetname(),'layer':b.GetLayerName(z.GetLayer())} for z in b.Zones()]};(D/'reports/amplifier-ground-access.json').write_text(json.dumps(report,indent=2));print([(r['capacitor'],r['through_hole_pad'],len(r['direct_copper_access_vias'])) for r in rows])

