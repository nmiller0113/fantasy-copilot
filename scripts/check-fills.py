#!/usr/bin/env python3
"""Check a knowledgebase gap fill against the source tables it cites.

Every "[filled <date>: <data file>]" marker in a profile must name a file that exists
under data/, and the sentence carrying the marker is then checked against that file's
rows, not against the file as a whole:

  1. Anchors are read from the whole line, the heading it sits under (a markdown
     heading, a bold-led bullet, or a plain label line ending in a colon) and the
     profile's own file name: every player name, every team code, and every NFL city or
     nickname that maps to a code. A data file may spell the team its own way, so a code
     is searched under every spelling data/teams.md lists for it (another site's code,
     the city, the nickname, the full name) for the tables that print names instead
     of codes. The script carries no team of its own; the list is the knowledgebase's.
  2. The rows of the cited table carrying one of those anchors are the search space. On
     a player table a name finds the row; on a team-level table (points allowed, EPA,
     win rates, scheme rates, line rankings) only the code does; a name that matches
     nothing contributes nothing. A line naming three or more different teams is a
     league-wide list rather than one subject's row (ESPN's player top twenties print
     twenty teams on one line), so it is split on "; " first and only the entry carrying
     the anchor can be searched.
  2a. A name is scoped to the teams the line names. Once several rows answer to the same
     name, it reaches only the rows that also carry one of the line's teams, or rows
     carrying no team at all; a name that answers to exactly one row in the table is
     already one player and reaches it either way, which is what lets a surname on its
     own find a benchmark player on another club. A word inside a multi-word team
     spelling is never a name, so a city word two clubs share, or a direction word
     three clubs share, cannot carry one club's line into the others' rows.
  3. At least one number in the sentence, bare four-digit seasons excluded, must appear
     as a whole token in that search space, with the sign respected. Both ends of a
     hyphenated range count; a season span or an ISO date is blanked first, so its tail
     is never read as a number.

A sentence whose anchors reach no row in the cited table fails: that is a wrong table,
or a cell about a team or player the table does not carry.

What a clean exit proves: the citation resolves, the line is about a team or player the
line, its heading or its file name names, and at least one of the sentence's figures
sits in the rows of one of them. What it does NOT prove:

  - that a figure landed in the right column;
  - that the sentence's other figures are right, only that one of them is in the rows.
    A sentence carrying one correct figure passes with every other figure wrong;
  - that a figure belongs to the team it is written under when the line names two teams.
    Every team on the line contributes its rows, so on "<team A> allowed this,
    <team B> that" a team-B figure passes under either. That is deliberate: the
    coach and line profiles quote a coordinator's previous stop on the same line as his
    current one, and no rule of shape tells those two apart. Write one subject to a line
    when the attribution has to be checkable, and a line naming one team is now held to
    that team's rows.

The one gap left in that scoping: a capitalized word that is no player's name but does
match exactly one row is admitted as a name, and that row can belong to a team the line
never mentions. The column labels these tables use are listed as non-names, so it takes
an unlisted one to happen.

The check reads only the marker's own line, so a filled sentence and its marker have to
sit on one line; a sentence wrapped across two lines is checked on its second half
alone, and its subject and its other figures on the first line are never seen.

A number the pass computed rather than copied (a rank, a share, a per-game average) is in no row, so it carries no filled marker at all: it gets a parenthetical naming the table it was computed from, and this check never reads it.

A depth chart holds names and no meaningful numbers, so a citation naming one is checked
by player name only, searched across all 32 teams the print-all page carries, and its
numbers are not checked at all. A cited file counts as a depth chart only when its name
carries "depth-chart" AND fewer than one row in ten holds three or more numbers, so a
stats table cannot buy the exemption with its file name.

A citation shaped like a file name (no spaces, or carrying data/ or a file extension)
is a file citation even when a date appears in the name, so a misspelled or
extensionless file name fails instead of passing as a search fill. A citation carrying
an outlet and a date is a search fill: counted, never checked against a table.

A bracket carrying the word "filled" that is not a well-formed marker fails as a
malformed marker, and a set holding data tables but no well-formed marker at all fails
too, so a mis-shaped marker vocabulary cannot pass the check by hiding every cell from
it.

Prints the counts and every failing sentence; exits 1 on any failure, and when data/ is
missing, data/teams.md is missing or empty, or no profile was found. Run it from the
season folder:

    python3 check-fills.py --dir . --date 2026-09-03      one fill date
    python3 check-fills.py --dir . --date all             every fill marker in the set
"""
import argparse, glob, os, re, sys

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--dir', required=True)
ap.add_argument('--date', required=True, help='YYYY-MM-DD, or "all"')
a = ap.parse_args()
if a.date != 'all' and not re.match(r'^\d{4}-\d{2}-\d{2}$', a.date):
    raise SystemExit('--date must be YYYY-MM-DD or all')

