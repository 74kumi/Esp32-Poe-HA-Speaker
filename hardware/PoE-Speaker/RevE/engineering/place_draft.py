"""Create a collision-free first placement and local-router input from Rev B.
Does not alter the recovered board or schematic connectivity.
"""
import pcbnew as p,json,math
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
D=BASE/'KiCad-RevB';b=p.LoadBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'))
m=json.loads((BASE/'engineering/revision-b-design.json').read_text(encoding='utf-8'))['components']
V=lambda x,y:p.VECTOR2I(round(x*1e6),round(y*1e6))
fps={f.GetReference():f for f in b.GetFootprints()}
preferred={'U3':(125,69),'U2':(150,70),'U12':(116,91),'U13':(116,99),'U14':(116,107),
 'C1':(190,130),'C2':(190,142),'C3':(207,143),'C4':(207,132),'C5':(199,108),'C6':(199,123),
 'L1':(216,98),'L2':(216,121),'U5':(208,111),'J3':(225,111),'J2':(225,135)}
fixed=['H1','H2','H3','H4','U1','J1','J4','J5','J6','J2','J3','U2','U3','U4','U5','U6','U7','U8','U9','U10','U11','U12','U13','U14']
occupied=[];placements={}
def box(f):
    bb=f.GetBoundingBox(False,False)
    return [bb.GetX()/1e6-.25,bb.GetY()/1e6-.25,bb.GetRight()/1e6+.25,bb.GetBottom()/1e6+.25]
def collide(a,z):return a[0]<z[2] and a[2]>z[0] and a[1]<z[3] and a[3]>z[1]
def allowed(f,bb):
    if bb[0]<71 or bb[1]<51 or bb[2]>229 or bb[3]>149:return False
    return not any(collide(bb,z) for _,z in occupied)
for f in fps.values():
    if f.IsFlipped():f.Flip(f.GetPosition(),False)
    # Embedded source text duplicates reference fields and causes stale markings.
    for g in list(f.GraphicalItems()):
        pass # Preserve embedded text until individual silkscreen cleanup
    f.Reference().SetVisible(True);f.Value().SetVisible(False)
order=fixed+sorted((r for r in fps if r not in fixed),key=lambda r:-(box(fps[r])[2]-box(fps[r])[0])*(box(fps[r])[3]-box(fps[r])[1]))
for ref in order:
    f=fps[ref];orig=(f.GetPosition().x/1e6,f.GetPosition().y/1e6)
    target=preferred.get(ref,orig)
    primary=any(pin['net'] and (pin['net'].startswith('POE_RECT') or pin['net'].startswith('POE_MODE') or pin['net'].endswith('_LED_A') and ref in ['R3','R4','R5']) for pin in m[ref]['pins'])
    if primary and ref not in ['U1','J1','U12','U13','U14']:target=(98,100+(int(''.join(filter(str.isdigit,ref)))%8)*4)
    if ref.startswith(('R10','C10','C11')) and m[ref]['group']=='Ethernet':target=(target[0]+8,target[1]+7)
    candidates=[(target[0]+dx*.5,target[1]+dy*.5) for dx in range(-70,71) for dy in range(-70,71)]
    candidates.sort(key=lambda xy:(xy[0]-target[0])**2+(xy[1]-target[1])**2)
    found=False
    for x,y in candidates:
        f.SetPosition(V(x,y));bb=box(f)
        if ref.startswith('H') or ref=='U1':found=True;break
        if primary and ref not in ['U1','J1','U12','U13','U14'] and bb[2]>109:continue
        if allowed(f,bb):found=True;break
    if not found:raise RuntimeError('No legal placement '+ref)
    occupied.append((ref,bb));placements[ref]={'original':orig,'draft':[x,y]}
    f.Reference().SetPosition(V((bb[0]+bb[2])/2,bb[1]-.7));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
    f.Reference().SetTextSize(V(.7,.7));f.Reference().SetTextThickness(p.FromMM(.1))
    # Courtyard/body boxes are intentionally conservative for this first pass.
for a in occupied:
    for z in occupied:
        if a[0]<z[0] and collide(a[1],z[1]):raise RuntimeError(('Overlap',a,z))
note=p.PCB_TEXT(b);note.SetText('REV B / FIRST BOARD DRAFT / NOT FOR FABRICATION');note.SetPosition(V(150,46));note.SetTextSize(V(1.3,1.3));note.SetLayer(p.Cmts_User);b.Add(note)
p.SaveBoard(str(D/'PoE-Speaker-RevB.kicad_pcb'),b)
(D/'reports/placement.json').write_text(json.dumps(placements,indent=2))
assert p.ExportSpecctraDSN(b,str(D/'reports/draft.dsn'))
print('Placed',len(fps),'footprints; no expanded body-box overlaps. Exported draft.dsn')



