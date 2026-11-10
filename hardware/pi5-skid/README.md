# Pi 5 rover drive plate and camera mount

Print this set to fit two N20 encoder motors, 34 mm rubber wheels and a standard Camera Module 3 to the PROBE LX-3 shell. The adapted drive plate has two motor saddles and a rounded front skid. The camera carrier uses the dome's original slide and latch. Use the stock [base, dome and electronics tray](../../stl/) with these parts.

## Print five pieces

Open the [editable five-part plate in Bambu Studio](ROVER_REMAINING_5_PARTS_CHECKED.3mf) to keep the checked placement, orientation and 100% scale. For a different layout or printer, import the individual meshes in millimetres and slice for your machine.

| Part | Quantity | Purpose |
| --- | ---: | --- |
| [Adapted drive plate](stl/PROBE-LX3_drive-plate_N20_SKID_CANDIDATE.stl) | 1 | Carries both motors and supports the front of the rover on its skid. |
| [Motor clamp cap](stl/N20_CAP_print_two.stl) | 2 | One cap holds each brass gearbox in its saddle. |
| [Camera carrier](stl/CAMERA_CARRIER_CANDIDATE.stl) | 1 | Holds the side edges of the standard Camera Module 3 board. |
| [Camera keeper](stl/CAMERA_KEEPER_CANDIDATE.stl) | 1 | Clips over the carrier to retain the board. |

The saved slice used a Bambu Lab P2S, a 0.4 mm nozzle, generic PLA and a textured PEI plate. Settings were 0.16 mm layers with a 0.20 mm first layer, four walls, 20% infill, a 3 mm outer brim, no supports, 220 °C nozzle and 55 °C bed. Studio estimated **2 h 38 min and 69.11 g** for all five parts. Select the actual printer and filament before slicing.

## Hardware and first fit

- **Motors.** Plan for **four M3 × 8 mm machine screws and four M3 hex nuts** total. Slide two nuts into each arm's side slots, set the brass gearbox in its saddle with the wheel outward and encoder inward, then place a cap over the gearbox. The two screw holes in each cap are 22 mm apart. Check for a small gap under the cap ears as the gearbox grips, about 1 mm wheel-to-arm clearance, and clearance for the encoder and its wires. Check both wheels and the skid meet a level surface before powered driving. The skid height assumes a 34 mm wheel and an axle centre 5 mm above the gearbox seat.
- **Camera.** No screws are needed for the carrier or keeper. Remove brim and try the keeper on the empty frame first. With power off and the ribbon disconnected, slide the PCB into the side channels, lens forward and ribbon connector toward the lower opening. Seat the keeper on the frame so the PCB stays flat. Check the ribbon path, dome fit and camera image before driving. Geometry uses the [standard Camera Module 3 drawing](https://datasheets.raspberrypi.com/camera/camera-module-3-standard-mechanical-drawing.pdf).
- **Other mounts.** The four chassis fasteners through the plate and base into the electronics tray are a separate set. The stock joint takes four M3 × 10 mm screws and four M3 × 4 × 5 mm heat-set inserts. See [stock chassis assembly](../../docs/ASSEMBLY.md#step-7--join-the-drive-plate-base-and-tray). A dedicated HC-SR04 mount and an L298N mounting position still need to be fitted to the actual rover.

## Verification and limits

The [7 November 2026 offline slice report](print-report.json) showed extrusion on all 222 layers and kept all 12 screw bores open across 476 bore/layer checks. The smallest calculated opening was about 3.34 mm. Both motor channels, the camera rails and the keeper recesses were open in the sliced paths. Remove brim between the clamp feet and inspect the underside of each cap's approximately 12.4 mm bridge for sag.

A wheel fitted the motor shaft and the motors ran on the bench. A small trial arm was used to check placement. The slice report does not establish final clamp grip, skid height under load, camera retention or clearances in a closed moving rover. The exported camera-carrier mesh has one collinear triangle at a rail face. Its volume is unaffected and the audited slicer accepted it.

The four STL files are the exact audited mesh exports. The editable 3MF contains all five pieces as a combined mesh and includes its printer profile and placement. Use the individual STLs for part-level edits. The shared project removes an account identifier and records attribution in the 3MF document metadata. Mesh, build transforms and slicer settings match the audited project. Check the packaged files against [SHA256SUMS](SHA256SUMS) with `shasum -a 256 -c SHA256SUMS` from this directory.

## Credits and source

Original PROBE LX-3 hardware © [LUMALIEN](https://lumalien.com). The remix preserves the shell interfaces from the [stock drive plate](../../stl/PROBE-LX3_drive-plate.stl) and the dome rail/latch from the [original Blender assembly](../../cad/PROBE-LX-3.blend). It replaces the motor retention and caster with printed saddles, caps and a skid, and replaces the upper camera/ToF support with two edge rails and a keeper. The original configuration includes a separate [stock camera bracket](../../stl/PROBE-LX3_camera-bracket.stl). [Source revision 72a04b4](https://github.com/kaku-san/PROBE-LX-3/tree/72a04b4ab8d25bf7737404c3294ec3d89b962e48).

The adapted hardware, meshes and documentation are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](../../LICENSE).
