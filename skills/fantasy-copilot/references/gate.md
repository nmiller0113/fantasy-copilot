# The pre-delivery gate

Written rules about reading every signal and checking every pull did not fire on their own: a
pick was made from one sorted column while other columns in the same rows pointed elsewhere,
and a pull that silently missed one team fed a "no trade clears the bar" answer that a reviewer
then confirmed from the same broken file. The gate makes those two failures mechanical rather
than remembered. Every in-season call (start, sit, add, drop, claim, trade) reaches the user
only as a block the gate printed, and the plugin's Stop hook blocks any reply that carries a
call outside such a block.

The scripts live in the plugin's `scripts/` folder: `gate.py` (check, board, render, hook) and
three page collectors for a Yahoo Fantasy plus Draft Sharks setup (`gate-collect.js`,
`gate-gp-collect.js`, `gate-ds-collect.js`). Everything about the user (league ids, roster
slots, holds, team names, name aliases, pass data) lives in a private gate home outside the
plugin: the folder named by the `FANTASY_GATE_HOME` environment variable, or `.fantasy-gate`
in the user's home folder. With no gate home the hook does nothing.

## The gate home

- `leagues.json`: per league key, the host league id, the user's team id, the Draft Sharks
  league id, the league size, the starting slots in order, the active roster limit (`roster`:
  starters plus bench, injured reserve excluded; an empty starting slot is not an open spot),
  the playoff format (`playoffs`: playoff teams, playoff weeks, consolation places), and the
  aliases a chat message may use for it.
- `holds.json`: the user's holds, each with the league, the player, the kind (`drop`, `trade`
  or `both`), the user's own words, and an active flag.
- `teams.json`: each NFL team code with its nickname and city, because a host may name a
  defense either way and a hold on one must match the other.
- `aliases.json` (optional): name spellings that differ between the host and the engine.
- `config.json`: `passes` (the folder for pass data, default `passes` in the gate home) and
  `reader` (the command that copies the browser's saved collector output into a folder; it
  receives the key prefix, the output folder and the site origin), and optionally `tz` (the
  time zone that decides a pass's date; local time otherwise).

## A pass

1. `gate.py open WEEK` creates the pass folder for today.
2. Collect. Host tab: set the collector's config object and paste `gate-collect.js`, then
   `gate-gp-collect.js` (games played, once per pass, since it is the same in every league).
   Engine: sync each league in the tab first (the sync runs only in the top-level page), then
   paste `gate-ds-collect.js`. For a trade, read the engine's trade value chart for that league
   into the pass's data folder. Every fetch is checked and retried, team ids come from the
   league's own team list, the standings (rank, record, points) come from the league page, and
   every league ends with coverage lines: nothing incomplete is saved silently.
3. `gate.py ingest` copies the collector output into the pass; a missing league fails.
4. `gate.py check` refuses the pass on any failed coverage line, a team count that differs from
   the league size, a section under its row floor, a stale engine sync, an engine roster that
   differs from the host roster, or a rostered player with real points and no games played. A
   failure is re-pulled, or the call that depends on it goes to the user as INCOMPLETE, naming
   the gap. It is never answered from partial data.
5. `gate.py board LEAGUE` shows the lineup holes and, for each, the bench plus the top free
   agents on every signal: the host's week and rest-of-season projections, the engine's week
   and rest-of-season projections, and last-four and season points per game. A missing value
   prints `?`, never zero. No single sort decides a candidate list.
6. Write one role card per player for the pass (as-of date, role line, the sources actually
   read) and a calls file per league: moves, lineup, fallbacks for questionable starters,
   overrides with reasons, holds lifted in the user's words, a trade with the partner's reason,
   and optionally a one-line reason per pick (`why`) and conditions to watch (`if`).
   One card per player means the same evidence in every league.
7. `gate.py render LEAGUE [NAME]` fails with a list of problems or prints the block ending
   `gate ✓ NAME <hash>`. The block is short: what the user clicks and by when, the lineup with
   changes marked, the conditions, and one line of reason per pick (the `why` text, or the week
   signals when none is given), naming any player the signals favored over the pick. Every signal, role card and override reason goes to
   `renders/NAME.txt`, which the block names. The block is pasted to the user verbatim, one
   league per message.
8. `gate.py watch` writes the pass's watch list (`watch.md`) and prints it as a stamped block:
   every waiver player who beats the user's weakest droppable bench player on both engines rest
   of season (a kicker or defense: the starter, both engines this week), with his arrival date,
   the user's waiver priority and the share of leagues that roster him; every condition and
   fallback from the delivered calls; and the pending claims. Each waiver row gets an explicit
   claim-or-wait call with its priority cost: a player with real production does not reach free
   agency. Then set reminders at each arrival and at the final injury reports.
9. `gate.py trades LEAGUE` for every league: trade potentials with every rival, never cut by a
   fixed number, each with both sides' gains this week, over the next four weeks, in the playoff
   weeks and rest of season (the weeks until the playoffs replace the next four when the format
   is set), each player's trade value and projection side by side, both sides' place in the
   playoff race with a contender's cushion, the other manager's weakest
   starters ranked against the league and what the deal does to them, and the engine's trade
   value where the league's chart is in the pass. Four ranked lists: best for both rest of
   season, best for both this week, sell to teams in a playoff spot (your weeks until the playoffs
   against their playoff weeks: a stashed star who returns for the playoffs is worth most to
   them), and buy from teams below the playoff line (your playoff weeks against their weeks
   until the playoffs). Leads are not calls:
   a lead reaches the user only through a calls file and `render`, after the chart, role cards
   and the partner's reason are in.
10. `gate.py close` marks the pass finished.

Two planning rules hold in `trades` and in every trade render. A pending claim the user is
certain to win (they hold waiver priority 1) counts as landed, so nothing waits on the day it
processes. And trade math runs week by week: each player scores his projected rate except in his
bye week, where the bench fills the slot, so a bye is never compared as a zero.

## What render refuses

An unfilled starting slot; a starter on bye or out; a questionable starter with no fallback; a
flex starter who kicks off before a starter he could swap with; an add that is not a free agent
(or a waiver claim flagged as one); a held player dropped or traded; a roster over capacity;
any add while an IR slot holds an untagged player; a contested starter or an add who loses most
of the shared signals to an available alternative, or a kicker or defense a free agent beats on
both engines, without an override that names the alternative and says why; too few signals
present for a pick; a role card missing, unsourced or stale; and a trade without both lineups
recomputed, the engine's trade value for every player, roster room, and a written reason the
other manager would say yes. No gain or value cutoff refuses a trade: the block shows both
sides' gains on every horizon (this week, the weeks until the playoffs or the next four, playoff
weeks, rest of season), each player's values side by side, who pays more on the engine's value, the other manager's needs
as computed, and a flag for any questionable player the user would send.

## The Stop hook

The hook reads every text block of the turn, verifies each stamped block against the renders
on file (an edited block fails; the watch list is stamped too), and looks for call lines
elsewhere once a league is named, trade-lead lines included. A
hit blocks the reply; the next reply is judged on its new text and must say the earlier text
was not a checked call, or carry a stamped block or an INCOMPLETE note. After three blocks in
a row it lets the reply through with a warning to the user. It cannot catch complete but wrong
data, a wrong role card, a call written without a verb and a position, or judgment errors.
