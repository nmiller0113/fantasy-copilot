#!/usr/bin/env python3
"""Write build/gaps-remaining-<date>.md: every line in the profiles that still says a
fact is missing, by file, with what it says. It is the round's report, and it covers
the same lines the yardstick (missing-lines.py) counts, so the two totals agree.

    python3 gap-list.py --dir <kb> --date YYYY-MM-DD

Each row is one of: a gap marker with the reason the round wrote ("no reason written"
for a bare marker, which no round with search budget reached, so it was not searched,
not proven absent); an unverified line; or a prose line saying a fact was not found,
not fetched, not reached or paywalled, which no round stamped. Needs Python 3.8 or
later and nothing else.
"""
import argparse, collections, glob, os, re

MISS = re.compile(r'\(Gap|not (?:found|fetched|reached|obtained|captured|retrieved|retrievable|verified|measured|located|surfaced)'
                  r'|no (?:data|figure|number|source) (?:reached|found|retrieved|obtained)|\[unverified'
                  r'|paywalled|could not be (?:fetched|read|retrieved|reached)|NOT (?:OBTAINED|retrieved)', re.I)

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True)
ap.add_argument('--date', required=True)
a = ap.parse_args()
K, D = a.dir, a.date
if not re.match(r'^\d{4}-\d{2}-\d{2}$', D):
    raise SystemExit('--date must be YYYY-MM-DD')

out = [f'# Gaps remaining after the {D} fill rounds', '',
       'One row per line that still says a fact is missing, by file: a gap marker with the reason the round wrote '
       '(a bare marker carries "no reason written": no round with search budget reached it, so it was not searched, '
       'not proven absent), an unverified line, or a prose line no round stamped. The context is the text before the marker, cut to fit.', '']
tot = collections.Counter(); files = 0; lines_total = 0
for sub in ('teams', 'nfl', 'coach', 'oline'):
    for p in sorted(glob.glob(os.path.join(K, sub, '*.md'))):
        rel = os.path.relpath(p, K).replace(os.sep, '/'); rows = []
        for i, l in enumerate(open(p, encoding='utf-8').read().split('\n'), 1):
            if not MISS.search(l):
                continue
            lines_total += 1
            gaps = list(re.finditer(r'\(Gap[^)]*\)?', l))
            for m in gaps:
                reason = re.sub(r'^\(Gaps?[:,]?\s*', '', m.group(0)).rstrip(')').strip()
                ctx = l[max(0, m.start() - 110):m.start()].strip().lstrip('-|* ').strip()
                rows.append(f'- line {i} (Gap): {reason or "no reason written"} | context: {ctx}'); tot['gap'] += 1
            if '[unverified' in l:
                rows.append(f'- line {i} [unverified]: {l[:160].strip().lstrip("-|* ")}'); tot['unverified'] += 1
            elif not gaps:
                rows.append(f'- line {i} (prose): {l[:160].strip().lstrip("-|* ")}'); tot['prose'] += 1
        if rows:
            files += 1; out.append(f'## {rel} ({len(rows)})'); out.extend(rows); out.append('')
out.insert(3, f'Totals: {lines_total} lines in {files} files (the yardstick): {tot["gap"]} gap markers, {tot["unverified"]} unverified lines, {tot["prose"]} unstamped prose lines (rows exceed lines where one line carries two markers).')
out.insert(3, '')
target = os.path.join(K, 'build', f'gaps-remaining-{D}.md')
os.makedirs(os.path.dirname(target), exist_ok=True)
open(target, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'lines {lines_total} in {files} files: gaps {tot["gap"]}, unverified {tot["unverified"]}, prose {tot["prose"]}, wrote {target}')
