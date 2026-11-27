#!/usr/bin/env python3
"""One-off: draw the favicon set and the social sharing card into ./static.

Run again only if the name, photo or colours change.
Requires: pillow, fonttools, brotli.
"""
import io
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "static" / "fonts"
NAVY = (8, 50, 121)  # primary, navy #083279
INK = (0, 0, 0)
MUTED = (85, 85, 85)


def static_ttf(woff2, **axes):
    f = TTFont(FONTS / woff2)
    f = instancer.instantiateVariableFont(f, axes)
    f.flavor = None
    buf = io.BytesIO()
    f.save(buf)
    buf.seek(0)
    return buf, f


def favicon():
    _, font = static_ttf("literata-latin-standard-normal.woff2", wght=600, opsz=72)
    gs = font.getGlyphSet()
    glyph = font.getBestCmap()[ord("R")]
    upm = font["head"].unitsPerEm
    adv = font["hmtx"][glyph][0]
    pen = SVGPathPen(gs)
    size, scale = 64, 46 / upm
    tx = (size - adv * scale) / 2
    ty = 47
    tpen = TransformPen(pen, (scale, 0, 0, -scale, tx, ty))
    gs[glyph].draw(tpen)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
           f'<rect width="{size}" height="{size}" rx="10" fill="#{NAVY[0]:02x}{NAVY[1]:02x}{NAVY[2]:02x}"/>'
           f'<path fill="#ffffff" d="{pen.getCommands()}"/></svg>\n')
    (ROOT / "static" / "favicon.svg").write_text(svg)

    buf, _ = static_ttf("literata-latin-standard-normal.woff2", wght=600, opsz=72)
    for px, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        big = px * 4
        im = Image.new("RGB", (big, big), NAVY)
        d = ImageDraw.Draw(im)
        buf.seek(0)
        f = ImageFont.truetype(buf, int(big * 0.72))
        bbox = d.textbbox((0, 0), "R", font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((big - w) / 2 - bbox[0], (big - h) / 2 - bbox[1]), "R", font=f, fill="white")
        im.resize((px, px), Image.LANCZOS).save(ROOT / "static" / name)


def og_card():
    serif, _ = static_ttf("literata-latin-standard-normal.woff2", wght=500, opsz=72)
    sans, _ = static_ttf("schibsted-grotesk-latin-wght-normal.woff2", wght=450)
    card = Image.open(ROOT / "tools" / "og-card-base.png").convert("RGB")
    d = ImageDraw.Draw(card)
    name_font = ImageFont.truetype(serif, 92)
    d.text((72, 150), "Reza", font=name_font, fill=NAVY)
    serif.seek(0)
    d.text((72, 245), "Alibakhshi", font=ImageFont.truetype(serif, 92), fill=NAVY)
    s1 = ImageFont.truetype(sans, 30)
    d.text((76, 390), "Assistant Professor of Information Systems", font=s1, fill=INK)
    sans.seek(0)
    d.text((76, 432), "IE Business School, Madrid", font=ImageFont.truetype(sans, 30), fill=MUTED)
    d.rectangle((76, 520, 76 + 64, 523), fill=(100, 145, 222))
    card.save(ROOT / "static" / "img" / "og-card.png", optimize=True)


if __name__ == "__main__":
    favicon()
    og_card()
    print("Images written to static/")
