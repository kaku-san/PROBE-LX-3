"""Distance math and the stop-before-hit gate. No motors."""

from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rover.fakes import mock_pin_factory
from rover.safety import SafetyGate
from rover.ultrasonic import HCSR04, SPEED_OF_SOUND_M_S, distance_m_from_echo_s


class DistanceMathTests(unittest.TestCase):
    def test_twenty_centimetres(self) -> None:
        seconds = (2 * 0.20) / SPEED_OF_SOUND_M_S
        self.assertAlmostEqual(distance_m_from_echo_s(seconds), 0.20, places=9)

    def test_zero_echo_is_zero_distance(self) -> None:
        self.assertEqual(distance_m_from_echo_s(0.0), 0.0)

    def test_negative_echo_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            distance_m_from_echo_s(-0.01)


class SafetyGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = SafetyGate(stop_distance_m=0.20, min_valid_m=0.02, clear_readings=3)

    def test_starts_locked(self) -> None:
        state = self.gate.snapshot()
        self.assertTrue(state.blocked)
        self.assertEqual(state.reason, "warmup")

    def test_needs_three_clear_readings(self) -> None:
        self.assertTrue(self.gate.update(1.0).blocked)
        self.assertTrue(self.gate.update(1.0).blocked)
        state = self.gate.update(1.0)
        self.assertFalse(state.blocked)
        self.assertEqual(state.reason, "ok")
        self.assertIn("Path clear", state.message)

    def test_close_reading_locks_and_resets_the_streak(self) -> None:
        self.gate.update(1.0)
        self.gate.update(1.0)
        state = self.gate.update(0.10)
        self.assertTrue(state.blocked)
        self.assertEqual(state.reason, "obstacle")
        self.assertIn("10 cm", state.message)
        self.assertTrue(self.gate.update(1.0).blocked)
        self.assertEqual(self.gate.snapshot().reason, "clearing")
        self.assertTrue(self.gate.update(1.0).blocked)
        self.assertFalse(self.gate.update(1.0).blocked)

    def test_missing_echo_locks_forward(self) -> None:
        self.gate.update(1.0)
        self.gate.update(1.0)
        self.gate.update(1.0)
        state = self.gate.update(None)
        self.assertTrue(state.blocked)
        self.assertEqual(state.reason, "sensor")
        self.assertIsNone(state.distance_m)

    def test_blind_zone_counts_as_too_close(self) -> None:
        state = self.gate.update(0.01)
        self.assertEqual(state.reason, "obstacle")

    def test_exact_threshold_is_not_below(self) -> None:
        state = self.gate.update(0.20)
        self.assertEqual(state.reason, "warmup")
        self.assertTrue(state.blocked)


class UltrasonicTimeoutTests(unittest.TestCase):
    def test_no_echo_returns_none(self) -> None:
        sensor = HCSR04(
            pin_factory=mock_pin_factory(),
            echo_timeout_s=0.05,
            settle_s=0,
        )
        try:
            started = time.monotonic()
            self.assertIsNone(sensor.read())
            elapsed = time.monotonic() - started
        finally:
            sensor.close()
        self.assertGreaterEqual(elapsed, 0.03)
        self.assertLess(elapsed, 0.5)


if __name__ == "__main__":
    unittest.main()
