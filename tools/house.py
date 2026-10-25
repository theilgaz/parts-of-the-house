"""Kolay Ev: tek sayfalık katlanır kağıt ev şablonu (SVG, mm cinsinden, A3 tuval).

house_svg(lang, hints, W, H, page_bg) bir SVG metni döndürür.
  lang    : "tr" | "en"  (yalnızca yardım yazıları; oda adları her iki dilde İngilizce)
  hints   : False ise kes/katla/yapıştır yazıları çizilmez (3D dokular için)
  W, H    : baskı boyutu (mm); tuval 297x420 olduğu için A4 verilince orantılı küçülür
"""
import math, random

STRINGS = {
    "tr": {
        "legend": "Düz çizgi = KES   ·   Kesik çizgi = KATLA   ·   Gri alan = YAPIŞTIR",
        "skirt": "ÜST KAT ZEMİNİNİN KULAKÇIĞI BURAYA YAPIŞIR",
        "tab": "KULAKÇIK",
        "under": "altına yapıştır",
        "midtab": "KULAKÇIK: arka duvara",
        "midname": "ÜST KAT ZEMİNİ  (sol: bedroom, sağ: bathroom)",
        "credit": "ev.ilg.az  ·  CC BY 4.0",
    },
    "en": {
        "legend": "Solid line = CUT   ·   Dashed line = FOLD   ·   Grey area = GLUE",
        "skirt": "GLUE THE UPSTAIRS FLOOR TAB HERE",
        "tab": "TAB",
        "under": "glue underneath",
        "midtab": "TAB: glue to back wall",
        "midname": "UPSTAIRS FLOOR  (left: bedroom, right: bathroom)",
        "credit": "ev.ilg.az  ·  CC BY 4.0",
    },
}


