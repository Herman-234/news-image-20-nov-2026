#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png after verifying it.

Checks: PNG signature, 1 MiB size cap, 1024x1024 dimensions, and the
SHA-256 recorded from the deterministic render. No network, stdlib only.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
EXPECTED_SHA256 = "9ebf23fc72ea9b2d0c44cd32fc086f28f217f24fc85e1082a7fbc4218439cd1c"  # recorded from the deterministic render

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIG:
        sys.exit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        sys.exit("entry.png is %dx%d, expected 1024x1024" % (width, height))
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 is not None and digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("OK %d bytes sha256=%s -> %s" % (len(data), digest, DST))


if __name__ == "__main__":
    main()
