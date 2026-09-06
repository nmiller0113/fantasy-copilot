#!/usr/bin/env python3
"""Read the user's private transaction files, one per fantasy league, and print one
report of what every room did: a per-league manager digest, every player dropped in the
window with an estimated clear date (his drop date plus that league's waiver period),
the names other managers added in more than one league, and the user's own adds and
drops.

    python3 scripts/transactions.py --dir <folder> [--since YYYY-MM-DD] [--league <slug>]

  --dir     the folder holding leagues.md and one file per league. It is the user's own
            private folder, beside the private document, never inside this plugin.
  --since   first day of the window, inclusive. Default: seven days before the newest
            row read.
  --league  limit the run to one league slug from leagues.md.

Reads  <dir>/leagues.md   one pipe row per league:
                            slug | the user's manager name | waiver days | host
       <dir>/<slug>.md    one pipe row per player movement, as pulled from the host's
                            transactions page:
                            timestamp | manager | movement | player | pos | team |
                            designation | source | txn
                          timestamp is YYYY-MM-DD HH:MM; movement is ADD, DROP,
                          TRADE-IN or TRADE-OUT; source is FA, W, TRADE or -; txn is
                          the id of one host transaction, so an add and the drop that
                          made room for it carry the same txn and no other row in the
                          file carries it. The host prints no such id: the puller makes
                          one from the timestamp, the manager, and a suffix whenever the
                          page shows more than one of that manager's entries in that
                          minute, which waiver processing does routinely. Every other
                          cell the page leaves blank is written -; txn is required and
                          never blank, because it is what pairs a drop with its add.

Blank lines and lines starting with # are ignored. The same page pulled twice repeats
its rows, so rows are de-duplicated on timestamp, manager, movement and player, within
a league. Any other line that is not a pipe row, and any pipe row this shape cannot
read, stops the run with the file and the line number; nothing is guessed.

The script surfaces what the rooms did. It does not rate, rank or recommend, and no
count it prints is a verdict on a player. Needs Python 3.8 or later and nothing else.
"""
import argparse
import collections
import datetime
import os
import re

MOVES = ('ADD', 'DROP', 'TRADE-IN', 'TRADE-OUT')
SOURCES = ('FA', 'W', 'TRADE', '-')
TS = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')
DAY = re.compile(r'^\d{4}-\d{2}-\d{2}$')
FIELDS = ('timestamp', 'manager', 'movement', 'player', 'pos', 'team',
          'designation', 'source', 'txn')


def rows(path):
    """Yield (line number, cells) for every pipe row of a file, comments skipped."""
    if not os.path.isfile(path):
        raise SystemExit(f'no {path}: write it first (see the script header for its rows)')
    with open(path, encoding='utf-8') as f:
        for n, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '|' not in line:
                raise SystemExit(f'{path} line {n}: not a pipe row and not a # comment')
            yield n, [c.strip() for c in line.strip('|').split('|')]


def read_leagues(folder):
    path = os.path.join(folder, 'leagues.md')
    out = []
    for n, c in rows(path):
        if len(c) != 4:
            raise SystemExit(f'{path} line {n}: {len(c)} cells, need 4 '
                             '(slug | manager | waiver days | host)')
        slug, you, days, host = c
        if not re.fullmatch(r'[A-Za-z0-9_-]+', slug):
            raise SystemExit(f'{path} line {n}: slug "{slug}" must be letters, digits, '
                             'hyphen or underscore')
        if not you or not host:
            raise SystemExit(f'{path} line {n}: the manager and host cells cannot be empty')
        if not days.isdigit():
            raise SystemExit(f'{path} line {n}: waiver days "{days}" must be a whole '
                             'number of days')
        if any(lg['slug'] == slug for lg in out):
            raise SystemExit(f'{path} line {n}: league {slug} is listed twice')
        out.append({'slug': slug, 'you': you, 'days': int(days), 'host': host})
    if not out:
        raise SystemExit(f'{path} holds no league rows (slug | manager | waiver days | host)')
    return out


