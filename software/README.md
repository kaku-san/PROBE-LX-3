# Kakuji drive software

This is Kakuji's Raspberry Pi 5 adaptation with an L298N, one HC-SR04 and a Camera Module 3.

It is a small Python program for a Raspberry Pi 5. You drive two N20 gear motors through an L298N from the terminal. An HC-SR04 pauses forward motion when something is too close. A separate command saves one JPEG from the Camera Module 3.

The [Pi 5 build handover](../docs/PI5-BUILD-HANDOVER.md) records the physical build, bench results and remaining fit checks. Use the wiring below for this adaptation. The original hardware guide describes the Adafruit bonnet, VL53L1X and USB Arducam. The adapted print set includes a Camera Module 3 carrier and keeper. The ultrasonic sensor needs a separate mount.

## Parts this program expects

| Part | How the software talks to it |
| --- | --- |
| Raspberry Pi 5 (8 GB is fine; any Pi 5 works) | Raspberry Pi OS Bookworm, 64-bit |
| Camera Module 3 on the CSI port | `picamera2` for one JPEG. Preview with `rpicam-hello`. |
| 2× N20 gear motors | The two outputs of the L298N |
| L298N motor driver | Six GPIO pins via `gpiozero` |
| HC-SR04 ultrasonic sensor | Trigger and echo GPIO pins |
| Separate Pi USB-C supply and regulated 5 V DC, 3 A motor adapter | Shared ground through Pi physical pin 14 |

`RPi.GPIO` does not work on a Pi 5. This project uses `gpiozero` (2.0 or newer) on purpose.

You do not need a Jetson, an Adafruit motor bonnet, a VL53L1X, a USB camera, a lidar, or an audio HAT for this program.

## Install on the Pi

On a Pi running **Raspberry Pi OS Bookworm (64-bit)**, install the dependencies:

```sh
sudo apt update
sudo apt install -y python3-gpiozero python3-lgpio python3-picamera2 rpicam-apps
```

Leave `GPIOZERO_PIN_FACTORY` unset. Bookworm's `gpiozero` uses the Pi 5 GPIO driver (`lgpio`) by itself.

The default user can already use GPIO and the camera. If you created an extra user and the programs say permission denied:

```sh
sudo usermod -aG gpio,video,render "$USER"
```

Log out and back in afterwards.

Check the install. This does not move the motors:

```sh
cd software
python3 scripts/check_env.py
```

You want `gpiozero: OK` and `picamera2: OK`.

`requirements.txt` installs `gpiozero` for laptop simulations of the drive stack. The standalone bench pulse tool requires Raspberry Pi OS, real `lgpio` and `pinctrl`. On the Pi, install `picamera2` from apt to match the camera stack.

### Try the commands on a laptop

```sh
cd software
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
ROVER_MOCK=1 .venv/bin/python scripts/drive.py stop
```

## Wire it

Shut down the Pi and unplug both supplies before changing wires. Pi GPIO inputs are rated for 3.3 V.

> Remove the **ENA**, **ENB** and **5V-EN regulator** caps for this hookup. With the ZX-040 heatsink at the top, use the six outer control posts in order: ENA, IN1, IN2, IN3, IN4, ENB. The two inner posts behind ENA and ENB carry +5 V. Leave both empty.

> Do not connect the HC-SR04 **ECHO** pin straight to the Pi. ECHO is a 5 V output. Put the divider on it first.

### Pin table

BCM numbers select GPIO lines in software. Physical numbers identify header positions. With USB/Ethernet sockets at the top, components up and the header on the left, physical pin 2 is bottom-left and pin 1 is bottom-right. The drive stack reads `pins.py`. The standalone bench pulse helper is fixed to the verified wiring shown here.

| Signal | Connects to | BCM | Physical pin |
| --- | --- | --- | --- |
| Left IN1 | L298N IN1 | 17 | 11 |
| Left IN2 | L298N IN2 | 27 | 13 |
| Left ENA | L298N ENA | 18 | 12 |
| Right IN3 | L298N IN3 | 22 | 15 |
| Right IN4 | L298N IN4 | 23 | 16 |
| Right ENB | L298N ENB | 13 | 33 |
| TRIG | HC-SR04 TRIG | 24 | 18 |
| ECHO | Divider midpoint | 25 | 22 |

ECHO in that table is the GPIO side of the divider, not the sensor pin itself.

