#!/usr/bin/env python3
"""The source tables the knowledgebase keeps, and nothing else: print the pull list for a
build or a refresh, or check that the files a run needs are present.

    python3 pull-list.py --dir <kb> --annual            # new season: everything
    python3 pull-list.py --dir <kb> --week N            # in season: the weekly set
    python3 pull-list.py --dir <kb> --week N --check    # refuse the run if any is missing

Each row: file name under data/, cadence, where it comes from (a page read in the browser
with the in-page rewrite, or a Draft Sharks tool), and the columns to keep at pull time.
Rows the fat audit of 2026-09-04 removed are not here and are never pulled again: the
per-defender advanced defense page, the advanced receiving page, the QB historical stats,
the depth-chart snapshot (read live), team advanced pages older than the current season,
EPA tables past the two the ratings use, and any season more than three back.
"""
import argparse, glob, os, re, sys

# (file, cadence, source, keep)
TABLES = [
    ('teams.md', 'season', 'written by hand at the season start', 'code and every spelling'),
    ('ds-fantasy-points-allowed-<season>.md', 'weekly in season, else season', 'Draft Sharks Tools > Fantasy Points Allowed', 'QB RB WR TE avg points and adjusted %'),
    ('ds-historical-stats-<season>-rb.md', 'weekly in season, else season', 'Draft Sharks Tools > Historical Stats, RB', 'opportunity share, red-zone opportunities, targets'),
    ('ds-historical-stats-<season>-wr.md', 'weekly in season, else season', 'Draft Sharks Tools > Historical Stats, WR', 'target share, end-zone targets, yards per route'),
    ('ds-historical-stats-<season>-te.md', 'weekly in season, else season', 'Draft Sharks Tools > Historical Stats, TE', 'target share, end-zone targets'),
    ('ds-offensive-line-rankings-<season>.md', 'season (the annual article)', 'Draft Sharks offensive line rankings article', 'rank, tier, quoted component ranks'),
    ('pfr-advanced-passing-<season>.md', 'weekly in season; prior two seasons once', 'pro-football-reference.com/years/<season>/passing_advanced.htm', 'Player Tm Att Sk Prss% PktTime Bltz Scrm RPO PA IAY'),
    ('pfr-advanced-rushing-<season>.md', 'weekly in season', 'pro-football-reference.com/years/<season>/rushing_advanced.htm', 'Player Tm Att YBC YAC BrkTkl'),
    ('pfr-team-advanced-<season>.md', 'weekly in season', 'pro-football-reference.com/years/<season>/advanced.htm', 'team rows, page chrome stripped'),
    ('pfr-redzone-rushing-<season>.md', 'weekly in season', 'pro-football-reference.com/years/<season>/redzone-rushing.htm', 'rows with 5+ attempts'),
    ('pfr-redzone-receiving-<season>.md', 'weekly in season', 'pro-football-reference.com/years/<season>/redzone-receiving.htm', 'rows with 5+ targets'),
    ('pfr-redzone-passing-<season>.md', 'weekly in season', 'pro-football-reference.com/years/<season>/redzone-passing.htm', 'quarterback rows'),
    ('pfr-fantasy-<season>.md', 'season; prior two seasons once', 'pro-football-reference.com/years/<season>/fantasy.htm', 'Player Tm Pos Age G GS RushAtt Tgt Rec PPR, 100-PPR floor or 2026-rostered'),
    ('pfr-team-offense-<season>.md', 'weekly in season; prior two seasons once', 'pro-football-reference.com/years/<season>/index.htm', 'plays, attempts, sacks taken, sack rate'),
    ('pfr-team-defense-<season>.md', 'weekly in season; prior two seasons once', 'pro-football-reference.com/years/<season>/opp.htm', 'blitz hurry pressure sacks missed tackles'),
    ('espn-win-rates-<season>.md', 'season (the annual leaderboard)', 'ESPN Analytics win rates article', 'team PBWR RBWR PRWR RSWR with ranks'),
    ('sharp-defense-scheme-rates-<season>.md', 'season (published before the new season)', 'Sharp Football Analysis coverage and tendencies pages', 'man zone single-high blitz box sub'),
    ('rbsdm-neutral-pass-rate-<span>.md', 'season', 'rbsdm.com Neutral Pass Freq table', 'team pass rate, the span the tab covers'),
    ('host-adp-<date>.md', 'before each draft, draft season only', "the host's draft-analysis ADP page where a sharp-user ADP is published", 'player, pos, team, basic ADP last 7 days, sharp-user ADP last 7 days'),
    ('ngs-passing-<season>.md', 'weekly in season', 'nextgenstats.nfl.com passing leaders', 'time to throw, aggressiveness, CPOE'),
    ('teamrankings-<season>.md', 'weekly in season', 'teamrankings.com team stat pages', 'plays per game, pass share, opponent plays, red-zone TD rate'),
]
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True); ap.add_argument('--annual', action='store_true'); ap.add_argument('--week', type=int, default=0); ap.add_argument('--check', action='store_true')
a = ap.parse_args()
weekly = [t for t in TABLES if t[1].startswith('weekly')]
rows = TABLES if a.annual or not a.week else weekly
print(f'{"file":45s} {"cadence":40s} source | keep')
for f, cad, src, keep in rows: print(f'{f:45s} {cad:40s} {src} | {keep}')
if a.check:
    # A "before each draft" table exists only in draft season and only where the host
    # publishes a sharp-user ADP, so it is listed but never required by the gate.
    required = [t for t in rows if not t[1].startswith('before each draft')]
    missing = []
    for f, cad, src, keep in required:
        pat = os.path.join(a.dir, 'data', f.replace('<season>', '*').replace('<span>', '*').replace('<date>', '*'))
        if not glob.glob(pat): missing.append(f)
    if missing:
        print('MISSING:', ', '.join(missing)); sys.exit(1)
    optional = len(rows) - len(required)
    print(f'check: all {len(required)} present' + (f' ({optional} draft-season table listed, not required)' if optional else ''))
