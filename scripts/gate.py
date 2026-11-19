#!/usr/bin/env python3
"""Fantasy pre-delivery gate (references/gate.md).

A fantasy call reaches the user only as a block printed by `render`, which refuses to print when the
data is incomplete, a starting slot is unfilled, a hold is dropped, the flex breaks lock order, a
pick loses most signals to an alternative without a stated reason, or a player has no sourced
role card. The Stop hook (`hook`) blocks any chat message that carries a call line outside a
valid stamped block.

  gate.py open   WEEK [DATE]       start a pass: passes/DATE/ (manifest open)
  gate.py ingest [DATE]            copy Chrome localStorage keys gate_DATE_* (Yahoo + DS) into the pass
  gate.py check  [DATE]            completeness -> coverage.json; exit 1 on any FAIL
  gate.py board  LEAGUE [DATE]     lineup holes + multi-signal candidate board per position
  gate.py render LEAGUE [NAME] [DATE]  validate passes/DATE/calls/NAME.json (default LEAGUE); print the stamped block
  gate.py watch  [DATE]            watch list: waiver arrivals worth a claim-or-wait call, conditions, pending claims -> watch.md
  gate.py trades LEAGUE [N] [DATE] trade potentials with every rival, both sides and their needs (top N, default 8); leads, not calls
  gate.py close  [DATE]
  gate.py hook                     Stop hook (hook JSON on stdin)
DATE defaults to today (local time, or the gate home's config.json "tz"). Week comes from the manifest.
"""
import hashlib, json, os, re, subprocess, sys, textwrap, time, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
GHOME = os.environ.get('FANTASY_GATE_HOME') or os.path.join(os.path.expanduser('~'), '.fantasy-gate')  # the user's private gate home
def _gconf():
    try:
        return json.load(open(os.path.join(GHOME, 'config.json')))
    except (OSError, ValueError):
        return {}
PASSES = os.environ.get('GATE_PASSES') or _gconf().get('passes') or os.path.join(GHOME, 'passes')
READER = _gconf().get('reader')  # command: READER PREFIX OUTDIR ORIGIN
YAHOO = 'https://football.fantasysports.yahoo.com'
DSORIG = 'https://www.draftsharks.com'
TEAMFIX = {'JAC': 'JAX', 'LVR': 'LV', 'WSH': 'WAS', 'LA': 'LAR'}
ALIAS = {}
try:
    ALIAS.update(json.load(open(os.path.join(GHOME, 'aliases.json'))))
except (OSError, ValueError):
    pass
PLAYABLE_TAGS = {'', 'Q', 'P', 'DTD'}   # every other Yahoo status (O, D, IR, IR-R, PUP-P, NFI-R, SUSP, NA, ...) means not playing


def out_tag(t):
    return (t or '') not in PLAYABLE_TAGS
ELIG = {'QB': {'QB'}, 'RB': {'RB'}, 'WR': {'WR'}, 'TE': {'TE'}, 'W/R/T': {'RB', 'WR', 'TE'}, 'Q/W/R/T': {'QB', 'RB', 'WR', 'TE'}, 'K': {'K'}, 'DEF': {'DEF'}}
FLEX = {'W/R/T', 'Q/W/R/T'}
WEEK_SIG = ['y_wk', 'ds_wk', 'l4g', 'szn_g']
ROS_SIG = ['y_ros', 'ds_ros']
SIGNAME = {'y_wk': 'Yahoo wk', 'ds_wk': 'DS wk', 'l4g': 'last-4/g', 'szn_g': 'season/g', 'y_ros': 'Yahoo ROS', 'ds_ros': 'DS ROS'}
SHORT = {'y_wk': 'Yahoo', 'ds_wk': 'DS', 'l4g': 'last-4', 'szn_g': 'season', 'y_ros': 'Yahoo ROS', 'ds_ros': 'DS ROS'}
MAX_AGE_H = 12
# a DEF is named by nickname or city depending on the view: both resolve to def-<code>
NFL = {}  # team code -> 'Nickname City', from the gate home's teams.json
try:
    NFL.update(json.load(open(os.path.join(GHOME, 'teams.json'))))
except (OSError, ValueError):
    pass


def def_key(name):
    n = name.strip().lower()
    for code, words in NFL.items():
        nick, city = words.split(' ', 1)
        if n in (nick.lower(), city.lower(), code.lower(), (city + ' ' + nick).lower()):
            return 'def-' + code
    return None


def today():
    tz = _gconf().get('tz')
    if tz:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo(tz)).strftime('%Y-%m-%d')
    return datetime.datetime.now().strftime('%Y-%m-%d')


def die(msg, code=1):
    print('GATE FAIL: ' + msg, file=sys.stderr)
    sys.exit(code)


def jload(p, default=None):
    try:
        return json.load(open(p))
    except FileNotFoundError:
        if default is not None:
            return default
        raise


def cfg():
    return jload(os.path.join(GHOME, 'leagues.json'))['leagues']


def pdir(date):
    return os.path.join(PASSES, date)


def key(name):
    n = re.sub(r'\b(Jr|Sr|II|III|IV|V)\b\.?', '', name)
    k = re.sub(r'[^a-z]', '', n.lower())
    return ALIAS.get(k, k)


def surname(name):
    """last name without Jr./Sr./II/III, as a key ('First Last Jr.' -> 'last')."""
    toks = [t for t in re.sub(r'\b(Jr|Sr|II|III|IV|V)\b\.?', '', name).split() if t]
    return key(toks[-1]) if toks else ''


def num(s):
    try:
        return float(str(s).replace('%', '').replace(',', '').strip())
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- parsing (Yahoo)


def yrow(line):
    parts = [p.strip() for p in line.split(' | ')]
    m = re.match(r'(.*?) \{(.*)\}$', parts[1]) if len(parts) > 1 else None
    if not m:
        return None
    d = {'slot': parts[0].replace('slot:', ''), 'name': m.group(1).strip(), 'info': m.group(2).strip()}
    mm = re.match(r'(?:([A-Z][A-Z0-9-]*) )?(\w+) - ([A-Z,]+)\b ?(.*)', d['info'])
    if mm:
        d['tag'], d['team'], d['pos_all'], d['kick'] = mm.group(1) or '', mm.group(2).upper(), mm.group(3).split(','), mm.group(4)
    else:
        d['tag'], d['team'], d['pos_all'], d['kick'] = '', '', [''], d['info']
    d['team'] = TEAMFIX.get(d['team'], d['team'])
    d['pos'] = d['pos_all'][0]
    for p in parts[2:]:
        if ':' in p:
            a, b = p.split(':', 1)
            d[a.strip()] = b.strip()
    d['key'] = ('def-' + d['team']) if d['pos'] == 'DEF' else key(d['name'])
    return d


def sections(text):
    sec, cur = {}, 'HEAD'
    for l in text.split('\n'):
        if l.startswith('## '):
            # rival labels carry team names that may contain " (", so keep them whole
            cur = l[3:].strip() if l.startswith('## RIVAL ') else l[3:].split(' (')[0].strip()
            sec.setdefault(cur, [])
            continue
        sec.setdefault(cur, []).append(l)
    return sec


def kick_order(kick):
    """'Thu 5:15 pm @ Hou' -> sortable minutes from Wednesday 00:00; None if bye/unknown."""
    m = re.match(r'(Wed|Thu|Fri|Sat|Sun|Mon|Tue)\s+(\d+):(\d+)\s*(am|pm)', kick or '')
    if not m:
        return None
    day = ['Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue'].index(m.group(1))
    h = int(m.group(2)) % 12 + (12 if m.group(4) == 'pm' else 0)
    return day * 1440 + h * 60 + int(m.group(3))


class League:
    def __init__(self, L, date):
        self.L, self.date = L, date
        self.c = cfg()[L]
        man = jload(os.path.join(pdir(date), 'manifest.json'))
        self.week = man['week']
        yp = os.path.join(pdir(date), 'data', f'gate_{date}_{L}.txt')
        dp = os.path.join(pdir(date), 'data', f'gate_{date}_ds_{L}.txt')
        self.ytext = open(yp).read()
        self.dtext = open(dp).read()
        self.s = sections(self.ytext)
        W = self.week
        self.lineup = []          # current week view rows (with Empty)
        for l in self.s.get(f'ROSTER week-{W} projection view', []):
            if not l.startswith('slot:'):
                continue
            if '(Empty)' in l:
                self.lineup.append({'slot': l.split(' | ')[0][5:], 'name': '(Empty)', 'key': None, 'pos': '', 'pos_all': [], 'tag': '', 'kick': ''})
            else:
                d = yrow(l)
                if d:
                    self.lineup.append(d)
        self.R = {}               # rostered players by key
        for d in self.lineup:
            if d.get('key'):
                r = dict(d)
                r['y_wk'] = num(d.get('Fan Pts'))
                self.R[d['key']] = r
        for lab, fld in ((f'ROSTER ROS projection', 'y_ros'), ('ROSTER SEASON 2026 actual', 'szn'), ('ROSTER LAST 4 WEEKS actual total', 'l4')):
            for l in self.s.get(lab, []):
                d = yrow(l) if l.startswith('slot:') else None
                if d and d['key'] in self.R:
                    self.R[d['key']][fld] = num(d.get('Fan Pts'))
        self.P = {}               # pool players by key
        for lab, rows in self.s.items():
            if not lab.startswith('POOL'):
                continue
            stat = lab.split()[-1]
            for l in rows:
                d = yrow(l) if l.startswith('slot:') else None
                if not d:
                    continue
                if lab.startswith('POOL ALL'):
                    continue
                r = self.P.setdefault(d['key'], dict(d))
                v = num(d.get('Fan Pts'))
                if stat == 'wkproj':
                    r['y_wk'] = v
                elif stat == 'ROSproj':
                    r['y_ros'] = v
                elif stat == 'season2026':
                    r['szn'], r['szn_gp'] = v, num(d.get('GP*') or d.get('GP'))
                elif stat == 'last4wk':
                    r['l4'], r['l4_gp'] = v, num(d.get('GP*') or d.get('GP'))
                r['status'] = d.get('Roster Status', r.get('status'))
        # games played for rostered players from the all-player pools
        self.GP = {}
        gp_file = os.path.join(pdir(date), 'data', f'gate_{date}_GP.txt')   # games played is the same in every league
        gp_secs = sections(open(gp_file).read()) if os.path.exists(gp_file) else {}
        for lab, rows in list(self.s.items()) + [('POOL ' + k, v) for k, v in gp_secs.items()]:
            if not (lab.startswith('POOL ALL') or lab.startswith('POOL GP ALL')):
                continue
            which = 'l4_gp' if 'last4' in lab else 'szn_gp'
            for l in rows:
                d = yrow(l) if l.startswith('slot:') else None
                if d:
                    self.GP.setdefault(d['key'], {})[which] = num(d.get('GP*') or d.get('GP'))
        for k, r in self.R.items():
            g = self.GP.get(k, {})
            r['l4_gp'], r['szn_gp'] = g.get('l4_gp'), g.get('szn_gp')
        self.DS = self._ds()
        self.stand = {}           # team id -> rank, record, points for (from the league page)
        for l in self.s.get('STANDINGS', []):
            q = l.split('|')
            m = re.match(r'(\d+)-(\d+)-(\d+)', q[4]) if len(q) >= 7 and q[0] == 'STAND' else None
            rk = re.sub(r'\D', '', q[1]) if m else ''
            if m and rk:
                self.stand[q[2]] = {'rank': int(rk), 'name': q[3], 'w': int(m.group(1)), 'l': int(m.group(2)), 't': int(m.group(3)), 'pf': num(q[5])}

    def _ds(self):
        out, sec = {}, None
        dre = re.compile(r'^(.*?) ([A-Z]{2,3}) (QB|RB|WR|TE|K|DEF)\d*\b')
        for l in self.dtext.split('\n'):
            if l.startswith('## '):
                sec = l[3:]
                continue
            c = [x.strip() for x in l.split(' | ')]
            if sec and sec.startswith('FAF') and len(c) == 15 and c[1].isdigit():
                m = dre.match(c[2])
                if m:
                    t = TEAMFIX.get(m.group(2), m.group(2))
                    k = ('def-' + t) if m.group(3) == 'DEF' else key(m.group(1))
                    out.setdefault(k, {}).update({'ds_wk': num(c[4]), 'ds_ceil': num(c[5]), 'ds_ros': num(c[11]), 'ds_val': num(c[14]), 'ds_tag': c[0], 'ds_name': m.group(1), 'ds_team': t})  # keep ds_dash from the dashboard
            elif sec and sec.startswith('dash table') and len(c) >= 10 and re.match(r'^(QB|RB|WR|TE|R W T|R W T Q|Q W R T|K|DEF|BN|IR)$', c[0]):
                m = dre.match(c[1])
                if m:
                    t = TEAMFIX.get(m.group(2), m.group(2))
                    k = ('def-' + t) if m.group(3) == 'DEF' else key(m.group(1))
                    out.setdefault(k, {}).update({'ds_wk': num(c[-1]), 'ds_ceil': num(c[7]), 'ds_ros': num(c[8]), 'ds_name': m.group(1), 'ds_team': t, 'ds_dash': True})
        return out

    def ds_for(self, k, name='', team='', pos=''):
        if k in self.DS:
            return self.DS[k]
        last = surname(name) if name else ''
        hits = [v for kk, v in self.DS.items() if kk.endswith(last) and v.get('ds_team') == team] if last else []
        return hits[0] if len(hits) == 1 else {}

    def games(self, r, kind):
        """games played: exact GP from Yahoo when present, else None (missing, never guessed)."""
        return r.get(kind)

    def signals(self, r):
        d = self.ds_for(r['key'], r['name'], r.get('team', ''), r.get('pos', ''))
        l4g = r.get('l4') / r['l4_gp'] if r.get('l4') is not None and r.get('l4_gp') else None
        sg = r.get('szn') / r['szn_gp'] if r.get('szn') is not None and r.get('szn_gp') else None
        return {'y_wk': r.get('y_wk'), 'ds_wk': d.get('ds_wk'), 'l4g': l4g, 'szn_g': sg, 'y_ros': r.get('y_ros'), 'ds_ros': d.get('ds_ros'), 'ds_ceil': d.get('ds_ceil')}

    def find(self, name):
        dk = def_key(name)
        if dk:
            for src, D in (('R', self.R), ('P', self.P)):
                if dk in D:
                    return src, D[dk]
        k = key(name)
        if k in self.R:
            return 'R', self.R[k]
        if k in self.P:
            return 'P', self.P[k]
        # DEF by nickname ("Chargers") -> pool or roster entry with that name
        for src, D in (('R', self.R), ('P', self.P)):
            for r in D.values():
                if r['name'].lower() == name.lower():
                    return src, r
        return None, None


