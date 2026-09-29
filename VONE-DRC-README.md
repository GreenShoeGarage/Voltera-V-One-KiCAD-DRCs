# Voltera V-One: KiCad DRC profiles

Version 1.0.1 | 2026-09-28 | GNU GPL v3

These independently prepared rules target conductive-ink printing with riveted vias. They are not an official Voltera release or a printer certification. Intended syntax: KiCad 9 and 10, custom-rule language version 1.

## Choose one

| File | Trace and different-net spacing | Small-rivet via pad |
|---|---:|---:|
| `VONE-10mil-recommended.kicad_dru` | 10 mil / 0.254 mm | 1.30 mm, our conservative choice |
| `VONE-8mil-minimum.kicad_dru` | 8 mil / 0.2032 mm | 0.90 mm, published head-coverage minimum |

Start with the 10 mil file. Voltera describes its minimum as 8 mil (approximately 0.2 mm) and recommends 10 mil for beginners. We use the exact mil conversions. The 8 mil file reduces margin; it is not a promise of successful printing. [1]

## Install

1. Back up your project and any existing custom rules.
2. Open the chosen `.kicad_dru` in a text editor and copy its complete contents.
3. In PCB Editor, open **File > Board Setup > Design Rules > Custom Rules** and paste into an empty rules editor.
4. Click **Check Rule Syntax**, then save. KiCad maintains the project's own `.kicad_dru` file.
5. Set the Board Setup values below. Refill zones, run DRC, and resolve the reported issues.

If the project already has rules, merge deliberately instead of replacing them. Keep only one `(version 1)` header. Custom rules are evaluated from the bottom, per applicable constraint; general rules can override netclass settings. Preserve stricter current, voltage, and other circuit-specific requirements in reviewed rules after this profile. [3]

An alternative for a NEW project with no existing rules is to close KiCad, copy the selected file beside the board, and rename it to the board/project stem, such as `MyBoard.kicad_dru` alongside `MyBoard.kicad_pcb`. Reopen and check syntax. Do not overwrite an existing rules file.

## Board Setup values to enter separately

Custom rules do not establish all board configuration or routing defaults.

| Setting | Recommended profile | Minimum profile |
|---|---:|---:|
| Physical Stackup: copper layers | 2 | 2 |
| Constraints: minimum clearance | 0.254 mm | 0.2032 mm |
| Constraints: minimum track width | 0.254 mm | 0.2032 mm |
| Constraints: minimum connection width | 0.254 mm | 0.2032 mm |
| Constraints: minimum via diameter | 1.30 mm | 0.90 mm |
| Constraints: minimum through-hole | 0.70 mm for supplied toolset | 0.70 mm for supplied toolset |
| Constraints: minimum annular width | 0.254 mm, our starting choice | 0.10 mm if retaining 0.90/0.70 mm vias |
| Default netclass: clearance | 0.254 mm | 0.2032 mm |
| Default netclass: track width | 0.40 mm, our starting choice | 0.2032 mm |
| Default netclass: via diameter / hole | 1.30 / 0.70 mm | 0.90 / 0.70 mm |

Board-level minimums cannot be relaxed by custom rules. A retained 0.254 mm annular minimum, for example, correctly prevents the minimum profile's 0.90/0.70 mm via: its radial ring is only (0.90 - 0.70) / 2 = 0.10 mm. Prefer larger pads when possible. The annular starting choices here are not separately published Voltera limits.

Do not lower existing circuit-specific clearances merely to match this table. The 0.70 mm hole minimum assumes the supplied drill set, not an absolute machine capability. Match actual hole sizes to the bits being used. [5]

## What the files do

| Rule | Behavior |
|---|---|
| Track width | Checks tracks/arcs against the selected width |
| Clearance | Checks separation between different-net conductive objects |
| Connection width | Checks pad-to-zone connection width; not every narrow artwork feature |
| Zone isolation | Uses 0.4064 mm / 16 mil clearance for zones |
| Thermal geometry | Sets gap and requested spoke width; the spoke-width constraint is `opt`, not an independent minimum check |
| Rivet via assertion | Requires through vias with a 0.70, 1.50, or 1.60 mm hole |
| Small via diameter | Requires the profile's pad diameter for a 0.70 mm via hole |
| Large via diameter | Requires at least 2.20 mm for a 1.50/1.60 mm via hole |
| Inner-layer routing | Disallows tracks and zones on internal copper layers |

All checks use KiCad's default error severity. The thermal settings influence zone generation; refill before inspecting. Existing geometry is not automatically resized.

The three rivet rules intentionally assume rivets at every via. If using another interlayer connection method, remove or adapt that complete three-rule group. Their conditions inspect `Via` objects, not component pads or mechanical holes.

## Manual checks still required

- **Riveted component pads:** small rivets need a 0.70 mm drill and at least 0.90 mm pad; large rivets need the matching 1.50/1.60 mm drill and at least 2.20 mm pad. Enlarge pads where spacing permits. Check both pad axes, hole position, and lead fit. These dimensions are NOT automatically enforced on footprint pads by these files. [2]
- **Hatching:** use actual hatch fill, line width 0.254 mm as a starting choice, and a gap appropriate to the circuit. Voltera recommends line width below 14 mil and below twice the V-One pass spacing if that setting changes. Set zone minimum width and thermal spokes appropriately. [1]
- **Packages:** conductive-print guidance is at least 0.65 mm IC pitch and 0603 imperial passives. Inspect actual pad geometry; DRC cannot infer general package suitability. [1]
- **Physical layout:** fit the 128 x 116 mm print area, allow clamp clearance, set actual board thickness, and use two layers. [6]
- **Drilling:** inspect all component and mechanical holes against available bits. Large rivet heads occupy the space between typical 2.54 mm header pins. [2,5]
- **Electrical performance:** trace printability does not establish ampacity, voltage isolation, impedance, or ink resistance. Use the material data and circuit requirements.
- **Exports:** apply Voltera's Gerber and Excellon export guide; DRC files cannot configure those dialogs. [4]

## Validation and limits

The delivered files were checked for balanced syntax, rule structure, documented constraint/property names, and the intended via-size mappings. Native KiCad is not installed in the authoring environment, so these files have NOT been executed by KiCad's parser or DRC engine. Run **Check Rule Syntax** and DRC in your installed version before relying on them. No physical print was tested.

The rule vocabulary was cross-checked against the KiCad 9 and 10 manuals. Older versions are not claimed as validated. Neither profile replaces footprint review, Gerber preview, or calibration.

## Sources

Accessed 2026-09-28, America/New_York. Material is paraphrased; the numeric limits remain attributable to their publishers.

1. Voltera, Circuit Design Guidelines: https://docs.voltera.io/docs/v-one/learn-v-one/circuit-design-for-v-one/circuit-design-guidelines
2. Voltera, Working with Rivets: https://docs.voltera.io/docs/v-one/learn-v-one/drill-attachment/working-with-rivets
3. KiCad, custom rules: https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#custom_design_rules and https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#custom_design_rules
4. Voltera, KiCad Export Guide: https://docs.voltera.io/docs/v-one/learn-v-one/circuit-design-for-v-one/ecad-export-guides/kicad-export-guide
5. Voltera, Custom Drill Bit Sizes: https://docs.voltera.io/docs/v-one/learn-v-one/drill-attachment/custom-drill-bit-sizes
6. Voltera, Technical Specifications: https://www.voltera.io/technical-specifications
