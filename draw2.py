#!/usr/bin/env python3
"""Round-2 front pages for news-image-20261119 (Thursday 19 November 2026).

Fresh renderer written for round 2. Same 50-story brief as round 1, but
the story list is rebuilt from what was actually reported across the whole
of 19 November: the trilateral HELD (under an hour, no deal), ANT's grey
market near $98, GTA VI at 99 on Metacritic with 17.1m copies sold,
New Zealand's 243/5 fightback at stumps, 72,000 evacuated ahead of
Cyclone Akvan, hawkish Fed minutes, Nvidia down despite a $115.8bn beat.
Stale or trivial round-1 items are out (Kahana was elected 17 Nov, the
Bond $100m is unconfirmed reports, the Jupiter / iPhone / Eurovision
items were never verified). Six new layouts G-L; see JUDGE-SCORECARD.md.

Render:  python3 draw2.py <G|H|I|J|K|L|ALL> [out.png]
ALL writes out_G.png .. out_L.png. 1024x1024, PIL only, no network.
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 22

PAPER = (247, 243, 231)
CARD = (253, 251, 245)
INK = (24, 24, 26)
RED = (178, 32, 32)
NAVY = (26, 60, 96)
TEAL = (12, 104, 96)
GOLD = (170, 120, 20)
GREY = (98, 96, 88)
PALE = (204, 198, 182)
DOTC = (40, 76, 112)
SKYTOP = (238, 176, 96)
SKYBOT = (247, 208, 138)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


class Sheet:
    """One 1024x1024 page plus the small text helpers every layout shares."""

    def __init__(self):
        self.img = Image.new("RGB", (SIDE, SIDE), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def lines(self, text, path, size, width, limit=99):
        """Greedy wrap of `text` to at most `limit` lines fitting `width`."""
        font = fnt(path, size)
        out, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if self.d.textlength(trial, font=font) <= width or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
        return out[:limit]

    def shrink(self, text, path, size, width):
        """Biggest font <= size that fits `text` in `width` (never below 8)."""
        s = size
        while s > 8 and self.d.textlength(text, font=fnt(path, s)) > width:
            s -= 1
        return fnt(path, s)

    def fit_lines(self, text, path, size, width, max_lines):
        """Shrink `size` until `text` wraps to at most `max_lines` (min 7)."""
        s = size
        while s > 7:
            if len(self.lines(text, path, s, width, limit=max_lines + 1)) <= max_lines:
                break
            s -= 1
        return self.lines(text, path, s, width, limit=max_lines), s

    def masthead(self, illustrated, ticker=None):
        d = self.d
        d.text((EDGE, 12), "THURSDAY 19 NOVEMBER 2026",
               font=fnt(SERIFB, 44), fill=INK)
        d.text((EDGE, 64),
               "THE WORLD IN ONE PICTURE  \u00b7  50 STORIES  \u00b7  "
               f"{illustrated} ILLUSTRATED  \u00b7  5 CONTINENTS",
               font=fnt(BOLD, 15), fill=RED)
        d.line([(EDGE, 90), (SIDE - EDGE, 90)], fill=INK, width=3)
        y = 98
        if ticker:
            d.rectangle([EDGE, y, SIDE - EDGE, y + 30], fill=RED)
            d.text((EDGE + 10, y + 7), ticker,
                   font=self.shrink(ticker, BOLD, 14, SIDE - 2 * EDGE - 20),
                   fill=(255, 255, 255))
            y += 38
        return y

    def foot(self, note=None):
        d = self.d
        y = SIDE - 26
        d.line([(EDGE, y - 6), (SIDE - EDGE, y - 6)], fill=INK, width=2)
        msg = note or ("Sum up 19 November's world news  \u00b7  as reported on "
                       "Thursday 19 November 2026  \u00b7  make.fun news-image-20261119")
        d.text((SIDE / 2, y + 2), msg, font=fnt(REG, 11), fill=GREY,
               anchor="ma")


# ---- the day's 50 stories, rebuilt for round 2 (see module docstring) ----
# Each entry: number, region, headline, subline, longitude, latitude.
# Regions: ASIA / AMERICAS / EUROPE / MIDEAST / TECH / WORLD.
NEWS = [
    (1, "ASIA", "TRUMP, XI, PUTIN: ONE TABLE",
     "First three-way summit; no deal", 114.1, 22.5),
    (2, "TECH", "ANTHROPIC DEBUTS AS ANT",
     "Priced $83; grey market nears $98", -122.4, 37.8),
    (3, "TECH", "GTA VI ARRIVES AT LAST",
     "99 Metacritic; 17.1m copies sold", -3.2, 55.9),
    (4, "EUROPE", "KERCH BRIDGE HIT A THIRD TIME",
     "Third strike in a week; traffic halted", 34.5, 45.3),
    (5, "TECH", "VOYAGER 1 ONE LIGHT-DAY OUT",
     "NASA confirms the record distance", -118.1, 34.1),
    (6, "AMERICAS", "JEFFRIES WINS 251-11 NOMINATION",
     "First Black Speaker if floor agrees 3 Jan", -77.0, 38.9),
    (7, "MIDEAST", "ISRAEL GROUND RAID IN GAZA",
     "First op past Yellow Line since truce", 34.5, 31.5),
    (8, "AMERICAS", "FED MINUTES: MORE HIKES LIKELY",
     "Almost all back rises; Waller floats 50bp", -77.0, 38.9),
    (9, "TECH", "WAYMO OFF US FREEWAYS",
     "Pulled after California ban", -122.4, 37.8),
    (10, "ASIA", "AKVAN: 72,000 EVACUATED",
     "Odisha moves 72,000; landfall Friday noon", 88.0, 19.0),
    (11, "AMERICAS", "WALL ST SPLIT ON FED MINUTES",
     "Dow -561, S&P falls 5th day", -74.0, 40.7),
    (12, "AMERICAS", "KRESS PROMISES PAY RISES",
     "Moves rises to Dec after Huang exit", -121.9, 37.3),
    (13, "ASIA", "INDIA HITS SCOTCH WITH 162% DUTY",
     "Bulk imports taxed amid pact row", 77.2, 28.6),
    (14, "AMERICAS", "NVIDIA FALLS DESPITE $115.8BN BEAT",
     "Revenue +103% yet shares -2.9%", -121.9, 37.3),
    (15, "AMERICAS", "FED WARNS ON AI BORROWING",
     "AI debt a 'material inflation risk'", -77.0, 38.9),
    (16, "EUROPE", "EU SPEEDS GREEN PERMITS",
     "Parliament and Council agree faster", 4.35, 50.85),
    (17, "ASIA", "INDIA-JAPAN 2+2 TALKS",
     "Defence, security ties are key", 139.7, 35.7),
    (18, "ASIA", "APEC OPENS IN SHENZHEN",
     "Xi pledges $20m for Asia-Pacific cooperation", 114.1, 22.5),
    (19, "MIDEAST", "TRUMP-XI: HORMUZ CONSENSUS",
     "Both agree oil must flow via the strait", 56.0, 26.5),
    (20, "EUROPE", "TRUMP-PUTIN TALK 40 MINUTES",
     "Ukraine discussed; no details given", 114.1, 22.5),
    (21, "AMERICAS", "CONGRESS PROBES TECH OUTAGES",
     "Lawmakers demand answers", -77.0, 38.9),
    (22, "ASIA", "NZ FIGHT BACK TO 243/5",
     "Nicholls 113*, Phillips 94* after 70/5", 174.8, -41.3),
    (23, "AMERICAS", "GOLD AT ONE-YEAR LOW",
     "Gold $3,726 as Fed stays hawkish", -74.0, 40.7),
    (24, "ASIA", "KOSPI TOPS 5,000",
     "Korea +1.99% as chip shares rebound", 127.0, 37.5),
    (25, "ASIA", "SENSEX SLIPS ON FED",
     "Sensex -0.61% to 82,032; Nifty -0.63%", 72.8, 19.1),
    (26, "MIDEAST", "OIL NEAR 3-MONTH LOW",
     "Crude $82 as dollar hits 19-month high", 54.4, 24.45),
    (27, "ASIA", "MOTHS READ MAGNETIC FIELD",
     "Bogong moths navigate by the stars", 149.1, -35.3),
    (28, "WORLD", "BLACK HOLES FROM FAILED STARS",
     "Failed blasts birth black holes", 0.0, 20.0),
    (29, "ASIA", "US-CHINA TRUCE ENDS 10 JAN",
     "Rare-earth exports 75% below normal", 116.4, 39.9),
    (30, "ASIA", "AUSSIE PAY GAP BELOW 20%",
     "Gender pay gap falls under a fifth", 151.2, -33.9),
    (31, "WORLD", "REFUGEE INTAKE WARNING",
     "Plan to all but end intake criticised", 0.0, 20.0),
    (32, "EUROPE", "PATTINSON'S $100M BOND",
     "Reports: $100m for three 007 films", -0.12, 51.5),
    (33, "AMERICAS", "TAKE-TWO JUMPS ON GTA",
     "Shares +7.5% on launch eve", -74.0, 40.7),
    (34, "AMERICAS", "7.9M WATCH GTA STREAMS",
     "Record concurrent viewers for launch", -74.0, 40.7),
    (35, "WORLD", "OUTAGES 'TIED TO AI UPDATES'",
     "Experts blame AI updates", 0.0, 20.0),
    (36, "EUROPE", "SPAIN VOTES IN 10 DAYS",
     "Conservatives lead polls", -3.7, 40.4),
    (37, "AMERICAS", "ANT OPTIONS FROM MONDAY",
     "Cboe lists options two days after debut", -74.0, 40.7),
    (38, "EUROPE", "KYIV'S BIGGEST DRONE NIGHT",
     "Biggest barrage on Russia of the war", 30.5, 50.45),
    (39, "ASIA", "BUMRAH PASSES SRINATH",
     "237th Test wicket in Wellington", 174.8, -41.3),
    (40, "EUROPE", "ZELENSKYY: SEVEN-STAGE OP",
     "President details the bridge operation", 30.5, 50.45),
    (41, "ASIA", "KAMBOJ WICKET ON DEBUT",
     "Removes Conway for 4 in first Test", 174.8, -41.3),
    (42, "AMERICAS", "NEWZOO TIPS RECORD WEEK",
     "GTA launch week $3.25-5.2bn forecast", -74.0, 40.7),
    (43, "MIDEAST", "TRUCE BODY FAULTS BOTH SIDES",
     "US-backed board faults both sides", 34.5, 31.5),
    (44, "ASIA", "XI: FREE AND OPEN TRADE",
     "Beijing pitches itself as stable partner", 114.1, 22.5),
    (45, "ASIA", "TRUMP: KIM 'MAY' JOIN",
     "Trump says Kim may join Shenzhen talks", 127.0, 37.5),
    (46, "TECH", "GTA AT 30FPS ONLY",
     "No 60fps mode, even on PS5 Pro", -3.2, 55.9),
    (47, "ASIA", "INDIA WIN TOSS, BOWL FIRST",
     "Gill opts to field on green pitch", 174.8, -41.3),
    (48, "ASIA", "AKVAN SCHOOLS SHUT",
     "Odisha shuts schools in six districts", 85.8, 20.3),
    (49, "AMERICAS", "BITCOIN SLIDES TO $63,479",
     "Crypto falls as dollar strengthens", -74.0, 40.7),
    (50, "AMERICAS", "FUTURES RISE ON ANT",
     "Nasdaq 100 +1% after $83 pricing", -74.0, 40.7),
]

TAGCOL = {"ASIA": TEAL, "AMERICAS": NAVY, "EUROPE": RED,
          "MIDEAST": (122, 74, 18), "TECH": NAVY, "WORLD": GREY}


def item(n):
    return NEWS[n - 1]


# ---- vignette pictures: which story gets a picture, and its short label ----
PICS12 = [(2, "ant", "ANT"), (3, "gta", "GTA VI"), (4, "bridge", "KERCH"),
          (5, "voyager", "VOYAGER 1"), (6, "capitol", "JEFFRIES"),
          (7, "raid", "GAZA RAID"), (9, "waymo", "WAYMO"),
          (10, "akvan", "AKVAN"), (8, "fed", "FED"),
          (32, "bond", "BOND"), (19, "hormuz", "HORMUZ"),
          (22, "cricket", "NZ 243/5")]
PICS18 = PICS12 + [(14, "chip", "NVIDIA"), (23, "gold", "GOLD"),
                   (34, "streams", "7.9M"), (37, "options", "OPTIONS"),
                   (29, "truce", "TRUCE"), (38, "drone", "DRONES")]

PICLABEL = {n: lab for n, _k, lab in PICS12 + PICS18}


# ---- dotted world map: continents as ellipses in lon/lat space ----
# Each ellipse: (centre lon, centre lat, lon radius, lat radius).
CONTINENTS = [
    (-100, 48, 26, 13), (-88, 32, 18, 8), (-155, 64, 11, 6),
    (-85, 15, 9, 5), (-60, -8, 11, 15), (-66, -28, 7, 9),
    (18, 5, 15, 15), (25, -18, 9, 9),
    (10, 55, 15, 8), (60, 58, 30, 10), (105, 35, 14, 9),
    (45, 30, 10, 7), (78, 21, 7, 9), (102, 12, 8, 7),
    (134, -25, 13, 7), (-2, 54, 3, 4),
    (139, 37, 4, 6), (172, -41, 3, 5), (-42, 72, 14, 6),
]


def _on_land(lon, lat):
    for clon, clat, rlon, rlat in CONTINENTS:
        if ((lon - clon) / rlon) ** 2 + ((lat - clat) / rlat) ** 2 <= 1:
            return True
    return False


def paint_map(sheet, box, numbered=8):
    """Dot continents, then a pin per story; the first `numbered` get numbers."""
    d = sheet.d
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD, outline=PALE)
    step_lon, step_lat = 5.0, 12.0  # near-square dot lattice in this projection
    xs = (x1 - x0) / 72.0
    ys = (y1 - y0) / 12.0
    r = max(1.4, min(xs, ys) * 0.36)
    lon = -180.0
    while lon < 180.0:
        lat = 85.0
        while lat > -60.0:
            if _on_land(lon, lat):
                px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
                py = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
                d.ellipse([px - r, py - r, px + r, py + r], fill=DOTC)
            lat -= step_lat
        lon += step_lon
    for n, _rg, _h, _s, slon, slat in NEWS:
        px = x0 + (slon + 180.0) / 360.0 * (x1 - x0)
        py = y0 + (90.0 - slat) / 180.0 * (y1 - y0)
        if n <= numbered:
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                      outline=(255, 255, 255), width=1)
            d.text((px, py - 1), str(n), font=fnt(BOLD, 10),
                   fill=(255, 255, 255), anchor="mm")
        else:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)


# ---- vignette glyphs: one tiny scene per kind, drawn from primitives ----
def glyph(sheet, kind, box):
    d = sheet.d
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "ant":
        d.rectangle(box, fill=(16, 24, 40))
        d.text((x0 + w * 0.38, y0 + 2), "ANT", font=fnt(BOLD, 14),
               fill=(110, 220, 130))
        pts = [(x0 + 4, y1 - 8), (x0 + w * 0.3, y1 - h * 0.55),
               (x0 + w * 0.55, y1 - h * 0.4), (x1 - 4, y0 + 6)]
        d.line(pts, fill=(110, 220, 130), width=2)
        d.ellipse([x1 - 10, y0 + 1, x1, y0 + 11], fill=(110, 220, 130))
        d.text((x0 + 4, y1 - 17), "$83", font=fnt(BOLD, 11),
               fill=(255, 255, 255))
    elif kind == "gta":
        d.rectangle(box, fill=(238, 150, 190))
        d.rectangle([x0, y1 - h * 0.42, x1, y1], fill=(40, 30, 60))
        for bx, bh in [(0.06, 0.55), (0.28, 0.75), (0.52, 0.6), (0.74, 0.85)]:
            d.rectangle([x0 + w * bx, y1 - h * bh, x0 + w * (bx + 0.18),
                         y1 - h * 0.42], fill=(20, 16, 40))
        d.ellipse([x1 - w * 0.3, y0 + 3, x1 - w * 0.08, y0 + h * 0.28],
                  fill=(255, 220, 120))
        d.text((x0 + 4, y1 - 15), "99", font=fnt(BOLD, 11),
               fill=(255, 255, 255))
    elif kind == "bridge":
        d.rectangle(box, fill=(190, 220, 235))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(90, 140, 170))
        d.arc([x0 + w * 0.1, y0 + h * 0.25, x1 - w * 0.1, y1 - h * 0.05],
              180, 360, fill=(60, 60, 60), width=3)
        d.line([(x0 + w * 0.1, y1 - h * 0.3), (x1 - w * 0.1, y1 - h * 0.3)],
               fill=(60, 60, 60), width=3)
        d.ellipse([cx - 6, cy - h * 0.3, cx + 6, cy - h * 0.3 + 12],
                  fill=(255, 120, 30))
        for t in range(6):
            a = math.pi * t / 5
            sx = cx + math.cos(a) * w * 0.3
            sy = cy - math.sin(a) * h * 0.2
            d.line([(sx, sy), (sx, sy + 5)], fill=(255, 140, 40), width=2)
    elif kind == "voyager":
        d.rectangle(box, fill=(10, 14, 34))
        for sx, sy, rr in [(0.2, 0.25, 1), (0.7, 0.15, 1), (0.85, 0.5, 1),
                           (0.35, 0.6, 1), (0.55, 0.35, 2)]:
            d.ellipse([x0 + w * sx - rr, y0 + h * sy - rr,
                       x0 + w * sx + rr, y0 + h * sy + rr],
                      fill=(255, 255, 255))
        d.line([(x0 + w * 0.15, y1 - h * 0.2), (x0 + w * 0.75, y0 + h * 0.25)],
               fill=(200, 200, 210), width=2)
        d.ellipse([x0 + w * 0.68, y0 + h * 0.12, x0 + w * 0.88, y0 + h * 0.38],
                  outline=(220, 220, 230), width=2)
        d.polygon([(x0 + w * 0.15, y1 - h * 0.2), (x0 + w * 0.3, y1 - h * 0.2),
                   (x0 + w * 0.2, y1 - h * 0.35)], fill=(180, 180, 190))
        d.text((x0 + 4, y1 - 14), "1 LIGHT-DAY", font=fnt(BOLD, 9),
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
        d.text((x0 + 4, y1 - 14), "GAZA", font=fnt(BOLD, 10),
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
        for rr in range(2, 16, 2):
            a0 = rr * 0.9
            d.arc([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8],
                  a0 * 57, a0 * 57 + 200, fill=(255, 255, 255), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 120, 60))
        d.text((x0 + 4, y1 - 14), "72,000 OUT", font=fnt(BOLD, 9),
               fill=(20, 40, 60))
    elif kind == "fed":
        d.rectangle(box, fill=(240, 238, 228))
        for i, bh in enumerate([0.4, 0.55, 0.48, 0.62, 0.78]):
            bx = x0 + w * (0.08 + i * 0.18)
            d.rectangle([bx, y1 - h * bh, bx + w * 0.12, y1 - h * 0.12],
                        fill=(120, 120, 110) if i < 4 else RED)
        d.line([(x0 + 3, y1 - h * 0.2), (x1 - 4, y0 + h * 0.15)],
               fill=RED, width=2)
        d.polygon([(x1 - 4, y0 + h * 0.15), (x1 - 12, y0 + h * 0.15),
                   (x1 - 4, y0 + h * 0.28)], fill=RED)
    elif kind == "bond":
        d.rectangle(box, fill=(12, 12, 16))
        d.ellipse([cx - w * 0.2, cy - h * 0.28, cx + w * 0.2, cy + h * 0.28],
                  outline=(212, 175, 55), width=2)
        d.text((cx, cy), "007", font=fnt(BOLD, 15),
               fill=(212, 175, 55), anchor="mm")
        d.text((x0 + 4, y1 - 14), "$100M", font=fnt(BOLD, 10),
               fill=(255, 255, 255))
    elif kind == "hormuz":
        d.rectangle(box, fill=(90, 140, 170))
        d.rectangle([x0, y1 - h * 0.35, x1, y1], fill=(40, 80, 120))
        d.rectangle([x0 + w * 0.15, y0 + h * 0.35, x1 - w * 0.15,
                     y0 + h * 0.62], fill=(120, 40, 30))
        d.rectangle([x0 + w * 0.3, y0 + h * 0.2, x0 + w * 0.4,
                     y0 + h * 0.35], fill=(200, 200, 200))
        d.polygon([(x0 + w * 0.7, y0 + h * 0.1), (x0 + w * 0.78, y0 + h * 0.3),
                   (x0 + w * 0.62, y0 + h * 0.3)], fill=(255, 200, 80))
        d.text((x0 + 4, y1 - 14), "OIL FLOWS", font=fnt(BOLD, 9),
               fill=(255, 255, 255))
    elif kind == "streams":
        d.rectangle(box, fill=(30, 30, 50))
        d.polygon([(cx - 8, y0 + h * 0.2), (cx - 8, y1 - h * 0.25),
                   (cx + 12, cy - 4)], fill=(255, 255, 255))
        d.text((x0 + 4, y1 - 14), "7.9M LIVE", font=fnt(BOLD, 10),
               fill=(255, 220, 120))
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
        d.text((x0 + 4, y0 + 2), "-2.9%", font=fnt(BOLD, 10), fill=(255, 120, 90))
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
        d.text((x0 + 4, y1 - 14), "243/5", font=fnt(BOLD, 10),
               fill=(255, 255, 255))
    elif kind == "options":
        d.rectangle(box, fill=(16, 24, 40))
        d.text((x0 + 4, y0 + h * 0.3), "OPTIONS", font=fnt(BOLD, 10),
               fill=(255, 255, 255))
        d.text((x0 + 4, y1 - 16), "FROM MONDAY", font=fnt(BOLD, 9),
               fill=(150, 200, 255))
    elif kind == "truce":
        d.rectangle(box, fill=(230, 225, 210))
        d.line([(x0 + w * 0.15, y0 + h * 0.5), (x1 - w * 0.15, y0 + h * 0.5)],
               fill=(60, 60, 60), width=2)
        d.ellipse([x0 + w * 0.2, y0 + h * 0.2, x0 + w * 0.38, y0 + h * 0.5],
                  fill=(178, 32, 32))
        d.ellipse([x0 + w * 0.62, y0 + h * 0.2, x0 + w * 0.8, y0 + h * 0.5],
                  fill=(26, 60, 96))
        d.text((x0 + 4, y1 - 14), "10 JAN", font=fnt(BOLD, 10), fill=INK)
    elif kind == "drone":
        d.rectangle(box, fill=(70, 80, 95))
        d.line([(x0 + w * 0.1, y1 - h * 0.3), (x1 - w * 0.1, y0 + h * 0.2)],
               fill=(220, 220, 220), width=2)
        d.ellipse([x1 - w * 0.3, y0 + h * 0.1, x1 - w * 0.08, y0 + h * 0.35],
                  outline=(220, 220, 220), width=2)
        d.polygon([(x0 + w * 0.1, y1 - h * 0.3), (x0 + w * 0.25, y1 - h * 0.3),
                   (x0 + w * 0.16, y1 - h * 0.5)], fill=(200, 200, 200))
        d.text((x0 + 4, y1 - 14), "BIGGEST YET", font=fnt(BOLD, 9),
               fill=(255, 255, 255))
    else:
        d.rectangle(box, fill=(220, 220, 215))


# ---- hero scenes ----
def _flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(178, 32, 32) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(26, 60, 96))
    for sx in range(3):
        for sy in range(2):
            d.ellipse([x + 2 + sx * 6, y + 2 + sy * 6,
                       x + 5 + sx * 6, y + 5 + sy * 6], fill=(255, 255, 255))


def _flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 30, 30))
    d.ellipse([x + 3, y + 3, x + 9, y + 9], fill=(255, 220, 80))
    for sx, sy in [(16, 4), (20, 8), (20, 13), (16, 16)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(255, 220, 80))


def _flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (26, 60, 160), (200, 30, 30)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def paint_summit(sheet, box):
    """Three flags over a table, three leaders: the Shenzhen trilateral."""
    d = sheet.d
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    bar_h = max(int(h * 0.24), 54)  # caption bar: room for two text lines
    scene_h = h - bar_h
    for i in range(scene_h):
        t = i / max(scene_h - 1, 1)
        rr = int(SKYTOP[0] + (SKYBOT[0] - SKYTOP[0]) * t)
        gg = int(SKYTOP[1] + (SKYBOT[1] - SKYTOP[1]) * t)
        bb = int(SKYTOP[2] + (SKYBOT[2] - SKYTOP[2]) * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(rr, gg, bb))
    d.ellipse([x1 - w * 0.22, y0 + scene_h * 0.08,
               x1 - w * 0.06, y0 + scene_h * 0.30],
              fill=(255, 214, 130))
    pole_y = y0 + scene_h - 6
    for fx, flag in [(0.10, _flag_us), (0.44, _flag_cn), (0.78, _flag_ru)]:
        px = x0 + w * fx
        d.line([(px, y0 + scene_h * 0.12), (px, pole_y)], fill=(40, 40, 40),
               width=3)
        flag(d, px + 2, y0 + scene_h * 0.12, 30, 20)
    table_y = y0 + scene_h - 6
    d.rectangle([x0, table_y, x1, table_y + 8], fill=(96, 58, 34))
    d.rectangle([x0, table_y, x1, table_y + 3], fill=(150, 100, 60))
    for fx, skin, hair, suit in [(0.2, (232, 192, 162), (242, 232, 212),
                                  (40, 60, 110)),
                                 (0.5, (236, 201, 166), (28, 28, 28),
                                  (60, 60, 70)),
                                 (0.8, (226, 186, 156), (205, 205, 205),
                                  (90, 40, 40))]:
        px = x0 + w * fx
        d.polygon([(px - 30, table_y), (px - 15, table_y - scene_h * 0.26),
                   (px + 15, table_y - scene_h * 0.26), (px + 30, table_y)],
                  fill=suit)
        d.polygon([(px - 6, table_y - scene_h * 0.26),
                   (px, table_y - scene_h * 0.08),
                   (px + 6, table_y - scene_h * 0.26)],
                  fill=(255, 255, 255))
        d.ellipse([px - 15, table_y - scene_h * 0.46, px + 15,
                   table_y - scene_h * 0.46 + 30], fill=skin)
        d.pieslice([px - 15, table_y - scene_h * 0.46, px + 15,
                    table_y - scene_h * 0.46 + 16], 180, 360, fill=hair)
    d.rectangle([x0, y1 - bar_h, x1, y1], fill=(12, 12, 16))
    d.text((x0 + 12, y1 - bar_h + 6), "THREE LEADERS, ONE TABLE",
           font=sheet.shrink("THREE LEADERS, ONE TABLE", SERIFB, 21, w - 24),
           fill=(255, 255, 255))
    d.text((x0 + 12, y1 - bar_h + 32),
           "First US-China-Russia summit; under an hour, no deal",
           font=sheet.shrink("First US-China-Russia summit; under an hour, "
                             "no deal", SERIF, 13, w - 24),
           fill=(240, 210, 130))


def paint_ant_scene(sheet, box):
    """ANT's first day: the $83 IPO price and the grey market near $98."""
    d = sheet.d
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(16, 24, 40))
    d.text((x0 + 12, y0 + 8), "ANT", font=fnt(BOLD, 26),
           fill=(110, 220, 130))
    d.text((x0 + 12, y0 + 40), "$83 IPO  \u2192  ~$98 GREY MARKET",
           font=sheet.shrink("$83 IPO  \u2192  ~$98 GREY MARKET", BOLD, 14,
                             w - 24), fill=(255, 255, 255))
    pts = [(x0 + 12, y1 - h * 0.45), (x0 + w * 0.3, y1 - h * 0.5),
           (x0 + w * 0.55, y1 - h * 0.62), (x1 - 12, y1 - h * 0.85)]
    d.line(pts, fill=(110, 220, 130), width=3)
    d.ellipse([x1 - 18, y1 - h * 0.85 - 6, x1 - 6, y1 - h * 0.85 + 6],
              fill=(110, 220, 130))
    d.rectangle([x0, y1 - h * 0.24, x1, y1], fill=(12, 12, 16))
    d.text((x0 + 12, y1 - h * 0.22), "ANTHROPIC DEBUTS AS ANT",
           font=sheet.shrink("ANTHROPIC DEBUTS AS ANT", SERIFB, 21, w - 24),
           fill=(255, 255, 255))
    d.text((x0 + 12, y1 - h * 0.11),
           "Record $81.3bn IPO; biggest debut ever",
           font=sheet.shrink("Record $81.3bn IPO; biggest debut ever",
                             SERIF, 13, w - 24), fill=(240, 210, 130))


