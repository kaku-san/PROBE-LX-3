"""Drive session: latched command plus the HC-SR04 stop-before-hit gate.

A forward command stays in effect until you send stop (or the process exits).
If something is too close, the motors pause. When the path is clear again,
forward continues. Back and the in-place turns are not paused.
"""

from __future__ import annotations

import logging
import threading

import pins
from rover.fakes import FakeRanger, mock_pin_factory
from rover.motors import DriveTrain
from rover.preflight import env_flag
from rover.safety import SafetyGate
from rover.ultrasonic import HCSR04

log = logging.getLogger(__name__)

COMMANDS = frozenset({"forward", "back", "left", "right", "stop"})
ALIASES = {
    "backward": "back",
    "reverse": "back",
    "forwards": "forward",
    "front": "forward",
}


def normalize_command(cmd: str) -> str:
    name = cmd.strip().lower()
    name = ALIASES.get(name, name)
    if name not in COMMANDS:
        allowed = ", ".join(sorted(COMMANDS))
        raise ValueError(f"unknown command {cmd!r}; expected one of: {allowed}")
    return name


class Rover:
    def __init__(
        self,
        motors: DriveTrain,
        sensor,
        mock: bool = False,
        gate: SafetyGate | None = None,
        poll_s: float | None = None,
        start: bool = True,
    ) -> None:
        self.motors = motors
        self.sensor = sensor
        self.mock = mock
        self.gate = gate or SafetyGate(
            stop_distance_m=pins.STOP_DISTANCE_M,
            min_valid_m=pins.MIN_VALID_DISTANCE_M,
            clear_readings=pins.CLEAR_READINGS,
        )
        self._poll_s = pins.SENSOR_POLL_S if poll_s is None else poll_s
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._closed = False
        self._held = "stop"
        self._applied = "stop"
        self._accepted = True
        self._threads: list[threading.Thread] = []
        self._last_sensor_log = 0.0
        self._last_reason = "warmup"
        if start:
            self.start()

    @classmethod
    def create(cls) -> "Rover":
        mock = env_flag("ROVER_MOCK")
        if mock:
            motors = DriveTrain(pin_factory=mock_pin_factory())
            sensor = FakeRanger(1.5)
            log.info("ROVER_MOCK=1: mock pins and a fixed 1.5 m reading")
            return cls(motors, sensor, mock=True)
        return cls(DriveTrain(), HCSR04(), mock=False)

    def start(self) -> None:
        if self._threads:
            return
        thread = threading.Thread(target=self._safety_loop, name="rover-safety", daemon=True)
        thread.start()
        self._threads = [thread]

    def command(self, cmd: str) -> dict:
        name = normalize_command(cmd)
        with self._lock:
            self._held = name
            self._apply_locked()
            return self._status_locked()

    def status(self) -> dict:
        with self._lock:
            return self._status_locked()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._stop_event.set()
        try:
            self.motors.stop()
        except Exception:
            log.exception("stop during close failed")
        for thread in self._threads:
            thread.join(timeout=1.0)
        for part in (self.motors, self.sensor):
            try:
                part.close()
            except Exception:
                log.exception("close failed for %s", type(part).__name__)

    def _apply_locked(self) -> None:
        blocked = self.gate.snapshot().blocked
        if self._held == "forward" and blocked:
            desired = "stop"
            accepted = False
        else:
            desired = self._held
            accepted = True
        # Re-driving every poll drops the PWM pin for a moment. Only touch
        # the motors when the command or the gate result changed.
        if desired == self._applied and accepted == self._accepted:
            return
        if desired == "stop":
            self.motors.stop()
        else:
            self.motors.drive(desired, pins.CRUISE_SPEED, pins.TURN_SPEED)
        self._applied = desired
        self._accepted = accepted

    def _status_locked(self) -> dict:
        state = self.gate.snapshot()
        distance_cm = None if state.distance_m is None else round(state.distance_m * 100.0, 1)
        distance_m = None if state.distance_m is None else round(state.distance_m, 4)
        return {
            "requested": self._held,
            "moving": self._applied,
            "accepted": self._accepted,
            "blocked": state.blocked,
            "reason": state.reason,
            "message": state.message,
            "distance_m": distance_m,
            "distance_cm": distance_cm,
            "sensor_ok": state.reason != "sensor",
            "stop_distance_cm": round(self.gate.stop_distance_m * 100.0, 1),
            "cruise_speed": pins.CRUISE_SPEED,
            "mock": self.mock,
        }

    def _safety_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                reading = self.sensor.read()
                state = self.gate.update(reading)
                now_reason = state.reason
                if now_reason == "obstacle" and self._last_reason != "obstacle":
                    distance_cm = 0.0 if state.distance_m is None else state.distance_m * 100.0
                    log.info("stop-before-hit at %.0f cm", distance_cm)
                elif now_reason == "sensor" and self._last_reason != "sensor":
                    log.warning("HC-SR04 has no echo; forward paused")
                self._last_reason = now_reason
                with self._lock:
                    was = self._applied
                    self._apply_locked()
                    if was != "forward" and self._applied == "forward" and self._held == "forward":
                        log.info("path clear, continuing forward")
            except Exception:
                log.exception("safety loop error")
            self._stop_event.wait(self._poll_s)
