#!/usr/bin/env python3
"""Save one JPEG from the Camera Module 3.

    python3 scripts/capture.py photo.jpg

Preview in a desktop session with the OS tool, then quit it before capturing:

    rpicam-hello -t 3000

ROVER_MOCK=1 writes a stand-in file and does not open a camera.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rover.camera import capture_jpeg
from rover.preflight import env_flag


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python3 scripts/capture.py photo.jpg", file=sys.stderr)
        return 2
    try:
        dest = capture_jpeg(argv[0], mock=env_flag("ROVER_MOCK"))
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
