#!/usr/bin/env python3
"""Draw the social preview card for The Countertop Guide.

Deterministic on purpose: same data in, same bytes out, so a rebuild never changes the
image hash or the feed. Brand art only - no product photography, no Amazon imagery and
no generated food shots (the policy read sits in flagged.html FLG-021 and FLG-030).
The one graphic is our own depth diagram, drawn from the dimensions the listings state.

Run:  python3 scripts/make_og.py   ->  assets/og-image.png
"""
import json, hashlib, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "products.json")))
SITE, PRODS = D["site"], {p["id"]: p for p in D["products"]}
INK, PAPER, CLAY, GOLD, TEAL, MUTED = "#171310", "#FBF7F0", "#B24320", "#E5B85C", "#7FBFB5", "#9E9382"
W, H, M = 1200, 630, 70
RIGHT = W - M
FONTS = {"serif": "DejaVuSerif-Bold.ttf", "serifr": "DejaVuSerif.ttf", "sans": "DejaVuSans.ttf", "sansb": "DejaVuSans-Bold.ttf"}


def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{FONTS[name]}", size)


def fit(d, text, name, size, max_w):
    """Shrink until the line fits inside max_w - no clipped headlines, ever."""
    while size > 10 and d.textlength(text, font=font(name, size)) > max_w:
        size -= 1
    return size, d.textlength(text, font=font(name, size))


def spaced(d, xy, text, f, fill, tracking=3):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking


def depth_of(pid):
    import re
    m = re.findall(r'([0-9.]+)"', PRODS[pid]["dimensions"])
    return float(m[0]) if m else None


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # tri-colour rule: the same signature the stylesheet uses
    d.rectangle([0, 0, int(W * .34), 12], fill=CLAY)
    d.rectangle([int(W * .34), 0, int(W * .67), 12], fill=TEAL)
    d.rectangle([int(W * .67), 0, W, 12], fill=GOLD)

    spaced(d, (M, 50), "SPEC-BACKED BUYING GUIDES", font("sansb", 20), GOLD, 4)
    chip = "SPONSORED LINKS, LABELLED"
    cw = d.textlength(chip, font=font("sansb", 17)) + 34
    d.rounded_rectangle([RIGHT - cw, 44, RIGHT, 78], 17, outline=GOLD, width=2)
    d.text((RIGHT - cw + 17, 52), chip, font=font("sansb", 17), fill=GOLD)

    s1, _ = fit(d, "The Countertop Guide", "serif", 74, RIGHT - M)
    d.text((M, 100), "The Countertop Guide", font=font("serif", s1), fill=PAPER)

    # Every block below records its true bottom edge and the next block starts under it.
    # An earlier version hard-coded a y for the diagram label that overlapped the
    # subtitle; this version cannot overlap because it measures instead of guessing.
    y = 196
    for line in ["Five machines. Every number", "read from its own Amazon listing."]:
        s, wdt = fit(d, line, "serifr", 42, RIGHT - M)
        d.text((M, y), line, font=font("serifr", s), fill=PAPER)
        y += s + 12
    L1 = "Capacity, counter depth and cleanup - with the gap in each listing named."
    L2 = "No stale prices: no page quotes one, the Amazon button is the price. No fake testing."
    s, _ = fit(d, L1, "sans", 22, RIGHT - M)
    sub = font("sans", s)
    d.text((M, y + 10), L1, font=sub, fill=MUTED)
    d.text((M, y + 10 + s + 8), L2, font=sub, fill=MUTED)
    sub_bottom = y + 10 + s + 8 + s

    # our own diagram, from the dimensions the listings state
    label_s, label_f, label_gap = 16, font("sansb", 16), 18
    label_y = sub_bottom + label_gap + 2
    y0, scale, bw, gap = 528, 6.4, 236, 26
    GLYPH_TOP = 26  # a bar tall enough to hold its own 34px figure: ~26px of glyph stack
    bars = []
    for pid in ("P3", "P1", "P2"):
        v = depth_of(pid)
        if v:
            nm = PRODS[pid]["shortName"]
            nm = nm.replace(PRODS[pid]["brand"], "").strip() or PRODS[pid]["shortName"]
            bars.append((PRODS[pid]["brand"] + " " + nm, v))
    # a bar shorter than GLYPH_TOP would put its own figure above the bar, so the
    # diagram is only drawn when the space is there; the guard is explicit, not hope.
    assert label_y + 16 + 8 + GLYPH_TOP < y0 - 20, "og-image: no room for the depth diagram"
    d.text((M, label_y), "COUNTER DEPTH AS THE LISTINGS STATE IT - OUR DIAGRAM", font=label_f, fill=MUTED)
    x = M
    for name, depth in bars:
        hgt = int(depth * scale)
        d.rectangle([x, y0 - hgt, x + bw, y0], fill="#302619")
        d.rectangle([x, y0 - hgt, x + bw, y0 - hgt + 2], fill=GOLD)
        d.rectangle([x, y0 - hgt, x + 6, y0], fill=CLAY)
        d.text((x + 18, y0 - hgt + 12), f'{depth}"', font=font("serif", 34), fill=PAPER)
        d.text((x + 18, y0 - hgt + 54), f"{round(depth * 2.54, 1)} cm", font=font("sans", 19), fill=MUTED)
        ns, _ = fit(d, name, "sansb", 19, bw - 30)
        # the caption sits under the baseline and must clear the footer band
        assert y0 + 12 + 19 <= H - 56 - 8, "og-image: bar captions run into the footer band"
        d.text((x + 18, y0 + 12), name, font=font("sansb", ns), fill=PAPER)
        x += bw + gap
    d.line([M, y0, x - gap, y0], fill="#3B2F24", width=2)

    d.rectangle([0, H - 56, W, H], fill="#100D0B")
    d.text((M, H - 40), "As an Amazon Associate I earn from qualifying purchases.", font=font("sans", 20), fill="#F6E7C4")
    d.text((RIGHT - d.textlength(f"Listing data checked {SITE['verifiedDate']}", font=font("sans", 18)), H - 38),
           f"Listing data checked {SITE['verifiedDate']}", font=font("sans", 18), fill=MUTED)

    out = os.path.join(ROOT, "assets", "og-image.png")
    img.save(out, "PNG", optimize=True)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
           f'aria-label="The Countertop Guide"><rect width="64" height="64" rx="13" fill="{INK}"/>'
           f'<rect x="9" y="40" width="10" height="14" fill="{CLAY}"/><rect x="23" y="29" width="10" height="25" fill="{TEAL}"/>'
           f'<rect x="37" y="17" width="10" height="37" fill="{GOLD}"/><rect x="9" y="14" width="10" height="7" rx="2" fill="{PAPER}"/></svg>')
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(svg + "\n")
    print("og-image.png", os.path.getsize(out), "bytes | sha256", hashlib.sha256(open(out, "rb").read()).hexdigest()[:16])


main()
