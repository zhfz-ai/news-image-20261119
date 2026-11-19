#!/usr/bin/env python3
"""Ship the round-2 front page for news-image-20261119.

The picture (entry.png, next to this file) sums up the world news of
Thursday 19 November 2026: the first US-China-Russia trilateral in
Shenzhen, Anthropic's Nasdaq debut as ANT, GTA VI's launch, the third
Kerch bridge strike of the week, Voyager 1 at one light-day, and 45 more
stories across 5 continents. It was drawn by draw2.py (PIL, no network);
this program only checks the finished PNG and places it where the
harness expects it.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Output: <out>/entry.png  (default /output/entry.png)
"""

import os
import struct
import sys
from pathlib import Path

MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
WANT_W = WANT_H = 1024


def png_size(blob):
    """Width and height from a PNG's IHDR chunk; None if malformed."""
    if len(blob) < 33 or blob[:8] != MAGIC:
        return None
    length, kind = struct.unpack(">I4s", blob[8:16])
    if kind != b"IHDR" or length != 13:
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    blob = src.read_bytes()
    size = png_size(blob)
    if size is None:
        print("entry.png is not a whole PNG file", file=sys.stderr)
        return 1
    if size != (WANT_W, WANT_H):
        print(f"entry.png is {size[0]}x{size[1]}, want "
              f"{WANT_W}x{WANT_H}", file=sys.stderr)
        return 1
    if len(blob) > MAX_BYTES:
        print(f"entry.png is {len(blob)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / "entry.png"
    dest.write_bytes(blob)
    if dest.stat().st_size != len(blob):
        print("entry.png copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(blob)} bytes, {size[0]}x{size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
