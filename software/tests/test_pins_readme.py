"""Pin map stays unique, and the README table matches pins.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pins

BANNED_SNIPPETS = (
    "adafruit_motorkit",
    "VL53L1X",
    "MotorKit",
)

TABLE_ROWS = {
    "Left IN1": pins.LEFT_IN1,
    "Left IN2": pins.LEFT_IN2,
    "Left ENA": pins.LEFT_EN,
    "Right IN3": pins.RIGHT_IN3,
    "Right IN4": pins.RIGHT_IN4,
    "Right ENB": pins.RIGHT_EN,
    "TRIG": pins.TRIG,
    "ECHO": pins.ECHO,
}


def pin_table(readme: str) -> dict[str, tuple[int, int]]:
    found: dict[str, tuple[int, int]] = {}
    for line in readme.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or not cells[2].isdigit() or not cells[3].isdigit():
            continue
        found[cells[0]] = (int(cells[2]), int(cells[3]))
    return found


class PinMapTests(unittest.TestCase):
    def test_gpio_numbers_are_unique_and_mapped(self) -> None:
        used = pins.gpio_pins()
        self.assertEqual(len(used), len(set(used)))
        self.assertEqual(set(used), set(pins.PHYSICAL))
        self.assertEqual(len(set(pins.PHYSICAL.values())), len(pins.PHYSICAL))
        for bcm, physical in pins.PHYSICAL.items():
            self.assertGreaterEqual(bcm, 2)
            self.assertLessEqual(bcm, 27)
            self.assertGreaterEqual(physical, 1)
            self.assertLessEqual(physical, 40)

    def test_stop_distance_is_beyond_the_blind_zone(self) -> None:
        self.assertGreater(pins.STOP_DISTANCE_M, pins.MIN_VALID_DISTANCE_M)
        self.assertGreaterEqual(pins.CLEAR_READINGS, 1)
        self.assertGreater(pins.CRUISE_SPEED, 0)
        self.assertLessEqual(pins.CRUISE_SPEED, 1)

    def test_describe_lines_mention_every_pin(self) -> None:
        text = "\n".join(pins.describe_lines())
        for bcm in pins.gpio_pins():
            self.assertIn(f"BCM {bcm}", text)
        self.assertIn(str(pins.PIN_5V_PHYSICAL), text)
        self.assertIn(str(pins.ECHO_SERIES_OHMS), text)
        self.assertIn(str(pins.ECHO_GND_OHMS), text)


class ReadmeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_readme_matches_pin_constants(self) -> None:
        found = pin_table(self.readme)
        for label, bcm in TABLE_ROWS.items():
            self.assertIn(label, found, label)
            self.assertEqual(found[label], (bcm, pins.PHYSICAL[bcm]))

    def test_readme_has_bringup_and_adaptation_note(self) -> None:
        text = self.readme
        stop_cm = int(round(pins.STOP_DISTANCE_M * 100))
        self.assertIn(f"{stop_cm} cm", text)
        self.assertIn("Kakuji", text)
        self.assertIn("not stock PROBE wiring", text)
        self.assertIn("L298N", text)
        self.assertIn("HC-SR04", text)
        self.assertIn("Camera Module 3", text)
        self.assertIn("gpiozero", text)
        self.assertIn("picamera2", text)
        self.assertIn("RPi.GPIO", text)
        self.assertIn("./scripts/run.sh", text)
        self.assertIn("scripts/drive.py", text)
        self.assertIn("scripts/capture.py", text)
        self.assertIn("1 kΩ", text)
        self.assertIn("2 kΩ", text)
        lowered = text.lower()
        self.assertNotIn("flask", lowered)
        self.assertNotIn("systemctl", lowered)


class SourceTests(unittest.TestCase):
    def test_python_does_not_use_other_hardware_libraries(self) -> None:
        for path in ROOT.rglob("*.py"):
            if "tests" in path.relative_to(ROOT).parts:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?m)^\s*(import RPi|from RPi\b|import flask|from flask)")
            self.assertNotIn("flask", text.lower(), str(path))
            for snippet in BANNED_SNIPPETS:
                self.assertNotIn(snippet, text, f"{snippet} in {path}")


if __name__ == "__main__":
    unittest.main()
