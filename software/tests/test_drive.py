"""Motor directions and the controller threads, using gpiozero mock pins."""

from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rover.controller import Rover, normalize_command
from rover.fakes import FakeRanger, mock_pin_factory
from rover.motors import DriveTrain
from rover.safety import SafetyGate


class DriveTrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.train = DriveTrain(pin_factory=mock_pin_factory())

    def tearDown(self) -> None:
        self.train.close()

    def test_directions(self) -> None:
        self.train.drive("forward", 0.6, 0.4)
        snap = self.train.snapshot()
        self.assertEqual(snap["left"], 1)
        self.assertEqual(snap["right"], 1)
        self.assertAlmostEqual(snap["left_speed"], 0.6)
        self.assertAlmostEqual(snap["right_speed"], 0.6)

        self.train.drive("back", 0.6, 0.4)
        snap = self.train.snapshot()
        self.assertEqual((snap["left"], snap["right"]), (-1, -1))

        self.train.drive("left", 0.6, 0.4)
        snap = self.train.snapshot()
        self.assertEqual((snap["left"], snap["right"]), (-1, 1))
        self.assertAlmostEqual(snap["left_speed"], 0.4)
        self.assertAlmostEqual(snap["right_speed"], 0.4)

        self.train.drive("right", 0.6, 0.4)
        snap = self.train.snapshot()
        self.assertEqual((snap["left"], snap["right"]), (1, -1))

        self.train.drive("stop", 0.6, 0.4)
        snap = self.train.snapshot()
        self.assertEqual(snap["left"], 0)
        self.assertEqual(snap["right"], 0)
        self.assertEqual(snap["left_speed"], 0)

    def test_speed_is_clamped(self) -> None:
        self.train.drive("forward", 5, 0.4)
        self.assertAlmostEqual(self.train.snapshot()["left_speed"], 1.0)
        self.train.drive("forward", -1, 0.4)
        self.assertEqual(self.train.snapshot()["left_speed"], 0.0)

    def test_unknown_command(self) -> None:
        with self.assertRaises(ValueError):
            self.train.drive("spin", 0.5, 0.5)


class CommandNameTests(unittest.TestCase):
    def test_aliases(self) -> None:
        self.assertEqual(normalize_command(" Backward "), "back")
        self.assertEqual(normalize_command("reverse"), "back")
        self.assertEqual(normalize_command("stop"), "stop")

    def test_rejects_unknown(self) -> None:
        with self.assertRaises(ValueError):
            normalize_command("fly")


def open_rover(distance: float, **kwargs) -> Rover:
    gate = SafetyGate(stop_distance_m=0.20, min_valid_m=0.02, clear_readings=1)
    gate.update(distance)
    return Rover(
        motors=DriveTrain(pin_factory=mock_pin_factory()),
        sensor=FakeRanger(distance),
        mock=True,
        gate=gate,
        poll_s=kwargs.get("poll_s", 0.02),
        start=True,
    )


class ControllerThreadTests(unittest.TestCase):
    def test_obstacle_stops_forward_and_still_allows_reverse(self) -> None:
        rover = open_rover(1.5, timeout_s=5.0)
        try:
            rover.command("forward")
            self.assertEqual(rover.motors.snapshot()["left"], 1)
            rover.sensor.distance_m = 0.05
            time.sleep(0.25)
            self.assertEqual(rover.motors.snapshot()["left"], 0)
            status = rover.status()
            self.assertTrue(status["blocked"])
            self.assertEqual(status["reason"], "obstacle")
            rover.command("back")
            snap = rover.motors.snapshot()
            self.assertEqual((snap["left"], snap["right"]), (-1, -1))
            rover.sensor.distance_m = 1.5
            time.sleep(0.25)
            self.assertFalse(rover.status()["blocked"])
            # Clearing the path does not restart the motors by itself.
            self.assertEqual(rover.motors.snapshot()["left"], -1)
            rover.command("forward")
            self.assertEqual(rover.motors.snapshot()["left"], 1)
        finally:
            rover.close()

    def test_latched_forward_continues_when_the_path_clears(self) -> None:
        rover = open_rover(1.5)
        try:
            rover.command("forward")
            rover.sensor.distance_m = 0.05
            time.sleep(0.25)
            self.assertEqual(rover.motors.snapshot()["left"], 0)
            rover.sensor.distance_m = 1.5
            time.sleep(0.25)
            self.assertFalse(rover.status()["blocked"])
            self.assertEqual(rover.motors.snapshot()["left"], 1)
            self.assertEqual(rover.status()["moving"], "forward")
        finally:
            rover.close()

    def test_forward_is_rejected_while_blocked(self) -> None:
        rover = open_rover(0.05)
        try:
            time.sleep(0.15)
            body = rover.command("forward")
            self.assertFalse(body["accepted"])
            self.assertEqual(rover.motors.snapshot()["left"], 0)
            body = rover.command("left")
            self.assertTrue(body["accepted"])
            self.assertEqual(rover.motors.snapshot()["left"], -1)
            self.assertEqual(rover.motors.snapshot()["right"], 1)
        finally:
            rover.close()


if __name__ == "__main__":
    unittest.main()
