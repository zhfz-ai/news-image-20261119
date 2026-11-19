#!/usr/bin/env python3
"""Draw candidate front pages summing up the world news of Thursday
19 November 2026, for make.fun news-image-20261119.

50 stories, all first reported on 19 November 2026 (Reuters, AP, BBC,
Al Jazeera, The Guardian, The Hindu, NDTV, Cricinfo, Kitco, and the
19 Nov wire digests). 13 illustrated: one hero scene (Trump in
Shenzhen for the APEC trilateral) plus 12 drawn vignettes for the
day's other biggest stories. Every story is pinned on the world map;
every hero and grid subline is complete, with no ellipsis anywhere.

Render: python3 draw.py <layout> <out.png>   (layouts A..F)
All layouts are 1024x1024 PNG, PIL only, no network, deterministic.
"""
import math
import random
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (31, 78, 121)
TEAL = (14, 110, 105)
GOLD = (176, 124, 18)
GREY = (90, 88, 80)
LIGHT = (233, 228, 213)
WHITE = (252, 250, 244)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# (num, region, category, headline, subline, lon, lat)
# Heroes 1-6 get numbered map pins; every other story gets a dot.
STORIES = [
    (1, "ASIA", "politics", "TRUMP IN CHINA FOR TRILATERAL",
     "Shakes hands with Xi and Putin ahead of historic talks", 114.1, 22.5),
    (2, "TECH", "tech", "ANTHROPIC DEBUTS AS ANT",
     "Claude maker prices IPO at $83; Nasdaq debut today", -122.4, 37.8),
    (3, "TECH", "culture", "GTA VI ARRIVES AT LAST",
     "Launches after 13 years to rave reviews",
     -3.2, 55.9),
    (4, "EUROPE", "war", "KERCH BRIDGE PARTLY COLLAPSES",
     "New video shows blasts before the span falls", 34.5, 45.3),
    (5, "TECH", "tech", "VOYAGER 1 ONE LIGHT-DAY OUT",
     "NASA confirms the record distance", -118.1, 34.1),
    (6, "AMERICAS", "politics", "JEFFRIES PICKED FOR SPEAKER",
     "First Black Speaker if elected", -77.0, 38.9),
    (7, "MIDEAST", "war", "ISRAEL GROUND RAID IN GAZA",
     "Rare operation beyond the Yellow Line", 34.5, 31.5),
    (8, "MIDEAST", "politics", "KAHANA IS KNESSET SPEAKER",
     "Matan Kahana voted in as speaker", 35.2, 31.8),
    (9, "TECH", "tech", "WAYMO OFF US FREEWAYS",
     "Driverless taxis pulled after California ban", -122.4, 37.8),
    (10, "ASIA", "weather", "CYCLONE AKVAN NEARS LAND",
     "Likely to cross Machilipatnam-Puri", 88.0, 19.0),
    (11, "MARKETS", "markets", "WALL ST SPLIT ON FED MINUTES",
     "Dow -561, S&P falls 5th day, Nasdaq rises", -74.0, 40.7),
    (12, "TECH", "tech", "KRESS PROMISES PAY RISES",
     "Nvidia interim chief's first all-hands: hikes for 49,000",
     -121.9, 37.4),
    (13, "ASIA", "markets", "INDIA HITS SCOTCH WITH 162% DUTY",
     "Bulk imports taxed amid UK pact row", 77.2, 28.6),
    (14, "AMERICAS", "culture", "PEW: ISLAM LARGEST BY 2035",
     "On track to pass Christianity, study finds", -77.0, 38.9),
    (15, "AMERICAS", "politics", "TRUMP CYBERCRIME PROJECT",
     "Administration unveils plan to combat cybercrime", -77.0, 38.9),
    (16, "EUROPE", "politics", "EU SPEEDS GREEN PERMITS",
     "Parliament and Council agree faster grid approvals", 4.35, 50.85),
    (17, "ASIA", "politics", "INDIA-JAPAN 2+2 TALKS",
     "Jaishankar: defence, security ties key", 139.7, 35.7),
    (18, "EUROPE", "culture", "WILLIAM & KATE PRAISE INDIA",
     "Royals hail 'enduring' UK-India ties with Modi", 77.2, 28.6),
    (19, "ASIA", "politics", "SC CONTEMPT CASE OPENS",
     "Top court acts over remarks against Chief Justice", 77.2, 28.6),
    (20, "ASIA", "politics", "SHINDE SENA PROTEST BACKFIRES",
     "Bal Thackeray photo torn in Sonia book row", 72.9, 19.1),
    (21, "AMERICAS", "tech", "CONGRESS PROBES TECH OUTAGES",
     "Lawmakers seek answers after outages", -77.0, 38.9),
    (22, "SPORT", "sport", "INDIA WIN TOSS, BOWL FIRST",
     "First Test against New Zealand opens", 174.8, -41.3),
    (23, "SPORT", "sport", "LITTON'S WORLD RECORD",
     "Eight dismissals in a Test innings", 90.4, 23.8),
    (24, "SPORT", "sport", "HARYANA DOMINATE TAMIL NADU",
     "SMAT: Bihar upset Delhi in high-scoring thriller", 77.2, 28.6),
    (25, "TECH", "tech", "NASA'S NUCLEAR SHIP TO MARS",
     "Spacecraft with three helicopters due late 2028", -118.1, 34.1),
    (26, "TECH", "tech", "JUPITER PLANET VANISHES",
     "Giant world gone; unseen neighbour blamed", -155.5, 19.8),
    (27, "TECH", "tech", "MOTHS READ MAGNETIC FIELD",
     "Bogong moths navigate by geomagnetic compass", 149.1, -35.3),
    (28, "TECH", "tech", "BLACK HOLES FROM FAILED STARS",
     "Failed explosions may birth black holes", -118.1, 34.1),
    (29, "TECH", "tech", "EARTH'S LOST BILLION YEARS",
     "Scientists may have found why a billion years is missing",
     -74.0, 40.7),
    (30, "ASIA", "politics", "AUSSIE PAY GAP BELOW 20%",
     "Gender pay gap falls under a fifth for first time", 151.2, -33.9),
    (31, "ASIA", "politics", "REFUGEE INTAKE WARNING",
     "Plan to all but end intake 'denies thousands a pathway'",
     151.2, -33.9),
    (32, "EUROPE", "culture", "PATTINSON'S $100M BOND",
     "Star set to earn nine figures for 007 saga", -0.1, 51.5),
    (33, "EUROPE", "culture", "HUNGER GAMES FAN, 13",
     "Artwork to screen before film in cinemas", -0.1, 51.5),
    (34, "ASIA", "culture", "RANVEER REUNITES WITH DHAR",
     "Actor to team with director again", 72.9, 19.1),
    (35, "TECH", "tech", "IPHONE 20 PRO LEAKS",
     "Curved titanium, cautious foldable sequel tipped", -122.0, 37.3),
    (36, "AMERICAS", "sport", "WORLD BOXING MEETS IN PANAMA",
     "Executive board gathers ahead of 2026 congress", -79.5, 9.0),
    (37, "TECH", "culture", "GTA VI CHEAPER IN REAL TERMS",
     "Price below past versions after inflation", -3.2, 55.9),
    (38, "AMERICAS", "tech", "OUTAGES 'TIED TO AI UPDATES'",
     "Tech experts link recent outages to AI rollouts", -84.5, 39.1),
    (39, "SPORT", "sport", "AKASH DEEP'S SECOND ACT",
     "The making of a second innings", 77.2, 28.6),
    (40, "TECH", "culture", "GTA: BORN IN BRITAIN",
     "NYT on the game's British roots", -3.2, 55.9),
    (41, "ASIA", "politics", "NSW BACKS HUMAN RIGHTS ACT",
     "Inquiry finds overwhelming support for state act", 151.2, -33.9),
    (42, "EUROPE", "culture", "IGLESIAS FACES COURT PROBE",
     "Julio Iglesias investigated over alleged sex offences", -3.7, 40.4),
    (43, "EUROPE", "politics", "SPAIN VOTES IN 10 DAYS",
     "Conservatives lead polls after eight years of Socialist rule",
     -3.7, 40.4),
    (44, "ASIA", "culture", "EUROVISION HEADS TO ASIA",
     "Song contest comes to Bangkok on Saturday", 100.5, 13.75),
    (45, "MARKETS", "markets", "GOLD SLIDES ON FED MINUTES",
     "Gold under pressure as Fed stays hawkish", -74.0, 40.7),
    (46, "ASIA", "politics", "CASEY HOSPITAL MENTAL HEALTH WIN",
     "Labor pledges $6m plan for 100-bed unit", 145.0, -37.8),
    (47, "ASIA", "markets", "PARRAMATTA ROAD SHAKE-UP",
     "Sydney plans hundreds of homes and jobs", 151.2, -33.9),
    (48, "ASIA", "politics", "CRITICAL MINERALS HEARINGS",
     "Inquiry hears evidence in Naracoorte and Port Pirie", 138.6, -34.9),
    (49, "AMERICAS", "sport", "ABU DHABI T10: EE VS YL",
     "27th match of the T10 league", 54.4, 24.5),
    (50, "TECH", "culture", "GTA 'END OF AN ERA'",
     "Economist: launch may mark the end of an era in gaming",
     -0.1, 51.5),
]

