# LUMALIEN PROBE LX-3 — Assembly Manual (v2)

LUMALIEN · Sep 24, 2026

## Overview

This manual builds the LUMALIEN PROBE LX-3 from 5 printed parts plus an optional lidar adapter, in 13 steps. The robot is a Ø245 mm dome on a Ø209 mm base, driven by two rear N20 motors with a front ball caster. It carries a Raspberry Pi 5, Geekworm X1200 UPS, Adafruit 4280 motor bonnet, Arducam B0385 camera and CQRobot VL53L1X distance sensor.

The dome twist-locks onto the base, so the electronics stay reachable. The drive plate accepts plain or encoder N20 motors. The dome is ready for two add-ons with no reprint: an RPLIDAR A1M8 on top, and a Waveshare WM8960 audio HAT with two speakers behind grilles in the rear.

## Printed parts

All parts are sized for a Bambu A1 (256 mm bed) with 3.0 mm walls. No part needs supports.

| Part | Size (mm) | Print orientation | Supports | Notes |
| --- | --- | --- | --- | --- |
| Dome | Ø244.8 × 120 | Rim down | None | 5.6 mm margin per side on the A1 bed. The inside of the top bridges about 45 mm; a little sag there is hidden. |
| Camera bracket | 67 × 61 × 35.6 | Flat back face down | None | Holds the camera and distance sensor. Slides into the dome's rail block, clicks in, and is screwed from below. |
| Base | Ø209.4 × 41.5 | Floor down | None | Plain shell. Walls lean 49°. |
| Electronics tray | Ø123 × 26 | Underside down | None | Carries the Pi 5 stack posts and the 4AA cradle. Reprint this, not the base, for electronics changes. |
| Drive plate | 161 × 124 × 7.5 | Top face down | None | Nut pockets face the bed, caster pad faces up. |
| Lidar adapter (optional) | 64 × 78 × 21.7 | Flat face down | None | Only needed for the lidar add-on. |

Clean every hole after printing, and push a zip tie through each speaker loop in the dome to clear it.

## Hardware and tools

The build uses 4 heat-set inserts, all in the electronics tray. Camera and sensor screws self-tap into printed pilot holes, with no inserts. Insert sizes are written thread × length × outside diameter (Dianrui kit labels).

| Joint | Fastener | Qty | Goes into | From |
| --- | --- | --- | --- | --- |
| Drive plate + base → tray | M3×4×5 heat-set insert | 4 | Ø4.2 × 5.5 mm holes, tray underside | Dianrui kit |
| Drive plate + base → tray | M3×10 button head | 4 | Through plate and base floor into the tray inserts | Fgruh M3 kit |
| Motor brackets → plate | M2 screw + M2 nut | 4 + 4 | Ø2.1 through-holes, nuts in hex pockets on plate top | Meccanixity bracket kit (or M2×8 socket pan) |
| Caster → plate | Caster's own adhesive pad | 1 | Flat Ø43.5 pad on the plate underside. Optional: 2 short self-tapping screws through the caster's holes, max 6 mm into the pad | MARRTEUM caster 4-pack |
| Camera → bracket | M2×8 socket pan | 4 | Ø1.7 × 7 mm pilot holes, self-tapping | M2×8 pack |
| Distance sensor → bracket | M2×5 button head | 2 | Ø1.7 × 5 mm pilot holes, self-tapping | uxcell M2×5 pack |
| Bracket → dome | M3×10 button head | 2 | Up through the recessed holes in the dome rim into Ø2.5 pilots in the bracket key, self-tapping | Fgruh M3 kit |
| Pi 5 + X1200 → tray posts | M2.5×20 screw | 4 | Down through the Pi 5, spacers and X1200; tips self-tap about 7 mm into the Ø2.2 post pilots | X1200 screws pack |
| 4AA pack → tray cradle | Zip tie, 4.8 mm wide, ≥250 mm long | 2 | Tunnels under the cradle pad | — |
| Motor bonnet | Optional M2.5 standoff, about 8 mm | 2 | Pi rear holes, under the bonnet | Not in current kits |

