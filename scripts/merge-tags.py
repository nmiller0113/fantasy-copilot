"""Merge outlet tag rows into the team files' Media read tables.

    python3 merge-tags.py --dir <kb> --outlet "<outlet name> <YYYY-MM-DD>" --json rows.json [--json more.json] [--dry-run]

Input: one or more JSON files, each an array of objects with keys team, player, tag, line
(pos and page are accepted and ignored). team is any spelling data/teams.md lists; tag,
lowercased, is one of sleeper, breakout, bust, risk, handcuff, hype, or "rookie" (recorded
as sleeper); line is one sentence. Extractor agents write these files from a guide's
pages; this script does the writing into the profiles, so an agent never edits a team file.

Player, line and outlet label are sanitized the same way: a pipe becomes a slash and every
run of whitespace folds to one space, so nothing a guide prints can break a table. In the
line and the label a semicolon also becomes a comma, because "; " is what separates the
fragments of a Line cell and a fragment this script writes has to stay one fragment for a
rerun to be able to lift it back out whole.

Matching a row to the table is two passes over the whole Media read table, never the first
row that looks close. Pass one takes an exact name match (the first of them, where a
player already holds several tag rows). Only when there is none does pass two try the
surname, a Jr./Sr./II-V suffix ignored, with a first name that fits: an initial matches
any first name starting with that letter, while two full first names must be the same word
or share their first three letters, so a nickname or a stray capital still merges and two
different names under one initial do not. Both passes ignore case. Pass two refuses the
row -- and with it the whole set -- if it matches more than one distinct name in the
table, or if the JSON name is an exact row name under a different team, either of which
means the guess would land on the wrong player. A first name that does not fit is not a
match at all, so the player gets a new row rather than someone else's.

A matched row keeps its place: the tag is added if new, the line is appended as "; <line>
(<outlet>)", and the Outlets count rises once per outlet, not once per row -- it rises
only when this outlet's label was not already the ending of a fragment in the Line cell.
A player the table does not hold gets a new row after the last one, count 1.

A rerun is idempotent per outlet: before appending, every existing fragment ending in this
exact outlet label is dropped from the Line cell and the count comes down by one, so
running the same JSON twice leaves the file identical to running it once. A new edition
replaces the previous edition's fragments only when --outlet is the same string, and only
on the rows the new edition names: a player the new edition dropped keeps the previous
edition's line and count under that label, because a row this run never touches is a row
this run never reads. So a rerun carries the guide's full set, never a hand-picked few.
A new date is a different label, so both editions stay on the row. Tags are never removed:
which tag an outlet contributed is not recorded, so a rerun cannot know what to take back.

Nothing else in the file is touched. Prints the counts; --dry-run prints them without
writing.

Refuse before write, always: a pre-flight pass checks that every row carries non-empty
team, player, tag and line, that the tag is in the vocabulary, that the team resolves to
exactly one code (an exact spelling from data/teams.md first, case-insensitively;
otherwise a substring match, refused when it fits more than one code), and that each
resolved team file exists with a "## Media read" section carrying a table header row.
Every new file body is then built in memory, and the files are written only after the last
team has succeeded, so no error can leave a half-merged knowledgebase. Exit 1, with the
offending rows listed, on any of it.
"""
import argparse, json, os, re, sys

TAGS = {'sleeper', 'breakout', 'bust', 'risk', 'handcuff', 'hype'}
TAGMAP = {'rookie': 'sleeper'}
CODE = re.compile(r'^[A-Z]{2,3}$')
INITIAL = re.compile(r'^[A-Za-z]\.?$')
SUFFIX = {'jr', 'jr.', 'sr', 'sr.', 'ii', 'iii', 'iv', 'v'}

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True); ap.add_argument('--outlet', required=True)
ap.add_argument('--json', action='append', required=True); ap.add_argument('--dry-run', action='store_true')
a = ap.parse_args()


def clean(v):
    """One line, no pipes: a pipe becomes a slash, whitespace runs fold to one space."""
    return ' '.join(str(v).split()).replace('|', '/')


def fragment_safe(v):
    """clean(), and a semicolon becomes a comma: "; " separates the Line cell's fragments,
    so a fragment this script writes must never contain one, or a rerun could not tell
    where this outlet's fragment began and would leave half of it behind."""
    return clean(v).replace(';', ',')


