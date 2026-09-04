# The knowledgebase: template, build, refresh, search

Read this when building or refreshing the knowledgebase described in section 10 of the
skill. It is not needed at the clock; at the clock the files are searched, not this page.

## Where it lives

Beside the user's private document, under the user's control, never inside this skill:

    kb/<season>/
      README.md                       structure, vocabulary, refresh procedure
      refresh-log.md                  one line per refresh: date, trigger, what changed
      data/                           the source tables, saved as pulled, one file per table
      teams/<CODE>.md                 one dossier per NFL team, same headings in every file
      nfl/availability.md             everyone not fully available, with replacement plan
      nfl/successor-map.md            PRIMARY / COMMITTEE / UNSETTLED per RB, WR, TE starter
      nfl/rookies.md                  rookies and young players behind veterans
      nfl/hype-and-reports.md         last 14 days of reporting and hype, by team, labeled
      nfl/suspensions.md              suspensions, exempt list, open reviews and appeals
      nfl/coaching-and-scheme.md      play callers, scheme, stated touch philosophy
      nfl/coach-tendencies.md         player scheme fit: bounceback, step-forward, downgrade
      nfl/defense-tendencies.md       DEF/ST units, what each defense gives up by position
      coach/<CODE>.md                 head coach and play caller tendency profile, numbers
      coach/<CODE>-defense.md         defensive coordinator profile, special teams if any
      oline/<CODE>.md                 offensive line profile: starters, numbers, impact
      nfl/offensive-lines.md          line ranking, who benefits, who is exposed
      nfl/schedule.md                 the season schedule, every team, every week
      nfl/defense-ratings.md          each defense rated soft/average/tough per position
      nfl/defense-injuries.md         key defenders out or limited, what each one softens
      schedule/<CODE>.md              the team's weekly matchup table by position
      nfl/schedule-strength.md        softest and toughest by position, season and windows

"League" in these files means the NFL; the user's fantasy league is never mixed in.

## Team dossier template

Every team file carries these headings, in this order, so a search lands in the same
place in every file:

    # <CODE> <Team> - <season> state (refreshed <date>)
    ## Coaching and scheme
    ## QB room
    ## RB room            (ends with a "Plan for absences" paragraph)
    ## WR room            (ends with a "Plan for absences" paragraph)
    ## TE room
    ## Availability: injuries, designations, absences     (a table)
    ## Rookies and successors behind veterans
    ## Media read (refreshed <date>)
    ## Hype and reports (last 14 days)
    ## Watch list
    ## Sources

Per player, in the rooms: name, age, role (lead, committee, passing downs, goal line,
backup), status and designation with the date applied, injury detail and timeline with
the outlet, expected share and its source.

The availability table: Player | Pos | Status or designation (date) | Injury | Timeline
(report, date, outlet) | Coach plan (quote of at most 12 words, speaker, date, outlet) |
Replacement and PRIMARY / COMMITTEE / UNSETTLED.

Rookies and successors: for each young player behind a veteran, the veteran's age and
games missed in each of the last three seasons, the young player's draft capital, camp
and preseason usage, first-team reps, the reported share trajectory (rising, flat,
unknown), and a verdict: takeover likely this season, possible, unlikely, with the
source that drives it.

Media read: up-and-comers and what reporters say; coach statements on roles (speaker,
quote, paraphrase, date, outlet); preseason usage and rest (snaps, touches, first-team
reps, who was held out of the finale and what the beat writer inferred); sleeper,
breakout, bust and risk tags with the outlet count; full-role replacements versus
committees for every starter.

## Coaching tendency profiles (the whole staff, one set per team)

The staff is profiled whole: the head coach, the offensive coordinator or whoever calls
plays, the defensive coordinator, and the special teams coordinator when a change this
year touches a kicker or returner. A play caller's record is evidence of what he will
do with the players he has now, and the record is public: PFF, Sharp Football
Analysis, Fantasy Points, Sumer Sports, FTN, Next Gen Stats write-ups, and beat
writers quoting the coach. The profile separates
three things and labels each: what he DID at prior stops and last season here
(numbers, with the season, the team and the outlet), what he SAYS he will do here
(dated quotes), and what reporters PREDICT (labeled prediction). The numbers: pass rate;
running back concentration (whether his lead back got 65 percent or more of the
touches), RB target share and goal-line usage; WR1 target share and air yards, whether
two receivers were fantasy-relevant under him; TE target share and red-zone targets,
whether a TE finished top 12 under him; play-action rate, passing volume against league
average; red-zone pass versus run inside the 10. Optional, written only when a pulled
table holds them and omitted otherwise (never searched for, never marked): pass rate
over expectation, tempo, personnel groupings, slot versus outside, designed QB runs,
deep-ball rate.

