#!/usr/bin/env python3
"""Pulse both N20s through the L298N. Lift the rover first.

Forward should roll both wheels toward the camera end of the body. If the
rover would spin in a circle, swap the two screws of the wheel that went
backward. If both wheels roll the wrong way, swap both pairs.

    python3 scripts/motor_test.py
    ROVER_YES=1 python3 scripts/motor_test.py
    ROVER_MOCK=1 python3 scripts/motor_test.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pins
from rover.fakes import mock_pin_factory
from rover.motors import DriveTrain
from rover.preflight import env_flag

HOLDS = (
    ("forward", 0.5),
    ("stop", 0.3),
    ("back", 0.5),
    ("stop", 0.3),
    ("left", 0.4),
    ("stop", 0.2),
    ("right", 0.4),
    ("stop", 0.2),
)


def confirm(mock: bool) -> None:
    if mock or env_flag("ROVER_YES"):
        return
    if not sys.stdin.isatty():
        print(
            "Refusing to move motors without a terminal. Set ROVER_YES=1 to override.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    print("Lift the rover so the wheels are off the ground.")
    print("ENA and ENB jumpers must be removed.")
    input("Press Enter to pulse the motors, or Ctrl+C to abort. ")


def main() -> int:
    mock = env_flag("ROVER_MOCK")
    confirm(mock)
    factory = mock_pin_factory() if mock else None
    train = DriveTrain(pin_factory=factory)
    scale = 0.02 if mock else 1.0
    try:
        for command, seconds in HOLDS:
            print(command)
            train.drive(command, pins.CRUISE_SPEED, pins.TURN_SPEED)
            if mock:
                snap = train.snapshot()
                print(
                    f"  left={snap['left']} right={snap['right']} "
                    f"speed={snap['left_speed']:.2f}/{snap['right_speed']:.2f}"
                )
            time.sleep(seconds * scale)
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        train.stop()
        train.close()
    print("motors off")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
