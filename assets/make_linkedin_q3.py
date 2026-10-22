#!/usr/bin/env python3
"""FinCoach AI LinkedIn graphic — SpaceX Q3 2026 earnings summary (M300). Sachlich, kein Clickbait."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG_TOP, BG_BOT = (10, 15, 26), (13, 20, 38)
CYAN = (0, 207, 255); EMERALD = (0, 204, 122); MAGENTA = (230, 57, 154)
ORANGE = (255, 107, 0); GOLD = (223, 175, 15); LAV = (153, 51, 255)
WHITE = (232, 240, 248); MUTED = (100, 116, 139); SLATE = (148, 163, 184)
CARD = (18, 26, 46); BORDER = (30, 41, 59); DARKTXT = (10, 15, 26)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
def fb(s): return ImageFont.truetype(FB, s)
def fr(s): return ImageFont.truetype(FR, s)
def fm(s): return ImageFont.truetype(FM, s)

img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
for r in (520, 360, 240):
    gd.ellipse([W - r, -r // 2, W + r, r + 100], fill=(0, 207, 255, 8))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=WHITE, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
def spaced(x, y, s, font, fill, gap=2):
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=font, fill=fill); cx += d.textlength(ch, font=font) + gap
def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def wrap(s, font, maxw):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

M = 72
BW = W - 2 * M

# ---- HEADER ----
bars = [(MAGENTA, 30), (CYAN, 44), (EMERALD, 58), (ORANGE, 72)]
for i, (col, hh) in enumerate(bars):
    x0 = M + i * 17
    d.rounded_rectangle([x0, 96 - hh, x0 + 12, 96], radius=5, fill=col)
text(M + 88, 56, "FinCoach AI", fb(30))
text(M + 88, 92, "by TheNextGenerationBanking.com", fr(17), MUTED)
pill = "Q3 2026 · MODUL M300"
pw = d.textlength(pill, font=fm(17)) + 36
d.rounded_rectangle([W - M - pw, 60, W - M, 100], radius=20, outline=BORDER, width=2, fill=CARD)
text(W - M - pw / 2, 80, pill, fm(17), CYAN, anchor="mm")

# ---- TITLE ----
spaced(M, 164, "QUARTALSZAHLEN · SPACEX (NASDAQ: SPCX)", fm(19), GOLD, gap=2)
text(M, 196, "SpaceX Q3 2026 — die Zahlen", fb(52))
text(M, 262, "Quartal zum 30.09.2026 · auf Basis der offiziellen Mitteilung, nüchtern eingeordnet.", fr(22), SLATE)

# ---- KPI CARDS (2x2) ----
cw = (BW - 24) // 2; ch = 150
def card(x, y, value, vcol, label, sub, subcol=SLATE):
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=16, fill=CARD, outline=BORDER, width=2)
    text(x + 26, y + 20, value, fb(46), vcol)
    text(x + 26, y + 84, label, fb(21), WHITE)
    text(x + 26, y + 116, sub, fr(18), subcol)
xl, xr = M, M + cw + 24
card(xl, 322, "$14,6 Mrd.", WHITE, "Umsatz Q3", "+161 % ggü. Vorjahr", EMERALD)
card(xr, 322, "$4,4 Mrd.", EMERALD, "Nettoergebnis", "erstmals positiv (Vj. -$1,1 Mrd.)")
card(xl, 492, "$8,8 Mrd.", WHITE, "Adj. EBITDA (Non-GAAP)", "+306 % ggü. Vorjahr", EMERALD)
card(xr, 492, "$0,35", GOLD, "EPS (verwässert)", "9 Monate noch -$0,15")

# ---- SEGMENT MIX BAR ----
sy = 676
text(M, sy, "UMSATZ-MIX Q3 · nach Segment", fb(22), WHITE)
by = sy + 34; bh = 62
segs = [(52, LAV, "SI"), (36, EMERALD, "Connectivity"), (12, CYAN, "Space")]
layer = Image.new("RGBA", (BW, bh), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
cx = 0.0; spans = []
for pct, col, lab in segs:
    sw = BW * pct / 100.0
    ld.rectangle([cx, 0, cx + sw + 1, bh], fill=col); spans.append((cx, sw, col, lab, pct)); cx += sw
mask = Image.new("L", (BW, bh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, BW - 1, bh - 1], radius=12, fill=255)
for cx0, sw, col, lab, pct in spans[1:]:
    ld.rectangle([cx0 - 1, 0, cx0 + 1, bh], fill=(10, 15, 26, 255))
img.paste(layer, (M, by), mask); d = ImageDraw.Draw(img)
for cx0, sw, col, lab, pct in spans:
    center = M + cx0 + sw / 2; tcol = DARKTXT if lum(col) > 150 else WHITE
    text(center, by + bh / 2 - 15, lab, fb(19), tcol, anchor="mm")
    text(center, by + bh / 2 + 10, f"{pct}%", fm(18), tcol, anchor="mm")
text(M, by + bh + 12, "SI in 12 Monaten vom kleinsten zum größten Segment (+830 %) · Starlink 13,6 Mio. Abos · Compute 1,7 GW", fr(17), MUTED)

# ---- EINORDNUNG BOX ----
ey = 846; ew = BW
body = ("Q3 markiert die Trendwende zur Profitabilität — getragen vom SI-Segment und starkem "
        "Connectivity-Cashflow. Mit Vorbehalt: auf 9-Monats-Sicht steht noch ein Nettoverlust "
        "(-$0,4 Mrd.), die KI-Capex liegt bei rund $40 Mrd. (9M). Ergebnisqualität über mehrere "
        "Quartale beobachten.")
lines = wrap(body, fr(20), ew - 48)
eh = 54 + len(lines) * 30 + 16
d.rounded_rectangle([M, ey, M + ew, ey + eh], radius=16, fill=(16, 22, 40), outline=BORDER, width=2)
d.rectangle([M, ey, M + 5, ey + eh], fill=GOLD)
text(M + 24, ey + 16, "EINORDNUNG", fm(18), GOLD)
for i, ln in enumerate(lines):
    text(M + 24, ey + 54 + i * 30, ln, fr(20), (203, 213, 225))

# ---- FOOTER ----
fy = 1205
d.line([(M, fy), (W - M, fy)], fill=BORDER, width=1)
text(M, fy + 18, "Zahlen: offizielle Q3-2026-Mitteilung (Primärquelle) · FinCoach-Faktencheck: 54 Konsistenzprüfungen · Non-GAAP markiert", fr(15), MUTED)
text(M, fy + 44, "Keine Anlage-, Steuer- oder Rechtsberatung · Stand 2026-10-21", fr(15), MUTED)
text(W - M, fy + 54, "nexus2learn.com/m300", fm(18), GOLD, anchor="rm")

out = "/home/user/fincoach-spacex-ipo-m298/assets/linkedin-q3-m300.png"
img.save(out)
print("saved", out, img.size)
