# Changelog

Every version of this plugin has one entry here, an annotated git tag `vX.Y.Z` on the
commit that declared it, and a GitHub release carrying this same text. The version number
lives only in `.claude-plugin/plugin.json`. Minor bump: the skill's rules changed. Patch:
everything else.

## [1.17.0] - 2026-09-03

**Rules changed: a knowledgebase build or refresh puts judgment on the strongest
model, extraction on a lower tier, and joins in a script; league-wide facts are
collected once and routed to teams.**

New: `scripts/schedule-tables.py` (Python 3.8 or later, no other dependency) writes
the 32 per-team schedule-strength tables and the NFL-wide rollup from the schedule
file and the defense-ratings file. A deterministic join, exact and re-runnable every
week, replacing 33 agent runs. The ratings file now keeps the shapes the script reads:
the team code alone in the Defense cell, one of the words soft, average, tough in each
rating cell, and the coming week's injury adjustments as a table "Defense | Position |
Season | Week N | Player out". The build step and the refresh step that produced those
files by agent now run the script.

New in `references/knowledgebase.md`, "Agents, models and scripts": three kinds of
agent work and what each runs on. Judgment (what a source supports, PRIMARY versus
COMMITTEE, scheme matched to a player, defense ratings, every skeptic) stays on the
strongest model at normal effort. Extraction (a transactions wire, an injury report, a
snap-count table into team-tagged items; collected numbers against a stated direction)
runs on a lower tier, which is handed the numbers rather than made to fetch them. Joins
(anything derivable from two existing files) are scripts, never models. Two shapes
follow: collect once and route, so 32 per-team agents do not each search the whole
week from scratch and each keeps one targeted search for local reporting; and edit only
where something changed, so a profile set is opened only for teams whose collected
items touch it. One workflow at a time; a failed call is retried once and then counted
as a gap, never filled in.

Changed: the refresh's sweep step is now collect-then-merge (step 1 and 2), still
"what changed since the last refresh date" under the same ground rules; the usage
check reads collected numbers; and the line-profile edit is limited to teams with a
collected line change. The reference states both input shapes the script reads, where
the script lives (copied from the plugin's `scripts/` folder into the season folder),
and that without Python the tables are reported as not built, never written by an
agent. Section 10 of the skill carries the one-sentence rule and points at the
reference. The validator scans shipped Python for the same leaks as the prose and
parse-checks it when Python is present.

## [1.16.0] - 2026-09-03

**Rules changed: the knowledgebase carries the whole coaching staff's tendencies,
the offensive lines, and the schedule rated by position, all matched to players and
refreshed weekly.**

Two more layers ride with the staff profiles. The offensive line profile, one per team:
the five starters with continuity, last season's pass-block and run-block grades and win
rates, pressure and sacks allowed, adjusted line yards, yards before contact and time to
throw, the 2026 changes and the line coach, and the direct impact one line per player on
the back, the quarterback and, through the quarterback, the pass-catchers; the NFL-wide
file ranks the lines and names who benefits and who is exposed, and it is read together
with the opposing coordinator's pressure profile in a weekly matchup. The schedule
layer: the season schedule built by two independent fetches and reconciled; every
defense rated soft, average or tough per position, preseason from last season's points
allowed adjusted by the defensive profile and in season from 2026 actuals; each team's
weekly matchup table with soft/average/tough counts for weeks 1-4, mid-season, and the
playoff windows 15-17 and 16-17; and an NFL-wide file of the softest and toughest
schedules by position and window with the week-by-week grid. Draft Sharks' Strength of
Schedule and Fantasy Points Allowed tools are the live overlay. Defensive injuries are
tracked as their own file and applied weekly: every key defender out, doubtful or on IR
with the position group his absence softens, so a defense's rating for the coming week
can differ from its season rating, and the difference is the weakness to exploit; the
defensive profile lists the key defenders for that purpose. Every one of these layers
is read alongside the engine's projection, never ahead of it. The build gains steps for
the per-team profiles, their rollups and the schedule; the weekly refresh is renumbered
one to six with the usage check as step 3 and the schedule update as step 4.

A coach's record at prior stops is public and it predicts what he does with the players
he has now. Section 10 now lists that layer among what the knowledgebase holds, and
`references/knowledgebase.md` gains the profiles for the whole staff. For the head coach
and the play caller: sources by name, the numbers to collect (pass rate, whether the
lead back gets 65 percent of the touches, RB target share, WR1 target share, whether a
tight end has finished top 12 under him, red-zone habits), the separation of what he
did (numbers) from what he says (dated quotes) from what reporters predict (labeled),
and the player-first ending, one line per
fantasy-relevant player with a direction, bounceback, step-forward, downgrade or
unchanged, and the number or quote that drives it. For the defensive coordinator: scheme
numbers (front, man versus zone, blitz and pressure rates, coverage shell, takeaways),
what the scheme gives up by position, the DEF/ST unit's direction with its first four
opponents, and the effect on the team's own offense; the NFL-wide defense file is the
matchup table for start/sit and streaming, read alongside the engine's projection.
Special teams only where a change touches a kicker or returner. The weekly refresh
gains a usage check: each player's actual snap
share, carries, routes and targets against the profile's direction, marked confirmed,
diverging or new, two diverging weeks changing the direction and one counting as
noise; in-season calls read the comparison rather than the preseason profile, alongside
the engine's projection. Layout gains `coach/<CODE>.md`, `coach/<CODE>-defense.md`,
`oline/<CODE>.md`, `schedule/<CODE>.md`, and the NFL-wide `coach-tendencies`,
`defense-tendencies`, `offensive-lines`, `schedule`, `defense-ratings`,
`defense-injuries` and `schedule-strength` files.

## [1.15.0] - 2026-09-03

**Sections 4, 5, 7 and 8 shrink to what matters at the clock, the detail moves to
reference files, and five field rules from live drafts are added.**

The restructure. The skill body sat a few lines under the validator's ceiling, and most
of that length was explanation the model does not need while a pick clock runs. Section
4 keeps the Draft Sharks facts that decide a call and says when to read
`references/draft-sharks.md` (setting up or rehearsing a league, drafting advice
questions, a misbehaving tool): the engine's indicators, the War Room's manual-mode
procedure and rehearsal, the Mock Draft Trainer, the sync extension, the Injury
Predictor and Rookie Model, the advice form, the tool inventory. Section 5 keeps its
field rules and says when to read `references/field-behaviors.md` (preparing a draft
day, a sync or War Room problem): the measured latencies, mock-room clone leagues, the
observations and the reasoning behind each rule. Section 7 keeps every rule of the
live-draft loop, including the IR-stash exception's two conditions, the "one adjustment,
not two" precedence between the section 6 band and the research-targets rule, and the
clause that a stated preference does not reopen the call, and loses only the
justifications it repeated two or three times. Section 8's IR stash procedure (sources,
tags, value test, the free window, the burn-the-claim flag, on-demand use) moves whole
to `references/ir-stash.md` behind a short rule. The body drops from 476 lines to
about 370.