# ---- page furniture: vignette band, hero cards, story grid ----
def paint_vignettes(sheet, box, pics):
    d = sheet.d
    x0, y0, x1, y1 = box
    cols = 6
    rows = (len(pics) + cols - 1) // cols
    gap = 6
    cw = (x1 - x0 - gap * (cols - 1)) / cols
    ch = (y1 - y0 - gap * (rows - 1)) / rows
    for i, (n, kind, _lab) in enumerate(pics):
        r, c = divmod(i, cols)
        vx0 = x0 + c * (cw + gap)
        vy0 = y0 + r * (ch + gap)
        vx1, vy1 = vx0 + cw, vy0 + ch
        glyph(sheet, kind, (vx0, vy0, vx1, vy1 - 14))
        d.rectangle([vx0, vy1 - 14, vx1, vy1], fill=INK)
        lab = PICLABEL[n]
        d.text((vx0 + 4, vy1 - 13),
               lab, font=sheet.shrink(lab, BOLD, 9, cw - 8),
               fill=(255, 255, 255))
        d.ellipse([vx0 + 2, vy0 + 2, vx0 + 16, vy0 + 16], fill=RED)
        d.text((vx0 + 9, vy0 + 9), str(n), font=fnt(BOLD, 8),
               fill=(255, 255, 255), anchor="mm")


