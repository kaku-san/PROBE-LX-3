# Kakuji drive software

This is Kakuji's L298N + HC-SR04 + Camera Module 3 adaptation, not stock PROBE wiring.

It is a small Python program for a Raspberry Pi 5. You drive two N20 gear motors through an L298N from the terminal. An HC-SR04 pauses forward motion when something is too close. A separate command saves one JPEG from the Camera Module 3.

The STLs, CAD, and the files in `docs/` and `manual/` are the original PROBE LX-3 hardware release. They were not changed. `docs/WIRING.md` and `docs/BOM.md` still describe an Adafruit motor bonnet, a VL53L1X, and a USB Arducam. Use this page for the electronics below. The stock distance-sensor holes and camera bracket were drawn around those other boards, so an HC-SR04 and a Camera Module 3 may not bolt on. Tape or a zip tie is enough to point the sensor forward and to hold the camera. This folder does not add new printed parts.

## Parts this program expects

| Part | How the software talks to it |
| --- | --- |
| Raspberry Pi 5 (8 GB is fine; any Pi 5 works) | Raspberry Pi OS Bookworm, 64-bit |
| Camera Module 3 on the CSI port | `picamera2` for one JPEG. Preview with `rpicam-hello`. |
| 2× N20 gear motors | The two outputs of the L298N |
| L298N motor driver | Six GPIO pins via `gpiozero` |
| HC-SR04 ultrasonic sensor | Trigger and echo GPIO pins |
| A 5 V supply for the Pi, and a motor supply | 18650 pack and/or a 5 V brick, wired as in the power section |

`RPi.GPIO` does not work on a Pi 5. This project uses `gpiozero` (2.0 or newer) on purpose.

You do not need a Jetson, an Adafruit motor bonnet, a VL53L1X, a USB camera, a lidar, or an audio HAT for this program.

## Install on the Pi

Flash **Raspberry Pi OS Bookworm (64-bit)**. Desktop or Lite both work. Connect Wi-Fi or a keyboard, then:

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

`requirements.txt` is for a laptop, where `ROVER_MOCK=1` runs the same commands with fake pins. On the Pi, the apt line above is the install. Do not pip-install `picamera2`; the apt package is the one that matches the camera stack.

### Try the commands on a laptop

```sh
cd software
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
ROVER_MOCK=1 .venv/bin/python scripts/drive.py stop
```

## Wire it

Power is unplugged while you wire. Two things will put 5 V onto a Pi pin if you skip them. Pi GPIO is not 5 V tolerant.

> Pull the **ENA** and **ENB** jumpers off the L298N **before** those pins are wired to the Pi. With the jumper on, the pin is tied to 5 V.

> Do not connect the HC-SR04 **ECHO** pin straight to the Pi. ECHO is a 5 V output. Put the divider on it first.

### Pin table

BCM numbers are what `gpiozero` uses. Physical pin 1 is the 3.3 V pin with the square pad, on the outer corner of the header. All of these numbers live in `pins.py`. Change them there if you move a wire, then restart.

| Signal | Connects to | BCM | Physical pin |
| --- | --- | --- | --- |
| Left IN1 | L298N IN1 | 17 | 11 |
| Left IN2 | L298N IN2 | 27 | 13 |
| Left ENA | L298N ENA | 18 | 12 |
| Right IN3 | L298N IN3 | 22 | 15 |
| Right IN4 | L298N IN4 | 23 | 16 |
| Right ENB | L298N ENB | 13 | 33 |
| TRIG | HC-SR04 TRIG | 24 | 18 |
| ECHO | HC-SR04 ECHO | 25 | 22 |

ECHO in that table is the GPIO side of the divider, not the sensor pin itself.

```
Pi header                         L298N
physical 11  GPIO17  ----------- IN1     (left, with OUT1 and OUT2)
physical 13  GPIO27  ----------- IN2
physical 12  GPIO18  ----------- ENA     jumper removed
physical 15  GPIO22  ----------- IN3     (right, with OUT3 and OUT4)
physical 16  GPIO23  ----------- IN4
physical 33  GPIO13  ----------- ENB     jumper removed
physical  6  GND     ----------- GND ---- motor-supply negative

HC-SR04
VCC  ---------------------------- physical pin 2 (5 V)
GND  ---------------------------- physical pin 6 (GND)
TRIG ---------------------------- physical pin 18 (GPIO 24)

ECHO --[ 1 kΩ ]--+-------------- physical pin 22 (GPIO 25)
                 |
               [ 2 kΩ ]
                 |
                GND
```

10 kΩ and 20 kΩ are fine too: same 1:2 ratio. The GPIO must see about 3.3 V when ECHO is high, which is what 1 kΩ / 2 kΩ does (`5 V × 2/3`).

