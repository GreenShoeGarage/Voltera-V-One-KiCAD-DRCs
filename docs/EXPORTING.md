# Exporting for the V-One

These settings accompany the DRC profiles; importing a rules file does not apply them. Labels vary by KiCad version. The [Voltera KiCad export guide](https://docs.voltera.io/docs/v-one/learn-v-one/circuit-design-for-v-one/ecad-export-guides/kicad-export-guide) illustrates KiCad 7; the current profiles target the documented KiCad 9/10 rule vocabulary.

## Gerber output

Open **PCB Editor → File → Plot**.

| Setting | Value |
|---|---|
| Format | Gerber |
| Layers | F.Cu, B.Cu, F.Paste, B.Paste as needed |
| Protel filename extensions | On |
| Coordinate format | 4.6 mm |
| Disable aperture macros | On |
| Use drill/place file origin | Off; pair with Absolute drill origin |
| Plot drawing sheet | Off |
| Plot on All Layers | Empty |
| Check zone fills before plotting | On |
| Mirror / negative output, where available | Off |

For a conservative parser-compatibility choice, leave extended X2 format and netlist attributes off; this is our additional recommendation, not an explicit requirement in Voltera's written guide. A Gerber job file is not needed for this workflow.

The older guide enables footprint values and references. Keep those objects on their documentation layers. Its "Do not tent vias" control concerns solder-mask output; in KiCad 9 that setting moved to Board Setup and via properties.

| Output | Purpose |
|---|---|
| `.gtl` | Top conductive pattern |
| `.gbl` | Bottom conductive pattern |
| `.gtp` | Top solder paste |
| `.gbp` | Bottom solder paste |

Avoid placing outlines, dimensions, and unwanted labels in conductive-pattern output. V-One software mirrors `.gbl` and `.gbp` automatically, so do not pre-mirror these files.

## Drill output

From Plot, open **Generate Drill Files**.

| Setting | Value |
|---|---|
| Format | Excellon |
| PTH and NPTH in one file | On |
| Origin | Absolute |
| Units | Millimeters |
| Zero format | Decimal |
| Mirror Y | Off |
| Map format | Optional; Gerber X2 follows Voltera's guide |

Use the `.drl` file for the holes. The drill map is a drawing, not the drilling program. Map X2 format is independent of circuit Gerber X2 output.

## Before loading the printer

Refill zones and run DRC. Open exported layers together in a Gerber viewer and check pad/hole registration, layer selection, dimensions, actual hatch fill, and absence of unwanted drawing objects. Verify each hole against the bit used. Preview the generated V-One toolpaths before dispensing.

Sources: [Voltera export guide](https://docs.voltera.io/docs/v-one/learn-v-one/circuit-design-for-v-one/ecad-export-guides/kicad-export-guide), [Voltera design guidance](https://docs.voltera.io/docs/v-one/learn-v-one/circuit-design-for-v-one/circuit-design-guidelines), and [KiCad plotting documentation](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#generating_outputs).