def read_moves(folder, league):
    path = os.path.join(folder, league['slug'] + '.md')
    seen = set()
    txns = {}
    out = []
    for n, c in rows(path):
        if len(c) != 9:
            raise SystemExit(f'{path} line {n}: {len(c)} cells, need 9 '
                             '(' + ' | '.join(FIELDS) + ')')
        for name, value in zip(FIELDS, c):
            if not value:
                raise SystemExit(f'{path} line {n}: {name} is empty; write - where the '
                                 'page shows nothing')
        ts, manager, move, player, pos, team, desig, src, txn = c
        if not TS.match(ts):
            raise SystemExit(f'{path} line {n}: timestamp "{ts}" must be YYYY-MM-DD HH:MM')
        try:
            when = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M')
        except ValueError:
            raise SystemExit(f'{path} line {n}: timestamp "{ts}" is not a real date and time')
        if move not in MOVES:
            raise SystemExit(f'{path} line {n}: movement "{move}" must be one of '
                             + ', '.join(MOVES))
        if src not in SOURCES:
            raise SystemExit(f'{path} line {n}: source "{src}" must be one of '
                             + ', '.join(SOURCES))
        if txn == '-':
            raise SystemExit(f'{path} line {n}: txn is -; every row needs the id of its '
                             'host transaction: the timestamp, the manager, and a suffix '
                             'when that manager has more than one entry in that minute')
        key = (ts, manager, move, player)
        if key in seen:
            continue
        seen.add(key)
        # One txn is one host transaction, which is what pairs a drop with the add that
        # made room for it. An id shared by unrelated rows would print a swap nobody
        # made, so a txn belongs to one timestamp, carries the adds and drops of one
        # manager, and holds at most one add and at most one drop: a host entry adds one
        # player and drops at most one. Waiver processing stamps a manager's claims with
        # the same minute, which is why the id takes a suffix and not the minute alone.
        # A trade is the exception the host itself makes: its TRADE-IN and TRADE-OUT rows
        # are one transaction between two managers, so they are held to the timestamp
        # only. This runs after the de-duplication above, so a repeated pull of one add
        # is not read as a second add.
        owns = move in ('ADD', 'DROP')
        prior = txns.get(txn)
        if prior is None:
            prior = txns[txn] = {'ts': ts, 'manager': None, 'ADD': False, 'DROP': False}
        elif prior['ts'] != ts:
            raise SystemExit(f'{path} line {n}: txn "{txn}" already belongs to the '
                             f'{prior["ts"]} transaction; one txn is one transaction')
        if owns:
            if prior['manager'] not in (None, manager):
                raise SystemExit(f'{path} line {n}: txn "{txn}" already carries the adds '
                                 f'and drops of {prior["manager"]}; an add and the drop '
                                 'that made room for it are one manager\'s move')
            if prior[move]:
                raise SystemExit(f'{path} line {n}: txn "{txn}" already holds one '
                                 f'{move.lower()}; one host entry adds one player and '
                                 'drops at most one, so give each entry in that minute '
                                 'its own id (the timestamp, the manager, a suffix)')
            prior['manager'] = manager
            prior[move] = True
        out.append({'when': when, 'day': when.date(), 'manager': manager, 'move': move,
                    'player': player, 'pos': pos, 'team': team, 'desig': desig,
                    'src': src, 'txn': txn, 'slug': league['slug']})
    return out


def table(head, body):
    line = '| ' + ' | '.join(head) + ' |'
    rule = '| ' + ' | '.join('---' for _ in head) + ' |'
    return [line, rule] + ['| ' + ' | '.join(r) + ' |' for r in body]


def by_pos(counter):
    if not counter:
        return '-'
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return ', '.join(f'{p} {n}' for p, n in items)


def swapped_for(league, row):
    """The player added in the same host transaction as this drop, or - if none."""
    for r in league['all']:
        if r['txn'] == row['txn'] and r['move'] == 'ADD':
            return r['player']
    return '-'


def picked_up(league, row):
    """The first add of this dropped player in this league after the drop, or None."""
    later = [r for r in league['all'] if r['player'] == row['player']
             and r['move'] == 'ADD' and r['when'] > row['when']]
    return min(later, key=lambda r: r['when']) if later else None


def managers_section(leagues):
    out = ['## Managers', '']
    for lg in leagues:
        out.append(f'### {lg["slug"]}')
        out.append('')
        if not lg['win']:
            out += ['No rows in the window.', '']
            continue
        adds = collections.defaultdict(collections.Counter)
        drops = collections.defaultdict(collections.Counter)
        txn_add = collections.defaultdict(set)
        txn_drop = collections.defaultdict(set)
        last = {}
        for r in lg['win']:
            m = r['manager']
            last[m] = max(last.get(m, r['day']), r['day'])
            if r['move'] == 'ADD':
                adds[m][r['pos']] += 1
                txn_add[m].add(r['txn'])
            elif r['move'] == 'DROP':
                drops[m][r['pos']] += 1
                txn_drop[m].add(r['txn'])
        order = sorted(last, key=lambda m: (-(sum(adds[m].values()) + sum(drops[m].values())),
                                            m.lower(), m))
        body = []
        for m in order:
            swaps = len(txn_add[m] & txn_drop[m])
            name = f'{m} (you)' if m == lg['you'] else m
            body.append([name, by_pos(adds[m]), by_pos(drops[m]), str(swaps), str(last[m])])
        out += table(['Manager', 'Adds', 'Drops', 'Swaps', 'Last move'], body) + ['']
    return out


