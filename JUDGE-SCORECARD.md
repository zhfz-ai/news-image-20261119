# Judge scorecard — news-image-20261119 (rebuild)

Six candidates (A–F), all 1024×1024, all 50 stories + world map, drawn
with a freshly written `draw.py` (PIL). Scored 0–2 on the 5 published
criteria, in the brief's order. Criterion 1 is the gate: any candidate
failing it outright is discarded (none did).

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
| C | newspaper 3-col: lead block + map + 44-item list | 2 | 2 | 1 | 2 | 2 | 9 | Grid is headlines only, no sublines; the day's smaller stories stay opaque. |
| D | timeline strip + map + 50 equal tiles | 2 | 2 | 1 | 2 | 2 | 9 | No hierarchy: the day's biggest stories are not distinguished; no sublines. |
| E | hero scene (Shenzhen) + map + 5 hero cards + grid | 2 | 2 | 2 | 2 | 2 | 10 | One dominant subject + map + full 50-story grid; only story 1 is a picture. |
| F | tabloid: 2 scenes + map strip + grid | 2 | 2 | 2 | 2 | 1 | 9 | Two strong scenes, but the bridge blast marks read as stray dashes. |

All six were downscaled to 300px and inspected: A, B, C, E, F keep a readable
structure at 300px; B's vignette band and scene stay clearest; D's tiles go
blank-ish at 300px (headlines only, no sublines).

Fixes made during this rebuild (found by inspection, before scoring):
- The Shenzhen tower spire poked above its scene box into the masthead
  subline: the spire tip is now capped inside the scene.
- Vignette captions overflowed their tiles ("ANTHROPIC DEBUTS" cut off):
  captions are now short labels, auto-fit to the tile width.
- The dotted map rendered as vertical streaks in flat strips: dot radius now
  scales with the smaller grid step.
- Grid sublines were cut mid-phrase (e.g. "Rare operation beyond the
  Yellow"): every subline was shortened to fit one line, and an automated
  wrap check now confirms zero overflows across all 50 stories (heroes at
  both sizes + grid tiles).

## Head-to-head (criteria 1–2 first, per the judge)

- B vs A vs E: tied on C1 (2–2–2) and C2 (2–2–2). Decided on C3: B gives 13
  stories a picture each — the ANT ticker, GTA city, Kerch bridge, Voyager
  probe, Capitol, Gaza raid, Waymo car, Akvan spiral, Wall St chart, Nvidia
  chip, Test cricket and gold bars — while A pictures none and E pictures
  only story 1. Criterion 3 asks for each story to be clear "from its
  picture and any short labels": B's vignettes are a real C3 advantage, not
  decoration. **B wins.**
- B beats C and D on C3 outright (complete sublines + pictures vs
  headlines-only grids).
- B beats F on C5 (clean vignettes and scene vs the bridge blast artefacts).

## Pick

**B — "Trump in China for trilateral" hero scene + 12-vignette band +
pinned world map + 50 stories.**
File: `entry.png` (1024×1024, under the 1 MiB cap). 50 stories, all events
that happened or were first reported on 19 November 2026 (Anthropic's $83
IPO pricing and Nasdaq debut, the Shenzhen trilateral, the Kerch bridge
strikes, Voyager 1's one-light-day crossing, and the 19 Nov wire digests);
5 continents; 7 fields (war, politics, tech, markets, weather, sport,
culture). Date named twice: masthead "THURSDAY 19 NOVEMBER 2026" and
footer "as reported on Thursday 19 November 2026".

Date-boundary notes: the Kerch bridge was first struck 16–17 Nov, but was
hit again in the early hours of Thursday 19 Nov (CNN: traffic suspended
after another attack), which is the story told here; Voyager 1 crossed one
light-day on 18 Nov 05:16 EST and NASA's JPL discussion and confirmation
coverage ran on 19 Nov. Two stories first reported late on 18 November in
one time zone and carried as 19 November news in another were checked and
left OUT: the Russian An-12 crash in Siberia (17 Nov) and Somalia's
accusations against the UAE (televised address 17 Nov, reported 18 Nov).