The profile is player-first: it ends with one line per fantasy-relevant player (QB, top
four RBs, top five WRs, top two TEs) stating the fit and a direction, bounceback (usage
the old scheme depressed and this caller's history feeds), step-forward (a young or
secondary player the tendencies elevate), downgrade (a role his history does not
support) or unchanged, with the number or quote that drives it. The NFL-wide file
collects every non-unchanged line by direction and position, strongest evidence first,
and keeps a section for candidates driven by a prediction rather than a number.

The defensive profile carries the coordinator's scheme with numbers (front, man versus
zone, blitz and pressure rates, coverage shell, takeaways and sacks at prior stops),
what the scheme has historically given up by position (rushing and RB receiving, slot
receivers, tight ends, deep passing), the personnel changes on defense, the key
defenders with status (edge rushers, interior linemen, the top corners, safeties,
linebackers, each with the position group his absence softens: a CB1 out softens the
defense against receivers, an edge out eases pressure for the opposing quarterback and
line, an interior run-stuffer out softens it against backs), and two
player-facing outputs: the DEF/ST unit's direction for the season with its first four
opponents, and the effect on the team's own offense (a defense that gets off the field
adds possessions; a slow, bad one adds garbage-time passing volume). The NFL-wide
defense file is the matchup table a start/sit or streaming call reads alongside the
engine's projection, not ahead of it: one row per defense, what it gives up by
position, with the source season. Where a prior-stop number and a current dated quote
disagree, the source hierarchy below decides: the coach's words first.

## Offensive line profile (one per team)

The line is the layer between a coach's plan and a back's or quarterback's numbers,
and it is measured: ESPN pass and run block win rates, pressure rate and sacks
allowed, yards before contact for the backs, time to throw for the quarterback, and,
only where an article quotes them or the user holds the subscription, PFF pass-block
and run-block grades and FTN adjusted line yards and adjusted sack rate. The
profile carries the five projected starters with age and status, continuity (how many
of the five started together last season), the swing tackle and top interior backup,
last season's numbers with ranks, the 2026 changes (arrivals, departures, draft picks,
the line coach and run-game coordinator and whether they are new), preseason
reporting, and the direct impact one line per player: the lead back and his backup
(run blocking, yards before contact, goal-line push), the quarterback (pressure, sacks,
time to throw), and the pass-catchers through the quarterback (a pressured passer
throws short and quick, so slot and back targets rise and deep shots fall). The
NFL-wide file ranks the lines with the numbers behind the ranking, and lists who
benefits from a line that improved and who is exposed by one that declined. In a
weekly matchup the line's pass-block quality meets the opposing coordinator's pressure
profile; the two files are read together.

## Schedule strength by position

The schedule file holds every team's opponent for every week, built by two
independent fetches and reconciled. The defense-ratings file rates every defense
soft, average or tough per position (QB, RB, WR, TE), preseason from last season's
fantasy points allowed by position adjusted by the defensive profile's 2026 changes,
and in season from actual points allowed once four weeks are in (blended before
that), then adjusted for the week by the defensive-injuries file: every key defender
out, doubtful or newly on IR, with the position group his absence softens, so that a
defense's rating for THIS week can differ from its season rating and the difference is
the weakness to exploit. Each team's schedule file applies the ratings week by week and
counts the soft/average/tough matchups per position for weeks 1-4, mid-season, and
the playoff windows (weeks 15-17 for most leagues, 16-17 for four-team brackets); the
NFL-wide file lists the softest and toughest schedules by position for the season and
for each window, and carries the week-by-week grid. The team files and the NFL-wide
file are generated, not written: `scripts/schedule-tables.py` joins the schedule file
to the ratings file (Python 3.8 or later, no other dependency), so they are never
hand-edited and never produced by an agent. The script reads its team codes from
`data/teams.md`, the same file the validator reads, and stops with a message when the
file is missing; it carries no team of its own, and the rollup lists the codes in sorted
order. The script ships in the plugin's `scripts/` folder, beside the validator; copy it into `kb/<season>/` at the first
build, again after every plugin update (the plugin's copy is the source when the two
differ), and run it from there, `python3 schedule-tables.py --dir . --date <today>`,
adding `--week <coming week>` in season. If no Python is available, say so, report
the tables as not built, and leave them absent; an agent never writes them instead.
Both inputs keep the shapes the script reads. The schedule file: one table row per
team, the team code in the first cell, then exactly 18 cells, one per week, each
`@CODE`, `vs CODE` or `BYE` (one BYE per row), with any notes under a `## Notes`
heading. The ratings file: the team code alone in the Defense cell, one of the words
soft, average, tough in each rating cell, and the week's injury adjustments as a table
"Defense | Position | Season | Week N | Player out" under "## Week N injury
adjustments". The script stops with a message on any row it cannot read; it never
guesses. This is the weekly matchup input
and the season-long difficulty read for any player, read alongside the engine's
projection, not ahead of it; the Draft Sharks Strength of Schedule and Fantasy Points
Allowed tools are the overlay, read live for the week's numbers, and when they disagree
with the file the tool wins and the file gets a refresh line.