Do not use M2×8 in the distance-sensor standoffs. It would bottom out in the 5 mm pilot.

**Tools:**

- Soldering iron with a heat-set insert tip (about 220–230 °C for PLA, 240–250 °C for PETG)
- Hex keys: 2.0 mm (M3 button), plus 1.3 mm or 1.5 mm for the M2 screws (check your packs)
- Small flat screwdriver for the bonnet terminal blocks
- Tweezers or needle-nose pliers, masking tape, flush cutters

## Assembly steps

Build the drive plate first, fix it to the empty base, then load the electronics, then the dome. Directions below: **front** is the camera side, **rear** is the battery-cradle side, and left/right are as the robot sees them.

### Step 1 — Test-fit the shells

1. Check the dome's ledge, the three notches and the rail block's groove are clean and free of stringing.
2. Set the dome on the base with the camera about 30° counter-clockwise (seen from above) of the front. The notches drop over the base lugs.
3. Twist clockwise until it stops. It should turn freely through about 30° and stop hard at each end.

### Step 2 — Heat-set inserts in the electronics tray

1. Turn the tray upside down on a towel.
2. Press an M3×4×5 insert into each of the 4 holes on the underside, straight and flush.
3. Let them cool for a minute before loading them.

### Step 3 — Nuts into the drive plate

1. Lay the plate top face up (the flat face, no pad).
2. Press an M2 nut into each of the 4 hex pockets on the arms (motor brackets).
3. Tape over all 4 pockets, then flip the plate so the raised caster pad faces up.

### Step 4 — Mount the motors

The motors ship with the wheels already on, so each goes on as one unit.

1. Lay a motor on each rear arm: wheel pointing outward, solder tabs (or encoder board) toward the centre.
2. Line the gearbox front face up with the arm tip. The wheel should sit about 1 mm clear of the tip.
3. Encoder motors only: the encoder board drops into the shallow pocket beside the wire slot.
4. Set a bracket over the gearbox with its two ears over the arm's two holes.
5. Drive 2 M2 screws through each bracket into the nuts. Snug them only; overtightening crushes the gearbox.
6. Spin each wheel by hand. It must turn freely and not touch the plate.

### Step 5 — Mount the caster

1. Wipe the raised round pad clean (isopropyl alcohol if you have it).
2. Peel the caster's adhesive backing, centre the caster on the pad and press hard for 30 seconds.
3. Leave it 24 hours before driving so the adhesive reaches full strength.
4. Optional backup: drive 2 short self-tapping screws through the caster's holes into the pad, no more than 6 mm deep, or they will reach the base floor.

### Step 6 — Route the motor wires

1. Feed each motor's wires up through the 10 × 5 mm slot just inboard of that motor.
2. Remove the tape from the nut pockets.

### Step 7 — Join the drive plate, base and tray

One set of 4 screws clamps all three parts together.

1. Stand the drive plate on its wheels and caster.
2. Set the base on the plate, lining up its 4 small holes and 2 wire slots with the plate's.
3. Drop the tray into the base, posts up, with the battery cradle over the motors (rear). Feed the motor wires up through the tray's matching slots.
4. Tip the assembly onto its side.
5. Drive 4 M3×10 button screws up through the plate and base floor into the tray inserts.

### Step 8 — Pi 5 and X1200 stack

1. Fit both 18650 cells into the X1200 first. The holders face down and are unreachable once the stack is in.
2. Set the Pi 5 on the X1200 with the spacers between them, so the pogo pins meet the Pi's underside pads.
3. Stand the stack on the 4 tray posts: 40-pin header toward the rear, USB/Ethernet end toward the robot's left.
4. Drive 4 M2.5×20 screws down through the Pi 5, spacers and X1200. The tips cut their own thread into the posts; stop at snug.

