#!/usr/bin/env python3
"""Front pages summing up the world news of Thursday 19 November 2026.

One file, six candidate layouts (A-F) of the same 50 stories, all events
that happened or were first reported on 19 Nov 2026 (ANT's Nasdaq debut,
the Shenzhen trilateral, GTA VI's launch, the Kerch bridge, Voyager 1's
one-light-day mark, and 44 more across 5 continents and 7 fields).

Render:  python3 draw.py <A|B|C|D|E|F|ALL> [out.png]
ALL writes out_A.png .. out_F.png. Every layout is 1024x1024, PIL only,
no network, deterministic: the same command always writes the same bytes.
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24

# ---- palette (chosen for newsprint: warm paper, dark ink, one red) ----
PAPER = (246, 242, 230)
CARD = (253, 251, 245)
INK = (22, 22, 24)
RED = (178, 32, 32)
NAVY = (26, 60, 96)
TEAL = (12, 104, 96)
GOLD = (170, 120, 20)
GREY = (96, 94, 86)
FAINT = (202, 196, 180)
SEA = (44, 92, 128)
LANDDOT = (38, 74, 110)
SKY = (232, 164, 92)
SKY2 = (244, 196, 120)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, path, size, width):
    """Largest font size <= size at which text fits width (min 8)."""
    s = size
    while s > 8 and d.textlength(text, font=font(path, s)) > width:
        s -= 1
    return font(path, s)


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                        width=width)


# ---- dotted world map: land cells as (row, col_start, col_end) runs ----
# Grid is 72 cols (5 deg lon each, -180..180) by 36 rows (5 deg lat each).
LAND = {
    1: [(26, 30), (39, 41)],
    2: [(10, 22), (25, 31), (39, 40), (44, 46), (50, 54)],
    3: [(2, 8), (10, 24), (27, 29), (38, 42), (44, 66)],
    4: [(2, 9), (10, 26), (33, 33), (37, 43), (44, 68)],
    5: [(4, 9), (10, 27), (34, 35), (37, 41), (42, 69)],
    6: [(10, 28), (34, 35), (36, 40), (41, 69), (67, 68)],
    7: [(8, 26), (33, 43), (44, 62), (67, 67)],
    8: [(7, 27), (33, 44), (45, 60), (64, 65)],
    9: [(7, 27), (33, 45), (46, 62), (63, 64)],
    10: [(8, 26), (33, 46), (46, 50), (52, 62), (63, 63)],
    11: [(6, 14), (34, 46), (47, 51), (53, 57), (57, 62)],
    12: [(5, 12), (34, 47), (48, 51), (53, 57), (58, 62)],
    13: [(5, 11), (34, 48), (54, 56), (58, 61)],
    14: [(6, 10), (34, 38), (44, 49), (58, 61), (62, 63)],
    15: [(7, 10), (35, 38), (44, 48), (55, 55), (59, 61)],
    16: [(8, 12), (12, 17), (35, 37), (44, 47), (59, 64)],
    17: [(10, 18), (36, 46), (59, 66), (66, 68)],
    18: [(10, 18), (36, 46), (60, 67)],
    19: [(10, 18), (37, 45), (61, 66)],
    20: [(11, 18), (37, 45), (62, 67)],
    21: [(11, 18), (38, 44), (47, 48), (60, 68)],
    22: [(11, 17), (38, 44), (47, 47), (60, 68)],
    23: [(11, 16), (38, 43), (60, 68)],
    24: [(12, 15), (38, 42), (61, 67), (69, 70)],
    25: [(12, 14), (62, 66), (69, 69)],
    26: [(12, 14), (64, 65), (69, 69)],
    27: [(12, 13)],
    28: [(12, 12)],
}


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
    return x, y


# ---- the day's 50 stories: (num, region, field, headline, subline, lon, lat)
STORIES = [
    (1, "ASIA", "politics", "TRUMP IN CHINA FOR TRILATERAL",
     "Shakes hands with Xi and Putin ahead of historic talks", 114.1, 22.5),
    (2, "TECH", "tech", "ANTHROPIC DEBUTS AS ANT",
     "Claude maker prices IPO at $83; Nasdaq debut today", -122.4, 37.8),
    (3, "TECH", "culture", "GTA VI ARRIVES AT LAST",
     "Launches after 13 years to rave reviews", -3.2, 55.9),
    (4, "EUROPE", "war", "KERCH BRIDGE PARTLY COLLAPSES",
     "New video shows blasts before the span falls", 34.5, 45.3),
    (5, "TECH", "tech", "VOYAGER 1 ONE LIGHT-DAY OUT",
     "NASA confirms the record distance", -118.1, 34.1),
    (6, "AMERICAS", "politics", "JEFFRIES PICKED FOR SPEAKER",
     "First Black Speaker if elected", -77.0, 38.9),
    (7, "MIDEAST", "war", "ISRAEL GROUND RAID IN GAZA",
     "Rare op beyond the Yellow Line", 34.5, 31.5),
    (8, "MIDEAST", "politics", "KAHANA IS KNESSET SPEAKER",
     "Matan Kahana voted in as speaker", 35.2, 31.8),
    (9, "TECH", "tech", "WAYMO OFF US FREEWAYS",
     "Pulled after California ban", -122.4, 37.8),
    (10, "ASIA", "weather", "CYCLONE AKVAN NEARS LAND",
     "May cross Machilipatnam-Puri", 88.0, 19.0),
    (11, "AMERICAS", "markets", "WALL ST SPLIT ON FED MINUTES",
     "Dow -561, S&P falls 5th day", -74.0, 40.7),
    (12, "AMERICAS", "tech", "KRESS PROMISES PAY RISES",
     "Interim chief's first all-hands", -121.9, 37.3),
    (13, "ASIA", "markets", "INDIA HITS SCOTCH WITH 162% DUTY",
     "Bulk imports taxed amid pact row", 77.2, 28.6),
    (14, "WORLD", "culture", "PEW: ISLAM LARGEST BY 2035",
     "On track to pass Christianity, study", 0.0, 20.0),
    (15, "AMERICAS", "politics", "TRUMP CYBERCRIME PROJECT",
     "New plan to combat cybercrime", -77.0, 38.9),
    (16, "EUROPE", "politics", "EU SPEEDS GREEN PERMITS",
     "Parliament and Council agree faster", 4.35, 50.85),
    (17, "ASIA", "politics", "INDIA-JAPAN 2+2 TALKS",
     "Defence, security ties are key", 139.7, 35.7),
    (18, "EUROPE", "culture", "WILLIAM & KATE PRAISE INDIA",
     "Royals hail 'enduring' UK-India ties", -0.12, 51.5),
    (19, "ASIA", "politics", "SC CONTEMPT CASE OPENS",
     "Top court acts over remarks against", 77.2, 28.6),
    (20, "ASIA", "politics", "SHINDE SENA PROTEST BACKFIRES",
     "Photo row erupts at rally", 72.8, 19.1),
    (21, "AMERICAS", "politics", "CONGRESS PROBES TECH OUTAGES",
     "Lawmakers demand answers", -77.0, 38.9),
    (22, "ASIA", "sport", "INDIA WIN TOSS, BOWL FIRST",
     "First Test vs New Zealand opens", 77.2, 28.6),
    (23, "ASIA", "sport", "LYTTON'S WORLD RECORD",
     "Eight dismissals in a Test innings", 90.4, 23.8),
    (24, "ASIA", "sport", "HARYANA DOMINATE TAMIL NADU",
     "Big win in Syed Mushtaq Ali Trophy", 77.2, 28.6),
    (25, "AMERICAS", "tech", "NASA'S NUCLEAR SHIP TO MARS",
     "Nuclear ship, three helicopters", -118.1, 34.1),
    (26, "WORLD", "tech", "JUPITER PLANET VANISHES",
     "Giant planet vanishes unseen", 0.0, 20.0),
    (27, "ASIA", "tech", "MOTHS READ MAGNETIC FIELD",
     "Bogong moths navigate by the stars", 149.1, -35.3),
    (28, "WORLD", "tech", "BLACK HOLES FROM FAILED STARS",
     "Failed blasts birth black holes", 0.0, 20.0),
    (29, "WORLD", "tech", "EARTH'S LOST BILLION YEARS",
     "Scientists may have found why", 0.0, 20.0),
    (30, "ASIA", "markets", "AUSSIE PAY GAP BELOW 20%",
     "Gender pay gap falls under a fifth", 151.2, -33.9),
    (31, "WORLD", "politics", "REFUGEE INTAKE WARNING",
     "Plan to all but end intake criticised", 0.0, 20.0),
    (32, "EUROPE", "culture", "PATTINSON'S $100M BOND",
     "Star set to earn nine figures for 007", -0.12, 51.5),
    (33, "AMERICAS", "culture", "HUNGER GAMES FAN, 13",
     "Fan art to screen before the film", -74.0, 40.7),
    (34, "ASIA", "culture", "RANVEER REUNITES WITH DHAR",
     "Actor to team with director again", 72.8, 19.1),
    (35, "AMERICAS", "tech", "IPHONE 20 PRO LEAKS",
     "Curved titanium, foldable tipped", -122.0, 37.3),
    (36, "AMERICAS", "sport", "WORLD BOXING MEETS IN PANAMA",
     "Board gathers ahead of vote", -79.5, 8.98),
    (37, "AMERICAS", "culture", "GTA VI CHEAPER IN REAL TERMS",
     "Price below past versions after", -3.2, 55.9),
    (38, "WORLD", "tech", "OUTAGES 'TIED TO AI UPDATES'",
     "Experts blame AI updates", 0.0, 20.0),
    (39, "ASIA", "sport", "AKASH DEEP'S SECOND ACT",
     "The making of a second innings", 88.4, 22.6),
    (40, "EUROPE", "culture", "GTA: BORN OF BRITAIN",
     "NYT on the game's British roots", -3.2, 55.9),
    (41, "ASIA", "politics", "NSW BACKS HUMAN RIGHTS ACT",
     "Inquiry finds overwhelming support", 151.2, -33.9),
    (42, "EUROPE", "culture", "IGLESIAS FACES COURT PROBE",
     "Singer faces probe over allegations", -3.7, 40.4),
    (43, "EUROPE", "politics", "SPAIN VOTES IN 10 DAYS",
     "Conservatives lead polls", -3.7, 40.4),
    (44, "ASIA", "culture", "EUROVISION HEADS TO ASIA",
     "Song contest comes to Bangkok", 100.5, 13.75),
    (45, "AMERICAS", "markets", "GOLD SLIDES ON FED MINUTES",
     "Gold slides as Fed stays put", -74.0, 40.7),
    (46, "ASIA", "politics", "CASEY HOSPITAL MENTAL HEALTH WIN",
     "Labor pledges $56m for 100 beds", 145.3, -38.1),
    (47, "ASIA", "politics", "PARRAMATTA ROAD SHAKE-UP",
     "Sydney plans hundreds of homes", 151.0, -33.8),
    (48, "ASIA", "politics", "CRITICAL MINERALS HEARINGS",
     "Evidence heard in Naracoorte", 140.7, -36.95),
    (49, "MIDEAST", "sport", "ABU DHABI T10: EE VS YL",
     "27th match of the T10 league", 54.4, 24.45),
    (50, "EUROPE", "culture", "GTA 'END OF AN ERA'",
     "Launch may mark end of an era", -0.12, 51.5),
]

# The 12 stories that also get a picture (vignette band, layout B).
VIGNETTES = [(2, "ant"), (3, "gta"), (4, "bridge"), (5, "voyager"),
              (6, "capitol"), (7, "raid"), (9, "waymo"), (10, "akvan"),
              (11, "wallst"), (12, "chip"), (22, "cricket"), (45, "gold")]

REGION_COLOR = {"ASIA": TEAL, "AMERICAS": NAVY, "EUROPE": RED,
                "MIDEAST": (122, 74, 18), "TECH": NAVY, "WORLD": GREY}


def story(num):
    return STORIES[num - 1]


# ---- small pictograms: one per vignette kind, drawn from primitives ----
def pictogram(d, kind, box):
    """Draw a tiny scene for `kind` inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "ant":
        d.rectangle(box, fill=(16, 24, 40))
        d.text((x0 + w * 0.42, y0 + 2), "ANT", font=font(FB, 13),
               fill=(110, 220, 130))
        pts = [(x0 + 4, y1 - 8), (x0 + w * 0.3, y1 - h * 0.55),
               (x0 + w * 0.55, y1 - h * 0.4), (x1 - 4, y0 + 6)]
        d.line(pts, fill=(110, 220, 130), width=2)
        d.ellipse([x1 - 9, y0 + 1, x1 + 1, y0 + 11], fill=(110, 220, 130))
        d.text((x0 + 4, y1 - 16), "$83", font=font(FB, 11), fill=(255, 255, 255))
    elif kind == "gta":
        d.rectangle(box, fill=(238, 150, 190))
        d.rectangle([x0, y1 - h * 0.42, x1, y1], fill=(40, 30, 60))
        for bx, bh in [(0.06, 0.55), (0.28, 0.75), (0.52, 0.6), (0.74, 0.85)]:
            d.rectangle([x0 + w * bx, y1 - h * bh, x0 + w * (bx + 0.18),
                         y1 - h * 0.42], fill=(20, 16, 40))
        d.ellipse([x1 - w * 0.3, y0 + 3, x1 - w * 0.08, y0 + h * 0.28],
                  fill=(255, 220, 120))
        d.line([(x0 + w * 0.55, y0 + h * 0.3), (x0 + w * 0.75, y0 + h * 0.05),
                (x0 + w * 0.72, y0 + h * 0.28)], fill=(30, 90, 40), width=2)
    elif kind == "bridge":
        d.rectangle(box, fill=(190, 220, 235))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(90, 140, 170))
        d.arc([x0 + w * 0.1, y0 + h * 0.25, x1 - w * 0.1, y1 - h * 0.05],
              180, 360, fill=(60, 60, 60), width=3)
        d.line([(x0 + w * 0.1, y1 - h * 0.3), (x1 - w * 0.1, y1 - h * 0.3)],
               fill=(60, 60, 60), width=3)
        for t in range(8):
            a = math.pi * t / 7
            sx = cx + math.cos(a) * w * 0.32
            sy = cy - math.sin(a) * h * 0.22
            d.line([(sx, sy), (sx, sy + 5)], fill=(255, 140, 40), width=2)
        d.ellipse([cx - 6, cy - h * 0.3, cx + 6, cy - h * 0.3 + 12],
                  fill=(255, 120, 30))
    elif kind == "voyager":
        d.rectangle(box, fill=(10, 14, 34))
        for sx, sy, r in [(0.2, 0.25, 1), (0.7, 0.15, 1), (0.85, 0.5, 1),
                          (0.35, 0.6, 1), (0.55, 0.35, 2)]:
            d.ellipse([x0 + w * sx - r, y0 + h * sy - r,
                       x0 + w * sx + r, y0 + h * sy + r], fill=(255, 255, 255))
        d.line([(x0 + w * 0.15, y1 - h * 0.2), (x0 + w * 0.75, y0 + h * 0.25)],
               fill=(200, 200, 210), width=2)
        d.ellipse([x0 + w * 0.68, y0 + h * 0.12, x0 + w * 0.88, y0 + h * 0.38],
                  outline=(220, 220, 230), width=2)
        d.polygon([(x0 + w * 0.15, y1 - h * 0.2), (x0 + w * 0.3, y1 - h * 0.2),
                   (x0 + w * 0.2, y1 - h * 0.35)], fill=(180, 180, 190))
        d.text((x0 + 4, y1 - 14), "1 LIGHT-DAY", font=font(FB, 9),
               fill=(150, 200, 255))
    elif kind == "capitol":
        d.rectangle(box, fill=(220, 230, 240))
        d.rectangle([x0 + w * 0.15, y1 - h * 0.35, x1 - w * 0.15, y1 - h * 0.25],
                    fill=(240, 240, 240))
        d.pieslice([cx - w * 0.2, y0 + h * 0.1, cx + w * 0.2, y0 + h * 0.55],
                   180, 360, fill=(250, 250, 250))
        d.rectangle([cx - 2, y0 + h * 0.05, cx + 2, y0 + h * 0.15],
                    fill=(120, 120, 120))
        for i in range(4):
            px = x0 + w * (0.22 + i * 0.18)
            d.rectangle([px, y1 - h * 0.25, px + 4, y1 - h * 0.05],
                        fill=(200, 200, 200))
        d.rectangle([x0 + w * 0.1, y1 - h * 0.08, x1 - w * 0.1, y1 - h * 0.02],
                    fill=(180, 180, 180))
    elif kind == "raid":
        d.rectangle(box, fill=(60, 70, 60))
        d.rectangle([x0 + w * 0.1, y1 - h * 0.5, x0 + w * 0.45, y1 - h * 0.2],
                    fill=(30, 30, 30))
        d.rectangle([x0 + w * 0.6, y1 - h * 0.65, x0 + w * 0.9, y1 - h * 0.2],
                    fill=(40, 40, 40))
        d.polygon([(x0 + w * 0.62, y0 + h * 0.2), (x1 - 2, y0 + h * 0.05),
                   (x1 - 2, y0 + h * 0.35)], fill=(255, 240, 160))
        d.text((x0 + 4, y1 - 14), "GAZA", font=font(FB, 10),
               fill=(255, 255, 255))
    elif kind == "waymo":
        d.rectangle(box, fill=(200, 225, 240))
        d.rounded_rectangle([x0 + w * 0.12, y0 + h * 0.42, x1 - w * 0.12,
                             y1 - h * 0.25], radius=6, fill=(30, 90, 160))
        d.rounded_rectangle([x0 + w * 0.25, y0 + h * 0.2, x1 - w * 0.25,
                             y0 + h * 0.45], radius=4, fill=(120, 190, 230))
        d.ellipse([x0 + w * 0.22, y1 - h * 0.3, x0 + w * 0.32, y1 - h * 0.18],
                  fill=(20, 20, 20))
        d.ellipse([x0 + w * 0.68, y1 - h * 0.3, x0 + w * 0.78, y1 - h * 0.18],
                  fill=(20, 20, 20))
        d.ellipse([x1 - w * 0.3, y0 + 2, x1 - 2, y0 + h * 0.32],
                  outline=RED, width=2)
        d.line([(x1 - w * 0.27, y0 + h * 0.06), (x1 - w * 0.05, y0 + h * 0.26)],
               fill=RED, width=2)
    elif kind == "akvan":
        d.rectangle(box, fill=(170, 210, 225))
        for r in range(2, 16, 2):
            a0 = r * 0.9
            d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
                  a0 * 57, a0 * 57 + 200, fill=(255, 255, 255), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 120, 60))
    elif kind == "wallst":
        d.rectangle(box, fill=(240, 238, 228))
        for i, bh in enumerate([0.5, 0.65, 0.42, 0.72, 0.35]):
            bx = x0 + w * (0.08 + i * 0.18)
            d.rectangle([bx, y1 - h * bh, bx + w * 0.12, y1 - h * 0.12],
                        fill=(120, 120, 110) if i < 4 else RED)
        d.line([(x0 + 3, y0 + h * 0.2), (x1 - 4, y1 - h * 0.25)],
               fill=RED, width=2)
        d.polygon([(x1 - 4, y1 - h * 0.25), (x1 - 12, y1 - h * 0.25),
                   (x1 - 4, y1 - h * 0.35)], fill=RED)
    elif kind == "chip":
        d.rectangle(box, fill=(30, 40, 30))
        d.rectangle([cx - w * 0.22, cy - h * 0.25, cx + w * 0.22,
                     cy + h * 0.25], fill=(40, 120, 70))
        d.rectangle([cx - w * 0.1, cy - h * 0.12, cx + w * 0.1,
                     cy + h * 0.12], fill=(140, 220, 160))
        for i in range(3):
            for yy in (cy - h * 0.25, cy + h * 0.25):
                px = cx + (i - 1) * w * 0.16
                d.line([(px, yy), (px, yy + (6 if yy < cy else -6))],
                       fill=(200, 200, 200), width=2)
    elif kind == "cricket":
        d.rectangle(box, fill=(120, 170, 90))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(90, 140, 70))
        for sx in (0.3, 0.42, 0.54):
            d.line([(x0 + w * sx, y1 - h * 0.3), (x0 + w * sx, y1 - h * 0.5)],
                   fill=(240, 220, 120), width=2)
        d.line([(x0 + w * 0.68, y0 + h * 0.15), (x0 + w * 0.85, y1 - h * 0.35)],
               fill=(190, 140, 90), width=4)
        d.ellipse([x0 + w * 0.12, y0 + h * 0.2, x0 + w * 0.24, y0 + h * 0.35],
                  fill=RED)
    elif kind == "gold":
        d.rectangle(box, fill=(250, 244, 220))
        for i in range(3):
            bx = x0 + w * (0.14 + i * 0.28)
            d.polygon([(bx, y1 - h * 0.3), (bx + w * 0.08, y1 - h * 0.48),
                       (bx + w * 0.2, y1 - h * 0.48), (bx + w * 0.28,
                                                        y1 - h * 0.3)],
                      fill=(212, 175, 55))
        d.line([(x0 + w * 0.7, y0 + h * 0.15), (x0 + w * 0.7, y1 - h * 0.15)],
               fill=RED, width=3)
        d.polygon([(x0 + w * 0.7, y1 - h * 0.15), (x0 + w * 0.58, y1 - h * 0.3),
                   (x0 + w * 0.82, y1 - h * 0.3)], fill=RED)


