"""HC-SR04 distance, timed with gpiozero pins.

gpiozero's DistanceSensor reports its max range when no echo comes back, which
looks the same as "nothing is nearby". This reader returns None on a timeout
so the safety gate can lock forward motion when the sensor is unplugged or
the echo wire is dead.

The echo pin on the sensor is 5 V. The Pi pin named in pins.ECHO must be the
midpoint of the two 1 kΩ resistors (nominal 2.5 V high).
"""

from __future__ import annotations

import logging
import time

import pins

log = logging.getLogger(__name__)

try:
    from gpiozero import DigitalInputDevice, DigitalOutputDevice
except ImportError as exc:  # pragma: no cover - same install path as motors.py
    raise ImportError(
        "gpiozero is required, and RPi.GPIO does not work on Pi 5. "
        "Install it with: sudo apt install python3-gpiozero python3-lgpio"
    ) from exc

# About 20 °C. A few degrees either way moves a 20 cm reading by millimetres.
SPEED_OF_SOUND_M_S = 343.0


def distance_m_from_echo_s(echo_high_s: float) -> float:
    """Convert the echo-high time (round trip) into metres."""
    if echo_high_s < 0:
        raise ValueError("echo duration must be >= 0")
    return (echo_high_s * SPEED_OF_SOUND_M_S) / 2.0


class HCSR04:
    def __init__(
        self,
        trigger: int | None = None,
        echo: int | None = None,
        pin_factory=None,
        echo_timeout_s: float | None = None,
        settle_s: float | None = None,
    ) -> None:
        self._trigger = None
        self._echo = None
        self._timeout = pins.ECHO_TIMEOUT_S if echo_timeout_s is None else echo_timeout_s
        self._closed = False
        trigger_pin = pins.TRIG if trigger is None else trigger
        echo_pin = pins.ECHO if echo is None else echo
        try:
            self._trigger = DigitalOutputDevice(trigger_pin, pin_factory=pin_factory)
            # pull_up=False enables the pulldown. Echo idles low.
            self._echo = DigitalInputDevice(echo_pin, pull_up=False, pin_factory=pin_factory)
        except Exception as exc:
            self.close()
            raise RuntimeError(
                "Could not open the HC-SR04 pins. Check TRIG and ECHO in "
                "software/pins.py. The echo wire must go through the resistor "
                "divider, not straight into the Pi. "
                f"Original error: {exc}"
            ) from exc
        settle = 0.05 if settle_s is None else settle_s
        if settle > 0:
            time.sleep(settle)

    def read(self) -> float | None:
        """Return metres, or None if the echo never arrives."""
        trigger = self._trigger
        echo = self._echo
        try:
            trigger.off()
            time.sleep(2e-6)
            trigger.on()
            time.sleep(10e-6)
            trigger.off()

            deadline = time.monotonic() + self._timeout
            while not echo.is_active:
                if time.monotonic() >= deadline:
                    return None
            start = time.monotonic()
            while echo.is_active:
                if time.monotonic() >= deadline:
                    return None
            end = time.monotonic()
        except Exception:
            log.exception("HC-SR04 read failed")
            return None
        finally:
            try:
                trigger.off()
            except Exception:
                log.debug("trigger off failed", exc_info=True)
        return distance_m_from_echo_s(end - start)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        for device in (self._trigger, self._echo):
            if device is None:
                continue
            try:
                device.close()
            except Exception:
                log.debug("GPIO close failed", exc_info=True)