```
Pi header                         L298N
physical 11  GPIO17  ----------- IN1     (left, with OUT1 and OUT2)
physical 13  GPIO27  ----------- IN2
physical 12  GPIO18  ----------- ENA     jumper removed
physical 15  GPIO22  ----------- IN3     (right, with OUT3 and OUT4)
physical 16  GPIO23  ----------- IN4
physical 33  GPIO13  ----------- ENB     jumper removed
physical 14  GND     ----------- spare breakout − ---- motor adapter negative / L298N GND

HC-SR04
VCC  ---------------------------- physical pin 2 (5 V)
GND  ---------------------------- physical pin 6 (GND)
TRIG ---------------------------- physical pin 18 (GPIO 24)

ECHO --[ 1 kΩ ]--+-------------- physical pin 22 (GPIO 25)
                 |
               [ 1 kΩ ]
                 |
                GND
```

The two 1 kΩ resistors divide a 5 V ECHO pulse to about **2.5 V** at GPIO25. Join the lower resistor and sensor ground to physical pin 6.

For the tested N20 harnesses (Robu SKU 476675), channel A uses red → OUT1 and white → OUT2. Channel B uses red → OUT3 and white → OUT4. Insulate each unused encoder wire separately: black (encoder supply), blue (encoder ground), yellow and green (signals). Software calls A left and B right. Confirm wheel direction with the wheels lifted after mounting.

Leave at least 70 mm of slack on wires that cross from the dome to the base. The dome twists to come off, and a short wire will pull a connector out.

### Motor power

The bench build uses a **SEM S530P2N1, 5 V DC, 3 A, centre-positive** barrel adapter. The Pi has its own USB-C supply. Share the ground, keeping the two positive supplies separate.

1. With motor power unplugged and all three jumper caps off, connect one breakout **+** pin to L298N VM (labelled `+12V`). Connect a second **+** pin to L298N logic `+5V`. Both receive **5 V**. A higher-voltage adapter on this hookup would also put that voltage on the logic supply.
2. Connect a breakout **−** pin to L298N GND. Connect a spare **−** pin to Pi physical **14** for the shared motor-control ground. Sensor VCC and ground remain on Pi physical **2** and **6**.
3. Use the OFF check below before applying motor power. Recheck after a reboot or another program has used the pins. Disconnect the motor adapter if a motor stalls or a control process becomes unresponsive.

This setup moved the unloaded motors in brief pulses. Battery power, sustained running and torque under chassis load still need validation.

### Camera cable

The Camera Module 3 has a 15-pin connector. The Pi 5 camera ports are 22-pin. Use the Pi 5 camera cable (22-pin on the Pi, 15-pin on the camera). A display cable looks similar and is not the same wiring.

Power off. Either `CAM/DISP0` or `CAM/DISP1` works. Lift the latch, push the cable in straight with the metal contacts facing away from the latch, and close the latch. Same idea on the camera end: contacts toward the contacts in the socket.

```sh
rpicam-hello --list-cameras
```

You want an `imx708` entry. Quit `rpicam-hello` before `scripts/capture.py`, or the camera is busy.

If the list is empty, add a line under `[all]` in `/boot/firmware/config.txt`, then reboot:

```
dtoverlay=imx708
```

If the camera is on `CAM/DISP0` (the port nearer the Ethernet jack) and it is still missing, use `dtoverlay=imx708,cam0` instead. Do not enable the legacy camera stack. Camera Module 3 needs libcamera.

## Bring-up

Do these in order. Driving is last, after each piece has worked on its own.

1. `python3 scripts/check_env.py`
2. `rpicam-hello --list-cameras`
3. Optional still, after that preview has quit:

```sh
python3 scripts/capture.py photo.jpg
```

   On a desktop session, `rpicam-hello -t 3000` shows a 3 second preview first.

4. Aim the sensor squarely at a flat target. Measure from its two round faces. Start from a writable directory so `lgpio` can create its notification FIFO even when the checkout is read-only:

```sh
software_dir=$(pwd -P)  # run from software/
bench_dir=$(mktemp -d)
(cd "$bench_dir" && env -u ROVER_MOCK GPIOZERO_PIN_FACTORY=lgpio python3 "$software_dir/scripts/check_distance.py")
```

   On the recorded bench, 30 readings at 16.51 cm were 16.7–16.8 cm and 30 at 31.75 cm were 31.5–32.8 cm. Removing the target produced 30 missing echoes. A missing return locks forward in the drive stack.

5. For the verified Pi 5 wiring, stop any drive process, unplug the motor adapter and keep the shafts clear or wheels lifted. In the same shell as step 4, run the OFF check:

```sh
(cd "$bench_dir" && python3 "$software_dir/scripts/motor_bench_pulse.py")
```

   With no arguments the helper sets all six motor outputs LOW and verifies them. After the OFF check passes and the operator is ready to watch an unloaded motor, apply motor power. Add `--motor A` or `--motor B` to the same command to pulse the selected channel once for 250 ms. `--motor both` pulses both once. Each explicit motor option starts immediately. Verify movement and the six LOW readings after each invocation. The helper uses real `lgpio` on gpiochip0 (`pinctrl-rp1`) and the OS `pinctrl` utility. **It does not support `ROVER_MOCK`.**

   The separate `python3 scripts/motor_test.py` runs a longer forward/reverse/turn sequence for checking directions after mounting, with wheels raised. Before reversing a pair of motor leads, disconnect motor power.

