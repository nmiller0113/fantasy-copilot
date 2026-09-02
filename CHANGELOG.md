# Changelog

Every version of this plugin has one entry here, an annotated git tag `vX.Y.Z` on the
commit that declared it, and a GitHub release carrying this same text. The version number
lives only in `.claude-plugin/plugin.json`. Minor bump: the skill's rules changed. Patch:
everything else.

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
