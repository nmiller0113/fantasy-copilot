#!/usr/bin/env python3
"""Lint every profile against the lean template (build/templates-lean.md): headings in order,
table headers exact, column counts right, minimum rows, no Sources or Gaps sections, no gap
parentheticals, no process tags except the two marker families [filled <date>: <source>] and
[unverified <date>], no URLs, no tool-budget narration. Exit 1 on any failure; the build and
every refresh stop on it. The last line also counts the "-" cells in the required columns
(age, role, status, absence plan, rookie evidence and verdict, tendency direction and number,
player direction, points allowed, defender status and what it softens, line starters): that
count is the build's progress figure and the refresh seed reads the same cells.

    python3 kb-lint.py --dir <kb> [--quiet]
"""
import argparse, glob, os, re, sys

SPEC = {
    'teams': {
        'head': re.compile(r'^# [A-Z]{2,3} .+ - refreshed \d{4}-\d{2}-\d{2}$'),
        'headings': ['## Rooms', '## Rookies and young players behind veterans', '## Coach statements', '## Media read (last 14 days)', '## Watch'],
        'tables': {'## Rooms': '| Player | Pos | Age | Role | Status | If out | Preseason usage and rest | Direction |',
                   '## Rookies and young players behind veterans': '| Player | Pos | Veteran ahead | Vet age | Vet games missed 2023-25 | Evidence | Takeover verdict |',
                   '## Media read (last 14 days)': '| Player | Tag | Outlets | Line |'},
        'minrows': {'## Rooms': 8},
        'required': {'## Rooms': [2, 3, 4, 5], '## Rookies and young players behind veterans': [5, 6]},
    },
    'coach-offense': {
        'head': re.compile(r'^# [A-Z]{2,3} offense staff - refreshed \d{4}-\d{2}-\d{2}$'),
        'headings': ['## Tendencies', '## Roster fit', '## What he has said'],
        'tables': {'## Tendencies': '| Tendency | Direction | Number (season, team, source) |',
                   '## Roster fit': '| Player | Pos | Direction | Driver |'},
        'minrows': {'## Tendencies': 6, '## Roster fit': 3},
        'required': {'## Tendencies': [1, 2], '## Roster fit': [2]},
    },
    'coach-defense': {
        'head': re.compile(r'^# [A-Z]{2,3} defense - refreshed \d{4}-\d{2}-\d{2}$'),
        'headings': ['## Gives up by position (2025 basis)', '## Key defenders', '## DEF/ST direction'],
        'tables': {'## Gives up by position (2025 basis)': '| Position | Points allowed per game | Rank (1 = softest) | Note |',
                   '## Key defenders': '| Player | Pos | Status | Absence softens |'},
        'minrows': {'## Gives up by position (2025 basis)': 4, '## Key defenders': 4},
        'required': {'## Gives up by position (2025 basis)': [1], '## Key defenders': [2, 3]},
    },
    'oline': {
        'head': re.compile(r'^# [A-Z]{2,3} offensive line - refreshed \d{4}-\d{2}-\d{2}$'),
        'headings': ['## Starters', '## Impact', '## Watch'],
        'tables': {'## Starters': '| Slot | Player | Note |'},
        'minrows': {'## Starters': 5},
        'required': {'## Starters': [1]},
    },
}
FORBID = [
    (re.compile(r'^#{2,4} (Sources|Gaps|Not retrieved)\b|\*\*(Sources|Gaps)\*\*', re.M), 'forbidden section'),
    (re.compile(r'\(Gap[:)]'), 'gap parenthetical'),
    (re.compile(r'\[(media pass|skeptic|round \d|gap fill|search|verified) [^\]]*\]'), 'process tag'),
    (re.compile(r'\[filled(?! \d{4}-\d{2}-\d{2}: [^\]]+\])'), 'malformed filled marker'),
    (re.compile(r'WebSearch|web-search budget|search budget|budget (was )?exhausted|session-wide|Method note|Research note', re.I), 'tool narration'),
    (re.compile(r'https?://'), 'URL'),
]
# The two marker families the vocabulary allows: [filled <date>: <data file or files, or outlet and date>] (check-fills.py validates the citation) and [unverified <date>].
ALLOW_TAG = re.compile(r'\[(filled \d{4}-\d{2}-\d{2}: [^\]]+|unverified \d{4}-\d{2}-\d{2})\]')

def kind_of(path):
    s = path.split(os.sep)
    if 'teams' in s: return 'teams'
    if 'oline' in s: return 'oline'
    if 'coach' in s: return 'coach-offense' if path.endswith('-offense.md') else 'coach-defense'
    return None

def lint(path, spec):
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n'); errs = []; open_cells = 0
    if not lines or not spec['head'].match(lines[0]): errs.append(f'header line: {lines[0][:80]!r}')
    pos = -1
    for h in spec['headings']:
        i = next((k for k, l in enumerate(lines) if l.strip() == h), -1)
        if i < 0: errs.append(f'missing heading {h}')
        elif i < pos: errs.append(f'heading out of order {h}')
        else: pos = i
    for h, header in spec['tables'].items():
        i = next((k for k, l in enumerate(lines) if l.strip() == h), -1)
        if i < 0: continue
        rows = []; j = i + 1
        while j < len(lines) and not lines[j].startswith('|'): j += 1
        if j >= len(lines) or lines[j].strip() != header:
            errs.append(f'{h}: table header is {lines[j].strip()[:90] if j < len(lines) else "missing"!r}'); continue
        ncol = header.count('|') - 1; j += 2
        while j < len(lines) and lines[j].startswith('|'):
            if lines[j].count('|') - 1 != ncol: errs.append(f'{h}: row has {lines[j].count("|") - 1} cells, want {ncol}: {lines[j][:60]!r}')
            cells = [c.strip() for c in lines[j].strip().strip('|').split('|')]
            open_cells += sum(1 for k in spec.get('required', {}).get(h, []) if k < len(cells) and cells[k] == '-')
            rows.append(lines[j]); j += 1
        if len(rows) < spec['minrows'].get(h, 0): errs.append(f'{h}: {len(rows)} rows, want at least {spec["minrows"][h]}')
    clean = ALLOW_TAG.sub('', text)
    for rx, what in FORBID:
        m = rx.search(clean)
        if m: errs.append(f'{what}: {clean[max(0, m.start() - 40):m.end() + 40].strip()[:100]!r}')
    return errs, open_cells

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True); ap.add_argument('--quiet', action='store_true')
a = ap.parse_args()
files = sorted(glob.glob(os.path.join(a.dir, 'teams', '*.md')) + glob.glob(os.path.join(a.dir, 'coach', '*.md')) + glob.glob(os.path.join(a.dir, 'oline', '*.md')))
bad = 0; open_total = 0
for p in files:
    k = kind_of(p)
    if not k: continue
    errs, oc = lint(p, SPEC[k]); open_total += oc
    if errs:
        bad += 1
        if not a.quiet:
            for e in errs[:6]: print(f'FAIL {os.path.relpath(p, a.dir)}: {e}')
print(f'kb-lint: {len(files)} files, {bad} failing; open cells in required columns: {open_total}')
sys.exit(1 if bad else 0)
