# Transaction watch: what every room did

Read this when running the transaction watch of skill section 8, on waiver eve or on
demand. It holds what a host's transactions page shows, how the rows are pulled, the
shape of the two files the script reads, and exactly what the report prints. It is not
needed at the clock.

## Where the files live

Beside the user's private document, under the user's control, never inside this skill:
one folder holding `leagues.md` and one `<slug>.md` per league. The user names that
folder in the private document (skill section 9), as the knowledgebase's location is
named there. League slugs, manager names and hosts live in those files and nowhere in
this plugin. The manager name written in `leagues.md` must be spelled as the host page
spells it, because that string is what marks the user's own rows.

## What the host's transactions page shows

Observed on one host, in the league's transactions view:

- one entry per transaction, carrying the added player's name, his NFL team, his
  position and the designation tag the host prints on the row (an IR or PUP style tag),
- the type of the move: free agent, waiver, or trade,
- the dropped player inside the SAME entry, marked as going to waivers,
- the manager who made it, and a timestamp,
- filters for added, dropped, trades and pending waiver offers, and an all-teams
  selector.

Hosts redesign these pages, so read what the page actually shows before trusting that
list, and pull with the all-teams selector on: the point of the pull is every room's
moves, not the user's.

## The pull

One pull per league, by the browser method the knowledgebase uses for a page a fetch
tool cannot read (`references/knowledgebase.md`, source tables): navigate to the
league's transactions page with all teams selected, run a page script that rewrites the
document body as one pipe-separated line per player movement, read the page text, and
append those lines to that league's file. A page script that returns the table as its
own result is capped at about a kilobyte, which is why the page text is what gets read.

Pull since the last pull, and let the pulls overlap rather than hunting for the seam:
within a league's file the script de-duplicates on timestamp, manager, movement and
player, keeping the first of the repeats.

One host entry that adds one player and drops another is TWO rows sharing one txn value.
That shared value is what pairs a drop with the add it made room for, so it is the cell
to get right. The host prints no such id, so the puller MAKES one: the timestamp, the
manager, and a SUFFIX whenever the page shows more than one of that manager's entries in
that minute. Waiver processing does exactly that, running a manager's claims in one
batch stamped with one minute, so the suffix is the normal case on waiver morning and
not an edge case. Any string does, as long as every row of one host entry carries it and
no other row in the file does.

The script holds the puller to it: a txn is required, is never `-`, belongs to one
timestamp, carries the adds and drops of one manager, and holds at most one `ADD` and at
most one `DROP`, because a host entry adds one player and drops at most one. Two of a
manager's claims left under one id would print an add the drop never paid for. A trade
is the one entry that spans two managers, so its rows share a txn and only the timestamp
is held.

A trade is one row per player per side: a one-for-one trade is two rows under one txn, a
`TRADE-OUT` under the manager giving the player up and a `TRADE-IN` under the manager
receiving him. A two-for-one is three rows, still one txn.

## The two files

`leagues.md`, one row per league, `#` lines and blank lines ignored:

    slug | the user's manager name in that league | waiver period in days | host

`<slug>.md`, one row per player movement, same skipping:

    YYYY-MM-DD HH:MM | manager | movement | player | pos | nfl team | designation | source | txn

Movement is `ADD`, `DROP`, `TRADE-IN` or `TRADE-OUT`. Source is `FA`, `W`, `TRADE` or
`-`. Designation is the host's tag or `-`. Every cell is written; a cell the page leaves
blank is written `-`, never left empty. The exception is txn, which is required, is
never `-`, and is unique to one host entry: it is the pairing key, and an id shared by
two entries would print a swap nobody made.

## What the report prints

Four sections, markdown to standard output, and nothing else:

- `## Managers`, one table per league in scope: manager, adds by position, drops by
  position, swaps, last move date. Counts only. The adds and drops columns count `ADD`
  and `DROP` movements; a trade movement counts in neither and moves only the last move
  date. Swaps is the number of that manager's transactions in the window holding both an
  `ADD` and a `DROP`. The user's manager row is marked `(you)`. Managers are ordered by
  how many adds and drops they made, then by name, and a league with no rows in the
  window says so.
- `## Dropped (all leagues)`, one row per player dropped in the window: player, pos,
  team, designation, the count of leagues he was dropped in, and one entry per drop
  giving the slug, the date, the manager (with `(you)` when it was the user), the player
  added in the same transaction (`-` when the drop was bare) and an estimated clear
  date, which is the drop date plus that league's waiver days and nothing else: it is
  arithmetic, not the host's own processing, so the host's row governs the real cost and
  date (skill section 8's replaceability test). When a later add of the same player
  appears in that league, the entry ends "(since added by <manager> on <date>)", naming
  the first add after that drop, so a name already off the wire reads as one. The pos,
  team and designation shown are the ones on his most recent drop row. Sorted by that
  league count, then most recent first.
- `## Added in 2+ leagues`, one row per player added in two or more leagues by managers
  other than the user: player, pos, team, and one entry per add giving the slug, the
  date, the manager and that row's source cell. The user's own adds are left out of the
  count and out of the entries, because the section is the market's read and the user
  stashing one name in every league he plays is his own move, not the room's. A player
  the user added in one league and another manager added in a second counts once and is
  therefore not shown.
- `## Yours`, one table per league in which the user's own manager has an add or a drop
  in the window, most recent first: date, movement, player, pos, team, designation,
  source. Trade movements are not in it, and when no league holds one of the user's own
  adds or drops the section says so.

The report surfaces what the rooms did. It does not rate, rank or recommend, and no
count in it is a statement about a player's value: that is the full read and the
engine's number (skill sections 8 and 10).

## Running it

    python3 transactions.py --dir <the private folder>
    python3 transactions.py --dir <the private folder> --since YYYY-MM-DD
    python3 transactions.py --dir <the private folder> --league <slug>

Python 3.8 or later and nothing else. The script ships in the plugin's `scripts/`
folder; copy it beside the private files, as the knowledgebase's scripts are copied into
its `build/` folder, and copy it again after every plugin update.

Without `--since` the window opens seven days before the newest row that run read, so
`--league` also narrows the default window to that league's own newest row. `--since` is
inclusive and takes rows dated on or after it.

Every line the shape cannot read stops the run with the file and the line number,
nothing guessed and nothing written: a league row that is not four cells or a movement
row that is not nine, a slug that is not letters, digits, hyphen or underscore, waiver
days that are not a whole number, a duplicate slug, a timestamp that is not
YYYY-MM-DD HH:MM or not a real date and time, a movement or source word outside the
lists above, an empty cell, a txn of `-`, a txn already used by another timestamp or by
another manager's adds and drops, a txn given a second add or a second drop, and a line
that is neither a pipe row nor a `#` comment.

Two more stop the run without a line number, since neither is a line: a `--league` slug
that `leagues.md` does not hold, which prints the slugs it does, and a league file that
is not there.