data_dir = os.path.join(a.dir, 'data')
if not os.path.isdir(data_dir):
    raise SystemExit(f'no data/ folder under {a.dir}')
data_files = {os.path.basename(p): open(p, encoding='utf-8', errors='replace').read()
              for p in glob.glob(os.path.join(data_dir, '*')) if os.path.isfile(p)}
profiles = sorted(p for sub in ('teams', 'nfl', 'coach', 'oline') for p in glob.glob(os.path.join(a.dir, sub, '*.md')))
if not profiles:
    raise SystemExit(f'no profiles under {a.dir} (teams/, nfl/, coach/, oline/)')

date_pat = r'\d{4}-\d{2}-\d{2}' if a.date == 'all' else re.escape(a.date)
marker = re.compile(r'\[filled (' + date_pat + r'): ([^\]]+)\]')
# Every well-formed marker whatever its date, so that --date <one day> still sees that
# the set has markers elsewhere, and so a near miss can be told from a good one.
MARKER_ANY = re.compile(r'\[filled (\d{4}-\d{2}-\d{2}): ([^\]]+)\]')
# A bracket that meant to be a fill marker. "[gap fill <date>]" says "fill", not
# "filled", so it is left alone.
NEARMISS = re.compile(r'\[[^\]\n]*\bfilled\b[^\]\n]*(?:\]|$)', re.I)
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
# Something shaped like a file: a name carrying an extension, or any data/ path.
FILEISH = re.compile(r'(?:data/[\w./-]+|[\w][\w.-]*\.(?:md|csv|tsv|txt|json|html?))\b')
PATHY = re.compile(r'^[\w./-]+$')                       # a whole citation with no spaces
num = re.compile(r'(?<![\d-])-?\d(?:[\d,]*\d)?(?:\.\d+)?%?')   # leading minus kept, no trailing comma
YEAR = re.compile(r'^(?:19[5-9]\d|20[0-3]\d)$')         # a bare four-digit season
# The far end of a hyphenated range: "10-12 games" carries 12 as well as 10.
RANGE_END = re.compile(r'(?<=\d)-(\d(?:[\d,]*\d)?(?:\.\d+)?%?)(?![\d.,])')
# A season span or an ISO date is not a range, so it is blanked before the numbers are
# read and neither its tail nor its year reaches the search.
SPAN = re.compile(r'(?:19[5-9]\d|20[0-3]\d)-\d\d(?:-\d\d)?(?!\d)')
# A ". " ends a sentence unless it closes one of these abbreviations. "est" carries a
# word boundary so that "the highest. " still ends a sentence.
BOUNDARY = re.compile(r'(?<!vs)(?<!Jr)(?<!Sr)(?<!No)(?<!St)(?<!\bavg)(?<!\bapprox)(?<!\best)\. |\| |; ')

# The teams and every spelling the pulled tables use come from the knowledgebase's own
# data/teams.md, never from this script: one team per line, cells split on "|", the
# first cell the code the profiles use, the rest every other form a data file prints
# (another site's code, the city, the nickname, the full name). Lines starting with "#"
# or holding no "|" are ignored. The build writes that file before the first pull.
TEAMS_FILE = os.path.join(data_dir, 'teams.md')
if not os.path.isfile(TEAMS_FILE):
    raise SystemExit(f'no {TEAMS_FILE}: write it first (one team per line: CODE | spelling | spelling ...)')
SPELLINGS = {}
for raw in open(TEAMS_FILE, encoding='utf-8'):
    if raw.lstrip().startswith('#') or '|' not in raw:
        continue
    cells = [c.strip() for c in raw.strip().strip('|').split('|')]
    cells = [c for c in cells if c and not set(c) <= set('-: ')]
    if len(cells) < 2 or not re.fullmatch(r'[A-Z]{2,3}', cells[0]):
        continue
    if cells[0] in SPELLINGS:
        raise SystemExit(f'{TEAMS_FILE}: team {cells[0]} listed twice')
    SPELLINGS[cells[0]] = sorted(set(cells), key=len, reverse=True)
if not SPELLINGS:
    raise SystemExit(f'{TEAMS_FILE} holds no team lines (CODE | spelling | spelling ...)')