def dropped_section(leagues):
    out = ['## Dropped (all leagues)', '']
    players = collections.OrderedDict()
    for lg in leagues:
        for r in lg['win']:
            if r['move'] != 'DROP':
                continue
            p = players.setdefault(r['player'], {'rows': [], 'entries': []})
            p['rows'].append(r)
            you = ' (you)' if r['manager'] == lg['you'] else ''
            clear = r['day'] + datetime.timedelta(days=lg['days'])
            back = picked_up(lg, r)
            gone = f' (since added by {back["manager"]} on {back["day"]})' if back else ''
            p['entries'].append((r['when'], lg['slug'],
                                 f'{lg["slug"]} {r["day"]} by {r["manager"]}{you}, '
                                 f'for {swapped_for(lg, r)}, clears {clear}{gone}'))
    if not players:
        return out + ['No rows in the window.', '']
    body = []
    for name, p in players.items():
        newest = max(p['rows'], key=lambda r: r['when'])
        entries = [e[2] for e in sorted(p['entries'], key=lambda e: (e[0], e[1]))]
        leagues_in = len({e[1] for e in p['entries']})
        body.append((leagues_in, newest['when'], name,
                     [name, newest['pos'], newest['team'], newest['desig'],
                      str(leagues_in), '; '.join(entries)]))
    body.sort(key=lambda b: (-b[0], -b[1].timestamp(), b[2]))
    head = ['Player', 'Pos', 'Team', 'Designation', 'Leagues', 'Dropped in']
    return out + table(head, [b[3] for b in body]) + ['']


def added_section(leagues):
    # The section is the market's read, so it counts the other managers only: the user
    # stashing one player in every league he plays is his own move, not the room's.
    out = ['## Added in 2+ leagues', '']
    players = collections.OrderedDict()
    for lg in leagues:
        for r in lg['win']:
            if r['move'] == 'ADD' and r['manager'] != lg['you']:
                players.setdefault(r['player'], []).append(r)
    body = []
    for name, rs in players.items():
        slugs = {r['slug'] for r in rs}
        if len(slugs) < 2:
            continue
        newest = max(rs, key=lambda r: r['when'])
        entries = [f'{r["slug"]} {r["day"]} {r["manager"]} {r["src"]}'
                   for r in sorted(rs, key=lambda r: (r['when'], r['slug']))]
        body.append((len(slugs), newest['when'], name,
                     [name, newest['pos'], newest['team'], '; '.join(entries)]))
    if not body:
        return out + ['No player was added in more than one league by a manager other '
                      'than the user in the window.', '']
    body.sort(key=lambda b: (-b[0], -b[1].timestamp(), b[2]))
    return out + table(['Player', 'Pos', 'Team', 'Leagues'], [b[3] for b in body]) + ['']


def yours_section(leagues):
    out = ['## Yours', '']
    any_rows = False
    for lg in leagues:
        mine = [r for r in lg['win']
                if r['manager'] == lg['you'] and r['move'] in ('ADD', 'DROP')]
        if not mine:
            continue
        any_rows = True
        out += [f'### {lg["slug"]}', '']
        body = [[str(r['day']), r['move'], r['player'], r['pos'], r['team'],
                 r['desig'], r['src']]
                for r in sorted(mine, key=lambda r: (r['when'], r['player']), reverse=True)]
        out += table(['Date', 'Movement', 'Player', 'Pos', 'Team', 'Designation', 'Source'],
                     body) + ['']
    if not any_rows:
        out += ['No rows in the window.', '']
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--since')
    ap.add_argument('--league')
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        raise SystemExit(f'no folder {a.dir}')
    leagues = read_leagues(a.dir)
    if a.league:
        keep = [lg for lg in leagues if lg['slug'] == a.league]
        if not keep:
            raise SystemExit(f'--league {a.league} is not in leagues.md; it holds: '
                             + ', '.join(lg['slug'] for lg in leagues))
        leagues = keep
    every = []
    for lg in leagues:
        lg['all'] = read_moves(a.dir, lg)
        every.extend(lg['all'])
    since = None
    if a.since:
        if not DAY.match(a.since):
            raise SystemExit('--since must be YYYY-MM-DD')
        try:
            since = datetime.datetime.strptime(a.since, '%Y-%m-%d').date()
        except ValueError:
            raise SystemExit(f'--since "{a.since}" is not a real date')
    elif every:
        since = max(r['when'] for r in every).date() - datetime.timedelta(days=7)
    for lg in leagues:
        lg['win'] = [r for r in lg['all'] if since is not None and r['day'] >= since]
    out = (managers_section(leagues) + dropped_section(leagues)
           + added_section(leagues) + yours_section(leagues))
    print('\n'.join(out).rstrip())


if __name__ == '__main__':
    main()
