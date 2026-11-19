"""news-image-20261119 entry: copy the pre-made image to the output directory.

The image (entry.png, in this repository) sums up the world news of
Thursday 19 November 2026 in one picture: Trump in China for the
trilateral with Xi and Putin at APEC, Anthropic's Nasdaq debut as ANT,
GTA VI arriving after 13 years, the Kerch bridge partly collapsing,
Voyager 1 reaching one light-day out, and Jeffries picked for Speaker
— plus a 12-picture vignette band, a pinned world map and 44 more
stories, 50 in all across 5 continents, every one first reported on
19 November 2026.
This program only copies it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR
when set, for local runs). Deterministic: the same input bytes always
produce the same output bytes. Standard library only, no network.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    src = HERE / "entry.png"
    if not src.is_file():
        print("entry.png missing from repository", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    if dest.stat().st_size != src.stat().st_size:
        print("entry.png copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
