# Visual guide for the Pi 5 and L298N build

Use the assembly cards in order. Disconnect power for assembly and follow the power sequence on the first-drive card. The English walkthrough takes about two and a half minutes. [Listen to the walkthrough](rover-assembly-walkthrough.mp3) · [Read the transcript](rover-assembly-walkthrough.txt)

| Card | What to check |
| --- | --- |
| [1. Mount the motors](assembly-01-motors.png) | Seat each gearbox under a printed cap. Check the space beside both wheels and the contact between the wheels, skid and floor. |
| [2. Assemble the chassis](assembly-02-chassis.png) | Stack the plate, bowl and tray. Align the wire slots and fasten the stack from below when the tray inserts are installed. |
| [3. Fit the camera and plan the sensor mount](assembly-03-camera-sensor.png) | Check the carrier and keeper with the camera ribbon disconnected. Measure the HC-SR04 for its separate mount. |
| [4. Seat the boards and route the wires](assembly-04-electronics.png) | Trial-fit the Pi 5, cooler, driver and mini breadboard. Keep leads clear of the fan, wheels and dome. |
| [5. Test the assembled rover](assembly-05-first-drive.png) | Test motor direction with the wheels raised. Check the camera and sensor while stationary, then verify onboard power before the first floor run. |

The wiring maps use **physical Raspberry Pi header pin numbers**. Orient the Pi with its USB sockets at the top and its GPIO header on the left.

- [Motor control wires and common ground](motor-seven-control-wires.svg) shows the six L298N control connections and the common ground on physical pin 14.
- [First HC-SR04 sensor](sensor-full-pin-map.svg) shows the six connections and the two 1 kΩ resistors. The junction between the resistors goes to physical pin 22 (GPIO25).

The mechanical illustrations adapt [LUMALIEN’s PROBE LX-3 hardware design](https://github.com/kaku-san/PROBE-LX-3/tree/72a04b4ab8d25bf7737404c3294ec3d89b962e48) with new motor saddles, clamp caps, a front skid and a camera carrier and keeper. The adapted illustrations are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
