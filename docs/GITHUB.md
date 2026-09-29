# Publish this repository to GitHub

Suggested repository name: `voltera-vone-kicad-drc`

Suggested description: `KiCad design-rule profiles and fabrication checklists for Voltera V-One conductive-ink PCB printing.`

Suggested topics: `kicad`, `pcb`, `drc`, `voltera`, `v-one`, `electronics`, `prototyping`.

## Upload with Git

Create an empty repository under your chosen GitHub account or organization. Do not initialize another README or license there; both are included here. Extract the release ZIP and open a terminal inside the extracted folder containing `README.md`.

```sh
git init -b main
git add .
git commit -m "Package V-One KiCad DRC profiles v1.0.1"
```

Then copy the exact remote URL GitHub shows for your new repository:

```sh
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_REPOSITORY_URL` before running that command. Your local Git identity and GitHub authentication must already be configured. The package contains source files, not a `.git` history or configured remote.

## Verify and release

1. Open Actions and confirm **Repository checks** passes. Actions must be enabled on the destination repository.
2. Preserve the README's native-KiCad and physical-print validation status until those checks are actually performed.
3. Run `python3 tools/build_release.py` to generate ZIP and SHA-256 files under `dist/`.
4. If ready to publish a version, create a `v1.0.1` tag and GitHub release, use the matching changelog entry, and attach those generated files.

GitHub Pages is not needed: this is a rule/documentation repository, not a web application. Keep the included full GNU GPL v3 license.
