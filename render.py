#!/usr/bin/env python3
"""Render the news image for make.fun news-image-20261120.

Draws a one-page newspaper front page for Friday 20 November 2026 with
Pillow (standard library + Pillow, no network, no randomness). Run:
    python3 render.py            # writes entry.png next to this file
The output is deterministic: same bytes on every run.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (24, 28, 36)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
RED = (178, 34, 34)
RED_SOFT = (205, 60, 50)
GOLD = (201, 162, 39)
GREY = (96, 100, 108)
LIGHT_LINE = (203, 196, 178)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom, steps=48):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        yy0 = y0 + int((y1 - y0) * i / steps)
        yy1 = y0 + int((y1 - y0) * (i + 1) / steps)
        draw.rectangle([x0, yy0, x1, yy1], fill=col)


def flag_us(draw, x, y, w=54, h=34):
    """Small stylised US flag."""
    stripe = h / 13.0
    for i in range(13):
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.42, y + stripe * 7], fill=(30, 58, 120))
    for r in range(4):
        for c in range(5):
            sx = x + 4 + c * 4.4
            sy = y + 3 + r * 4.4
            draw.ellipse([sx, sy, sx + 1.6, sy + 1.6], fill=(255, 255, 255))


def draw_white_house(draw, x, y, w, h):
    """Neoclassical white mansion with portico, lawn and flag."""
    # lawn
    draw.rectangle([x, y + h - 42, x + w, y + h], fill=(110, 168, 92))
    draw.rectangle([x, y + h - 42, x + w, y + h - 38], fill=(88, 140, 74))
    # main block
    bx, by = x + 30, y + 96
    bw, bh = w - 60, h - 96 - 42
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(250, 250, 246),
                   outline=(180, 180, 172), width=2)
    # wings
    draw.rectangle([bx - 22, by + 34, bx, by + bh], fill=(244, 244, 238),
                   outline=(180, 180, 172), width=2)
    draw.rectangle([bx + bw, by + 34, bx + bw + 22, by + bh],
                   fill=(244, 244, 238), outline=(180, 180, 172), width=2)
    # windows (inside the main block, not hanging below it onto the lawn)
    for i in range(5):
        wx = bx + 26 + i * ((bw - 52) // 4)
        draw.rectangle([wx, by + 24, wx + 22, by + 60],
                       fill=(52, 74, 104), outline=(200, 200, 192), width=1)
    # portico: columns + pediment
    cx, cy, cw = bx + bw // 2, by - 6, 150
    draw.polygon([(cx - cw // 2 - 8, cy), (cx + cw // 2 + 8, cy),
                  (cx, cy - 42)], fill=(250, 250, 246),
                 outline=(180, 180, 172))
    draw.ellipse([cx - 12, cy - 36, cx + 12, cy - 12], fill=GOLD)
    for i in range(4):
        colx = cx - cw // 2 + 12 + i * ((cw - 24) // 3)
        draw.rectangle([colx, cy, colx + 12, by + bh], fill=(255, 255, 255),
                       outline=(190, 190, 182), width=1)
    draw.rectangle([cx - cw // 2 - 6, by + bh - 8, cx + cw // 2 + 6, by + bh],
                   fill=(226, 226, 218))
    # flag pole + flag
    draw.rectangle([cx - 1, cy - 96, cx + 1, cy - 42], fill=(90, 90, 84))
    flag_us(draw, cx + 2, cy - 96, 52, 32)


def draw_calendar(draw, x, y, w, h):
    """Wall calendar page whose big red year is the hook: 2027."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(255, 255, 255), outline=(160, 155, 145), width=2)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10,
                           fill=RED)
    draw.rectangle([x, y + 24, x + w, y + 34], fill=RED)
    draw.text((x + w // 2, y + 5), "DECISION MOVED TO",
              font=font(13, bold=True), fill=(255, 255, 255), anchor="ma")
    draw.text((x + w // 2, y + 44), "2027",
              font=font(62, bold=True), fill=RED, anchor="ma")
    draw.text((x + w // 2, y + 112), "after Jan 1",
              font=font(16, bold=True), fill=INK, anchor="ma")
    # red arrow from left edge pointing at the year
    draw.line([x - 34, y + 74, x - 6, y + 74], fill=RED, width=5)
    draw.polygon([(x - 6, y + 66), (x - 6, y + 82), (x + 8, y + 74)],
                 fill=RED)


def gamepad(draw, cx, cy, s, col=(255, 255, 255), accent=(255, 214, 64)):
    """Simple game controller icon centred at (cx, cy), size s."""
    w, h = int(s * 1.5), int(s * 0.95)
    x0, y0 = cx - w // 2, cy - h // 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(s * 0.30),
                           fill=col)
    draw.rounded_rectangle([x0, y0 + h - int(s * 0.28), x0 + int(s * 0.34),
                            y0 + h + int(s * 0.16)], radius=8, fill=col)
    draw.rounded_rectangle([x0 + w - int(s * 0.34), y0 + h - int(s * 0.28),
                            x0 + w, y0 + h + int(s * 0.16)], radius=8, fill=col)
    # d-pad
    px, py = x0 + int(s * 0.30), y0 + h // 2
    draw.rectangle([px - 5, py - 16, px + 5, py + 16], fill=NAVY)
    draw.rectangle([px - 16, py - 5, px + 16, py + 5], fill=NAVY)
    # buttons
    for dx, dy in ((26, -8), (38, 6), (14, 6), (26, 18)):
        draw.ellipse([x0 + w - int(s * 0.62) + dx - 6, py + dy - 6,
                      x0 + w - int(s * 0.62) + dx + 6, py + dy + 6],
                     fill=accent, outline=NAVY, width=1)


def cyclone_spiral(draw, cx, cy, r, col=(255, 255, 255)):
    """Cyclone swirl made of concentric arcs."""
    for i, rr in enumerate(range(r, 8, -14)):
        start = 20 + i * 55
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 250,
                 fill=col, width=6)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)