CODES = set(SPELLINGS)
# A word or phrase that names a team, mapped to its code: every non-code spelling.
WORD_TO_CODE = {f: c for c, fs in SPELLINGS.items() for f in fs if not re.fullmatch(r'[A-Z]{2,3}', f)}
# One pass that finds every team a line mentions, however the file spells it.
FORM_TO_CODE = {f: c for c, fs in SPELLINGS.items() for f in fs}
ANY_TEAM = re.compile(r'(?<![\w])(' + '|'.join(re.escape(f) for f in
                      sorted(FORM_TO_CODE, key=len, reverse=True)) + r')(?![\w])')
# Capitalized words that are never a player: headings, positions, sources, calendar.
NOT_A_NAME = {
    'Gap', 'Leak', 'Source', 'Sources', 'Season', 'Week', 'Weeks', 'Year', 'League', 'Team',
    'Teams', 'Draft', 'Sharks', 'Pro', 'Football', 'Reference', 'Sports', 'Analytics', 'Sharp',
    'Sumer', 'Next', 'Gen', 'Stats', 'ESPN', 'PFF', 'FTN', 'NFL', 'The', 'Athletic', 'StatMuse',
    'PlayerProfiler', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday', 'Full', 'Red', 'Zone', 'End', 'Rank', 'Note', 'Notes',
    'Passing', 'Rushing', 'Receiving', 'Defense', 'Offense', 'Coverage', 'Scheme', 'Snap',
    'Target', 'Targets', 'Play', 'Man', 'Zone', 'Blitz', 'Light', 'Heavy', 'Sub', 'Package',
    'Proxy', 'Context', 'Age', 'Projected', 'Whether', 'Which', 'Stated', 'Time', 'Rate',
    'Pass', 'Rush', 'Block', 'Stop', 'Win', 'Pressure', 'Pocket', 'Route', 'Routes',
    'Air', 'Yards', 'Attempts', 'Deep', 'Short', 'Motion', 'Shotgun', 'Empty', 'Screen',
    'Personnel', 'Down', 'Third', 'Neutral', 'Carries', 'Dropbacks', 'Share', 'Splits',
}
# A word inside a multi-word team spelling is never a player name, because on its own it
# reaches every other club that shares the word (a city word two clubs share, a
# direction word three clubs share).
TEAM_WORDS = {w for f in WORD_TO_CODE for w in f.split() if len(f.split()) > 1}
NAME_TOKEN = re.compile(r"\b[A-Z][a-zA-Z'.-]{2,}\b")
# The heading a bullet sits under names its subject when the bullet itself does not: a
# markdown heading, a bold-led bullet, or a plain label line ending in a colon, which is
# how the coach profiles introduce a benchmark unit ("<season> <team> under <coordinator>:").
HEADING = re.compile(r'^\s*(?:#{1,6}\s|[-*]?\s*\*\*[^*]+\*\*|[^-*#\s][^\n]{0,140}:\s*$)')
# Table lines that are prose, not data: a header, a source note, a column list, a rule.
PROSE = re.compile(r'^\s*(?:#|\|?\s*-{3,}|Source|Sources|Columns|Glossary|Note|Notes|Definitions)\b')


def cited_files(src):
    """Every data file a citation names, and what shape the citation has when it names
    none: "file" if it carries a path or an extension, "word" if it is a single token
    with no spaces, "prose" otherwise."""
    named = [f for f in data_files if re.search(r'(?<![\w.-])' + re.escape(f) + r'(?![\w-])', src)]
    if named:
        return named, 'file'
    if FILEISH.search(src):
        return [], 'file'
    if PATHY.match(src.strip()):
        # "ds-fantasy-points-allowed-2025" is a saved file missing its extension, not an
        # outlet: say so, rather than sending the writer looking for a date to add.
        if any(f.startswith(src.strip()) for f in data_files):
            return [], 'file'
        return [], 'word'
    return [], 'prose'


def is_depth_chart(name):
    """A depth chart is named for one and reads like one: names, not measurements. Every
    real table here carries three or more numbers on a third of its rows or more; the
    depth chart carries them on one row in four hundred. Without the second half of the
    test, renaming a stats file would buy it the no-numbers-checked exemption."""
    if 'depth-chart' not in name:
        return False
    rows = [ln for ln in data_files[name].split('\n') if ln.strip() and not PROSE.match(ln)]
    dense = sum(1 for ln in rows if len(num.findall(ln)) >= 3)
    return bool(rows) and dense * 10 < len(rows)


