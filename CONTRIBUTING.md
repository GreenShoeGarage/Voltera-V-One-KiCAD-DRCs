# Contributing

For a rule change, describe the manufacturing problem, cite the relevant primary Voltera/KiCad source, and identify whether the value is a published limit or a project recommendation.

Keep the two profiles independent. Preserve their source comments. Account for custom-rule precedence and board-wide minimums. Do not claim a condition is enforced on component pads when its scope is only vias.

Before submitting:

1. Run `python3 tools/validate_repo.py`.
2. Follow [native verification](docs/TESTING.md) for any changed rule and report the exact KiCad version and observed violations.
3. Update the setup guide and changelog when behavior changes.
4. Add new distributable files to `MANIFEST.txt`.

Changes to checker, workflow, and packaging infrastructure need the relevant local check; they do not require a fabricated PCB. Physical-print claims require actual recorded print results. Contributions to original content are accepted under GPL-3.0-only.