def dove(draw, cx, cy, s, col=(255, 255, 255)):
    """Stylised dove in flight: sleek body, raised wing, head and beak."""
    # tail feathers (left)
    for k, dy in enumerate((-6, 0, 6)):
        draw.line([cx - s - 16, cy + dy, cx - s + 6, cy + dy // 2],
                  fill=col, width=5)
    # body
    draw.ellipse([cx - s, cy - s // 3, cx + s, cy + s // 2], fill=col)
    # raised wing
    draw.pieslice([cx - s // 2, cy - s - 6, cx + s // 2, cy + s // 3],
                  180, 360, fill=(214, 226, 238))
    # head + beak
    draw.ellipse([cx + s // 2, cy - s // 2 - 10, cx + s + 14, cy - s // 6],
                 fill=col)
    draw.polygon([(cx + s + 12, cy - s // 3), (cx + s + 28, cy - s // 4),
                  (cx + s + 12, cy - s // 6)], fill=(255, 190, 60))
    draw.ellipse([cx + s + 2, cy - s // 2 - 2, cx + s + 6, cy - s // 2 + 2],
                 fill=NAVY)
    # olive sprig below
    draw.line([cx - s + 2, cy + s // 2 + 4, cx + s - 8, cy + s // 2 + 12],
              fill=(96, 150, 80), width=3)
    for dx in (0, 14, 28):
        draw.ellipse([cx - s + 4 + dx, cy + s // 2 + 8 - 3,
                      cx - s + 12 + dx, cy + s // 2 + 8 + 3],
                     fill=(96, 150, 80))


def probe_and_rock(draw, cx, cy, s):
    """Space probe approaching a grey asteroid."""
    rock = [(cx - s - 26, cy - 8), (cx - s + 4, cy - s + 8),
            (cx - s + 34, cy - s + 26), (cx - s + 30, cy + 6),
            (cx - s + 2, cy + s - 14), (cx - s - 28, cy + s - 26)]
    draw.polygon(rock, fill=(120, 124, 132), outline=(70, 74, 84))
    draw.ellipse([cx - s + 2, cy - s + 30, cx - s + 14, cy - s + 42],
                 fill=(90, 94, 102))
    # probe body + panels
    px, py = cx + s - 10, cy + 6
    draw.rectangle([px - 12, py - 12, px + 12, py + 12], fill=(230, 232, 236),
                   outline=(70, 74, 84), width=2)
    draw.rectangle([px - 44, py - 7, px - 14, py + 7], fill=(52, 96, 168))
    draw.rectangle([px + 14, py - 7, px + 44, py + 7], fill=(52, 96, 168))
    draw.arc([px - 4, py - 30, px + 22, py - 4], 200, 340,
             fill=(230, 232, 236), width=3)
    for i in range(4):
        x = cx - s + 30 + i * 22
        y = cy - s + 44 + i * 14
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=GOLD)


def flags_pair(draw, cx, cy, s):
    """India tricolour and Union Jack on two poles."""
    fw, fh = int(s * 1.15), int(s * 0.72)
    # India
    x0, y0 = cx - fw - 8, cy - fh // 2
    for i, c in enumerate(((255, 153, 51), (255, 255, 255), (19, 136, 8))):
        draw.rectangle([x0, y0 + i * fh // 3, x0 + fw, y0 + (i + 1) * fh // 3],
                       fill=c)
    draw.ellipse([x0 + fw // 2 - 7, y0 + fh // 2 - 7,
                  x0 + fw // 2 + 7, y0 + fh // 2 + 7],
                 outline=(0, 0, 128), width=2)
    draw.rectangle([x0 - 3, y0 - 16, x0 - 1, y0 + fh + 14], fill=(90, 90, 84))
    # Union Jack (simplified)
    x1 = cx + 8
    draw.rectangle([x1, y0, x1 + fw, y0 + fh], fill=(0, 36, 125))
    draw.line([x1, y0, x1 + fw, y0 + fh], fill=(255, 255, 255), width=5)
    draw.line([x1 + fw, y0, x1, y0 + fh], fill=(255, 255, 255), width=5)
    draw.line([x1 + fw // 2, y0, x1 + fw // 2, y0 + fh],
              fill=(255, 255, 255), width=8)
    draw.line([x1, y0 + fh // 2, x1 + fw, y0 + fh // 2],
              fill=(255, 255, 255), width=8)
    draw.line([x1 + fw // 2, y0, x1 + fw // 2, y0 + fh],
              fill=(200, 16, 46), width=3)
    draw.line([x1, y0 + fh // 2, x1 + fw, y0 + fh // 2],
              fill=(200, 16, 46), width=3)
    draw.rectangle([x1 + fw + 1, y0 - 16, x1 + fw + 3, y0 + fh + 14],
                   fill=(90, 90, 84))


def card(draw, box, bg, headline, deck, icon=None, head_size=23,
         deck_size=16, head_col=(255, 255, 255), deck_col=(228, 232, 240)):
    """A coloured story card with optional icon strip on top."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill=bg)
    y = y0 + 14
    if icon is not None:
        icon(draw, (x0 + x1) // 2, y + 34)
        y += 78
    y = draw_wrapped(draw, x0 + 16, y, headline, font(head_size, bold=True),
                     head_col, x1 - x0 - 32, leading=head_size + 6)
    draw_wrapped(draw, x0 + 16, y + 6, deck, font(deck_size),
                 deck_col, x1 - x0 - 32, leading=deck_size + 5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=(60, 58, 50), width=3)

    # ---- masthead ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((28, 22), "THE WORLD IN ONE DAY",
           font=font(44, serif=True), fill=(255, 255, 255))
    d.text((W - 28, 18), "FRIDAY", font=font(20, bold=True),
           fill=GOLD, anchor="ra")
    d.text((W - 28, 46), "20 NOVEMBER 2026", font=font(26, bold=True),
           fill=(255, 255, 255), anchor="ra")
    d.rectangle([0, 104, W, 108], fill=RED)
    d.text((28, 116), "FRIDAY, 20 NOVEMBER 2026  •  TWELVE STORIES FROM AROUND THE WORLD",
           font=font(17, bold=True), fill=INK)
    d.text((W - 28, 116), "make.fun", font=font(17, bold=True),
           fill=GREY, anchor="ra")

    # ---- lead hero: White House + 2027 calendar ----
    hx0, hy0, hx1, hy1 = 24, 148, 648, 440
    vgrad(d, (hx0, hy0, hx1, hy1), (196, 222, 240), (243, 226, 196))
    d.ellipse([hx1 - 120, hy0 + 18, hx1 - 66, hy0 + 72], fill=(252, 240, 190))
    draw_white_house(d, hx0 + 56, hy0 + 66, 400, 226)
    draw_calendar(d, hx1 - 236, hy1 - 168, 200, 148)
    # caption bar under the hero
    d.rectangle([hx0, hy1, hx1, 556], fill=NAVY)
    y = draw_wrapped(d, hx0 + 18, hy1 + 14,
                     "TRUMP PUSHES IRAN CALL TO 2027",
                     font(26, bold=True), (255, 255, 255), hx1 - hx0 - 36,
                     leading=32)
    draw_wrapped(d, hx0 + 18, y + 6,
                 "President says he will \u201csee what happens\u201d after "
                 "January 1 \u2014 no rush on the Gulf call.",
                 font(16), (210, 218, 232), hx1 - hx0 - 36, leading=21)

    # ---- right rail: GTA VI + Cyclone Akvan ----
    card(d, (664, 148, 1000, 348), (43, 35, 80),
         "GTA VI: $2.36BN IN ONE DAY",
         "Sensor Tower: 24.6m copies sold \u2014 the biggest debut ever.",
         icon=lambda dr, cx, cy: gamepad(dr, cx, cy, 46))
    card(d, (664, 360, 1000, 556), (14, 107, 122),
         "CYCLONE AKVAN SLAMS ODISHA",
         "Landfall near Gopalpur at noon; 3 lakh evacuated, 423 teams out.",
         icon=lambda dr, cx, cy: cyclone_spiral(dr, cx, cy, 40))

    # ---- middle row: three cards ----
    card(d, (24, 572, 344, 786), (58, 74, 96),
         "EUROPE READY TO TALK TO RUSSIA",
         "Leaders say they are ready for negotiations to end the war in "
         "Ukraine.",
         icon=lambda dr, cx, cy: dove(dr, cx, cy, 30))
    card(d, (352, 572, 672, 786), (16, 24, 40),
         "HAYABUSA2 DROPS ASTEROID LANDING",
         "Engine trouble forces Japan\u2019s probe to abandon its touchdown "
         "plan.",
         icon=lambda dr, cx, cy: probe_and_rock(dr, cx, cy, 30))
    card(d, (680, 572, 1000, 786), (122, 72, 24),
         "MODI MEETS WILLIAM AND KATE",
         "PM hosts the Prince and Princess of Wales in New Delhi; talks on "
         "India\u2013UK ties.",
         icon=lambda dr, cx, cy: flags_pair(dr, cx, cy, 34))

    # ---- In Brief panel ----
    d.rounded_rectangle([24, 802, 1000, 982], radius=12,
                        fill=(255, 255, 255), outline=LIGHT_LINE, width=2)
    d.text((44, 814), "IN BRIEF", font=font(20, bold=True), fill=RED)
    d.line([44, 842, 980, 842], fill=LIGHT_LINE, width=2)
    briefs = [
        ("CRICKET", "Nicholls 113* as New Zealand reach 243/5 on day one "
         "against India in Wellington."),
        ("CINCINNATI", "Fiona the hippo dies at the zoo after swallowing "
         "a hat."),
        ("SENEGAL", "Dozens missing after a migrant boat sinks off the "
         "coast."),
        ("MARKETS", "Sensex up 1.21% and Nifty up 1.14% in a strong rally."),
        ("AI", "Anthropic\u2019s valuation reportedly reaches $1.5 trillion."),
        ("DEFENCE", "India signs a Rs 1,976-crore deal with Israel "
         "Aerospace Industries."),
    ]
    col_w, row_h = 468, 44
    for i, (tag, text) in enumerate(briefs):
        cx = 44 + (i % 2) * (col_w + 8)
        cy = 854 + (i // 2) * row_h
        d.ellipse([cx, cy + 4, cx + 9, cy + 13], fill=RED)
        draw_wrapped(d, cx + 16, cy, tag + " \u2014 " + text, font(15),
                     INK, col_w - 16, leading=19)

    # ---- footer ----
    d.text((28, 992),
           "All stories first reported Friday 20 November 2026  •  Sources: "
           "Reuters, BBC, Sensor Tower, IMD, Space.com, ANI",
           font=font(13), fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
