#!/usr/bin/env python3
"""Ship the pre-rendered front page for news-image-20261119.

The picture itself (entry.png, next to this file) sums up the world news
of Thursday 19 November 2026: the Shenzhen trilateral, Anthropic's
Nasdaq debut as ANT, GTA VI's launch, the Kerch bridge, Voyager 1 at one
light-day, and 44 more stories across 5 continents. It was drawn by
draw.py (PIL, no network); this program only places the finished PNG
where the harness expects it.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Output: <out>/entry.png  (default /output/entry.png)
"""

import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def ship() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    blob = src.read_bytes()
    if not blob.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    import os

    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(src, dest)
    if dest.stat().st_size != len(blob):
        print("entry.png copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(ship())