The additions, each from a live draft, and each a rule the model did not have before:
compare 3D values within one reload and never across, because they re-scale as the pool
thins (section 5); a DS re-sync before the room opens may not pick up the host's
randomized order, so the slot is verified in the host's own room (section 5); on a
freshly synced league the War Room's position filters may not apply and two rankings
tables can exist at once, so read the visible rows of the ALL list
(`references/field-behaviors.md`); the host's draft room carries a last-7-days ADP column
and an injury tag per row, the market price and the flag other drafters skip on sight
(`references/field-behaviors.md`); a grade card can render a wrong letter for a minute
after a draft, so read the analysis page (`references/field-behaviors.md`); and the IR
stash run starts from the knowledgebase's availability list (`references/ir-stash.md`).
Two reference sentences are cross-links only: the Rookie Model bullet points at the
knowledgebase for coach statements, and the Draft Analysis entry lists what the tab
shows. Minor bump, because rules were added.

## [1.14.0] - 2026-09-03

**Rules changed: the copilot keeps a knowledgebase of the state of the NFL.**

New section 10, kept short, with the full procedure in a new reference file the model
reads only when building or refreshing: `references/knowledgebase.md`. Draft Sharks
carries the numbers; it does not carry who the coach named, whether an injured starter's
replacement is one man or a committee, how old the veteran ahead of a rookie is, or who
was rested in the preseason finale. Those facts decide bench rounds, stashes and waiver
claims and cannot be looked up on a live clock, so the copilot writes them down first: a
dossier per team with the same headings (rooms by position with age, role, status and
designation; the coach's plan for absences; an availability table; rookies and young
players behind veterans with the veteran's games missed over three seasons and the share
trajectory; a media read with preseason usage and rest signals and the sleeper, breakout,
bust and risk tags; hype labeled as hype), plus NFL-wide cross-cuts (the availability
list with each replacement plan; a successor map with PRIMARY, COMMITTEE or UNSETTLED for
every NFL RB, WR and TE starter; rookies; recent reporting and hype; suspensions and open
reviews; play callers and scheme). The first build needs the user's go-ahead and a
confirmed location, with the cross-cuts alone offered as a starter set. Two rules stay
in the skill: a source hierarchy for roles and usage only (coach
and general manager statements, then preseason usage and rest, then beat reporting, then
themed article sweeps, then depth charts last), scoped so that Draft Sharks remains
primary for value, projections and timelines as section 6 step 9 already says; and
refresh before every decision, as a delta, then search the files rather than browse
them. The reference file carries the layout, the dossier template, the vocabulary, the
build (one pass per team, parallel where the harness offers subagents, a skeptic on the
highest-impact claims, independent cross-cuts, a critic round, a media pass), the refresh
with its Draft Sharks overlay that records the gap between a changed role and the
engine's number, and search commands for a Unix shell and for PowerShell. Hooks: section
6 step 9 gains a fifth rule, refresh first and sweep only what is newer, inside its own
recency window; section 8's waiver eve refreshes first and reads RB, WR and TE
candidates against the successor map alongside the projection; its lineup-lock morning
opens the availability list first; section 7's bench-round read takes its up-and-comers,
full-role replacements and rest signals from the media read; section 9 places the
knowledgebase beside the private document. The validator's companion-file check now
resolves `references/` and `assets/` paths beside SKILL.md, where the skill layout puts
them, as well as at the package root, and its privacy and line-ending scans now cover
the reference files. The README gains the knowledgebase under What it does.