### Step 9 — Motor bonnet

1. Press the motor bonnet straight down onto the Pi's 40-pin header.

### Step 10 — 4AA battery pack

1. Stand the pack on its edge on the rear cradle, between the ribs.
2. Thread 2 zip ties through the tunnels under the cradle, up both faces and over the top.
3. Put the tie heads on top of the pack, pull tight and trim.

### Step 11 — Base wiring

1. Left motor wires to bonnet terminal M1, right motor to M2. If a wheel runs backward in testing, swap that motor's two wires.
2. 4AA pack leads to the bonnet's motor power terminal, red to +. Leave the pack switched off or a cell out.

### Step 12 — Camera and distance sensor into the dome

Load the bracket on the bench first, then slide it into the dome.

1. Camera: lens facing away from the bracket, set the board on the 4 short standoffs. Drive 4 M2×8 socket pan screws through the board into the standoffs, gently. Plug the camera cable in through the window in the bracket plate.
2. Distance sensor: plug its cable in first; the connector faces down. Set the board on the 2 long standoffs, chip facing away from the bracket, and fix it with 2 M2×5 button screws.
3. Set the dome upside down on a towel. Find the rail block on the ledge below the camera opening.
4. Hold the bracket with the lens toward the opening. Drop the dovetail key into the open end of the groove and push the bracket toward the wall.
5. The latch rides up over the block and clicks into its notch as the key hits the end stop. The lens now sits in the Ø24 opening and the sensor chip faces its window.
6. On the dome's rim face, below the camera, find the two recessed holes. Drive 2 M3×10 button screws up through them into the bracket key until snug. The heads sit below the rim face, so the dome still seats on the base.
7. To remove: take out the 2 screws, push the latch arm up (toward the dome top) where it passes the end of the block, and slide the bracket back out.
8. Route both cables down toward the base with at least 70 mm of slack. They must reach the Pi with the dome unlocked.

### Step 13 — Connect and close

1. Camera USB lead into a Pi USB port.
2. Distance sensor to the Pi's I2C pins: 3.3 V, GND, SDA (GPIO2), SCL (GPIO3). Reach them through the bonnet's pass-through pads or a stacking header. The sensor (0x29) and bonnet (0x60) use different I2C addresses.
3. Tuck the cables so nothing crosses the base lugs.
4. Set the dome on 30° counter-clockwise, then twist clockwise to the stop. The camera now faces the front, over the caster.
5. To open: twist counter-clockwise to the stop and lift.

## Optional: lidar add-on (RPLIDAR A1M8)

The dome already has the lidar holes, so the upgrade needs no reprint: 3 inserts, the printed adapter and 7 screws.

| Joint | Fastener | Qty | Goes into |
| --- | --- | --- | --- |
| Adapter → dome | M3×4×5 heat-set insert | 3 | Ø4.2 × 5.5 mm holes in the dome's flat top |
| Adapter → dome | M3×6 button head | 3 | Adapter counterbores into the inserts |
| Lidar → adapter | M2.5 screw | 4 | Ø2.7 holes through the adapter posts |

1. Press 3 M3×4×5 inserts into the 3 small holes on the dome's flat top, flush.
2. Fix the lidar to the adapter posts with its motor toward the rear, using 4 M2.5 screws.
3. Feed the lidar cable through the adapter's centre hole and the dome's Ø12 centre hole.
4. Seat the adapter on the dome's flat top and fix it with 3 M3×6 button screws.
5. Plug the cable into a Pi USB port through the lidar's adapter board. Leave slack for the 30° dome twist.

The lidar adds about 170 g at the top, so keep acceleration and braking gentle in software.

## Optional: audio add-on (Waveshare WM8960 Audio HAT)

The dome already has both speaker grilles and the zip-tie loops, so the upgrade needs no reprint. The kit is the Waveshare WM8960 Audio HAT (built-in mics) with its two 8 Ω 5 W speakers (100 × 45 × 21 mm).

