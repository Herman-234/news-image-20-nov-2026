#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261120 entry.

Copies the pre-rendered entry.png (produced by render.py, Pillow) to
/output/entry.png and verifies it: it must be a real PNG, under the 1 MiB
limit, and its SHA-256 must match the value recorded at submit time.

Run from the repo root:
    python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
EXPECTED_SIZE = (1024, 1024)

# SHA-256 of entry.png at the submitted commit. Update if entry.png changes.
EXPECTED_SHA256 = "9fa5d8f92148918ea03c3faf398cc3139a77700dfea1fb637bf0fd928984bb4e"


def main():
    if not os.path.exists(SRC):
        print("entry.png not found; run python3 render.py first",
              file=sys.stderr)
        return 1
    data = open(SRC, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a valid PNG", file=sys.stderr)
        return 1
    # PNG IHDR chunk: width and height are the first 8 bytes after the
    # 8-byte signature + 8-byte chunk header (length + "IHDR").
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        print("entry.png is %dx%d, expected %dx%d"
              % (width, height, EXPECTED_SIZE[0], EXPECTED_SIZE[1]),
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit"
              % len(data), file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("SHA-256 mismatch: got %s, expected %s"
              % (digest, EXPECTED_SHA256), file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("entry.png verified: %d bytes, sha256 %s" % (len(data), digest))
    print("copied to", DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