def cells_of(line):
    return [x.strip() for x in line.strip().strip('|').split('|')]


def is_data_row(line):
    if not line.startswith('|'): return False
    c = cells_of(line)
    return len(c) >= 4 and c[0] != 'Player' and not c[0].startswith('---')


def is_header_row(line):
    return line.startswith('|') and cells_of(line)[0] == 'Player'


def surname(name):
    parts = [p for p in name.split() if p.lower() not in SUFFIX]
    return parts[-1] if parts else ''


def near_match(name, row):
    """Pass two's test: the surname (a Jr./Sr./II-V suffix ignored) equal, and the first
    names compatible. An initial matches any first name starting with that letter; two
    full first names must be the same word or share their first three letters, so a
    nickname or a different capitalization still merges while two different names under
    one initial do not. Case never decides either comparison."""
    a1, b1 = surname(name).lower(), surname(row).lower()
    if not a1 or a1 != b1: return False
    f = name.split()[0] if name.split() else ''
    g = row.split()[0] if row.split() else ''
    if not f or not g: return False
    if INITIAL.match(f) or INITIAL.match(g): return f[:1].lower() == g[:1].lower()
    return f.lower() == g.lower() or f[:3].lower() == g[:3].lower()


def section(lines):
    """(start, end) of the Media read section, or None."""
    start = None
    for i, l in enumerate(lines):
        if l.startswith('## Media read'): start = i; break
    if start is None: return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '): end = j; break
    return start, end


def die(bad):
    print('merge-tags: refused,', len(bad), 'bad row(s), nothing written:')
    print('\n'.join(bad[:20]))
    if len(bad) > 20: print(f'... and {len(bad) - 20} more')
    sys.exit(1)


# --- team spellings ---------------------------------------------------------
teams_md = os.path.join(a.dir, 'data', 'teams.md')
if not os.path.isfile(teams_md): die([f'no team list at {teams_md}'])
spellings = {}
for raw in open(teams_md, encoding='utf-8'):
    if '|' not in raw: continue
    cs = [c.strip() for c in raw.strip().strip('|').split('|')]
    if not CODE.match(cs[0]): continue
    for c in cs:
        if c: spellings.setdefault(c.lower(), cs[0])
if not spellings: die([f'no team rows in {teams_md}'])


def resolve(team):
    """(code, error): an exact spelling first, then a substring that fits one code only."""
    t = clean(team).lower()
    if t in spellings: return spellings[t], None
    hits = sorted({v for k, v in spellings.items() if len(k) > 3 and (k in t or t in k)})
    if len(hits) == 1: return hits[0], None
    if hits: return None, 'fits ' + ', '.join(hits)
    return None, 'not in data/teams.md'


# --- the knowledgebase's team files -----------------------------------------
teams_dir = os.path.join(a.dir, 'teams')
if not os.path.isdir(teams_dir): die([f'no teams directory at {teams_dir}'])
files = {}   # code -> list of lines
elsewhere = {}   # player name, lowercased -> set of codes holding a row for it
for fn in sorted(os.listdir(teams_dir)):
    if not fn.endswith('.md'): continue
    c = fn[:-3]
    ls = open(os.path.join(teams_dir, fn), encoding='utf-8').read().split('\n')
    files[c] = ls
    sec = section(ls)
    if not sec: continue
    for k in range(sec[0], sec[1]):
        if is_data_row(ls[k]): elsewhere.setdefault(cells_of(ls[k])[0].lower(), set()).add(c)

# --- rows -------------------------------------------------------------------
rows = []
for p in a.json:
    try: data = json.load(open(p, encoding='utf-8'))
    except Exception as e: die([f'{p}: {e}'])
    if not isinstance(data, list): die([f'{p}: not a JSON array'])
    rows += data