| Joint | Fastener | Qty | Goes into |
| --- | --- | --- | --- |
| Motor bonnet → audio HAT | M2.5 brass standoff, 11 mm | 1 per bonnet mounting hole | Between the two boards, so they can't touch |
| Speakers → dome | Zip tie, 4.8 mm wide, ≥150 mm long | 4 | Through the loops above and below each speaker end |

1. Lift the motor bonnet off the Pi.
2. Press the audio HAT onto the Pi's 40-pin header.
3. Fit the 11 mm standoffs on the HAT, then press the motor bonnet onto the pins that come up through the HAT and fix it to the standoffs. The pins must reach at least 7.5 mm above the HAT board; if they don't, add a 2×20 stacking header.
4. With the dome upside down, set each speaker face-down over its grille (the two hole fields on the rear half of the dome), long side horizontal.
5. At each end of a speaker, thread a zip tie through the lower loop, up between the speaker end and the wall, through the upper loop, then around the back of the speaker's stepped end. Pull snug and trim.
6. Route the speaker lead to the HAT's speaker connector with enough slack for the 30° dome twist.

## Checks before first power-on

Run these with the robot on the bench before the first drive.

- [ ] Both wheels and the caster touch the table and the robot sits level.
- [ ] Wheels spin freely by hand, with about 1 mm clear of the plate arms.
- [ ] The robot does not tip backward when rocked; the caster stays loaded.
- [ ] The dome twists through its full 30° both ways with all cables connected and no pull on the plugs.
- [ ] 4AA leads are on the bonnet's motor power terminal with correct polarity before inserting the last cell.
- [ ] 18650 cells are charged and the Pi boots from the X1200 alone.
- [ ] `lsusb` shows the camera, and `i2cdetect -y 1` shows 0x29 (distance sensor) and 0x60 (bonnet).
- [ ] Each wheel turns forward on a forward command. If not, swap that motor's two wires at the bonnet.
- [ ] Audio add-on only: `i2cdetect -y 1` also shows 0x1a (WM8960), and both speakers play.

## Upgrade paths

**Raspberry Pi AI HAT+ 2 (Hailo-10H, 8 GB) — fits, no reprint.** It runs small language models (1–1.5B: Qwen2/2.5 1.5B, Llama 3.2 1B, DeepSeek-R1-Distill 1.5B) through an Ollama-compatible server, in its own 8 GB of RAM, so it suits the 2 GB Pi 5. Expect about the same speed as running the model on the Pi's CPU; the gain is freed Pi memory and running vision plus a language model together. It draws up to 3 W, which shortens battery time.

Stack, bottom to top: X1200 → Pi 5 with active cooler → AI HAT+ 2 (PCIe ribbon, on its standoffs) → audio HAT (optional) → motor bonnet. The Hailo uses PCIe, not GPIO, so nothing clashes; I2C addresses stay unique (bonnet 0x60/0x70, audio 0x1a, distance sensor 0x29). The dome has plenty of height for the extra layer. Check that the 40-pin header passes up through the AI HAT (add a 2×20 stacking header if not), and watch temperatures with the full stack inside the closed dome.

The original AI HAT+ (Hailo-8 / 8L) is for vision only and cannot run language models.

**NVIDIA Jetson Orin Nano — not a drop-in swap.** The dev kit (about 103 × 90.5 mm) is larger than the Pi 5 and won't fit the tray's post pattern or diameter. The X1200 is Pi 5-only (5 V through pogo pins), while the Orin Nano needs about 9–20 V at up to 25 W. The motor bonnet should work over the Orin's I2C header pins, but may not stack past its heatsink; the WM8960 audio HAT needs a driver and device-tree work on JetPack. The dome, base, drive plate, camera bracket and speakers carry over; the tray and power system would need a redesign.