## Vocabulary

Status uses the host's words: healthy, questionable, doubtful, out, IR, IR-designated
to return, PUP, NFI, commissioner exempt, suspended (n games). A designation is a fact
with a date. "Expected to miss weeks" is a report and carries its outlet. A replacement
plan is PRIMARY (one man takes the whole role), COMMITTEE (a named split) or UNSETTLED,
and the file says which source made it so. Hype is labeled hype; reporting is labeled
reporting. Markers on a line: `[verified <date>]` a skeptic corrected it, `[unverified
<date>]` no dated source was found either way, `[gap fill <date>]` a critic round added
a fact that is not a number from a table, `[<date>]` a refresh changed it, `(Gap)` a
number or fact the pass could not reach (written in place of the number, never
omitted; a cell no public source will ever answer is deleted instead, see the
never-chased list under Source tables), `[filled <date>: <data file>]` a cell filled from a saved source table,
naming the file under `data/` with its extension, and `[filled <date>: <outlet>
<date>]` a cell filled from a dated search result. Any number copied from a table
carries the filled form, never `[gap fill]`. The check script tells the two apart by
shape, not by date: a citation with no spaces in it, or one carrying `data/` or a file
extension, is a file citation, so a misspelled, extensionless or wrongly dated file
name fails instead of passing as a search fill, even when the file's own name ends in
a date. The search form is counted and never checked against a table. Write the marker
exactly: a bracket carrying the word "filled" in any other shape (a missing colon, a
missing date, no source named at all) fails as a malformed marker, and a set whose
`data/` holds tables but whose profiles hold no well-formed marker fails as well, so a
drifted vocabulary cannot pass the check by hiding every cell from it.

The line a filled number sits on has to say whose number it is: the check finds the
row by the player's name or the team, taking both from the line, its heading and the
profile's file name, and a line naming neither fails. A heading here is a markdown
heading, a bold-led bullet, or a plain label line ending in a colon, which is how the
coach files introduce a benchmark unit ("<season> <team> under <coordinator>:"). Keep a
filled sentence and its marker on one line: the check reads only the marker's own line,
so a sentence wrapped across two is checked on its second half alone and its subject and
other figures on the first line are never seen. Write the number as the table
writes it, sign included. A number the pass computed rather than read (a rank, a
per-game average, a share) is in no row, so keep the table's own input beside it:
"22.2 percent play-action, 67 of 302" checks, while "22.2 percent" alone normally fails
and passes only where it happens to match some other column. Only one of a sentence's
figures has to land, so a sentence carrying one correct number passes with every other
number on it wrong: the check thins the wrong figures out over a set, it does not clear
any one line. And keep one subject to a line where the attribution matters, because the
script holds you to it: a name several players answer to reaches only the rows of a team
that same line names, or rows carrying no team, so a figure from a club the line never
mentions does not pass. A name only one row answers to is already one player, which is
how a surname on its own still finds the benchmark player under a different club's
profile. A line carrying two teams is checked against both, and neither
figure is pinned to its own team, so name the team beside the number when two are in
play.

## Source hierarchy for roles and usage

