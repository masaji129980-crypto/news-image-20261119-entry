"""Draw the 19 November 2026 world-news summary image.

Original artwork drawn entirely in code with Pillow: no photos, no
downloaded assets, no copied artwork. Deterministic: fixed palette,
fixed geometry, fixed fonts, no randomness and no timestamps, so two
runs produce byte-identical PNG output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 233)      # warm newsprint
INK = (24, 28, 38)          # near-black
NAVY = (18, 38, 66)         # masthead
RED = (178, 34, 34)         # accent
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
LINE = (180, 172, 150)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_summit(d, x, y, s, c):
    """Three leaders seated at a table: three heads, three flags."""
    # table
    d.rectangle([x, y + 62 * s, x + 150 * s, y + 72 * s], fill=c)
    d.rectangle([x + 8 * s, y + 72 * s, x + 18 * s, y + 96 * s], fill=c)
    d.rectangle([x + 132 * s, y + 72 * s, x + 142 * s, y + 96 * s], fill=c)
    # three heads + shoulders
    cols = [(178, 34, 34), (18, 38, 66), (201, 162, 39)]
    for i, col in enumerate(cols):
        cx = x + (25 + 50 * i) * s
        d.ellipse([cx - 13 * s, y + 8 * s, cx + 13 * s, y + 34 * s], fill=col)
        d.pieslice([cx - 20 * s, y + 34 * s, cx + 20 * s, y + 66 * s],
                   180, 360, fill=col)
    # three small flags on the table
    for i, col in enumerate(cols):
        fx = x + (30 + 50 * i) * s
        d.line([fx, y + 40 * s, fx, y + 62 * s], fill=INK, width=max(2, int(2 * s)))
        d.polygon([(fx, y + 40 * s), (fx + 16 * s, y + 45 * s), (fx, y + 50 * s)],
                  fill=col)


def draw_scales(d, x, y, s, c):
    """Scales of justice."""
    d.line([x + 75 * s, y + 6 * s, x + 75 * s, y + 92 * s], fill=c,
           width=max(3, int(4 * s)))
    d.line([x + 15 * s, y + 18 * s, x + 135 * s, y + 18 * s], fill=c,
           width=max(3, int(4 * s)))
    d.ellipse([x + 68 * s, y + 2 * s, x + 82 * s, y + 16 * s], fill=c)
    for cx in (x + 15 * s, x + 135 * s):
        d.line([cx, y + 18 * s, cx, y + 52 * s], fill=c, width=max(2, int(3 * s)))
        d.polygon([(cx - 26 * s, y + 52 * s), (cx + 26 * s, y + 52 * s),
                   (cx, y + 80 * s)], fill=c)
    d.rectangle([x + 55 * s, y + 92 * s, x + 95 * s, y + 98 * s], fill=c)


def draw_bridge(d, x, y, s, c):
    """A bridge deck with towers and a blast star above it."""
    d.rectangle([x + 4 * s, y + 66 * s, x + 146 * s, y + 78 * s], fill=c)
    for tx in (x + 28 * s, x + 112 * s):
        d.rectangle([tx, y + 34 * s, tx + 10 * s, y + 78 * s], fill=c)
    d.line([x + 33 * s, y + 34 * s, x + 75 * s, y + 66 * s], fill=c,
           width=max(2, int(3 * s)))
    d.line([x + 117 * s, y + 34 * s, x + 75 * s, y + 66 * s], fill=c,
           width=max(2, int(3 * s)))
    # explosion star
    cx, cy = x + 75 * s, y + 22 * s
    pts = []
    import math
    for i in range(12):
        r = 26 * s if i % 2 == 0 else 10 * s
        a = math.pi * i / 6 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(214, 90, 20))


def draw_tank(d, x, y, s, c):
    """Tank silhouette: hull, turret, barrel, wheels."""
    d.rounded_rectangle([x + 8 * s, y + 52 * s, x + 142 * s, y + 82 * s],
                        radius=int(8 * s), fill=c)
    d.rounded_rectangle([x + 48 * s, y + 30 * s, x + 96 * s, y + 56 * s],
                        radius=int(6 * s), fill=c)
    d.rectangle([x + 92 * s, y + 38 * s, x + 146 * s, y + 46 * s], fill=c)
    for i in range(5):
        cx = x + (28 + 22 * i) * s
        d.ellipse([cx - 8 * s, y + 78 * s, cx + 8 * s, y + 94 * s],
                  fill=INK, outline=(255, 255, 255), width=2)


def draw_missile(d, x, y, s, c):
    """Rocket arcing up with a flame trail."""
    # flame
    d.polygon([(x + 55 * s, y + 96 * s), (x + 75 * s, y + 96 * s),
               (x + 65 * s, y + 66 * s)], fill=(214, 90, 20))
    d.polygon([(x + 58 * s, y + 96 * s), (x + 72 * s, y + 96 * s),
               (x + 65 * s, y + 78 * s)], fill=GOLD)
    # body
    d.polygon([(x + 48 * s, y + 70 * s), (x + 82 * s, y + 70 * s),
               (x + 92 * s, y + 30 * s), (x + 65 * s, y + 6 * s),
               (x + 38 * s, y + 30 * s)], fill=c)
    d.polygon([(x + 48 * s, y + 70 * s), (x + 30 * s, y + 86 * s),
               (x + 52 * s, y + 74 * s)], fill=c)
    d.polygon([(x + 82 * s, y + 70 * s), (x + 100 * s, y + 86 * s),
               (x + 78 * s, y + 74 * s)], fill=c)
    d.ellipse([x + 56 * s, y + 34 * s, x + 74 * s, y + 52 * s], fill=WHITE)


def draw_chart(d, x, y, s, c):
    """Rising market chart with an arrow."""
    d.line([x + 10 * s, y + 92 * s, x + 140 * s, y + 92 * s], fill=c,
           width=max(3, int(4 * s)))
    d.line([x + 10 * s, y + 92 * s, x + 10 * s, y + 8 * s], fill=c,
           width=max(3, int(4 * s)))
    pts = [(x + 14 * s, y + 78 * s), (x + 45 * s, y + 66 * s),
           (x + 70 * s, y + 70 * s), (x + 100 * s, y + 40 * s),
           (x + 128 * s, y + 14 * s)]
    d.line(pts, fill=(34, 139, 34), width=max(4, int(5 * s)), joint="curve")
    d.polygon([(x + 128 * s, y + 14 * s), (x + 112 * s, y + 12 * s),
               (x + 126 * s, y + 30 * s)], fill=(34, 139, 34))
    d.ellipse([x + 122 * s, y + 8 * s, x + 134 * s, y + 20 * s],
              fill=(34, 139, 34))


ICONS = {
    "summit": draw_summit,
    "scales": draw_scales,
    "bridge": draw_bridge,
    "tank": draw_tank,
    "missile": draw_missile,
    "chart": draw_chart,
}

# (tag, icon, accent, headline, subline)
STORIES = [
    ("DIPLOMACY", "summit", NAVY,
     "Three leaders, one table",
     "Trump, Xi & Putin hold a first three-way summit in Shenzhen."),
    ("JUSTICE", "scales", (90, 60, 120),
     "Myanmar guilty of genocide",
     "ICJ: first genocide ruling by the world court."),
    ("WAR IN UKRAINE", "bridge", (120, 60, 30),
     "Crimean Bridge hit again",
     "Ukraine strikes the bridge a third time in one week."),
    ("MIDDLE EAST", "tank", (110, 30, 30),
     "Tanks push into central Gaza",
     "Israel launches a ground operation beyond the ceasefire line."),
    ("IRAN WAR", "missile", (140, 40, 20),
     "Gulf states under fire",
     "US strikes Qeshm island; Iran hits Kuwait & Bahrain."),
    ("TECH", "chart", (20, 90, 60),
     "Anthropic IPO breaks records",
     "Shares at $83 — about $81 billion raised, a record debut."),
]


def draw_image(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    f_kicker = font(FONT_SANS_BOLD, 26)
    f_date = font(FONT_SERIF_BOLD, 74)
    f_sub = font(FONT_SANS, 26)
    d.text((32, 14), "THE WORLD IN ONE DAY  •  THURSDAY", font=f_kicker,
           fill=GOLD)
    d.text((W - 32 - d.textlength("WORLD NEWS", font=f_sub), 14),
           "WORLD NEWS", font=f_sub, fill=(200, 210, 225))
    d.text((30, 48), "19 NOVEMBER 2026", font=f_date, fill=WHITE)

    # ---- Story grid: 2 cols x 3 rows ----
    margin, gap = 24, 20
    pw = (W - 2 * margin - gap) // 2
    ph = 252
    top = 178
    f_tag = font(FONT_SANS_BOLD, 21)
    f_head = font(FONT_SANS_BOLD, 30)
    f_body = font(FONT_SANS, 23)

    for i, (tag, icon, accent, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        # panel
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=PANEL, outline=LINE, width=2)
        d.rounded_rectangle([x, y, x + pw, y + 40], radius=10, fill=accent)
        d.rectangle([x, y + 24, x + pw, y + 40], fill=accent)
        d.text((x + 16, y + 8), tag, font=f_tag, fill=WHITE)
        # icon, left side
        ix, iy = x + 18, y + 62
        ICONS[icon](d, ix, iy, 0.85, accent)
        # text, right of icon
        tx = x + 178
        tw = pw - 178 - 16
        lines = wrap(d, head, f_head, tw)
        ly = y + 56
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 36
        blines = wrap(d, body, f_body, tw)
        ly += 6
        for ln in blines[:3]:
            d.text((tx, ly), ln, font=f_body, fill=(70, 70, 70))
            ly += 29

    # ---- Footer ----
    fy = H - 44
    d.rectangle([0, fy, W, H], fill=NAVY)
    f_foot = font(FONT_SANS, 22)
    foot = "Thursday 19 November 2026  •  Six stories that shaped the day"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, fy + 9),
           foot, font=f_foot, fill=WHITE)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import sys
    draw_image(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