CAT_COLOR = {
    "war": (178, 34, 34), "politics": (31, 78, 121), "tech": (14, 110, 105),
    "markets": (120, 90, 10), "weather": (70, 110, 160), "sport": (90, 110, 30),
    "culture": (140, 70, 130),
}
REGION_COLOR = {
    "ASIA": (178, 34, 34), "EUROPE": (31, 78, 121), "MIDEAST": (120, 90, 10),
    "AMERICAS": (14, 110, 105), "TECH": (70, 70, 90), "MARKETS": (120, 90, 10),
    "SPORT": (90, 110, 30),
}

# Illustrated stories: hero scene (story 1) + 12 vignettes.
# (story num, vignette key, short label shown under the vignette)
VIGNETTES = [
    (2, "ticker", "ANT DEBUTS"),
    (3, "gta", "GTA VI"),
    (4, "bridge", "KERCH BRIDGE"),
    (5, "voyager", "VOYAGER 1"),
    (6, "capitol", "JEFFRIES"),
    (7, "strike", "GAZA RAID"),
    (9, "car", "WAYMO"),
    (10, "cyclone", "AKVAN"),
    (11, "chart", "WALL ST"),
    (12, "chip", "NVIDIA"),
    (22, "cricket", "IND VS NZ"),
    (45, "gold", "GOLD SLUMPS"),
]

# ------------------------------------------------------------- world map
# Simplified continent outlines as (lon, lat) polygons.
NA = [(-168, 66), (-156, 71), (-140, 70), (-128, 71), (-115, 73), (-100, 74),
      (-90, 74), (-85, 70), (-82, 66), (-78, 62), (-72, 62), (-65, 60),
      (-60, 55), (-55, 52), (-59, 47), (-65, 44), (-70, 42), (-74, 39),
      (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-94, 29),
      (-97, 26), (-102, 23), (-105, 20), (-100, 18), (-95, 16), (-90, 14),
      (-86, 13), (-83, 9), (-79, 9), (-82, 13), (-87, 13), (-92, 15),
      (-96, 16), (-101, 18), (-105, 20), (-110, 22), (-114, 27), (-117, 32),
      (-122, 37), (-124, 42), (-124, 48), (-128, 52), (-134, 57), (-141, 60),
      (-148, 61), (-155, 58), (-162, 58), (-166, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-54, 68), (-50, 71), (-42, 75), (-32, 76), (-22, 74),
             (-20, 70), (-25, 68), (-32, 66), (-40, 64), (-48, 61), (-54, 60),
             (-58, 64)]
SA = [(-80, 9), (-77, 5), (-75, 1), (-78, -3), (-81, -6), (-80, -10),
      (-77, -14), (-75, -18), (-70, -20), (-70, -25), (-70, -30), (-72, -35),
      (-73, -40), (-73, -45), (-71, -50), (-69, -54), (-66, -55), (-68, -52),
      (-66, -48), (-64, -42), (-60, -38), (-57, -34), (-53, -33), (-49, -28),
      (-45, -24), (-41, -22), (-38, -16), (-35, -9), (-35, -6), (-38, -4),
      (-42, -2), (-45, -1), (-50, 0), (-52, 3), (-55, 6), (-59, 8),
      (-63, 10), (-68, 11), (-72, 12), (-76, 10), (-80, 9)]
AFRICA = [(-17, 15), (-16, 20), (-12, 25), (-10, 30), (-6, 34), (-1, 35),
          (3, 37), (9, 37), (11, 34), (15, 32), (20, 32), (25, 31), (30, 31),
          (33, 28), (35, 24), (37, 20), (39, 16), (41, 12), (44, 11),
          (48, 11), (51, 11), (48, 6), (45, 2), (42, -2), (40, -6),
          (39, -11), (37, -16), (35, -20), (33, -25), (30, -29), (27, -33),
          (22, -34), (18, -33), (16, -28), (14, -22), (12, -17), (13, -12),
          (12, -7), (9, -1), (9, 4), (5, 4), (-2, 5), (-8, 5), (-12, 8),
          (-16, 12), (-17, 15)]
MADAG = [(44, -16), (48, -17), (50, -20), (47, -24), (44, -25), (43, -21),
         (44, -16)]