def is_search_fill(src):
    """A search citation carries an outlet and the source's date."""
    return DATE.search(src) is not None


def is_year(n):
    """A bare four-digit season. "1,979" carries a comma, so it is a measurement."""
    return ',' not in n and '.' not in n and '%' not in n and YEAR.match(n) is not None


def numbers_in(sentence):
    """Every measurement the sentence states. Both ends of a hyphenated range count, so
    "10-12 games" offers 10 and 12. A season span or an ISO date ("2023-24",
    "2026-09-03") is blanked first, so its tail is never read as the end of a range."""
    masked = SPAN.sub(lambda m: ' ' * len(m.group()), sentence)
    found = num.findall(masked) + [m.group(1) for m in RANGE_END.finditer(masked)]
    return [n for n in found if not is_year(n)]


def whole_number_in(n, table):
    """The number as a whole token: commas tolerated in the table, sign respected."""
    n = n.rstrip('%').replace(',', '')
    sign, digits = (n[0], n[1:]) if n.startswith('-') else ('', n)
    body = ',?'.join(re.escape(ch) for ch in digits)
    lead = re.escape(sign) if sign else r'(?<!-)'
    return re.search(r'(?<![\d.,])' + lead + body + r'(?![\d.,])', table) is not None


def anchors(line, file_code):
    """The player names and teams a stretch of text is about, plus the profile's own
    team. An all-capitals token is never a player here: the tables print names in
    mixed case, so OLB, ADOT and YBC are column and position labels, not names."""
    names = set()
    for w in NAME_TOKEN.findall(line):
        w = re.sub(r"'s$", '', w)
        if (len(w) > 2 and not w.isupper() and w not in NOT_A_NAME
                and w not in TEAM_WORDS
                and w not in WORD_TO_CODE and w.upper() not in CODES):
            names.add(w)
    codes = {w for w in re.findall(r'\b[A-Z]{2,3}\b', line) if w in CODES}
    for word, code in WORD_TO_CODE.items():
        if re.search(r'\b' + re.escape(word) + r'\b', line):
            codes.add(code)
    if file_code:
        codes.add(file_code)
    return names, codes


def name_rows(names, lines):
    return [ln for ln in lines
            if any(re.search(r'(?<![\w.-])' + re.escape(n) + r'(?![\w-])', ln) for n in names)]


ROWS = {}


def data_rows(named):
    """The cited files' data rows. A line naming three or more different teams is a
    league-wide list, not one subject's row (ESPN's player top twenties print twenty
    teams on one line), so it is split on "; " and only the entry carrying the anchor
    can be searched."""
    key = tuple(named)
    if key not in ROWS:
        out = []
        for c in named:
            for ln in data_files[c].split('\n'):
                if not ln.strip() or PROSE.match(ln):
                    continue
                if len({FORM_TO_CODE[m.group(1)] for m in ANY_TEAM.finditer(ln)}) >= 3:
                    out.extend(seg for seg in ln.split('; ') if seg.strip())
                else:
                    out.append(ln)
        ROWS[key] = out
    return ROWS[key]


def rows_for(names, codes, lines):
    """The data rows carrying one of the anchors. A player name and the team code are
    both searched: on a player table the name finds the row, on a team table only the
    code does, and a name that matches nothing simply contributes nothing.

    A name that several rows answer to is scoped to the teams the line names: it counts
    only where the row also carries one of those teams, however the file spells it, or
    carries no team at all. Without that, a common first name or surname on one team's
    line reaches every other player who shares it, on every other team, so a figure
    from a team the line never names passes. A name that answers to exactly one row in
    the table is already one player and needs no tie-break, which is what lets a surname
    on its own find a benchmark player on the club the line is comparing against. When
    the line names no team at all there is nothing to scope to, and every name stands
    alone."""
    # Longest spelling first, one pass: a short spelling that is also the start of another
    # team's spelling never claims that other team's row.
    by_code = [ln for ln in lines if any(FORM_TO_CODE[m.group(1)] in codes for m in ANY_TEAM.finditer(ln))]
    coded = {id(ln) for ln in by_code}
    by_name, seen_name = [], set()
    for n in names:
        hit = name_rows([n], lines)
        solo = len(hit) == 1
        for ln in hit:
            if id(ln) in seen_name:
                continue
            if not codes or solo or id(ln) in coded or not ANY_TEAM.search(ln):
                seen_name.add(id(ln))
                by_name.append(ln)
    how = 'name+code' if by_name and by_code else ('name' if by_name else 'code')
    seen, rows = set(), []
    for ln in by_name + by_code:
        if id(ln) not in seen:
            seen.add(id(ln))
            rows.append(ln)
    return rows, how