6. Drive from the terminal:

```sh
./scripts/run.sh
```

   That is an interactive prompt (`python3 scripts/drive.py`). Type `forward`, `back`, `left`, `right`, or `stop`. `quit` or Ctrl+C stops the motors and exits.

One shot, until Ctrl+C:

```sh
python3 scripts/drive.py forward
python3 scripts/drive.py back
python3 scripts/drive.py left
python3 scripts/drive.py right
python3 scripts/drive.py stop
```

Hold a command for one second, then stop:

```sh
python3 scripts/drive.py forward --seconds 1
```

`back` is also accepted as `backward` or `reverse`.

## Stop before a hit

A background loop reads the HC-SR04 about ten times a second.

- A reading **below 20 cm** pauses a forward command and stops the motors. Back, Left, and Right still run, so you can leave the obstacle. Left and Right turn in place.
- No echo (sensor unplugged, or the echo never falls) pauses forward the same way. A dead sensor must not look like an empty room.
- Readings under 2 cm are the sensor's blind zone. Those pause forward too.
- Forward stays paused until three clear readings in a row. If the command is still `forward`, the rover then continues. It does not start forward on its own if the last command was stop, back, or a turn.
- Ctrl+C, `stop`, or `quit` always stops the motors.

`STOP_DISTANCE_M`, `CRUISE_SPEED`, and `TURN_SPEED` are in `pins.py`. The drive stack's default cruise setting is 60% duty. If a wheel stalls, stop and check motor mounting, clearance and power connections before further driving.

The terminal prints a line about twice a second while a timed or one-shot command is running: distance, whether forward is blocked, and the safety message.

## Files

```
software/
├── README.md                 this guide
├── pins.py                   GPIO numbers, stop distance, speeds
├── requirements.txt          laptop mock-mode install (gpiozero)
├── rover/
│   ├── motors.py             L298N via gpiozero
│   ├── ultrasonic.py         HC-SR04, timeout means "no echo"
│   ├── safety.py             stop-before-hit rules
│   ├── camera.py             one Camera Module 3 JPEG
│   └── controller.py         latched command plus the distance gate
└── scripts/
    ├── run.sh                interactive prompt
    ├── drive.py              forward / back / left / right / stop
    ├── check_env.py          versions and the pin table
    ├── check_distance.py     print centimetres
    ├── motor_bench_pulse.py  verified Pi 5 OFF check and finite unloaded pulse
    ├── motor_test.py         forward, reverse and turns with wheels lifted
    └── capture.py            save photo.jpg
```

## Tests without a rover

```sh
cd software
python3 -m unittest discover -s tests -v
```

The suite uses `gpiozero` mock pins. For laptop use, `ROVER_MOCK=1` enables mock mode in `drive.py`, `motor_test.py`, `check_distance.py` and `capture.py`. Run the standalone `motor_bench_pulse.py` only on its matching hardware.

## When something does not work

| What you see | What to check |
| --- | --- |
| `gpiozero` missing, or a message about RPi.GPIO | `sudo apt install python3-gpiozero python3-lgpio`. You need version 2.0 or newer. |
| Permission denied on `/dev/gpiochip` | User is in the `gpio` group. Log out and back in. |
| `picamera2` import error | Apt package, not pip. Driving does not need the camera. |
| Camera list is empty | Cable contacts face away from the latch. Pi 5 needs the 22-to-15 camera cable. Try the `imx708` overlay above. |
| Camera in use | Quit `rpicam-hello` before `scripts/capture.py`. |
| Distance never changes | TRIG and ECHO swapped, or ECHO skipped the divider. `check_distance.py` should move when your hand does. |
| Forward always pauses | The sensor is inside 20 cm of the bench, or there is no echo. The status line says which. `back` still works. |
| Forward never pauses | `check_distance.py` while you cover the sensor. If the number stays large, the echo is not reaching GPIO 25. |
| Wheels only twitch | Disconnect motor power. Check the free wheel/shaft clearance and both 5 V driver feeds. |
| Forward spins the rover | Check each channel's direction with the wheels lifted. Disconnect motor power before swapping a motor pair. |
| Pi reboots when the wheels start | Check the Pi's USB-C supply, separate motor adapter and shared ground. |

## License

The Python in this `software/` directory is MIT (see `LICENSE` here). The rest of the repository — STLs, CAD, renders, and the hardware docs — stays under CC BY-SA 4.0, which is the upstream PROBE LX-3 license.
