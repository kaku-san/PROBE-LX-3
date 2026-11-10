# PROBE LX-3 | Pi 5 build handover

**10 November 2026. Resume at the first motor mount.** The Pi, camera, first distance sensor and both motors worked on the bench. The builder reports that the wheels fit the shafts and that the last prints are finished. The latest physical check still outstanding is a gearbox held securely on the **full** drive plate, with its wheel clear of the plastic.

**First action for the next agent.** With the motor adapter unplugged and the Pi shut down and disconnected from USB-C, have the builder place one motor on the adapted plate. The wheel faces out, the wires face in and the printed cap sits over the brass gearbox. Check for at least 1 mm of clearance between the wheel and the printed arm and that the encoder plug clears the plate. If the screws are missing, do the hand fit with power off. Give the builder one picture and a batch of steps in plain English. One angled photo of both mounts is enough to discuss the fit. [Motor mounting picture](build-images/assembly-01-motors.png)

## What has actually been tested

| Item | Evidence | Next physical check |
| --- | --- | --- |
| Pi 5 + active cooler | Pi booted, SSH worked, and the environment check passed. | Recheck power and GPIO state before movement after a reboot. |
| Camera Module 3 | The Pi detected the IMX708 and captured an image. | Check lens clearance, retention, ribbon routing and the image with the dome in place. |
| HC-SR04 #1 | At 6.5 in (16.51 cm), 30/30 echoes were 16.7–16.8 cm. At 12.5 in (31.75 cm), 30/30 were 31.5–32.8 cm. With the box removed, all 30 samples returned **no echo**. | Mount it facing forward and repeat the two-distance check. The second sensor is deferred. |
| Two JGA12-N20 6 V, 150 RPM motors and L298N ZX-040 | On 5 Nov, A, B and both together moved in separate 250 ms unloaded tests. Each command exited successfully and all six controls read LOW afterward. | Check direction with the wheels raised after mounting. Reverse, encoder feedback, torque under load and floor driving are unverified. |
| Printed hardware | Builder reports base, tray, dome and final batch complete. Wheel-to-shaft fit was reported. | Check both caps, wheel/skid contact, chassis fasteners and camera fit. No post-assembly drive has been reported. |

## Wiring to preserve

Numbers in the last column are **physical positions** on the Pi's 40-pin header. BCM is the numbering used by the software. [Motor pin map](build-images/motor-seven-control-wires.svg) · [Sensor pin map](build-images/sensor-full-pin-map.svg)

| Connection | Wire | BCM | Physical pin |
| --- | --- | ---: | ---: |
| Motor A, ENA / IN1 / IN2 | Purple / yellow / orange | 18 / 17 / 27 | 12 / 11 / 13 |
| Motor B, ENB / IN3 / IN4 | Grey / green / blue | 13 / 22 / 23 | 33 / 15 / 16 |
| Motor supply common ground, spare breakout − to Pi GND | Black | — | 14 |
| Sensor VCC / sensor ground row to Pi GND | Yellow / black (sensor GND itself is green) | — | 2 / 6 |
| Sensor TRIG | Brown | 24 | 18 |
| Sensor ECHO divider midpoint | Blue | 25 | 22 |

**Echo divider.** White sensor ECHO → 1 kΩ → shared row with the blue Pi lead → 1 kΩ → ground. Each shared breadboard row uses separate holes on the same side of the center gap. Equal resistors give about 2.5 V from a 5 V echo. The early handoff's 1 kΩ above / 10 kΩ below would deliver about 4.55 V to the Pi GPIO and must not be used.

**Motor power on the bench.** The Pi used its own USB-C supply. A separate SEM S530P2N1, 5 V DC / 3 A, centre-positive adapter fed a Robu R216508 barrel breakout. Two breakout + pins fed driver VM (red, terminal marked +12V) and driver logic +5V (orange). Breakout − connected to driver GND and Pi physical 14. All three caps were removed: ENA, ENB and regulator-enable. Motor A red/white went to OUT1/OUT2, motor B red/white to OUT3/OUT4. The four encoder leads on each motor were unused; keep their tips individually insulated. The driver’s +12V label does **not** change the supply voltage for this hookup.