EURASIA = [(-10, 36), (-9, 39), (-9, 43), (-4, 44), (-2, 46), (-4, 48),
           (-1, 49), (1, 51), (3, 52), (6, 53), (8, 55), (10, 57), (8, 59),
           (5, 60), (6, 62), (10, 64), (13, 66), (16, 68), (20, 69),
           (25, 70), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69),
           (55, 69), (60, 69), (65, 69), (70, 72), (75, 73), (80, 73),
           (85, 74), (90, 75), (95, 76), (100, 77), (105, 77), (110, 76),
           (115, 74), (120, 73), (125, 72), (130, 72), (135, 72), (140, 72),
           (145, 72), (150, 70), (155, 70), (160, 69), (165, 67), (170, 67),
           (175, 66), (178, 65), (178, 62), (172, 60), (168, 60), (162, 58),
           (158, 53), (156, 51), (152, 55), (148, 59), (143, 59), (141, 55),
           (140, 50), (138, 46), (135, 44), (132, 43), (130, 42), (128, 39),
           (126, 38), (124, 38), (121, 35), (120, 32), (122, 29), (120, 26),
           (117, 24), (114, 22), (110, 20), (108, 18), (106, 14), (105, 10),
           (103, 7), (101, 6), (99, 8), (98, 12), (96, 15), (94, 17),
           (92, 20), (90, 22), (88, 22), (86, 20), (84, 19), (82, 17),
           (80, 14), (78, 9), (77, 8), (75, 11), (73, 16), (72, 20),
           (70, 21), (68, 23), (66, 25), (61, 25), (57, 26), (54, 26),
           (52, 25), (50, 28), (48, 29), (44, 32), (40, 33), (36, 36),
           (33, 36), (30, 36), (27, 37), (23, 36), (19, 40),
           (16, 38), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37),
           (-6, 36), (-10, 36)]
ARABIA = [(48, 29), (52, 26), (55, 24), (59, 22), (58, 20), (55, 17),
          (52, 15), (48, 14), (44, 13), (42, 15), (39, 18), (37, 22),
          (36, 26), (38, 28), (40, 29), (43, 29), (45, 29), (48, 29)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-2, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 36), (141, 39),
         (141, 42), (143, 44), (145, 44), (142, 42), (140, 39), (138, 36),
         (135, 34), (132, 33), (130, 31)]
SUMATRA = [(95, 5), (100, 0), (104, -3), (106, -6), (104, -6), (100, -2),
           (96, 2), (95, 5)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -2), (113, -3),
          (110, -2), (109, 1)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -7)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (141, -8), (136, -8),
             (132, -4), (131, -1)]
PHIL = [(120, 18), (122, 16), (122, 14), (120, 13), (121, 11), (122, 10),
        (124, 11), (126, 10), (126, 7), (124, 6), (122, 7), (120, 10),
        (120, 14), (120, 18)]
NZ = [(167, -45), (170, -42), (174, -39), (176, -38), (178, -37),
      (175, -40), (172, -43), (168, -46), (167, -45)]
AUS = [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
       (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
       (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
       (140, -17), (136, -15), (135, -12), (132, -12), (130, -13), (126, -14),
       (122, -17), (118, -20), (114, -22)]
CUBA = [(-85, 22), (-80, 23), (-75, 20), (-74, 20), (-78, 21), (-83, 22),
        (-85, 22)]
ICELAND = [(-22, 64), (-18, 66), (-14, 64), (-18, 63), (-22, 64)]
LAND = [NA, GREENLAND, SA, AFRICA, MADAG, EURASIA, ARABIA, UK, JAPAN,
        SUMATRA, BORNEO, JAVA, NEWGUINEA, PHIL, NZ, AUS, CUBA, ICELAND]


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(point_in_poly(lon, lat, p) for p in LAND)

# ------------------------------------------------------------ drawing kit
def masthead(d, y=0, h=88, big=48, sub=None):
    d.rectangle([0, y, W, y + h], fill=PAPER)
    title = "THURSDAY 19 NOVEMBER 2026"
    size = big
    while size > 30:
        f_date = font(FSB, size)
        if d.textlength(title, font=f_date) <= W - 48:
            break
        size -= 2
    f_sub = font(FR, 20)
    tw = d.textlength(title, font=f_date)
    d.text(((W - tw) / 2, y + 6), title, font=f_date, fill=INK)
    if sub is None:
        sub = ("THE WORLD IN ONE PICTURE  \u00b7  50 STORIES  \u00b7  "
               "5 CONTINENTS  \u00b7  ONE DAY")
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, y + h - 30), sub, font=f_sub, fill=RED)
    d.line([(24, y + h - 4), (W - 24, y + h - 4)], fill=INK, width=3)
    d.line([(24, y + h + 1), (W - 24, y + h + 1)], fill=INK, width=1)
    return y + h


def footer(d, y=1004):
    f = font(FR, 14)
    txt = ("Sum up 19 November's world news  \u00b7  as reported on Thursday "
           "19 November 2026  \u00b7  make.fun news-image-20261119")
    tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, y), txt, font=f, fill=GREY)


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (85.0 - lat) / 170.0 * (y1 - y0)
    return x, y


def draw_map(d, box, dot=7, pin_r=13, label_pins=True, pin_scale=1.0):
    """Dot-grid world map; numbered red pins for the 6 hero stories and a
    small red dot for every other story (duplicate coords get a small
    deterministic offset so stacked stories stay visible)."""
    x0, y0, x1, y1 = box
    step = dot + 3
    gx = x0 + step / 2
    while gx < x1:
        lon = -180 + (gx - x0) / (x1 - x0) * 360.0
        gy = y0 + step / 2
        while gy < y1:
            lat = 85 - (gy - y0) / (y1 - y0) * 170.0
            if on_land(lon, lat):
                r = dot / 2
                d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=BLUE)
            gy += step
        gx += step
    d.rectangle([x0, y0, x1, y1], outline=(180, 175, 160), width=1)
    # small dots for the non-hero stories, jittered on duplicate coords
    _jitter = [(0, 0), (8, 0), (-8, 0), (0, 8), (0, -8), (8, 8), (-8, -8),
               (8, -8)]
    _seen = {}
    for (num, region, cat, head, sub, plon, plat) in STORIES[6:]:
        key = (plon, plat)
        k = _seen.get(key, 0)
        _seen[key] = k + 1
        dx, dy = _jitter[k % len(_jitter)]
        px, py = lonlat_to_xy(plon, plat, box)
        r = 5
        d.ellipse([px + dx - r, py + dy - r, px + dx + r, py + dy + r],
                  fill=RED, outline=WHITE, width=1)
    # Pins 1 (Shenzhen) and 4 (Kerch) sit far apart; pin 5 (Pasadena) and
    # pin 2 (San Francisco) sit close: nudge 2 with a leader line.
    PIN_DXDY = {2: (16, -12)}
    if label_pins:
        f_pin = font(FB, int(15 * pin_scale))
        for (num, region, cat, head, sub, plon, plat) in STORIES[:6]:
            px, py = lonlat_to_xy(plon, plat, box)
            dx, dy = PIN_DXDY.get(num, (0, 0))
            qx, qy = px + dx, py + dy
            if (dx, dy) != (0, 0):
                d.line([(px, py), (qx, qy)], fill=RED, width=2)
            r = pin_r * pin_scale
            d.ellipse([qx - r, qy - r, qx + r, qy + r], fill=RED,
                      outline=WHITE, width=2)
            tw = d.textlength(str(num), font=f_pin)
            d.text((qx - tw / 2, qy - r + 2), str(num), font=f_pin, fill=WHITE)


