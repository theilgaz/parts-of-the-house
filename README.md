# Kolay Ev · Parts of the House

İngilizce derslerindeki "Parts of the House" konusu için ücretsiz, tek sayfalık katlanır kağıt ev.
A3 renkli bastırılır, kesilir, katlanır, yapıştırılır. Mutfak, oturma odası, banyo, yatak odası ve
bahçe hazır; oda adları İngilizce yazılı.

**Site:** https://ev.ilg.az

A free, one-sheet fold-up paper house for the "Parts of the House" English lesson. Print on A3,
cut, fold, glue. The site and the printables are available in Turkish and English.

## İndirilebilir dosyalar

| Dosya | İçerik |
|---|---|
| `docs/downloads/kolay-ev-A3-tr.pdf` | Şablon, A3 (Türkçe yardım yazıları) |
| `docs/downloads/kolay-ev-A4-tr.pdf` | Aynı şablon A4'e küçültülmüş |
| `docs/downloads/talimat-tr.pdf` | Tek sayfa talimat ve video metni (okunuşlarıyla) |
| `docs/downloads/kolay-ev-A3-en.pdf` | Template, A3 (English hints) |
| `docs/downloads/kolay-ev-A4-en.pdf` | Same template scaled to A4 |
| `docs/downloads/instructions-en.pdf` | One-page instructions and video script |

Baskı: A3, renkli, mat kuşe 250-300 gr, ölçek %100. Bitmiş ev yaklaşık 17 × 20 × 9 cm.

## Yapı

```
docs/                 GitHub Pages sitesi (derleme yok, düz HTML/CSS/JS)
  index.html          sayfa (Türkçe metin HTML'de, İngilizce app.js içinde)
  app.js              dil seçimi + three.js ile katlanan 3D model
  style.css
  assets/tex/         3D modelin dokuları (build.py üretir)
  assets/preview-*.png şablon önizlemesi
  downloads/          PDF'ler (build.py üretir)
tools/
  house.py            şablon çizimi (SVG, mm, A3 tuval)
  sheet.py            talimat sayfası
  build.py            PDF'leri ve dokuları üretir
```

## Yeniden üretmek

Şablonda bir şey değişince:

```sh
brew install librsvg        # rsvg-convert (Debian/Ubuntu: apt install librsvg2-bin)
python3 tools/build.py
```

Çıktılar `docs/downloads/` ve `docs/assets/` altına yazılır; ikisi de repoya eklenir ki site
derleme adımı olmadan çalışsın.

Yerelde denemek için (dokular `file://` ile yüklenmez):

```sh
python3 -m http.server -d docs 8000
```

## GitHub Pages

Settings → Pages → Source: *Deploy from a branch*, Branch: `main`, klasör: `/docs`.
Özel alan adı `docs/CNAME` dosyasında (`ev.ilg.az`). DNS'te `ev` → `theilgaz.github.io` CNAME kaydı
gerekir (Cloudflare'de proxy kapalı, yalnızca DNS).

## Katkı

Yeni oda, eşya, dil veya baskı düzeni önerileri için issue ya da PR açabilirsiniz.
Şablon değişikliklerinde `tools/house.py` düzenlenir ve `tools/build.py` çalıştırılır.

## Lisans

- Kod: MIT (`LICENSE`)
- Şablon, PDF'ler ve görseller: CC BY 4.0 (`LICENSE-CONTENT.md`). Serbestçe bastırıp
  dağıtabilirsiniz; kaynağı belirtmeniz yeterli.