def paint_cards(sheet, box, nums, head_size=13):
    d = sheet.d
    x0, y0, x1, y1 = box
    n = len(nums)
    gap = 8
    cw = (x1 - x0 - gap * (n - 1)) / n
    for i, num in enumerate(nums):
        _, region, head, sub, _lo, _la = item(num)
        cx0 = x0 + i * (cw + gap)
        cx1 = cx0 + cw
        col = TAGCOL.get(region, GREY)
        d.rectangle([cx0, y0, cx1, y1], fill=CARD, outline=PALE)
        d.rectangle([cx0, y0, cx1, y0 + 3], fill=col)
        d.text((cx0 + 7, y0 + 8), f"{num}. {region}",
               font=fnt(BOLD, 10), fill=col)
        yy = y0 + 24
        for line in sheet.lines(head, BOLD, head_size, cw - 14, limit=2):
            d.text((cx0 + 7, yy), line, font=fnt(BOLD, head_size), fill=INK)
            yy += head_size + 3
        sublines, ssize = sheet.fit_lines(sub, REG, 10, cw - 14, 2)
        for line in sublines:
            d.text((cx0 + 7, yy), line, font=fnt(REG, ssize), fill=GREY)
            yy += ssize + 3


def paint_grid(sheet, box, nums, cols=5, sub=True, summary=True, ill=13):
    d = sheet.d
    x0, y0, x1, y1 = box
    rows = math.ceil(len(nums) / cols)
    gap = 6
    cw = (x1 - x0 - gap * (cols - 1)) / cols
    ch = (y1 - y0 - gap * (rows - 1)) / rows
    for i, num in enumerate(nums):
        r, c = divmod(i, cols)
        tx0 = x0 + c * (cw + gap)
        ty0 = y0 + r * (ch + gap)
        _, _rg, head, subline, _lo, _la = item(num)
        d.rectangle([tx0, ty0, tx0 + cw, ty0 + ch], fill=CARD, outline=PALE)
        d.ellipse([tx0 + 5, ty0 + 5, tx0 + 17, ty0 + 17], fill=RED)
        d.text((tx0 + 11, ty0 + 11), str(num), font=fnt(BOLD, 8),
               fill=(255, 255, 255), anchor="mm")
        yy = ty0 + 4
        for line in sheet.lines(head, BOLD, 11, cw - 26, limit=2):
            d.text((tx0 + 21, yy), line, font=fnt(BOLD, 11), fill=INK)
            yy += 13
        if sub:
            one, ssize = sheet.fit_lines(subline, REG, 9, cw - 26, 1)
            for line in one:
                d.text((tx0 + 21, yy), line, font=fnt(REG, ssize), fill=GREY)
                yy += ssize + 2
    if summary:
        r, c = divmod(len(nums), cols)
        tx0 = x0 + c * (cw + gap)
        ty0 = y0 + r * (ch + gap)
        d.rectangle([tx0, ty0, tx0 + cw, ty0 + ch], fill=INK)
        d.text((tx0 + 8, ty0 + 6), "THE DAY IN NUMBERS",
               font=fnt(BOLD, 10), fill=(240, 210, 130))
        d.text((tx0 + 8, ty0 + 22), f"50 stories \u00b7 {ill} illustrated",
               font=fnt(REG, 9), fill=(255, 255, 255))
        if ty0 + 45 <= y1:
            d.text((tx0 + 8, ty0 + 34), "5 continents \u00b7 7 fields \u00b7 19 Nov",
                   font=fnt(REG, 9), fill=(255, 255, 255))


