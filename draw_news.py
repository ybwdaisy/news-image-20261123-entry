#!/usr/bin/env python3
"""Render the 23 November 2026 world-news image (1024x1024 PNG).

Fresh layout written for this entry: masthead, one lead story, a 2x2 grid,
a briefs strip and a sources footer. All facts come from NEWS.md in this repo.
Run: python3 draw_news.py  ->  writes entry.png beside this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (25, 25, 25)
NAVY = (22, 38, 79)
RED = (158, 27, 30)
GRAY = (90, 90, 90)
RULE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap on pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            if draw.textlength(cur + " " + w, font=fnt) <= max_w:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_block(draw, x, y, max_w, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # side margin
    cw = W - 2 * mx  # content width

    # ---- Masthead: navy band with date ----
    band_h = 118
    d.rectangle([0, 0, W, band_h], fill=NAVY)
    f_small = font(SANS_B, 21)
    f_date = font(SERIF_B, 52)
    small = "T H E   W O R L D   I N   O N E   I M A G E"
    tw = d.textlength(small, font=f_small)
    d.text(((W - tw) / 2, 16), small, font=f_small, fill=(255, 255, 255))
    date = "MONDAY \u00b7 23 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 48), date, font=f_date, fill=(255, 255, 255))
    d.rectangle([0, band_h, W, band_h + 5], fill=RED)

    y = band_h + 26

    # ---- Lead story ----
    f_kick = font(SANS_B, 20)
    d.text((mx, y), "CLIMATE", font=f_kick, fill=RED)
    y += 30
    f_lead = font(SERIF_B, 66)
    d.text((mx, y), "COP31 COLLAPSES", font=f_lead, fill=INK)
    y += 82
    f_deck = font(SANS, 24)
    deck = (
        "After the longest talks in history, the climate summit ends with "
        "no deal \u2014 the EU rejects a pact that never mentions fossil fuels. "
        "The first breakdown since Copenhagen 2009."
    )
    lines = wrap(d, deck, f_deck, cw)
    assert len(lines) <= 3, f"lead deck overflow: {lines}"
    y = draw_block(d, mx, y, cw, lines, f_deck, INK, 32)
    y += 10
    d.line([mx, y, W - mx, y], fill=RULE, width=2)
    y += 16

    # ---- 2x2 grid ----
    stories = [
        ("HORMUZ", RED, "Three tankers hit in the strait",
         "Attacks hit their highest level since the war began; "
         "two supertankers said hit by mines."),
        ("UKRAINE", NAVY, "14 missing after drone hits flats",
         "A Russian drone flattened part of a five-storey block in Dymer. "
         "Nine were evacuated; rescuers search the rubble."),
        ("NVIDIA", NAVY, "US spy probe widens",
         "Washington is probing alleged spy Alice Huang; her associate "
         "is accused of smuggling Nvidia chips to China."),
        ("INDONESIA", NAVY, "3 dead, 36 missing in factory fire",
         "A blaze swept a candy factory in Banten with about 300 workers "
         "inside. Fifteen were rescued alive."),
    ]
    gap = 24
    cell_w = (cw - gap) // 2
    f_grid_kick = font(SANS_B, 18)
    f_grid_head = font(SERIF_B, 29)
    f_grid_body = font(SANS, 20)
    grid_top = y
    row_h = 0
    for i, (kick, color, head, body) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = mx + col * (cell_w + gap)
        cy = grid_top + row * 196
        d.text((x, cy), kick, font=f_grid_kick, fill=color)
        hlines = wrap(d, head, f_grid_head, cell_w)
        assert len(hlines) <= 2, f"grid headline overflow: {hlines}"
        by = draw_block(d, x, cy + 28, cell_w, hlines, f_grid_head, INK, 36)
        blines = wrap(d, body, f_grid_body, cell_w)
        assert len(blines) <= 3, f"grid body overflow: {blines}"
        draw_block(d, x, by + 6, cell_w, blines, f_grid_body, (60, 60, 60), 27)
        if col == 0:
            d.line([x + cell_w + gap // 2, cy, x + cell_w + gap // 2,
                    cy + 178], fill=RULE, width=1)
    y = grid_top + 2 * 196 + 6
    d.line([mx, y, W - mx, y], fill=RULE, width=2)
    y += 16

    # ---- Briefs strip ----
    f_brief_head = font(SANS_B, 20)
    d.text((mx, y), "ALSO TODAY", font=f_brief_head, fill=RED)
    y += 30
    f_brief = font(SANS, 19)
    briefs = [
        "UN talks on lethal AI weapons to continue.",
        "Modi and Nepal's PM meet in Delhi; Tata Steel sells tubes unit for 28,000 crore rupees.",
        "Thousands march in Lisbon over living costs.",
        "Bahrain takes Iran's attack to the UN Security Council.",
        "Verstappen wins in Las Vegas; Pant hits 128 in Wellington.",
    ]
    for b in briefs:
        blines = wrap(d, "\u2022  " + b, f_brief, cw)
        assert len(blines) <= 2, f"brief overflow: {blines}"
        y = draw_block(d, mx, y, cw, blines, f_brief, INK, 25)
        y += 3

    # ---- Footer: sources ----
    y += 8
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    y += 10
    f_src = font(SANS, 16)
    src = "Sources: CNN \u00b7 Reuters \u00b7 WSJ \u00b7 Al Jazeera \u00b7 AP \u00b7 Japan Times \u2014 morning of 23 Nov 2026"
    slines = wrap(d, src, f_src, cw)
    draw_block(d, mx, y, cw, slines, f_src, GRAY, 22)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
