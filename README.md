# Voltera V-One KiCad DRC

KiCad custom design-rule profiles and fabrication checklists for printing conductive circuits with the Voltera V-One.

**Start with the 10 mil profile.** This project includes a separate 8 mil profile for designs approaching Voltera's published minimum. Both assume riveted through vias. These are independent community rules, not an official Voltera product.

Version **1.0.1** · **GNU GPL v3 only** · Intended for **KiCad 9 and 10**

## Quick start

1. Download or clone this repository. No compilation or plugin installation is needed to use the rules.
2. Back up your KiCad project and existing custom rules.
3. Copy the contents of [VONE-10mil-recommended.kicad_dru](VONE-10mil-recommended.kicad_dru).
4. Open **PCB Editor → File → Board Setup → Design Rules → Custom Rules** and paste into an empty editor. Merge deliberately if rules already exist; keep one `(version 1)` header and preserve stricter project requirements.
5. Select **Check Rule Syntax**, then save.
6. Enter the complementary constraints and routing defaults in the [setup guide](VONE-DRC-README.md#board-setup-values-to-enter-separately).
7. Refill zones, run DRC, review footprints, and follow the [Gerber/drill export checklist](docs/EXPORTING.md).

Use only one profile in a project. Rules inspect geometry; they do not automatically repair existing tracks or footprints.

## Profiles

| File | Track width / different-net clearance | Small rivet via pad / hole |
|---|---:|---:|
| [Recommended](VONE-10mil-recommended.kicad_dru) | 10 mil / 0.254 mm | 1.30 / 0.70 mm |
| [Published-minimum profile](VONE-8mil-minimum.kicad_dru) | 8 mil / 0.2032 mm | 0.90 / 0.70 mm |

The 1.30 mm pad is our conservative starting choice. Voltera's small-rivet head-coverage minimum is 0.90 mm. Both profiles use 16 mil zone isolation and require a pad diameter of at least 2.20 mm around large-rivet vias. See the setup guide for assumptions, provenance, and manual checks.

## Included

- Two editable `.kicad_dru` profiles, nine rules each.
- [Detailed installation and Board Setup guide](VONE-DRC-README.md).
- [Export checklist](docs/EXPORTING.md) and [native KiCad verification procedure](docs/TESTING.md).
- [GitHub publishing instructions](docs/GITHUB.md).
- Dependency-free structural checker and reproducible release builder.
- GitHub Actions workflow, issue and pull-request templates, and full [GPL v3 license](LICENSE).

## Validation status

**Structural checks pass; native KiCad and physical printing remain untested.** The checker validates file structure and a documented subset of rule syntax. It does not execute conditions, emulate DRC, check a board, or establish printability. GitHub Actions runs the same structural check. See [VALIDATION.md](VALIDATION.md) for the release record.

For local repository checks, install Python 3.10 or newer and run:

```sh
python3 tools/validate_repo.py
```

On Windows, `py -3 tools/validate_repo.py` is an alternative. Python is only needed for repository tooling, not for importing the rule files into KiCad.

Build a distribution and its SHA-256 checksum:

```sh
python3 tools/build_release.py
```

The output goes to `dist/`. The builder includes exactly the files in [MANIFEST.txt](MANIFEST.txt).

## Design review still required

Review component-pad dimensions, rivet fit, available drill bits, package pitch, hatch fill, clamping, and electrical performance. The via rules do not automatically validate riveted component pads. Gerber and Excellon export options must be set separately.

## Contributing and licensing

See [CONTRIBUTING.md](CONTRIBUTING.md). Original repository content is licensed under **GPL-3.0-only**; the complete license is included. Voltera and KiCad names identify compatibility and do not imply affiliation. Primary technical sources are listed in the [setup guide](VONE-DRC-README.md#sources).
