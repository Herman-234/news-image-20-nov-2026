#!/usr/bin/env python3
"""Draw the 20 November 2026 one-day news image (1024x1024 PNG).

Fresh, self-contained renderer: Pillow + DejaVu fonts, stdlib only,
no network. Layout: navy masthead, White House hero with the 2027
callout, two right-hand cards, three mid cards, an In Brief panel.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
FONTS = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 242, 231)
INK = (24, 24, 24)
GREY = (96, 96, 96)
LIGHT_GREY = (200, 198, 190)
NAVY = (27, 42, 74)
NAVY_DARK = (22, 32, 56)
RED = (178, 34, 34)
GOLD = (216, 178, 60)
SKY_TOP = (176, 208, 226)
SKY_BOT = (238, 228, 200)
GREEN = (110, 168, 92)
PURPLE = (58, 44, 92)
TEAL = (14, 110, 120)
SLATE = (64, 84, 112)
BROWN = (124, 72, 20)
WHITE = (255, 255, 255)
PALE = (225, 220, 240)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, max_w, leading=None):
    lh = leading if leading is not None else int(font.size * 1.25)
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def fit_font(d, text, name, start, max_w):
    size = start
    while size > 10 and d.textlength(text, font=F(name, size)) > max_w:
        size -= 1
    return F(name, size)


def card(d, box, fill, radius=14):
    d.rounded_rectangle(box, radius=radius, fill=fill)


def draw_controller(d, x, y):
    d.rounded_rectangle([x, y, x + 96, y + 38], radius=14, fill=(32, 26, 60))
    d.rectangle([x + 14, y + 15, x + 26, y + 23], fill=WHITE)
    d.rectangle([x + 18, y + 11, x + 22, y + 27], fill=WHITE)
    for i, c in enumerate([(216, 178, 60), (178, 34, 34), (255, 255, 255), (110, 168, 92)]):
        cx, cy = x + 66 + (i % 2) * 12, y + 12 + (i // 2) * 12
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c)


def draw_cyclone(d, cx, cy):
    for r, start, end in [(38, 30, 300), (28, 120, 30), (18, 210, 120)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=WHITE, width=4)


def draw_globe(d, cx, cy):
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=WHITE, width=3)
    d.ellipse([cx - 12, cy - 26, cx + 12, cy + 26], outline=WHITE, width=2)
    d.line([cx - 26, cy, cx + 26, cy], fill=WHITE, width=2)
    d.arc([cx - 26, cy - 12, cx + 26, cy + 12], 200, 340, fill=WHITE, width=2)


def draw_satellite(d, x, y):
    d.rectangle([x, y + 8, x + 26, y + 22], fill=(120, 160, 200))
    d.rectangle([x + 32, y, x + 62, y + 30], fill=WHITE)
    d.rectangle([x + 68, y + 8, x + 94, y + 22], fill=(120, 160, 200))
    d.arc([x + 40, y - 14, x + 54, y], 180, 360, fill=GOLD, width=3)


def draw_flags(d, x, y):
    # India: saffron / white / green with navy wheel dot
    d.rectangle([x, y, x + 40, y + 8], fill=(255, 153, 51))
    d.rectangle([x, y + 8, x + 40, y + 16], fill=WHITE)
    d.rectangle([x, y + 16, x + 40, y + 24], fill=(19, 136, 8))
    d.ellipse([x + 17, y + 9, x + 23, y + 15], outline=(0, 0, 128), width=1)
    # UK: simplified Union Jack
    x2 = x + 50
    d.rectangle([x2, y, x2 + 40, y + 24], fill=(1, 33, 105))
    d.rectangle([x2 + 16, y, x2 + 24, y + 24], fill=WHITE)
    d.rectangle([x2, y + 8, x2 + 40, y + 16], fill=WHITE)
    d.rectangle([x2 + 18, y, x2 + 22, y + 24], fill=(200, 16, 46))
    d.rectangle([x2, y + 10, x2 + 40, y + 14], fill=(200, 16, 46))


def draw_hero_scene(d):
    # sky gradient bands
    for yy in range(150, 450):
        t = (yy - 150) / 300.0
        c = tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3))
        d.line([(24, yy), (660, yy)], fill=c)
    # sun
    d.ellipse([560, 176, 612, 228], fill=(250, 228, 150))
    # ground
    d.rectangle([24, 424, 660, 450], fill=GREEN)
    # White House: side wings, main block, windows, columns, pediment, dome, flag
    d.rectangle([118, 376, 152, 424], fill=WHITE, outline=LIGHT_GREY)
    d.rectangle([528, 376, 562, 424], fill=WHITE, outline=LIGHT_GREY)
    d.rectangle([152, 350, 528, 424], fill=WHITE, outline=LIGHT_GREY)
    for wx in (176, 216, 464, 504):
        d.rectangle([wx, 368, wx + 22, 398], fill=NAVY)
    d.polygon([(282, 350), (398, 350), (340, 308)], fill=WHITE, outline=LIGHT_GREY)
    d.ellipse([324, 292, 356, 324], fill=GOLD, outline=(180, 140, 40))
    d.line([340, 248, 340, 292], fill=INK, width=3)
    d.rectangle([340, 250, 380, 268], fill=WHITE, outline=RED)
    for i in range(3):
        d.line([340, 253 + i * 6, 380, 253 + i * 6], fill=RED, width=2)
    d.rectangle([340, 250, 356, 260], fill=(30, 50, 120))
    for cx in (298, 326, 354, 382):
        d.rectangle([cx, 352, cx + 10, 424], fill=WHITE, outline=LIGHT_GREY)
    d.rectangle([330, 396, 356, 424], fill=NAVY_DARK)
    d.rectangle([282, 424, 398, 431], fill=(220, 220, 220))
    d.rectangle([272, 431, 408, 438], fill=(205, 205, 205))
    # callout box: decision moved to 2027
    d.rounded_rectangle([440, 200, 648, 332], radius=10, fill=WHITE, outline=RED, width=3)
    d.rectangle([443, 203, 645, 238], fill=RED)
    f_head = F(SANS_B, 15)
    t = "DECISION MOVED TO"
    d.text(((440 + 648 - d.textlength(t, font=f_head)) / 2, 213), t, font=f_head, fill=WHITE)
    f_big = F(SERIF_B, 62)
    t = "2027"
    d.text(((440 + 648 - d.textlength(t, font=f_big)) / 2, 244), t, font=f_big, fill=RED)
    f_sub = F(SANS_B, 18)
    t = "after Jan 1"
    d.text(((440 + 648 - d.textlength(t, font=f_sub)) / 2, 306), t, font=f_sub, fill=INK)
    d.line([400, 268, 438, 268], fill=RED, width=4)
    d.polygon([(400, 268), (416, 260), (416, 276)], fill=RED)


def brief_item(d, x, y, lead, body, max_w):
    f_lead = F(SANS_B, 16)
    f_body = F(SANS, 16)
    d.ellipse([x, y + 7, x + 8, y + 15], fill=RED)
    lx = x + 16
    lead_w = d.textlength(lead, font=f_lead)
    lines = wrap(d, body, f_body, max_w - lead_w - 16)
    d.text((lx, y), lead, font=f_lead, fill=RED)
    d.text((lx + lead_w, y), lines[0], font=f_body, fill=INK)
    yy = y + 20
    for ln in lines[1:]:
        d.text((lx, yy), ln, font=f_body, fill=INK)
        yy += 20
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    f_title = fit_font(d, title, SERIF_B, 52, 640)
    d.text((28, 26), title, font=f_title, fill=WHITE)
    f_day = F(SANS_B, 20)
    t = "FRIDAY"
    d.text((W - 28 - d.textlength(t, font=f_day), 22), t, font=f_day, fill=GOLD)
    f_date = F(SANS_B, 26)
    t = "20 NOVEMBER 2026"
    d.text((W - 28 - d.textlength(t, font=f_date), 50), t, font=f_date, fill=WHITE)
    d.rectangle([0, 104, W, 110], fill=RED)
    # dateline strip
    f_dl = F(SANS_B, 17)
    d.text((28, 120), "FRIDAY, 20 NOVEMBER 2026  \u2022  TWELVE STORIES FROM AROUND THE WORLD",
           font=f_dl, fill=INK)
    t = "make.fun"
    d.text((W - 28 - d.textlength(t, font=f_dl), 120), t, font=f_dl, fill=GREY)

    # hero panel
    draw_hero_scene(d)
    d.rectangle([24, 450, 660, 560], fill=NAVY)
    f_hl = F(SANS_B, 26)
    y = para(d, 40, 462, "TRUMP PUSHES IRAN CALL TO 2027", f_hl, WHITE, 600, leading=32)
    f_sl = F(SANS, 17)
    para(d, 40, y + 4, "President says he will \u201csee what happens\u201d after Jan 1 "
                       "\u2014 no rush on the Gulf call.", f_sl, PALE, 600, leading=21)

    # right column cards
    card(d, [672, 150, 1000, 350], PURPLE)
    draw_controller(d, 700, 172)
    para(d, 692, 226, "GTA VI: $2.36BN IN ONE DAY", F(SANS_B, 26), WHITE, 288, leading=30)
    para(d, 692, 292, "Sensor Tower: 24.6m copies sold \u2014 the biggest debut ever.",
         F(SANS, 18), PALE, 288, leading=22)
    card(d, [672, 360, 1000, 560], TEAL)
    draw_cyclone(d, 836, 408)
    para(d, 692, 448, "CYCLONE AKVAN SLAMS ODISHA", F(SANS_B, 26), WHITE, 288, leading=30)
    para(d, 692, 506, "Landfall near Gopalpur; 3 lakh evacuated, 423 teams out.",
         F(SANS, 18), PALE, 288, leading=22)

    # mid row cards
    card(d, [24, 572, 344, 788], SLATE)
    draw_globe(d, 184, 606)
    para(d, 40, 644, "EUROPE READY TO TALK TO RUSSIA", F(SANS_B, 25), WHITE, 288, leading=29)
    para(d, 40, 708, "Leaders say they are ready for negotiations to end the war in Ukraine.",
         F(SANS, 18), PALE, 288, leading=22)
    card(d, [352, 572, 672, 788], NAVY_DARK)
    draw_satellite(d, 482, 590)
    para(d, 368, 644, "HAYABUSA2 DROPS ASTEROID LANDING", F(SANS_B, 25), WHITE, 288, leading=29)
    para(d, 368, 708, "Engine trouble forces Japan\u2019s probe to abandon its touchdown plan.",
         F(SANS, 18), PALE, 288, leading=22)
    card(d, [680, 572, 1000, 788], BROWN)
    draw_flags(d, 776, 592)
    para(d, 696, 644, "MODI MEETS WILLIAM AND KATE", F(SANS_B, 25), WHITE, 288, leading=29)
    para(d, 696, 708, "PM hosts the Prince and Princess of Wales in New Delhi; talks on India\u2013UK ties.",
         F(SANS, 18), PALE, 288, leading=22)

    # In Brief panel
    d.rounded_rectangle([24, 800, 1000, 980], radius=12, fill=WHITE, outline=LIGHT_GREY, width=2)
    d.text((44, 812), "IN BRIEF", font=F(SANS_B, 20), fill=RED)
    d.line([44, 842, 980, 842], fill=LIGHT_GREY, width=1)
    briefs_left = [
        ("CRICKET \u2014 ", "Nicholls 113* as New Zealand reach 243/5 on day one against India."),
        ("SENEGAL \u2014 ", "Dozens missing after a migrant boat sinks off the coast."),
        ("AI \u2014 ", "Anthropic\u2019s valuation reportedly reaches $1.5 trillion."),
    ]
    briefs_right = [
        ("CINCINNATI \u2014 ", "Fiona the hippo dies at Cincinnati Zoo."),
        ("MARKETS \u2014 ", "Sensex up 1.21% and Nifty up 1.14% in a strong rally."),
        ("DEFENCE \u2014 ", "India signs a Rs 1,976-crore deal with Israel Aerospace Industries."),
    ]
    for i, (lead, body) in enumerate(briefs_left):
        brief_item(d, 44, 850 + i * 43, lead, body, 452)
    for i, (lead, body) in enumerate(briefs_right):
        brief_item(d, 524, 850 + i * 43, lead, body, 452)

    # footer
    f_ft = F(SANS, 14)
    t = "All stories first reported Friday 20 November 2026  \u2022  Sources: Reuters, BBC, Sensor Tower, IMD, Space.com, ANI"
    d.text(((W - d.textlength(t, font=f_ft)) / 2, 990), t, font=f_ft, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote %s %d bytes sha256=%s" % (OUT, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