Left and right are the rover's left and right while it drives toward the camera. On the PROBE body the camera is the front and the motors are at the rear. OUT1/OUT2 are the left N20. OUT3/OUT4 are the right N20. Motor wire colour does not matter yet; the motor test tells you if a pair is swapped.

Leave at least 70 mm of slack on wires that cross from the dome to the base. The dome twists to come off, and a short wire will pull a connector out.

`LEFT_EN` (GPIO 18) and `RIGHT_EN` (GPIO 13) are on two different PWM channels. `gpiozero` on a Pi 5 is software PWM, so any free GPIO works if you edit `pins.py`. GPIO 12 shares a hardware PWM channel with GPIO 18, so leave GPIO 12 alone if you later switch to hardware PWM.

### Motor power

The Pi and the motors can share a ground. They should not share a power wire. Motor current through a Pi pin will reset or damage the Pi.

The L298N drops roughly 1.5–2 V inside the chip. Many N20 gearmotors are happy around 6 V at the motor terminals, so the pack feeding the L298N motor terminal wants to be a bit higher than that. A single bare 18650 (about 3.7 V) is a poor motor supply on this driver, and it must not be plugged into the Pi's USB-C port. Use a holder or pack that already has its own protection and leads.

**2S 18650 pack (about 7.4 V) for the motors, separate 5 V brick for the Pi.** This is the better of the two supplies you may have.

1. Pi USB-C comes from the 5 V brick only.
2. Pack positive goes to the L298N motor terminal (often marked `+12V` or `VMS`). Pack negative goes to L298N GND.
3. Leave the L298N 5 V jumper **installed**, so the board makes its own logic 5 V from the motor pack.
4. Do **not** connect the L298N 5 V pin to the Pi's 5 V pin.
5. Do connect L298N GND to Pi GND (physical pin 6). The sensor ground uses that same node.

**Only a 5 V brick.** It can feed the Pi and the motor terminal. The motors will run slowly, because they only see about 3–3.5 V after the L298N drop. Raise `CRUISE_SPEED` in `pins.py` if they only twitch.

1. Pi USB-C from the brick.
2. Brick 5 V also to the L298N motor terminal. Brick negative to L298N GND and to Pi GND.
3. **Remove** the L298N 5 V jumper. The onboard regulator cannot make 5 V from a 5 V input.
4. Connect the brick's 5 V (or Pi physical pin 2) to the L298N logic `+5V` pin, so the inputs have a supply. Do not also tie that pin back to a second 5 V source.
5. Do not power the Pi from the L298N 5 V pin. That regulator cannot run a Pi 5.

If the wheels are stalled against a wall or a table, pick the rover up. A stalled N20 gets hot, and a weak shared brick will reboot the Pi. If the program ever locks up, disconnect the motor pack. That stops the motors even if the Pi does not.

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

4. Distance, with nothing touching the sensor, then with your hand about 10 cm in front:

```sh
python3 scripts/check_distance.py
```

   A clear space prints tens of centimetres. Your hand should drop the number. `no echo — forward would be locked` means a forward command will pause. Ctrl+C ends the script. It does not run the motors.

5. Sit the rover on a box so the wheels are in the air. Then:

```sh
python3 scripts/motor_test.py
```

   It asks you to press Enter. Forward should turn both wheels so the rover would roll toward the camera. If it would spin in a circle, swap the two screws of the wheel that went the wrong way. If both wheels are backwards, swap both pairs. You can also swap that channel's two `IN` numbers in `pins.py` instead of the screws.

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

`STOP_DISTANCE_M`, `CRUISE_SPEED`, and `TURN_SPEED` are in `pins.py`. `CRUISE_SPEED = 0.60` is 60% of full duty, so a stall is gentler than 100%. On a 5 V brick you may need to raise it before the N20s actually turn.

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
    ├── motor_test.py         short wheel pulse, rover lifted
    └── capture.py            save photo.jpg
```

## Tests without a rover

```sh
cd software
python3 -m unittest discover -s tests -v
```

The tests use `gpiozero`'s mock pins. They do not need a Pi, a camera, or a motor. `ROVER_MOCK=1` does the same thing for the scripts.

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
| Wheels only twitch | Raise `CRUISE_SPEED`. On 5 V into an L298N this is common. |
| Forward spins the rover | One motor pair is reversed. Swap that pair's two screws. |
| Pi reboots when the wheels start | Motor current is going through the Pi's supply. Use the separate motor pack, and keep the grounds tied. |

## License

The Python in this `software/` directory is MIT (see `LICENSE` here). The rest of the repository — STLs, CAD, renders, and the hardware docs — stays under CC BY-SA 4.0, which is the upstream PROBE LX-3 license.
