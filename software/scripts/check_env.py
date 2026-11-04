#!/usr/bin/env python3
"""Print versions and the pin table. Does not move motors or open GPIO."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pins
from rover.preflight import gpiozero_report, pi_model, picamera2_report


def main() -> int:
    print(f"Python {sys.version.split()[0]}")
    model = pi_model()
    on_pi = bool(model and "Raspberry Pi" in model)
    print(f"Board: {model or 'not a Raspberry Pi (no device-tree model)'}")
    gpio_ok, gpio_detail = gpiozero_report()
    cam_ok, cam_detail = picamera2_report()
    print(f"gpiozero: {'OK' if gpio_ok else 'MISSING'} — {gpio_detail}")
    print(f"picamera2: {'OK' if cam_ok else 'MISSING'} — {cam_detail}")
    print()
    print("Wiring from software/pins.py (BCM numbers, gpiozero):")
    for line in pins.describe_lines():
        print(" ", line)
    print()
    print("Remove the L298N ENA and ENB jumpers before those wires touch the Pi.")
    print("Do not connect the HC-SR04 ECHO pin straight to a GPIO pin.")
    if not gpio_ok:
        return 1
    if on_pi and not cam_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