def house_svg(lang="tr", hints=True, W=297, H=420, page_bg=True):
    T = STRINGS[lang]
    o=[]
    def a(s): o.append(s)
    CUT='fill="none" stroke="#222" stroke-width="0.45" stroke-linejoin="round"'
    FOLD='stroke="#222" stroke-width="0.4" stroke-dasharray="2.2,1.6" fill="none"'
    FONT='font-family="Helvetica, Arial, sans-serif" font-weight="bold"'
    def rect(x,y,w,h,fill,stroke="none",sw=0.3,rx=0,extra=""):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
    def line(x1,y1,x2,y2,st): a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {st}/>')
    def circ(x,y,r,fill,stroke="none",sw=0.3): a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def poly(pts,fill,stroke="none",sw=0.3): a(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def path(d,fill,stroke="none",sw=0.3): a(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(x,y,s,size=4,fill="#333",anchor="middle",w="bold"):
        a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="Helvetica, Arial, sans-serif" font-weight="{w}">{s}</text>')
    def hint(*args, **kw):
        if hints: text(*args, **kw)
    def label(x,y,s):
        w=len(s)*2.55+6
        rect(x,y,w,6.5,"#fff","#555",0.3,3.2); text(x+w/2,y+4.7,s,3.8,"#333")
    def tab(pts): poly(pts,"#f4f1ea")
    INK="#3b3b3b"
    # palette
    LAV="#E8DDF6"; BLU="#D3ECF6"; YEL="#FFF0C2"; PEA="#FADCCB"; ROOF="#D9604C"; ROOFD="#B84A39"; GRASS="#9BD27A"; GRASSD="#7FBF5E"; WOOD="#E3B07E"; WOODD="#C98E59"; SKIRT="#FFFFFF"
    L0,L1,R0,R1=13.5,63.5,233.5,283.5; YT,YM,YB=65,137,209; YF,YG=259,299; AX=148.5; AY=12
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 297 420">')
    if page_bg: rect(0,0,297,420,"#fff")
    # ---------- back wall ----------
    rect(L1,YT,85,72,LAV); rect(AX,YT,85,72,BLU); rect(L1,YM,85,72,YEL); rect(AX,YM,85,72,PEA)
    # bathroom tiles
    for i in range(9):
        for j in range(4):
            rect(AX+1+i*9.4,YT+40+j*8,9,7.6,"#BFE2F0","#fff",0.4)
    # skirting (upstairs strip where floor tabs go)
    rect(L1,YM-10,170,10,SKIRT); line(L1,YM-10,R0,YM-10,'stroke="#ccc" stroke-width="0.3"')
    line(AX,YT,AX,YB,'stroke="#fff" stroke-width="0.8"'); line(L1,YM,R0,YM,'stroke="#999" stroke-width="0.5"')
    hint(AX,YM-4.2,T["skirt"],2.6,"#aaa",w="normal")
    # bedroom: window with curtains, picture, shelf
    rect(74,78,26,22,"#BDE3FA","#fff",1.2); line(87,78,87,100,'stroke="#fff" stroke-width="1"'); line(74,89,100,89,'stroke="#fff" stroke-width="1"')
    circ(80,84,2.6,"#FFE27A")
    path("M70,76 h8 q-3,13 0,26 h-8 z","#F4A6C0"); path("M104,76 h-8 q3,13 0,26 h8 z","#F4A6C0"); rect(68,75,38,2,"#B7859A",rx=1)
    rect(113,80,16,13,"#fff","#C98E59",1); path("M115,91 l4,-6 l3,4 l2,-2 l3,4 z","#8CC97A"); circ(125,84,1.3,"#F9C74F")
    rect(110,107,32,1.6,WOODD)
    for k,(c,h) in enumerate([("#E76F51",9),("#2A9D8F",8),("#E9C46A",10),("#6D597A",7),("#F4A261",9)]): rect(112+k*3.2,107-h,2.8,h,c)
    circ(135,103.5,3.5,"#8CC97A"); rect(132.5,104,5,3,"#C98E59")
    label(L1+3,YT+3,"BEDROOM")
    # bathroom: shower, mirror, sink, towel
    rect(AX+6,YT+12,1.5,22,"#9AA5AE"); path(f"M{AX+4},{YT+12} h10 l-2,4 h-6 z","#9AA5AE")
    for k in range(5): line(AX+6+k*1.4,YT+17,AX+5+k*2,YT+24,'stroke="#7FC8F8" stroke-width="0.6"')
    a(f'<ellipse cx="{AX+60}" cy="{YT+20}" rx="9" ry="11" fill="#E9F6FB" stroke="#9AA5AE" stroke-width="1.2"/>')
    path(f"M{AX+48},{YT+38} h24 q0,9 -12,9 q-12,0 -12,-9 z","#fff","#9AA5AE",0.6); rect(AX+58,YT+47,4,15,"#fff","#9AA5AE",0.6)
    rect(AX+59,YT+34,1.2,4,"#9AA5AE")
    rect(AX+74,YT+30,1.2,14,"#9AA5AE"); rect(AX+75.5,YT+30,6,16,"#F28FAD")
    label(AX+3,YT+3,"BATHROOM")
    # kitchen: cabinets, window, counter+stove, fridge
    for k in range(3): rect(L1+4+k*14,YM+12,13,14,"#9FD8CB","#fff",0.6); circ(L1+4+k*14+10.5,YM+23,0.7,"#555")
    rect(L1+50,YM+12,22,17,"#BDE3FA","#fff",1.2); line(L1+61,YM+12,L1+61,YM+29,'stroke="#fff" stroke-width="1"')
    rect(L1+2,YM+44,58,4,"#8D99AE")
    for k in range(4): rect(L1+3+k*14.3,YM+48,13.3,24,"#9FD8CB","#fff",0.6); rect(L1+3+k*14.3+5.5,YM+51,2.5,0.8,"#555")
    for cx in (L1+12,L1+22): a(f'<ellipse cx="{cx}" cy="{YM+44}" rx="3.6" ry="1.2" fill="#333"/>')
    path(f"M{L1+30},{YM+44} v-5 h8 v5 z","#E76F51"); rect(L1+29,YM+38.5,10,1,"#C4553D")
    rect(L1+63,YM+30,19,42,"#F1F3F5","#9AA5AE",0.6); line(L1+63,YM+45,L1+82,YM+45,'stroke="#9AA5AE" stroke-width="0.6"')
    rect(L1+66,YM+36,1,6,"#9AA5AE"); rect(L1+66,YM+48,1,8,"#9AA5AE")
    label(L1+3,YM+3,"KITCHEN")
    # living room: picture, tv, cabinet, lamp, plant
    rect(AX+30,YM+22,32,20,"#2B2D42","#555",0.6); rect(AX+31.5,YM+23.5,29,17,"#4CC9F0"); path(f"M{AX+42},{YM+27} l7,4.5 l-7,4.5 z","#fff")
    rect(AX+24,YM+56,44,16,WOOD,WOODD,0.5); line(AX+46,YM+56,AX+46,YM+72,f'stroke="{WOODD}" stroke-width="0.5"')
    rect(AX+44,YM+42,4,14,"#555"); circ(AX+42,YM+64,0.8,"#555"); circ(AX+50,YM+64,0.8,"#555")
    rect(AX+6,YM+14,14,11,"#fff","#C98E59",1); circ(AX+13,YM+19.5,3,"#F4A261")
    rect(AX+73,YM+34,1.2,38,"#555"); path(f"M{AX+68},{YM+34} h11 l-2,-8 h-7 z","#F9C74F")
    rect(AX+6,YM+62,9,10,"#C98E59"); circ(AX+10.5,YM+57,6,"#6BBF59")
    label(AX+3,YM+3,"LIVING ROOM")
    # ---------- gable ----------
    poly([(L1,YT),(AX,AY),(R0,YT)],ROOF)
    for r in range(6):
        yy=YT-6-r*8.5; half=85*(yy-AY)/(YT-AY)
        line(AX-half,yy,AX+half,yy,f'stroke="{ROOFD}" stroke-width="0.5"')
    circ(AX,YT-30,7,"#BDE3FA","#fff",1.3); line(AX-7,YT-30,AX+7,YT-30,'stroke="#fff" stroke-width="0.9"'); line(AX,YT-37,AX,YT-23,'stroke="#fff" stroke-width="0.9"')
    text(AX,YT-11,"MY HOUSE",7,"#fff")
    # ---------- side walls ----------
    for x0,up,down,flip in ((L0,LAV,YEL,False),(R0,BLU,PEA,True)):
        rect(x0,YT,50,72,up); rect(x0,YM,50,72,down); rect(x0,YM-10,50,10,SKIRT)
        line(x0,YM,x0+50,YM,'stroke="#999" stroke-width="0.5"')
        rect(x0+14,YT+16,22,20,"#BDE3FA","#fff",1.2); line(x0+25,YT+16,x0+25,YT+36,'stroke="#fff" stroke-width="1"')
        rect(x0+14,YM+16,22,20,"#BDE3FA","#fff",1.2); line(x0+14,YM+26,x0+36,YM+26,'stroke="#fff" stroke-width="1"')
        hint(x0+25,YM-4.2,T["tab"],2.6,"#aaa",w="normal")
    # ---------- ground floor + garden ----------
    for i in range(9):
        for j in range(5):
            rect(L1+i*85/9,YB+j*10,85/9,10,"#fff" if (i+j)%2 else "#F2C6B4")
    for k in range(5): rect(AX,YB+k*10,85,10,WOOD if k%2 else "#E8BC8E"); line(AX,YB+k*10,R0,YB+k*10,f'stroke="{WOODD}" stroke-width="0.3"')
    a(f'<ellipse cx="{AX+42}" cy="{YB+28}" rx="28" ry="13" fill="#90BEDE"/>'); a(f'<ellipse cx="{AX+42}" cy="{YB+28}" rx="22" ry="9" fill="none" stroke="#fff" stroke-width="0.6" stroke-dasharray="1.5,1.2"/>')
    rect(L1,YF,170,40,GRASS)
    path(f"M{AX-9},{YF} h18 l6,40 h-30 z","#E9DCC5")
    for (x,y) in [(AX-5,YF+6),(AX+2,YF+15),(AX-6,YF+24),(AX+3,YF+33)]: a(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.5" fill="#CBB89B"/>')
    random.seed(4)
    for _ in range(26):
        x=random.uniform(L1+4,R0-4); y=random.uniform(YF+4,YG-4)
        if abs(x-AX)<20: continue
        c=random.choice(["#F94144","#F9C74F","#F8F9FA","#F3722C","#B5179E"])
        for ang in range(0,360,72):
            circ(x+1.2*math.cos(math.radians(ang)),y+1.2*math.sin(math.radians(ang)),1,c)
        circ(x,y,0.8,"#FFD166")
    label(L1+3,YF+3,"GARDEN")
    # ---------- tabs on side walls ----------
    tab([(L0,YB),(L0+5,YB+10),(L1-5,YB+10),(L1,YB)]); tab([(R0,YB),(R0+5,YB+10),(R1-5,YB+10),(R1,YB)])
    hint(L0+25,YB+6.5,T["under"],2.6,"#999",w="normal"); hint(R0+25,YB+6.5,T["under"],2.6,"#999",w="normal")
    # ---------- house cut + fold ----------
    a(f'<path d="M{AX},{AY} L{R0},{YT} L{R1},{YT} L{R1},{YB} L{R1-5},{YB+10} L{R0+5},{YB+10} L{R0},{YB} L{R0},{YG} L{L1},{YG} L{L1},{YB} L{L1-5},{YB+10} L{L0+5},{YB+10} L{L0},{YB} L{L0},{YT} L{L1},{YT} Z" {CUT}/>')
    for (x1,y1,x2,y2) in [(L1,YT,L1,YB),(R0,YT,R0,YB),(L1,YB,R0,YB),(L0,YB,L1,YB),(R0,YB,R1,YB)]: line(x1,y1,x2,y2,FOLD)
    # ---------- middle floor (loose) ----------
    MX,MY,MW,MD=25,320,168,49
    rect(MX,MY,MW/2,MD,WOOD)
    for k in range(5): line(MX,MY+k*MD/5,MX+MW/2,MY+k*MD/5,f'stroke="{WOODD}" stroke-width="0.3"')
    a(f'<ellipse cx="{MX+MW/4}" cy="{MY+30}" rx="22" ry="10" fill="#F4A6C0"/>')
    for i in range(9):
        for j in range(5): rect(MX+MW/2+i*MW/18,MY+j*MD/5,MW/18,MD/5,"#fff" if (i+j)%2 else "#BFE2F0")
    a(f'<ellipse cx="{MX+MW*0.75}" cy="{MY+32}" rx="12" ry="6" fill="#F28FAD"/>')
    tab([(MX+5,MY),(MX+9,MY-10),(MX+MW-9,MY-10),(MX+MW-5,MY)])
    tab([(MX,MY+4),(MX-10,MY+8),(MX-10,MY+MD-4),(MX,MY+MD)])
    tab([(MX+MW,MY+4),(MX+MW+10,MY+8),(MX+MW+10,MY+MD-4),(MX+MW,MY+MD)])
    hint(MX+MW/2,MY-3.6,T["midtab"],2.6,"#999",w="normal")
    a(f'<path d="M{MX},{MY} L{MX+5},{MY} L{MX+9},{MY-10} L{MX+MW-9},{MY-10} L{MX+MW-5},{MY} L{MX+MW},{MY} L{MX+MW},{MY+4} L{MX+MW+10},{MY+8} L{MX+MW+10},{MY+MD-4} L{MX+MW},{MY+MD} L{MX},{MY+MD} L{MX-10},{MY+MD-4} L{MX-10},{MY+8} L{MX},{MY+4} Z" {CUT}/>')
    for (x1,y1,x2,y2) in [(MX,MY,MX+MW,MY),(MX,MY,MX,MY+MD),(MX+MW,MY,MX+MW,MY+MD)]: line(x1,y1,x2,y2,FOLD)
    hint(MX+MW/2,MY+MD+5,T["midname"],3,"#666")
    # ---------- standees ----------
    def standee(x,y,w,h,draw,name,b0=0,b1=None):
        # x,y = top-left of item; tab under item's base (b0..b1)
        b1=w if b1 is None else b1
        tab([(x+b0,y+h),(x+b0+2.5,y+h+7),(x+b1-2.5,y+h+7),(x+b1,y+h)])
        a(f'<path d="M{x+b0},{y+h} L{x+b0+2.5},{y+h+7} L{x+b1-2.5},{y+h+7} L{x+b1},{y+h}" {CUT}/>')
        draw(x,y)
        line(x+b0,y+h,x+b1,y+h,FOLD)
        text(x+w/2,y+h+11,name,2.8,"#666")
    def bed(x,y):
        rect(x,y,50,26,"#fff"); rect(x+2,y,46,14,"#9C6644",rx=3); rect(x,y+12,50,10,"#F4A6C0"); rect(x+6,y+8,15,6,"#fff",rx=2.5); rect(x+29,y+8,15,6,"#fff",rx=2.5)
        rect(x+1,y+22,3,4,"#7F5539"); rect(x+46,y+22,3,4,"#7F5539")
        a(f'<path d="M{x+2},{y} h46 v12 h2 v14 h-50 v-14 h2 z" {CUT}/>')
    def sofa(x,y):
        rect(x+4,y,44,13,"#2A9D8F",rx=3); rect(x,y+8,9,14,"#21867A",rx=2.5); rect(x+43,y+8,9,14,"#21867A",rx=2.5); rect(x+7,y+12,38,8,"#34B3A3",rx=1.5)
        rect(x+12,y+3,10,7,"#F9C74F",rx=2); rect(x+3,y+22,3,3,"#555"); rect(x+46,y+22,3,3,"#555"); rect(x+0,y+21.5,52,0.01,"none")
        a(f'<path d="M{x+4},{y} h44 v8 h4 v17 h-52 v-17 h4 z" {CUT}/>')
    def table(x,y):
        rect(x+12,y,16,10,YEL); rect(x,y+10,40,3,WOODD); rect(x+3,y+13,2.5,11,WOODD); rect(x+34.5,y+13,2.5,11,WOODD)
        a(f'<ellipse cx="{x+20}" cy="{y+8}" rx="8" ry="3" fill="#fff" stroke="#bbb" stroke-width="0.3"/>'); circ(x+17,y+6,2.2,"#E63946"); circ(x+22,y+5.5,2.2,"#F9C74F"); circ(x+20,y+3.6,2,"#80B918")
        a(f'<path d="M{x},{y+10} h12 v-10 h16 v10 h12 v3 h-3 v11 h-34 v-11 h-3 z" {CUT}/>')
        # filler between legs so cut is easy
        rect(x+5.5,y+13,29,11,YEL)
    def tub(x,y):
        rect(x,y,46,24,"#E3F4FB"); path(f"M{x},{y+8} h46 v4 q0,10 -10,10 h-26 q-10,0 -10,-10 z","#fff","#9AA5AE",0.5)
        for (cx,cy,r) in [(x+10,y+6,3),(x+16,y+5,3.6),(x+23,y+6,3),(x+30,y+5,3.4),(x+36,y+6,2.8)]: circ(cx,cy,r,"#E3F4FB","#BFE2F0",0.3)
        rect(x+4,y+21,3,3,"#C9A227"); rect(x+39,y+21,3,3,"#C9A227")
        a(f'<path d="M{x},{y} h46 v24 h-46 z" {CUT}/>')
    def tree(x,y):
        rect(x,y+56,34,4,"#7FBF5E"); rect(x+14,y+34,6,22,"#8D5B3E"); circ(x+17,y+18,17,GRASSD); circ(x+10,y+14,2,"#E63946"); circ(x+24,y+20,2,"#E63946"); circ(x+15,y+26,2,"#E63946")
        a(f'<path d="M{x},{y+60} V{y+56} H{x+14} V{y+34.73} A17,17 0 1,1 {x+20},{y+34.73} V{y+56} H{x+34} V{y+60} Z" {CUT}/>')
    def bush(x,y):
        bp=f"M{x},{y+18} V{y+11} Q{x},{y+1} {x+12},{y+1} Q{x+24},{y+1} {x+24},{y+11} V{y+18} Z"
        path(bp,"#6BBF59"); circ(x+7,y+11,4,"#5AAE4A"); circ(x+16,y+9,4.5,"#5AAE4A"); circ(x+8,y+7,1.3,"#F94144"); circ(x+15,y+5,1.3,"#F9C74F"); circ(x+18,y+11,1.3,"#F94144")
        a(f'<path d="{bp}" {CUT}/>')
    standee(14,382,50,26,bed,"BED (bedroom)")
    standee(72,382,52,25,sofa,"SOFA (living room)")
    standee(134,384,40,24,table,"TABLE (kitchen)",3,37)
    standee(214,312,46,24,tub,"BATHTUB (bathroom)")
    standee(212,348,34,60,tree,"TREE (garden)")
    standee(256,390,24,18,bush,"FLOWERS")
    # legend
    hint(10,6.5,T["legend"],3.2,"#555","start","normal")
    if hints: text(287,6.5,T['credit'],2.6,'#999','end','normal')
    a('</svg>')
    return "\n".join(o)
