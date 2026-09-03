#!/usr/bin/env python3
"""Build the knowledgebase's per-team schedule-strength tables and the NFL-wide
schedule-strength rollup from two files that already exist: the season schedule
and the defense ratings by position. A deterministic join: no model, no search,
no judgment. Re-run it after every ratings refresh.

    python3 scripts/schedule-tables.py --dir kb/<season> --date YYYY-MM-DD [--week N]

  --dir   the season's knowledgebase folder (references/knowledgebase.md, layout)
  --date  today, written into every file's "refreshed" line
  --week  in season: the coming week. Adds a "remaining" window from that week and
          applies the ratings file's "## Week N injury adjustments" table, whose
          rows are: Defense | Position | Season | Week N | Player out

Reads   <dir>/nfl/schedule.md          (falls back to nfl/schedule-<year>.md or
                                        league/schedule-<year>.md); one table row per
                                        team code, then 18 cells: @CODE, vs CODE or
                                        BYE (one BYE per row); notes under ## Notes
        <dir>/nfl/defense-ratings.md   (falls back to nfl/defense-ratings-<year>.md
                                        or league/defense-ratings-<year>.md)
Writes  <dir>/schedule/<CODE>.md for all 32 teams
        <dir>/nfl/schedule-strength.md (or league/, matching the ratings file)

Ratings are the words soft, average or tough in the first four rating columns of
the ratings table (a trailing marker such as "[2026-10-01]" is ignored). Letters in
the output: S soft, A average, T tough. Any missing team, missing rating, unknown
opponent or unreadable cell stops the run with a message; nothing is guessed.
Needs Python 3.8 or later and nothing else.
"""
import argparse
import glob
import os
import re

TEAMS = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET',
         'GB', 'HOU', 'IND', 'JAX', 'KC', 'LV', 'LAC', 'LAR', 'MIA', 'MIN', 'NE', 'NO',
         'NYG', 'NYJ', 'PHI', 'PIT', 'SF', 'SEA', 'TB', 'TEN', 'WAS']
POS = ['QB', 'RB', 'WR', 'TE']
LETTER = {'soft': 'S', 'average': 'A', 'tough': 'T'}
WINDOWS = [('Season (1-18)', 1, 18), ('Weeks 1-4', 1, 4), ('Weeks 5-14', 5, 14),
           ('Playoffs 15-17', 15, 17), ('Playoffs 16-17', 16, 17)]


def find(kb, stem):
    """First existing file among the layout's names for this stem."""
    for pat in (f'nfl/{stem}.md', f'nfl/{stem}-[0-9]*.md', f'league/{stem}.md', f'league/{stem}-[0-9]*.md'):
        hits = sorted(glob.glob(os.path.join(kb, pat)))
        if hits:
            return hits[0]
    raise SystemExit(f'no {stem} file under {kb}/nfl or {kb}/league')


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def rating_letter(cell):
    m = re.match(r'\s*(soft|average|tough)\b', cell, re.I)
    if not m:
        raise SystemExit(f'unreadable rating cell: {cell!r}')
    return LETTER[m.group(1).lower()]


def parse_schedule(path):
    sched, notes, in_notes = {}, [], False
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('## '):
                in_notes = line.startswith('## Notes')
            c = cells(line) if line.startswith('|') else None
            if c and c[0] in TEAMS and len(c) == 19 and not in_notes:
                sched[c[0]] = c[1:]
            elif in_notes and line.strip() and not line.startswith('#') and not line.startswith('|'):
                notes.append(line.rstrip())
    missing = [t for t in TEAMS if t not in sched]
    if missing:
        raise SystemExit(f'schedule rows missing: {missing}')
    for t, row in sched.items():
        if sum(1 for x in row if x == 'BYE') != 1:
            raise SystemExit(f'{t}: expected exactly one BYE in the row, got {row}')
    return sched, notes