def vote(sa, sb, sigs):
    """a vs b over sigs present for both: (wins_a, wins_b, shared, detail)"""
    wa = wb = n = 0
    det = []
    for s in sigs:
        x, y = sa.get(s), sb.get(s)
        if x is None or y is None:
            continue
        n += 1
        if x > y + 1e-9:
            wa += 1; det.append('+' + SIGNAME[s])
        elif y > x + 1e-9:
            wb += 1; det.append('-' + SIGNAME[s])
    return wa, wb, n, det


def fmt(v, g=False):
    return '?' if v is None else (f'{v:.1f}' if g else f'{v:.2f}' if v < 100 else f'{v:.1f}')


# ---------------------------------------------------------------- commands
def cmd_open(date, week):
    p = pdir(date)
    for sub in ('data', 'calls', 'renders'):
        os.makedirs(os.path.join(p, sub), exist_ok=True)
    man = {'date': date, 'week': int(week), 'open': True, 'opened': int(time.time())}
    json.dump(man, open(os.path.join(p, 'manifest.json'), 'w'), indent=1)
    if not os.path.exists(os.path.join(p, 'cards.json')):
        json.dump({'_note': 'one role card per player for this pass: {"Name": {"asof": "YYYY-MM-DD", "role": "...", "sources": ["what was READ, dated"]}}'}, open(os.path.join(p, 'cards.json'), 'w'), indent=1)
    print(f'pass {date} week {week} open: {p}')


def cmd_ingest(date):
    out = os.path.join(pdir(date), 'data')
    got = []
    for origin in (YAHOO, DSORIG):
        if not READER:
            die('ingest: no "reader" command in the gate home config.json')
        r = subprocess.run(READER.split() + [f'gate_{date}_', out, origin], capture_output=True, text=True)
        got += [l for l in r.stdout.split('\n') if '->' in l]
    want = [f'gate_{date}_{L}' for L in cfg()] + [f'gate_{date}_ds_{L}' for L in cfg()] + [f'gate_{date}_GP']
    have = set(f[:-4] for f in os.listdir(out) if f.endswith('.txt'))
    missing = [w for w in want if w not in have]
    print('\n'.join(got))
    if missing:
        die('ingest: missing keys (not in Chrome storage yet, or the collector did not save): ' + ', '.join(missing))
    print(f'ingest OK: {len(want)} files')


def cmd_check(date):
    p = pdir(date)
    man = jload(os.path.join(p, 'manifest.json'))
    res, fails = {}, []
    gpf = os.path.join(p, 'data', f'gate_{date}_GP.txt')
    gp_fail = []
    if not os.path.exists(gpf):
        gp_fail.append('games-played file missing (run gate-gp-collect.js)')
    else:
        gpt = open(gpf).read()
        for x in [l.split('|') for l in gpt.split('\n') if l.startswith('COV|')] or [['', '', 'GP', '', '', 'FAIL', 'no coverage lines']]:
            if x[5] != 'OK':
                gp_fail.append(f'games played: {x[2]} expected {x[3]} got {x[4]} {x[6]}'.strip())
    for L, c in cfg().items():
        lr = {'checks': 0, 'fail': []}
        for kind, fn in (('yahoo', f'gate_{date}_{L}.txt'), ('ds', f'gate_{date}_ds_{L}.txt')):
            fp = os.path.join(p, 'data', fn)
            if not os.path.exists(fp):
                lr['fail'].append(f'{kind}: file missing'); continue
            t = open(fp).read()
            cov = [l.split('|') for l in t.split('\n') if l.startswith('COV|')]
            if not cov:
                lr['fail'].append(f'{kind}: no coverage lines (collector did not finish)')
            for x in cov:
                lr['checks'] += 1
                if x[5] != 'OK':
                    lr['fail'].append(f'{kind}: {x[2]} expected {x[3]} got {x[4]} {x[6]}'.strip())
            # recount every section from the data itself, whatever the collector's own COV lines said
            secs = sections(t)
            for lab, rows in secs.items():
                n_rows = sum(1 for l in rows if ' {' in l or re.match(r'^\S*\s*\|\s*\d+\s*\|', l))
                floor = None
                if kind == 'yahoo' and (lab.startswith('POOL') or lab.startswith('RIVAL') or lab.startswith('ROSTER')):
                    floor = 10 if lab.startswith('POOL') else 12
                elif kind == 'ds' and lab.startswith('FAF '):
                    floor = {'QB': 10, 'RB': 40, 'WR': 60, 'TE': 25, 'K': 10, 'DEF': 10}.get(lab.split()[-1], 10)
                if floor is not None and n_rows < floor:
                    lr['fail'].append(f'{kind}: section "{lab[:50]}" has {n_rows} rows (< {floor})')
            if kind == 'yahoo' and 'STANDINGS' in secs:
                good = [l for l in secs['STANDINGS'] if re.match(r'^STAND\|\D*\d+\|\d+\|[^|]+\|\d+-\d+-\d+\|', l)]
                if len(good) != c['teams']:
                    lr['fail'].append(f"yahoo: standings parse {len(good)} of {c['teams']} teams (rank, team id, name, W-L-T)")
            if kind == 'ds' and not re.search(r'^SYNC: Synced:\s*(\d+ seconds?|a minute|[1-5]?\d minutes?(?: \d+ seconds?)?) ago', t, re.M):
                lr['fail'].append('ds: sync stamp missing or older than 60 minutes')
            if kind == 'yahoo':
                tl = [l for l in t.split('\n') if l.startswith('TEAMS: ')]
                n = len(tl[0][7:].split(' || ')) if tl and tl[0][7:] else 0
                rivals = len(re.findall(r'^## RIVAL \d+ .* :: ROS$', t, re.M))
                if n != c['teams']:
                    lr['fail'].append(f'yahoo: team list {n} != league size {c["teams"]}')
                if rivals != c['teams'] - 1:
                    lr['fail'].append(f'yahoo: rival rosters {rivals} != {c["teams"] - 1}')
                lr['teams'], lr['rivals'] = n, rivals
        lr['fail'] += gp_fail
        if not lr['fail']:
            try:
                lg = League(L, date)
                # every rostered skill player with real points has games played (or his per-game signals go missing)
                nogp = [r['name'] for r in lg.R.values() if r.get('pos') in ('QB', 'RB', 'WR', 'TE') and (r.get('szn') or 0) > 15 and not r.get('szn_gp')]
                if nogp:
                    lr['fail'].append('games played missing for rostered ' + ', '.join(nogp[:6]))
                # same for the last 4 weeks: points scored there with no games played would print last-4/g as ?
                nogp4 = [r['name'] for r in lg.R.values() if r.get('pos') in ('QB', 'RB', 'WR', 'TE') and (r.get('l4') or 0) > 0 and not r.get('l4_gp')]
                if nogp4:
                    lr['fail'].append('last-4 games played missing for rostered ' + ', '.join(nogp4[:6]))
                ydash = set(k for k, r in lg.R.items() if r.get('slot') != 'IR')
                dsdash = set(k for k, v in lg.DS.items() if v.get('ds_dash'))
                miss = [lg.R[k]['name'] for k in ydash if k not in dsdash and not lg.ds_for(k, lg.R[k]['name'], lg.R[k].get('team', '')).get('ds_dash')]
                if miss:
                    lr['fail'].append('ds dashboard does not match the Yahoo roster (sync?): missing ' + ', '.join(miss[:6]))
            except Exception as e:
                lr['fail'].append(f'parse error: {e}')
        lr['status'] = 'PASS' if not lr['fail'] else 'FAIL'
        res[L] = lr
        if lr['fail']:
            fails.append(L)
    cov = {'date': date, 'week': man['week'], 'checked': time.time() + 1, 'leagues': res}   # +1s: files written in the same second are not 'newer'
    json.dump(cov, open(os.path.join(p, 'coverage.json'), 'w'), indent=1)
    for L, r in res.items():
        print(f"{L:<8} {r['status']}  checks {r['checks']}  teams {r.get('teams', '?')} rivals {r.get('rivals', '?')}" + ('' if not r['fail'] else '\n   ' + '\n   '.join(r['fail'][:8])))
    if fails:
        die('coverage FAIL in ' + ', '.join(fails) + ': re-pull those pages, or deliver as INCOMPLETE naming them')
    print('coverage PASS, all 8 leagues')


