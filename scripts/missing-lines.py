#!/usr/bin/env python3
"""The one yardstick for a gap fill: lines that say a fact is missing.

Counts, across teams/ nfl/ coach/ oline/, every line carrying a gap marker, an
unverified marker, or prose saying a figure was not found, not fetched, not reached,
paywalled or not verified. Progress is measured on this count before and after a
round, never on marker counts alone. With --write it also saves the file list as the
next round's selection (build/gap-fill-<label>-files.json: the file list and, under
"open", every matching line per file with its line number, which the fill prompts quote).

    python3 missing-lines.py --dir <kb> [--write <label> --date YYYY-MM-DD] [--by-file]
"""
import argparse, glob, json, os, re

MISS = re.compile(r'\(Gap|not (?:found|fetched|reached|obtained|captured|retrieved|retrievable|verified|measured|located|surfaced)'
                  r'|no (?:data|figure|number|source) (?:reached|found|retrieved|obtained)|\[unverified'
                  r'|paywalled|could not be (?:fetched|read|retrieved|reached)|NOT (?:OBTAINED|retrieved)', re.I)
SETS = ('teams', 'nfl', 'coach', 'oline')

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True)
ap.add_argument('--write', help='label for build/gap-fill-<label>-files.json')
ap.add_argument('--date', default='')
ap.add_argument('--by-file', action='store_true')
a = ap.parse_args()

files, total, open_lines = [], 0, {}
for s in SETS:
    for p in sorted(glob.glob(os.path.join(a.dir, s, '*.md'))):
        hits = [f'L{i}: {l.rstrip()[:240]}' for i, l in enumerate(open(p, encoding='utf-8'), 1) if MISS.search(l)]
        n = len(hits)
        if n:
            rel = os.path.relpath(p, a.dir).replace(os.sep, '/')
            files.append((rel, n)); total += n; open_lines[rel] = hits
            if a.by_file: print(f'{n:4d} {rel}')
print(f'missing-fact lines {total} in {len(files)} files')
if a.write:
    out = os.path.join(a.dir, 'build', f'gap-fill-{a.write}-files.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({'date': a.date, 'selection': 'every profile with a line matching the missing-fact patterns (marker or prose), missing-lines.py', 'lines': total, 'files': [f for f, _ in files], 'open': open_lines}, open(out, 'w'), indent=1)
    odir = os.path.join(a.dir, 'build', f'gap-fill-{a.write}-open')
    os.makedirs(odir, exist_ok=True)
    for f, lines in open_lines.items():
        name = f[:-3] if f.endswith('.md') else f
        open(os.path.join(odir, name.replace('/', '__') + '.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('wrote', out, 'and', len(open_lines), 'open-line files under', odir)
