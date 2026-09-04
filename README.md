# Fantasy Copilot

A Claude Code skill that turns Claude into a fantasy football copilot riding shotgun with
[Draft Sharks](https://www.draftsharks.com): live draft-day advising, pre-draft strategy and
draft plans, and season-long weekly guidance (start/sit, waivers, trades, playoff prep).

**Requires Draft Sharks.** This skill advises alongside Draft Sharks' valuation engine: its
Draft War Room, 3D Value, live-draft sync extension, injury model, and in-season suite.
Without a paid Draft Sharks subscription it has nothing to steer by. **Only Draft Sharks is
supported today; other tools may be added in the future.**

Two things the skill will establish up front:

- **Your subscription tier.** Draft Sharks sells several tiers and they gate real features
  (keeper/dynasty/auction tools, analyst Q&A). The skill asks which tier you pay for, scopes
  its claims and workflows to it, and, because tier contents change over time, verifies the
  current offering on draftsharks.com before asserting what your tier includes.
- **Browser access for live drafts.** Real-time in-draft advising requires Claude to see
  your draft room and the Draft Sharks panel as picks land, for example via the Claude in
  Chrome extension. Without browser access you still get pre-draft strategy and weekly
  guidance, and the skill will tell you plainly that live advising is unavailable.

## What it does

- **Draft day:** a two-line recommendation decided *before* your pick clock starts, live
  color commentary the whole draft (run alerts, pivot flags, reactions), opponent-need
  tracking, and rehearsed fallbacks for every known sync failure mode.
- **Pre-draft:** league-synced settings audits, mock-draft calibration, slot-specific plans
  with tier-cliff triggers and pivot trees, and (top tier) drafted questions for Draft
  Sharks' Personalized Advice analysts.
- **In-season:** a weekly cadence over Draft Sharks' tools: waivers by rest-of-season value,
  lineup and matchup calls (floor when favored, ceiling when underdog), trade guidance
  (finding the right partner, valuing both sides of an offer in your league's scoring, not
  someone else's), and trade-deadline and playoff-week positioning.
- **IR stashes:** an on-demand sweep of injured free agents, Draft Sharks first, that tags
  who actually returns this season, values them against your bench, and leads with the
  next date a player clears to free agency so a stash never costs waiver priority.
- **A knowledgebase of the NFL's current state:** a dossier per team (who the coach
  named, whether an injured starter's replacement is one man or a committee, the rookie
  behind the aging veteran, preseason usage and rest) plus NFL-wide cross-cuts, built
  before the season with your go-ahead and refreshed as a delta before every decision.
  The numbers behind it come from source tables pulled once (Draft Sharks' own tools
  first, then the free public tables) and saved beside the profiles, so no pass has to
  fetch a table on its own.
- **Discipline you'll be glad it has:** it never clicks a pick or submits a roster move
  (you drive, always), it never skews Draft Sharks' projections to match its own opinions
  (two independent signals, argued out loud), and it keeps your league details in your own
  private notes file, never in the skill.

## Install

```
/plugin marketplace add nmiller0113/claude-marketplace
/plugin install fantasy-copilot@nates-plugins
```

Then `/reload-plugins`, or restart. Update later with
`/plugin update fantasy-copilot@nates-plugins` followed by `/reload-plugins` again.

## Using it

- It loads automatically for fantasy football work: drafts, mocks, waivers, trades, lineups,
  or Draft Sharks questions. Load it on demand with `/fantasy-copilot:fantasy-copilot`.
- On first use, tell it about your leagues (host, format, scoring, roster). It will keep a
  private league-profile document in your files; that is where everything specific to you
  lives, and where it appends dated lessons after every draft and season.
- During a live draft, keep the draft room and the Draft Sharks sync panel visible to Claude
  through its browser access (Claude in Chrome) and let it talk. You click. It advises.
- The skill is keenly aware of your league's settings, and every opinion it gives is
  formulated around them. Third-party grades, ranks, and analyzers that do not account for
  your format and scoring get treated as noise, and that applies everywhere a settings-blind
  number shows up: draft grades, matchup ratings, trade evaluators, generic expert ranks.

## Maintaining

The plugin itself needs no shell, interpreter, or particular operating system: it is a
skill file, its reference files, and a manifest. Four optional scripts ship with it:
`scripts/schedule-tables.py` builds the knowledgebase's schedule-strength tables from
the schedule and the defense-ratings files (Python 3.8 or later, nothing else), reading
the team codes from the knowledgebase's own `data/teams.md` and stopping when that file
is missing; the skill copies it into the knowledgebase folder and runs it there during a
build or refresh, and without Python it reports the tables as not built rather than
having an agent write them. `scripts/missing-lines.py` (same requirement) is the gap
rounds' yardstick: it counts the profile lines that say a fact is missing, writes the
next round's file list, and writes each file's open lines with their line numbers for
the fill prompts; `scripts/gap-list.py` (same requirement) ends a round by writing every
line that still says a fact is missing, by file, with the reason where one was written,
which is the report. The fourth, `scripts/check-fills.py` (same
requirement; without Python the build reports the fills as unchecked rather than
checked, and the set is not called complete), checks that each profile sentence a build filled from a saved source
table cites a table that exists and carries at least one of the sentence's numbers in
the rows of a player or team the line, its heading or its file name names. A marker
that names no source does not pass, and neither does a sentence whose subject is absent
from the table it cites. A name several players answer to is held to the teams that same
line names, so another club's row cannot answer for the player the line is about; a name
only one row answers to is already one player and finds him wherever he plays, and a
row that names no team at all answers to any name; those are the two ways a figure from
a club the line never mentions still passes. Two things a clean run does not prove: that the figure came from the right column; and that the
sentence's other figures are right, since one correct figure carries the sentence past
every wrong one beside it. A line that names two teams is still checked against both,
which is how the coach files quote a coordinator's previous unit beside his current one,
so write one subject to a line where the attribution has to be checkable. A depth-chart
citation is checked by player name instead, searched across all 32 teams, since a depth
chart holds no numbers worth checking. The release validator, `scripts/check.sh`, is a
maintainer tool run by hand before publishing and needs bash and git; on Windows, Git
for Windows provides both. Users never run it, and Claude never runs it inside the skill.

## License

MIT.
