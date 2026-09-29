#!/usr/bin/env python3
"""Lint this repository's rule subset; does not run KiCad or evaluate DRC."""
# SPDX-License-Identifier: GPL-3.0-only

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '__pycache__', 'dist', '.venv', 'local-checks', '.idea', '.vscode'}
TOKEN = re.compile(r'\s+|#[^\n]*|\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"#]+')
DIMENSION = re.compile(r'[0-9]+(?:\.[0-9]+)?(?:mm|mil)')
MODIFIERS = {
    'track_width': {'min', 'opt', 'max'},
    'clearance': {'min'},
    'connection_width': {'min'},
    'thermal_relief_gap': {'min'},
    'thermal_spoke_width': {'opt'},
    'via_diameter': {'min', 'max'},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_rules(text):
    """Return nested expressions, preserving quoted atoms; no evaluation."""
    stack = [[]]
    offset = 0
    while offset < len(text):
        match = TOKEN.match(text, offset)
        require(match is not None, f'Unexpected or unterminated token near offset {offset}')
        token = match.group()
        offset = match.end()
        if token.isspace() or token.startswith('#'):
            continue
        if token == '(':
            child = []
            stack[-1].append(child)
            stack.append(child)
        elif token == ')':
            require(len(stack) > 1, 'Unmatched closing parenthesis')
            stack.pop()
        else:
            stack[-1].append(token)
    require(len(stack) == 1, 'Unclosed expression')
    return stack[0]


def quoted(atom):
    return isinstance(atom, str) and len(atom) >= 2 and atom.startswith('"') and atom.endswith('"')


def validate_rules(path):
    expressions = parse_rules(path.read_text(encoding='utf-8'))
    require(expressions and expressions[0] == ['version', '1'], 'Expected (version 1) first')
    names = set()
    for rule in expressions[1:]:
        require(isinstance(rule, list) and len(rule) >= 3 and rule[0] == 'rule', 'Expected rule expression')
        require(quoted(rule[1]) and rule[1] not in names, 'Missing/duplicate quoted rule name')
        names.add(rule[1])
        constraints = set()
        for clause in rule[2:]:
            require(isinstance(clause, list) and len(clause) >= 2, 'Invalid rule clause')
            kind = clause[0]
            if kind in {'condition', 'layer', 'severity'}:
                require(len(clause) == 2, f'Invalid {kind} clause')
                if kind == 'condition':
                    require(quoted(clause[1]) and '\n' not in clause[1], 'Condition must be a quoted single-line expression')
                elif kind == 'severity':
                    require(clause[1] in {'error', 'warning', 'ignore', 'exclusion'}, 'Unknown severity')
                else:
                    require(clause[1] in {'inner', 'outer', 'F.Cu', 'B.Cu'}, 'Layer outside supported subset')
                continue
            require(kind == 'constraint' and len(clause) >= 3, 'Unknown/incomplete clause')
            name = clause[1]
            require(name not in constraints, 'Duplicate constraint type within rule')
            constraints.add(name)
            if name == 'assertion':
                require(len(clause) == 3 and quoted(clause[2]), 'Assertion must be one quoted expression')
            elif name == 'disallow':
                require(all(x in {'track', 'via', 'micro_via', 'buried_via', 'pad', 'zone', 'text', 'graphic', 'hole', 'footprint'} for x in clause[2:]), 'Unknown disallowed type')
            else:
                require(name in MODIFIERS, f'Unsupported constraint: {name}')
                used = set()
                for parameter in clause[2:]:
                    require(isinstance(parameter, list) and len(parameter) == 2, 'Invalid dimension parameter')
                    modifier, dimension = parameter
                    require(modifier in MODIFIERS[name] and modifier not in used, f'Invalid/repeated modifier for {name}')
                    require(isinstance(dimension, str) and DIMENSION.fullmatch(dimension), 'Expected numeric mm/mil dimension')
                    used.add(modifier)
        require(constraints, 'Rule has no constraints')
    require(names, 'No rules found')
    return len(names)


def manifest_files(root=ROOT):
    entries = [line.strip() for line in (root / 'MANIFEST.txt').read_text().splitlines() if line.strip() and not line.lstrip().startswith('#')]
    require(len(entries) == len(set(entries)), 'Duplicate manifest path')
    for entry in entries:
        relative = Path(entry)
        require(not relative.is_absolute() and '..' not in relative.parts and '\\' not in entry, f'Unsafe manifest path: {entry}')
        path = root / relative
        require(path.resolve().is_relative_to(root.resolve()) and not path.is_symlink(), f'Invalid file location: {entry}')
        require(path.is_file() and path.stat().st_size > 0, f'Missing/empty file: {entry}')
    return entries


def validate(root=ROOT):
    require(re.fullmatch(r'\d+\.\d+\.\d+', (root / 'VERSION').read_text().strip()), 'Invalid release version')
    files = manifest_files(root)
    for required in ['README.md', 'LICENSE', 'VERSION', 'MANIFEST.txt', 'VONE-DRC-README.md', '.github/workflows/checks.yml', 'VONE-10mil-recommended.kicad_dru', 'VONE-8mil-minimum.kicad_dru']:
        require(required in files, f'Missing required manifest entry: {required}')
    license_text = (root / 'LICENSE').read_text()
    require('GNU GENERAL PUBLIC LICENSE' in license_text and 'Version 3, 29 June 2007' in license_text and len(license_text) > 30000, 'Full GPL v3 license required')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not (set(p.relative_to(root).parts) & IGNORED) and p.name not in {'.DS_Store', 'Thumbs.db'} and not p.name.endswith(('~', '.swp')) and not p.name.startswith('.env')}
    require(actual == set(files), f'Manifest mismatch; unlisted: {sorted(actual - set(files))}; absent: {sorted(set(files) - actual)}')
    for entry in files:
        path = root / entry
        if path.suffix == '.kicad_dru':
            print(f'PASS {entry}: {validate_rules(path)} structurally valid rules')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', path.read_text()):
                if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                relative = target.split('#', 1)[0]
                require((path.parent / relative).exists(), f'Broken relative link in {entry}: {target}')
    print(f'PASS manifest, relative file links, license, and version: {len(files)} files')
    print('LIMIT: native KiCad syntax/DRC, expression evaluation, and printer tests are not performed.')
    return files


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, OSError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
