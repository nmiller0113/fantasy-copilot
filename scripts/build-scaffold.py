#!/usr/bin/env python3
"""Scaffold the per-team profiles in the template shape, and fill what a table can fill.

    python3 build-scaffold.py --dir <kb> --date YYYY-MM-DD --season <season>         # write missing files as skeletons
    python3 build-scaffold.py --dir <kb> --date YYYY-MM-DD --season <season> --ages  # fill "-" Age / Vet age / Vet games missed cells by player name

Skeleton: every heading and table header of the templates in references/knowledgebase.md
(hardcoded here) for teams/, coach/ and oline/, a header line with the code, and the team-level numeric cells a saved table holds:
the four gives-up rows from ds-fantasy-points-allowed-<season-1>.md and the ESPN win rates
and sacks from espn-win-rates-<season-1>.md and pfr-team-offense-<season-1>.md when
present, each stamped [filled <date>: <file>]. Player rows are judgment and stay empty for
the judgment agent. --ages reads the pfr-fantasy-<season-1>, -<season-2>, -<season-3>
pages and fills, by exact player name, the Age cell (last season's age plus one), and the
Vet age and Vet games missed <season-3>-<season-1> cells (17 minus games played per season, summed
over the seasons the pages hold, and the cell says how many of the three that is; a
season a player is absent from, below the pull floor or out of the league, is not
counted as missed). Existing files are never overwritten; only "-" cells are filled.
Column positions: the scripts index the saved tables by position under the layouts
pull-list.py names (the DS points-allowed row is Team, then avg and adjusted pairs per
position; the ESPN row is Team, PRWR, RSWR, PBWR, RBWR; the team-offense row's sacks
taken sit 19th after the team), so a table trimmed to other columns yields "-", never a
wrong number from the wrong column. Needs Python 3.8 or later.
"""
import argparse, glob, os, re

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True); ap.add_argument('--date', required=True); ap.add_argument('--season', type=int, required=True)
ap.add_argument('--ages', action='store_true')
a = ap.parse_args(); K, D, S = a.dir, a.date, a.season
if not re.match(r'^\d{4}-\d{2}-\d{2}$', D): raise SystemExit('--date must be YYYY-MM-DD')
if S < 1900: raise SystemExit('--season must be a four-digit year')
teams_file = os.path.join(K, 'data', 'teams.md')
if not os.path.isfile(teams_file): raise SystemExit(f'no {teams_file}: write it first')
SPELL = {}
for raw in open(teams_file, encoding='utf-8'):
    c = [x.strip() for x in raw.strip().strip('|').split('|')] if '|' in raw and not raw.lstrip().startswith('#') else []
    if len(c) >= 2 and re.fullmatch(r'[A-Z]{2,3}', c[0]): SPELL[c[0]] = c
CODES = sorted(SPELL)

def rows_of(path):
    """Pipe-separated rows of a data table (lines with 2+ pipes after the header block)."""
    if not os.path.isfile(path): return []
    out = []
    for l in open(path, encoding='utf-8'):
        if l.count('|') >= 2 and not l.startswith('#'): out.append([c.strip() for c in l.strip().strip('|').split('|')])
    return out

def team_row(rows, code):
    forms = sorted(SPELL[code], key=len, reverse=True)
    for r in rows:
        for c in r[:2]:
            if any(c == f for f in forms): return r
    return None

prior = S - 1
# The rookies header's games-missed column names the three seasons behind the new one, so
# the header the skeleton writes is built from --season and never from a hardcoded year.
span = f'{S - 3}-{prior % 100:02d}'
fpa = rows_of(os.path.join(K, 'data', f'ds-fantasy-points-allowed-{prior}.md'))
espn = rows_of(os.path.join(K, 'data', f'espn-win-rates-{prior}.md'))
toff = rows_of(os.path.join(K, 'data', f'pfr-team-offense-{prior}.md'))