Strongest first. A coach's or general manager's statement, with the speaker, the date
and the outlet, quoted at most a dozen words verbatim and then paraphrased. Preseason
usage: snap and touch counts, first-team reps, and rest, because a young player held
out of the finale after playing earlier is a player the staff has decided on. Beat
reporting from the last two weeks. Themed article sweeps seeded with the season's
sleeper, breakout, bust, risky-pick and handcuff pieces from the major outlets and from
Draft Sharks' own advice pages, because the same name in three outlets says something
about what a draft room will do. Depth charts last: a depth chart is a list, not a
plan, and it says nothing about share. This hierarchy is for roles and usage only. For
value, projections and injury timelines, Draft Sharks stays the primary source (skill
section 6, step 9): its Injury Predictor, Shark Bites and rest-of-season projections
supply the numbers the dossier records next to the role.

## Source tables: pull the numbers before the profiles ask for them

A profile that needs a number should never send an agent to find it. The first build
of this knowledgebase wrote 439 cells reading "not reached", "paywalled" or "(Gap)"
because 130 agents each tried to fetch the same handful of tables through a fetch tool
that a bot check, a truncation cap or a sign-up gate stopped, while every one of those
tables was open to a signed-in browser or a plain page load. The fix is a step, not a
retry: pull each table once, save it under `data/` with its URL, pull date, season and
column order, and hand the profiles the file. Filling a cell from a saved table is
extraction, so it runs on the lower tier and is checked by a script that anchors each
filled sentence to the rows it should have come from, by player name or team, and
requires at least one of the sentence's numbers to be in those rows. A clean exit proves
the citation resolves, the line is about a team or player the cited table covers, and
one of the sentence's figures is in the rows of a team or player the line, its heading
or its file name names. A name several players answer to is held to the teams that line
names, or to rows carrying no team, so another club's figure cannot pass under it; a
name only one row answers to reaches that row wherever it sits, since one row is already
one player. It does not prove the figure came from the right column; and it does not
prove the sentence's other figures are right, only that one of them is in the rows, so
one correct figure carries a line past every wrong figure beside it. A line naming two
teams is checked against both, which is deliberate: a coach or line profile quotes a
coordinator's previous stop on the same line as his current one, and no rule of shape
tells those two apart. One subject to a line is what makes the attribution checkable,
and the script now enforces it for every other case. The number itself is read from the
table, not remembered.

What each table answers, and where it comes from (all read for a visitor or a Draft
Sharks subscriber on the pull date; check the page still loads before trusting the
list, because sites gate and ungate):

- Draft Sharks Fantasy Points Allowed (Tools, Intel): points allowed per game and
  adjusted percentage for every defense by position, seasons back to 2021. The second
  basis source under the defense ratings and the positional points-allowed split.
- Draft Sharks Historical Stats (Tools, Intel): per player by season and week range.
  Backs carry opportunity share, red-zone snap share and red-zone opportunities;
  receivers and tight ends carry target share, end-zone targets, average target
  distance and yards per route; quarterbacks carry dropbacks, air yards per attempt
  and QBR. Twenty-five rows load at a time and the Load More control is slow; the
  Player Name box answers a single lookup faster than paging.
- Draft Sharks depth charts (Tools, Intel; the print-all page holds all 32 teams,
  offense and defense): who is listed first. The weakest source in the hierarchy,
  never a rep count.
- Draft Sharks offensive line rankings (the annual article): all 32 lines ranked,
  with PFF grade ranks, ESPN win-rate ranks and adjusted sack rate ranks quoted for
  the top and bottom tiers.
- Pro Football Reference advanced passing, rushing, receiving and defense pages
  (free; the site runs a bot check that clears on its own in a browser and blocks a
  fetch tool): pressure rate, pocket time, blitzes faced, scrambles, RPO and
  play-action volume per quarterback; yards before and after contact and broken
  tackles per back; depth of target, YAC and drops per receiver; coverage numbers,
  missed-tackle rate and pressures per defender; the same at team level on the team
  advanced page.
- ESPN Analytics win rates (the annual leaderboard article, free): pass rush, run
  stop, pass block and run block win rate for all 32 teams with ranks, and the
  player top twenties.
- Sharp Football Analysis coverage schemes and defensive tendencies pages (free):
  man and zone rate, single-high and two-high rate, blitz, light and heavy box, sub
  package, all 32 defenses for the last completed season, published before the new
  season under the new season's date.
- Sumer Sports team defense (free): EPA per play, per pass and per rush, success
  rate, yards and touchdowns allowed, interception rate.
- Next Gen Stats passing leaders (free, but the page is a JS app that is blank to a
  fetch tool and renders in a browser): time to throw, completed and intended air
  yards, aggressiveness, air yards to the sticks, completion rate over expectation.
