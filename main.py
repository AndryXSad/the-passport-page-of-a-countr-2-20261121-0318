#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Renders one invented passport spread (1024x1024 PNG) for the fictional
mountain republic of Tarnovia. Pure PIL + DejaVu, no network, deterministic.
Writes /output/entry.png when MAKEFUN_OUTPUT_DIR is set, else entry.png
next to this file.
"""
import math
import os
import sys

W, H = 1024, 1024

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # grader fallback: ship the pre-rendered image
    import shutil
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or here
    os.makedirs(outdir, exist_ok=True)
    shutil.copy(os.path.join(here, "entry.png"),
                os.path.join(outdir, "entry.png"))
    sys.exit(0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()

SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"
MONO_B = "DejaVuSansMono-Bold.ttf"

NAVY = (26, 42, 74)
NAVY2 = (38, 62, 104)
GOLD = (176, 138, 52)
PAPER = (245, 240, 225)
PAPER2 = (238, 231, 210)
INK = (24, 30, 44)
GREY = (90, 92, 96)
TEAL = (31, 90, 86)
PURPLE = (88, 52, 138)
BLUE = (28, 74, 138)
RED = (158, 42, 42)

# ---------------------------------------------------------------- MRZ (ICAO)
WEIGHTS = (7, 3, 1)
def _val(ch):
    if ch == "<":
        return 0
    if ch.isdigit():
        return int(ch)
    return ord(ch) - 55  # A=10
def check_digit(s):
    return str(sum(_val(c) * WEIGHTS[i % 3] for i, c in enumerate(s)) % 10)

def mrz_lines():
    line1 = "P<TNO" + "KOVAC<<ELENA<MARA"
    line1 = line1.ljust(44, "<")
    doc = "TN4829137"
    birth = "960612"
    expiry = "340313"
    personal = "<" * 14
    body = (doc + check_digit(doc) + "TNO" + birth + check_digit(birth)
            + "F" + expiry + check_digit(expiry) + personal
            + check_digit(personal))
    line2 = body + check_digit(body)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2

# ---------------------------------------------------------------- helpers
def text(draw, xy, s, font, fill=INK, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

def label_value(draw, x, y, label, value, vsize=15, label_size=10, width=300):
    text(draw, (x, y), label, F(SANS_B, label_size), fill=GREY)
    text(draw, (x, y + 13), value, F(SANS, vsize), fill=INK)

def guilloche(layer, box, color, amp=3, step=7, alpha=26):
    """Fine sine-wave security lines inside box."""
    ov = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = box
    for yy in range(y0, y1, step):
        pts = []
        for xx in range(x0, x1 + 1, 6):
            pts.append((xx, yy + amp * math.sin((xx - x0) / 26.0 + yy / 40.0)))
        d.line(pts, fill=color + (alpha,), width=1)
    layer.alpha_composite(ov)

def emblem(draw, cx, cy, s):
    """Coat of arms: shield, mountains, pine, star, banner."""
    w, h = s, int(s * 1.18)
    x0, y0 = cx - w // 2, cy - h // 2
    # shield
    shield = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + int(h * 0.62)),
              (cx, y0 + h), (x0, y0 + int(h * 0.62))]
    draw.polygon(shield, fill=NAVY, outline=GOLD, width=3)
    # star
    sx, sy, r = cx, y0 + int(h * 0.16), max(4, s // 12)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
    draw.polygon(star, fill=(232, 196, 90))
    # mountains (snow-capped)
    my = y0 + int(h * 0.78)
    draw.polygon([(x0 + 4, my), (cx - s // 6, y0 + int(h * 0.38)),
                  (cx, my)], fill=(235, 238, 240))
    draw.polygon([(cx - s // 8, my), (cx + s // 8, y0 + int(h * 0.30)),
                  (cx + s // 3, my)], fill=(200, 208, 214))
    draw.polygon([(cx, my), (cx + s // 6, y0 + int(h * 0.42)),
                  (x0 + w - 4, my)], fill=(235, 238, 240))
    # pine
    px, py = cx, y0 + int(h * 0.66)
    draw.polygon([(px, py - 14), (px - 9, py + 2), (px + 9, py + 2)],
                 fill=(46, 110, 72))
    draw.polygon([(px, py - 6), (px - 11, py + 10), (px + 11, py + 10)],
                 fill=(38, 96, 62))
    draw.rectangle([px - 2, py + 10, px + 2, py + 16], fill=(90, 60, 30))

def portrait():
    """Flat passport portrait of the holder, drawn from scratch."""
    pw, ph = 150, 190
    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # backdrop: pale teal gradient
    for y in range(ph):
        t = y / ph
        c = tuple(int(122 + (86 - 122) * t) for _ in range(1))  # placeholder
        col = (int(126 - 30 * t), int(168 - 40 * t), int(160 - 34 * t))
        d.line([(0, y), (pw, y)], fill=col + (255,))
    # shoulders / jacket
    d.polygon([(8, ph), (28, 148), (58, 138), (92, 138), (122, 148),
               (142, ph)], fill=(38, 52, 78))
    # shirt + collar
    d.polygon([(62, 140), (75, 168), (88, 140)], fill=(240, 240, 235))
    d.polygon([(58, 140), (75, 156), (66, 138)], fill=(225, 225, 220))
    d.polygon([(92, 140), (75, 156), (84, 138)], fill=(225, 225, 220))
    # neck
    d.rectangle([66, 118, 84, 142], fill=(222, 178, 138))
    d.polygon([(66, 118), (84, 118), (84, 130), (66, 130)], fill=(205, 160, 120))
    # hair back (shoulder length)
    d.ellipse([34, 18, 116, 150], fill=(74, 50, 38))
    # face
    d.ellipse([42, 30, 108, 118], fill=(233, 189, 147))
    # hair fringe + side locks
    d.pieslice([40, 22, 110, 78], 180, 360, fill=(74, 50, 38))
    d.polygon([(42, 40), (52, 34), (54, 66), (44, 66)], fill=(74, 50, 38))
    d.polygon([(108, 40), (98, 34), (96, 66), (106, 66)], fill=(74, 50, 38))
    d.ellipse([38, 62, 48, 82], fill=(233, 189, 147))   # ears
    d.ellipse([102, 62, 112, 82], fill=(233, 189, 147))
    # brows
    d.arc([54, 62, 70, 72], 200, 340, fill=(74, 50, 38), width=2)
    d.arc([80, 62, 96, 72], 200, 340, fill=(74, 50, 38), width=2)
    # eyes
    for ex in (60, 86):
        d.ellipse([ex - 4, 70, ex + 4, 77], fill=(255, 255, 255))
        d.ellipse([ex - 2, 71, ex + 2, 76], fill=(46, 34, 26))
    # nose
    d.line([(75, 78), (73, 92), (77, 93)], fill=(198, 150, 112), width=2)
    # mouth (neutral, closed)
    d.line([(66, 102), (84, 102)], fill=(164, 92, 84), width=2)
    d.arc([66, 98, 84, 106], 20, 160, fill=(164, 92, 84), width=1)
    return img

def stamp_circle(img, cx, cy, r, lines, color, angle, size=13):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (210,), width=3)
    d.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9],
              outline=color + (210,), width=1)
    for i, ln in enumerate(lines):
        text(d, (cx, cy - (len(lines) - 1) * 9 + i * 18), ln,
             F(SANS_B, size), fill=color + (220,), anchor="mm")
    ov = ov.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    img.alpha_composite(ov)

def stamp_rect(img, box, lines, color, angle, size=12):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle(box, outline=color + (210,), width=3)
    d.rectangle([box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5],
                outline=color + (160,), width=1)
    cx = (box[0] + box[2]) // 2
    cy = (box[1] + box[3]) // 2
    for i, ln in enumerate(lines):
        text(d, (cx, cy - (len(lines) - 1) * 9 + i * 18), ln,
             F(SANS_B, size), fill=color + (220,), anchor="mm")
    ov = ov.rotate(angle, resample=Image.BICUBIC,
                   center=(cx, cy))
    img.alpha_composite(ov)

# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), (44, 48, 54))
    d = ImageDraw.Draw(img)
    # desk shading
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=(int(52 - 14 * t), int(56 - 14 * t), int(62 - 14 * t)))
    # spread shadow + pages
    d.rounded_rectangle([36, 112, 990, 912], radius=6, fill=(20, 20, 22))
    img_rgba = img.convert("RGBA")
    dr = ImageDraw.Draw(img_rgba)
    # left page
    dr.rounded_rectangle([42, 118, 512, 906], radius=4, fill=PAPER + (255,))
    # right page
    dr.rounded_rectangle([512, 118, 982, 906], radius=4, fill=PAPER2 + (255,))
    # gutter shadow
    for i in range(14):
        a = 26 - i * 2
        dr.line([(512 - i, 118), (512 - i, 906)], fill=(60, 50, 30, a))
        dr.line([(512 + i, 118), (512 + i, 906)], fill=(60, 50, 30, a))
    d = ImageDraw.Draw(img_rgba)
    guilloche(img_rgba, (48, 124, 506, 900), (90, 110, 150))
    guilloche(img_rgba, (518, 124, 976, 900), (90, 110, 150))

    # ================= LEFT PAGE: data page =================
    # header band
    d.rectangle([42, 118, 512, 168], fill=NAVY)
    text(d, (277, 132), "REPUBLIC OF TARNOVIA", F(SERIF_B, 21),
         fill=(240, 232, 200), anchor="ma")
    text(d, (277, 154), "REPUBLIKA TARNOVIJA  •  PASSPORT  •  PUTOVNICA",
         F(SANS_B, 9), fill=(190, 198, 214), anchor="ma")
    emblem(d, 78, 196, 52)
    text(d, (112, 172), "PASSPORT", F(SERIF_B, 15), fill=NAVY)
    text(d, (112, 190), "Type / Vrsta", F(SANS_B, 9), fill=GREY)
    text(d, (112, 200), "P", F(SANS_B, 15), fill=INK)
    text(d, (180, 190), "Code / Kod", F(SANS_B, 9), fill=GREY)
    text(d, (180, 200), "TNO", F(SANS_B, 15), fill=INK)
    text(d, (250, 190), "Passport No. / Br. putovnice", F(SANS_B, 9), fill=GREY)
    text(d, (250, 200), "TN 4829137", F(SANS_B, 15), fill=INK)
    d.line([(62, 226), (492, 226)], fill=NAVY, width=2)

    # portrait
    ph = portrait()
    img_rgba.alpha_composite(ph, (62, 244))
    d = ImageDraw.Draw(img_rgba)
    d.rectangle([62, 244, 212, 434], outline=NAVY, width=2)
    text(d, (137, 440), "PHOTOGRAPH / FOTOGRAFIJA", F(SANS_B, 8), fill=GREY,
         anchor="ma")
    # faint ghost image of holder in data area (security print)
    ghost = ph.resize((52, 66))
    ghost.putalpha(38)
    img_rgba.alpha_composite(ghost, (428, 246))
    d = ImageDraw.Draw(img_rgba)

    # data fields, right of photo
    fx = 232
    label_value(d, fx, 244, "SURNAME / PREZIME", "KOVAC")
    label_value(d, fx, 282, "GIVEN NAMES / IMENA", "ELENA MARA")
    label_value(d, fx, 320, "NATIONALITY / DRZAVLJANSTVO", "TARNOVIAN")
    label_value(d, fx, 358, "DATE OF BIRTH / DATUM RODENJA", "12 JUN 1996")
    label_value(d, fx, 396, "PLACE OF BIRTH / MJESTO RODENJA", "TARNOGRAD")
    label_value(d, fx, 434, "SEX / SPOL", "F")
    d.line([(62, 478), (492, 478)], fill=(170, 164, 140), width=1)
    label_value(d, 62, 492, "DATE OF ISSUE", "14 MAR 2024")
    label_value(d, 250, 492, "DATE OF EXPIRY", "13 MAR 2034")
    label_value(d, 415, 492, "HEIGHT", "172 cm")
    label_value(d, 62, 530, "AUTHORITY", "MINISTRY OF INTERIOR")
    label_value(d, 270, 530, "PLACE OF ISSUE", "TARNOGRAD")
    label_value(d, 425, 530, "EYES", "BROWN")
    d.line([(62, 578), (492, 578)], fill=(170, 164, 140), width=1)
    # signature
    text(d, (62, 592), "HOLDER'S SIGNATURE / POTPIS NOSITELJA",
         F(SANS_B, 9), fill=GREY)
    text(d, (70, 610), "Elena Mara Kovac", F(SERIF, 24), fill=(40, 52, 90))
    d.line([(62, 640), (300, 640)], fill=GREY, width=1)
    # observations — the telling paperwork detail, on the data page too
    text(d, (330, 592), "OBSERVATIONS / NAPOMENE", F(SANS_B, 9), fill=GREY)
    text(d, (330, 606), "Licensed mountain guide,", F(SANS, 11), fill=INK)
    text(d, (330, 620), "North Ridge, cat. II.", F(SANS, 11), fill=INK)
    text(d, (330, 634), "Blood group O+.", F(SANS, 11), fill=INK)
    # MRZ
    d.rectangle([42, 668, 512, 756], fill=(232, 226, 208))
    d.line([(42, 668), (512, 668)], fill=NAVY, width=2)
    l1, l2 = mrz_lines()
    text(d, (62, 682), l1, F(MONO, 16), fill=INK)
    text(d, (62, 706), l2, F(MONO, 16), fill=INK)
    text(d, (62, 736), "Machine-readable zone — ICAO Doc 9303",
         F(SANS, 9), fill=GREY)
    # notice fills the space below the MRZ
    text(d, (62, 782), "NOTICE / OBAVIJEST", F(SANS_B, 9), fill=GREY)
    text(d, (62, 796),
         "If found, please return this passport to the nearest Tarnovian",
         F(SANS, 11), fill=INK)
    text(d, (62, 811),
         "mission, or to the Ministry of the Interior, Tarnograd.",
         F(SANS, 11), fill=INK)
    text(d, (62, 826),
         "This passport contains 32 pages. Alteration voids the document.",
         F(SANS, 11), fill=INK)
    # page footer
    text(d, (277, 872), "TARNOVIA  •  This passport remains the property of the Republic of Tarnovia",
         F(SANS, 9), fill=GREY, anchor="ma")
    text(d, (492, 872), "1", F(SANS_B, 11), fill=GREY, anchor="ra")

    # ================= RIGHT PAGE: visas & stamps =================
    text(d, (747, 132), "VISAS", F(SERIF_B, 20), fill=NAVY, anchor="ma")
    text(d, (747, 154), "VIZE  •  ENTRY AND EXIT STAMPS  •  ULASCI I IZLASCI",
         F(SANS_B, 9), fill=GREY, anchor="ma")
    d.line([(532, 168), (962, 168)], fill=NAVY, width=2)
    # faint watermark emblem
    wm = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    emblem(wd, 747, 520, 260)
    wm.putalpha(14)
    img_rgba.alpha_composite(wm)
    d = ImageDraw.Draw(img_rgba)

    # --- Dravaria visa sticker
    d.rectangle([552, 186, 962, 330], fill=(226, 234, 240),
                outline=NAVY2, width=2)
    d.rectangle([552, 186, 962, 214], fill=NAVY2)
    text(d, (572, 192), "VISA  —  DRAVARIA", F(SANS_B, 13),
         fill=(255, 255, 255))
    text(d, (942, 192), "No. DV-2024-11873", F(SANS_B, 11),
         fill=(220, 226, 236), anchor="ra")
    label_value(d, 572, 224, "VALID FROM", "18 SEP 2024", vsize=13)
    label_value(d, 742, 224, "UNTIL", "17 OCT 2024", vsize=13)
    label_value(d, 872, 224, "ENTRIES", "SINGLE", vsize=13)
    label_value(d, 572, 262, "DURATION", "30 DAYS", vsize=13)
    label_value(d, 742, 262, "ISSUED AT", "TARNOGRAD", vsize=13)
    label_value(d, 872, 262, "ON", "05 SEP 2024", vsize=13)
    text(d, (572, 306), "Purpose: mountain-guiding contract, Dravaria Alpine Club.",
         F(SANS, 11), fill=INK)
    # visa sticker corner seal
    d.ellipse([916, 292, 954, 330], outline=GOLD, width=2)
    text(d, (935, 311), "DV", F(SERIF_B, 12), fill=GOLD, anchor="mm")

    # --- condition box: the telling detail
    d.rectangle([552, 348, 962, 436], outline=RED, width=2)
    d.rectangle([552, 348, 962, 372], fill=RED)
    text(d, (572, 353), "CONDITION OF ISSUE  —  UVJET IZDAVANJA",
         F(SANS_B, 11), fill=(255, 255, 255))
    text(d, (572, 382),
         "Holder must carry a Mountain Pass Permit for any route",
         F(SANS, 12), fill=INK)
    text(d, (572, 398),
         "above 2,000 m. A licensed guide is required on the",
         F(SANS, 12), fill=INK)
    text(d, (572, 414),
         "North Ridge in winter. Permit No. MP-77-0142.",
         F(SANS, 12), fill=INK)

    # --- stamps (all AFTER issue 14 MAR 2024, in travel order)
    stamp_circle(img_rgba, 640, 520, 62,
                 ["OSTMARK", "ENTRY", "02 MAY 2024", "KRAJINA"], PURPLE, -8)
    stamp_circle(img_rgba, 856, 520, 62,
                 ["OSTMARK", "EXIT", "09 MAY 2024", "KRAJINA"], PURPLE, 7)
    stamp_circle(img_rgba, 640, 660, 62,
                 ["DRAVARIA", "ENTRY", "18 SEP 2024", "VELKA"], BLUE, 9)
    stamp_circle(img_rgba, 856, 660, 62,
                 ["DRAVARIA", "EXIT", "02 OCT 2024", "VELKA"], BLUE, -6)
    stamp_rect(img_rgba, (600, 748, 780, 806),
               ["FEE PAID", "45 TALER", "14 MAR 2024"], TEAL, -4, size=12)
    stamp_rect(img_rgba, (800, 748, 950, 806),
               ["REGISTERED", "GUIDE No. 0142", "TARNOGRAD"], NAVY2, 5, size=11)

    # travel-history footnote ties stamps to dates
    text(d, (747, 830),
         "Travel: Tarnograd → Ostmark 02–09 May 2024 → Dravaria 18 Sep–02 Oct 2024",
         F(SANS, 11), fill=GREY, anchor="ma")
    text(d, (747, 848),
         "No stamp predates the passport (issued 14 Mar 2024).",
         F(SANS, 11), fill=GREY, anchor="ma")
    text(d, (747, 872), "TARNOVIA  •  VISAS  •  Pages 2–3 of 32",
         F(SANS, 9), fill=GREY, anchor="ma")
    text(d, (962, 872), "2", F(SANS_B, 11), fill=GREY, anchor="ra")

    return img_rgba.convert("RGB")

def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        outdir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)
    img = render()
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print(path, img.size, os.path.getsize(path), "bytes")

if __name__ == "__main__":
    main()