def skeleton(code):
    name = SPELL[code][-1]
    g = team_row(fpa, code); e = team_row(espn, code); o = team_row(toff, code)
    def gives(pos):
        if not g: return f'| {pos} | - | - | - |'
        # the DS table's row is Team | QB Avg | QB Adj | RB Avg | RB Adj | ...; the Adj cells carry '%', so the plain numbers are the four averages in position order
        nums = [c for c in g[1:] if re.match(r'^-?\d+(\.\d+)?$', c)]
        idx = {'QB': 0, 'RB': 1, 'WR': 2, 'TE': 3}[pos]
        return f'| {pos} | {nums[idx] if len(nums) > idx else "-"} [filled {D}: ds-fantasy-points-allowed-{prior}.md] | - | - |' if len(nums) > idx else f'| {pos} | - | - | - |'
    sacks = '-'
    if o:
        nums = [c for c in o[1:] if re.match(r'^-?\d+(\.\d+)?$', c)]
        sacks = f'{nums[18]} [filled {D}: pfr-team-offense-{prior}.md]' if len(nums) > 18 else '-'
    files = {
        f'teams/{code}.md': f"""# {code} {name} - refreshed {D}

Play caller: - | Head coach: - | Defensive coordinator: -

## Rooms

| Player | Pos | Age | Role | Status | If out | Preseason usage and rest | Direction |
|---|---|---|---|---|---|---|---|

## Rookies and young players behind veterans

| Player | Pos | Veteran ahead | Vet age | Vet games missed {span} | Evidence | Takeover verdict |
|---|---|---|---|---|---|---|

## Coach statements

- -

## Media read (last 14 days)

| Player | Tag | Outlets | Line |
|---|---|---|---|

## Watch

- -
""",
        f'coach/{code}-offense.md': f"""# {code} offense staff - refreshed {D}

Play caller: - | Head coach: - | OC if different: -

## Tendencies

| Tendency | Direction | Number (season, team, source) |
|---|---|---|
| RB concentration | - | - |
| RB targets | - | - |
| WR1 share | - | - |
| TE share | - | - |
| Pass rate vs league | - | - |
| Red zone | - | - |

## Roster fit

| Player | Pos | Direction | Driver |
|---|---|---|---|

## What he has said

- -
""",
        f'coach/{code}-defense.md': f"""# {code} defense - refreshed {D}

Coordinator: - | Scheme: - | {prior} blitz rate -, pressure rate -

## Gives up by position ({prior} basis)

| Position | Points allowed per game | Rank (1 = softest) | Note |
|---|---|---|---|
{gives('QB')}
{gives('RB')}
{gives('WR')}
{gives('TE')}

## Key defenders

| Player | Pos | Status | Absence softens |
|---|---|---|---|

## DEF/ST direction

-
""",
        f'oline/{code}.md': f"""# {code} offensive line - refreshed {D}

Rank: - of 32 (DS {S}) | ESPN {prior} pass block win rate {(e[3] if e and len(e) > 3 else '-')}, run block win rate {(e[4] if e and len(e) > 4 else '-')}{f' [filled {D}: espn-win-rates-{prior}.md]' if e else ''} | {prior} sacks allowed {sacks}, sack rate - | RB1 yards before contact {prior} - per attempt | QB pressure rate {prior} -

## Starters

| Slot | Player | Note |
|---|---|---|
| LT | - | - |
| LG | - | - |
| C | - | - |
| RG | - | - |
| RT | - | - |
| Depth | - | - |

## Impact

- RB1: -
- QB: -
- Pass-catchers: -

## Watch

- -
""",
    }
    written = 0
    for rel, body in files.items():
        p = os.path.join(K, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.isfile(p): open(p, 'w', encoding='utf-8').write(body); written += 1
    return written

def fill_ages():
    ages, games = {}, {}
    for yr in (prior, prior - 1, prior - 2):
        for r in rows_of(os.path.join(K, 'data', f'pfr-fantasy-{yr}.md')):
            if len(r) < 5 or not re.match(r'^\d+$', r[3] or ''): continue
            name = r[0]
            if yr == prior: ages[name] = int(r[3]) + 1
            games.setdefault(name, {})[yr] = int(r[4]) if re.match(r'^\d+$', r[4]) else 0
    def missed(name):
        # Only seasons the pages hold count: a season a player is absent from (below the pull
        # floor, not in the league) is not 17 games missed, so the cell says how many seasons
        # it covers.
        if name not in games: return None
        present = sorted(games[name])
        return f'{sum(17 - games[name][yr] for yr in present)} over {len(present)} of 3 seasons on the pages'
    changed = 0
    for p in sorted(glob.glob(os.path.join(K, 'teams', '*.md'))):
        lines = open(p, encoding='utf-8').read().split('\n'); sect = ''
        for i, l in enumerate(lines):
            if l.startswith('## '): sect = l.strip()
            if not l.startswith('|') or l.startswith('|---') or l.startswith('| Player'): continue
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if sect == '## Rooms' and len(c) == 8 and c[2] == '-' and c[0] in ages:
                c[2] = str(ages[c[0]]); changed += 1
            elif sect == '## Rookies and young players behind veterans' and len(c) == 7:
                vet = c[2]
                if c[3] == '-' and vet in ages: c[3] = str(ages[vet]); changed += 1
                if c[4] == '-' and missed(vet) is not None: c[4] = f'{missed(vet)} [filled {D}: pfr-fantasy-{prior}.md]'; changed += 1
            else: continue
            lines[i] = '| ' + ' | '.join(c) + ' |'
        open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'ages: {changed} cells filled from the fantasy pages')

if a.ages: fill_ages()
else:
    n = sum(skeleton(c) for c in CODES)
    print(f'scaffold: {n} files written for {len(CODES)} teams (existing files untouched)')