# --- pre-flight -------------------------------------------------------------
bad = []
byteam = {}
for n, r in enumerate(rows, 1):
    if not isinstance(r, dict): bad.append(f'row {n}: not an object'); continue
    who = str(r.get('player', '?'))
    miss = [f for f in ('team', 'player', 'tag', 'line')
            if not isinstance(r.get(f), str) or not r.get(f).strip()]
    if miss: bad.append(f'row {n} ({who}): empty or missing ' + ', '.join(miss)); continue
    tag = str(r['tag']).strip().lower()
    tag = TAGMAP.get(tag, tag)
    if tag not in TAGS: bad.append(f'row {n} ({who}): tag {r["tag"]!r} outside the vocabulary'); continue
    c, err = resolve(r['team'])
    if c is None: bad.append(f'row {n} ({who}): team {r["team"]!r} {err}'); continue
    byteam.setdefault(c, []).append((n, r, tag))
for c in sorted(byteam):
    if c not in files: bad.append(f'{c}: no file at ' + os.path.join(teams_dir, c + '.md')); continue
    sec = section(files[c])
    if not sec: bad.append(f'{c}: no "## Media read" section'); continue
    if not any(is_header_row(files[c][k]) for k in range(*sec)):
        bad.append(f'{c}: the Media read section has no table header row')
if bad: die(bad)

# --- build every new file in memory ----------------------------------------
label = f'({fragment_safe(a.outlet)})'
added = merged = repeat = 0
contents = {}
for c in sorted(byteam):
    lines = list(files[c])
    start, end = section(lines)
    state = {}   # table row index -> {'n': count or None, 'text': Line cell without this outlet}
    for n, r, tag in byteam[c]:
        name = clean(r['player']); text = fragment_safe(r['line']).rstrip('.')
        hit = None
        for k in range(start, end):
            if is_data_row(lines[k]) and cells_of(lines[k])[0].lower() == name.lower(): hit = k; break
        if hit is None:
            near = [k for k in range(start, end)
                    if is_data_row(lines[k]) and near_match(name, cells_of(lines[k])[0])]
            names = sorted({cells_of(lines[k])[0] for k in near}, key=str.lower)
            if len({x.lower() for x in names}) > 1:
                bad.append(f'row {n} ({name}, {c}): surname match is ambiguous between ' + ', '.join(names))
                continue
            if names:
                other = elsewhere.get(name.lower(), set()) - {c}
                if other:
                    bad.append(f'row {n} ({name}, {c}): would land on {names[0]}, but {name} has a row under ' + ', '.join(sorted(other)))
                    continue
                hit = near[0]
        if hit is None:
            k = max(i for i in range(start, end) if lines[i].startswith('|'))
            lines.insert(k + 1, f'| {name} | {tag} | 1 | {text} {label} |')
            # the row is this outlet's already: a second row for the same player later in
            # the same run appends to it, and must not strip the fragment just written.
            state[k + 1] = {'n': 0, 'text': f'{text} {label}'}
            end += 1; added += 1
            continue
        cs = cells_of(lines[hit])
        if hit not in state:
            frags = cs[3].split('; ')
            keep = [f for f in frags if not f.endswith(' ' + label)]
            had = len(keep) != len(frags)
            if had: repeat += 1
            try: count = int(cs[2])
            except ValueError: count = None
            if count is not None and had: count = max(count - 1, 0)
            state[hit] = {'n': count, 'text': '; '.join(keep).strip('; ')}
        st = state[hit]
        st['text'] = f"{st['text']}; {text} {label}" if st['text'] else f'{text} {label}'
        tags = [t for t in cs[1].split('/') if t]
        if tag not in tags: tags.append(tag)
        cs[1] = '/'.join(tags) if tags else tag
        if st['n'] is not None: cs[2] = str(st['n'] + 1)
        cs[3] = st['text']
        lines[hit] = '| ' + ' | '.join(cs) + ' |'
        merged += 1
    contents[os.path.join(teams_dir, c + '.md')] = '\n'.join(lines)
if bad: die(bad)

# --- write ------------------------------------------------------------------
if not a.dry_run:
    for p in sorted(contents):
        open(p, 'w', encoding='utf-8').write(contents[p])
print(f'merge-tags: {len(rows)} rows from {len(a.json)} file(s), {len(byteam)} teams: '
      f'{added} rows added, {merged} merged ({repeat} table rows already carried this outlet and were replaced)'
      + (' (dry run, nothing written)' if a.dry_run else ''))
