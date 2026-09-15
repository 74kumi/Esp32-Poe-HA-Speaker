"""Trial widening direct U5 ground pin tracks, preserving routes and vias."""
from pathlib import Path
import pcbnew as p,json
D=Path('KiCad-RevE');b=p.LoadBoard(str(D/'PoE-Speaker-RevE.kicad_pcb'));f=next(f for f in b.GetFootprints() if f.GetReference()=='U5');c=b.GetConnectivity();ts=list(b.GetTracks());lookup={t.m_Uuid.AsString():t for t in ts};ids=set()
for pad in f.Pads():
 if pad.GetNetname()=='GND':ids.update(x.m_Uuid.AsString() for x in c.GetConnectedTracks(pad))
rows=[]
for uid in sorted(ids):
 t=lookup[uid]
 if isinstance(t,p.PCB_VIA) or t.GetNetname()!='GND' or p.ToMM(t.GetWidth())>=.4:continue
 rows.append({'uuid':uid,'old_width_mm':p.ToMM(t.GetWidth()),'new_width_mm':.4});t.SetWidth(p.FromMM(.4))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'power-trial.kicad_pcb'),b);(D/'reports/amp-ground-pin-widths.json').write_text(json.dumps({'changes':rows,'status':'trial'},indent=2));print('Widened',len(rows))
