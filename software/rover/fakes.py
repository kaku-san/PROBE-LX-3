"""In-process stand-ins so the drive logic can run without a rover attached."""

from __future__ import annotations


class FakeRanger:
    """Distance sensor whose reading is whatever `distance_m` is set to.

    `None` means "no echo", which the safety gate treats as a fault.
    """

    def __init__(self, distance_m: float | None = 1.5) -> None:
        self.distance_m = distance_m

    def read(self) -> float | None:
        return self.distance_m

    def close(self) -> None:
        return None


def mock_pin_factory():
    """gpiozero mock pins that accept PWM, for tests and ROVER_MOCK."""
    from gpiozero.pins.mock import MockFactory, MockPWMPin

    return MockFactory(pin_class=MockPWMPin)