def icon(d, cx, cy, r, cat):
    """Small pictogram in a coloured disc."""
    col = CAT_COLOR[cat]
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    w = (255, 255, 255)
    if cat == "war":  # explosion burst
        for a in range(8):
            ang = a * math.pi / 4
            x2 = cx + r * 0.62 * math.cos(ang)
            y2 = cy + r * 0.62 * math.sin(ang)
            d.line([(cx, cy), (x2, y2)], fill=w, width=3)
        d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
                  fill=w)
    elif cat == "politics":  # flag
        d.line([(cx - r * 0.3, cy + r * 0.55), (cx - r * 0.3, cy - r * 0.55)],
               fill=w, width=3)
        d.polygon([(cx - r * 0.3, cy - r * 0.55), (cx + r * 0.55, cy - r * 0.3),
                   (cx - r * 0.3, cy - r * 0.05)], fill=w)
    elif cat == "tech":  # chip
        d.rectangle([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4],
                    outline=w, width=3)
        d.rectangle([cx - r * 0.15, cy - r * 0.15, cx + r * 0.15, cy + r * 0.15],
                    fill=w)
        for dx in (-r * 0.4, 0, r * 0.4):
            d.line([(cx + dx, cy - r * 0.7), (cx + dx, cy - r * 0.4)], fill=w, width=2)
            d.line([(cx + dx, cy + r * 0.4), (cx + dx, cy + r * 0.7)], fill=w, width=2)
    elif cat == "markets":  # bars
        for i, h in enumerate((0.35, 0.6, 0.85)):
            bx = cx - r * 0.55 + i * r * 0.5
            d.rectangle([bx, cy + r * 0.5 - r * h, bx + r * 0.32, cy + r * 0.5],
                        fill=w)
    elif cat == "weather":  # cyclone spiral
        pts = []
        for t in range(0, 300, 12):
            a = t * math.pi / 180 * 1.6
            rr = r * 0.12 + r * 0.55 * t / 300
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.line(pts, fill=w, width=3)
    elif cat == "sport":  # ball
        d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5],
                  outline=w, width=2)
        d.polygon([(cx, cy - r * 0.25), (cx + r * 0.25, cy + r * 0.1),
                   (cx, cy + r * 0.35), (cx - r * 0.25, cy + r * 0.1)], fill=w)
    else:  # culture: star
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r * 0.6 if i % 2 == 0 else r * 0.25
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=w)


def hero_card(d, s, x0, y0, x1, y1, head_size=21, sub_size=14):
    num, region, cat, head, sub, lon, lat = s
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(200, 195, 180), width=1)
    d.rectangle([x0, y0, x0 + 5, y1], fill=CAT_COLOR[cat])
    if (y1 - y0) < 110:
        # compact horizontal card: icon at left, head to its right, sub below
        icon(d, x0 + 24, y0 + 21, 15, cat)
        f_n = font(FB, 13)
        d.text((x0 + 46, y0 + 5), f"{num}. {region}", font=f_n,
               fill=CAT_COLOR[cat])
        f_h = font(FB, head_size - 2)
        lines = wrap(d, head, f_h, (x1 - x0) - 56)
        yy = y0 + 23
        for ln in lines[:2]:
            if yy + head_size - 2 > y1 - 2:
                break
            d.text((x0 + 46, yy), ln, font=f_h, fill=INK)
            yy += head_size
        f_s = font(FR, sub_size)
        for ln in wrap(d, sub, f_s, (x1 - x0) - 20)[:2]:
            if yy + sub_size <= y1 - 4:
                d.text((x0 + 10, yy), ln, font=f_s, fill=(70, 68, 62))
                yy += sub_size + 2
        return
    icon(d, x0 + 24, y0 + 21, 14, cat)
    f_n = font(FB, 15)
    d.text((x0 + 44, y0 + 10), f"{num}. {region}", font=f_n, fill=CAT_COLOR[cat])
    f_h = font(FB, head_size)
    lines = wrap(d, head, f_h, (x1 - x0) - 20)
    yy = y0 + 42
    for ln in lines[:2]:
        if yy + head_size > y1 - sub_size - 6:
            break
        d.text((x0 + 10, yy), ln, font=f_h, fill=INK)
        yy += head_size + 3
    f_s = font(FR, sub_size)
    for ln in wrap(d, sub, f_s, (x1 - x0) - 20)[:2]:
        if yy + sub_size <= y1 - 4:
            d.text((x0 + 10, yy), ln, font=f_s, fill=(70, 68, 62))
            yy += sub_size + 2


def grid_tile(d, s, x0, y0, x1, y1, head_size=11, sub_size=9, show_sub=True):
    """Compact tile: number + headline share the top lines (headline wraps
    to at most 2 lines), then the subline (up to 2 lines). Fits a ~43px
    tile with headline and sub both complete."""
    num, region, cat, head, sub, lon, lat = s
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(205, 200, 185), width=1)
    icon(d, x0 + 11, y0 + 10, 8, cat)
    f_n = font(FB, 10)
    d.text((x0 + 22, y0 + 3), str(num), font=f_n, fill=CAT_COLOR[cat])
    f_h = font(FB, head_size)
    lines = wrap(d, head, f_h, (x1 - x0) - 30)
    yy = y0 + 3
    for ln in lines[:2]:
        if yy + head_size > y1 - 2:
            break
        d.text((x0 + 24, yy), ln, font=f_h, fill=INK)
        yy += head_size + 2
    if show_sub:
        f_s = font(FR, sub_size)
        for ln in wrap(d, sub, f_s, (x1 - x0) - 12)[:2]:
            if yy + sub_size <= y1 - 3:
                d.text((x0 + 6, yy), ln, font=f_s, fill=(70, 68, 62))
                yy += sub_size + 1


def grid_area(d, stories, x0, y0, x1, y1, cols, rows, tile_fn=grid_tile, **kw):
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    gap = 6
    for i, s in enumerate(stories):
        r, c = divmod(i, cols)
        tx0 = x0 + c * cw + gap / 2
        ty0 = y0 + r * ch + gap / 2
        tx1 = x0 + (c + 1) * cw - gap / 2
        ty1 = y0 + (r + 1) * ch - gap / 2
        tile_fn(d, s, tx0, ty0, tx1, ty1, **kw)


def section_bar(d, y, text, color=INK):
    f = font(FB, 16)
    d.rectangle([24, y, W - 24, y + 26], fill=color)
    d.text((34, y + 4), text, font=f, fill=WHITE)
    return y + 26


def summary_cell(d, x0, y0, x1, y1):
    """Last grid cell: the day in numbers (fills the 45th cell).
    Two info lines only: the cell is ~42px tall in the tightest layout."""
    d.rectangle([x0, y0, x1, y1], fill=INK)
    f1 = font(FB, 12)
    d.text((x0 + 8, y0 + 4), "THE DAY IN NUMBERS", font=f1, fill=(255, 220, 120))
    f2 = font(FR, 10)
    d.text((x0 + 8, y0 + 19), "50 stories \u00b7 13 illustrated", font=f2, fill=WHITE)
    d.text((x0 + 8, y0 + 30), "5 continents \u00b7 7 fields \u00b7 19 Nov", font=f2,
           fill=WHITE)


