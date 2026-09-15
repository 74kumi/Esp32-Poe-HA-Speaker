from pathlib import Path
import pcbnew as p
path=Path('KiCad-RevE/PoE-Speaker-RevE.kicad_pcb');b=p.LoadBoard(str(path));tracks=list(b.GetTracks())
for t in tracks:
 if str(t.m_Uuid.AsString())=='4484e84a-29dd-4419-b453-8e5ce5a08c03':b.Remove(t)
for f in b.GetFootprints():
 if f.GetReference()=='U16':f.Reference().SetPosition(p.VECTOR2I(p.FromMM(252),p.FromMM(80.4)))
 if f.GetReference() in ['C120','C121','C122']:f.SetFPID(p.LIB_ID('SpeakerRevB','C_1210_3225Metric'))
source=Path(r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty\C_1210_3225Metric.kicad_mod')
(path.parent/'SpeakerRevB.pretty'/source.name).write_bytes(source.read_bytes())
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