def candidates(lg, positions, k=5):
    """bench + union of the top k free agents/waiver players by EVERY signal (no single sort decides)."""
    out = {}
    for key_, r in lg.R.items():
        if r.get('slot') in ('BN',) and set(r.get('pos_all', [])) & positions:
            out[key_] = ('bench', r)
    pool = [(kk, r) for kk, r in lg.P.items() if set(r.get('pos_all', [])) & positions]
    for s in WEEK_SIG + ROS_SIG:
        ranked = sorted(pool, key=lambda x: -(lg.signals(x[1]).get(s) or -1e9))
        for kk, r in ranked[:k]:
            if lg.signals(r).get(s) is not None:
                out.setdefault(kk, ((r.get('status') or 'FA'), r))
    return out


def board_lines(lg, slot_or_pos):
    positions = ELIG.get(slot_or_pos, {slot_or_pos})
    cand = candidates(lg, positions)
    rows = []
    for kk, (src, r) in cand.items():
        s = lg.signals(r)
        rows.append((r, src, s))
    out = []
    ranks = {}
    for sg in WEEK_SIG + ROS_SIG:
        vals = sorted([x[2].get(sg) for x in rows if x[2].get(sg) is not None], reverse=True)
        ranks[sg] = vals
    def rk(sg, v):
        return '' if v is None else f"#{ranks[sg].index(v) + 1}"
    rows.sort(key=lambda x: -sum(1 for sg in WEEK_SIG if x[2].get(sg) is not None and ranks[sg] and x[2][sg] >= ranks[sg][min(2, len(ranks[sg]) - 1)]))
    out.append(f"  {'player':<24}{'src':<11}" + ''.join(f"{SIGNAME[s]:>13}" for s in WEEK_SIG + ROS_SIG) + '  ceil  tag kick')
    for r, src, s in rows:
        out.append(f"  {r['name'][:23]:<24}{src[:10]:<11}" + ''.join(f"{fmt(s.get(sg)) + rk(sg, s.get(sg)):>13}" for sg in WEEK_SIG + ROS_SIG) + f"  {fmt(s.get('ds_ceil'))}  {r.get('tag') or '-'} {(r.get('kick') or '')[:16]}")
    return out


def cmd_board(L, date):
    lg = League(L, date)
    print(f'== {L} week {lg.week} board ({date}). Signals: ' + ', '.join(SIGNAME[s] for s in WEEK_SIG + ROS_SIG) + '. ? = missing (never 0). #n = rank among the candidates shown.')
    holes = []
    for d in lg.lineup:
        if d['slot'] in ('BN', 'IR'):
            continue
        bad = d['name'] == '(Empty)' or 'Bye' in (d.get('kick') or '') or out_tag(d.get('tag')) or d.get('tag') == 'Q'
        r = lg.R.get(d.get('key'), {})
        s = lg.signals(r) if r else {}
        print(f"{d['slot']:<8}{d['name'][:24]:<25}{d.get('tag') or '-':<5}{(d.get('kick') or '')[:22]:<23}" + ('' if not r else ' '.join(f"{SIGNAME[x]} {fmt(s.get(x))}" for x in WEEK_SIG)) + ('   <== ' + ('EMPTY' if d['name'] == '(Empty)' else 'BYE' if 'Bye' in d.get('kick', '') else d.get('tag')) if bad else ''))
        if bad:
            holes.append(d['slot'])
    for d in lg.lineup:
        if d['slot'] == 'IR' and d.get('key') and not d.get('tag'):
            print(f"!! IR slot holds {d['name']} with no IR-eligible tag: blocks every add and trade until moved")
    print('HOLES:', holes or 'none')
    for slot in sorted(set(holes), key=lambda x: list(ELIG).index(x)):
        print(f'-- {slot} candidates (bench + top 5 free agents on each signal):')
        print('\n'.join(board_lines(lg, slot)))


def team_players(lg, which):
    """{key: {name,pos,ros,n4,tag}} for 'me' or a rival id."""
    out = {}
    if which == 'me':
        labs = (('ROSTER ROS projection', 'ros'), ('ROSTER NEXT 4 WEEKS projection', 'n4'))
    else:
        labs = ((f'RIVAL {which[0]} :: {which[1]} :: ROS', 'ros'), (f'RIVAL {which[0]} :: {which[1]} :: NEXT4', 'n4'))
    for lab, fld in labs:
        for l in lg.s.get(lab, []):
            d = yrow(l) if ' | ' in l else None
            if not d and ' | ' in l:  # rival rows have no 'slot:' prefix handling difference
                continue
            if d and d.get('pos') in ('QB', 'RB', 'WR', 'TE'):
                r = out.setdefault(d['key'], {'name': d['name'], 'pos': d['pos'], 'pos_all': d['pos_all'], 'tag': d.get('tag', ''), 'slot': d['slot'], 'team': d.get('team', ''), 'bye': num(d.get('Bye'))})
                r[fld] = num(d.get('Fan Pts')) or 0.0
    return out


LAST_WEEK = 17      # the last fantasy week: trade math sums through it
NFL_LAST = 18       # the host's rest-of-season projection runs through the last NFL week, so rates divide by games through it


def roster_cap(lg):
    """(active roster limit, source): leagues.json "roster" when set, else the size most rival rosters sit at.
    Displayed rows are not the limit: an empty starting slot shows as a row on a full roster."""
    if lg.c.get('roster'):
        return int(lg.c['roster']), 'leagues.json'
    counts = []
    for pid in rivals(lg):
        n = 0
        for l in lg.s.get(f'RIVAL {pid[0]} :: {pid[1]} :: ROS', []):
            d = yrow(l) if ' | ' in l else None
            if d and d.get('slot') != 'IR':
                n += 1
        counts.append(n)
    if counts:
        return max(set(counts), key=counts.count), 'most rival rosters'
    return len([d for d in lg.lineup if d['slot'] != 'IR']), 'roster rows'


def _rates(p, week):
    """(near, far) points a game: the next-4 projection over the next-4 games and the rest over the
    games after, so a bye week scores 0 and the bench fills it instead of hiding inside a season total."""
    bye = p.get('bye')
    near_w = [w for w in range(week, min(week + 3, LAST_WEEK) + 1) if w != bye]
    far_w = [w for w in range(week + 4, NFL_LAST + 1) if w != bye]
    ros, n4 = p.get('ros') or 0.0, p.get('n4')
    if n4 is None or not near_w:
        r = ros / max(1, len(near_w) + len(far_w))
        return r, r
    near = n4 / len(near_w)
    far = (ros - n4) / len(far_w) if far_w else near
    return near, max(far, 0.0)


def weekly_total(players, slots, week, w_end, w_start=None):
    """sum of the best lineup for each week from `w_start` (default: this week) to `w_end`, each player at his rate
    (as of `week`) except in his bye week."""
    rates = {k: _rates(p, week) for k, p in players.items()}
    tot, cache = 0.0, {}
    for w in range(w_start or week, min(w_end, LAST_WEEK) + 1):
        near = w < week + 4
        off = tuple(sorted(k for k, p in players.items() if p.get('bye') == w))
        ck = (near, off)
        if ck not in cache:
            wk = {k: dict(p, wk=(0.0 if k in off else rates[k][0 if near else 1])) for k, p in players.items()}
            cache[ck] = best_lineup(wk, slots, 'wk')
        tot += cache[ck]
    return tot


def horizons(lg):
    """(field, first week, last week, weeks): this week, next 4, the playoff weeks (when leagues.json names them and
    they are still ahead), rest of season."""
    W = lg.week
    po = (lg.c.get('playoffs') or {}).get('weeks')
    out = [('wk', W, W, 1)]
    if po and po[0] - 1 >= W:
        out.append(('rs', W, po[0] - 1, po[0] - W))          # the rest of the regular season: what the race is decided on
    else:
        out.append(('n4', W, W + 3, 4))
    if po and po[1] >= W:
        a = max(po[0], W)
        out.append(('po', a, po[1], po[1] - a + 1))
    out.append(('ros', W, LAST_WEEK, max(1, LAST_WEEK - W + 1)))
    return out