## [1.13.0] - 2026-09-02

**Rules changed: the bench rounds get the judgment layer the early rounds already had.**

Section 7 gains four rules and two amendments, from misses observed in live money
drafts where the starters graded well and the bench ranked near the bottom on ceiling.
The amendments: the flex is a starter slot in the bye check, so a flex candidate is
compared to every starter; and the grade-cost rule's list of overrides now includes an
IR stash and a contested bench dart. The rules: when the top row and the next candidate, neither a sweep
target, sit within about 5 3D points, the rec still leads with one name, and the second
line states the judgment tie-break (section 3's criteria 5a, 6 and 8, plus age and
current depth-chart role) only when that layer favors a name other than the top row,
before the clock rather than after the user asks; this is the second sanctioned case of
a second name, alongside the bye check, and when the bye check has claimed the second
line the stack finding keeps it. Pre-draft sweep names inside the research-target
band stay on the candidate list at every pick, a disagreement with DS about one of them
is said between picks instead of settled by dropping the name, and the name spoken at
the clock stands unless verification shows him drafted, news breaks, or the user names
a different player. A player carrying an IR-eligible designation in a league that
allows injured players straight to IR is a free roster spot to take before the room
does, under section 8's RETURNS tag and value test, with the designation on the host's
row as the test and a contested dart taking precedence. And once starters are filled,
the between-pick read names the positions the room has hoarded and the ones it is short
on, then drains the short position or takes the upside dart the room left, saying which
dart is contested, because a floor-only bench buys no ceiling.

## [1.12.0] - 2026-09-02

**The import audit walks the host's full category list and knows DS's field inventory.**

Section 6 step 1 now states what the Draft Sharks scoring editor can hold, all seven
tabs, and which common host categories have no field there and therefore score nothing
in DS's projections: player 2-point conversions, blocked kicks, returned extra points,
player return touchdowns, offensive fumble-return TDs. The audit rule changes from
"check that DS's rows match the host" to "walk the host's list and record what cannot
import", so a new league carries no surprise. The inventory is marked as a snapshot
with the same re-verify rule the subscription section uses: re-read the live editor on
every new league, and the live editor wins. The Advanced Scoring switch is documented:
on after a sync, it is what shows the bonus and per-position PPR rows, and it must not
be toggled during an audit. Verified 2026-09-02 on two synced Yahoo leagues with
identical editors.

## [1.11.1] - 2026-09-02

**Line endings pinned to LF, and the leak scan learns Windows path shapes.**

