"""Bütün çıktıları üretir: PDF'ler (docs/downloads) ve 3D dokuları (docs/assets/tex).

Kullanım:  python3 tools/build.py
Gerekenler: Python 3.9+, rsvg-convert (macOS: brew install librsvg, Debian: apt install librsvg2-bin)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from house import house_svg  # noqa: E402
from sheet import sheet_svg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(ROOT, "docs", "downloads")
TEX = os.path.join(ROOT, "docs", "assets", "tex")
PX_PER_MM = 6

# 3D modelde kullanılan parçalar: (x, y, genişlik, yükseklik) mm, A3 tuvalinde
CROPS = {
    "back": (63.5, 12, 170, 197), "left": (13.5, 65, 50, 144), "right": (233.5, 65, 50, 144),
    "floor": (63.5, 209, 170, 90), "mid": (25, 320, 168, 49),
    "bed": (14, 382, 50, 26), "sofa": (72, 382, 52, 25), "table": (134, 384, 40, 24),
    "tub": (214, 312, 46, 24), "tree": (212, 348, 34, 60), "bush": (256, 390, 24, 18),
}


def rsvg(svg_text, out, fmt):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg_text)
    try:
        subprocess.run(["rsvg-convert", "-f", fmt, f.name, "-o", out], check=True)
    finally:
        os.unlink(f.name)


def main():
    if not shutil.which("rsvg-convert"):
        sys.exit("rsvg-convert bulunamadı (brew install librsvg)")
    os.makedirs(DL, exist_ok=True)
    os.makedirs(TEX, exist_ok=True)

    for lang in ("tr", "en"):
        rsvg(house_svg(lang), os.path.join(DL, f"kolay-ev-A3-{lang}.pdf"), "pdf")
        rsvg(house_svg(lang, W=210, H=297), os.path.join(DL, f"kolay-ev-A4-{lang}.pdf"), "pdf")
        rsvg(sheet_svg(lang), os.path.join(DL, f"talimat-{lang}.pdf" if lang == "tr" else "instructions-en.pdf"), "pdf")
        rsvg(house_svg(lang), os.path.join(ROOT, "docs", "assets", f"preview-{lang}.png"), "png")

    body = re.search(r"<svg[^>]*>(.*)</svg>", house_svg(hints=False, page_bg=False), re.S).group(1)
    for name, (x, y, w, h) in CROPS.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*PX_PER_MM}" height="{h*PX_PER_MM}" '
               f'viewBox="{x} {y} {w} {h}">{body}</svg>')
        rsvg(svg, os.path.join(TEX, f"{name}.png"), "png")

    for f in sorted(os.listdir(DL)):
        print(f"docs/downloads/{f}  {os.path.getsize(os.path.join(DL, f)) // 1024} KB")
    print(f"docs/assets/tex/  {len(CROPS)} doku")


if __name__ == "__main__":
    main()