def _ord(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def race(lg, tid):
    """-> ('in' | 'chasing' | 'out' | None, plain text): a team's place in the playoff race from the standings and
    leagues.json "playoffs" (teams, weeks, consolation). Wins only; the host's tiebreaks are not modeled."""
    s = lg.stand.get(str(tid))
    if not s:
        return None, 'standing not in this pull'
    rec = f"{s['w']}-{s['l']}" + (f"-{s['t']}" if s['t'] else '')
    txt = f"{rec}, {_ord(s['rank'])} of {len(lg.stand)}"
    po = lg.c.get('playoffs') or {}
    if not (po.get('teams') and po.get('weeks')):
        return None, txt
    P, reg_end = po['teams'], po['weeks'][0] - 1
    left = max(0, reg_end - lg.week + 1)
    ranked = sorted(lg.stand.values(), key=lambda x: x['rank'])
    line = ranked[P - 1]['w'] if len(ranked) >= P else None
    if s['rank'] <= P:
        out_w = ranked[P]['w'] if len(ranked) > P else None
        cush = (s['w'] - out_w) if out_w is not None else None
        cls, st = 'in', 'in a playoff spot' + ('' if cush is None else f", {cush} win{'s' if cush != 1 else ''} clear of the first team out" if cush > 0 else ', level on wins with the first team out') + f", {left} games left"
    elif line is not None and s['w'] + left >= line:
        gap = line - s['w']
        cls, st = 'chasing', (f"{gap} win{'s' if gap != 1 else ''} behind the last playoff spot" if gap > 0 else 'level on wins with the last playoff spot') + f", {left} games left" + ('; must win out' if gap > 0 and gap >= left else '')
    else:
        cls, st = 'out', 'out of the playoff race'
    cons = po.get('consolation')
    if cons and s['rank'] > P:
        st += f"; consolation bracket is {_ord(cons[0])}-{_ord(cons[1])}"
    return cls, f"{txt} ({st}; playoffs weeks {po['weeks'][0]}-{po['weeks'][1]})"


def gains_text(g, side, lg):
    """'+1.0 this week, +0.4/wk until the playoffs (weeks 11-15), +2.0/wk playoff weeks 16-17, +1.0/wk rest of season'
    (next 4 instead of the weeks until the playoffs when the league's playoff format is not set)."""
    lab = {'wk': ' this week', 'n4': '/wk next 4', 'ros': '/wk rest of season'}
    parts = []
    for fld, a, b, n in horizons(lg):
        v = g.get(f'{side}_{fld}')
        if v is None:
            continue
        v = 0.0 if abs(v) < 0.05 else v
        parts.append(f"{v:+.1f}" + ({'po': f"/wk playoff weeks {a}-{b}", 'rs': f"/wk until the playoffs (weeks {a}-{b})"}.get(fld) or lab[fld]))
    return ', '.join(parts)


def trade_gains(lg, me, th, give, get, base=None):
    """per-week lineup gain for both sides on every horizon (this week, next 4, playoff weeks, rest of season), byes
    filled from the bench."""
    slots = lg.c['slots']
    me2 = {k: v for k, v in me.items() if k not in give}
    me2.update({k: th[k] for k in get})
    th2 = {k: v for k, v in th.items() if k not in get}
    th2.update({k: me[k] for k in give})
    W = lg.week
    g = {}
    for fld, a, end, n in horizons(lg):
        bm = base[('me', fld)] if base else weekly_total(me, slots, W, end, a)
        bt = base[('th', fld)] if base else weekly_total(th, slots, W, end, a)
        g['me_' + fld] = (weekly_total(me2, slots, W, end, a) - bm) / n
        g['th_' + fld] = (weekly_total(th2, slots, W, end, a) - bt) / n
    return g


def pending_claim(lg):
    """the user's first pending waiver claim when it is certain: the user holds waiver priority 1, so even a
    contested claim goes to them. -> (add_name, drop_name, date label) or None."""
    head = next((l for l in lg.ytext.split('\n') if l.startswith('HEADER:')), '')
    pend = next((l for l in lg.ytext.split('\n') if l.startswith('PENDING:')), '')
    if not re.search(r'Waiver Priority: 1st\b', head):
        return None
    m = re.search(r'Waiver 1 \(([^)]*)\): Add (.+?)(?:, Drop (.+?))?(?= View| Waiver \d| Week \d|$)', pend)
    return (m.group(2).strip(), (m.group(3) or '').strip(), m.group(1)) if m else None


def planned_me(lg):
    """the user's players for planning: the roster with a certain pending claim already applied."""
    me = team_players(lg, 'me')
    pc = pending_claim(lg)
    note = ''
    if pc:
        add, drop, when = pc
        src, r = lg.find(add)
        if r and src != 'R':
            if drop:
                me.pop(key(drop), None)
            me[r['key']] = {'name': r['name'], 'pos': r.get('pos'), 'pos_all': r.get('pos_all') or [r.get('pos')], 'tag': r.get('tag', ''),
                            'slot': 'BN', 'team': r.get('team', ''), 'bye': num(r.get('Bye')), 'ros': r.get('y_ros') or 0.0}
            note = f"counts the pending claim as landed (Add {add}" + (f", Drop {drop}" if drop else '') + f", {when}): you hold waiver priority 1"
    return me, note


def best_lineup(players, slots, fld):
    pool = sorted(players.items(), key=lambda x: -(x[1].get(fld) or 0))
    used, tot = set(), 0.0
    for s in slots:
        if s in ('K', 'DEF'):
            continue
        for k, d in pool:
            if k not in used and set(d.get('pos_all', [d['pos']])) & ELIG[s]:
                used.add(k); tot += d.get(fld) or 0; break
    return tot


def rivals(lg):
    out = []
    for lab in lg.s:
        m = re.match(r'RIVAL (\d+) :: (.*) :: ROS$', lab)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def hold_key(lg, h):
    """resolve a hold's player through the league's own rows, so 'Vikings' matches def-MIN."""
    src, r = lg.find(h['player'])
    return r['key'] if r else key(h['player'])



def per_game(p, week):
    """rest-of-season points a game: the host's projection over his games left through the last NFL week."""
    games = [w for w in range(week, NFL_LAST + 1) if w != p.get('bye')]
    return (p.get('ros') or 0.0) / max(1, len(games))


def slot_labels(slots):
    """starting slots as labels: RB1, RB2, WR1, WR2, TE, FLEX, SFLEX (kickers and defenses left out)."""
    out, seen = [], {}
    for s in slots:
        if s in ('K', 'DEF'):
            continue
        base = {'W/R/T': 'FLEX', 'Q/W/R/T': 'SFLEX'}.get(s, s)
        seen[base] = seen.get(base, 0) + 1
        out.append((s, base + (str(seen[base]) if slots.count(s) > 1 else '')))
    return out


def slot_assign(players, slots, week):
    """best lineup by rest-of-season points a game -> {label: (name, points a game)}."""
    pool = sorted(players.items(), key=lambda x: -per_game(x[1], week))
    used, out = set(), {}
    for s, lab in slot_labels(slots):
        pick = next(((k, d) for k, d in pool if k not in used and set(d.get('pos_all') or [d.get('pos')]) & ELIG[s]), None)
        if pick:
            used.add(pick[0])
            out[lab] = (pick[1]['name'] + (f" ({pick[1]['tag']})" if pick[1].get('tag') else ''), per_game(pick[1], week))
        else:
            out[lab] = ('(none)', 0.0)
    return out


def league_starters(lg):
    """every team's best lineup by slot -> {team id or 'me': {label: (name, points a game)}}."""
    teams = {'me': planned_me(lg)[0]}
    for pid in rivals(lg):
        teams[pid] = team_players(lg, pid)
    return {t: slot_assign(p, lg.c['slots'], lg.week) for t, p in teams.items()}


def slot_rank(starters, team, lab, value):
    """1 = the league's best starter at that slot, counting `value` for `team` against every other team."""
    others = [a[lab][1] for t, a in starters.items() if t != team and lab in a]
    return 1 + len([v for v in others if v > value]), len(others) + 1


def their_needs(lg, starters, pid, th2):
    """why the partner might want the deal: his weakest starting slots ranked against the league, and what the
    deal does to each slot it changes. Plain words, no cutoff."""
    before = starters[pid]
    after = slot_assign(th2, lg.c['slots'], lg.week)
    ranked = sorted(before, key=lambda lab: -slot_rank(starters, pid, lab, before[lab][1])[0])
    weak = []
    for lab in ranked[:2]:
        r, n = slot_rank(starters, pid, lab, before[lab][1])
        weak.append(f"{lab} {before[lab][0]} {before[lab][1]:.1f}/g ({r} of {n})")
    moves = []
    for lab in before:
        if after[lab][0] != before[lab][0]:
            r0, n = slot_rank(starters, pid, lab, before[lab][1])
            r1, _ = slot_rank(starters, pid, lab, after[lab][1])
            moves.append(f"{lab} {before[lab][0]} {before[lab][1]:.1f} -> {after[lab][0]} {after[lab][1]:.1f}/g ({r0} -> {r1} of {n})")
    return ('their weakest starters: ' + '; '.join(weak),
            'the deal for them: ' + ('; '.join(moves) if moves else 'no starter changes (it adds depth only)'))


def trade_check(lg, tr, cards, holds, over, hold_ov, errs):
    lines, flags = [], []
    partner = [r for r in rivals(lg) if tr.get('partner', '').lower() in r[1].lower()]
    if len(partner) != 1:
        errs.append(f"trade partner '{tr.get('partner')}' matches {len(partner)} teams in the pull ({', '.join(r[1] for r in rivals(lg))})")
        return lines
    pid = partner[0]
    me, plan_note = planned_me(lg)
    th = team_players(lg, pid)
    give = [key(n) for n in tr.get('give', [])]
    get = [key(n) for n in tr.get('get', [])]
    if not give or not get:
        errs.append('trade: give and get must each name at least one player'); return lines
    if len(set(give)) != len(give) or len(set(get)) != len(get):
        errs.append('trade: a player is named twice'); return lines
    for n, k in zip(tr.get('give', []), give):
        if k not in me:
            errs.append(f'trade give {n}: not on your roster')
        else:
            if out_tag(me[k].get('tag')) or me[k].get('tag') == 'Q':
                flags.append(f"you send {n} tagged {me[k]['tag']}: their manager sees that tag, so say it in the offer")
            for h in holds:
                if hold_key(lg, h) == k and h['kind'] in ('trade', 'both') and n not in hold_ov:
                    errs.append(f'trade give {n}: HOLD ("{h["quote"]}")')
    for n, k in zip(tr.get('get', []), get):
        if k not in th:
            errs.append(f'trade get {n}: not on {pid[1]}\'s roster')
    # drops that make room: each must be a rostered player who is not in the deal and not held
    drops = []
    for n in tr.get('drops', []):
        src, r = lg.find(n)
        if src != 'R':
            errs.append(f'trade drop {n}: not on your roster')
        elif r['key'] in give or r['key'] in [d['key'] for d in drops]:
            errs.append(f'trade drop {n}: already leaving in this trade (named in give, or twice in drops)')
        else:
            for h in holds:
                if hold_key(lg, h) == r['key'] and h['kind'] in ('drop', 'both') and n not in hold_ov:
                    errs.append(f'trade drop {n}: HOLD ("{h["quote"]}") - needs hold_override with the user\'s words')
            drops.append(r)
    nerr = len(errs)
    for n in tr.get('give', []) + tr.get('get', []):
        card_for(cards, n, lg.date, errs)
    if any(k not in me for k in give) or any(k not in th for k in get) or len(errs) > nerr:
        return lines
    # DS trade values (league-scored chart, read this pass) for every player in the deal
    dsv, tvc = tvc_values(lg)
    dval = lambda d: ds_value(dsv, d)
    vg = [dval(me[k]) for k in give]; vt = [dval(th[k]) for k in get]
    if None in vg or None in vt:
        errs.append(f'trade: DS trade value missing for ' + ', '.join([me[k]['name'] for k, v in zip(give, vg) if v is None] + [th[k]['name'] for k, v in zip(get, vt) if v is None]) + f' (read the DS Trade Value Chart for {lg.L} into {os.path.basename(tvc)})')
        return lines
    # roster room: more players in than out needs drops in the same calls file
    room = roster_cap(lg)[0] - len([d for d in lg.lineup if d['slot'] != 'IR' and d.get('key')])
    extra = len(get) - len(give) - room - len(drops)
    if extra > 0:
        errs.append(f'trade: you receive {len(get)} for {len(give)} with {room} open roster spots: name {extra} drop(s) in trade["drops"]')
    g = trade_gains(lg, me, th, give, get)
    if not (tr.get('partner_reason') or '').strip():
        errs.append(f"trade: say why {pid[1]} would say yes (their needs, what the deal fills for them) in partner_reason")
    th2 = {k: v for k, v in th.items() if k not in get}
    th2.update({k: me[k] for k in give})
    needs = their_needs(lg, league_starters(lg), pid, th2)
    lines.append(f"TRADE with {pid[1]} (rival roster read: {len(th)} players)")
    if plan_note:
        lines.append('  ' + plan_note)
    tag = lambda d: '%s (%s %s)' % (d['name'], d['team'], d['pos'])
    lines.append('  GIVE ' + ', '.join(tag(me[k]) for k in give) + '  /  GET ' + ', '.join(tag(th[k]) for k in get))
    if drops:
        lines.append('  DROP to make room: ' + ', '.join(tag(d) for d in drops))
    dv = sum(vg) - sum(vt)
    lines.append(f"  DS trade value (league-scored chart): you give {sum(vg)} ({' + '.join(str(v) for v in vg)}), get {sum(vt)} ({' + '.join(str(v) for v in vt)})"
                 + (f"; you pay {dv} more" if dv > 0 else f"; they pay {-dv} more" if dv < 0 else '; even'))
    def sbs(d, v):
        return f"{d['name']}{' (' + d['tag'] + ')' if d.get('tag') else ''}: DS {v}, Yahoo rest of season {d.get('ros') or 0:.0f}"
    lines.append('  side by side, you give: ' + '; '.join(sbs(me[k], v) for k, v in zip(give, vg)))
    lines.append('  side by side, you get:  ' + '; '.join(sbs(th[k], v) for k, v in zip(get, vt)))
    yg, yt = sum(me[k].get('ros') or 0 for k in give), sum(th[k].get('ros') or 0 for k in get)
    lines.append(f"  totals: DS {sum(vg)} given v {sum(vt)} received ({abs(dv)} = {100 * abs(dv) / max(1, sum(vg) + sum(vt)):.0f}% of the deal, "
                 + ('even' if dv == 0 else 'you pay more' if dv > 0 else 'they pay more') + f"); Yahoo rest of season {yg:.0f} given v {yt:.0f} received")
    lines.append(f"  you: {gains_text(g, 'me', lg)} (best lineup each week before vs after, Yahoo; byes filled from the bench)")
    lines.append(f"  {pid[1]}: {gains_text(g, 'th', lg)}")
    lines.append(f"  standings: you {race(lg, lg.c['team'])[1]}; {pid[1]} {race(lg, pid[0])[1]}")
    lines.append('  ' + needs[0])
    lines.append('  ' + needs[1])
    if tr.get('partner_reason'):
        lines.append(f"  why they would say yes: {tr['partner_reason']}")
    for f in flags:
        lines.append('  flag: ' + f)
    if over.get('trade'):
        lines.append(f"  note: {over['trade']}")
    byk = {key(k): v for k, v in cards.items() if isinstance(v, dict)}
    for n in tr.get('give', []) + tr.get('get', []):
        c = byk.get(key(n), {})
        lines.append(f"  {n} ({c.get('asof')}): {c.get('role')}  [read: {'; '.join(c.get('sources', []))}]")
    return lines


def card_for(cards, nm, date, errs):
    """the player's role card (looked up by key, not spelling); records a failure when missing, unsourced or stale."""
    byk = {key(k): v for k, v in cards.items() if isinstance(v, dict)}
    c = byk.get(key(nm))
    lo = (datetime.date.fromisoformat(date) - datetime.timedelta(days=3)).isoformat()
    if not c or not c.get('sources') or not c.get('role'):
        errs.append(f'{nm}: no role card with read sources in cards.json'); return None
    if not (lo <= c.get('asof', '') <= date):
        errs.append(f'{nm}: role card dated {c.get("asof")} (must be {lo} to {date})'); return None
    return c


def cmd_render(L, date, name=None):
    name = name or L          # calls/NAME.json -> renders/NAME.json, stamp 'gate ✓ NAME hash'
    p = pdir(date)
    errs = []
    cov = jload(os.path.join(p, 'coverage.json'), {})
    lc = cov.get('leagues', {}).get(L)
    if not lc or lc.get('status') != 'PASS':
        errs.append('coverage is not PASS for ' + L + ' (run check)')
    elif time.time() - cov.get('checked', 0) > MAX_AGE_H * 3600:
        errs.append(f'coverage older than {MAX_AGE_H}h: re-pull')
    else:
        for fn in (f'gate_{date}_{L}.txt', f'gate_{date}_ds_{L}.txt'):
            fp = os.path.join(p, 'data', fn)
            if os.path.exists(fp) and os.path.getmtime(fp) > cov.get('checked', 0):
                errs.append(f'{fn} changed after the last check: run check again')
    cpath = os.path.join(p, 'calls', name + '.json')
    if not os.path.exists(cpath):
        die(f'no calls file {cpath}')
    calls = jload(cpath)
    cards = jload(os.path.join(p, 'cards.json'), {})
    holds = [h for h in jload(os.path.join(GHOME, 'holds.json'))['holds'] if h['active'] and h['league'] == L]
    lg = League(L, date)
    over = calls.get('override', {})
    hold_ov = calls.get('hold_override', {})
    lines = []
    # moves
    roster = dict(lg.R)
    adds = []
    for mv in calls.get('moves', []):
        a, dname = mv.get('add'), mv.get('drop')
        if a:
            src, r = lg.find(a)
            if src == 'R':
                errs.append(f'add {a}: already on the roster')
            elif src is None:
                errs.append(f'add {a}: not in this league\'s pool pull (owned, or below the pulled pages)')
            else:
                st = r.get('status') or ''
                if st != 'FA' and not (mv.get('claim') and st.startswith('W')):
                    errs.append(f'add {a}: status {st or "?"} (FA required, or "claim": true for W)')
                rr = dict(r); rr['slot'] = 'BN'
                roster[r['key']] = rr; adds.append(rr)
        if dname:
            src, r = lg.find(dname)
            if src != 'R':
                errs.append(f'drop {dname}: not on the roster')
            else:
                for h in holds:
                    if hold_key(lg, h) == r['key'] and h['kind'] in ('drop', 'both') and dname not in hold_ov:
                        errs.append(f'drop {dname}: HOLD ("{h["quote"]}") - needs hold_override with the user\'s words')
                roster.pop(r['key'], None)
        if a and dname:
            sa_, sd_ = lg.find(a)[1], lg.find(dname)[1]
            if sa_ and sd_:
                if set(sa_.get('pos_all', [])) & set(sd_.get('pos_all', [])):
                    wa, wb, n, det = vote(lg.signals(sa_), lg.signals(sd_), WEEK_SIG + ROS_SIG)
                    mv['_vote'] = f'vs {dname}: wins {wa} of {n} ({", ".join(x[1:] for x in det if x[0] == "+") or "none"}); loses {", ".join(x[1:] for x in det if x[0] == "-") or "none"}'
                    if wb > wa and a not in over:
                        errs.append(f'add {a} over {dname}: loses {wb}-{wa} on {n} signals - needs override reason')
                elif not mv.get('drop_reason'):
                    errs.append(f'drop {dname} ({sd_.get("pos")}) for {a} ({sa_.get("pos")}): cross-position, needs drop_reason')
    cap, cap_src = roster_cap(lg)
    act = len([k for k, r in roster.items() if r.get('slot') != 'IR'])
    if act > cap:
        errs.append(f'roster {act} active > the {cap}-player limit ({cap_src}): an add needs a drop')
    if adds:
        for d in lg.lineup:
            if d['slot'] == 'IR' and d.get('key') in roster and not d.get('tag'):
                errs.append(f"IR slot holds {d['name']} with no IR tag: Yahoo blocks adds until he is moved out")
    trade_lines = trade_check(lg, calls['trade'], cards, holds, over, hold_ov, errs) if calls.get('trade') else []
    do_lineup = 'lineup' in calls or not calls.get('trade')   # a trade-only render skips the lineup
    # lineup
    lu = calls.get('lineup', {})
    want = {}
    for s in lg.c['slots']:
        want[s] = want.get(s, 0) + 1
    for s, n in (want.items() if do_lineup else []):
        got = lu.get(s, [])
        if len(got) != n:
            errs.append(f'lineup slot {s}: {len(got)} named, {n} required (every starting slot must be filled)')
    starters = []
    seen = set()
    for s, names in lu.items():
        for nm in names:
            src, r = lg.find(nm)
            r2 = roster.get(r['key']) if r else None
            if not r2:
                errs.append(f'{s} {nm}: not on the roster after the moves'); continue
            if r['key'] in seen:
                errs.append(f'{nm} named twice'); continue
            seen.add(r['key'])
            if not (set(r2.get('pos_all', [])) & ELIG.get(s, set())):
                errs.append(f'{s} {nm}: not eligible ({"/".join(r2.get("pos_all", []))})')
            if 'Bye' in (r2.get('kick') or ''):
                errs.append(f'{s} {nm}: on bye')
            if out_tag(r2.get('tag')):
                errs.append(f'{s} {nm}: tagged {r2["tag"]}')
            if r2.get('tag') == 'Q' and nm not in calls.get('fallback', {}):
                errs.append(f'{s} {nm}: questionable with no fallback named')
            starters.append((s, nm, r2))
    # lock order: the flex holds the latest kickoff among flex-eligible starters
    for s, nm, r in starters:
        if s not in FLEX:
            continue
        ko = kick_order(r.get('kick'))
        for s2, nm2, r2 in starters:
            if s2 in FLEX or not (set(r2.get('pos_all', [])) & ELIG[s]) or not (set(r.get('pos_all', [])) & ELIG[s2]):
                continue
            ko2 = kick_order(r2.get('kick'))
            if ko is not None and ko2 is not None and ko2 > ko and nm not in calls.get('lock_override', {}):
                errs.append(f'lock order: flex {nm} ({r.get("kick")}) kicks before {s2} {nm2} ({r2.get("kick")}): swap them, or lock_override')
    # signal votes: every starter in a hole slot and every add vs the alternatives on every signal
    holes = {d['slot'] for d in lg.lineup if d['slot'] not in ('BN', 'IR') and (d['name'] == '(Empty)' or 'Bye' in (d.get('kick') or '') or out_tag(d.get('tag')) or d.get('tag') == 'Q')}
    started = {r['key'] for _, _, r in starters}
    dec = []
    for s, nm, r in starters:
        moved = lg.R.get(r['key'], {}).get('slot') not in (s,)          # benched or new into this slot
        contested = s in holes or r['key'] in {x['key'] for x in adds} or s in FLEX or moved
        if not contested:
            continue
        sr = lg.signals(r)
        present = [x for x in WEEK_SIG if sr.get(x) is not None]
        need = 2 if r.get('pos') in ('K', 'DEF') else 3          # K/DEF only have the two engine projections
        if len(present) < need and nm not in over:
            errs.append(f'{s} {nm}: only {len(present)} of 4 week signals present ({", ".join(SIGNAME[x] for x in present)}) - needs override')
        cand = candidates(lg, ELIG[s])
        for kk, alt in lg.R.items():       # a current starter the calls bench is an alternative too
            if alt.get('slot') not in ('BN', 'IR') and kk not in started and set(alt.get('pos_all', [])) & ELIG[s]:
                cand.setdefault(kk, ('bench', alt))
        beaten = []
        for kk, (src, alt) in cand.items():
            if kk in started or kk == r['key']:
                continue
            if src == 'bench' and kk not in roster:
                continue
            if src != 'bench' and (alt.get('status') or '') != 'FA':
                continue  # not addable today
            if out_tag(alt.get('tag')) or 'Bye' in (alt.get('kick') or ''):
                continue
            asg = lg.signals(alt)
            wa, wb, n, det = vote(asg, sr, WEEK_SIG)
            gap = [x for x in WEEK_SIG if sr.get(x) is None and asg.get(x) is not None]   # signals only the alternative has
            if (n >= 2 and wa > wb) or (gap and n >= 1 and wa >= wb):
                beaten.append((alt['name'], wa, wb, n, src))
        txt = over.get(nm, '')
        for an, wa, wb, n, src in beaten:
            if surname(an) not in key(txt):
                errs.append(f'{s} {nm}: {an} ({src}) beats him {wa}-{wb} on {n} week signals - name {an} in override["{nm}"] with the reason, or start {an}')
        card = card_for(cards, nm, date, errs) or {}
        dec.append((s, nm, sr, beaten, txt, card))
    # K and DEF are checked every pass: an incumbent starter (not held) vs the free agents on both engines
    kd = []
    for s, nm, r in starters:
        if s not in ('K', 'DEF') or any(d[1] == nm for d in dec) or any(hold_key(lg, h) == r['key'] for h in holds):
            continue
        sr = lg.signals(r)
        better = []
        for kk, (src, alt) in candidates(lg, ELIG[s]).items():
            if src == 'bench' or kk in roster or (alt.get('status') or '') != 'FA' or out_tag(alt.get('tag')) or 'Bye' in (alt.get('kick') or ''):
                continue
            asg = lg.signals(alt)
            wa, wb, n, det = vote(asg, sr, ['y_wk', 'ds_wk'])
            if wa == 2 or (wa == 1 and n == 1):          # better on both engines (or on the only one the starter has)
                better.append((alt['name'], asg))
        txt = over.get(nm, '')
        for an, asg in better:
            if surname(an) not in key(txt):
                errs.append(f'{s} {nm} (Yahoo wk {fmt(sr.get("y_wk"))} / DS wk {fmt(sr.get("ds_wk"))}): free agent {an} ({fmt(asg.get("y_wk"))} / {fmt(asg.get("ds_wk"))}) is better on both engines - name {an} in override["{nm}"] with the reason, or add and start {an}')
        if better:
            kd.append((s, nm, sr, better, txt))
    add_over = {}
    for a in adds:
        card_for(cards, a['name'], date, errs)
        # an add is compared with the other free agents at his position on all six signals
        if a.get('pos') in ('K', 'DEF'):
            sigs = ['y_wk', 'ds_wk']
        else:
            sigs = WEEK_SIG + ROS_SIG
        for kk, (src, alt) in candidates(lg, set(a.get('pos_all', []))).items():
            if kk == a['key'] or src == 'bench' or (alt.get('status') or '') != 'FA' or out_tag(alt.get('tag')) or kk in {x['key'] for x in adds}:
                continue
            wa, wb, n, det = vote(lg.signals(alt), lg.signals(a), sigs)
            if n >= 2 and wa > wb:
                add_over.setdefault(a['name'], []).append(f"{alt['name']} {wa}-{wb}")
            if n >= 2 and wa > wb and surname(alt['name']) not in key(over.get(a['name'], '')):
                errs.append(f"add {a['name']}: {alt['name']} (FA) beats him {wa}-{wb} on {n} signals - name {alt['name']} in override[\"{a['name']}\"] with the reason, or add {alt['name']}")
    if errs:
        print(f'GATE FAIL {L}: {len(errs)} problem(s)', file=sys.stderr)
        for e in errs:
            print('  - ' + e, file=sys.stderr)
        sys.exit(1)
    # the evidence: every signal, role card and override, saved beside the block
    ytime = re.search(r'pulled (.*?)(?: PT)?$', lg.ytext, re.M)
    E = [f'▶ {L} (Yahoo {ytime.group(1) if ytime else "?"}; rivals {lc.get("rivals")}/{cfg()[L]["teams"] - 1}; coverage PASS)']
    if calls.get('moves'):
        E.append('MOVES')
        for mv in calls['moves']:
            a, dn = mv.get('add'), mv.get('drop')
            ra = lg.find(a)[1] if a else None
            rd = lg.find(dn)[1] if dn else None
            t = '  ' + ('CLAIM ' if mv.get('claim') else 'ADD ') + (f"{a} ({ra['team']} {ra['pos']}, {ra.get('status')})" if a else '') + (f" / DROP {dn} ({rd['team']} {rd['pos']})" if dn else '') + (f"  [{mv['when']}]" if mv.get('when') else '')
            E.append(t)
            if mv.get('_vote'):
                E.append('     ' + mv['_vote'])
            if mv.get('drop_reason'):
                E.append('     drop: ' + mv['drop_reason'])
            if a and ra and add_over.get(ra['name']):
                E.append(f"     free agents who win more of the 6 signals: {', '.join(add_over[ra['name']])}. Why {a}: {over.get(a) or over.get(ra['name'])}")
    E.extend(trade_lines)
    if do_lineup:
        E.append('LINEUP')
    order = []
    for s in lg.c['slots']:
        if s not in order:
            order.append(s)
    for s in order:
        for nm in lu.get(s, []):
            r = roster.get(key(nm)) or lg.find(nm)[1]
            E.append(f"  {s:<8}{nm} ({r.get('team')} {r.get('pos')}{', ' + r['tag'] if r.get('tag') else ''}; {(r.get('kick') or '').strip()})")
    if dec:
        E.append('WHY (signals: ' + ', '.join(SIGNAME[x] for x in WEEK_SIG) + ')')
        for s, nm, sr, beaten, txt, card in dec:
            E.append(f"  {s} {nm}: " + ', '.join(f"{SIGNAME[x]} {fmt(sr.get(x))}" for x in WEEK_SIG) + f"; DS ceiling {fmt(sr.get('ds_ceil'))}")
            E.append(f"     role ({card.get('asof')}): {card.get('role')}  [read: {'; '.join(card.get('sources', []))}]")
            if beaten:
                E.append(f"     over {', '.join(b[0] for b in beaten)} (they win more signals): {txt}")
            if nm in calls.get('fallback', {}):
                E.append(f"     fallback: {calls['fallback'][nm]}")
    for s, nm, sr, better, txt in kd:
        E.append(f"  {s} {nm} (Yahoo wk {fmt(sr.get('y_wk'))} / DS wk {fmt(sr.get('ds_wk'))}) over free agents better on both engines, " + ', '.join(f"{an} ({fmt(asg.get('y_wk'))} / {fmt(asg.get('ds_wk'))})" for an, asg in better) + f": {txt}")
    for n in calls.get('notes', []):
        E.append('  note: ' + n)
    ev_text = '\n'.join(E)
    # the block the user reads: clicks first, the lineup, conditions, one line of why each; lines kept short
    wrap = lambda t, ind='  ', sub='     ': textwrap.wrap(t, 88, initial_indent=ind, subsequent_indent=sub) or [ind]
    week = jload(os.path.join(p, 'manifest.json'), {}).get('week', '?')
    when = ytime.group(1).strip() if ytime else '?'
    try:
        dt = datetime.datetime.strptime(when, '%m/%d/%Y, %I:%M:%S %p')
        when = dt.strftime('%a ') + str(int(dt.strftime('%I'))) + dt.strftime(':%M %p')
    except ValueError:
        pass
    why = calls.get('why', {})
    tg = lambda r: f"{r.get('team')} {r.get('pos')}" if r else '?'
    B = [f'{L} · week {week} · data {when} · {lc.get("rivals")}/{cfg()[L]["teams"] - 1} rivals read ✓']
    if calls.get('moves'):
        B += ['', 'DO (you click)']
        for i, mv in enumerate(calls['moves'], 1):
            a, dn = mv.get('add'), mv.get('drop')
            ra = lg.find(a)[1] if a else None
            rd = lg.find(dn)[1] if dn else None
            t = (('Claim ' if mv.get('claim') else 'Add ') + f"{a} ({tg(ra)})" if a else '') + ((' · drop ' if a else 'Drop ') + f"{dn} ({tg(rd)})" if dn else '')
            B += wrap(t + (f"  by {mv['when'].replace('before ', '')}" if mv.get('when') else ''), f'  {i}. ', '     ')
    if trade_lines:
        B += ['', 'TRADE (you send it)']
        for t in trade_lines:
            if '[read:' not in t:
                B += wrap(re.sub(r'^TRADE with ', 'with ', t.strip()), '  ', '     ')
    if do_lineup:
        lab = {'W/R/T': 'FLEX', 'Q/W/R/T': 'SFLEX'}
        segs = []
        for s in order:
            nms = []
            for nm in lu.get(s, []):
                r = roster.get(key(nm)) or lg.find(nm)[1] or {}
                star = '*' if lg.R.get(r.get('key'), {}).get('slot') != s else ''
                nms.append(star + nm + (f" ({r['tag']})" if r.get('tag') else ''))
            segs.append(f"{lab.get(s, s):<5} " + ' · '.join(nms))
        B += ['', 'START  (* = change)']
        line = ''
        for sg in segs:
            if line and len(line) + 3 + len(sg) > 86:
                B.append('  ' + line); line = sg
            else:
                line = (line + '   ' + sg) if line else sg
        if line:
            B.append('  ' + line)
        dropped = {lg.find(mv['drop'])[1]['key'] for mv in calls.get('moves', []) if mv.get('drop') and lg.find(mv['drop'])[1]}
        benched = [d['name'] for k, d in lg.R.items() if d.get('slot') not in ('BN', 'IR') and k not in started and k not in dropped]
        if benched:
            B += wrap('to the bench: ' + ', '.join(benched))
    conds = [f"{nm}: {t}" for nm, t in calls.get('fallback', {}).items()] + list(calls.get('if', []))
    if conds:
        B += ['', 'IF']
        for c in conds:
            B += wrap(c, '  · ', '    ')
    W, seen_w = [], set()
    for s, nm, sr, beaten, txt, card in dec:
        sig = ' · '.join(f"{SHORT[x]} {fmt(sr.get(x))}" for x in (WEEK_SIG[:2] if s in ('K', 'DEF') else WEEK_SIG))
        alts = [b[0] for b in beaten] + [x for x in add_over.get(nm, []) if x.rsplit(' ', 1)[0] not in [b[0] for b in beaten]]
        W.append((nm, why.get(nm) or sig, alts))
    for a in adds:
        if a['name'] not in {w[0] for w in W}:
            sa = lg.signals(a)
            W.append((a['name'], why.get(a['name']) or ' · '.join(f"{SHORT[x]} {fmt(sa.get(x))}" for x in WEEK_SIG + ROS_SIG), add_over.get(a['name'], [])))
    for s, nm, sr, better, txt in kd:
        W.append((nm + ' kept', why.get(nm) or 'free agents ahead this week on both engines', [b[0] for b in better]))
    if W:
        B += ['', 'WHY']
        for nm, t, alts in W:
            if nm in seen_w:
                continue
            seen_w.add(nm)
            alts = [re.sub(r' \d+-\d+$', '', x) for x in alts]          # add_over carries 'Name 4-2'
            B += wrap(f"{nm}: {t}" + (f" (signals favor {', '.join(alts)}; the reason is in the evidence)" if alts else ''), '  · ', '    ')
    notes = calls.get('notes', [])
    if notes:
        B += ['', 'NOTE']
        for n in notes:
            B += wrap(n, '  · ', '    ')
    os.makedirs(os.path.join(p, 'renders'), exist_ok=True)
    evp = os.path.join(p, 'renders', name + '.txt')
    with open(evp, 'w') as f:
        f.write(ev_text + '\n')
    B += ['', 'evidence: ' + evp.replace(os.path.expanduser('~'), '~', 1)]
    body = '\n'.join(B)
    h = hashlib.sha256(body.encode()).hexdigest()[:8]
    json.dump({'league': L, 'name': name, 'date': date, 'hash': h, 'ts': int(time.time()), 'text': body, 'evidence': ev_text}, open(os.path.join(p, 'renders', name + '.json'), 'w'), indent=1)
    print(body)
    print(f'gate ✓ {name} {h}')


def tvc_values(lg):
    """the league's Draft Sharks trade value chart for this pass -> ({key: value}, path); empty when not read."""
    tvc = os.path.join(pdir(lg.date), 'data', f'gate_{lg.date}_tvc_{lg.L}.txt')
    dsv = {}
    if os.path.exists(tvc):
        for l in open(tvc).read().split('\n'):
            m = re.match(r'^(\d+) \| col\d \| (?:Mine )?(.*?) ([A-Z]{2,3}) (QB|RB|WR|TE)\d+$', l.strip())
            if m:
                dsv[key(m.group(2))] = int(m.group(1))
                dsv.setdefault(surname(m.group(2)) + '|' + TEAMFIX.get(m.group(3), m.group(3)), int(m.group(1)))
    return dsv, tvc


def ds_value(dsv, d):
    return dsv.get(key(d['name'])) if key(d['name']) in dsv else dsv.get(surname(d['name']) + '|' + d.get('team', ''))


def cmd_trades(L, date, top=8):
    """trade potentials with every rival, both sides' lineups week by week (byes filled from the bench), and why the
    other manager might say yes. Nothing is cut by a fixed number: candidates are ranked by what helps both
    sides (rest of season, and this week), never filtered, except that a deal must help the user on at least
    one horizon; held players stay out, injured players count at their projection, a player with no projection
    has nothing to trade. Leads only: a lead reaches the user through a calls
    file and render."""
    import itertools
    lg = League(L, date)
    holds = [h for h in jload(os.path.join(GHOME, 'holds.json'))['holds'] if h['active'] and h['league'] == L]
    held = {hold_key(lg, h) for h in holds if h['kind'] in ('trade', 'both')}
    me, note = planned_me(lg)
    slots, W = lg.c['slots'], lg.week
    dsv, tvc = tvc_values(lg)
    room = roster_cap(lg)[0] - len([d for d in lg.lineup if d['slot'] != 'IR' and d.get('key')])
    print(f'== {L} trade potentials, week {W} ({date}). Yahoo projections, best lineup each week, byes filled from the bench. '
          'DS trade values: ' + ('read' if dsv else f'not read (chart: {os.path.basename(tvc)})') + '.')
    if note:
        print('   ' + note)
    print('   you: ' + race(lg, lg.c['team'])[1])
    print('   Leads, not calls: a lead reaches the user only through a calls file and render.')
    pc = pending_claim(lg)
    pend = key(pc[0]) if pc else None      # not on the roster until the claim processes
    mine = [k for k, v in me.items() if k not in held and k != pend and (v.get('ros') or 0) > 0]   # an injured player counts at his projection
    hz = horizons(lg)
    bm = {f: weekly_total(me, slots, W, e, a) for f, a, e, n in hz}
    starters = league_starters(lg)
    leads, nriv = [], 0
    for pid in rivals(lg):
        th = team_players(lg, pid)
        if not th:
            continue
        nriv += 1
        bt = {f: weekly_total(th, slots, W, e, a) for f, a, e, n in hz}
        theirs = [k for k, v in th.items() if (v.get('ros') or 0) > 0]   # zero projection: nothing to gain
        for ng, nt in ((1, 1), (1, 2), (2, 1), (2, 2)):
            for G in itertools.combinations(mine, ng):
                for T in itertools.combinations(theirs, nt):
                    me2 = {k: v for k, v in me.items() if k not in G}
                    me2.update({k: th[k] for k in T})
                    gm = {f: (weekly_total(me2, slots, W, e, a) - bm[f]) / n for f, a, e, n in hz}
                    if max(gm.values()) <= 0:
                        continue                  # helps the user on no horizon: not a potential for him
                    th2 = {k: v for k, v in th.items() if k not in T}
                    th2.update({k: me[k] for k in G})
                    gt = {f: (weekly_total(th2, slots, W, e, a) - bt[f]) / n for f, a, e, n in hz}
                    vg = [ds_value(dsv, me[k]) for k in G]
                    vt = [ds_value(dsv, th[k]) for k in T]
                    leads.append((gm, gt, pid, [me[k] for k in G], [th[k] for k in T], vg, vt, th2))
    print(f'   rivals read: {nriv}/{cfg()[L]["teams"] - 1}; potentials: {len(leads)}')
    if nriv != cfg()[L]['teams'] - 1:
        print(f'!! INCOMPLETE: {nriv} rival rosters in the pull for {cfg()[L]["teams"] - 1} rivals: re-pull before trusting this list')
    tag = lambda p: f"{p['name']} ({p.get('team')} {p.get('pos')})"

    def show(rows, n_show):
        seen, shown = set(), 0
        for gm, gt, pid, G, T, vg, vt, th2 in rows:
            sig = (pid[1], tuple(sorted(p['name'] for p in T)))
            sig2 = (pid[1], tuple(sorted(p['name'] for p in G)))
            if sig in seen or sig2 in seen:
                continue
            seen.update((sig, sig2))
            dv = (sum(vg) - sum(vt)) if None not in vg + vt else None
            ds = 'DS ?' if dv is None else f"DS you give {sum(vg)}, get {sum(vt)}"
            drops = len(T) - len(G) - room
            gg = {'me_' + k: v for k, v in gm.items()}
            gg.update({'th_' + k: v for k, v in gt.items()})
            print(f"  you {gains_text(gg, 'me', lg)} | {ds}" + (f' | needs {drops} drop' if drops > 0 else ''))
            print(f"     give {', '.join(tag(p) for p in G)}  /  get {', '.join(tag(p) for p in T)}")
            vv = lambda p, v: f"{p['name']}{' (' + p['tag'] + ')' if p.get('tag') else ''} DS {'?' if v is None else v}, Yahoo ROS {p.get('ros') or 0:.0f}"
            print(f"     side by side: give {'; '.join(vv(p, v) for p, v in zip(G, vg))}  |  get {'; '.join(vv(p, v) for p, v in zip(T, vt))}")
            print(f"     {pid[1]}, {race(lg, pid[0])[1]}: {gains_text(gg, 'th', lg)}")
            for line in their_needs(lg, starters, pid, th2):
                print('     ' + line)
            shown += 1
            if shown >= n_show:
                break
    print(f'-- best for both sides rest of season (ranked by the smaller of the two gains), top {top}:')
    show(sorted(leads, key=lambda x: -min(x[0]['ros'], x[1]['ros'])), top)
    print('-- best for both sides this week (ranked by the smaller of the two this-week gains), top 3:')
    show(sorted(leads, key=lambda x: -min(x[0]['wk'], x[1]['wk'])), 3)
    if any(f == 'po' for f, a, e, n in hz) and not lg.stand:
        print('-- sell to contenders / buy from teams below the line: no standings in this pull (re-collect with this version)')
    elif any(f == 'po' for f, a, e, n in hz):
        sell = [x for x in leads if race(lg, x[2][0])[0] == 'in']
        near = 'rs' if any(f == 'rs' for f, a, e, n in hz) else 'n4'
        print('-- sell to teams in a playoff spot: your weeks until the playoffs against their playoff weeks (ranked by the smaller), top 3:')
        show(sorted(sell, key=lambda x: -min(x[0][near], x[1]['po'])), 3)
        buy = [x for x in leads if race(lg, x[2][0])[0] in ('chasing', 'out')]
        print('-- buy from teams below the playoff line: your playoff weeks against their weeks until the playoffs (ranked by the smaller), top 3:')
        show(sorted(buy, key=lambda x: -min(x[0]['po'], x[1][near])), 3)

def _arrival(status, year):
    m = re.match(r'W \((\w{3}) (\d+)\)', status or '')
    if not m:
        return status or ''
    d = datetime.datetime.strptime(f'{m.group(1)} {m.group(2)} {year}', '%b %d %Y')
    return d.strftime('%A %Y-%m-%d')


def cmd_watch(date):
    """the pass's watch list: waiver players worth a claim-or-wait call, the injury and condition table from the
    delivered calls, and pending claims. Prints it and writes passes/DATE/watch.md."""
    p = pdir(date)
    year = int(date[:4])
    holds_all = [h for h in jload(os.path.join(GHOME, 'holds.json'))['holds'] if h['active']]
    renders = {}
    for fn in sorted(os.listdir(os.path.join(p, 'renders'))) if os.path.isdir(os.path.join(p, 'renders')) else []:
        if fn.endswith('.json'):
            r = jload(os.path.join(p, 'renders', fn))
            if r.get('league') and r.get('ts', 0) >= renders.get(r['league'], {}).get('ts', 0) and 'trade' not in r.get('name', '').lower():
                renders[r['league']] = r
    out = [f'# Watch list, week {jload(os.path.join(p, "manifest.json"), {}).get("week", "?")} (pass {date})', '',
           'Every waiver row gets an explicit claim-or-wait call with its priority cost: a player with real',
           'production does not reach free agency. Waiver arrivals are the host\'s W (date) labels: the overnight',
           'run that morning hands the player to the best claim, or makes him a free agent.', '',
           '## Waiver players', '',
           '| League | Player | Arrives | Beats | Your priority | % rostered | Last 4 /g | Claim or wait? |', '|---|---|---|---|---|---|---|---|']
    pend_lines, cond = [], []
    for L in cfg():
        lg = League(L, date)
        held = {hold_key(lg, h) for h in holds_all if h['league'] == L and h['kind'] in ('drop', 'both')}
        head = next((l for l in lg.ytext.split('\n') if l.startswith('HEADER:')), '')
        pri = (re.search(r'Waiver Priority: (\d+\w*)', head) or [None, '?'])[1]
        pend = next((l for l in lg.ytext.split('\n') if l.startswith('PENDING:')), '')
        pdrops = set()
        for m in re.finditer(r'Waiver \d+ \(([^)]*)\): Add (.+?)(?:, Drop (.+?))?(?= View| Waiver \d| Week \d|$)', pend):
            if m.group(3):
                pdrops.add(key(m.group(3)))
            pend_lines.append(f'- {L}: claim Add {m.group(2)}' + (f', Drop {m.group(3)}' if m.group(3) else '') + f', processes {_arrival("W (" + m.group(1) + ")", year)}'
                              + (' (certain: priority 1)' if pri == '1st' and m.group(0).startswith('Waiver 1 ') else ''))
        one_qb = lg.c['slots'].count('QB') == 1 and 'Q/W/R/T' not in lg.c['slots']
        nqb = len([r for r in lg.R.values() if r.get('pos') == 'QB'])
        bench = [r for k, r in lg.R.items() if r.get('slot') == 'BN' and k not in held and k not in pdrops and not out_tag(r.get('tag'))
                 and r.get('pos') not in ('K', 'DEF') and lg.signals(r).get('y_ros') is not None and lg.signals(r).get('ds_ros') is not None]
        weak = min(bench, key=lambda r: lg.signals(r)['y_ros']) if bench else None
        for k, r in lg.P.items():
            st = r.get('status') or ''
            if not st.startswith('W') or out_tag(r.get('tag')):
                continue
            s = lg.signals(r)
            beats = ''
            if r.get('pos') in ('K', 'DEF'):
                cur = next((x for x in lg.R.values() if x.get('slot') == r.get('pos')), None)
                if cur:
                    cs = lg.signals(cur)
                    if all((s.get(x) is not None and cs.get(x) is not None and s[x] > cs[x]) for x in ('y_wk', 'ds_wk')):
                        beats = f"{cur['name']} this week (Yahoo {fmt(s['y_wk'])} v {fmt(cs['y_wk'])}, DS {fmt(s['ds_wk'])} v {fmt(cs['ds_wk'])})"
            elif weak and not (r.get('pos') == 'QB' and one_qb and nqb >= 2):
                ws = lg.signals(weak)
                if s.get('y_ros') is not None and s.get('ds_ros') is not None and s['y_ros'] > ws['y_ros'] and s['ds_ros'] > ws['ds_ros']:
                    beats = f"{weak['name']} rest of season (Yahoo {fmt(s['y_ros'])} v {fmt(ws['y_ros'])}, DS {fmt(s['ds_ros'])} v {fmt(ws['ds_ros'])})"
            if beats:
                out.append(f"| {L} | {r['name']} ({r.get('team')} {r.get('pos')}) | {_arrival(st, year)} | {beats} | {pri} | {r.get('% Ros', '?')} | {fmt(s.get('l4g'))} | DECIDE |")
        rec = renders.get(L)
        if rec:
            c = jload(os.path.join(p, 'calls', rec['name'] + '.json'), {})
            for nm, t in c.get('fallback', {}).items():
                src, r = lg.find(nm)
                cond.append(f"| {L} | {nm} | {t} | {(r or {}).get('kick', '?') if r else '?'} |")
            for t in c.get('if', []) if isinstance(c.get('if', []), list) else [c.get('if')]:
                cond.append(f'| {L} | - | {t} | - |')
    out += ['', '## Injuries and conditions (from the delivered calls)', '', '| League | Player | If | His kickoff |', '|---|---|---|---|'] + (cond or ['| - | - | none | - |'])
    out += ['', '## Pending claims', ''] + (pend_lines or ['- none'])
    out += ['', 'Then set a reminder at each arrival and at the final injury reports, and run `trades` for every league.']
    body = '\n'.join(out)
    open(os.path.join(p, 'watch.md'), 'w').write(body + '\n')
    h = hashlib.sha256(body.encode()).hexdigest()[:8]
    os.makedirs(os.path.join(p, 'renders'), exist_ok=True)
    json.dump({'league': 'watch', 'name': 'watch', 'date': date, 'hash': h, 'ts': int(time.time()), 'text': body},
              open(os.path.join(p, 'renders', 'watch.json'), 'w'), indent=1)
    print(body)
    print(f'gate ✓ watch {h}')


def cmd_close(date):
    mp = os.path.join(pdir(date), 'manifest.json')
    man = jload(mp)
    man['open'] = False
    man['closed'] = int(time.time())
    json.dump(man, open(mp, 'w'), indent=1)
    print('pass closed', date)


# ---------------------------------------------------------------- Stop hook
CALL_VERB = re.compile(r'\b(add|adds|drop|drops|claim|start|starts|bench|sit|swap|move|moves|put|offer|trade|stream|flex)\b', re.I)
POS_MARK = re.compile(r'\((?:[A-Z]{2,3}\s+)?(QB|RB|WR|TE|K|DEF)\b[^)]*\)'
                      r'|\b(to|at|into|in)\s+(?:the\s+)?(?:\w+\s+)?(QB|RB|WR|TE|K|DEF|flex|superflex|W/R/T|Q/W/R/T)\b'
                      r'|\b(QB|RB|WR|TE|DEF)\s*:'
                      r'|\b[A-Z][a-z]+\s+(DEF|D/ST)\b', re.I)
# a bare lineup line: "QB: First Last", "**WRs: Last and Last**", "- Flex: Last"
SLOT_LINE = re.compile(r'^\s*(?:[-*]\s*)?\**\s*(QB|RBs?|RB2|WRs?|WR2|TE|Flex|K|DEF|Superflex|W/R/T)\b[^:\n]{0,14}:\s*\**\s*[A-Z][a-z]', re.I)
# a render-format line pasted without its stamp: '  WR    *Name · Name', '  1. Add Name (...' (and the older '  ADD Name (...')
BLOCK_LINE = re.compile(r'^\s{2}(QB|RB|WR|TE|W/R/T|Q/W/R/T|FLEX|SFLEX|K|DEF)\s{1,}\*?[A-Z]|^\s{2}(ADD|CLAIM|GIVE) [A-Z]|^\s{2}\d+\. (Add|Claim|Drop) [A-Z]|^\s*give [A-Z].*\s/\s+get [A-Z]')


def last_turn_blocks(inp):
    """every text block Claude wrote since the user's last prompt (not only the final message), in order."""
    bl = turn_from_transcript(inp.get('transcript_path'))
    lam = inp.get('last_assistant_message') or ''
    if lam and lam not in '\n'.join(bl):
        bl.append(lam)
    return bl


def last_turn_text(inp):
    return '\n'.join(last_turn_blocks(inp))


def turn_from_transcript(tp):
    if not tp or not os.path.exists(tp):
        return []
    with open(tp, 'rb') as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - 3_000_000))
        lines = f.read().decode('utf-8', 'replace').split('\n')
    texts = []
    for l in reversed(lines):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if not isinstance(o, dict):
            continue
        m = o.get('message') or {}
        if not isinstance(m, dict):
            continue
        if o.get('type') == 'user' and not o.get('isMeta'):
            c = m.get('content')
            if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'text' for x in c) and not any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c)):
                break
        if o.get('type') == 'assistant':
            for x in (m.get('content') or []):
                if isinstance(x, dict) and x.get('type') == 'text':
                    texts.append(x.get('text', ''))
    return list(reversed(texts))