OS-agnosticism pass. The repository had no line-ending policy, so a Windows checkout
with git's default autocrlf setting would write CRLF files: the validator's own CRLF
check would then fail every run, the validator script itself would not start under
env, and every line of the skill file, frontmatter included, would carry a carriage
return. A .gitattributes now pins LF on checkout for every platform; a clone made
before it keeps its CRLF files until a fresh checkout. The validator's local-path
leak scan matched only Unix path shapes, so a Windows maintainer's drive-letter or
UNC path in a shipped file would have passed; both shapes are now in the scan. Two
more validator fixes from the same pass: run under a shell other than bash, or under
bash in POSIX mode as sh, it now refuses loudly with exit 2 (under dash or ash its
CRLF probe would degrade to a string that never matches and pass silently), and it
normalises its own path so a caller handing it a backslash path on Windows lands in
the package root instead of the parent directory. The ignore file gains the Windows
junk files, so a Windows checkout is not reported dirty by the release gate. The
validator remains a bash script that a maintainer runs by hand, and that is a platform
requirement that cannot be removed, so the README now states it in a Maintaining
section (bash and git; Git for Windows provides both; users never run it), and the
validator itself enforces it with the shell guard above. The skill runs no commands
and needs none. Nothing the plugin does has changed.

## [1.11.0] - 2026-09-01

**Snipe first: the copilot forecasts the picks between turns and takes our player before
the room does.**

Section 7 adds the forecast that the one-pick-early rule was missing: between picks,
for the opponents who pick before us, the copilot names the position their roster needs
most and the player the board gives them for it, from their roster, the live trend, and
ADP. That forecast is the list of players least likely to reach us, a data point like
the rest. It decides which pick is the early one for the research-targets rule; whether
the target is worth taking early is still that rule's 10-point band, and outside the
band the situation at the pick decides. A target not on the forecast is where the odds
column gets its say. The forecast is said between picks in one line; the rec at the
clock stays name first, two lines. Section 2 adds the posture behind the voice: the
copilot plays to beat the room, not to keep pace with it, two steps ahead, predicting
what the room does next and taking our player first.

## [1.10.0] - 2026-09-01

**Room trends are read and exploited, never followed.**

Section 7 adds a rule for runs, fads, and streaks of reaches in the draft room: a trend
is a data point like the others and never changes the plan silently. Between picks the
copilot states what the room did, the number it changes for one specific target (odds,
a value gap, whether a stash still reaches the free pool), and whether that is signal or
the room overreacting; the user decides, before the clock. When the room is wrong, that
is value left on the board: the player it skipped, the tier it ignores while it chases
the run, the value its reaches leave behind. The reading happens between picks; the call
at the clock is still one name. Changing the plan takes the discussion; taking value the
room dropped takes only the name. Section 8 adds the in-season half: managers who
overpaid for a name on draft day overpay after one big week, so trade into their
overreactions, buying the player the room undervalues and selling the one it chases.

## [1.9.0] - 2026-09-01

**Starter bye protection is an enforced step before every starter-slot name.**

The skill already said to check byes (section 3) and to plan for them (section 6), and a
draft still ended with two starting receivers on the same bye, because nothing in the
live loop made the check run. Section 7 now requires, for every candidate finalized
before the user's turn, a bye comparison against every rostered starter at the same
position, the flex, and any other slot he is eligible for (superflex QBs included), done
while the room is picking, with one re-read of the named player's bye at the clock. A
stack is stated in the rec's second line with the best non-stacking candidate named,
the one carve-out from the one-name rule, and the user decides; if every candidate
stacks, the rec says so. Section 3 states that DS's same-position bye alert must be
read in the War Room, that 3D folding byes into its number does not discharge the
check, and that starter bye protection is a disclosure default, not a veto. Section 6
requires a bye map in the plan's round bands.

## [1.8.0] - 2026-09-01

**Live-draft rules from a sharp money room: odds are ADP, targets go a pick early, the
grade is never promised.**

A ten-team public money draft took six of the copilot's pre-draft targets within three
picks of the user's turn, each time with the Next Pick Odds column saying the player
would survive. Odds and countdown are built from host ADP, and ADP lags the news feed
by days; a room that drafts off the feed takes a riser a full round early. New rules:
Next Pick Odds is a floor on risk, not a forecast, for any player tagged a riser
(section 4); a research target within about 10 3D points of the top live row is taken
at this pick, not the next (section 7); round bands place risers one round earlier in
public and money rooms (section 6); the grade cost of any engine override is stated in
the rec, and the grade is never predicted (section 7). Field behaviors added (section
5): the standalone War Room rankings list goes stale within a few picks and is reloaded
before every user turn; non-elite QBs show 3D 0 in 1-QB formats until the tier cliff is
a round out, read as the wait signal (the mechanism is inferred, not documented by DS);
money rooms have been seen drafting IR stashes in the last two rounds, so a planned
stash goes before the final pick.

