#!/usr/bin/env python3
"""Print HC-SR04 distances. Does not run the motors.

Put your hand in front of the sensor. The number should fall. "no echo" means
the web page would lock forward.

    python3 scripts/check_distance.py
    ROVER_MOCK=1 python3 scripts/check_distance.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rover.fakes import FakeRanger
from rover.preflight import env_flag
from rover.ultrasonic import HCSR04


def main() -> int:
    mock = env_flag("ROVER_MOCK")
    if mock:
        sensor = FakeRanger(0.42)
        count = 3
        pause = 0.0
        print("ROVER_MOCK=1: printing a fixed 42 cm reading.")
    else:
        print("Echo must already be on the resistor divider, not wired straight to the Pi.")
        print("Ctrl+C stops the readings. Motors are not used.")
        sensor = HCSR04()
        count = 30
        pause = 0.2
    try:
        for index in range(count):
            distance = sensor.read()
            if distance is None:
                print(f"{index:02d}  no echo — forward would be locked")
            else:
                print(f"{index:02d}  {distance * 100:6.1f} cm")
            if pause:
                time.sleep(pause)
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        sensor.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