def fit_font(d, path, text, start, max_w):
    """Largest font size at or below start whose text fits max_w."""
    size = start
    while size > 12:
        fnt = font(path, size)
        if d.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, 12)

# ------------------------------------------------------------- scene art
def scene_shenzhen(d, x0, y0, x1, y1):
    """Shenzhen dusk: amber sky, tower skyline, descending plane, three
    flag poles for the US-China-Russia trilateral welcome."""
    bands = [(252, 196, 120), (247, 178, 96), (238, 158, 80), (226, 138, 74)]
    bh = (y1 - y0) / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh + 1], fill=col)
    d.ellipse([x1 - 92, y0 + 14, x1 - 34, y0 + 72], fill=(250, 214, 110))
    rnd = random.Random(1911)
    # Shenzhen towers, tallest in the middle
    bx = x0 + 8
    while bx < x1 - 26:
        bw = rnd.randint(26, 46)
        bh2 = rnd.randint(56, y1 - y0 - 96)
        d.rectangle([bx, y1 - bh2, bx + bw, y1], fill=(52, 58, 86))
        for wy in range(y1 - bh2 + 8, y1 - 8, 13):
            for wx in range(bx + 5, bx + bw - 6, 11):
                if rnd.random() < 0.45:
                    d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 216, 110))
        bx += bw + 5
    # pointed landmark tower
    tx = x0 + (x1 - x0) * 0.62
    d.polygon([(tx - 16, y1), (tx, y0 + 34), (tx + 16, y1)], fill=(40, 46, 74))
    d.ellipse([tx - 4, y0 + 30, tx + 4, y0 + 38], fill=(255, 216, 110))
    # descending plane, nose down toward the runway
    px, py = x0 + (x1 - x0) * 0.30, y0 + 46
    d.polygon([(px - 52, py + 8), (px + 48, py - 14), (px + 64, py - 6),
               (px - 36, py + 16)], fill=(28, 28, 38))
    d.polygon([(px - 8, py + 4), (px + 4, py - 20), (px + 16, py + 2)],
              fill=(28, 28, 38))
    d.polygon([(px - 28, py + 12), (px - 16, py + 26), (px - 6, py + 12)],
              fill=(28, 28, 38))
    # three flag poles on the runway strip
    ry = y1 - 14
    d.rectangle([x0, ry, x1, y1], fill=(30, 30, 34))
    cols = [(178, 34, 34), (200, 40, 40), (31, 78, 121)]
    for i, col in enumerate(cols):
        fx = x0 + 30 + i * 34
        d.line([(fx, ry - 26), (fx, ry)], fill=(240, 240, 230), width=2)
        d.polygon([(fx, ry - 26), (fx + 20, ry - 21), (fx, ry - 16)], fill=col)


def scene_bridge(d, x0, y0, x1, y1):
    """Strait at dawn, arched bridge, blast over the deck."""
    d.rectangle([x0, y0, x1, y1], fill=(150, 190, 215))
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.45], fill=(235, 225, 200))
    d.ellipse([x0 + 30, y0 + 18, x0 + 90, y0 + 78], fill=(245, 200, 90))
    for i in range(5):
        yy = y0 + (y1 - y0) * (0.55 + i * 0.09)
        d.line([(x0 + 10, yy), (x1 - 10, yy)], fill=(255, 255, 255), width=2)
    # bridge deck + arch + towers
    mid = (x0 + x1) / 2
    d.line([(x0 + 8, y1 - 70), (x1 - 8, y1 - 70)], fill=(40, 40, 50), width=8)
    d.arc([mid - 170, y1 - 200, mid + 170, y1 - 40], 180, 360, fill=(40, 40, 50),
          width=8)
    for tx in (x0 + 60, mid - 12, x1 - 72):
        d.rectangle([tx, y1 - 190, tx + 12, y1 - 70], fill=(40, 40, 50))
    # blast
    cx, cy = mid + 60, y1 - 95
    for i in range(9):
        a = i * math.pi * 2 / 9
        d.line([(cx, cy), (cx + 26 * math.cos(a), cy + 26 * math.sin(a))],
               fill=(255, 120, 20), width=5)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 180, 40))


# ------------------------------------------------------------- vignettes
# Each draws one story's picture inside a small box (x0, y0, x1, y1).
def _vign_frame(d, x0, y0, x1, y1, sky):
    d.rectangle([x0, y0, x1, y1], fill=sky, outline=(200, 195, 180), width=1)


def vign_bridge(d, x0, y0, x1, y1):
    _vign_frame(d, x0, y0, x1, y1, (168, 198, 220))
    mid = (x0 + x1) / 2
    d.line([(x0 + 4, y1 - 22), (x1 - 4, y1 - 22)], fill=(40, 40, 50), width=5)
    d.arc([mid - 34, y1 - 62, mid + 34, y1 - 6], 180, 360, fill=(40, 40, 50),
          width=5)
    cx, cy = mid + 18, y1 - 32
    for i in range(8):
        a = i * math.pi / 4
        d.line([(cx, cy), (cx + 13 * math.cos(a), cy + 13 * math.sin(a))],
               fill=(255, 120, 20), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 180, 40))
    d.line([(x0 + 6, y1 - 10), (x1 - 6, y1 - 10)], fill=(255, 255, 255), width=2)


def vign_strike(d, x0, y0, x1, y1):
    _vign_frame(d, x0, y0, x1, y1, (232, 196, 140))
    # desert + ground line + burst + smoke
    d.rectangle([x0, y1 - 20, x1, y1], fill=(190, 150, 90))
    cx, cy = (x0 + x1) / 2 - 14, y1 - 34
    d.rectangle([cx - 2, y1 - 52, cx + 2, y1 - 20], fill=(60, 60, 60))
    d.ellipse([cx - 8, y1 - 58, cx + 4, y1 - 46], fill=(60, 60, 60))
    bx, by = (x0 + x1) / 2 + 16, y0 + 26
    for i in range(8):
        a = i * math.pi / 4
        d.line([(bx, by), (bx + 12 * math.cos(a), by + 12 * math.sin(a))],
               fill=(255, 90, 20), width=3)
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 170, 40))
    d.ellipse([x0 + 10, y0 + 8, x0 + 28, y0 + 22], fill=(120, 115, 105))


