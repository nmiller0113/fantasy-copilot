#!/usr/bin/env python3
"""Print the starters whose absence plan is still open (If out = UNSETTLED or "-") as
"CODE | player | pos" rows, for the refresh's roles collector (args.openPlans).

    python3 refresh-seed.py --dir <kb>
"""
import argparse, glob, os, re
ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--dir', required=True); a = ap.parse_args()
STARTER = re.compile(r'starter|RB1|WR1|WR2|TE1|QB1', re.I)
for p in sorted(glob.glob(os.path.join(a.dir, 'teams', '*.md'))):
    code = os.path.basename(p)[:-3]; lines = open(p, encoding='utf-8').read().split('\n')
    i = next((k for k, l in enumerate(lines) if l.strip() == '## Rooms'), -1)
    if i < 0: continue
    for l in lines[i + 3:]:
        if not l.startswith('|'): break
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 8 and STARTER.search(c[3]) and (c[5] == '-' or c[5].upper().startswith('UNSETTLED')):
            print(f'{code} | {c[0]} | {c[1]}')