## [1.7.4] - 2026-09-01

**The README no longer carries the release procedure.**

The Publishing section added in 1.7.3 described how to cut a release. The README is for
people installing the plugin, and the procedure it described is already enforced by
scripts/check.sh (release mode refuses an unlogged, untagged, unannotated or dirty
version) and stated in this file's preamble. Duplicating an enforced rule in user prose is
a copy that drifts. The validator's own requirements stay in its header comment. Doc
only; nothing the plugin does has changed.

## [1.7.3] - 2026-09-01

**A changelog, a tag and a release for every version, and a release gate in the validator.**

Every version so far was a number in plugin.json with nothing pointing at it: no tag to
check out or diff against, no release to read. This version adds CHANGELOG.md (one entry
per version, the same text as each release note) and a release gate: scripts/check.sh
now reads the declared version, fails when CHANGELOG.md has no entry for it, warns when
no matching tag exists, and with --release refuses to pass unless an annotated tag for
that version sits on the current commit and the working tree is clean, so an untagged or
half-committed version cannot ship. CHANGELOG.md joins the leak scan. README states the
release order and what the validator needs. The tags v1.1.1 through v1.7.3 and their
releases are published from this commit, each tag on the commit that declared its
version; they are not part of the commit itself.

## [1.7.2] - 2026-09-01

**README names the IR stash sweep; pre-draft procedure ends with the post-draft IR step.**

