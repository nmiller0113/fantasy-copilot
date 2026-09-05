# Verified field behaviors (live-tested against Yahoo)

Read this when preparing a draft day or diagnosing a sync problem. Section 5 of the
skill holds the rules these observations produced; this page holds the observations
and the reasoning, so a maintainer can tell a still-true rule from a stale one.

## Sync and latency

- Measured cross-off latency of the sync panel: 4 seconds or less per pick; panel
  attach under a minute.
- For a few seconds after a pick lands, the panel can render its suggestion cards with
  the 3D values and the projections filled in and the name and team still blank. A
  value-only card is not a name: in that window read the name off the reloaded War Room
  list, and never name a player from a card whose name has not rendered.
- **Host mock rooms get fresh league ids**, so DS errors "Error Syncing!" on every mock
  and its Set-Up flow creates a junk clone league per mock. Real league rooms carry the
  linked ids and should attach clean. Delete clone leagues afterward: a wrong league
  selected in the War Room is a classic failure mode, and clones multiply it.
- A synced draft order before the host randomizes is often just JOIN ORDER. Hosts
  commonly randomize 30-60 minutes out, and a DS re-sync before the room opens may not
  pick the randomized order up; the host's own draft room shows it. Re-sync at the
  reveal and verify the user's slot before trusting any slot-specific plan.

## Settings-blind numbers

Host draft grades, matchup ratings, built-in trade evaluators, and generic expert
ranks routinely ignore the league's format and scoring (for example a host's draft
grade that scores against 1-QB ADP will C-grade a correct early superflex QB). Every
opinion this skill gives is formulated from the league's actual settings; the
league-aware signal (DS's synced valuations plus the copilot's own settings-aware read)
outranks any settings-blind number in every decision: drafts, start/sit, waivers, and
trades alike. A grade card can also render a wrong letter for a minute after a draft
and then correct itself; read the analysis page, not the first card.

## The host draft room

- Hosts may **re-arm autopick every time a clock expires**. If it engages, kill it
  immediately, or it insta-picks later rounds.
- **Queue trick**: pre-queue DS's top 2-3 in the host's queue before each pick; an
  expiry then drafts from the user's list, not the host's default ranks.
- Hosts redesign draft-room UIs yearly. Before the clock starts, have the user locate
  the player SEARCH BOX and confirm autopick is off; hunting for redesigned controls on
  a live clock has cost real picks.
- The host's draft room shows the market: a last-7-days ADP column and an injury tag
  on each player's row. That ADP is the price the room is likely to pay; the tag is
  what other drafters see and sometimes skip on sight, which is where a value falls.

## The standalone War Room tab

- The rankings list goes stale within a few picks: just-picked rows stay at the top
  with their old values and newly surfaced rows do not appear until a page reload,
  while the header pick ticker and the roster panel stay live. Reload the tab about
  three picks before each of the user's turns, every turn; sync survives the reload.
  The at-the-clock verification in skill section 7 runs against the live pick ticker
  plus the reloaded list, never against a list that has not been reloaded this turn.
  Trust the pick tape and roster panel over the rankings list.
- Do not open League Settings mid-draft: visiting that pane can silently flip the
  league to Manual Mode (a re-sync clears it).
- On a freshly synced league the position filter buttons may not apply, and two
  rankings tables can exist in the page at once; read the visible rows of the ALL list.
- 3D values re-scale as the draft goes: the same player's number rises as the user's
  next pick approaches and the pool thins. Compare rows within one reload, never across.

## Observed engine behaviors

- In 1-QB formats the War Room shows every non-elite QB at 3D 0, rank 0, 0% odds for
  most of the draft, and those rows flip to real numbers about one round before the QB
  tier cliff. The raw rows carry full projections, so the zeros are the value column,
  not a render failure. The reading that fits: the engine sees no gap between the QB
  you take now and the one at your next pick. Treat the zeros as the wait signal and
  the flip as the cliff warning; the mechanism is inferred, not documented by DS.
- Public money rooms have been seen drafting IR-designated players as stashes in the
  last two rounds. If the plan wants an IR stash, take him before the user's final pick,
  not with it.