def parse_ratings(path, week):
    ratings, adj, refreshed, section = {}, {}, '', ''
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('# '):
                m = re.search(r'refreshed (\d{4}-\d{2}-\d{2})', line)
                refreshed = m.group(1) if m else ''
            if line.startswith('## '):
                section = line.strip()
                continue
            if not line.startswith('|'):
                continue
            c = cells(line)
            if c[0] not in TEAMS:
                continue
            if week and section.startswith(f'## Week {week} injury adjustments'):
                if len(c) < 4 or c[1].upper() not in POS:
                    raise SystemExit(f'unreadable adjustment row (want Defense | Position | Season | Week {week} | Player out): {line.strip()!r}')
                adj[(c[0], c[1].upper())] = (rating_letter(c[3]), c[4] if len(c) > 4 else '')
            elif not section.startswith('## Week'):
                if len(c) >= 5 and c[0] not in ratings:
                    ratings[c[0]] = {p: rating_letter(c[i + 1]) for i, p in enumerate(POS)}
    missing = [t for t in TEAMS if t not in ratings]
    if missing:
        raise SystemExit(f'ratings missing for: {missing}')
    return ratings, adj, refreshed


def opp_code(cell):
    return cell.replace('vs ', '').replace('@', '').strip()


def rate_row(code, row, ratings, adj, week):
    out = []
    for w, cell in enumerate(row, start=1):
        if cell == 'BYE':
            out.append((w, 'BYE', None, ''))
            continue
        opp = opp_code(cell)
        if opp not in ratings:
            raise SystemExit(f'{code} week {w}: unknown opponent {cell!r}')
        r = dict(ratings[opp])
        note = ''
        if week and w == week:
            for p in POS:
                if (opp, p) in adj:
                    r[p] = adj[(opp, p)][0]
                    note += f'{p} {adj[(opp, p)][0]} ({adj[(opp, p)][1]}); '
        out.append((w, cell, r, note.strip('; ')))
    return out


def windows_for(week):
    w = list(WINDOWS)
    if week and week > 1:
        w.insert(1, (f'Remaining ({week}-18)', week, 18))
    return w


def counts(rated, lo, hi):
    c = {p: {'S': 0, 'A': 0, 'T': 0} for p in POS}
    for w, _cell, r, _ in rated:
        if r and lo <= w <= hi:
            for p in POS:
                c[p][r[p]] += 1
    return c