def vign_chip(d, x0, y0, x1, y1):
    _vign_frame(d, x0, y0, x1, y1, (24, 92, 74))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = (x1 - x0) * 0.30
    d.rectangle([cx - s, cy - s, cx + s, cy + s], outline=(255, 255, 255), width=4)
    d.rectangle([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4],
                fill=(120, 200, 60))
    for dx in (-s, 0, s):
        d.line([(cx + dx, cy - s - 10), (cx + dx, cy - s)], fill=(255, 255, 255),
               width=3)
        d.line([(cx + dx, cy + s), (cx + dx, cy + s + 10)], fill=(255, 255, 255),
               width=3)
    d.line([(x0 + 8, y1 - 14), (cx - 6, y1 - 30), (cx + 2, y1 - 22),
            (x1 - 8, y1 - 40)], fill=(255, 220, 90), width=4)


def vign_chart(d, x0, y0, x1, y1):
    _vign_frame(d, x0, y0, x1, y1, (245, 240, 226))
    d.line([(x0 + 8, y0 + 12), (x1 - 8, y0 + 12)], fill=(180, 175, 160), width=1)
    pts = [(x0 + 8, y0 + 18), (x0 + 26, y0 + 26), (x0 + 44, y0 + 22),
           (x0 + 60, y0 + 40), (x1 - 10, y0 + 52)]
    d.line(pts, fill=(178, 34, 34), width=4)
    d.polygon([(x1 - 10, y0 + 52), (x1 - 22, y0 + 50), (x1 - 12, y0 + 64)],
              fill=(178, 34, 34))
    for i, h in enumerate((14, 22, 30)):
        bx = x0 + 14 + i * 22
        d.rectangle([bx, y1 - 10 - h, bx + 12, y1 - 10], fill=(120, 90, 10))


def vign_gold(d, x0, y0, x1, y1):
    _vign_frame(d, x0, y0, x1, y1, (245, 240, 226))
    # three gold bars + falling arrow
    for i, (bx, by) in enumerate(((x0 + 10, y1 - 26), (x0 + 32, y1 - 26),
                                  (x0 + 21, y1 - 42))):
        d.polygon([(bx, by), (bx + 20, by), (bx + 17, by + 12), (bx + 3, by + 12)],
                  fill=(212, 160, 40), outline=(150, 110, 20))
    d.line([(x1 - 12, y0 + 10), (x1 - 12, y0 + 44)], fill=(178, 34, 34), width=4)
    d.polygon([(x1 - 12, y0 + 52), (x1 - 20, y0 + 40), (x1 - 4, y0 + 40)],
              fill=(178, 34, 34))


def vign_ticker(d, x0, y0, x1, y1):
    """Nasdaq ticker: dark board, ANT in green, rising line."""
    _vign_frame(d, x0, y0, x1, y1, (18, 28, 44))
    f_t = font(FB, 22)
    d.text((x0 + 8, y0 + 6), "ANT", font=f_t, fill=(120, 220, 120))
    f_p = font(FB, 13)
    d.text((x0 + 8, y0 + 32), "$83", font=f_p, fill=WHITE)
    d.line([(x0 + 8, y1 - 16), (x0 + 30, y1 - 34), (x0 + 48, y1 - 26),
            (x0 + 66, y1 - 44), (x1 - 8, y1 - 52)], fill=(120, 220, 120), width=4)
    d.polygon([(x1 - 8, y1 - 52), (x1 - 20, y1 - 50), (x1 - 10, y1 - 38)],
              fill=(120, 220, 120))


def vign_gta(d, x0, y0, x1, y1):
    """Vice-city dusk: pink-orange sky, palm silhouettes, tower skyline."""
    bands = [(255, 150, 180), (255, 120, 120), (200, 90, 140)]
    bh = (y1 - y0) / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh + 1], fill=col)
    d.ellipse([x1 - 30, y0 + 8, x1 - 8, y0 + 30], fill=(255, 230, 140))
    # towers
    for bx, bw, bh2 in ((x0 + 6, 16, 34), (x0 + 26, 20, 48), (x0 + 50, 14, 28),
                        (x0 + 68, 18, 40)):
        d.rectangle([bx, y1 - bh2, bx + bw, y1], fill=(40, 30, 60))
    # palm: trunk + fronds
    px = x0 + (x1 - x0) * 0.55
    d.line([(px, y1), (px + 4, y1 - 30)], fill=(30, 40, 30), width=3)
    for a in (-70, -30, 10, 50):
        ex = px + 4 + 16 * math.cos(a * math.pi / 180)
        ey = y1 - 30 + 10 * math.sin(a * math.pi / 180)
        d.line([(px + 4, y1 - 30), (ex, ey)], fill=(30, 60, 30), width=3)
    d.rectangle([x0, y1 - 8, x1, y1], fill=(30, 30, 40))


def vign_voyager(d, x0, y0, x1, y1):
    """Deep space: stars, the probe's dish and boom, pale blue dot."""
    _vign_frame(d, x0, y0, x1, y1, (8, 12, 30))
    rnd = random.Random(1977)
    for _ in range(14):
        sx = x0 + rnd.randint(4, int(x1 - x0) - 4)
        sy = y0 + rnd.randint(4, int(y1 - y0) - 4)
        r = rnd.choice((1, 1, 2))
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # dish
    d.arc([cx - 16, cy - 16, cx + 16, cy + 16], 200, 340, fill=(200, 200, 210),
          width=4)
    d.line([(cx, cy), (cx + 22, cy + 14)], fill=(200, 200, 210), width=3)
    d.ellipse([cx + 18, cy + 10, cx + 26, cy + 18], fill=(255, 220, 90))
    # boom + pale blue dot
    d.line([(cx - 10, cy + 4), (cx - 30, cy + 18)], fill=(160, 160, 180), width=2)
    d.ellipse([x0 + 8, y1 - 14, x0 + 14, y1 - 8], fill=(140, 180, 230))


def vign_capitol(d, x0, y0, x1, y1):
    """US Capitol: dome, columns, flag on top."""
    _vign_frame(d, x0, y0, x1, y1, (200, 214, 230))
    cx = (x0 + x1) / 2
    d.line([(cx, y0 + 6), (cx, y0 + 16)], fill=(60, 60, 60), width=2)
    d.polygon([(cx, y0 + 6), (cx + 12, y0 + 9), (cx, y0 + 12)], fill=(178, 34, 34))
    d.arc([cx - 16, y0 + 14, cx + 16, y0 + 40], 180, 360, fill=WHITE, width=3)
    d.rectangle([cx - 16, y0 + 26, cx + 16, y0 + 34], fill=WHITE)
    d.rectangle([x0 + 12, y0 + 34, x1 - 12, y0 + 40], fill=WHITE)
    for col_x in (x0 + 18, x0 + 34, x0 + 50, x1 - 34, x1 - 50, x1 - 66):
        d.rectangle([col_x, y0 + 40, col_x + 6, y1 - 12], fill=WHITE)
    d.rectangle([x0 + 10, y1 - 12, x1 - 10, y1 - 6], fill=WHITE)
    d.rectangle([x0, y1 - 6, x1, y1], fill=(90, 130, 70))