# ---- the six round-2 candidate layouts ----
def page_g(sh):
    """Summit hero + 12 vignettes + tall map + 6 cards + grid (r1-B shape)."""
    y = sh.masthead(13)
    paint_summit(sh, (EDGE, y, 500, y + 196))
    paint_vignettes(sh, (508, y, SIDE - EDGE, y + 196), PICS12)
    paint_map(sh, (EDGE, y + 204, SIDE - EDGE, y + 344))
    paint_cards(sh, (EDGE, y + 352, SIDE - EDGE, y + 464), [1, 2, 3, 4, 5, 6])
    paint_grid(sh, (EDGE, y + 472, SIDE - EDGE, SIDE - 34),
               list(range(7, 51)), cols=5)
    sh.foot()


def page_h(sh):
    """Split hero (summit + ANT scene) + 12 vignettes + map + grid, no cards."""
    y = sh.masthead(14)
    paint_summit(sh, (EDGE, y, 512, y + 196))
    paint_ant_scene(sh, (520, y, SIDE - EDGE, y + 196))
    paint_vignettes(sh, (EDGE, y + 204, SIDE - EDGE, y + 340), PICS12)
    paint_map(sh, (EDGE, y + 348, SIDE - EDGE, y + 468))
    pictured = {1} | {n for n, _k, _l in PICS12}
    rest = [n for n in range(1, 51) if n not in pictured]
    paint_grid(sh, (EDGE, y + 476, SIDE - EDGE, SIDE - 34),
               rest, cols=5, ill=14)
    sh.foot()


