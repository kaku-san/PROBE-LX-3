# Bill of Materials

[← Back to README](../README.md) · Next: [Printing →](PRINTING.md)

This is everything you need to build a PROBE LX-3 from scratch. Brand names are the exact parts the design was modelled and fit-checked around. Swap in equivalents at your own risk, and check dimensions before you print.

> **Tip:** Copy this file into a GitHub issue or your notes app to tick parts off as they arrive.

---

## 1. Electronics

| ✓ | Qty | Part | Notes |
| :-: | :-: | --- | --- |
| ☐ | 1 | **Raspberry Pi 5** (2 GB or larger) | 2 GB is enough. Larger boards fit the same way. |
| ☐ | 1 | **Geekworm X1200** 2-cell 18650 UPS HAT for Pi 5 | Powers the Pi through pogo pins. Includes spacers and M2.5×20 screws, which the build uses. |
| ☐ | 2 | **18650 Li-ion cells** | For the X1200. Check Geekworm's X1200 docs for the cell types it supports. |
| ☐ | 1 | **Adafruit 4280** DC + Stepper Motor Bonnet for Raspberry Pi | Drives both N20s over I²C (address 0x60). |
| ☐ | 1 | **Arducam B0385** USB camera module (38 × 38 mm board) | Mounts in the dome's camera bracket and connects over USB. |
| ☐ | 1 | **CQRobot VL53L1X** time-of-flight distance sensor (28.5 × 23 mm board) | I²C 0x29. Includes a PH2.0 cable. |
| ☐ | 1 | **microSD card** (32 GB+) | For the Pi's OS. |
| ☐ | 1 | **USB-C charger** | To charge the X1200. Use the supply Geekworm recommends. |
| ☐ | — | **Jumper wires** (female, 4 × for the VL53L1X to Pi I²C) | Or a 2×20 stacking header. See [Wiring](WIRING.md). |

## 2. Drive and motion

| ✓ | Qty | Part | Notes |
| :-: | :-: | --- | --- |
| ☐ | 2 | **N20 micro gear motor with wheel** (~43 mm tyre) | Plain or encoder versions both fit, and the plate has an encoder-board pocket. Modelled on the **12SG-N20VA-100-EN**. Choose a voltage that suits a 4 × AA (~6 V) supply. |
| ☐ | 2 | **Meccanixity N20 motor bracket** (with M2 screws and nuts) | One per motor. |
| ☐ | 1 | **MARRTEUM ball caster** (20 mm ball, adhesive pad) | Sold as a 4-pack. You need 1. |
| ☐ | 1 | **4 × AA battery holder**, with a switch and leads | Motor power. Held on the tray cradle with zip ties. |
| ☐ | 4 | **AA cells** | NiMH rechargeables recommended. |

## 3. Fasteners and consumables

All counts are for the **core build**. The totals already include the counts from the table below it.

| ✓ | Qty | Fastener | Used for |
| :-: | :-: | --- | --- |
| ☐ | 4 | **M3 × 4 × 5 heat-set insert** (thread × length × OD) | Electronics tray underside |
| ☐ | 6 | **M3 × 10 button head** | 4 × plate + base → tray · 2 × camera bracket → dome |
| ☐ | 4 + 4 | **M2 screw + M2 nut** | Motor brackets → drive plate. Use the bracket-kit screws or M2 × 8 socket pan heads. |
| ☐ | 4 | **M2 × 8 socket pan head** | Camera → bracket (self-tapping into printed pilots) |
| ☐ | 2 | **M2 × 5 button head** | Distance sensor → bracket (self-tapping). **Don't use M2 × 8 here.** It bottoms out. |
| ☐ | 4 | **M2.5 × 20 screw** | Pi 5 + X1200 → tray posts. Included with the X1200. |
| ☐ | 2 | **Zip tie, 4.8 mm wide, ≥ 250 mm long** | 4 × AA pack → tray cradle |
| ☐ | 2 | *(optional)* **Short self-tapping screws** | Backup for the caster pad. Max 6 mm into the pad. |
| ☐ | 2 | *(optional)* **M2.5 standoff, ~8 mm** | Supports the rear edge of the motor bonnet |

### Where the fasteners go

