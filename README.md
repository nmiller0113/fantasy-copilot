# Fantasy Copilot

A Claude Code skill that turns Claude into a fantasy football copilot riding shotgun with
[Draft Sharks](https://www.draftsharks.com): live draft-day advising, pre-draft strategy and
draft plans, and season-long weekly guidance (start/sit, waivers, trades, playoff prep).

**Requires Draft Sharks.** This skill advises alongside Draft Sharks' valuation engine: its
Draft War Room, 3D Value, live-draft sync extension, injury model, and in-season suite.
Without a paid Draft Sharks subscription it has nothing to steer by. **Only Draft Sharks is
supported today; other tools may be added in the future.**

## What it does

- **Draft day:** a two-line recommendation decided *before* your pick clock starts, live
  color commentary the whole draft (run alerts, pivot flags, reactions), opponent-need
  tracking, and rehearsed fallbacks for every known sync failure mode.
- **Pre-draft:** league-synced settings audits, mock-draft calibration, slot-specific plans
  with tier-cliff triggers and pivot trees, and (top tier) drafted questions for Draft
  Sharks' Personalized Advice analysts.
- **In-season:** a weekly cadence over Draft Sharks' tools: waivers by rest-of-season value,
  lineup calls (floor when favored, ceiling when underdog), trade-deadline and playoff-week
  positioning.
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
  (for example via browser access) and let it talk. You click. It advises.
- Superflex players: this skill is opinionated about format-correct QB valuation and will
  tell you to ignore your host's format-blind draft grades. That is the point.

## License

MIT.
