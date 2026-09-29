# Verification

## Repository checks

Run `python3 tools/validate_repo.py` from the repository root. This dependency-free structural linter checks the distribution manifest, relative Markdown links, version, license presence, balanced rule expressions, unique rule names, and the supported constraint forms used in this repository.

It does **not** execute KiCad expressions, run KiCad DRC, evaluate pad connectivity, or certify manufacturability. Its accepted syntax is intentionally narrower than the full KiCad language. When adding other valid KiCad constructs, update the linter's supported subset after checking the official documentation.

The GitHub Actions workflow performs these checks and builds the release. It does not install or launch KiCad. The workflow has not been executed on GitHub as part of this initial packaging task.

## Native KiCad checks

Use a disposable project under the ignored `local-checks/` directory. Keep a record of KiCad version, profile, board constraints, input geometry, and actual results.

1. Paste one profile into Custom Rules and run **Check Rule Syntax**.
2. Apply the Board Setup values in the setup guide.
3. Add separated fixtures for the checks below, refill zones, then run DRC.
4. Check the rule name in each violation. Resolve unrelated outline/connectivity violations separately.
5. Repeat for the other profile; do not combine profiles or retain a stricter global minimum when testing the 8 mil boundaries.

| Fixture | Expected result to verify |
|---|---|
| 0.25 mm track in 10 mil profile | Width violation |
| 0.254 mm track in 10 mil profile | No width violation |
| 0.20 mm track in 8 mil profile | Width violation; 8 mil is exactly 0.2032 mm |
| 0.2032 mm track in 8 mil profile | No width violation |
| Different-net traces with sub-limit gap | Clearance violation |
| Via, 0.70 mm hole / 1.20 mm pad, recommended profile | Small-rivet diameter violation |
| Via, 0.70 mm hole / 1.30 mm pad, recommended profile | No rivet diameter/type violation |
| Via, 0.70 mm hole / 0.90 mm pad, minimum profile | No rivet diameter/type violation, with appropriate global annular minimum |
| Via, 1.60 mm hole / 2.00 mm pad | Large-rivet diameter violation |
| Via, 1.60 mm hole / 2.20 mm pad | No rivet diameter/type violation |
| Through via with 0.80 mm hole | Rivet assertion violation |
| Small pad-to-zone connection | Connection-width check should report the undersized connection |
| Zone adjacent to a different-net object | Refill/check should respect 16 mil isolation |

Passing one fixture does not mean the whole board passes. Through-hole footprint pads intentionally fall outside the via-specific rules and need manual rivet review. Verify actual hatch fill independently.

An optional native command after installing rules on your test project is:

```sh
kicad-cli pcb drc --exit-code-violations --output local-checks/drc.rpt local-checks/check.kicad_pcb
```

On macOS, KiCad documents the executable at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`; quote that path when invoking it. The rules file must share the board/project stem. Expect a nonzero result when intentionally testing violations. Source: [KiCad CLI documentation](https://docs.kicad.org/9.0/en/cli/cli.html).

## Physical verification

After native and Gerber checks, print a small coupon with representative tracks, gaps, pads, hatch, and rivets using your actual material/process. Record results rather than treating minimum design numbers as a guarantee. No physical test result is included with this release.