def page_i(sh):
    """Small summit hero + 18 vignettes (3 rows) + map + grid, no cards row."""
    y = sh.masthead(19)
    paint_summit(sh, (EDGE, y, SIDE - EDGE, y + 130))
    paint_vignettes(sh, (EDGE, y + 138, SIDE - EDGE, y + 396), PICS18)
    paint_map(sh, (EDGE, y + 404, SIDE - EDGE, y + 494))
    paint_grid(sh, (EDGE, y + 502, SIDE - EDGE, SIDE - 34),
               list(range(7, 51)), cols=5, sub=False, ill=19)
    sh.foot()


def page_j(sh):
    """Big full-width summit hero + tall map + 12 vignettes + grid, no cards."""
    y = sh.masthead(13)
    paint_summit(sh, (EDGE, y, SIDE - EDGE, y + 220))
    paint_map(sh, (EDGE, y + 228, SIDE - EDGE, y + 348))
    paint_vignettes(sh, (EDGE, y + 356, SIDE - EDGE, y + 512), PICS12)
    paint_grid(sh, (EDGE, y + 520, SIDE - EDGE, SIDE - 34),
               list(range(7, 51)), cols=5, sub=False)
    sh.foot()


def page_k(sh):
    """Summit hero + 12 vignettes + map + all-50 grid (roomy tiles, no cards)."""
    y = sh.masthead(13)
    paint_summit(sh, (EDGE, y, 500, y + 196))
    paint_vignettes(sh, (508, y, SIDE - EDGE, y + 196), PICS12)
    paint_map(sh, (EDGE, y + 204, SIDE - EDGE, y + 324))
    paint_grid(sh, (EDGE, y + 332, SIDE - EDGE, SIDE - 34),
               list(range(1, 51)), cols=5, summary=False)
    sh.foot()


