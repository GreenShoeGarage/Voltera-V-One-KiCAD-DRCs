# Release validation record

Version: **1.0.1**. Packaging date: **2026-09-28**, America/New_York.

| Check | Result |
|---|---|
| Rule expression structure and documented subset | Passed for both profiles |
| Rule conditions and numeric constraints vs. 1.0 | Unchanged; comments only updated |
| Relative documentation links and required files | Passed |
| Distribution manifest completeness | Passed |
| Python tool syntax and local execution | Passed |
| GitHub workflow YAML structure | Parsed locally |
| Archive CRC and manifest membership | Passed |
| Repeated-build reproducibility | Matching ZIP SHA-256 |
| Full GNU GPL v3 license | Included |
| Native KiCad parser and DRC | Not run; KiCad unavailable here |
| GitHub-hosted workflow execution | Not run; repository not published by this task |
| Physical V-One printing | Not run |

The structural checker is a narrow linter, not KiCad. Follow [TESTING.md](docs/TESTING.md) to establish native and physical results for a specific environment. This report describes the packaged release, not later modifications.