def vign_car(d, x0, y0, x1, y1):
    """Driverless car: road, car body, sensor arcs above the roof."""
    _vign_frame(d, x0, y0, x1, y1, (214, 226, 232))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(70, 70, 78))
    d.line([(x0, y1 - 9), (x1, y1 - 9)], fill=(255, 220, 90), width=2)
    cx, cy = (x0 + x1) / 2, y1 - 30
    d.polygon([(cx - 34, cy + 10), (cx - 26, cy - 8), (cx - 8, cy - 14),
               (cx + 14, cy - 14), (cx + 30, cy - 6), (cx + 34, cy + 10)],
              fill=(31, 78, 121))
    d.ellipse([cx - 24, cy + 4, cx - 12, cy + 16], fill=(20, 20, 26))
    d.ellipse([cx + 12, cy + 4, cx + 24, cy + 16], fill=(20, 20, 26))
    # lidar puck + sensor arcs
    d.rectangle([cx - 4, cy - 20, cx + 6, cy - 14], fill=(20, 20, 26))
    for r in (22, 30):
        d.arc([cx - r, cy - 14 - r, cx + r, cy - 14 + r], 180, 360,
              fill=(178, 34, 34), width=2)
    # red cross over the freeway sign
    d.line([(x1 - 22, y0 + 8), (x1 - 8, y0 + 22)], fill=(178, 34, 34), width=3)
    d.line([(x1 - 8, y0 + 8), (x1 - 22, y0 + 22)], fill=(178, 34, 34), width=3)


def vign_cyclone(d, x0, y0, x1, y1):
    """Cyclone Akvan: spiral over the Bay of Bengal coast."""
    _vign_frame(d, x0, y0, x1, y1, (180, 205, 225))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 4
    pts = []
    for t in range(0, 360, 10):
        a = t * math.pi / 180 * 1.7
        rr = 2 + 24 * t / 360
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(pts, fill=WHITE, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(70, 110, 160))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(120, 150, 110))
    d.line([(x0 + 6, y1 - 12), (x1 - 6, y1 - 12)], fill=(255, 255, 255), width=1)


def vign_cricket(d, x0, y0, x1, y1):
    """Test cricket: green outfield, bat, red ball, stumps."""
    _vign_frame(d, x0, y0, x1, y1, (110, 165, 90))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(200, 190, 150))
    # stumps
    for sx in (x0 + 12, x0 + 18, x0 + 24):
        d.line([(sx, y1 - 34), (sx, y1 - 16)], fill=(240, 220, 140), width=3)
    # bat
    d.polygon([(x1 - 30, y0 + 12), (x1 - 22, y0 + 10), (x1 - 18, y0 + 34),
               (x1 - 26, y0 + 36)], fill=(210, 170, 110))
    d.line([(x1 - 26, y0 + 12), (x1 - 30, y0 + 2)], fill=(120, 80, 40), width=3)
    # red ball
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(178, 34, 34),
              outline=WHITE, width=2)
    d.arc([cx - 9, cy - 9, cx + 9, cy + 9], 20, 160, fill=WHITE, width=1)


VIGNETTE_FNS = {
    "bridge": vign_bridge, "strike": vign_strike, "chip": vign_chip,
    "chart": vign_chart, "gold": vign_gold, "ticker": vign_ticker,
    "gta": vign_gta, "voyager": vign_voyager, "capitol": vign_capitol,
    "car": vign_car, "cyclone": vign_cyclone, "cricket": vign_cricket,
}


def vignette_band(d, x0, y0, x1, y1):
    """12 vignettes in 6 columns x 2 rows, each with a short label."""
    cols, rows = 6, 2
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    gap = 6
    f_l = font(FB, 10)
    for i, (num, key, label) in enumerate(VIGNETTES):
        r, c = divmod(i, cols)
        vx0 = x0 + c * cw + gap / 2
        vy0 = y0 + r * ch + gap / 2
        vx1 = x0 + (c + 1) * cw - gap / 2
        vy1 = y0 + (r + 1) * ch - gap / 2
        VIGNETTE_FNS[key](d, vx0, vy0, vx1, vy1 - 16)
        tw = d.textlength(label, font=f_l)
        d.text((vx0 + (vx1 - vx0 - tw) / 2, vy1 - 14), label, font=f_l,
               fill=INK)
        # story number in a small red disc, top-left of the picture
        d.ellipse([vx0 + 2, vy0 + 2, vx0 + 18, vy0 + 18], fill=RED,
                  outline=WHITE, width=1)
        f_n = font(FB, 10)
        ntw = d.textlength(str(num), font=f_n)
        d.text((vx0 + 10 - ntw / 2, vy0 + 4), str(num), font=f_n, fill=WHITE)

# ------------------------------------------------------------- layouts
def layout_a():
    """Front page: map + 6 hero cards + 50-story grid."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    draw_map(d, (24, y + 8, W - 24, y + 192), dot=7)
    y2 = y + 200
    grid_area(d, STORIES[:6], 24, y2, W - 24, y2 + 170, 3, 2, hero_card,
              head_size=18, sub_size=12)
    y3 = y2 + 178
    grid_area(d, STORIES[6:], 24, y3, W - 24, 996, 5, 9, grid_tile)
    summary_cell(d, 24 + 4 * (W - 48) / 5 + 3, y3 + 8 * (996 - y3) / 9 + 3,
                 W - 24 - 3, 996 - 3)
    footer(d)
    return img


def layout_b():
    """Hero scene + 12-vignette band + map + hero cards + grid.
    13 illustrated stories; the day's biggest stories are pictures,
    not just headlines."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d, sub=("THE WORLD IN ONE PICTURE  \u00b7  50 STORIES  "
                         "\u00b7  13 ILLUSTRATED  \u00b7  5 CONTINENTS"))
    # hero scene left, vignette band right
    scene_shenzhen(d, 24, y + 8, 400, y + 212)
    d.rectangle([24, y + 156, 400, y + 212], fill=(18, 18, 18))
    d.text((36, y + 164), "TRUMP IN CHINA FOR TRILATERAL",
           font=fit_font(d, FSB, "TRUMP IN CHINA FOR TRILATERAL", 21, 352),
           fill=WHITE)
    d.text((36, y + 190), "Shakes hands with Xi and Putin ahead of talks",
           font=font(FR, 14), fill=(255, 220, 120))
    vignette_band(d, 416, y + 8, W - 24, y + 212)
    # map left, hero cards full-width row, then the grid
    y2 = y + 220
    draw_map(d, (24, y2, W - 24, y2 + 144), dot=6, pin_r=11)
    y3 = y2 + 152
    grid_area(d, STORIES[1:6], 24, y3, W - 24, y3 + 96, 5, 1, hero_card,
              head_size=17, sub_size=12)
    # grid: stories 7-50 (44) + summary cell
    y4 = y3 + 104
    grid_area(d, STORIES[6:], 24, y4, W - 24, 996, 5, 9, grid_tile)
    summary_cell(d, 24 + 4 * (W - 48) / 5 + 3, y4 + 8 * (996 - y4) / 9 + 3,
                 W - 24 - 3, 996 - 3)
    footer(d)
    return img