def aliases():
    """[(compiled pattern, league)]; short aliases (three characters or fewer) match case-sensitively, so a lowercase word spelled like one does not."""
    out = []
    for L, c in cfg().items():
        for a in c.get('aliases', [L]):
            out.append((re.compile(r'(?<![\w-])' + re.escape(a) + r'(?![\w-])', 0 if len(a) <= 3 else re.I), L))
    return out


def check_message(text):
    """-> list of problems (empty = allowed). A text that is a list of blocks is checked as one message, except
    that a block opening with 'INCOMPLETE: <reason>' is exempt on its own (not the blocks around it)."""
    if isinstance(text, list):
        text = '\n'.join(b for b in text if not re.match(r'\s*INCOMPLETE:\s*\S', b))
    if not text.strip():
        return []
    if re.match(r'\s*INCOMPLETE:\s*\S', text):
        return []
    probs = []
    # verify stamped blocks and cut them out
    for m in list(re.finditer(r'^gate ✓ (\S+) ([0-9a-f]{8})\s*$', text, re.M)):
        L, h = m.group(1), m.group(2)
        rec = None
        for d in sorted(os.listdir(PASSES), reverse=True)[:3] if os.path.isdir(PASSES) else []:
            fp = os.path.join(PASSES, d, 'renders', L + '.json')
            if os.path.exists(fp):
                r = jload(fp)
                if r.get('hash') == h:
                    rec = r; break
        if not rec:
            probs.append(f'stamp "gate ✓ {L} {h}" matches no render on file')
            continue
        if rec['text'] not in text:
            probs.append(f'{L} block was edited after render (paste it verbatim)')
            continue
        text = text.replace(rec['text'], '').replace(m.group(0), '')
    al = aliases()
    ctx = None
    hits = []
    for line in text.split('\n'):
        st = line.strip()
        named = [L for rx, L in al if rx.search(line)]
        if named:
            ctx = named[-1]       # once a league is named, every later line is read as belonging to it
        if named or ctx:
            if (CALL_VERB.search(line) and POS_MARK.search(line)) or SLOT_LINE.search(line) or BLOCK_LINE.search(line):
                hits.append(st[:120])
    if hits:
        probs.append('unrendered fantasy call(s): ' + ' || '.join(hits[:3]))
    return probs


