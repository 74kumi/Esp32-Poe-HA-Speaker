import pcbnew as p,json
from pathlib import Path
path=Path('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');b=p.LoadBoard(str(path));tracks=list(b.GetTracks())
for t in tracks:
 if str(t.m_Uuid.AsString())=='c65abb52-8617-44a8-b93d-2de0120003bf':b.Remove(t)
for x,y in [(250.8875,69.9375),(247.6967,82.7842)]:
 v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
for f in b.GetFootprints():
 if f.GetReference()=='U16':f.Reference().SetPosition(p.VECTOR2I(p.FromMM(255.7),p.FromMM(74)))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
