# Draft Sharks: mechanisms, tools and procedures

Read this when setting up a league, rehearsing the War Room, drafting Personalized
Advice questions, or when a DS tool behaves unexpectedly. Section 4 of the skill holds
the facts needed at the clock; this page holds the rest.

## The valuation engine

- **3D Value (0-100)** is recomputed in under a second after every pick from 17
  indicators: league scoring, positional scarcity and dropoff by the user's NEXT pick,
  roster needs, opponent needs, ADP, injury-model discount, ceiling odds, bench depth,
  strength of schedule, byes, tiers. It is the number the skill advises alongside.
- **Tier boards**: draft to the cliff, not the rank. In superflex the QB tier cliff is
  the highest-leverage read in the draft.
- **ADP Countdown and Next Pick Odds** are the "will he come back to me" signals.
  Rankings views carry a literal "Next Pick Odds" percentage column, and hovering a
  player shows the countdown of picks until his ADP. Both are built from host ADP, so
  they are only as current as the host's ADP window. For a player whose news is fresher
  than that window (an exempt-list beneficiary, a lead back named this week, a starter
  cleared to play) the odds overstate survival: a room that drafts off the news feed
  takes him a full round before ADP says. For anyone tagged a riser in the pre-draft
  sweep, read the number as a floor on risk, never as a forecast.
- **Upside Mode** auto-engages around mid-draft and re-weights toward ceiling. Trust it
  late.
- **Injury Predictor** is an ML model; Projected Games Missed is baked into projections.
  "Low" values on fragile stars are the model working, not a bug.
- **SHARK Rookie Model plus Depth Charts** is the criterion-8 workflow: a high-SHARK
  rookie sitting behind an aging or fragile veteran is a time-share threat; price it
  into the veteran. The knowledgebase (skill section 10) carries the coach statements
  and usage reports that the model does not.

## The War Room

- **Mine/Theirs manual mode**: toggle Sync Enabled off under Manage Draft and every
  rankings row grows Mine and Theirs buttons: hand-entered picks, instant recompute, the
  fallback that keeps the War Room smart if sync fails; entries persist across reloads.
- The live War Room has NO "Undo Last Pick" (Mock Trainer only); the real undo is the
  Grid tab: click the pick's card, then its red trash icon.
- **NEVER click "Clear Rosters" mid-draft**: it fires a native browser confirm dialog
  (which freezes browser automation) and wipes every pick.
- "Re-sync" refreshes settings and order without touching entered picks.
- Rehearse manual mode in a REAL league's War Room and trash the test picks after; the
  Mock Trainer keeps simulating AI picks with sync off, so it cannot rehearse this.
- **Mock Draft Trainer**: league-synced mocks against varying-AI opponents. One mock is
  not a plan; run several to see the range of run timing.
- **Sync extension**: injects a Suggested Picks panel INTO the host draft room (one tab).
  DS's own docs say deleting the synced team and re-syncing fresh fixes "99% of sync
  issues"; do it the day before, never on the clock.

## The scoring editor's fields

The editor's inventory, a snapshot from synced Yahoo leagues in 2026: Passing (yards
per point, TD, completions, interceptions, sacks taken, first downs, long-play and
yardage-threshold bonuses, long-TD bonuses); Rushing (yards, TD, attempts, fumbles
lost, first downs, the same bonus rows); Receiving (yards, TD, targets, PPR set per
position for WR, RB and TE, punt and kick return yards, first downs, the same bonus
rows); Kicking (XP made and missed, FG missed, FG by distance bucket); Team Defense
(TD, special-teams TD, sacks, interceptions, fumble recoveries, safety, points-allowed
and yards-allowed ladders); IDP (tackles, assists, sacks, interceptions, fumbles
recovered and forced, passes defended, tackles for loss, QB hits, tackle-count
bonuses, TDs); Misc (head-coach win and points only). Host categories with no field
anywhere in that inventory, so they score nothing in DS's projections: player 2-point
conversions, blocked kicks, returned extra points, player return touchdowns (only
return yards exist), offensive fumble-return TDs.

## Personalized Advice (top tier only)

A league-aware form under Support, Advice section (categories: start-sit, waivers,
trades, keepers, general). Draft the questions for the user; the user approves sending.
Submit at least 48 hours before a draft when possible; same-day answers have been
observed, so a late question is still worth sending. Target the human-judgment gaps:
criteria 6 and 8, format strategy, scoring-specific value. Any analyst response is data
points, not directives (the signals rule in skill section 3): summarize it as inputs
alongside everything else, never as a plan to execute.

## Signal purity

**Adjust Projections** exists in the account area. Never use it. DS must stay an
unskewed, independent opinion. The copilot's takes live in the plan and the
conversation; disagreements with DS get DISCUSSED with the user, never written into
DS's engine. If that page shows non-default adjustments, flag it.

## The tool inventory

There is no "Perfect Draft" tool at DS; post-draft grading is League Analyzer's Draft
Analysis tab (grade, starter strength, bench strength, placement on DS, consensus and
ceiling projections). In-season suite: Team Dashboard, Free Agent Finder, Trade
Navigator, League Analyzer, Who Should I Start, Strength of Schedule, Fantasy Points
Allowed, Trade Value Charts, Shark Bites news, mobile app. Rest-of-season projections
are the currency of every in-season decision.
