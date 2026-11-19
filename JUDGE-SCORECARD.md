# Judge scorecard — news-image-20261119, round 2

Six candidates (G–L), all 1024×1024, all the same rebuilt 50-story list +
world map, drawn with a freshly written `draw2.py` (PIL). Scored 0–2 on
the 5 published criteria, in the brief's order. Criterion 1 is the gate:
any candidate failing it outright is discarded (none did).

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

## The rebuilt story list (round 2 vs round 1)

24 stories kept (several re-headlined with real numbers: Jeffries 251-11,
NZ stumps 243/5, Akvan 72,000 evacuated, ANT grey market ~$98, GTA 99 /
17.1m). 26 replaced. OUT: Kahana (elected 17 Nov, not 19 Nov), Pew, the
Trump cybercrime item, William & Kate, the SC contempt item, Shinde Sena,
Lytton, Haryana, the NASA nuclear ship, Jupiter "vanishes", Earth's lost
billion years, Hunger Games fan, Ranveer, iPhone 20 leaks, World Boxing,
GTA "cheaper in real terms", Akash Deep feature, GTA "born of Britain",
NSW human rights, Iglesias, Eurovision-to-Asia, Casey hospital, Parramatta
Road, critical minerals hearings, Abu Dhabi T10, GTA "end of an era".
IN (all verified from 19 Nov reporting): Fed minutes — more hikes likely,
Nvidia falls despite a $115.8bn beat, Fed warns on AI borrowing, APEC opens
in Shenzhen, Trump–Xi Hormuz consensus, Trump–Putin 40-minute talk, NZ
fight back to 243/5, gold at a one-year low, Kospi tops 5,000, Sensex slips,
oil near a 3-month low, US–China truce ends 10 Jan, Take-Two jumps on GTA,
7.9m watch GTA streams, ANT options from Monday, Kyiv's biggest drone
night, Bumrah passes Srinath, Zelenskyy on the seven-stage bridge op,
Kamboj wicket on debut, Newzoo tips a record week, truce body faults both
sides, Xi on free and open trade, Trump saying Kim "may" join, GTA at
30fps only, Akvan schools shut, Bitcoin slides to $63,479, futures rise
on ANT. The Pattinson $100m Bond item is kept but hedged as "Reports:" —
it is unconfirmed. Waymo (ban 11 Nov, reported 17–18 Nov) and the
Wednesday Wall St close are kept as in round 1: first widely reported
on 18–19 Nov.

## Scores

| Cand | Layout | C1 | C2 | C3 | C4 | C5 | Total | Notes |
|------|--------|----|----|----|----|----|-------|-------|
| G | summit hero + 12 vignettes + tall map + 6 cards + grid | 2 | 2 | 2 | 2 | 2 | 10 | Every story has headline + subline; top 6 get cards; summit hero is specific (3 flags, 3 leaders). |
| H | split hero (summit + ANT scene) + 12 vignettes + map + grid, no cards | 2 | 2 | 1 | 2 | 2 | 9 | Two big scenes read best at 300px, but 13 pictured stories have no headline/subline anywhere (Kerch, Jeffries label-only). |
| I | small summit hero + 18 vignettes (3 rows) + map + grid, no cards | 2 | 2 | 1 | 2 | 1 | 8 | Most pictures (19 illustrated), but grid is headline-only, no sublines; short hero leaves the leaders as heads over the table edge. |
| J | big full-width summit hero + tall map + 12 vignettes + grid, no cards | 2 | 2 | 1 | 2 | 2 | 9 | Biggest hero reads well; grid headline-only, no sublines. |
| K | summit hero + 12 vignettes + map + all-50 grid, no cards | 2 | 2 | 2 | 2 | 2 | 10 | Roomiest grid tiles (all 50 with sublines); no hierarchy beyond the hero — top stories get no bigger type. |
| L | G + red LATE ticker strip of the day's late flashes | 2 | 2 | 2 | 2 | 2 | 10 | Ticker names the late flashes explicitly, but repeats facts already on the page and costs 38px of grid height. |

All six were downscaled to 300px and inspected: G, H, J, K, L keep a
readable structure at 300px (masthead date, hero scene(s), vignette band,
map band, grid table all distinct); I's hero is cramped at 300px. G and H
were compared side by side at 300px: H's split hero is the more striking
top band, G's cards row is the clearer hierarchy.

Fixes made during this round (found by inspection, before scoring):
- Grid sublines were cut mid-phrase in the first render: sublines now
  shrink-to-fit one line (min 7pt) and the longest ones were shortened in
  the data, so every subline is complete.
- The summit scene's figures read as dark blobs and the table as a mound:
  suits are now distinct colours with white shirts, the table is a flat
  band, and the caption bar is guaranteed 54px so two text lines fit even
  in the short hero.
- The dotted map rendered as vertical streaks: dots now sit on a
  near-square lattice (5° lon × 12° lat) over a finer continent set, so
  the continents read as clusters.
- The "OPTIONS" vignette's ANT text collided with its number badge: the
  text is gone (the label below already says OPTIONS).
- The summary cell's third line was cut off in the short-grid layouts:
  it is drawn only when it fits inside the grid box.
- H's summary cell said "13 illustrated" for 14 pictures: fixed in code
  (ill=14) and H re-rendered.

## Head-to-head (criteria 1–2 first, per the judge)

- G vs K vs L: tied on C1 (2–2–2) and C2 (2–2–2). Decided on C3/C5: G
  gives the six biggest stories hero cards with full headlines and
  sublines, so the day's hierarchy is visible at one glance; K spreads
  all 50 evenly with no lead stories; L's ticker repeats facts the page
  already states. **G wins.**
- G beats H and J on C3 outright (complete sublines for every story vs
  pictured stories with label-only captions / headline-only grids).
- G beats I on C5 (clean hero and map vs the cramped short hero).

## Pick

**G — "Three leaders, one table" summit hero + 12-vignette band + dotted
world map + 6 hero cards + 50 stories.**
File: `entry.png` (1024×1024, 178,472 bytes, under the 1 MiB cap;
re-render is byte-identical, sha256
f333ef350defa3b300ddc67c2920966ead70e207b3be144c39dee5bf1ca854eb).
50 stories, all events that happened or were first reported on 19
November 2026; 5 continents; 7 fields (war, politics, tech, markets,
weather, sport, culture). Date named twice: masthead "THURSDAY 19
NOVEMBER 2026" and footer "as reported on Thursday 19 November 2026".

## Round 2 vs round 1 (the current entry)

Round 1 (layout B, 50 stories, 13 illustrated) and round 2 (layout G, 50
stories, 13 illustrated) share the same shape, so the comparison is the
content, not the frame. On C2 round 2 is clearly ahead: 26 of 50 stories
are replaced by more consequential, later-reported 19 Nov items (Fed
minutes, the Nvidia beat/fall, NZ at stumps, the Akvan evacuation, the
Hormuz consensus, the Trump–Putin talk, the drone night, the options and
futures items) and the kept stories carry real numbers (251-11, 243/5,
72,000, $98, 99, 17.1m). On C4 round 2 is ahead: the 17 Nov Kahana vote
and the unverified Jupiter / iPhone / Eurovision items are out, and the
unconfirmed Bond figure is hedged as reports. On C3 round 2 is ahead:
every subline is complete (round 1 cut several mid-phrase) and the hero
is a specific scene of the day's biggest event instead of a generic
skyline. On C1 and C5 round 2 is equal-or-better. **Verdict: round 2
clearly beats round 1 — submit-candidate.**
