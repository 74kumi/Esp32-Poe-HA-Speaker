from pathlib import Path
import pcbnew as p
path=Path('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');b=p.LoadBoard(str(path))
remove={'cf64b13b-52c3-436c-9a82-5c9eca0dec78','3b251f4a-13f5-4dd2-b850-930c38d43bab','27ec4723-523f-43e7-a4b0-4ed40cb1226f'}
tracks=list(b.GetTracks())
for t in tracks:
 if str(t.m_Uuid.AsString()) in remove:
  print(t.GetNetname(),p.ToMM(t.GetStart()),p.ToMM(t.GetEnd()));b.Remove(t)
for f in b.GetFootprints():
 if f.GetReference()=='U16':f.Reference().SetPosition(p.VECTOR2I(p.FromMM(255.7),p.FromMM(73)))
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
