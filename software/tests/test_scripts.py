"""The bring-up scripts run in mock mode without GPIO hardware."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScriptTests(unittest.TestCase):
    def _run(self, script: str, extra_env: dict | None = None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["ROVER_MOCK"] = "1"
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script)],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_check_env(self) -> None:
        result = self._run("check_env.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gpiozero: OK", result.stdout)
        self.assertIn("BCM 17", result.stdout)
        self.assertIn("physical pin 11", result.stdout)

    def test_check_distance_mock(self) -> None:
        result = self._run("check_distance.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("42.0 cm", result.stdout)

    def test_motor_test_mock(self) -> None:
        result = self._run("motor_test.py")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("forward", result.stdout)
        self.assertIn("left=1", result.stdout)
        self.assertIn("motors off", result.stdout)

    def test_motor_test_refuses_a_non_interactive_real_run(self) -> None:
        env = os.environ.copy()
        env.pop("ROVER_MOCK", None)
        env.pop("ROVER_YES", None)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "motor_test.py")],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            stdin=subprocess.DEVNULL,
        )
        # No TTY and no ROVER_YES: do not pulse real motors.
        # On a machine without GPIO the pin open can also fail; either outcome
        # must happen before a long motor pulse, and must be a non-zero exit
        # when stdin is closed and mock mode is off. A missing pin factory
        # raises before the hold loop. Accept the explicit refusal (exit 2)
        # or a GPIO open failure (exit 1 via traceback). Never exit 0.
        self.assertNotEqual(result.returncode, 0, result.stdout)
        combined = result.stdout + result.stderr
        self.assertTrue(
            "Refusing to move motors" in combined or "Could not open the L298N" in combined,
            combined,
        )

    def test_drive_stop_and_timed_forward(self) -> None:
        env = os.environ.copy()
        env["ROVER_MOCK"] = "1"
        stop_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "drive.py"), "stop"],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(stop_run.returncode, 0, stop_run.stderr)
        self.assertIn("motors stopped", stop_run.stdout)
        timed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "drive.py"), "forward", "--seconds", "0.8"],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(timed.returncode, 0, timed.stderr + timed.stdout)
        self.assertIn("requested=forward", timed.stdout)
        self.assertIn("motors stopped", timed.stdout)

    def test_drive_interactive_quit_and_bad_command(self) -> None:
        env = os.environ.copy()
        env["ROVER_MOCK"] = "1"
        session = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "drive.py")],
            cwd=ROOT,
            env=env,
            input="status\nquit\n",
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(session.returncode, 0, session.stderr + session.stdout)
        self.assertIn("motors stopped", session.stdout)
        bad = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "drive.py"), "fly"],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn("motors stopped", bad.stdout)

    def test_capture_mock(self) -> None:
        dest = Path("/tmp/kakuji-mock-photo.jpg")
        if dest.exists():
            dest.unlink()
        env = os.environ.copy()
        env["ROVER_MOCK"] = "1"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "capture.py"), str(dest)],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(dest.read_bytes().startswith(b"\xff\xd8"))
        missing = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "capture.py")],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(missing.returncode, 2)


if __name__ == "__main__":
    unittest.main()