def layout_c():
    """Newspaper, three columns: lead text block + map + numbered list."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    lx0, lx1 = 24, 300
    s = STORIES[0]
    d.rectangle([lx0, y + 8, lx1, y + 300], fill=WHITE,
                outline=(200, 195, 180), width=1)
    d.rectangle([lx0, y + 8, lx1, y + 40], fill=RED)
    d.text((lx0 + 10, y + 14), "1. LEAD STORY \u2014 SHENZHEN", font=font(FB, 16),
           fill=WHITE)
    f_h = font(FSB, 28)
    lines = wrap(d, "TRUMP IN CHINA FOR TRILATERAL", f_h, lx1 - lx0 - 20)
    yy = y + 52
    for ln in lines:
        d.text((lx0 + 10, yy), ln, font=f_h, fill=INK)
        yy += 32
    f_b = font(FR, 16)
    body = ("The US president arrived in China to open a rare "
            "three-way summit with China's Xi Jinping and Russia's "
            "Vladimir Putin on the APEC sidelines \u2014 trade, Ukraine "
            "and Iran on the table.")
    for ln in wrap(d, body, f_b, lx1 - lx0 - 20):
        d.text((lx0 + 10, yy), ln, font=f_b, fill=(60, 58, 52))
        yy += 21
    grid_area(d, STORIES[1:3], lx0, y + 308, lx1, y + 590, 1, 2, hero_card,
              head_size=18, sub_size=12)
    cx0, cx1 = 308, 716
    draw_map(d, (cx0, y + 8, cx1, y + 300), dot=6, pin_r=11)
    grid_area(d, STORIES[3:6], cx0, y + 308, cx1, y + 590, 1, 3, hero_card,
              head_size=18, sub_size=12)
    rx0, rx1 = 724, W - 24
    d.rectangle([rx0, y + 8, rx1, y + 888], fill=WHITE,
                outline=(200, 195, 180), width=1)
    f_t = font(FB, 15)
    d.text((rx0 + 8, y + 14), "THE REST \u2014 44 MORE", font=f_t, fill=INK)
    d.line([(rx0 + 8, y + 38), (rx1 - 8, y + 38)], fill=INK, width=1)
    yy = y + 46
    f_h2 = font(FB, 12)
    for s in STORIES[6:]:
        num, region, cat, head, sub, lon, lat = s
        d.text((rx0 + 8, yy), f"{num}.", font=f_h2, fill=CAT_COLOR[cat])
        for ln in wrap(d, head, f_h2, rx1 - rx0 - 46)[:1]:
            d.text((rx0 + 40, yy), ln, font=f_h2, fill=INK)
        yy += 18
    footer(d)
    return img


def layout_d():
    """Timeline strip + map + 50 equal tiles, headlines only."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d, h=80, big=44)
    ty = y + 8
    d.rectangle([24, ty, W - 24, ty + 52], fill=INK)
    f_t = font(FB, 16)
    acts = [("ASIA WAKENS", "Trilateral in Shenzhen \u00b7 GTA VI lands"),
            ("EUROPE MIDDAY", "Kerch bridge falls \u00b7 Anthropic debuts"),
            ("AMERICAS EVENING", "Jeffries picked \u00b7 Fed minutes bite")]
    ax = 24
    for name, sub in acts:
        d.text((ax + 12, ty + 5), name, font=f_t, fill=(255, 220, 120))
        d.text((ax + 12, ty + 28), sub, font=font(FR, 13), fill=WHITE)
        ax += (W - 48) // 3
    y2 = ty + 60
    draw_map(d, (24, y2, W - 24, y2 + 300), dot=7)
    y3 = y2 + 308
    grid_area(d, STORIES, 24, y3, W - 24, 996, 5, 10, grid_tile,
              head_size=12, sub_size=10, show_sub=False)
    footer(d)
    return img


def layout_e():
    """Hero scene (Shenzhen) + map + 5 hero cards + grid."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    scene_shenzhen(d, 24, y + 8, 512, y + 248)
    d.rectangle([24, y + 192, 512, y + 248], fill=(18, 18, 18))
    d.text((36, y + 198), "TRUMP IN CHINA FOR TRILATERAL",
           font=fit_font(d, FSB, "TRUMP IN CHINA FOR TRILATERAL", 26, 464),
           fill=WHITE)
    d.text((36, y + 226), "Shakes hands with Xi and Putin ahead of talks",
           font=font(FR, 15), fill=(255, 220, 120))
    draw_map(d, (520, y + 8, W - 24, y + 248), dot=6, pin_r=11)
    y2 = y + 256
    grid_area(d, STORIES[1:6], 24, y2, W - 24, y2 + 100, 5, 1, hero_card,
              head_size=16, sub_size=11)
    y3 = y2 + 108
    grid_area(d, STORIES[6:], 24, y3, W - 24, 996, 5, 9, grid_tile)
    summary_cell(d, 24 + 4 * (W - 48) / 5 + 3, y3 + 8 * (996 - y3) / 9 + 3,
                 W - 24 - 3, 996 - 3)
    footer(d)
    return img


def layout_f():
    """Tabloid: two scenes + map strip + grid."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d, h=112, big=58)
    scene_bridge(d, 24, y + 8, 506, y + 228)
    d.rectangle([24, y + 170, 506, y + 228], fill=(18, 18, 18))
    d.text((36, y + 176), "KERCH BRIDGE PARTLY COLLAPSES",
           font=fit_font(d, FSB, "KERCH BRIDGE PARTLY COLLAPSES", 22, 458),
           fill=WHITE)
    d.text((36, y + 204), "New video shows blasts before the span falls",
           font=font(FR, 14), fill=(255, 220, 120))
    scene_shenzhen(d, 518, y + 8, W - 24, y + 228)
    d.rectangle([518, y + 170, W - 24, y + 228], fill=(18, 18, 18))
    d.text((530, y + 176), "TRUMP IN CHINA FOR TRILATERAL",
           font=fit_font(d, FSB, "TRUMP IN CHINA FOR TRILATERAL", 22, 470),
           fill=WHITE)
    d.text((530, y + 204), "Shakes hands with Xi and Putin ahead of talks",
           font=font(FR, 14), fill=(255, 220, 120))
    y2 = y + 236
    draw_map(d, (24, y2, W - 24, y2 + 168), dot=6, pin_r=10, label_pins=True)
    y3 = y2 + 176
    grid_area(d, STORIES[6:], 24, y3, W - 24, 996, 5, 9, grid_tile,
              head_size=12, sub_size=10)
    summary_cell(d, 24 + 4 * (W - 48) / 5 + 3, y3 + 8 * (996 - y3) / 9 + 3,
                 W - 24 - 3, 996 - 3)
    footer(d)
    return img


LAYOUTS = {"A": layout_a, "B": layout_b, "C": layout_c,
           "D": layout_d, "E": layout_e, "F": layout_f}

if __name__ == "__main__":
    key = sys.argv[1].upper()
    out = sys.argv[2]
    img = LAYOUTS[key]()
    img.save(out, optimize=True)
    import os
    print(f"{key}: {out} {img.size} {os.path.getsize(out)} bytes")
