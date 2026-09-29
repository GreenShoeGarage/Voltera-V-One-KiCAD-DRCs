#!/usr/bin/env python3
"""Build the explicit source manifest into a deterministic ZIP and SHA-256."""
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import hashlib
from pathlib import Path
import zipfile

from validate_repo import ROOT, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist', help='Output directory (default: dist)')
    args = parser.parse_args()
    files = validate()
    version = (ROOT / 'VERSION').read_text().strip()
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f'VONE-KiCad-DRC-v{version}-github-ready.zip'
    prefix = f'voltera-vone-kicad-drc-{version}'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for relative in sorted(files):
            info = zipfile.ZipInfo(f'{prefix}/{relative}', date_time=(2026, 9, 28, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, (ROOT / relative).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as check:
        if check.testzip() is not None or len(check.infolist()) != len(files):
            raise RuntimeError('Archive integrity check failed')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + '.sha256')
    checksum.write_text(f'{digest}  {archive.name}\n', encoding='utf-8')
    print(f'Created {archive}')
    print(f'Created {checksum}')


if __name__ == '__main__':
    main()