def page_l(sh):
    """Layout G plus a red LATE ticker strip of the day's late flashes."""
    ticker = ("LATE: ANT GREY MARKET NEARS $98  \u00b7  TRILATERAL ENDS WITH "
              "NO DEAL  \u00b7  NZ 243/5 AT STUMPS  \u00b7  72,000 EVACUATED")
    y = sh.masthead(13, ticker=ticker)
    paint_summit(sh, (EDGE, y, 500, y + 180))
    paint_vignettes(sh, (508, y, SIDE - EDGE, y + 180), PICS12)
    paint_map(sh, (EDGE, y + 188, SIDE - EDGE, y + 318))
    paint_cards(sh, (EDGE, y + 326, SIDE - EDGE, y + 430), [1, 2, 3, 4, 5, 6])
    paint_grid(sh, (EDGE, y + 438, SIDE - EDGE, SIDE - 34),
               list(range(7, 51)), cols=5)
    sh.foot()


PAGES = {"G": page_g, "H": page_h, "I": page_i,
         "J": page_j, "K": page_k, "L": page_l}


def build(which):
    sh = Sheet()
    PAGES[which](sh)
    return sh.img


def main(argv):
    if len(argv) < 2 or argv[1] not in list(PAGES) + ["ALL"]:
        print("usage: draw2.py <G|H|I|J|K|L|ALL> [out.png]")
        return 2
    which = argv[1]
    out = argv[2] if len(argv) > 2 else None
    if which == "ALL":
        for name in "GHIJKL":
            path = out.replace(".png", f"_{name}.png") if out else f"out_{name}.png"
            build(name).save(path)
            print(f"{name}: {path}")
        return 0
    path = out or "entry.png"
    build(which).save(path)
    print(f"{which}: {path} ({SIDE}x{SIDE})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
