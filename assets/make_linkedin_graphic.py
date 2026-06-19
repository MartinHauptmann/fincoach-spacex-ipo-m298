#!/usr/bin/env python3
"""Generate the FinCoach AI LinkedIn graphic for the SpaceX post-IPO update."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
BG_TOP, BG_BOT = (10, 15, 26), (13, 20, 38)
CYAN = (0, 207, 255)
EMERALD = (0, 204, 122)
MAGENTA = (230, 57, 154)
ORANGE = (255, 107, 0)
GOLD = (223, 175, 15)
WHITE = (232, 240, 248)
MUTED = (100, 116, 139)
CARD = (18, 26, 46)
BORDER = (30, 41, 59)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
def fb(s): return ImageFont.truetype(FB, s)
def fr(s): return ImageFont.truetype(FR, s)
def fm(s): return ImageFont.truetype(FM, s)

img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img)

# vertical gradient background
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)))

# soft cyan glow top-right
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in [(520, 8), (380, 10), (240, 14)]:
    gd.ellipse([W - r, -r // 2, W + r, r + 120], fill=(0, 207, 255, a))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=WHITE, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def spaced(x, y, s, font, fill, gap=3):
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + gap
    return cx

M = 72

# ---- HEADER: logo bars + wordmark ----
bars = [(MAGENTA, 30), (CYAN, 44), (EMERALD, 58), (ORANGE, 72)]
bx, baseY = M, 96
for i, (col, h) in enumerate(bars):
    x0 = bx + i * 17
    d.rounded_rectangle([x0, baseY - h, x0 + 12, baseY], radius=5, fill=col)
text(bx + 88, 56, "FinCoach AI", fb(30))
text(bx + 88, 92, "by TheNextGenerationBanking.com", fr(17), MUTED)
# right pill
pill = "ANALYSE · MODUL M298"
pw = d.textlength(pill, font=fm(17)) + 36
d.rounded_rectangle([W - M - pw, 60, W - M, 100], radius=20, outline=BORDER, width=2, fill=CARD)
text(W - M - pw / 2, 80, pill, fm(17), CYAN, anchor="mm")

# ---- EYEBROW ----
spaced(M, 178, "IPO-DEBÜT · 12.06.2026 · SPCX · NASDAQ", fm(20), CYAN, gap=2)

# ---- HEADLINE ----
text(M, 212, "SpaceX ist an der Börse.", fb(60))

# ---- BIG METRIC ----
text(M, 300, "~$2,42 Bln.", fb(112), CYAN)
text(M, 432, "Marktkapitalisierung  ·  Schluss 18.06.2026: $185,00 (−3,56 %)", fr(24), WHITE)

# ---- VALUATION TIMELINE ----
ty = 510
nodes = [
    ("S-1-FILING", "~$1,75 Bln.", MUTED),
    ("IPO 12.06.", "$135 → ~$150 (+11 %)", EMERALD),
    ("HEUTE", "~$2,42 Bln.", CYAN),
]
seg = (W - 2 * M) / len(nodes)
centers = [M + seg * i + seg / 2 for i in range(len(nodes))]
for i in range(1, len(nodes)):
    mid = (centers[i - 1] + centers[i]) / 2
    d.text((mid, ty + 34), "→", font=fb(30), fill=MUTED, anchor="mm")
for i, (lab, val, col) in enumerate(nodes):
    cx = centers[i]
    text(cx, ty + 4, lab, fm(17), MUTED, anchor="ma")
    text(cx, ty + 30, val, fb(24), col, anchor="ma")

# ---- STAT CARDS ----
sy, sh = 600, 132
stats = [
    ("~$75 Mrd.", "Emissionserlös", "bis ~$86 Mrd. mit Greenshoe", EMERALD),
    ("~5 %", "Free Float", "frei handelbar → hohe Volatilität", ORANGE),
    ("bis 30 %", "Retail-Quote", "sehr hoher Privatanleger-Anteil", MAGENTA),
]
gap = 24
cw = (W - 2 * M - 2 * gap) / 3
for i, (big, lab, sub, col) in enumerate(stats):
    x0 = M + i * (cw + gap)
    d.rounded_rectangle([x0, sy, x0 + cw, sy + sh], radius=16, fill=CARD, outline=BORDER, width=2)
    d.rounded_rectangle([x0, sy, x0 + 6, sy + sh], radius=3, fill=col)
    text(x0 + 26, sy + 20, big, fb(40), col)
    text(x0 + 26, sy + 72, lab, fb(20), WHITE)
    text(x0 + 26, sy + 100, sub, fr(15), MUTED)

# ---- CRITICAL COUNTERPOINT ----
cy0, ch = 768, 96
d.rounded_rectangle([M, cy0, W - M, cy0 + ch], radius=16, fill=(28, 18, 32), outline=(74, 30, 52), width=2)
d.rounded_rectangle([M, cy0, M + 6, cy0 + ch], radius=3, fill=MAGENTA)
text(M + 28, cy0 + 18, "KRITISCHER GEGENPUNKT", fm(16), MAGENTA)
text(M + 28, cy0 + 44, "Morningstar Fair Value ~$780 Mrd. — rund 3× unter dem aktuellen Marktpreis.", fb(23), WHITE)

# ---- FOOTER ----
fyL = 900
d.line([(M, fyL), (W - M, fyL)], fill=BORDER, width=1)
text(M, fyL + 22, "Datenstand 2026-06-19  ·  Bewertungszahlen medien-/nutzerbasiert, nicht unabhängig verifiziert.", fr(18), MUTED)
text(M, fyL + 50, "Keine Anlage-, Steuer- oder Rechtsberatung.", fr(18), MUTED)
text(W - M, fyL + 59, "fincoach-spacex-ipo-m298", fm(18), CYAN, anchor="rm")

out = "/home/user/fincoach-spacex-ipo-m298/assets/linkedin-spacex-ipo.png"
img.save(out, "PNG")
print("saved", out, img.size)
