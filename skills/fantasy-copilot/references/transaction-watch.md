# Transaction watch: what every room did

Read this when running the transaction watch of skill section 8, on waiver eve or on
demand. It holds what a host's transactions page shows, how the rows are pulled, the
shape of the two files the script reads, and exactly what the report prints. Its last
section, the waiver-run window, is the one part read at a clock: the flip.

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

Four sections, markdown to standard output, and nothing else. Every date in every section
is printed as its weekday and ISO date, `Sat YYYY-MM-DD`, so a date is never read off by a
day or paired with the wrong weekday; quote it that way when saying it.

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
  added in the same transaction (`-` when the drop was bare) and the date he arrives,
  `arrives <Wkd date>`, which is the drop date plus that league's waiver days plus one.
  The plus one is the host's rule, verified on one host; a league on another host compares
  that host's label on one waived player to the computed arrival once before the estimate
  is trusted there. The waiver period does not start at the drop: it starts the following
  calendar day in the host's time zone, runs the league's waiver days, and the host's
  overnight run the MORNING AFTER it ends hands him to the winning claim; unclaimed, he is
  a free agent from that run, or from the flip at the period's end where the host has one
  (The waiver-run window, below). So with two waiver days the arrival is the drop date
  plus three days whatever the clock time of the drop, and the host's own status label on
  a player still on waivers shows this same arrival date. It is still arithmetic on the
  waiver-days cell, not the host's processing, so the host's row governs the real cost
  and date (skill section 8's replaceability test). When a later add of the same player
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
    python3 transactions.py --drop YYYY-MM-DD --days N

The last is the one-date mode: no files, no `--dir`, one drop date and that league's
waiver days in, four lines out, `today`, `dropped`, `on waivers <first> through <last>`
(`on waivers: none` when the days are 0) and `arrives <date> at the host's overnight
run`, each date with its weekday. Use it for every date said about a waiver window,
instead of counting days in prose. `--days` is a whole number 0 to 7 and is required with
`--drop`; `--since` and `--league` belong to the report and are refused with it, as
`--days` is refused without it, since the report reads each league's waiver days from
`leagues.md`.

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

## The waiver-run window

Where the host flips unclaimed players to free agency at the moment the waiver period
ends, ahead of the run that settles the claims, that gap is its own pass and not the
tail of the claim pass. Two readings are taken in it, both of every league and neither
of a subset.

The arrival date the script prints does not move, since the flip and the run fall on the
same morning; this section orders the two within it: skill section 8's "a claim until that
waiver period ends" is this flip where the host has one, and the run where it has none.

**The pool is re-read for every league at the flip, however settled a league looked
before it.** A pool read even an hour earlier is stale: the flip moves every
unclaimed player off waivers into the free-agent pool at once, so the best player at a
position can enter a league's pool at that moment and, with every manager's adds landing
in the same minutes, be gone minutes later. Skipping the leagues whose first choice was already
taken, and re-reading only the rest, misses that arrival in the leagues that were
skipped. The read asks the host for free agents only, never the availability filter that
also returns players still on waivers, since those cannot be added now and reading them as
available is how a name gets recommended that the user cannot click.

**The team's own pending block is read before any add or drop is named in that league.**
A player already committed as the drop on a filed claim cannot be dropped a second time,
so naming him is an error the user discovers only as a refusal at the host. The block is
read from the host's team page in the same pass as the pool, and every player it holds
as a drop is treated as unavailable until the run resolves, unless the claim holding him
is named for cancellation in the same line, which is the user's click. This applies most sharply to
the assistant's own claims from earlier the same evening: a roster the assistant changed
itself is still state to be re-read, not state it can recall.

Where one league's room has repeatedly moved faster than the others, that league is
worked first in the window rather than in list order, and which league that is belongs
in the private document beside the manager who makes it true.

The same pass names every starting slot the host shows empty. A claimed or added kicker
or defense arrives on the bench, and a slot left empty scores nothing, which costs more
across a portfolio than any single add in the window gains. `references/lineups.md` holds
what then goes in each slot, and its "Saying the number" governs every comparison this pass
offers, the pool's board as much as the lineup's. The engine's raw projection for each pool
name is the one the waiver-eve Finder read already holds, since the flip moves availability
and not projections, unless the engine's news feed shows an item on him since that read, in which case his
Finder number is re-read;
the host's number is this pass's own.
