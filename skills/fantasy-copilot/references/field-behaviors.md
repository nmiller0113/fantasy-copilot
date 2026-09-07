# Verified field behaviors (live-tested against Yahoo)

Read this when preparing a draft day or diagnosing a sync problem. Sections 5, 7 and 8
of the skill hold the rules these observations produced; this page holds the observations
and the reasoning, so a maintainer can tell a still-true rule from a stale one.

## Sync and latency

- Measured cross-off latency of the sync panel: 4 seconds or less per pick; panel
  attach under a minute.
- For a few seconds after a pick lands, the panel can render its suggestion cards with
  the 3D values and the projections filled in and the name and team still blank. A
  value-only card is not a name: in that window read the name off the reloaded War Room
  list, and never name a player from a card whose name has not rendered.
- The sync panel inside the host's draft window is an extension frame, and its text is
  NOT in the host page's text layer: a text read of that page returns the host's own
  rows and nothing of the panel. An empty text read is therefore a failed read, not an
  empty panel, and a screenshot is the read that works. Naming off a memory or an
  inference because the text read came back empty cost a pick: skill section 7 now
  requires a row the copilot can see at that moment, and the words "no read" when
  there is none.
- **Host mock rooms get fresh league ids**, so DS errors "Error Syncing!" on every mock
  and its Set-Up flow creates a junk clone league per mock. Real league rooms carry the
  linked ids and should attach clean. Delete clone leagues afterward: a wrong league
  selected in the War Room is a classic failure mode, and clones multiply it.
- A synced draft order before the host randomizes is often just JOIN ORDER. Hosts
  commonly randomize 30-60 minutes out, and a DS re-sync before the room opens may not
  pick the randomized order up; the host's own draft room shows it. Re-sync at the
  reveal and verify the user's slot before trusting any slot-specific plan. Observed
  again: a re-sync run after the order was revealed but before the room went live
  fetched the join order, and the engine re-slotted itself only when the first live
  pick landed. The re-sync is not the verification; the host's room is (skill
  section 5).

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
- The host's ranked pick suggestions are a good forecast of what the room takes (in one
  room they matched the first nineteen picks exactly) and a bad census of what is left.
  That list ranks an injury-tagged player low enough to keep him off its top rows while
  he sits undrafted, so absence from it is absence from the FORECAST, never absence from
  the board. Reading it as a census left a back with the highest value on the board
  unpicked for two turns. The pick tape, the roster panel and the engine's crossed-off
  board are the only evidence a player is drafted (skill section 7), and two players
  sharing a surname are told apart on the tape, not on a list.
- The host's autodraft control changes its border style once the room goes live, and
  renders highlighted even when autodraft is confirmed OFF. The border is a state the
  room paints, not the setting; read the control's own state, and have the user confirm
  it before the clock as skill section 5 already requires.
- Waiting for the user's turn is done in SHORT batches. A batch of waits returns only
  when its last wait ends, so a long batch issued a few picks out returns after the
  clock has come and gone: eighteen ten-second waits in one batch cost a whole turn, and
  the user drafted two picks unassisted. Skill section 5 carries the cadence: never more
  than six ten-second waits in one batch between turns, at most three before a clock
  read inside about five picks, one wait per read inside two.

## The standalone War Room tab

- The rankings list goes stale within a few picks: just-picked rows stay at the top
  with their old values and newly surfaced rows do not appear until a page reload,
  while the header pick ticker and the roster panel stay live. Reload the tab about
  three picks before each of the user's turns, every turn; sync survives the reload.
  The at-the-clock verification in skill section 7 runs against the live pick ticker
  plus a row in view, the reloaded list or the in-room panel by screenshot, never
  against a list that has not been reloaded this turn. Trust the pick tape and roster
  panel over the rankings list.
- Do not open League Settings mid-draft: visiting that pane can silently flip the
  league to Manual Mode (a re-sync clears it).
- On a freshly synced league the position filter buttons may not apply, and two
  rankings tables can exist in the page at once; read the visible rows of the ALL list.
  Still true in a live room, and it bites hardest on the last two positions: with no
  working filter the kicker and defense rows sit far below the visible rows of the ALL
  list. Read them from the in-room sync panel at the clock, by screenshot; the host's
  own player list filtered there finds the candidate, the panel's row is the read
  (skill section 7).
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
- The Team Dashboard's Starters and Bench blocks have been seen disagreeing with the
  lineup set on the host for the same roster, every player accounted for on both pages.
  The sync carries who is on the roster and which slots the IR holds; the arrangement
  of those players into starters and bench read as the engine's own recommendation, but
  whether a re-sync would have aligned it with the host was not tested, so the mechanism
  is inferred from one roster. Read as the user's slots, that arrangement said
  a position had no bench cover when the host's team page showed one, and a bye-cover
  answer built on it was wrong. Membership and IR occupancy can be read off the
  dashboard; which player sits in which slot comes from the host's own team page only.
