"""Stop-before-hit gate.

Forward is locked until several readings in a row are at or beyond the stop
distance. A missing echo locks forward as well. Back and the in-place turns
are not locked here; the rover controller decides which commands to drop.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyState:
    blocked: bool
    reason: str
    distance_m: float | None
    message: str


class SafetyGate:
    def __init__(
        self,
        stop_distance_m: float,
        min_valid_m: float,
        clear_readings: int,
    ) -> None:
        if clear_readings < 1:
            raise ValueError("clear_readings must be at least 1")
        if not (0 <= min_valid_m < stop_distance_m):
            raise ValueError("min valid distance must be below the stop distance")
        self.stop_distance_m = float(stop_distance_m)
        self.min_valid_m = float(min_valid_m)
        self.clear_readings = int(clear_readings)
        self._clear_count = 0
        self._lock = threading.Lock()
        self._state = self._compose("warmup", None, True)

    def update(self, distance_m: float | None) -> SafetyState:
        with self._lock:
            if distance_m is None or distance_m < 0:
                self._clear_count = 0
                self._state = self._compose("sensor", None, True)
                return self._state
            if distance_m < self.min_valid_m or distance_m < self.stop_distance_m:
                self._clear_count = 0
                self._state = self._compose("obstacle", distance_m, True)
                return self._state
            self._clear_count += 1
            if self._clear_count >= self.clear_readings:
                self._state = self._compose("ok", distance_m, False)
                return self._state
            if self._state.reason in {"obstacle", "clearing"}:
                reason = "clearing"
            else:
                reason = "warmup"
            self._state = self._compose(reason, distance_m, True)
            return self._state

    def snapshot(self) -> SafetyState:
        with self._lock:
            return self._state

    def _compose(self, reason: str, distance_m: float | None, blocked: bool) -> SafetyState:
        stop_cm = self.stop_distance_m * 100.0
        if reason == "ok":
            message = "Path clear."
        elif reason == "obstacle":
            seen = "too close" if distance_m is None else f"{distance_m * 100:.0f} cm"
            message = (
                f"Something is {seen} ahead. Forward locks under {stop_cm:.0f} cm. "
                "Back up or turn."
            )
        elif reason == "sensor":
            message = (
                "No echo from the HC-SR04. Forward is locked. "
                "Check 5 V, ground, the trigger wire, and the echo divider."
            )
        elif reason == "clearing":
            message = "Path is clearing. Forward stays locked for a moment."
        else:
            message = (
                "Checking the space ahead. Forward stays locked until the path looks clear."
            )
        return SafetyState(
            blocked=blocked,
            reason=reason,
            distance_m=distance_m,
            message=message,
        )