# ---- hero scenes ----
def scene_shenzhen(d, box):
    """Sunset skyline with a jet: Trump in China for the trilateral."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(SKY[0] + (SKY2[0] - SKY[0]) * t)
        g = int(SKY[1] + (SKY2[1] - SKY[1]) * t)
        b = int(SKY[2] + (SKY2[2] - SKY[2]) * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    d.ellipse([x1 - w * 0.28, y0 + h * 0.1, x1 - w * 0.1, y0 + h * 0.32],
              fill=(255, 214, 130))
    d.polygon([(x0 + w * 0.1, y0 + h * 0.22), (x0 + w * 0.3, y0 + h * 0.18),
               (x0 + w * 0.26, y0 + h * 0.28)], fill=(30, 30, 40))
    d.polygon([(x0 + w * 0.28, y0 + h * 0.2), (x0 + w * 0.34, y0 + h * 0.16),
               (x0 + w * 0.33, y0 + h * 0.26)], fill=(30, 30, 40))
    base = y1 - h * 0.28
    towers = [(0.02, 0.30, 0.10), (0.14, 0.42, 0.09), (0.25, 0.60, 0.08),
              (0.35, 0.34, 0.10), (0.47, 0.68, 0.09), (0.58, 0.5, 0.09),
              (0.69, 0.38, 0.09), (0.8, 0.55, 0.09), (0.9, 0.32, 0.08)]
    for fx, fh, fw in towers:
        d.rectangle([x0 + w * fx, base - h * fh, x0 + w * (fx + fw), base],
                    fill=(35, 35, 55))
    d.polygon([(x0 + w * 0.47, base - h * 0.68), (x0 + w * 0.51, y0 + 8),
               (x0 + w * 0.55, base - h * 0.68)], fill=(35, 35, 55))
    for wx in range(6):
        d.rectangle([x0 + w * (0.05 + wx * 0.15), base - h * 0.06,
                     x0 + w * (0.09 + wx * 0.15), base - h * 0.02],
                    fill=(255, 220, 110))
    d.rectangle([x0, base, x1, y1], fill=(25, 25, 40))
    d.rectangle([x0, y1 - h * 0.24, x1, y1], fill=(12, 12, 16))
    d.text((x0 + 12, y1 - h * 0.22), "TRUMP IN CHINA FOR TRILATERAL",
           font=fit(d, "TRUMP IN CHINA FOR TRILATERAL", FSB, 21, w - 24),
           fill=(255, 255, 255))
    d.text((x0 + 12, y1 - h * 0.11),
           "Shakes hands with Xi and Putin ahead of talks",
           font=fit(d, "Shakes hands with Xi and Putin ahead of talks",
                    FSR, 13, w - 24), fill=(240, 210, 130))


def scene_bridge(d, box):
    """The Kerch bridge: arch, sea, blast."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(186, 214, 232))
    d.rectangle([x0, y1 - h * 0.32, x1, y1], fill=(88, 138, 168))
    d.arc([x0 + w * 0.08, y0 + h * 0.2, x1 - w * 0.08, y1 - h * 0.05],
          180, 360, fill=(52, 52, 52), width=4)
    d.line([(x0 + w * 0.08, y1 - h * 0.32), (x1 - w * 0.08, y1 - h * 0.32)],
           fill=(52, 52, 52), width=4)
    d.line([(x0 + w * 0.5, y0 + h * 0.2), (x0 + w * 0.5, y1 - h * 0.32)],
           fill=(52, 52, 52), width=3)
    for t in range(10):
        a = math.pi * t / 9
        sx = (x0 + x1) / 2 + math.cos(a) * w * 0.36
        sy = y0 + h * 0.62 - math.sin(a) * h * 0.32
        d.line([(sx, sy), (sx, sy + 6)], fill=(255, 130, 30), width=2)
    d.ellipse([(x0 + x1) / 2 - 10, y0 + h * 0.12, (x0 + x1) / 2 + 10,
               y0 + h * 0.12 + 20], fill=(255, 120, 30))
    d.rectangle([x0, y1 - h * 0.24, x1, y1], fill=(12, 12, 16))
    d.text((x0 + 12, y1 - h * 0.22), "KERCH BRIDGE PARTLY COLLAPSES",
           font=fit(d, "KERCH BRIDGE PARTLY COLLAPSES", FSB, 21, w - 24),
           fill=(255, 255, 255))
    d.text((x0 + 12, y1 - h * 0.11),
           "New video shows blasts before the span falls",
           font=fit(d, "New video shows blasts before the span falls",
                    FSR, 13, w - 24), fill=(240, 210, 130))


