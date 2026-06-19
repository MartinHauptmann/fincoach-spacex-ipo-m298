#!/usr/bin/env python3
"""FinCoach AI LinkedIn graphic — SpaceX IPO allocation cascade (M299)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG_TOP, BG_BOT = (10, 15, 26), (13, 20, 38)
CYAN = (0, 207, 255); EMERALD = (0, 204, 122); MAGENTA = (230, 57, 154)
ORANGE = (255, 107, 0); GOLD = (223, 175, 15); LAV = (153, 51, 255)
INDIGO = (99, 102, 241); WHITE = (232, 240, 248); MUTED = (100, 116, 139)
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
    gd.ellipse([W - r, -r // 2, W + r, r + 100], fill=(223, 175, 15, 8))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=WHITE, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
def spaced(x, y, s, font, fill, gap=2):
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=font, fill=fill); cx += d.textlength(ch, font=font) + gap
def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

M = 72

def stacked_bar(x, y, w, h, segs):
    """segs: list of (pct, color, label). Draws clipped rounded bar, labels inline."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    cx = 0.0
    spans = []
    for pct, col, lab in segs:
        sw = w * pct / 100.0
        ld.rectangle([cx, 0, cx + sw + 1, h], fill=col)
        spans.append((cx, sw, col, lab, pct)); cx += sw
    mask = Image.new("L", (w, h), 0); md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=14, fill=255)
    # thin separators
    for cx0, sw, col, lab, pct in spans[1:]:
        ld.rectangle([cx0 - 1, 0, cx0 + 1, h], fill=(10, 15, 26, 255))
    img.paste(layer, (x, y), mask)
    for cx0, sw, col, lab, pct in spans:
        center = x + cx0 + sw / 2
        tcol = DARKTXT if lum(col) > 150 else WHITE
        if sw >= 120:
            text(center, y + h / 2 - 16, lab, fb(20), tcol, anchor="mm")
            text(center, y + h / 2 + 9, f"{pct}%", fm(19), tcol, anchor="mm")
        elif sw >= 46:
            text(center, y + h / 2, f"{pct}%", fm(18), tcol, anchor="mm")

# ---- HEADER ----
bars = [(MAGENTA, 30), (CYAN, 44), (EMERALD, 58), (ORANGE, 72)]
bx, baseY = M, 96
for i, (col, hh) in enumerate(bars):
    x0 = bx + i * 17
    d.rounded_rectangle([x0, baseY - hh, x0 + 12, baseY], radius=5, fill=col)
text(bx + 88, 56, "FinCoach AI", fb(30))
text(bx + 88, 92, "by TheNextGenerationBanking.com", fr(17), MUTED)
pill = "ZUTEILUNG · MODUL M299"
pw = d.textlength(pill, font=fm(17)) + 36
d.rounded_rectangle([W - M - pw, 60, W - M, 100], radius=20, outline=BORDER, width=2, fill=CARD)
text(W - M - pw / 2, 80, pill, fm(17), GOLD, anchor="mm")

# ---- TITLE ----
spaced(M, 168, "IPO-ZUTEILUNGS-KASKADE · SPACEX", fm(20), GOLD, gap=2)
text(M, 200, "Wer bekommt die Aktien?", fb(54))
text(M, 268, "Von der Welt bis zum Broker — die Allokation als verschachtelte Kaskade.", fr(23), WHITE)

# ---- STAGES ----
BW = W - 2 * M
BH = 72
def stage(y, label, note, segs, note_col=MUTED):
    text(M, y, label, fb(22), WHITE)
    stacked_bar(M, y + 34, BW, BH, segs)
    text(M, y + 34 + BH + 12, note, fr(17), note_col)

stage(330, "① TRANCHEN  ·  Gesamtemission ~$75 Mrd.",
      "Real bei SpaceX: Retail bis ~30 %  ·  Mitarbeiter bis ~5 %  ·  Greenshoe +15 % separat  ·  Free Float ~5 %",
      [(70, CYAN, "Institutionell"), (15, EMERALD, "Anchor"), (10, GOLD, "Retail"), (5, LAV, "Mit.")])

stage(500, "② GEOGRAFISCH  ·  reportierte Ist-Verteilung 85 : 10 : 5",
      "USA-Heimatmarkt dominiert (ITAR-Home-Bias) · DE ~5 % des Deals · Auslandsanteil ~15 % FOCI-sensibel",
      [(85, CYAN, "USA (Core)"), (10, EMERALD, "Europa/UK"), (5, GOLD, "Asien/Rest")],
      note_col=MAGENTA)

stage(670, "③ KONSORTIUM  ·  Banken-Syndikat",
      "3 Global Coordinators · 4 Bookrunners · 6 Co-Manager  ·  Gross Spread ~1 % (0,75–1,5 %)",
      [(54, CYAN, "Global Coordinators"), (28, EMERALD, "Bookrunners"), (18, GOLD, "Co-Manager")])

# Stage 4 with legend
y4 = 840
text(M, y4, "④ DEUTSCHLAND  ·  ~5 % des Deals → Broker & Verbünde", fb(22), WHITE)
de = [(40, CYAN, "Konsortialbank (Deutsche Bank)"),
      (21, EMERALD, "Direktbanken / Neobroker"),
      (12, GOLD, "Genossenschaft (DZ-Verbund)"),
      (12, ORANGE, "Sparkassen (Deka/LBBW)"),
      (10, INDIGO, "Privatbanken / VV"),
      (4, MUTED, "übrige Broker"),
      (1, MAGENTA, "Sozial-/Ethikbanken")]
stacked_bar(M, y4 + 34, BW, BH, de)
# legend 2 columns
ly = y4 + 34 + BH + 16
col_w = BW / 2
for i, (pct, col, lab) in enumerate(de):
    cxl = M + (i % 2) * col_w
    ry = ly + (i // 2) * 30
    d.ellipse([cxl, ry + 4, cxl + 14, ry + 18], fill=col)
    text(cxl + 24, ry, f"{lab}", fr(17), WHITE)
    text(cxl + col_w - 30, ry, f"{pct}%", fm(17), col, anchor="ra")
text(M, ly + 4 * 30 + 8, "Reportierte Fill-Rates (Repartierung): ING ~25 %  ·  Trade Republic ~12,9 % (gekürzt) — Report, nicht verifiziert", fr(15), GOLD)

# ---- FOOTER ----
fy = 1180
d.line([(M, fy), (W - M, fy)], fill=BORDER, width=1)
text(M, fy + 20, "Szenario-Werte (an reale Branchenspannen angelehnt) + reportierte Ist-Angaben · M-DBOM: SCENARIO · Stand 2026-06-19 · nicht verifiziert.", fr(16), MUTED)
text(M, fy + 47, "Keine Anlage-, Steuer- oder Rechtsberatung.", fr(17), MUTED)
text(W - M, fy + 56, "fincoach-spacex-ipo-m298", fm(18), GOLD, anchor="rm")

out = "/home/user/fincoach-spacex-ipo-m298/assets/linkedin-zuteilung-m299.png"
img.save(out, "PNG"); print("saved", out, img.size)
