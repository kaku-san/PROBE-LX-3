"""Two N20 gear motors on one L298N, driven by gpiozero.

Each channel is the L298N truth table:

    IN_A   IN_B   EN     result
    high   low    PWM    forward
    low    high   PWM    backward
    low    low    0      stop (coast)

IN_A / IN_B are IN1 / IN2 for the left motor and IN3 / IN4 for the right.
EN is ENA or ENB. The board's ENA and ENB jumpers must be removed, or those
pins are tied to 5 V.
"""

from __future__ import annotations

import logging

import pins

log = logging.getLogger(__name__)

try:
    from gpiozero import DigitalOutputDevice, PWMOutputDevice
except ImportError as exc:  # pragma: no cover - exercised on a bare Pi image
    raise ImportError(
        "gpiozero is required, and RPi.GPIO does not work on Pi 5. "
        "Install it with: sudo apt install python3-gpiozero python3-lgpio"
    ) from exc


def _clamp(speed: float) -> float:
    return max(0.0, min(1.0, float(speed)))


class MotorChannel:
    """One L298N half: two direction pins and one PWM enable."""

    def __init__(
        self,
        in_a: int,
        in_b: int,
        enable: int,
        pin_factory=None,
    ) -> None:
        self._in_a = None
        self._in_b = None
        self._en = None
        self._closed = False
        try:
            self._in_a = DigitalOutputDevice(in_a, pin_factory=pin_factory)
            self._in_b = DigitalOutputDevice(in_b, pin_factory=pin_factory)
            self._en = PWMOutputDevice(
                enable,
                frequency=pins.PWM_HZ,
                pin_factory=pin_factory,
            )
        except Exception:
            self.close()
            raise

    def forward(self, speed: float) -> None:
        self._run(forward=True, speed=speed)

    def backward(self, speed: float) -> None:
        self._run(forward=False, speed=speed)

    def _run(self, forward: bool, speed: float) -> None:
        # Drop the enable before flipping direction so the motor cannot
        # get a full-speed pulse in the old direction.
        self._en.value = 0
        if forward:
            self._in_a.on()
            self._in_b.off()
        else:
            self._in_a.off()
            self._in_b.on()
        self._en.value = _clamp(speed)

    def stop(self) -> None:
        if self._en is not None:
            self._en.value = 0
        if self._in_a is not None:
            self._in_a.off()
        if self._in_b is not None:
            self._in_b.off()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self.stop()
        for device in (self._en, self._in_a, self._in_b):
            if device is None:
                continue
            try:
                device.close()
            except Exception:
                log.debug("GPIO close failed", exc_info=True)

    @property
    def direction(self) -> int:
        """1 forward, -1 backward, 0 stopped or braking."""
        a_on = bool(self._in_a is not None and self._in_a.is_active)
        b_on = bool(self._in_b is not None and self._in_b.is_active)
        if a_on and not b_on:
            return 1
        if b_on and not a_on:
            return -1
        return 0

    @property
    def speed(self) -> float:
        if self._en is None:
            return 0.0
        return float(self._en.value)


class DriveTrain:
    """Differential drive. Left and right use the same pin convention.

    If Forward makes the rover spin in a circle, one motor is electrically
    backwards: swap that motor's two screws on the L298N. If both wheels roll
    the wrong way, swap both pairs (or swap each channel's IN pins in pins.py).
    "Forward" means toward the camera, which is the front of the PROBE body.
    The motors sit at the rear.
    """

    def __init__(self, pin_factory=None) -> None:
        self._left: MotorChannel | None = None
        self._right: MotorChannel | None = None
        try:
            self._left = MotorChannel(
                pins.LEFT_IN1, pins.LEFT_IN2, pins.LEFT_EN, pin_factory=pin_factory
            )
            self._right = MotorChannel(
                pins.RIGHT_IN3, pins.RIGHT_IN4, pins.RIGHT_EN, pin_factory=pin_factory
            )
        except Exception as exc:
            self.close()
            raise RuntimeError(
                "Could not open the L298N GPIO pins. On a Pi 5 install "
                "python3-gpiozero and python3-lgpio, and run as a user in the "
                "gpio group. To move a wire, edit software/pins.py. "
                f"Original error: {exc}"
            ) from exc

    def drive(self, command: str, cruise: float, turn: float) -> None:
        if command == "stop":
            self.stop()
        elif command == "forward":
            self._left.forward(cruise)
            self._right.forward(cruise)
        elif command == "back":
            self._left.backward(cruise)
            self._right.backward(cruise)
        elif command == "left":
            # Turn in place: left wheel back, right wheel forward.
            self._left.backward(turn)
            self._right.forward(turn)
        elif command == "right":
            self._left.forward(turn)
            self._right.backward(turn)
        else:
            raise ValueError(f"unknown drive command {command!r}")

    def stop(self) -> None:
        if self._left is not None:
            self._left.stop()
        if self._right is not None:
            self._right.stop()

    def close(self) -> None:
        self.stop()
        for channel in (self._left, self._right):
            if channel is not None:
                channel.close()

    def snapshot(self) -> dict[str, float]:
        return {
            "left": self._left.direction,
            "right": self._right.direction,
            "left_speed": self._left.speed,
            "right_speed": self._right.speed,
        }
