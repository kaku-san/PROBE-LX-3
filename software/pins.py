"""Pin map and tunables for Kakuji's rover.

Change numbers here, then restart the program. Nothing else has to be edited
unless you also want the wiring table in README.md to match.

Numbers are BCM (Broadcom) GPIO, which is what gpiozero expects. The physical
pin is the 40-pin header position, counting from pin 1 (3.3 V, the square pad)
at the outer corner of the header.

LEFT_EN (GPIO 18) and RIGHT_EN (GPIO 13) sit on different PWM channels
(PWM0 and PWM1). gpiozero on a Pi 5 uses software PWM and can drive any GPIO,
but if you later switch to hardware PWM, do not move RIGHT_EN onto GPIO 12.
GPIO 12 shares PWM0 with GPIO 18.

GPIO 2, 3, 14, and 15 are left free (I2C and the serial console).
"""

from __future__ import annotations

# Left N20 on L298N channel A (OUT1 / OUT2). IN_A high means "forward".
LEFT_IN1 = 17  # physical pin 11
LEFT_IN2 = 27  # physical pin 13
LEFT_EN = 18  # physical pin 12, PWM, ENA — remove the ENA jumper

# Right N20 on L298N channel B (OUT3 / OUT4).
RIGHT_IN3 = 22  # physical pin 15
RIGHT_IN4 = 23  # physical pin 16
RIGHT_EN = 13  # physical pin 33, PWM, ENB — remove the ENB jumper

# HC-SR04. ECHO is 5 V. It must go through the divider before it touches the Pi.
TRIG = 24  # physical pin 18
ECHO = 25  # physical pin 22, after the divider

# Header pins that are not GPIO.
PIN_5V_PHYSICAL = 2
PIN_GND_PHYSICAL = 6

# 1 kΩ from the sensor ECHO pin to the GPIO, 2 kΩ from that GPIO node to GND.
# 10 kΩ and 20 kΩ work too (same 1:2 ratio).
ECHO_SERIES_OHMS = 1000
ECHO_GND_OHMS = 2000

PHYSICAL = {
    LEFT_IN1: 11,
    LEFT_IN2: 13,
    LEFT_EN: 12,
    RIGHT_IN3: 15,
    RIGHT_IN4: 16,
    RIGHT_EN: 33,
    TRIG: 18,
    ECHO: 22,
}

# Duty cycle on ENA / ENB. 1.0 is full on. N20s on an L298N often need
# around 0.5 or more before they start, especially from a 5 V brick.
CRUISE_SPEED = 0.60
TURN_SPEED = 0.45
PWM_HZ = 1000

# Stop forward motion when the reading is below this. "Below" is strict:
# a reading equal to the threshold is still treated as clear.
STOP_DISTANCE_M = 0.20
# HC-SR04 readings under about 2 cm are in the blind zone. Treat them as
# "too close" rather than as a far, missing echo.
MIN_VALID_DISTANCE_M = 0.02
# How many clear readings in a row before forward is allowed again.
CLEAR_READINGS = 3
# Time between distance measurements. HC-SR04 wants a gap of about 60 ms.
SENSOR_POLL_S = 0.10
# Give up on an echo after this long (~5 m round trip at 343 m/s).
ECHO_TIMEOUT_S = 0.030

# Still size for scripts/capture.py. Preview on the Pi is rpicam-hello.
CAMERA_SIZE = (640, 480)


def gpio_pins() -> list[int]:
    """Every BCM number this stack drives, in wiring order."""
    return [LEFT_IN1, LEFT_IN2, LEFT_EN, RIGHT_IN3, RIGHT_IN4, RIGHT_EN, TRIG, ECHO]


def describe_lines() -> list[str]:
    """Plain-text wiring lines printed by scripts/check_env.py."""
    rows = [
        ("Left IN1", "L298N IN1", LEFT_IN1),
        ("Left IN2", "L298N IN2", LEFT_IN2),
        ("Left ENA", "L298N ENA, jumper removed", LEFT_EN),
        ("Right IN3", "L298N IN3", RIGHT_IN3),
        ("Right IN4", "L298N IN4", RIGHT_IN4),
        ("Right ENB", "L298N ENB, jumper removed", RIGHT_EN),
        ("TRIG", "HC-SR04 TRIG", TRIG),
        ("ECHO", "HC-SR04 ECHO via divider", ECHO),
    ]
    lines = [
        f"{name:<10} {dest:<32} BCM {bcm:<2}  physical pin {PHYSICAL[bcm]}"
        for name, dest, bcm in rows
    ]
    lines.append(
        f"HC-SR04 VCC to physical pin {PIN_5V_PHYSICAL} (5 V). The sensor wants 5 V."
    )
    lines.append(
        f"Common ground: motor-pack negative, L298N GND, sensor GND, Pi physical pin {PIN_GND_PHYSICAL}."
    )
    lines.append(
        f"Echo divider: {ECHO_SERIES_OHMS} ohm from ECHO to the GPIO, "
        f"{ECHO_GND_OHMS} ohm from the GPIO to ground."
    )
    return lines