Two follow-ups the user asked for. The README's in-season list did not mention the
IR feature 1.7.0 added. The pre-draft procedure stopped at the injury sweep, so the
post-draft handoff (state the pool's clear date, then run the IR sweep that day) had
no home; it is now step 10.

## [1.7.1] - 2026-09-01

**The IR stash sweep runs on demand any week, and leads with the next free clear date.**

1.7.0 tied the sweep to waiver eve and post-draft. Users ask for it whenever they are
thinking about their bench, and the piece they most need first is the calendar: when
the next pool clears to free agency, so they are ready before the window opens rather
than reacting after it. Patch: same procedure, wider trigger, calendar first.

## [1.7.0] - 2026-09-01

**IR stash research as a procedure, with the free-pickup window and a burn-the-claim flag.**

The in-season section had one IR bullet: returns-this-season only, verify against
current depth charts. It said nothing about HOW to research the pool or WHEN a stash
can be taken without spending waiver priority. Both gaps cost real claims in practice:
a rolling-priority claim burned on a player who would have cleared to free agency two
days later, and a season-out stash claimed off percent-rostered popularity.

This release turns the bullet into the same discipline the pre-draft sweep uses:
DS-first sources (Free Agent Finder by rest-of-season projection, Injury Predictor,
the player's own Shark Bites page since the public feed only shows about a day,
Team Dashboard, depth charts with their review date), a RETURNS / SEASON-OUT /
NO TIMETABLE tag on every candidate, a value test against the healthy alternative
and the displaced bench player, and a recorded per-league waiver calendar so the
default is always the free clear date. The burn-the-claim flag is the only sanctioned
exception, and it must carry its price in the same line.

Minor bump: the skill's rules changed.

## [1.6.0] - 2026-09-01

**Pre-draft injury/value sweep must be DS-first, recency-windowed, priced-in-aware.**

Live-draft prep exposed a methodology hole: a generic web-news sweep that
sidelined the paid Draft Sharks engine and mislabeled 3-week-old, already-
priced news as fresh 'risers.' New step 6.9 makes the injury & value layer:

- DS-FIRST: Injury Predictor, Shark Bites, depth charts, Free Agent Finder,
  and rest-of-season projections are the primary source; web search only
  supplements to catch what DS has not reflected yet.
- RECENCY-WINDOWED: last ~7-10 days only; older news is already in DS's
  number and the room's ADP, so it is not an edge.
- FRESH-vs-PRICED-IN tagging on every finding; old news at a correct price
  is not actionable.
- CROSS-CHECK every riser/faller against the DS 3D value before it earns the
  label; the edge is the GAP between fresh reality and a lagging price.

check.sh: 0 fail, 1 warn (237 lines vs 200 target). validate passes.

## [1.5.0] - 2026-08-31

**Field lessons from the first live drafts.**

Two real Yahoo drafts and a money-league prep cycle surfaced knowledge that
holds for every Draft Sharks subscriber:

- Correction: a literal Next Pick Odds column exists in rankings views; the
  skill previously claimed otherwise.
- Mine/Theirs manual mode fully mapped: no undo in the live War Room (Grid
  trash icon is the real undo), Clear Rosters fires a native confirm and
  wipes everything, re-sync preserves entered picks, and the Mock Trainer
  cannot rehearse manual mode because it keeps simulating with sync off.
- New verified field behaviors: stale-tab vs live-panel split, settings-pane
  Manual Mode trap, join-order placeholder draft orders, and yearly host UI
  redesigns (find the search box before the clock starts).
- Live loop: decide early but deliver the name at the live clock, verified
  against the crossed-off board; one name, no hedged fallbacks.
- In-season: redraft IR doctrine (designated-to-return only; percent-rostered
  measures popularity, not value; verify current-year depth charts).
- Advice form: same-day turnarounds observed, late questions still worth it.

check.sh: 0 fail, 1 warn (body 220 lines vs 200 target; the added field
behavior is worth the overage). claude plugin validate passes.

## [1.4.1] - 2026-08-24

**State the data-points rule on the Personalized Advice mechanism itself.**

The 1.4.0 signals rule already covers analyst answers, but the place a
future reader looks when an advice reply arrives is the Personalized
Advice bullet, so the rule is now stated there too, in the user's own
phrasing: any analyst response is data points, not directives.

Patch bump: restates an existing rule where it is consumed; no rule
changed.

## [1.4.0] - 2026-08-24

**Signals combine as data points, never as directives.**

User feedback after the first Personalized Advice answer came back: the
skill summarized analyst advice as 'anchors' and 'hard stops', which
over-weights one input. The rule now stated in the value framework: DS's
board, analyst answers, pre-built plans, the assistant's own read, and the
live room all sit at the same table; no single signal outweighs another by
default, and the situation at the moment of decision dictates which one
carries the call. Analyst advice and pre-draft plans are priors to update,
never directives to execute.

Minor bump: the skill's rules changed.

## [1.3.0] - 2026-08-24

**League-settings awareness generalized beyond drafts and formats.**

User feedback on the README's superflex bullet. The principle was stated
too narrowly twice over: it named one format (superflex) when the real
claim is that every opinion is formulated from the league's actual
settings, whatever they are; and it scoped the warning to draft grades
when settings-blind third-party numbers appear everywhere decisions get
made: matchup ratings, built-in trade evaluators, and generic expert ranks
as much as draft grades. The skill now states the general rule and applies
it to every decision type: drafts, start/sit, waivers, and trades alike.

Also adds trade guidance to the README's in-season list (partner finding
and valuing both sides of an offer in the league's own scoring), which was
present in the skill's cadence but missing from the README's description.

Minor bump: the skill's rules changed.

## [1.2.0] - 2026-08-24

**Tier awareness, live-offering verification, and browser-access requirement.**

Three rules changes from user feedback on the shipped README:

1. The skill now ASKS which Draft Sharks tier the user pays for, records it
   in their private document, and scopes every claim and workflow to it. A
   base-tier user must never be offered the Personalized Advice workflow,
   and a keeper league needs the middle tier before the skill plans around
   keeper tools.

2. Tier contents are treated as a snapshot, not ground truth. Before
   asserting a feature exists at the user's tier, recommending an upgrade
   or downgrade, and at each season start, the skill verifies the current
   offering at draftsharks.com/subscribe. The live offering wins over the
   skill's own text when they disagree.

3. Browser access for Claude (Claude in Chrome or equivalent) is now a
   stated requirement for the live-draft copilot function, in both the
   skill and the README first section. Real-time advising only exists if
   Claude can see the draft room and the DS panel as picks land; without
   it the skill still does pre-draft strategy and weekly guidance and must
   say plainly that live advising is off the table.

Minor bump: the skill's rules changed.

## [1.1.1] - 2026-08-24

**Initial public release of the Draft Sharks fantasy copilot.**

A fantasy football copilot skill for Draft Sharks subscribers: live
draft-day advising, pre-draft strategy, and season-long weekly guidance.
Requires Draft Sharks; only Draft Sharks is supported today.

History note: this repo was briefly published earlier today and then
deleted and recreated with fresh history, because the release validator's
first revision enumerated author-specific identifiers as a denylist, which
made the guard itself a copy of the data it existed to keep out. The
validator now asserts a shape instead (any 5+ digit run in shipped prose
fails) and states honestly what it cannot cover: names in prose are
ordinary words no scan can prove absent, so the publisher reads every
shipped file end to end before pushing. Version starts at 1.1.1 to stay
continuous for anyone who saw the earlier publication.
