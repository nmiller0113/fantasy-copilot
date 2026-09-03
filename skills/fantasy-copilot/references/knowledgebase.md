# The knowledgebase: template, build, refresh, search

Read this when building or refreshing the knowledgebase described in section 10 of the
skill. It is not needed at the clock; at the clock the files are searched, not this page.

## Where it lives

Beside the user's private document, under the user's control, never inside this skill:

    kb/<season>/
      README.md                       structure, vocabulary, refresh procedure
      refresh-log.md                  one line per refresh: date, trigger, what changed
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
(dated quotes), and what reporters PREDICT (labeled prediction). The numbers: pass rate
and pass rate over expectation; tempo and personnel groupings; running back
concentration (whether his lead back got 65 percent or more of the touches), RB target
share and goal-line usage; WR1 target share and air yards, slot versus outside, whether
two receivers were fantasy-relevant under him; TE target share and red-zone targets,
whether a TE finished top 12 under him; designed QB runs, play-action and deep-ball
rates, passing volume against league average; red-zone pass versus run inside the 10.

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
and it is measured: PFF pass-block and run-block grades, ESPN pass and run block win
rates, FTN adjusted line yards and adjusted sack rate, pressure rate and sacks
allowed, yards before contact for the backs, time to throw for the quarterback. The
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
hand-edited and never produced by an agent. The script ships in the plugin's
`scripts/` folder, beside the validator; copy it into `kb/<season>/` at the first
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
it, `[<date>]` a refresh changed it.

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

## Build (once, before the season)

0. Confirm the location with the user and get an explicit go-ahead (skill section 10);
   offer the NFL-wide cross-cuts alone as the starter set when the full build is more
   than the user wants.
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
   a gap round fills the high and medium items.
8. A media pass: themed sweeps (sleepers, breakouts, busts and risky picks, rookies and
   up-and-comers, preseason usage and rest, coach statements on roles, injury risk and
   timelines, handcuffs to own), each reading many whole articles, merged into every
   dossier's Media read section, then skeptic-checked.
9. README and the first refresh-log line.

## Refresh (a delta)

Weekly, the morning after the week's last game and before waivers clear; and before
every draft, lineup lock, trade decision, waiver or free-agent move, and roster move.

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
   claim and applies corrections.
3. Usage check (in season): for every fantasy-relevant player, compare the week's
   actual snap share, carries, routes and targets (collected once from the league-wide
   tables at PFF, Fantasy Points, Next Gen Stats or the box scores) against his
   caller's tendency profile and the direction the profile gave him, and mark the line
   confirmed, diverging or new (a role the profile did not predict). Two diverging
   weeks change the direction; one is noise. In-season calls read the comparison
   rather than the preseason profile, alongside the engine's projection and not ahead
   of it.
4. Schedule and defense update (in season): refresh the defensive-injuries file from
   the week's practice reports and designations (every key defender out, doubtful or
   on IR, and the position group his absence softens); refresh the defense ratings
   from the season's points allowed by position (blended with last season until four
   weeks are in) and write the injury adjustments for the coming week as the table the
   script reads; then run `scripts/schedule-tables.py` with the coming week, which
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
  team codes, and comparing collected numbers to a stated direction. A lower tier does
  this as well as the strongest one; the two-week rule absorbs a single mislabel in
  the usage check. Give the tier the numbers; never make it fetch what a collector can
  hand it.
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