- TeamRankings team stat pages (free; 403 to a fetch tool, open in a browser): plays
  per game, pass play share, opponent plays per game, red-zone touchdown rate for and
  against, each with the prior season beside it.
- rbsdm.com team tiers (free JS app, browser only): offensive and defensive EPA per
  play and success rate.
- The same Pro Football Reference advanced pages for each earlier season a coach
  profile names (the play caller's prior stops): one pull per season, saved with the
  season in the file name, so a prior-stop cell is a copy and not a search.
- Pro Football Reference red zone pages (rushing, receiving, passing; free, browser
  only): every player's attempts or targets, yards, touchdowns and share of the team's
  plays inside the 20, inside the 10 and, for rushing, inside the 5. The goal-line and
  inside-the-10 split cells the first build marked subscription-only are here.
- Pro Football Reference fantasy rankings page, one per season for the last three
  (browser only): every fantasy-relevant player's age, games played and games started
  that season, with his team, so a veteran's games missed over three seasons and a
  player's age are a copy; the current season's page also carries carries, targets and
  receptions. Cut the tail at a stated points floor and say so in the header.
- Pro Football Reference season index and opposition pages, one per season for the
  last three (browser only): team offense (plays, yards per play, pass and rush
  attempts, sacks taken and sack rate, score rate) and team defense (plays faced,
  blitz, hurry, knockdown and pressure rates, sacks, pressures, missed tackles, depth
  of target faced, passer rating allowed). A play caller's or coordinator's prior stop
  is a row in the earlier season's file, so a coordinator cell is a copy too.
- rbsdm.com neutral pass frequency table (free JS app, browser only): early-down neutral-situation pass rate with
  dropback and rush EPA. The tab's season filter may not take; the header states the
  seasons the table actually covers and the profile cites that span. The
  pass-rate-over-expectation tab draws one team at a time as a chart and is not
  tabulated, which is why that figure is optional in the staff profile.

A page that answers a cell but returns 403, 404 or an empty body to the fetch tool is
read in the browser (Claude in Chrome or the user's own) and saved like any other
table; "unreachable by the fetch tool" is never a reason to leave a cell open. The
method that works: navigate to the page, run a page script that rewrites the document
body as one pipe-separated line per row built from the table's cells (the chosen
columns only, by their column keys), then read the page text and save it under a header
naming the URL, the pull date, the season, the row floor if the tail was cut, and the
column order. Three shortcuts fail and are not retried: a script that returns the table
as its own result (the return value is capped at about a kilobyte), a clipboard write
from the page (it hangs), and a request from the page to a local receiver (blocked
without an error). A site's own export controls are not used either; the page text is
the export.

Never chased, and never carried in a profile as a missing cell: a figure only a
subscription publishes (PFF grades beyond what an article quotes, FTN adjusted line
yards and DVOA, Fantasy Points Data, Sharp Football's book-only splits, Sumer Sports'
and Next Gen Stats' paid tiers: personnel groupings, alignment and route rates, tempo
and no-huddle rates, pass rate over expectation, designed-run splits, most deep-ball
rates), unless the user holds that subscription and says so, and a figure no outlet
prints (camp rep counts, preseason snap counts and shares). Where a free table happens
to hold one of these, it is copied like any other cell; where none does, the profile
simply omits it. A round that meets such a cell deletes it,
clause by clause when the line also holds a fact, and records the deletion in its
return value; a profile carries facts and cells a later round can fill, nothing else.
The owner's rule: good beats perfect, and a line that says a number is behind a paywall
is noise at the clock.

Two rules follow. A cell that says a number was not reached is a table not yet pulled,
not a search to run: pull the table, then fill. And a pulled table is data, saved
verbatim with its header; a profile cites the file and the season, never a memory of
the page, and `scripts/check-fills.py` (copied into the season folder like the
schedule script and run from there, `python3 check-fills.py --dir . --date <fill
date>`, or `--date all` for every fill) confirms that the cited file exists and that at
least one number in each filled sentence is in that file's rows for the player or team
the line, its heading or its file name names, and exits non-zero when either fails. One
number landing is the whole of it, so the check thins wrong figures out of a set without
clearing any one line. A citation naming a depth chart
is the one exception: a depth chart holds names and no meaningful numbers, so it is
checked by player name, searched across all 32 teams the print-all page carries rather
than scoped to the profile's own, and its numbers are not checked at all. That exemption is earned
twice over, so it cannot be borrowed: the file's name has to carry `depth-chart`, and
the file itself has to read like a depth chart, fewer than one row in ten holding three
or more numbers. Save the depth-chart pull under a name that carries `depth-chart`, and
save nothing else under one.

## Build (once, before the season)

0. Confirm the location with the user and get an explicit go-ahead (skill section 10);
   offer the NFL-wide cross-cuts alone as the starter set when the full build is more
   than the user wants. Write `data/teams.md` first: one team per line, the code the
   profiles use, then every spelling the tables to be pulled print for it (another
   site's code, the city, the nickname, the full name); the check script and the schedule script
   read their teams from that file and carry none of their own. Then pull the source tables
   above into `data/` before any profile pass starts, so no pass fetches one of those
   tables on its own (the season schedule in step 6 is fetched there, twice, by
   design).
1. One pass per team, in parallel where the harness offers subagents and one at a time
   where it does not, each writing the dossier from the hierarchy above. Ground rules
   for every pass: today's date and the Week 1 dates stated up front; sources from the
   last 14 days preferred and anything older labeled with its date; no preseason memory
   presented as current without a dated source; no fantasy advice, no projections, no
   guessing (missing facts go under a Gaps note); a time box.
2. A skeptic pass per team: the 6 to 12 highest-impact claims (named starters,
   designations, timelines, primary-versus-committee plans, suspensions) re-searched
   independently, each returned as confirmed, contradicted with a correction, or
   unverified; the default when uncertain is unverified, never confirmed.
3. A patch pass applies the corrections in place and marks unverified lines.
4. The NFL-wide survey files (availability, successor map, rookies, hype, suspensions,
   coaching and scheme) are built independently of the dossiers, so they can disagree
   with them; a disagreement there is a finding, not an error to smooth over.
5. The staff and line profiles, one pass per team each: the head coach and play
   caller to `coach/<CODE>.md`, the defensive coordinator to
   `coach/<CODE>-defense.md`, the offensive line to `oline/<CODE>.md`. Each profile
   set then rolls up into its NFL-wide file or files (coach-tendencies,
   defense-tendencies, offensive-lines) with a skeptic on the rollup's strongest
   claims. A rollup compiles its own per-team files, so a disagreement between the two
   is an error to fix, not a finding.
6. The schedule and the defenses: two independent fetches of the season schedule,
   reconciled slot by slot into `nfl/schedule.md`; the defensive-injuries file from
   the profiles' key-defender lists and the current designations; then the defense
   ratings file from last season's points allowed by position, adjusted by the
   defensive profiles and by the injuries already known; then `scripts/schedule-tables.py`
   writes each team's weekly matchup table (`schedule/<CODE>.md`) and the NFL-wide
   schedule-strength rollup from those two files.
7. A critic reads the whole set and lists what is missing or thin, most severe first;
   a gap round fills the high and medium items, from the saved tables first (marked
   `[filled <date>: <data file>]`) and by search second, then `scripts/check-fills.py`
   runs from the season folder and must exit clean before the set is called complete.
   The gap rounds run this way, learned the hard way on the first build:
   - Select the files by what they say, not by the marker: a profile carries most of
     its missing facts as prose ("not found", "not retrieved", "not obtained") with no
     marker at all, so a selection on `(Gap)` alone skipped a third of the pool.
   - Progress is measured on that same yardstick, the count of lines that say a fact is
     missing, before and after; the marker count rises during a round because the
     round stamps unmarked prose, so it measures nothing on its own.
   - One agent per file per round, handed the previous round's open list with what it
     tried and why it failed, a fixed search budget, and two rules for a cell it cannot
     close: one on the never-chased list (Source tables) is deleted; one that waits on a
     statement not yet made, a game not yet played or a report not yet issued keeps its
     bare marker for the next round. A file gets another round only while its last round
     filled something.
   - The search tool's quota is per session; find the limit before the round and plan
     rounds inside it, across sessions when the pool is larger than one session's quota, and the browser-read tables above are
     pulled first so the searches go to facts no table holds.
   - The check script runs after every round, not only at the end, because extraction
     agents write undated citations, sourceless markers and bracketed notes that only
     the script catches; the marker grammar goes into every prompt verbatim.
   - An agent records what it tried in its return value, never in the profile: a
     profile line narrating a failed fetch is noise at the clock and is deleted, and so
     is a line narrating the tool budget ("search was unavailable", "budget exhausted"):
     it describes the pass, not the league; sources it lists move to the Sources section
     if they are not already there.
   - The yardstick is a script, `scripts/missing-lines.py` (copied into the season
     folder like the others; it creates `build/` when the folder is absent):
     `python3 missing-lines.py --dir . --write <label> --date <today>` prints the count, writes the file list for the round under `build/`, and
     writes one open-line list per file (line number and text) under
     `build/gap-fill-<label>-open/`. Every fill prompt names the agent's list and tells
     it to go to those lines. This is not optional: an agent handed a description of the
     forms matches the literal phrases and skips the rest (a five-file pilot returned
     zero fills; the same files with their lists returned dozens).
   - The prompt names every form a missing fact takes: the bare marker, any marker an
     older round wrote with a reason (re-checked against every table pulled since,
     because the reason is older than the table, then deleted or stripped to the bare
     form), the unverified marker, and the prose forms the script matches.
   - Pilot five files after any prompt change before the pool runs, and read the
     returns, not the counts: a return that says the file had nothing to fill is the
     prompt's failure until proven otherwise.
   - The table-copy pass and the search pass are separate runs of the fill agents, never
     one run that does both per file, so table copying spends no search quota and the
     search rounds get all of it; and the pass that adds basis sources to the ratings
     file runs once per build and never again (a second run appends a second copy).
   - After a new table is pulled mid-fill, the data stage runs again, before any search
     round, on the files whose open lines name what the table answers, selected by
     keyword from the open-line lists.
   - The round ends with `scripts/gap-list.py` (copied into the season folder like the
     others): `python3 gap-list.py --dir . --date <today>` writes
     `build/gaps-remaining-<date>.md`, every line the yardstick counts (markers with
     the reason beside them, unverified lines, unstamped prose), by file, and prints the
     totals, which equal the yardstick's; the report to the user quotes the yardstick before and
     after, the check script's line, and that file, never a marker-count table.
8. A media pass: themed sweeps (sleepers, breakouts, busts and risky picks, rookies and
   up-and-comers, preseason usage and rest, coach statements on roles, injury risk and
   timelines, handcuffs to own), each reading many whole articles, merged into every
   dossier's Media read section, then skeptic-checked.
9. README and the first refresh-log line.

## Refresh (a delta)

Weekly, the morning after the week's last game and before waivers clear; and before
every draft, lineup lock, trade decision, waiver or free-agent move, and roster move.

0. Re-pull the tables first, on their own cadence, before any collector or merge runs;
   each file in `data/` carries its pull date, so the stale ones are the ones to redo:
   weekly in season, every table that changes with the games (the advanced passing,
   rushing, receiving and defense pages, the team advanced page, the Next Gen Stats
   leaders, the pace and red-zone pages, the EPA and success-rate tables, the
   points-allowed-by-position table, the per-player usage shares, the depth charts);
   once a season, the annual articles (line rankings, win-rate leaderboards, coverage
   scheme rates) when they publish, and the prior seasons' fantasy rankings, season
   index and opposition pages (three seasons back, for ages, games missed and prior
   stops); never again, the prior-season pages once pulled. The current season's red
   zone, fantasy rankings, index and opposition pages join the weekly in-season list. A new season
   starts the same way the build does: `data/teams.md` first, then the annual and
   prior-season tables, then the in-season tables as soon as a week is played, and the
   previous season's in-season tables are kept under their season name because the
   coach and line profiles cite them as prior stops. The gap-round procedure under
   build step 7 is the same in a refresh: a merge that leaves cells open runs it, with
   the check script after every round.
1. Collect, once: a few collectors read the pages that cover all 32 teams (the
   transactions wire, the official injury report, the news feeds, the league's
   suspension announcements; in season also the week's line changes and the usage
   tables), each asking "what changed since <last refresh date>" under the build's
   ground rules, and return items tagged by team. Routing the items to teams is plain
   code.
2. Merge: per team, and per NFL file, an agent gets its routed items plus one targeted
   search of its own, "what changed since <last refresh date>" for the local reporting
   the wide net misses, same ground rules, same headings, editing in place and marking
   changed lines with the date. Verify: a skeptic re-checks every changed high-impact
   claim and applies corrections. Any cell a merge filled from a saved table carries
   `[filled <date>: <data file>]`, and `scripts/check-fills.py` runs after the merge
   with that date and must exit clean.
3. Usage check (in season): for every fantasy-relevant player, compare the week's
   actual snap share, carries, routes and targets (collected once from the box scores
   and the free league-wide tables, Next Gen Stats included, with PFF and Fantasy Points
   only where the user holds the subscription) against his caller's tendency profile and the
   direction the profile gave him, and mark the line confirmed, diverging or new (a role
   the profile did not predict). Two diverging weeks change the direction; one is noise.
   In-season calls read the comparison rather than the preseason profile, alongside the
   engine's projection and not ahead of it.
4. Schedule and defense update (in season): refresh the defensive-injuries file from
   the week's practice reports and designations (every key defender out, doubtful or
   on IR, and the position group his absence softens); re-pull the Draft Sharks
   Fantasy Points Allowed table for the current season into `data/` and refresh the
   defense ratings from its points allowed by position (blended with last season until
   four weeks are in) and write the injury adjustments for the coming week as the table
   the script reads; then run `scripts/schedule-tables.py` with the coming week, which
   re-rates every team's table and re-counts its windows; and edit the line profile,
   with its player impact, only for the teams whose collected items carry a line
   change (an injury to a starter, a position switch).
5. Overlay: for every player whose role changed, read the engine's current value and
   rest-of-season projection (war room or Team Dashboard) and write the gap between the
   new role and the number into the team's Watch list. That gap is the edge; it closes
   within days. Nothing is written back into the engine.
6. Log one line in refresh-log.md: date, trigger, what changed.

The pre-draft sweep in section 6 step 9 becomes: refresh, then search only for what is
newer than the refresh, within the step's own recency window, and read every target
against the successor map, the rookies file and the media read before it earns a band.

## Agents, models and scripts

A build or a refresh is many agent runs, and they are not all the same kind of work.
Three kinds, and what each runs on:

- **Judgment**: deciding what a source supports and marking a gap instead of guessing,
  turning a coach's words into PRIMARY or COMMITTEE, matching a scheme to a named
  player, rating a defense, and every skeptic pass. These run on the strongest model
  the harness offers, at its normal effort. A weaker model here produces plausible
  lines that are wrong, and a skeptic on a weaker model is a weaker check on the very
  thing the user is relying on.
- **Extraction**: transcribing a structured page that already covers all 32 teams (a
  transactions wire, an official injury report, a snap-count table) into items with
  team codes, comparing collected numbers to a stated direction, and filling a
  profile's cell from a saved source table found by grep. A lower tier does this as
  well as the strongest one; the two-week rule absorbs a single mislabel in the usage
  check, and `scripts/check-fills.py` checks each filled sentence against the rows of
  the table it cites for the player or team the line, its heading or its file name names
  (at least one of the sentence's numbers must be in those rows, which is why one right
  figure carries a line; a shared name is held to the teams the line names, so another
  club's figure does not pass; a depth-chart citation is checked by name instead,
  searched across all 32 teams). Give the tier the numbers; never make it
  fetch what a collector can hand it, and never let it read a data folder whole when a
  grep for the team code finds the row.
- **Joins**: anything derivable from two files that already exist (the schedule tables,
  the window counts, the matchup grid, any ranking by count). A script, never a model:
  it is exact, free, seconds instead of dozens of agents, and re-runnable every week.

Two shapes follow. Collect once, then route: a fact that covers the whole NFL is
fetched by one collector and handed to the per-team agents in their prompt, so 32
agents do not each search the whole week from scratch; each keeps one targeted search
for the local reporting the wide net misses. Edit only where something changed: a
profile set (lines, staff) is opened only for the teams whose collected items touch
it. Run one workflow at a time; several at once trip the API's rate limits and the
failures look like missing data. A failed agent call is retried once under a distinct
label and then counted as a gap in the report, never filled in.

## Search, do not browse

Any OS, run from `kb/<season>/`. Examples with a Unix shell and with PowerShell:

    grep -n "PRIMARY" nfl/successor-map.md
    Select-String -Path nfl\successor-map.md -Pattern "PRIMARY"

    grep -n -A2 "<player>" teams/<CODE>.md
    Select-String -Path teams\<CODE>.md -Pattern "<player>" -Context 0,2

    grep -n "PUP\|IR-designated\|exempt" nfl/availability.md
    Select-String -Path nfl\availability.md -Pattern "PUP|IR-designated|exempt"

Who eats if a starter is out: the successor map. Whether a young player is taking the
job: the rookies file. Whether a designation allows an IR slot: the availability list's
designation column, then the host's own row, which wins on disagreement.