def write_team(kb, code, rated, notes, date, refreshed, week, sched_name, ratings_name):
    lines = [f'# {code} schedule strength - refreshed {date}', '',
             f'Built by schedule-tables.py from {sched_name} and {ratings_name} (ratings refreshed '
             f'{refreshed}). S soft, A average, T tough: what the opponent defense is likely to give up to '
             'that position. Facts only; read alongside the engine\'s projection, never ahead of it.', '',
             '| Week | Opponent | vs QB | vs RB | vs WR | vs TE |', '|---|---|---|---|---|---|']
    foot = []
    for w, cell, r, note in rated:
        if r is None:
            lines.append(f'| {w} | BYE | - | - | - | - |')
        else:
            star = '*' if note else ''
            lines.append(f'| {w} | {cell}{star} | {r["QB"]} | {r["RB"]} | {r["WR"]} | {r["TE"]} |')
            if note:
                foot.append(f'* Week {w} {cell}: injury adjustment, {note}')
    lines += foot + ['', '## Windows', '', '| Window | Pos | Soft | Average | Tough |', '|---|---|---|---|---|']
    for name, lo, hi in windows_for(week):
        c = counts(rated, lo, hi)
        for p in POS:
            lines.append(f'| {name} | {p} | {c[p]["S"]} | {c[p]["A"]} | {c[p]["T"]} |')
    lines.append('')
    season = counts(rated, 1, 18)
    for p in POS:
        po = ','.join((r[p] if r else '-') for w, _cell, r, _ in rated if 15 <= w <= 17)
        lines.append(f'- {p}: {season[p]["S"]} soft / {season[p]["A"]} average / {season[p]["T"]} tough '
                     f'over the season; weeks 15-17 {po}.')
    bye = next(w for w, _cell, r, _ in rated if r is None)
    mine = [n for n in notes if re.search(rf'\b{code}\b', n)]
    lines += ['', '## Notes', '', f'- Bye week {bye}.']
    lines += [n if n.lstrip().startswith('-') else f'- {n}' for n in mine] + ['']
    os.makedirs(os.path.join(kb, 'schedule'), exist_ok=True)
    with open(os.path.join(kb, 'schedule', f'{code}.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_league(out_path, all_rated, date, refreshed, week, sched_name, ratings_name):
    L = [f'# Schedule strength by position - refreshed {date}', '',
         f'Built by schedule-tables.py from the 32 schedule/<CODE>.md tables (ratings refreshed {refreshed}). '
         'Score per window = soft games minus tough games; ties broken by soft count, then team code. '
         'S soft, A average, T tough. Facts only; read alongside the engine\'s projection, never ahead of it.', '']
    for name, lo, hi in windows_for(week):
        L += [f'## {name}', '']
        for p in POS:
            rows = []
            for code, rated in all_rated.items():
                c = counts(rated, lo, hi)[p]
                rows.append((c['S'] - c['T'], c['S'], code, c))
            rows.sort(key=lambda x: (-x[0], -x[1], x[2]))

            def fmt(x):
                return f'{x[2]} ({x[3]["S"]}S/{x[3]["A"]}A/{x[3]["T"]}T)'
            L.append(f'- {p} softest: ' + ', '.join(fmt(x) for x in rows[:5]))
            L.append(f'- {p} toughest: ' + ', '.join(fmt(x) for x in reversed(rows[-5:])))
        L.append('')
    L += ['## Week-by-week matchup grid', '',
          'Cell: opponent then QB/RB/WR/TE letters; * = injury adjustment applied this week.', '',
          '| Team | ' + ' | '.join(f'Wk{w}' for w in range(1, 19)) + ' |', '|---|' + '---|' * 18]
    for code, rated in all_rated.items():
        cs = []
        for _w, cell, r, note in rated:
            cs.append('BYE' if r is None else
                      f'{cell.replace("vs ", "")} {r["QB"]}/{r["RB"]}/{r["WR"]}/{r["TE"]}{"*" if note else ""}')
        L.append(f'| {code} | ' + ' | '.join(cs) + ' |')
    L += ['', '## How this file is refreshed', '',
          f'Weekly, after {ratings_name} is refreshed (the season\'s points allowed blended in until four weeks '
          'are played, then actuals, with the coming week\'s injury adjustments as a table "Defense | Position | '
          'Season | Week N | Player out" under "## Week N injury adjustments"): run '
          'from the season folder `python3 schedule-tables.py --dir . --date <today> --week <coming week>`. It rewrites all '
          '32 schedule/<CODE>.md files and this file. No hand edits here; they are overwritten.', '',
          '## Sources', '', f'- {sched_name} (the schedule and its notes)',
          f'- {ratings_name} (ratings and their basis, with the week\'s injury adjustments)', '']
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--date', required=True)
    ap.add_argument('--week', type=int, default=0)
    a = ap.parse_args()
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', a.date):
        raise SystemExit('--date must be YYYY-MM-DD')
    if a.week < 0 or a.week > 18:
        raise SystemExit('--week must be 1 to 18 (omit it before the season)')
    sched_path = find(a.dir, 'schedule')
    ratings_path = find(a.dir, 'defense-ratings')
    sched_name = os.path.relpath(sched_path, a.dir)
    ratings_name = os.path.relpath(ratings_path, a.dir)
    sched, notes = parse_schedule(sched_path)
    ratings, adj, refreshed = parse_ratings(ratings_path, a.week)
    all_rated = {}
    for code in TEAMS:
        rated = rate_row(code, sched[code], ratings, adj, a.week)
        all_rated[code] = rated
        write_team(a.dir, code, rated, notes, a.date, refreshed, a.week, sched_name, ratings_name)
    out_path = os.path.join(os.path.dirname(ratings_path), 'schedule-strength.md')
    write_league(out_path, all_rated, a.date, refreshed, a.week, sched_name, ratings_name)
    print(f'schedule tables: {len(all_rated)} teams written to schedule/, {len(ratings)} defenses rated, '
          f'{len(adj)} week-{a.week} adjustments applied, {os.path.relpath(out_path, a.dir)} written')


if __name__ == '__main__':
    main()