def cmd_hook():
    if not os.path.exists(os.path.join(GHOME, 'leagues.json')):
        sys.exit(0)  # no gate home: this user has not set the gate up
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        inp = {}
    state = os.path.join(PASSES, '.hook_state.json')
    try:
        st = jload(state, {})
    except ValueError:
        st = {}
    blocks = last_turn_blocks(inp)
    sid = inp.get('session_id', '')
    prev = st.get(sid) if isinstance(st.get(sid), dict) else None
    if prev and inp.get('stop_hook_active') and len(blocks) > prev.get('judged', 0):
        # after a block, only the text written since is judged; it must retract or replace the unchecked call
        new = blocks[prev['judged']:]
        probs = check_message(new)
        joined = '\n'.join(new)
        if not probs and not (re.search(r'not a checked call', joined, re.I) or re.search(r'^gate ✓ \S+ [0-9a-f]{8}\s*$', joined, re.M) or any(re.match(r'\s*INCOMPLETE:\s*\S', b) for b in new)):
            probs = ['after a block, tell the user the earlier text was "not a checked call", or replace it with a rendered block or an INCOMPLETE: note']
    else:
        probs = check_message(blocks)
    if not probs:
        if sid in st:
            st.pop(sid, None); json.dump(st, open(state, 'w'))
        sys.exit(0)
    n = (prev or {}).get('n', 0) + 1
    st[sid] = {'n': n, 'judged': len(blocks)}
    os.makedirs(PASSES, exist_ok=True)
    json.dump(st, open(state, 'w'))
    if n > 3:
        st.pop(sid, None); json.dump(st, open(state, 'w'))
        print(json.dumps({'systemMessage': 'Fantasy gate: a call reached you without passing the gate after 3 blocks. Treat it as unchecked. ' + '; '.join(probs)[:400]}))
        sys.exit(0)
    reason = ('FANTASY GATE BLOCKED this reply: ' + '; '.join(probs) + '. Fantasy calls reach the user only as a block printed by '
              '`gate.py render <league>` (the plugin scripts folder), pasted verbatim with its "gate ✓" stamp. '
              'Tell the user plainly that the previous text was not a checked call, then render it, or start the message with '
              '"INCOMPLETE:" naming the failed check.')
    print(json.dumps({'decision': 'block', 'reason': reason}))
    sys.exit(0)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    c = a[0]
    if c == 'hook':
        return cmd_hook()
    if c == 'open':
        if len(a) < 2:
            die('usage: gate.py open WEEK [DATE]')
        return cmd_open(a[2] if len(a) > 2 else today(), a[1])
    date = None
    rest = a[1:]
    if rest and re.match(r'\d{4}-\d\d-\d\d$', rest[-1]):
        date = rest.pop()
    date = date or today()
    if c == 'ingest':
        return cmd_ingest(date)
    if c == 'check':
        return cmd_check(date)
    if c == 'board':
        return cmd_board(rest[0], date)
    if c == 'render':
        return cmd_render(rest[0], date, rest[1] if len(rest) > 1 else None)
    if c == 'trades':
        return cmd_trades(rest[0], date, int(rest[1]) if len(rest) > 1 else 8)
    if c == 'watch':
        return cmd_watch(date)
    if c == 'close':
        return cmd_close(date)
    print(__doc__); sys.exit(2)


if __name__ == '__main__':
    main()
