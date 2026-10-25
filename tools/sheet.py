"""Kolay Ev talimat sayfası (A4, tek sayfa): baskı, yapım, video metni."""

CONTENT = {
    "tr": {
        "title": "Kolay Ev: Parts of the House",
        "sub": "Tek A3 sayfa · kes, katla, yapıştır · yaklaşık 40 dakika",
        "print_h": "1. Çıktı (kitapçı / fotokopici)",
        "print": [
            "Dosya: kolay-ev-A3-tr.pdf  →  A3, RENKLİ, MAT KUŞE 250-300 gr.",
            "Ölçek %100 (Gerçek boyut). A3 yoksa A4 dosyasını basın; ev biraz küçük olur.",
            "Evde gerekenler: makas, stick yapıştırıcı, cetvel, bitmiş bir tükenmez kalem.",
        ],
        "build_h": "2. Yapım",
        "steps": [
            ("Kes: düz çizgilerden kesin. 8 parça çıkar: ev (tek parça), üst kat zemini ve 6 küçük eşya.",),
            ("Çiz: kesik çizgilerin üstünden cetvelle, bitmiş tükenmezle bastırarak geçin. Kuşe böyle çatlamadan katlanır.",),
            ("Katla: bütün kesik çizgileri RESİMLİ YÜZ İÇERİDE kalacak şekilde katlayın.",
             "Yan duvarlar öne gelir, zemin (bahçe dahil) öne yatar. Ev bir kutu köşesi gibi ayakta durur."),
            ("Yapıştır: yan duvarların altındaki gri kulakçıkları içeri kıvırın, zeminin ALTINA yapıştırın.",),
            ("Üst kat: üst kat zemininin 3 gri kulakçığını yukarı kıvırın. Arkalarına yapıştırıcı sürüp",
             "duvardaki beyaz “KULAKÇIK” şeritlerine bastırın. Sol yarısı bedroom, sağ yarısı bathroom."),
            ("Eşyalar: her eşyanın alt kulakçığını arkaya kıvırıp zemine yapıştırın.",
             "Bed ve bathtub üst kata, table mutfağa, sofa oturma odasına, tree ve flowers bahçeye."),
        ],
        "tip": "İpucu: Çocuğunuz eşyaları renklendirebilir, duvarlara kendi resimlerini çizebilir. Zorunlu değil, her şey hazır renkli.",
        "video_h": "3. Video metni (yaklaşık 45 saniye)",
        "pron": True,
        "foot": [
            "“dh” = dilin ucu dişlerin arasındayken söylenen d. Odayı parmağıyla gösterip cümleyi söylesin.",
            "Çekim: gün ışığında, telefon yatay ve sabit, TV kapalı. 2-3 deneme yeter.",
        ],
    },
    "en": {
        "title": "Kolay Ev: Parts of the House",
        "sub": "One A3 sheet · cut, fold, glue · about 40 minutes",
        "print_h": "1. Printing (copy shop or home)",
        "print": [
            "File: kolay-ev-A3-en.pdf  →  A3, COLOUR, MATTE COATED CARD 250-300 gsm.",
            "Scale 100% (Actual size). No A3? Print the A4 file; the house comes out a bit smaller.",
            "You also need: scissors, a glue stick, a ruler and an empty ballpoint pen.",
        ],
        "build_h": "2. Building",
        "steps": [
            ("Cut along the solid lines. You get 8 pieces: the house (one piece), the upstairs floor and 6 small items.",),
            ("Score: run the empty pen along every dashed line with a ruler, so the card folds without cracking.",),
            ("Fold every dashed line with the PRINTED SIDE INSIDE.",
             "The side walls come forward and the floor (with the garden) lies forward. The house stands like a box corner."),
            ("Glue: tuck the grey tabs under the side walls inwards and glue them UNDER the floor.",),
            ("Upstairs: fold the 3 grey tabs of the upstairs floor up. Put glue on their backs and",
             "press them onto the white “TAB” strips on the walls. Left half is the bedroom, right half the bathroom."),
            ("Furniture: fold each item's bottom tab back and glue it to the floor.",
             "Bed and bathtub go upstairs, table in the kitchen, sofa in the living room, tree and flowers in the garden."),
        ],
        "tip": "Tip: everything is already in colour. Children can still colour the furniture or draw pictures on the walls.",
        "video_h": "3. Video script (about 45 seconds)",
        "pron": False,
        "foot": [
            "Point at each room while saying its sentence.",
            "Filming: daylight, phone landscape and steady, TV off. Two or three takes are enough.",
        ],
    },
}

SCRIPT = [
    ("Hello! My name is ___.", "Helıv! May neym iz ___."),
    ("This is my house.", "Dhis iz may haus."),
    ("This is the kitchen. In the kitchen, we eat.", "Dhis iz dhı kiçın. İn dhı kiçın, vi iit."),
    ("This is the living room. In the living room, we watch TV.", "…dhı living ruum… vi voç tii-vii."),
    ("This is the bathroom. In the bathroom, I take a shower.", "…dhı baathruum… ay teyk ı şavır."),
    ("This is the bedroom. In the bedroom, I sleep.", "…dhı bedruum… ay sliip."),
    ("This is the garden. In the garden, I play.", "…dhı gaardın… ay pley."),
    ("I love my house! Thank you!", "Ay lav may haus! Tenk yu!"),
]

FONT = "Helvetica, Arial, sans-serif"


def sheet_svg(lang="tr"):
    C = CONTENT[lang]
    o, y = [], [22.0]

    def t(s, size=10.5, bold=False, color="#222", gap=None, x=18):
        w = "bold" if bold else "normal"
        o.append(f'<text x="{x}" y="{y[0]:.1f}" font-size="{size*0.3528:.2f}" font-family="{FONT}" font-weight="{w}" fill="{color}">{s}</text>')
        y[0] += gap if gap is not None else size * 0.3528 * 1.55

    t(C["title"], 20, True, gap=9)
    t(C["sub"], 10, color="#666", gap=10)
    t(C["print_h"], 12.5, True)
    for s in C["print"]:
        t("•  " + s)
    y[0] += 4
    t(C["build_h"], 12.5, True)
    for n, step in enumerate(C["steps"], 1):
        t(f"{n}) {step[0]}")
        for cont in step[1:]:
            t(cont, x=24)
    y[0] += 2
    t(C["tip"], 9.5, color="#666")
    y[0] += 5
    t(C["video_h"], 12.5, True)
    for en, pron in SCRIPT:
        t(en, 10.5, True, gap=0)
        if C["pron"]:
            o.append(f'<text x="125" y="{y[0]:.1f}" font-size="3.5" font-family="{FONT}" fill="#777">{pron}</text>')
        y[0] += 6.2
    y[0] += 2
    for s in C["foot"]:
        t(s, 9.5, color="#666")
    o.append(f'<text x="192" y="288" font-size="3" font-family="{FONT}" fill="#999" text-anchor="end">theilgaz.github.io/parts-of-the-house  ·  CC BY 4.0</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">'
            '<rect width="210" height="297" fill="#fff"/>' + "".join(o) + "</svg>")