# ---- page furniture ----
def masthead(d, y=14):
    d.text((MARGIN, y), "THURSDAY 19 NOVEMBER 2026",
           font=font(FSB, 44), fill=INK)
    d.text((MARGIN, y + 52),
           "THE WORLD IN ONE PICTURE  ·  50 STORIES  ·  13 ILLUSTRATED  ·  "
           "5 CONTINENTS",
           font=font(FB, 15), fill=RED)
    d.line([(MARGIN, y + 78), (W - MARGIN, y + 78)], fill=INK, width=3)
    return y + 86


def footer(d, text=None):
    y = H - 26
    d.line([(MARGIN, y - 6), (W - MARGIN, y - 6)], fill=INK, width=2)
    msg = text or ("Sum up 19 November's world news  ·  as reported on "
                   "Thursday 19 November 2026  ·  make.fun news-image-20261119")
    d.text((W / 2, y + 2), msg, font=font(FR, 11), fill=GREY, anchor="ma")


def draw_map(d, box, numbered=True):
    """Dotted continents with a pin per story; heroes get numbered pins."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD, outline=FAINT)
    cw = (x1 - x0) / 72.0
    ch = (y1 - y0) / 36.0
    rr = max(1.0, min(cw, ch) * 0.32)
    for row, runs in LAND.items():
        for c0, c1 in runs:
            for c in range(c0, c1 + 1):
                px = x0 + (c + 0.5) * cw
                py = y0 + (row + 0.5) * ch
                d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=LANDDOT)
    for num, _rg, _fd, _h, _s, lon, lat in STORIES:
        px, py = lonlat_to_xy(lon, lat, box)
        if numbered and num <= 6:
            d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                      outline=(255, 255, 255), width=1)
            d.text((px, py - 1), str(num), font=font(FB, 9),
                   fill=(255, 255, 255), anchor="mm")
        else:
            d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=RED)


def hero_cards(d, box, nums, headline_size=13):
    """Row of hero story cards: tag, headline, subline."""
    x0, y0, x1, y1 = box
    n = len(nums)
    gap = 8
    cw = (x1 - x0 - gap * (n - 1)) / n
    for i, num in enumerate(nums):
        _, region, _fd, head, sub, _lon, _lat = story(num)
        cx0 = x0 + i * (cw + gap)
        cx1 = cx0 + cw
        d.rectangle([cx0, y0, cx1, y1], fill=CARD, outline=FAINT)
        d.rectangle([cx0, y0, cx1, y0 + 3], fill=REGION_COLOR.get(region, GREY))
        d.text((cx0 + 7, y0 + 8), f"{num}. {region}",
               font=font(FB, 10), fill=REGION_COLOR.get(region, GREY))
        hl = wrap(d, head, font(FB, headline_size), cw - 14)
        yy = y0 + 24
        for line in hl[:2]:
            d.text((cx0 + 7, yy), line, font=font(FB, headline_size), fill=INK)
            yy += headline_size + 3
        sl = wrap(d, sub, font(FR, 10), cw - 14)
        for line in sl[:2]:
            d.text((cx0 + 7, yy), line, font=font(FR, 10), fill=GREY)
            yy += 13


def story_grid(d, box, nums, cols, with_sub=True, summary=True):
    """Uniform tiles: number badge, headline, subline; optional summary cell."""
    x0, y0, x1, y1 = box
    rows = math.ceil(len(nums) / cols)
    gap = 6
    cw = (x1 - x0 - gap * (cols - 1)) / cols
    ch = (y1 - y0 - gap * (rows - 1)) / rows
    for i, num in enumerate(nums):
        r, c = divmod(i, cols)
        tx0 = x0 + c * (cw + gap)
        ty0 = y0 + r * (ch + gap)
        _, _rg, _fd, head, sub, _lon, _lat = story(num)
        d.rectangle([tx0, ty0, tx0 + cw, ty0 + ch], fill=CARD, outline=FAINT)
        d.ellipse([tx0 + 5, ty0 + 5, tx0 + 17, ty0 + 17], fill=RED)
        d.text((tx0 + 11, ty0 + 11), str(num), font=font(FB, 8),
               fill=(255, 255, 255), anchor="mm")
        hl = wrap(d, head, font(FB, 11), cw - 26)
        yy = ty0 + 4
        for line in hl[:2]:
            d.text((tx0 + 21, yy), line, font=font(FB, 11), fill=INK)
            yy += 13
        if with_sub:
            sl = wrap(d, sub, font(FR, 9), cw - 26)
            for line in sl[:1]:
                d.text((tx0 + 21, yy), line, font=font(FR, 9), fill=GREY)
                yy += 11
    if summary:
        r, c = divmod(len(nums), cols)
        tx0 = x0 + c * (cw + gap)
        ty0 = y0 + r * (ch + gap)
        d.rectangle([tx0, ty0, tx0 + cw, ty0 + ch], fill=INK)
        d.text((tx0 + 8, ty0 + 6), "THE DAY IN NUMBERS",
               font=font(FB, 10), fill=(240, 210, 130))
        d.text((tx0 + 8, ty0 + 22), "50 stories · 13 illustrated",
               font=font(FR, 9), fill=(255, 255, 255))
        d.text((tx0 + 8, ty0 + 34), "5 continents · 7 fields · 19 Nov",
               font=font(FR, 9), fill=(255, 255, 255))


def vignette_band(d, box):
    """Two rows of six pictograms, each labelled with its story number."""
    x0, y0, x1, y1 = box
    cols, rows = 6, 2
    gap = 6
    cw = (x1 - x0 - gap * (cols - 1)) / cols
    ch = (y1 - y0 - gap * (rows - 1)) / rows
    for i, (num, kind) in enumerate(VIGNETTES):
        r, c = divmod(i, cols)
        vx0 = x0 + c * (cw + gap)
        vy0 = y0 + r * (ch + gap)
        vx1, vy1 = vx0 + cw, vy0 + ch
        pictogram(d, kind, (vx0, vy0, vx1, vy1 - 14))
        d.rectangle([vx0, vy1 - 14, vx1, vy1], fill=INK)
        _, _rg, _fd, head, _s, _lo, _la = story(num)
        short = {"ANTHROPIC DEBUTS AS ANT": "ANT",
                 "GTA VI ARRIVES AT LAST": "GTA VI",
                 "KERCH BRIDGE PARTLY COLLAPSES": "KERCH",
                 "VOYAGER 1 ONE LIGHT-DAY OUT": "VOYAGER 1",
                 "JEFFRIES PICKED FOR SPEAKER": "JEFFRIES",
                 "ISRAEL GROUND RAID IN GAZA": "GAZA RAID",
                 "WAYMO OFF US FREEWAYS": "WAYMO",
                 "CYCLONE AKVAN NEARS LAND": "AKVAN",
                 "WALL ST SPLIT ON FED MINUTES": "WALL ST",
                 "KRESS PROMISES PAY RISES": "NVIDIA",
                 "INDIA WIN TOSS, BOWL FIRST": "IND VS NZ",
                 "GOLD SLIDES ON FED MINUTES": "GOLD"}.get(head, head)
        d.text((vx0 + 4, vy1 - 13), short,
               font=fit(d, short, FB, 9, cw - 8), fill=(255, 255, 255))
        d.ellipse([vx0 + 2, vy0 + 2, vx0 + 16, vy0 + 16], fill=RED)
        d.text((vx0 + 9, vy0 + 9), str(num), font=font(FB, 8),
               fill=(255, 255, 255), anchor="mm")


# ---- the six candidate layouts ----
def blank():
    im = Image.new("RGB", (W, H), PAPER)
    return im, ImageDraw.Draw(im)


def layout_a(d):
    """Front page: map + 6 hero cards + 44-tile grid."""
    y = masthead(d)
    draw_map(d, (MARGIN, y, W - MARGIN, y + 210))
    hero_cards(d, (MARGIN, y + 218, W - MARGIN, y + 330), [1, 2, 3, 4, 5, 6])
    story_grid(d, (MARGIN, y + 338, W - MARGIN, H - 34),
               list(range(7, 51)), cols=5)
    footer(d)


def layout_b(d):
    """Hero scene + 12 vignettes + map + hero cards + grid. The pick."""
    y = masthead(d)
    scene_shenzhen(d, (MARGIN, y, 500, y + 196))
    vignette_band(d, (508, y, W - MARGIN, y + 196))
    draw_map(d, (MARGIN, y + 204, W - MARGIN, y + 318))
    hero_cards(d, (MARGIN, y + 326, W - MARGIN, y + 440), [1, 2, 3, 4, 5, 6])
    story_grid(d, (MARGIN, y + 448, W - MARGIN, H - 34),
               list(range(7, 51)), cols=5)
    footer(d)


def layout_c(d):
    """Newspaper, three columns: lead block + map + 44-item list."""
    y = masthead(d)
    scene_shenzhen(d, (MARGIN, y, 470, y + 260))
    draw_map(d, (478, y, W - MARGIN, y + 260))
    hero_cards(d, (MARGIN, y + 268, W - MARGIN, y + 380), [1, 2, 3, 4, 5, 6])
    story_grid(d, (MARGIN, y + 388, W - MARGIN, H - 34),
               list(range(7, 51)), cols=4, with_sub=False, summary=False)
    footer(d)


def layout_d(d):
    """Timeline strip + map + 50 equal tiles, no hierarchy."""
    y = masthead(d)
    d.rectangle([MARGIN, y, W - MARGIN, y + 44], fill=INK)
    d.text((MARGIN + 10, y + 10),
           "ASIA WAKENS  ·  TRILATERAL IN SHENZHEN  ·  GTA VI LANDS  ·  "
           "ANT DEBUTS  ·  KERCH BRIDGE FALLS",
           font=font(FB, 14), fill=(240, 210, 130))
    draw_map(d, (MARGIN, y + 52, W - MARGIN, y + 190))
    story_grid(d, (MARGIN, y + 198, W - MARGIN, H - 34),
               list(range(1, 51)), cols=5, with_sub=False, summary=False)
    footer(d)


def layout_e(d):
    """Hero scene + map + 5 hero cards + grid; only story 1 is a picture."""
    y = masthead(d)
    scene_shenzhen(d, (MARGIN, y, W - MARGIN, y + 210))
    draw_map(d, (MARGIN, y + 218, W - MARGIN, y + 336))
    hero_cards(d, (MARGIN, y + 344, W - MARGIN, y + 452), [2, 3, 4, 5, 6])
    story_grid(d, (MARGIN, y + 460, W - MARGIN, H - 34),
               list(range(7, 51)), cols=5)
    footer(d)


def layout_f(d):
    """Tabloid: two scenes + map strip + grid."""
    y = masthead(d)
    scene_shenzhen(d, (MARGIN, y, 500, y + 190))
    scene_bridge(d, (508, y, W - MARGIN, y + 190))
    draw_map(d, (MARGIN, y + 198, W - MARGIN, y + 282))
    story_grid(d, (MARGIN, y + 290, W - MARGIN, H - 34),
               list(range(1, 51)), cols=5, summary=False)
    footer(d)


LAYOUTS = {"A": layout_a, "B": layout_b, "C": layout_c,
           "D": layout_d, "E": layout_e, "F": layout_f}


def render(which):
    im, d = blank()
    LAYOUTS[which](d)
    return im


def main(argv):
    if len(argv) < 2 or argv[1] not in list(LAYOUTS) + ["ALL"]:
        print("usage: draw.py <A|B|C|D|E|F|ALL> [out.png]")
        return 2
    which = argv[1]
    out = argv[2] if len(argv) > 2 else None
    if which == "ALL":
        for name in "ABCDEF":
            path = out.replace(".png", f"_{name}.png") if out else f"out_{name}.png"
            render(name).save(path)
            print(f"{name}: {path}")
        return 0
    im = render(which)
    path = out or "entry.png"
    im.save(path)
    print(f"{which}: {path} ({W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