def sentence_before(line, pos):
    """The sentence holding the marker: from the last boundary before it, stepping back
    exactly one more boundary when that slice carries no figure at all, which is what a
    marker placed after the closing period or after a trailing caveat looks like. One
    step, never the whole line: a second sentence must not borrow the first one's number."""
    starts = [0] + [b.end() for b in BOUNDARY.finditer(line, 0, pos)]
    s = line[starts[-1]:pos]
    if not re.search(r'\d', s) and len(starts) > 1:
        s = line[starts[-2]:pos]
    return s


def team_code_of(path):
    """The team a profile is about, from teams/<CODE>.md, coach/<CODE>-defense.md, oline/<CODE>.md."""
    stem = os.path.basename(path)[:-3]
    head = stem.split('-')[0].upper()
    return head if head in CODES else None


data_fills = search_fills = bad_cite = no_num = bad_num = no_anchor = 0
malformed = markers_any = gaps = unverified = verified = 0
failures = []
for p in profiles:
    rel = os.path.relpath(p, a.dir)
    file_code = team_code_of(p)
    text = open(p, encoding='utf-8').read()
    gaps += len(re.findall(r'\(Gap\b', text))   # (Gap) and (Gap: <reason>) alike
    unverified += text.count('[unverified')
    if a.date != 'all':
        verified += text.count(f'[verified {a.date}]')
    heading = ''
    for line in text.split('\n'):
        if HEADING.match(line):
            heading = line
        good = {g.start() for g in MARKER_ANY.finditer(line)}
        markers_any += len(good)
        for n in NEARMISS.finditer(line):
            if n.start() not in good:
                malformed += 1
                failures.append(f'{rel}: malformed fill marker, use [filled <date>: <source>]: {n.group()[:100]}')
        for m in marker.finditer(line):
            src = m.group(2).strip()
            named, shape = cited_files(src)
            if not named:
                if shape == 'file':
                    bad_cite += 1
                    failures.append(f'{rel}: cites a data file that does not exist: {src}')
                elif shape == 'word':
                    bad_cite += 1
                    failures.append(f'{rel}: citation is one word and names no file under data/; '
                                    f'a search fill needs an outlet and the source date: {src}')
                elif is_search_fill(src):
                    search_fills += 1
                else:
                    bad_cite += 1
                    failures.append(f'{rel}: citation names neither a file under data/ nor an '
                                    f'outlet with the source date: {src}')
                continue
            data_fills += 1
            sentence = sentence_before(line, m.start())
            joined = '\n'.join(data_files[c] for c in named)
            shown = ', '.join(named)
            if all(is_depth_chart(c) for c in named):
                names, _ = anchors(line + ' ' + heading, file_code)
                if not any(re.search(r'(?<![\w.-])' + re.escape(n) + r'(?![\w-])', joined) for n in names):
                    no_anchor += 1
                    failures.append(f'{rel}: no player name from the sentence is in {shown}: {sentence.strip()[:140]}')
                continue
            numbers = numbers_in(sentence)
            if not numbers:
                no_num += 1
                failures.append(f'{rel}: no number in the filled sentence: {sentence.strip()[:140]}')
                continue
            names, codes = anchors(line + ' ' + heading, file_code)
            rows, how = rows_for(names, codes, data_rows(named))
            if not rows:
                no_anchor += 1
                failures.append(f'{rel}: no team code or name from the sentence is in {shown}: {sentence.strip()[:140]}')
                continue
            space = '\n'.join(rows)
            if not any(whole_number_in(n, space) for n in numbers):
                bad_num += 1
                failures.append(f'{rel}: none of {numbers[:6]} in the {how}-anchored rows of {shown}: {sentence.strip()[:140]}')

if markers_any == 0 and data_files:
    failures.append(f'{a.dir}: data/ holds {len(data_files)} table(s) but no [filled <date>: <source>] '
                    f'marker was found in any profile')

print(f'data fills: {data_fills} (missing cited file: {bad_cite}, no number in sentence: {no_num}, '
      f'no anchor row in cited table: {no_anchor}, number not in anchored rows: {bad_num}); '
      f'search fills: {search_fills}; malformed markers: {malformed}; (Gap) markers left: {gaps}; '
      f'[unverified] left: {unverified}' + (f'; [verified {a.date}]: {verified}' if a.date != 'all' else ''))
for f in failures:
    print(' FAIL', f)
sys.exit(1 if failures else 0)
