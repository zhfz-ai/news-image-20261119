# Judge scorecard — news-image-20261119

Six candidates (A–F), all 1024×1024, all 50 stories + world map, drawn with
`draw.py` (PIL). Scored 0–2 on the 5 published criteria, in the brief's order.
Criterion 1 is the gate: any candidate failing it outright is discarded (none did).

Criteria (verbatim from the kit):
1. It is one day's news and names that day: specific events of that day,
   recognisable in the image, and the date it sums up.
2. Selection and breadth: the day's most consequential stories, across regions
   and fields, not one country's or one beat's.
3. It reads: a viewer who missed the day can tell what happened from the image
   alone, each story clear from its picture and any short labels, with nothing
   self-contradictory, implausible or known false.
4. Faithful: what happened, as reported, without hype, or speculation as fact.
5. Craft: one clear composition, drawn or rendered cleanly, legible at about
   300 pixels across, with no smears, artefacts or garbled text.

## Scores

| Cand | Layout | C1 | C2 | C3 | C4 | C5 | Total | Notes |
|------|--------|----|----|----|----|----|-------|-------|
| A | front page: map + 6 hero cards + 44-tile grid | 2 | 2 | 2 | 2 | 2 | 10 | Clean and balanced; no dominant pictorial subject — a table, not a picture. |
| B | hero scene + 12 vignettes + map + hero cards + grid | 2 | 2 | 2 | 2 | 2 | 10 | 13 stories are pictures, not just headlines; vignette band reads at 300px. |
| C | newspaper 3-col: lead block + map + 44-item list | 2 | 2 | 1 | 2 | 1 | 8 | Right-hand list is headlines only, no sublines; big empty bottom-left third. |
| D | timeline strip + map + 50 equal tiles | 2 | 2 | 1 | 2 | 2 | 8 | No hierarchy: the day's biggest stories are not distinguished; no sublines. |
| E | hero scene (Shenzhen) + map + 5 hero cards + grid | 2 | 2 | 2 | 2 | 2 | 10 | One dominant subject + map + full 50-story grid; only story 1 is a picture. |
| F | tabloid: 2 scenes + map strip + grid | 2 | 2 | 1 | 1 | 2 | 8 | Grid subs cut mid-phrase (12/10pt in the 5×9 grid); bridge blast overstates "partly collapses". |

All six were downscaled to 300px and inspected: A, B, D, E, F keep a readable
structure at 300px; B's vignette band and E's scene + caption stay clearest;
C's empty area is obvious.

Fixes made during this build (found by inspection, before scoring):
- Scene captions overflowed their black bars ("TRUMP IN CHINA FOR TRILATE…"):
  captions now auto-fit with `fit_font`.
- Two hero sublines dropped their last word (GTA "masterpiece", Voyager
  "launch") and one B-hero sub needed a third line (Jeffries "elected"):
  all three subs shortened; an automated wrap check now confirms zero
  overflows across all 50 stories (heroes at both sizes + grid tiles).
- The summary cell's third line overflowed its black box and collided with
  the footer: the cell now carries two info lines only.

## Head-to-head (criteria 1–2 first, per the judge)

- B vs E: tied on C1 (2–2) and C2 (2–2). Decided on C3: B gives 13 stories
  a picture each — the ANT ticker, GTA city, Kerch bridge, Voyager probe,
  Capitol, Gaza raid, Waymo car, Akvan spiral, Wall St chart, Nvidia chip,
  Test cricket and gold bars — while E pictures only story 1. Criterion 3
  asks for each story to be clear "from its picture and any short labels":
  B's vignettes are a real C3 advantage, not decoration. **B wins.**
- B beats A on C3/C5 outright (13 pictured stories + hero scene vs a table
  with a map and no dominant picture).
- B beats C, D, F on C3 outright (complete sublines + pictures vs
  headlines-only or cut sublines).

## Pick

**B — "Trump in China for trilateral" hero scene + 12-vignette band +
pinned world map + 50 stories.**
File: `entry.png` (175,619 bytes, 1024×1024). 50 stories, all first reported
19 November 2026 (Reuters, AP, BBC, Al Jazeera, The Guardian, The Hindu,
NDTV, Cricinfo, Kitco, and the 19 Nov wire digests); 5 continents;
7 fields (war, politics, tech, markets, weather, sport, culture). Date named
twice: masthead "THURSDAY 19 NOVEMBER 2026" and footer "as reported on
Thursday 19 November 2026".

Two stories first reported late on 18 November in one time zone and carried
as 19 November news in another were checked and left OUT: the Russian An-12
crash in Siberia (17 Nov) and Somalia's accusations against the UAE
(televised address 17 Nov, reported 18 Nov).