## Printed parts, fasteners and remaining work

The adapted five-piece batch contains one drive plate with built-in motor seats and front skid, two motor caps, a Camera Module 3 carrier and a keeper. The two 34 mm wheels are purchased. Stock shell instructions still apply at the base/tray interface. The adapted plate uses the printed caps and skid in place of the stock motor brackets and caster. [Adapted STLs and editable print project](../hardware/pi5-skid/README.md) · [Assembly pictures and English audio](build-images/README.md)

1. **Secure both motors.** Slide two plain M3 nuts into each arm's side slots and use **two M3 × 8 mm screws per cap**, measured under the head. Tighten evenly until the motor stays put. The M3 pillar kit's screw lengths are unconfirmed. Once secure, flip the plate onto a smooth surface. Both wheels and the skid should touch, and each wheel should clear the arm.
2. **Join the chassis.** Route motor leads through the matching slots. Set the bowl on the drive plate and the tray in the bowl with posts facing up. Four **M3 × 10 mm** button-head screws go upward through plate and bowl into four **M3 × 4 × 5 mm heat-set inserts** under the tray. Check that the inserts and screws are available. Dry-fit the stack if they're missing.
3. **Fit camera and electronics.** Try the keeper on the empty carrier first. With power disconnected, slide the camera into its grooves, lens forward, connector down. Fit the keeper to the frame and leave a loose bend in the ribbon. Mount the Pi, driver and divider on insulated supports with clearance for the fan, terminals and shell. The stock X1200 stack's Pi screw lengths do not establish the right length for the bare Pi and cooler.
4. **Make the ultrasonic mount.** The HC-SR04 has no holder in the five-piece batch. Measure the actual board, spacing and diameter of both round heads, connector clearance and available front space before designing the holder. Check the dome twist, keep both ultrasonic faces exposed and leave the camera's view clear.
5. **Test the assembled rover.** Support it with the wheels clear. Start the Pi with the motor adapter disconnected, set/verify all controls LOW, then use brief supervised pulses. Confirm the two wheels would propel the rover in the same direction. Check camera and sensor while stationary. Close the dome after cables and boards are secure.
6. **Qualify onboard power, then drive.** The wall-powered test did not validate batteries. Identify the actual pack topology, protection, regulator and charger, then verify the regulated outputs before connecting the Pi or driver. The builder's meter was missing its probes. After a successful raised-wheel test on the onboard supply, try one short move and stop on a clear floor. Autonomous/local-brain work comes later.

## Software and resuming on the Pi

The original Pi checkout was at `72a04b4`. Confirm the revision actually present on the Pi before relying on newly published files. The real sensor run succeeded from a writable working directory because the Pi checkout was root-owned and `lgpio` needed to create a notification FIFO. From a checkout that contains this handover, the following runs the **sensor only**:

```sh
repo=$(git rev-parse --show-toplevel)
cd /tmp
env -u ROVER_MOCK GPIOZERO_PIN_FACTORY=lgpio python3 -u "$repo/software/scripts/check_distance.py"
```

The [bench helper](../software/scripts/motor_bench_pulse.py) defaults to actively setting all six controls LOW. It uses real `lgpio` and `pinctrl` on the Pi. Run it from a writable directory, with no competing motor-control process. For a deliberate unloaded/raised test with the builder ready, `--motor A`, `--motor B` or `--motor both` each request one 250 ms pulse per selected enable. Verify all six outputs LOW afterward. A reboot or another GPIO program changes the state. The general drive CLI and longer motor-test sequence in the [software guide](../software/README.md) have separate behavior.

The original CAD, derived hardware and illustrations credit LUMALIEN under [CC BY-SA 4.0](../LICENSE). The rover software uses the [MIT license](../software/LICENSE).