| Joint | Fastener | Qty | Goes into |
| --- | --- | :-: | --- |
| Drive plate + base → tray | M3×4×5 heat-set insert | 4 | Ø4.2 × 5.5 mm holes, tray underside |
| Drive plate + base → tray | M3×10 button head | 4 | Through plate and base floor into the tray inserts |
| Motor brackets → plate | M2 screw + M2 nut | 4 + 4 | Ø2.1 through-holes, nuts in hex pockets on the plate top |
| Caster → plate | Caster's adhesive pad | 1 | Flat Ø43.5 pad on the plate underside |
| Camera → bracket | M2×8 socket pan | 4 | Ø1.7 × 7 mm pilot holes, self-tapping |
| Distance sensor → bracket | M2×5 button head | 2 | Ø1.7 × 5 mm pilot holes, self-tapping |
| Bracket → dome | M3×10 button head | 2 | Up through the recessed holes in the dome rim into Ø2.5 pilots in the bracket key |
| Pi 5 + X1200 → tray posts | M2.5×20 | 4 | Down through the Pi, spacers and X1200. Tips self-tap about 7 mm into Ø2.2 post pilots. |
| 4AA pack → tray cradle | Zip tie ≥ 250 mm | 2 | Tunnels under the cradle pad |

## 4. Filament

| ✓ | Qty | Material | Notes |
| :-: | :-: | --- | --- |
| ☐ | ~1 kg | **PLA or PETG** | One spool covers every part. The renders use white (dome), black (base), grey (drive plate) and purple (tray, bracket, lidar adapter). |

See [PRINTING.md](PRINTING.md) for per-part settings.

## 5. Tools

- [ ] 3D printer with a **256 × 256 mm bed or larger** (designed on a Bambu Lab A1)
- [ ] Soldering iron with a **heat-set insert tip** (220–230 °C for PLA, 240–250 °C for PETG)
- [ ] Hex keys: **2.0 mm** (M3 button heads), plus **1.3 mm or 1.5 mm** for M2 (check your screw packs)
- [ ] Small flat screwdriver for the bonnet terminal blocks
- [ ] Tweezers or needle-nose pliers
- [ ] Masking tape
- [ ] Flush cutters
- [ ] Isopropyl alcohol (for the caster pad)
- [ ] Soldering gear, if your N20s come without leads

---

## Optional add-ons

These fit the stock dome with **no reprint**. Details are in [UPGRADES.md](UPGRADES.md).

### Lidar: SLAMTEC RPLIDAR A1M8

| ✓ | Qty | Part |
| :-: | :-: | --- |
| ☐ | 1 | SLAMTEC **RPLIDAR A1M8** (with its USB adapter board) |
| ☐ | 1 | Printed **lidar adapter** (`stl/PROBE-LX3_lidar-adapter_optional.stl`) |
| ☐ | 3 | M3 × 4 × 5 heat-set insert |
| ☐ | 3 | M3 × 6 button head |
| ☐ | 4 | M2.5 screw, length to suit the A1M8 mounting holes (they pass through Ø2.7 holes in the adapter posts) |

### Audio: Waveshare WM8960 Audio HAT

| ✓ | Qty | Part |
| :-: | :-: | --- |
| ☐ | 1 | **Waveshare WM8960 Audio HAT** (built-in mics) |
| ☐ | 2 | **Waveshare 8 Ω 5 W speaker** (100 × 45 × 21 mm) |
| ☐ | 1 per bonnet hole | M2.5 brass standoff, 11 mm |
| ☐ | 4 | Zip tie, 4.8 mm wide, ≥ 150 mm long |
| ☐ | (maybe) 1 | 2×20 stacking header, if the HAT's pass-through pins stand less than 7.5 mm above its board |

### Compute: Raspberry Pi AI HAT+ 2

| ✓ | Qty | Part |
| :-: | :-: | --- |
| ☐ | 1 | Raspberry Pi **AI HAT+ 2** (Hailo-10H, 8 GB) |
| ☐ | 1 | Raspberry Pi 5 **Active Cooler** |
| ☐ | (maybe) 1 | 2×20 stacking header |

---

[← Back to README](../README.md) · Next: [Printing →](PRINTING.md)
