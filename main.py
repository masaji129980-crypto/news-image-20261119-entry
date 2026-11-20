"""Entrypoint: write the 19 November 2026 world-news summary image.

Writes one PNG, entry.png, to $MAKEFUN_OUTPUT_DIR (or /output/ when
unset). The image is drawn in code by draw.py; no network, no files
outside this repository are read.
"""

import os
import sys

from draw import draw_image

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    draw_image(out_path)
    # Self-check the competition limits before finishing: valid PNG
    # signature, at most 1 MiB, at most 1024x1024.
    with open(out_path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a valid PNG")
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    from PIL import Image

    with Image.open(out_path) as im:
        if im.size[0] > MAX_DIM or im.size[1] > MAX_DIM:
            sys.exit(f"entry.png is {im.size}, over the 1024x1024 limit")
        print(f"wrote {out_path}: {len(data)} bytes, {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
