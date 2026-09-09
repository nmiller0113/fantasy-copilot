# Changelog

Every version of this plugin has one entry here, an annotated git tag `vX.Y.Z` on the
commit that declared it, and a GitHub release carrying this same text. The version number
lives only in `.claude-plugin/plugin.json`. Minor bump: the skill's rules changed. Patch:
everything else.

## [1.41.0] - 2026-09-09

**The skill knew how to choose a starter and nothing about when the roster stops being able
to change one. Every rostered player, starter or bench, locks in place at the scheduled
kickoff of his OWN game, and inactive lists come out about ninety minutes before each
kickoff, so a questionable player in a late window resolves after the earlier windows have
already locked. That makes the arrangement of the starters across the slots a free decision
the copilot was not making: the projected total is the same whichever eligible slot a starter
occupies, but the flex is the only slot a body of any eligible position can enter, and a
body enters it only while it is unlocked. One ordered rule now arranges the week. The flex
is filled from the position whose starters outnumber its fixed slots. When one of that
position's starters is questionable, he sits in the flex and the healthy ones in the fixed
slots, so a scratch is one move, any bench body of any flex-eligible position kicking off in
his window or later into the flex, with no dependence on a healthy starter still being
unlocked; that claim outranks the latest-kickoff rule and the earliest-game rule, and when
two of them are questionable the flex goes to the one with the later kickoff, since his news
lands last. Otherwise the flex holds the healthy one with the latest kickoff, and the week's
earliest game never sits there. A questionable starter in a fixed slot is covered only by a
bench body at his own position kicking off in his window or later, or, while the flex holder
shares his position and is still unlocked when the news lands, by the chain, the flex holder
into the fixed slot and an unlocked bench body into the flex; a starter neither covers takes
the no-cover call, made before the EARLIER of his own kickoff and the safe alternative's
kickoff, the free-agent pool checked first, because deferring past that lock chooses the
questionable starter with no pivot. Every pivot is named with the window it is good until,
the earlier of the pivot body's kickoff and the kickoff of the player leaving the slot,
and a body named for two risks is said as such. The week is written down too, from the first
practice report to the last inactive list, in a new reference the two weekly bullets point
at.**

### Added

- `skills/fantasy-copilot/references/lineups.md`. What locks and when, as a table: a starter
  whose game has kicked off cannot be benched, moved or dropped for the rest of the week; a
  bench player whose game has started is never a substitute, though he is still droppable
  where the host's setting for locking benched players is off; a free agent whose game has
  not started is a free add, and one whose game has started is a claim until the weekly run
  on a host whose weekly-waiver setting places players on waivers at kickoff. Both settings
  are read once per league into the private document. Then the ordered flex rule in three
  numbered clauses, the same sentences section 8 carries, read in order, with the kickoff
  window an input to it and never a rule of its own, and why the first clause comes first: a
  questionable starter at a position with no surplus stays in his fixed slot, since in the
  flex he would leave that slot with nobody eligible to fill it, and the chain, run for the
  earlier of two questionable starters at the surplus position, spends the later one's pivot.
  The arrangement worked on three shapes, each table stating every slot, every player's
  position and window, and every starter's pivot with the kickoff it is good until: a surplus
  position with one questionable starter in the late-afternoon window, the healthy one in the
  last game, where the questionable one takes the flex and a bench body of a third position
  is his one-move pivot, good until his own late-afternoon kickoff; a questionable starter in
  the week's earliest game at a position with no surplus and no same-position bench body,
  where clause 3 finds no cover and the no-cover call is made before the earliest game locks,
  the pool checked first; and the chain, a surplus position's fixed-slot starter scratched
  with no earlier flag while the flex holder is still unlocked, covered in two moves good
  until the scratched starter's own kickoff, with the reason clause 1 redoes that arrangement
  the moment a flag lands while both are unlocked. Bench coverage by window (a pivot counts
  only if his game kicks off no earlier than the moment the news arrives; a bench body in the
  last game of the week is insurance for every earlier slot; the free-agent pool is a pivot
  source until each pool player's own kickoff and is checked before any starter takes the
  no-cover call; a bench body named as the pivot for two risks is said as such, since he
  covers whichever is ruled out first); the no-cover deadline; the week as a table of what is
  read on each day and what comes out of it, with the host's own projections and lineup
  suggestions gated by section 5's settings test, its start and roster rates reading the
  room, not the player, and surviving that test as section 4 says, and the day's inactives
  and injury tags read off the host's roster page; and the common mistakes: starting on
  reputation instead of projection and usage, overreacting to one week, ignoring the game
  script, starting a questionable player with no pre-decided pivot, overweighting weather, a
  healthy early-week starter parked in the flex, and comparing more than three players for
  one slot.

### Changed

- Section 8's Post-waivers bullet carries the same ordered rule, clause for clause in the
  same sentences, the two-risk naming rule and the same no-cover deadline. The league is
  re-synced in the engine before the Team Dashboard is read, since a stale sync has been seen
  omitting the newest adds and drops; the host's own team page prints each player's kickoff
  and every player locks in place at his own; a bench player whose game has started is
  nobody's substitute. The bullet points at the new reference, as the lock-morning bullet now
  does.
- Section 8's Lineup lock morning bullet: every swap is decided and said before the first
  window locks, the pivot takes the VACATED slot and a body of another position covers a
  fixed slot only through the chain, the inactives about ninety minutes before each kickoff
  are the last read, and the host page is re-read before any lineup is called set. The bare
  "inactives check" it replaces said neither when to read them nor what to have ready.
- Prime directive 1 now reads "never touch a control on the host's pages that makes or
  proposes a pick or a roster change: accept, reject and counter included; a filter, selector
  or view that only changes what a page shows is a read." It named picks and roster moves
  only, which covered no trade control at all, since a reject and a counter move no roster;
  written wider it would have forbidden the all-teams selector and the filters the
  transaction watch runs on (`references/transaction-watch.md`). The trade bullet ends "The
  user decides."
- Section 7's room-trends line carries the posture that was section 2's: "read them, never
  follow them; exploit them, never chase them; play to beat the room, never keep pace with
  it." It sits where the room is actually read; section 2 keeps the voice.
- Section 6's step 6 says the USER submits the Personalized Advice questions, matching
  section 8's high-stakes bullet, which now reads "draft a Personalized Advice question for
  the user to send".
- The frontmatter description is unchanged: it already opens on ANY fantasy football work and
  names start/sit decisions, so a "set my lineup" request fires the skill without an edit.
- Paid for inside the 500-line body, which ends where it began, at exactly 500. No rule,
  exception, condition or number was removed; what went was restatement, pointers to rules
  stated in full elsewhere, and illustrations of rules the same sentence defines. Section 3
  drops "Starter bye protection is a disclosure default, not a veto", which is what section
  7's bye check does in full (say the stack, name the best non-stacking candidate, give the
  top row when every candidate stacks, and the user decides), and "Treat analyst advice and
  pre-draft plans as priors to update, never as directives to execute", which is its own
  paragraph's lead (every input is a data point, none is gospel; no single signal outweighs
  another by default). Section 4 drops the one-line Personalized Advice bullet, whose two
  halves are now the tier gate in the Subscription tier section, step 6 and the high-stakes
  bullet; its host-subscription paragraph keeps the snapshot caveat in fewer words. Section
  5's reload bullet keeps the rule (the live pick ticker and roster panel are trusted over
  the rankings list) and drops the reason clause, which `references/field-behaviors.md`
  holds. Section 6's step 0 is shortened to the same two confirmations; its step 9 merges the
  refresh-first sub-bullet into the recency sub-bullet, every clause kept (refresh first,
  sweep only what is newer than that refresh, inside the last seven to ten days); and its
  step 10 goes, its two triggers folded into section 8's IR bullet, which already carried the
  cadence and now reads "on demand any week, on waiver eve, right after each draft to name
  the candidates, and again when the undrafted pool clears". Section 7's snipe paragraph
  drops "A public room drafts straight off that list, so its next names weigh as one input,
  never a directive" (the data-point rule is section 3's, the observation is in the
  field-behaviors reference, and the paragraph still says the forecast is not a promise) and
  the sample wording of the one-line call, the one-line rule itself unchanged; its bye check
  keeps "the plan's bye map is the input" and drops "not a substitute", which the same
  paragraph enforces by requiring the check at every starter-slot name; its bench-round read
  drops the two illustrations of a hoarded and a short position, the two-line read unchanged;
  and its sweep paragraph shortens the gone-claim rule to "one look at the engine's board or
  the pick tape and nothing more", since the same paragraph already says the name stands
  unless verification shows him drafted, and the at-the-clock paragraph says what counts as
  that evidence. Section 8's waiver-eve bullet drops "Mind the DROP side", which the
  replaceability test runs on every add-or-drop and states for each side; that test now says
  the cost is read from the host's row "never the engine's Free Agent Finder, which does not
  tell a free agent from a player on waivers and carries neither"; its IR bullet drops "A
  drafted stash costs the pick alone: the bench slot comes back at the IR move", which
  section 7's dart paragraph states in full and the IR reference repeats, and drops "Order
  the pool by the knowledgebase read, the projection said beside each name", which is section
  10's rule for every name in a decision, a stash named among them, and the IR reference's
  own ordering section, and its closing pointer still reads "Sources, tags and the full
  procedure"; its transaction bullet says "the market's read, a data point only (section 3)"
  for the same rule; its bye-week bullet is unchanged. Section 9 keeps the user-agnostic rule
  as one clause. Section 10 drops "and none of it can be looked up on a live clock unless it
  is already written down", the reason for a knowledgebase the sentence goes on to require
  and whose live-clock rule the section's closing paragraph states, and the three examples of
  which file answers which question, which `references/knowledgebase.md` maps in its search
  section; the rule to search the files rather than browse them is unchanged, and so is the
  schedule-tables parenthetical. Three items left the body: section 4's Personalized Advice
  bullet, section 6's step 10 and step 9's refresh sub-bullet, each folded into a bullet that
  already carried its rule. Nothing else was added, removed or reordered; the paragraphs the
  version touched were rewrapped at the file's width with their words unchanged.

## [1.40.0] - 2026-09-09

**The report's clear date was a day early, and the host's own label was being read as a day
late. A host's waiver period does not start when the player is dropped: it starts the
following calendar day in the host's time zone, runs the league's waiver days, and the host's
overnight processing run the MORNING AFTER it ends is what makes him a free agent or hands
him to the winning claim. With two waiver days that is the drop date plus three, whatever the
clock time of the drop, and it is the date the host prints on a waived player's status label
and in the pending block of the user's team page. The script printed the drop date plus the
waiver days and called it the clear date, which is the LAST waiver day, one day before anyone
can have him, so the copilot advised acting a day early and read the host's label as meaning
a day later than it did. Dates worked out in prose were wrong too, a weekday misnamed and a
date off by one. Now every date the report prints carries its weekday, the dropped section
says `arrives <Wkd date>`, and the script answers a waiver window on its own from one date.**

### Changed

- `scripts/transactions.py` prints every date as its weekday and ISO date, `Sat YYYY-MM-DD`:
  the dropped section's drop date, its "since added by ... on" date and its arrival date, the
  managers table's last-move column, the added-in-two-leagues entries and the Yours table's
  date column. The columns, the section names and everything else printed are unchanged.
- The script gains a one-date mode, `--drop YYYY-MM-DD --days N`, that reads no files and
  prints four lines: `today`, `dropped`, `on waivers <first> through <last>` (`on waivers:
  none` when the days are 0) and `arrives <date> at the host's overnight run`. `--days` is a
  whole number 0 to 7 and is required with `--drop`; `--dir` is not needed, `--since` and
  `--league` are refused with a message saying they belong to the report, and `--days` is
  refused without `--drop`. A date that is not real stops the run, as bad input does
  everywhere else in the script.
- Section 8's transaction watch bullet: the report's arrival date follows the host's rule
  (the period starts the day after the drop, runs the league's waiver days, and he arrives at
  the run the morning after it ends), and his row on the host is re-read before a claim is
  filed. It no longer says the date is arithmetic that the host's row overrides, which read as
  permission to guess the real one.
- Section 8 gains a date rule: every date the copilot says carries its weekday and comes from
  the script's `--drop` mode or from the host's row, never from arithmetic in prose. The
  host's status label on a waived player IS the day he arrives, and the team page's pending
  block carries the same date for a filed claim. Where the host's weekly-waiver setting puts
  unclaimed players on waivers at their game's kickoff, a free agent whose game has started is
  a claim until that weekly run, not an add, and which setting the league runs is read once
  from its settings page into the private document.
- "Clear date" is now "arrival date" in section 8's replaceability test and IR stash bullet:
  one name for the one date, the day the player can actually be had.
- `references/transaction-watch.md` documents the arrival date and the host rule behind it,
  the weekday format every date is printed in, and the `--drop` mode with what it refuses.
- Paid for inside the 500-line body by cutting restatement and illustration only, with no
  rule, exception, condition or number removed. Section 6's step 4 drops the reason clause
  "those rooms draft off the news feed, and ADP lags the feed by days" into a shorter form of
  the same sentence, and drops "so a stack with an earlier pick is visible before the clock,
  not discovered after", the reason for a bye map the sentence still requires and section 7's
  bye check still calls the input. Step 9's two sub-bullets on fresh-versus-priced are merged
  into one, every clause kept: tag it, cross-check it against the engine's value before it
  earns the label, actionable only if the value has not caught up, say "already priced" not
  "riser." That step also drops "never as a replacement for the paid engine" and "Ignore old
  news as an edge", both stated by their own bullets (the engine is PRIMARY and web news the
  supplement; older news is already in the number and the room's ADP). Section 7's dart
  paragraph drops "and the grade cost is said (the grade-cost rule below)", which the
  grade-cost paragraph states for any pick over the top live row. Section 8's free-claim
  bullet merges "in preference order" with "Order by value" into one clause and drops "the
  user files them" (prime directive 1: the user clicks every roster move) and "Never in a
  FAAB league, where every claim spends budget", which is the bullet's own opening condition,
  a rolling priority list with no FAAB. Its trade bullet drops one "scored to the synced
  league" (section 5's settings test) and its bye-week bullet drops "buying the player the
  room undervalues and selling the one it is chasing", which is what trading into their
  overreactions is, and what section 7's room-trends paragraph says of value the room leaves.
  The replaceability test drops its two examples of a replaceable position, a class the same
  sentence defines and the knowledgebase rows at the end of the bullet name. The IR bullet
  drops "where the setting is off, that add needs an open bench slot first", stated three
  sentences earlier in the same bullet, and "At the draft section 7's board test and dart
  forecast decide the order", which is section 7's IR paragraph in full. Section 10 drops the
  restatement of name-first and the two-line limit on a live clock, keeping the pointer to
  section 7, which is where both live. Several paragraphs were rewrapped; no heading, bullet
  or numbered item was added, removed or reordered except the one new bullet in section 8
  and step 9's two sub-bullets merged into one.

### Fixed

- The dropped section's estimated date was the drop date plus the league's waiver days,
  labelled "clears". That is the last waiver day, one day BEFORE the player can be had. It is
  now the drop date plus the waiver days plus one, labelled `arrives`, and the script's
  docstring states the rule it comes from: the period starts the day after the drop in the
  host's time zone, runs the league's waiver days, and the host's overnight run the morning
  after it ends delivers the player. Every undrafted player follows the same rule where the
  post-draft setting sends undrafted players to waivers, so the pool clears on that date too.
- Dates the copilot worked out in its head, and said without a weekday, have been wrong in
  both directions. Every date now comes from the script or the host's row and carries the
  weekday that proves it.

## [1.39.0] - 2026-09-08

**One rule the copilot had in the file and did not run, and one it did not have, both on a live
clock. A turn is two picks with a long gap behind the second one, and the pair has to be
planned against that gap: taking the engine's top row at the first pick spent it on a need that
survives the gap, while two starting slots whose tiers were ending did not get filled and one
of them was gone two picks later. And the tie-break layer lists age and depth-chart role but
not the injury flag the engine puts on the row, and it said when to SAY the tie-break without
ever saying when to RUN it. Both are now written as what the copilot does. The wait cadence
gains its missing number and the shape of the message at the clock: inside two picks it is one
ten-second wait per read, and the clock confirmation goes out first, off a read taken the
moment the host shows the clock live, with the name bold and alone on the first line.**

### Changed

- Section 7's tie-break paragraph adds the injury flag the engine shows on the row to the
  judgment layer's inputs, beside age and depth-chart role, and fixes when the layer runs:
  inside the band it is RUN before the name is said, never after. A flagged player in his
  thirties is never named by default over a clean candidate inside the band; the layer
  decides between them and the second line says why whenever the name is not the top row.
- Section 7 gains a turn-pair rule, its own paragraph after the tie-break. Two of the user's
  picks with up to two opponent picks between them are planned as a pair against the gap
  behind the second pick, not row by row: the starting needs whose tier ends inside that gap
  fill the pair, ordered by the snipe-first forecast (the one least likely to reach the
  second pick goes first), and the top row at the first pick is taken only when the pair
  holds no need, or one need that reaches the second pick by that forecast. Filling the first
  pick this way comes before the research-target rule and the tie-break; when the pair rule
  leaves the top row standing, both run as usual.
- Section 5's wait-batch bullet fixes the length inside two picks at ONE ten-second wait per
  read, and states the message at the clock: the confirmation is the first text sent, off a
  read taken the moment the host shows the user's clock live, the name bold and alone on the
  first line. It points at section 7 for name-first instead of restating it.
- Paid for inside the 500-line body by cutting restatement only, with no rule, exception,
  condition, cross-reference or number removed. The requirements' browser bullet drops the
  positive half of a conditional ("real-time recommendations exist only if Claude can SEE the
  draft room and the DS panel"), which the sentence after it states in the negative. Section
  2's posture line drops the two clauses restating section 7's snipe-first and research-target
  rules, keeping the posture and the pointer. Section 3's bye paragraph drops "a value that
  already includes the bye is not a warning the user has heard", which restates "3D folds
  byes into its number silently" in the same sentence. Section 6's injury sweep drops "five
  rules, because skipping them dresses correctly-priced players as edges", which its own last
  sub-bullet states as a rule. Section 7's opening drops "and the name is said as the plan's,
  not the engine's", which is what the DS-lags rule it cites in the same clause says. Section
  7's room-trends paragraph drops "at the clock the call is still one name" (its section's
  opening: one name per call) and "changing the plan takes the discussion" (the same
  paragraph, two sentences earlier: never changes the plan silently, the user decides before
  the clock). Section 7's research-target paragraph drops "once he is gone no later pick
  replaces him", which taking him at THIS pick instead of betting he survives to the next
  already implies. Section 7's sweep-name paragraph drops "a reversal at the clock produces a
  pick nobody chose", the consequence its own heading states. Section 7's dart paragraph
  drops the sentence repeating the IR paragraph above it, now a pointer to it, and
  "contention on kickers and defenses is low", which the pool-count sentence after it states
  as a number. Section 7's room-trends paragraph also drops its three examples of value left
  on the board, and the grade-cost paragraph drops its four examples of a pick over the top
  row (the list 1.13.0 extended with the stash and the dart): "any pick over the top live
  row" covers all of them. Section 7's opening drops "a name given early gets sniped into a
  scramble", one of three reasons for a rule the sentence still states, and the tie-break
  paragraph drops "and not after the user asks", which "before the clock" already says, and
  the bench-rounds paragraph drops "a floor-only bench buys no ceiling", the reason for a rule
  the sentence still states.
  Several paragraphs were rewrapped; apart from the new paragraph and its blank line, no
  heading, bullet or numbered item was added, removed or reordered.

## [1.38.0] - 2026-09-08

**The host setting that 1.37.0 made the condition of the dart rule does not govern the
move the rule depends on. "Allow injured players from waivers or free agents to be added
directly to injury slot" governs POOL PICKUPS only: with it on, a tagged player goes from
the pool into an IR slot on a full bench; with it off, that add needs an open bench slot
first and then the move. It never governs a player already on the roster, who can be moved
from bench to IR in every league. So a drafted stash frees its bench slot after the draft
everywhere, and the dart rule applies in every league, not only on a direct-to-IR host.**

### Fixed

- Section 7's injured-reserve paragraph no longer opens on the host setting. The
  designation costs no bench slot because a rostered player carrying it moves to the IR
  slot after the draft, which every host with an IR slot allows; the add-directly-to-IR
  setting governs pool adds, not this.
- Section 7's dart paragraph loses the same opening condition. The user moves the stash to
  IR after the draft in every league, so the last kicker or defense pick is a dart in every
  league. As written, 1.37.0 excluded the leagues the rule applies to.
- Section 8's IR-stash bullet is rebuilt on the real distinction, drafted versus pool. A
  drafted stash costs the pick alone, since the bench slot comes back at the IR move. A pool
  stash costs a bench player only where the setting is off, where the add needs an open
  bench slot first and the move follows; with the setting on it goes straight to IR on a
  full bench. "An open IR slot is filled, never held" is now host-independent, with the
  open-bench-slot precondition stated for the pool case. The burn-the-claim test is
  unchanged.
- `references/ir-stash.md` gains a "What the host setting governs" section stating the
  mechanism in full once: the setting's own wording, that it governs pool pickups only,
  what changes when it is off, and that it never governs a rostered player. The value test,
  the filled-never-held section and the settings-to-record list are corrected to match.

### Changed

- The dart rule gains its timing: the skipped position is added at the clear, never on a
  claim while the user's priority has value. Contention on kickers and defenses is low, and
  a claim that costs priority buys nothing the clear does not. Scoped to section 8's
  free-claim bullet as well as its burn-the-claim test, since a claim from last priority
  costs nothing and the post-draft state after drafting from the first slot is exactly
  that.
- Paid for inside the 500-line body by cutting restatement, no rule removed or weakened:
  section 8's transaction-watch bullet also shortens "whose reading of the host's own row
  governs the real cost and clear date" to a pointer, since the replaceability bullet below
  it states that the cost and the clear date are read from the host's own row;
  section 3's bye paragraph drops the clause restating section 7's bye check and a pointer
  to the paragraph directly below it; section 4's host-subscription paragraph drops the
  settings-panel test section 5's first bullet states in full and the half of its snapshot
  sentence the tier-gates paragraph it cites already carries; section 6's import audit drops
  a restatement of section 4's Adjust Projections rule and the live-editor-wins half of its
  snapshot sentence; section 6's post-draft IR sweep drops the clear-date instruction
  section 8's own bullet ends on; section 7's dart paragraph drops "the risk is the room's,
  not the position's", which the pool-count sentence after it states as a number; section
  8's IR-stash bullet drops a sentence restating section 7's board test, keeping the
  pointer; section 10's opening drops a sentence saying the knowledgebase is read beside
  the engine, which the same section states twice more and section 8's trade bullet a third
  time. Six paragraphs were rewrapped to the file's wrap width, and the section 7 and
  section 8 paragraphs that changed.

Why: 1.37.0 read the host's help text for the pool-pickup case and wrote it in as the
condition for the roster-move case. They are different mechanisms. The roster move has no
setting behind it at all, so the rule that turns a drafted stash into a free roster spot,
and the last kicker or defense pick into a dart, holds in every league with an IR slot. A
condition that excludes the leagues a rule applies to is worse than no condition: it reads
as a check the copilot must pass, and it fails it in rooms where the play is available.

## [1.37.0] - 2026-09-08

**A drafted IR stash does not really cost a bench body for the season. On a host that
allows an injured player straight to the IR slot, the user moves the stash to IR after the
draft, its bench slot empties, and the roster goes one body short of full at that move.
That empty slot is filled for free when the undrafted pool clears, so the last kicker or
defense pick is better spent on a bench dart: skip one position per drafted stash, take the
position the pool holds fewer of, and add the skipped one free at the clear.**

### Changed

- Section 7 gains a paragraph after the injured-reserve one, since it is the same fact read
  forward: where the designation costs no bench slot, the roster the draft ends with is one
  body light, and the pool fills that slot at the clear. So one position is skipped and the
  pick becomes a bench dart. One position per drafted stash, never more, since each further
  add would need a drop.
- Which position is skipped is decided, not left open. Take the one the pool holds fewer of,
  and add the skipped one free when the undrafted players clear.
- The risk is stated as a number the copilot can compute in any room, not as a rule of thumb
  about kickers and defenses: thirty-two minus the number of teams, less one for every roster
  that drafts a second at the position. Ten teams leaves 22 of each in the pool, at positions
  half the room streams anyway, so the move is near free; a bigger room, or one that doubles
  up at the position, is a different number, and the copilot says the number rather than the
  slogan. The user decides, and the grade cost is named under section 7's existing grade-cost
  rule.
- Section 8's IR-stash bullet is reconciled with it: the value test still applies when the
  stash costs a bench player, but on a direct-to-IR host a draft pick costs the pick, not a
  season-long bench body.
- Paid for inside the 500-line body by cutting restatements, no rule removed: section 2's
  posture paragraph drops the sentence restating section 7's snipe forecast; section 3's bye
  paragraph drops the superflex example and the slot-by-slot list that section 7's bye check
  states in full, keeping the disclosure-not-veto rule and pointing at it; section 4's
  Personalized Advice bullet drops the never-a-directive clause that section 3 already
  carries, and its host-subscription paragraph drops two clauses its own opening sentence and
  section 5 already state; section 6's import audit shortens the snapshot sentence stated
  twice above it and drops a pointer to a reference section 4 already routes to for this
  exact task, its sweep drops a sentence the recency-window bullet above it already says, and
  its post-draft IR sweep drops a clause restating section 8's filled-never-held rule;
  section 7's tie-break paragraph drops a restatement of the one-name rule and its
  sweep-names paragraph drops a rationale clause its own opening paragraph states as a rule;
  section 8's transaction watch drops a two-lines-per-name pointer belonging to section 10;
  section 10's opening drops a pointer sentence after the rule it points at, and its refresh
  rule drops the list of decisions that "every decision" already covers. Twelve paragraphs were rewrapped to
  the file's wrap width, the nine cut paragraphs and three with no word changed.

Why: the copilot priced a drafted stash as if it took a bench body all season, and on a
direct-to-IR host it does not. It takes the pick and then gives the slot back, which means
every draft on such a host ends with a free roster spot the user has already paid for and a
last pick spent on the most replaceable position on the board. The fix is not "skip the
kicker": it is to compute the room's own pool count first, skip only one position per stash,
and say what the empty slot costs on the grade before the user decides.

## [1.36.0] - 2026-09-08

**Where a league's waiver priority is a rolling list rather than a budget, the team
holding LAST priority pays nothing for a claim: a win leaves it last, which is where it
already was, and a loss changes nothing. So while the user holds last priority every
claim on an upgrade is free, and the play is a claim on every player in the pool who
would improve the roster, not a claim on the single best one.**

### Changed

- Section 8 gains a "Last priority makes every claim free" bullet, placed ahead of waiver
  eve because it governs every claim and not only stashes. Where a successful claim sends
  the claimant to the back of a rolling priority list and no budget is spent, the team
  holding last priority pays nothing: a win leaves it where it already was and a loss
  changes nothing. While the user holds it, the play is a claim on every pool player who
  would improve the roster, in preference order, a drop named for each where the roster is
  full, and the user files them.
- The same bullet carries the two guards that keep the rule honest. The priority rank is
  read from the host's own team page and never inferred from the draft slot, because other
  teams' claims move it. A claim on a player who would clear to free agency unclaimed
  costs the same nothing but gains nothing either, so the list is ordered by value and the
  drops named are the roster's true last bodies; who earns a bench slot stays the
  replaceability and IR-stash tests' call, and this rule settles only the cost. The window
  opens after a draft from the first slot, initial priority being inverse draft order, and
  after every claim the user wins; it closes when a team above the user wins one and the
  user's priority regains value. It never applies in a budget league, where every claim
  spends.
- The burn-the-claim test in section 8's IR-stash bullet now states that it governs only
  while the user's priority has value, and points at the new bullet.
- Paid for inside the 500-line body by cutting restatements, no rule removed: section 4's
  host-subscription paragraph drops a clause naming the two rules that already claim the
  sharp ADP for themselves and compresses a sentence that restated its own opening;
  section 5's reload bullet drops a verification sentence section 7 states in full while
  citing section 5; section 6's import audit drops the inverse restatement of its own
  first half, and its sweep step drops a partial file list that section 10 requires in
  full for every name; section 7's snipe forecast drops a repeat of the inputs named one
  sentence earlier and keeps its never-a-directive guard, and its research-target rule drops
  a restatement of section 4's reading of the odds column; section 8's waiver-eve bullet
  drops "said beside the engine's projection, never instead of it", a standing rule of
  section 10, its transaction-watch bullet drops a sentence describing report output the
  cited reference documents, and its IR-stash bullet drops a restatement of its own bolded
  "filled, never held"; section 10's opening drops a sentence of scene-setting and
  shortens the never-collected parenthetical to the pointer at the reference that holds
  that list. Three paragraphs in section 10 were reflowed to the file's wrap width with no
  words changed.

Why: the copilot had one cost model for a claim, the burn-the-claim test, and it assumed
priority was worth something. In a rolling-list league the team at the bottom is the one
case where it is not, and treating a free claim as if it cost something leaves upgrades on
the wire for nothing gained. The window is narrow and it closes without announcement, so
the rule carries its own end condition and reads the rank from the host rather than
assuming it from where the user drafted.

## [1.35.0] - 2026-09-07

**An incoming trade offer is now read for what it fixes on the OTHER roster before any
number is compared: his bye map, his quarterback situation, his thin position, and the
schedule between now and the next time the two rosters meet. The math comes second and
all of it sits beside the engine, and a one-for-one at the same market price that the
engine grades even is the shape to distrust rather than the shape to accept.**

### Changed

- Section 8 gains a "Trade offers: motive before math" bullet, placed before the
  bye-week stretch. Every incoming offer is read first for what it fixes on the offering
  roster: which of his starters sit the weeks the offer's players are off, his
  quarterback situation and the day's news on both teams, the position he is thin at,
  and the schedule between now and the next meeting of the two rosters. An offer from a
  team above the user in the projected standings is read hardest, because an even swap
  that closes his hole is a gift to the team the user is chasing, and a bye week he has
  open is kept open.
- The same bullet then names the math, all of it beside the engine and none of it
  instead: the Trade Analyzer grade and rest-of-season number per side scored to the
  synced league, the host evaluator's week-by-week differential as a data point (the
  season total hides the bye swing it shows), the Injury Predictor row per player,
  section 7's bye check run on the incoming player against the user's starters at his
  position, the first bench body there and the flex, and section 10's full read on both
  players. When the engines tie, section 3's judgment layer decides, one line per input.
  The answer leads with accept, reject or counter, gives the reason in two lines and
  names a counter in one line with what it prices in; the user decides and clicks, and
  the copilot never touches an accept, reject or counter control.
- Paid for inside the 500-line body by tightening restatements, no rule removed:
  section 8's transaction-watch, replaceability and IR-stash bullets drop wording that
  repeated a rule already stated in the same bullet or in the file it cites; section
  10's full-read paragraph drops two sentences that restated its own bolded rule and one
  duplicate of "neither ahead of the other"; section 10's opening drops a clause of
  scene-setting; section 6's advice-question step drops a parenthetical that repeats
  section 4's "the copilot drafts, the user sends"; section 5's reference pointer and
  section 7's snipe forecast lose descriptions of what they had already said. Six
  paragraphs elsewhere were reflowed to the file's wrap width with no words changed.

Why: a swap can be even on both engines and still be a losing trade, because the value
that moves is not only the player's. A manager above the user in the standings has a bye
hole and a schedule of his own, and the offer that closes his hole opens the user's,
which no season-total grade shows. Reading the offer for its motive first puts that on
the table before the numbers agree with each other.

## [1.34.0] - 2026-09-06

**The name spoken at the clock is now a row the copilot can see on the engine's board at
that moment, and a ranked list that omits a player is no longer evidence he is drafted.
Waiting for the user's turn is done in short batches, because a batch of waits returns
only when its last wait ends and a long one can swallow the clock.**

### Changed

- Section 7's "At the clock" sentence requires a visible engine row: the in-room sync
  panel read by screenshot, or the standalone list reloaded this turn. With no row in
  view when the clock goes live the copilot says "no read" and reloads or screenshots,
  and never names from memory or inference; when the engine is still blank after that
  reload or screenshot the section's DS-lags rule takes over and the name is said as the
  plan's, not the engine's. Absence from a ranked list, the host's own pick suggestions
  included, is never evidence a player is drafted, since such lists rank a tagged player
  low; only the pick tape, the roster panel or the engine's crossed-off board says
  drafted.
- Section 7's "Sweep names ride to the clock" paragraph gives a claim that the named
  player is gone, from the user or from the copilot's read of a host list, one look at
  the engine's board or the pick tape, and changes the name only if that look shows him
  crossed off or picked; a host list's filter has produced a false "gone".
- Section 5 gains the waiting cadence: never more than six ten-second waits in one batch
  between the user's turns, at most three before a read of the host's clock inside about
  five picks of it, one wait per read inside two. Its War Room bullet now takes the
  in-room panel by screenshot as an at-the-clock read beside the reloaded list.
- `references/field-behaviors.md` gains the six observations behind those rules: the
  sync panel is an extension frame whose text is not in the host page's text layer, so a
  screenshot is the read; the host's ranked suggestions forecast the room well and
  census the board badly, hiding a tagged player who is still available; the host's
  autodraft control renders highlighted once the room is live even when off; a re-sync
  before the room opened fetched join order and the engine re-slotted itself at the
  first live pick; a batch of waits returns only when the last ends; and the War Room's
  dead position filters put the kicker and defense rows out of sight, so the host's
  player list finds the candidate and the in-room panel's row is the read.

Why: both failures were the same mechanism, a name spoken from something other than a
live read. One turn named off a list's silence while the highest value on the board sat
undrafted, and two picks went unassisted inside one batch of waits. A rule that can be
satisfied by memory is a rule that gets skipped; requiring a row on the screen, or the
words "no read", makes the skip visible.

## [1.33.0] - 2026-09-06

**The engine's dashboard says who is on the roster, not who is starting. Its Starters
and Bench blocks are the lineup the engine would play, so slot assignments are now read
from the host's own team page and nowhere else. Roster membership and IR occupancy are
still read off the dashboard.**

### Changed

- Section 8's "Post-waivers" bullet splits the dashboard into what it reports and what
  it recommends. Membership and IR occupancy are the synced truth; the Starters and
  Bench blocks are the engine's recommended lineup and not the lineup the user has set,
  so every slot assignment, and with it every bye cover and every statement of who
  covers whom, is read only from the host's own team page. Section 7's bye check is
  cited, not restated: what changed is where its slots come from, not the check.
- `references/field-behaviors.md` gains the observation behind the rule, under "Observed
  engine behaviors": a dashboard whose starters and bench disagreed with the lineup set
  on the host for the same roster, and the wrong bye-cover answer that reading them as
  the user's slots produced.

Why: a bye-cover read is only as good as the slots it is read from, and the dashboard's
slots have been seen to differ from the host's; the host page is the one that is never
wrong about them.

## [1.32.0] - 2026-09-06

**Every room's moves become one report. A new script reads the transactions pulled from
each of the user's leagues and prints what every manager added, dropped and swapped, each
player dropped in the window with an estimated clear date (his drop date plus that
league's waiver period), and the names other managers chased in more than one league.
Section 8 says what the copilot does with each of those, on waiver eve and on demand.**

### Added

- `scripts/transactions.py` (Python 3.8 or later, nothing else). It reads a private
  folder holding `leagues.md` and one pipe-row file per league, de-duplicates the rows
  that repeat when pulls overlap, and prints four sections to standard output: the
  per-league manager digest (adds and drops by position, swaps, last move date), every
  player dropped in the window with what he was swapped for in each league that dropped
  him and an estimated clear date there (the drop date plus that league's waiver period,
  arithmetic and not the host's own processing), the players managers other than the user
  added in two or more leagues (the user's own adds are left out of that count, since the
  section is the market's read and not a list of his own stashes), and the user's own adds
  and drops. A dropped player the same league has since added says so in his entry.
  `--dir` is required, `--since` defaults to seven days before the newest row the run
  read, and `--league` limits the run to one slug. Any line the shape cannot read stops
  the run with the file and the line number, the txn cell included: it is the key that
  pairs a drop with the add that made room for it, so it is required, is never `-`,
  belongs to one timestamp, carries one manager's adds and drops (a trade's rows
  excepted), and holds at most one add and one drop, which is what a host entry is. The
  script surfaces what the rooms did; it does not rate, rank or recommend.
- The row shape's txn is built by the puller from the timestamp, the manager and a suffix
  when the page shows more than one of that manager's entries in that minute. Waiver
  processing batches a manager's claims into a single minute, so the timestamp and the
  manager alone are not unique on the morning the report matters most.
- `references/transaction-watch.md`: what a host's transactions page shows, the browser
  pull method, the shape of the two files, exactly what each section of the report holds,
  and the command. It is a new file rather than a section of
  `references/field-behaviors.md`, which holds the live draft-day observations behind
  section 5 and not a pull method or a file format.

### Changed

- Section 8 gains one bullet, "Transaction watch", after "Waiver eve": the pull and the
  run, then what each part of the report is for. Every dropped name is a candidate and
  takes the full read plus this section's replaceability and burn-the-claim tests, whose
  reading of the host's own row governs the real cost and clear date, the report's date
  being arithmetic on the drop date; a dropped player already picked up in that league is
  shown as such; a drop paired with a same-position add in one transaction is a role or
  injury question for the knowledgebase before anything else; a dropped streaming defense
  or kicker is noise unless the pool is thin; a name other managers added in two or more
  leagues is the market's read, a data point and never a directive; and the manager
  digest reads each room's needs, feeding the bye-week stretch's trade targets and the
  burn-the-claim test's contention input.
- Section 9's list of what the private document holds gains the transactions folder's
  path, which is where the watch reads its rows from.
- README counts eleven shipped scripts and names the new one.

Why: the drop side of the wire is where the other rooms' mistakes land, and the copilot
was reading one league's free agent list rather than every league's transaction page. No
rule about how a candidate is judged changed; the report only puts the names in front of
the tests that already existed.

## [1.31.0] - 2026-09-05

**Three rules a live draft wrote. The first bench body at a position is bye cover, so it
gets the same bye check a starter gets; the host's own ranked suggestions join the inputs
to the snipe forecast, because a public room drafts off them; and a suggestion card that
has rendered its numbers but not its name is not a name to read a player off.**

### Changed

- Section 7's bye check no longer waves bench players through. The first bench body
  drafted at a position exists to cover the starters' byes there and in the flex, so his
  bye is compared to those starters exactly as a starter's would be: a stack is a
  finding, and the second line names the week he covers or the stack. Bodies after the
  first at that position stay unchecked, so the rule adds one comparison per position,
  not a sweep of the bench.
- The snipe forecast takes a fourth input: the ranked pick suggestions the host's draft
  room shows every drafter. A public room drafts straight off that list, so its next
  names weigh in the forecast alongside roster need, the trend and ADP. It is read
  between picks as a data point, never as a directive.
- `references/field-behaviors.md` records a rendering window observed live: for a few
  seconds after a pick lands the sync panel can show its suggestion cards with the 3D
  values and projections filled in and the name and team blank. A value-only card is not
  a name, so the name comes off the reloaded War Room list in that window, and no player
  is ever named from a card whose name has not rendered.

## [1.30.0] - 2026-09-04

**The season comes out of the scripts. Every place a year was typed into a shape the lint
enforces exactly is now derived, so the first build of a new season passes its own lint
with no script edited, and `rollups.py` creates the output folder instead of ending the
build in a traceback.**

### Breaking

- `rollups.py` now requires `--season N`; every saved invocation (a refresh script, a
  REFRESH note) must add it. It is required rather than derived from `--date` because a
  refresh run in January belongs to the season that just ended, not to the calendar year,
  and a season guessed from the date would name the wrong file and read the wrong heading.
  A `--season` that no profile's defence heading agrees with now stops the run before
  anything is written, instead of writing a defence table of `-` cells and exiting 0.

### Changed

- `scripts/kb-lint.py` takes an optional `--season N`. The defence heading
  "## Gives up by position (<year> basis)" and the rookies header's "Vet games missed
  <year>-<yy>" column are no longer hardcoded: with `--season` both are computed from it
  (basis year `season-1`, span `season-3` to `season-1`), and without it both are read
  out of the knowledgebase's own files, taking the value most of the files carry. An
  existing knowledgebase therefore lints unchanged with no flag, a new season's lints as
  soon as its files carry its year, and a single file that disagrees with the rest still
  fails. When a kind of file is present and no year can be read from any of them, or when
  the top two years are tied, the script stops and names the flag rather than lints
  against a guess or breaks the tie by glob order.
- `scripts/build-scaffold.py` builds the rookies header's span from `--season` the way it
  already built the defence heading and the blitz-rate line, so a scaffold and the lint
  agree on the first run of a new season.
- `scripts/rollups.py`: the season sets the coaching file's name and title, the defence
  heading the script reads out of the profiles, the rookies header's span, and the ratings
  file the defence rollup points at. The script also creates `nfl/` when it is not there,
  so the first build of a season no longer crashes on a missing folder.
- All three scripts that take `--season` reject a value below 1900 with `--season must be
  a four-digit year`, rather than computing a basis year from it.
- `scripts/pull-list.py`: the fantasy page's keep rule said a specific year's rosters; it
  now says the coming season's.
- `references/knowledgebase.md`: the templates carry `<season>` and `<season-1>` in place
  of typed years, with a line saying the scaffold writes them and the lint reads them
  back; the layout names `coaching-and-scheme-<season>`; the Build and Refresh steps pass
  `--season <season>` to `rollups.py`; the ratings-basis sentences name the season rather
  than a year. README says what the two scripts now derive. Dated prose about past events
  is left as it stands.

Why: a plugin other people install must not fail its own lint the first time a new season
starts. The shape was enforced exactly while the year inside it was typed in several
files, so the first build of a season would have needed the scripts and the templates
edited together, by whoever remembered that they had to be. No rule changed.

Note for anyone upgrading a knowledgebase built on an earlier version: the scripts are
copied into the knowledgebase's `build/` folder, so the copies and that knowledgebase's
own refresh notes have to be updated together. Copying the new `rollups.py` in without
adding `--season <season>` to the command written in `REFRESH.md` leaves a refresh that
stops on a missing argument.

## [1.29.1] - 2026-09-04

**No rule changes: a sweep review's findings applied as text. Contradictions between
sections reconciled, claims trimmed to what the scripts actually do, stale counts and
dead cross-references corrected, and the skill body cut back below the validator's
ceiling.**

### Changed

- Contradictions: three places said the knowledgebase is read "alongside" or "not ahead
  of" the engine's projection while section 10's rule has the read done first and the
  case and the number said together; all three now say "said beside the engine's
  projection, never instead of it". Section 5's settings-blind rule now carries the
  exception section 4 already states (a host tool the settings panel shows scored to
  this league). Section 6's post-draft IR step now runs the stash procedure at once and
  again on the clear date, which is what section 8 and the reference say.
- Claims the scripts do not keep: the refresh seed is described as seeding the role
  collector from the starters whose absence plan is still open, not "the collectors"
  from every `-` cell (skill section 10, and the sentence removed from
  `scripts/kb-lint.py`'s docstring); README names the nine rollup files rather than
  "every NFL-wide file"; `scripts/pull-list.py --check` no longer claims to check dates;
  the knowledgebase reference names the rollup outputs the script actually writes.
- `scripts/merge-tags.py` reads `data/teams.md` the way the other three readers do, a
  leading and trailing pipe stripped, so a markdown-table row is accepted.
- Stale text: the build's agent count, the burn-the-claim test's contention input (the
  host's transaction trends, per section 4), the joins list, and the location the
  scripts are copied to and run from (the knowledgebase's `build/` folder, in the
  reference's every command and in README).
- Dead cross-references: the draft-time IR value test points at itself and section 7's
  dart forecast rather than a value test section 7 does not hold; `scripts/kb-lint.py`
  and `scripts/build-scaffold.py` cite the templates in `references/knowledgebase.md`
  instead of a `build/templates-lean.md` the plugin does not ship; the refresh's
  runnable form is described as the user's own workflow file; the validator is named;
  and the draft-time comparator names the healthy player the pick would otherwise take,
  which is what "the bench player he displaces" meant at a draft.
- Bloat, every rule kept: the scoring editor's field inventory moves verbatim from
  SKILL.md section 6 to `references/draft-sharks.md` under its own heading, with the
  audit rules and the pointer left in the skill; section 10's prose copy of the
  knowledgebase layout becomes one clause per set; the IR bullet drops the restatement
  of the section 10 read it already points at; and the reference's guide-pass step, its
  build history clauses and README's fill-check paragraph defer to the scripts'
  `--help`.

Why: a sweep review of 1.29.0 read every rule against every other rule and against the
shipped scripts. Nothing it found changed a rule; what it found was text that had drifted
from the rules and from the code, and a skill body 489 lines into a 500-line ceiling with
no room for the next rule.

## [1.29.0] - 2026-09-04

**The draft-season guide pass is a script: extractor agents write JSON tag rows from a
subscriber draft guide, `scripts/merge-tags.py` writes them into the team files' media
reads.**

### Added

- `scripts/merge-tags.py`: `--dir <kb> --outlet "<guide> <date>" --json <rows> [--json
  ...] [--dry-run]`. Each row (team, player, tag, line) lands in the team file's Media
  read table: a known player keeps his row with the tag added, the line appended under
  the outlet label and the Outlets count up one per outlet, not per row; a new player
  gets a row with count 1. The row is matched in two passes over the whole table, case
  ignored -- an exact name first, then the surname with a first name that fits (an
  initial matches a letter; two full first names must match or share three letters) --
  so a near-name higher in the table cannot take a line meant for the player below it,
  and a first name that does not fit is a new row rather than someone else's. A rerun
  under the same `--outlet` string is idempotent: the outlet's fragments and its count
  are lifted out before the new ones go in, so twice equals once. That holds per row the
  rerun names, so a rerun carries the guide's full set: a player the new edition dropped
  keeps the previous edition's line and count under that label, since a row the run
  never touches is a row it never reads. A new date in the label keeps both editions on
  the row. Tags are never removed, because which tag an outlet contributed is not
  recorded. Team spellings come from `data/teams.md`, matched
  exactly first and by substring only when that fits one code; "rookie" is recorded as
  sleeper; pipes become slashes and semicolons commas in the line and the label, so a
  guide's punctuation can neither break a table nor blur a fragment boundary. Everything
  refuses before it writes: a pre-flight pass over the rows, the teams and the tables,
  then every new file built in memory and written only after the last team succeeds.
  Verified on the guide's 368 rows across all 32 files: the second run left the tree
  byte-identical to the first, and each refusal left it untouched.

### Changed

- `references/knowledgebase.md`, Build: step 2b, the draft-season guide pass, names the
  extractor read (at most eight pages per read, JSON outside the knowledgebase), the
  merge command and what it does to a row -- the two matching passes, the count that
  rises once per outlet, the several tag rows a player may hold and which one the lines
  land on, the sanitizing of pipes and semicolons, `rookie` recorded as sleeper, the
  rerun that replaces this outlet's lines and leaves the tags -- and says to rerun on
  each new edition before the season, the guide's full set and not a hand-picked few,
  with the same label to replace the previous edition and a new date to keep both, and
  lists what refuses the whole set before any write.
- README: ten optional scripts.

Why: the guide's tags were merged by a one-off script the first time; the rule that
research is not done until the skill can repeat it puts the script in the plugin.

## [1.28.0] - 2026-09-04

**Rules changed: a host subscription the user holds is read as three data points beside
the engine (sharp-user ADP before a draft, the subscriber draft guide as a media-read
outlet in draft season, transaction trends and the lineup assistant and trade market in
season) and nothing else.**

### Changed

- New paragraph after section 4, "Host subscriptions are data points, not a second
  engine": the host tier is asked for and recorded in the private document; where the
  host offers it, the sharp-user ADP (top-tier users only) is read beside the basic ADP
  before every draft, pulled as a table into `data/` (pull-list table twenty-one,
  cadence before each draft in draft season) and read at the clock by grep, and enters
  the one-round-earlier band and the snipe forecast's ADP input; the subscriber draft guide is one seeded outlet for the knowledgebase's media
  read, its tags recorded like any outlet and its pages never saved as files; in season
  the transaction trends are the contention input of the burn-the-claim test (they read
  the room, not the player); the lineup assistant and trade market are second opinions
  only where verified as scored to the league's settings, otherwise noise under section
  5. The host's advanced-stat and alternative-projection views are not collected even
  when held. The feature list is a snapshot; the live offering wins.
- Section 6 step 4: a name the sharp-user ADP prices earlier than the basic ADP is banded
  at the earlier of the sharp price and one round before the basic ADP, one adjustment,
  not two. Section 7's snipe forecast names the sharp-user ADP as its ADP input where
  the host publishes one.
- `references/knowledgebase.md`: the host subscription's draft guide joins the
  themed-sweep outlets for the media read (pages never saved under `data/`); the kept
  tables become twenty-one with the host ADP table; the never-collected paragraph
  carries the host advanced-stat exclusion so a collector working from that file sees
  it.
- `scripts/pull-list.py`: the host ADP table row, cadence "before each draft, draft
  season only", columns player, pos, team, basic and sharp-user ADP over the last seven
  days; `--check` substitutes the `<date>` placeholder and lists a before-each-draft
  table without requiring it, since it exists only in draft season and only where the
  host publishes a sharp-user ADP.

Why: the user upgraded to the host's top tier and asked that it be used the way the
engine's subscription is used, without adding fat. A survey of the tier found three
features a decision in this skill reads and a set that duplicates what is already held.

## [1.27.0] - 2026-09-04

**Rule changed: the cost of an add is read from the host's own row for that player,
never from the engine's free-agent finder.**

### Changed

- Section 8, replaceability test: the add's cost is named in one of two forms, free
  and instant or a priority or FAAB cost with the clear date, and read from the host's
  row for that player; the engine's Free Agent Finder does not distinguish a free
  agent from a player on waivers and carries neither the cost nor the clear date.
- `references/ir-stash.md`, the free window: the recorded settings give the cadence,
  the player's own host row gives his current status, because a just-dropped player
  sits on a fresh waiver period no recorded setting predicts.

Why: a copilot called two dropped players "free agency, instant" from the finder's add
label while the host's transaction log, already read that morning, showed both on
two-day waivers. The user caught it.

## [1.26.0] - 2026-09-04

**Rules changed: every add-or-drop runs the replaceability test beside the number; a
back or receiver on the successor map holds bench value whether or not the starter is
owned.**

### Changed

- Section 8, new bullet after waiver eve: after the full read and beside the engine's
  number, with the add's cost in priority or FAAB named in the same line, each side of
  an add-or-drop is tagged as re-acquirable from the league's pool later or not. A
  player at a position the pool still holds several of at the same tier (a second
  quarterback in a one-quarterback league, a streaming defense or kicker) can be; a
  player whose value is contingent on an injury or role change cannot, because he is
  claimed the day it happens. The test argues the slot for the one who cannot be
  replaced and says how the replaceable need is met the week it arises; a projection
  gap alone does not settle the call: the gap and the test are both said and the user
  decides. When both sides carry the same tag the test is silent, and how many
  contingent stashes a bench carries is the user's call. The successor map names the
  contingent players: a back or receiver listed under COMMITTEE, or as PRIMARY if the
  starter is out, holds that value on the user's bench whether or not the user owns
  the starter.

Why: with the full read done and every row said, a copilot still let the engine's
projection gap decide a bench slot between a second quarterback and a committee back
who becomes the lead the day the starter is hurt. The user asked the question the read
did not: which of the two can I get back from the pool later.

## [1.25.0] - 2026-09-04

**Rules changed: every name in a decision gets the knowledgebase's full read, said
beside the engine's number; once the draft is over an open IR slot on a direct-to-IR
host is filled from free agency, never held; the IR-eligible pool is ordered by that
read.**

### Changed

- Section 8, IR stash research: the value test (projection beats the best healthy free
  agent and the displaced bench player) now applies only when the stash costs a bench
  player, at the draft or on a host without direct-to-IR adds. Once the draft is over
  (the post-draft clear date included), on a direct-to-IR host, an open IR slot is
  filled with the best eligible RETURNS player
  who has cleared to free agency whenever one exists: the add displaces nobody and the
  later swap is free, so "leave it empty" is never the answer; a candidate still on
  waivers goes through the burn-the-claim flag first, and at the draft the pick is the
  cost so section 7 governs. The pool is ordered by the knowledgebase read (the
  starter's age, status and absence plan, his games missed where the rookies table
  holds it, the coach's stated plan, the stash's own history under that staff, the
  return window) with the projection stated beside it, neither ahead of the other,
  because the projection alone prices the starter staying healthy and scores every
  backup near zero. Both are said per name and the user decides.
- `references/ir-stash.md`: the value test scoped the same way, plus two new sections
  carrying the open-slot rule and the ceiling read.
- Section 10, new rule: every name in a decision (add, drop, stash, start, trade
  side) gets the knowledgebase's full read before the number is looked up, and the
  case and the number are then said together:
  Rooms row, the starter ahead of or beside him, the rookies file, the play caller's
  tendencies and roster fit, the offensive line's impact, the schedule table with
  defense ratings and injured key defenders, and the media read's tags; a row the
  knowledgebase does not hold is named as not held, never inferred. The case is said
  in two lines per name with the projection beside it as the engine's independent
  number, neither ahead of the other; where they disagree both are said and the user
  decides. On a live clock the name still comes first and the two-line limit stands;
  the read is done in the pre-draft plan and refreshed between picks for the names
  still live.

Why: a copilot quoted a backup running back's near-zero projection and advised holding
an open IR slot empty, while the knowledgebase already held the starter's age, his
missed camp, the coach's stated uncertainty about the backup plan and the backup's prior
starts under
that staff. The user made the case the skill should have made.

## [1.24.0] - 2026-09-04

**Rules changed: the division skeptic checks every team, never a sample; a computed
figure carries a parenthetical naming its table, never a filled marker; and "run one
workflow at a time" is withdrawn for file-level pools, which are split across two or
three workflows launched together, while several judgment workflows at once remain a
rate-limit risk.**

Why: the reshape that followed 1.23.0 sampled two teams in each of the eight divisions
(sixteen teams) and found 152 lost facts; the pass over the other sixteen found 276
more, about thirteen per team over the 32. In a table, a computed rank or
share cannot keep the table's input beside it, and the check reads a cell alone. The
harness caps a workflow's concurrency by the machine's cores, so a hundred-file rewrite
in one workflow ran four hours where three ran one.

Changed: build step 3, the vocabulary's computed-figure sentence, the agents section,
and the same sentence in `scripts/check-fills.py`'s docstring, which had kept the old
rule.

## [1.23.0] - 2026-09-04

**Rules changed: the knowledgebase is tables, not prose. Every profile follows a fixed
template, the NFL-wide files are joins a script writes, a refresh writes cells, and the
build has no gap rounds, no critic and no synthesis agents. Twenty source tables are
kept; the fat a decision never reads is on a never-collected list.**

Why: the owner's audit of 2026-09-04 (seven auditors, one skeptic per set) found half
to four-fifths of every profile set to be build exhaust and depth no decision procedure
reads: source URL lists, method notes, gap sections, contract dollars, box-score lines
the engine's projection is built on, the same absence call written four times, and
per-season tendency splits; and the first refresh design (a merge agent per file and a
re-searching skeptic per team, about 115 agents) could not finish inside one session's
search quota. The measured bill was 20M tokens for the build and 52M for the fill after
it; the reshaped build is estimated at 5 to 13M and the weekly refresh under 1M.

New: `scripts/build-scaffold.py` (every profile in its template shape with the team-level
table cells filled; `--ages` fills ages and games missed by name from the fantasy pages),
`scripts/kb-lint.py` (the template, enforced; builds and refreshes stop on it; its last
line counts the open cells in the required columns, the build's progress figure),
`scripts/rollups.py` (every NFL-wide file as a join over the team tables),
`scripts/pull-list.py` (the twenty kept tables, cadence, columns, `--check`),
`scripts/refresh-seed.py` (starters whose absence plan is still open, for the role
collector). The reference's templates section (four table shapes), a rewritten Source
tables section (kept twenty, never-collected list), a rewritten Build (pull, scaffold by
script, one judgment agent per team, one skeptic per division, scripts) and Refresh
(three collectors, division editors, division skeptics, one ratings agent in season,
scripts after), and an Agents section that says which tier does what and why. Five
scripts are new, not four.

Changed: the vocabulary keeps two markers (`[filled <date>: <data file>]`,
`[unverified <date>]`) and drops the rest; skill section 10 says the same in one
paragraph; README lists the nine scripts. `missing-lines.py` and `gap-list.py` stay as
the yardstick for a prose-shaped knowledgebase from the first build.

## [1.22.0] - 2026-09-04

**Rules changed: a cell no public source will ever answer is deleted from the profile,
not marked with a reason. The never-chased list (subscription-only charting, camp rep
and snap counts nobody prints) is stated once under Source tables, and a gap round
spends nothing on it.**

Changed: the `(Gap: <reason>)` marker form is withdrawn; the vocabulary and build step
7 say a never-fillable cell is deleted (the Source tables paragraph says clause by
clause when the line also holds a fact) and that a cell waiting on a statement, a game
or a report keeps its bare marker for the next round. The "not available to a visitor"
paragraph became the never-chased list, with its two carve-outs kept (grade ranks an
article quotes, tools the user subscribes to). The staff profile template lists pass
rate over expectation, tempo, personnel groupings, slot versus outside, designed QB
runs and deep-ball rate as optional, written only when a pulled table holds them; the
line profile lists PFF grades and FTN line yards the same way. Skill section 10 says the
deletion rule in one clause. Owner's rule behind it: good beats
perfect, and a line that says a number is behind a paywall is noise at the clock.

## [1.21.0] - 2026-09-04

**Rules changed: a gap round ends with `scripts/gap-list.py`, which writes every line
that still says a fact is missing, by file, with the reason where a round wrote one,
and that list is the report.**

New: `scripts/gap-list.py` (Python 3.8 or later, nothing else; copied into the season
folder like the other scripts): `python3 gap-list.py --dir . --date <today>` writes
`build/gaps-remaining-<date>.md` and prints the totals. It matches the same lines the
yardstick counts (gap markers, unverified lines, and the unstamped prose forms), so its
total equals the yardstick's and no open line is missing from the report. Build step 7 names it as the
round's last step and says what the report to the user quotes: the yardstick before and
after, the check script's line, and that file, never a marker-count table. README lists
the four scripts.

## [1.20.0] - 2026-09-04

**Rules changed: the gap rounds measure and select with `scripts/missing-lines.py`
and hand every fill agent its own open-line list; the table-copy pass and the search
pass are separate runs of the fill agents; a new table pulled mid-fill sends the data stage back over the
files it answers before any search; and the schedule script reads its team codes from
`data/teams.md` like the validator does.**

New: `scripts/missing-lines.py`, the yardstick (the count of lines that say a fact is
missing, the next round's file list, and one open-line list per file under `build/`).
Four source tables the reference now names, all browser-only: the Pro Football
Reference red zone pages (inside-20, inside-10 and inside-5 splits, which the first
build had marked subscription-only), the fantasy rankings page per season (age, games
played and started, three seasons back), the season index and opposition pages per
season (team plays, sacks, blitz, hurry and pressure rates, prior stops), and the
rbsdm neutral pass frequency table with its season-filter caveat. The browser pull
method is written down: an in-page rewrite of the document body into pipe-separated
rows, then the page text; the three shortcuts that fail are named so they are not
retried. Refresh step 0 states the table cadence: weekly in season for the tables the
games change, once a season for the annual articles and the prior-season pages, and a
new season starts with `data/teams.md`.

Changed: `scripts/schedule-tables.py` carries no team list; it reads `data/teams.md`,
stops with a message when the file is missing or lists a code twice (the validator
now stops on a doubled code too), and lists the rollup's rows in sorted
code order (the 32 team tables are byte-identical to the previous version's output;
two rollup rows move). Build step 7 adds the pilot rule (five files after any prompt
change, read the returns), the rule that the prompt names every marker and prose form
and that a reasoned marker older than a table is re-checked against it, and the rule
that budget-narration lines are deleted rather than left to inflate the count.

## [1.19.0] - 2026-09-04

**Rules changed: the knowledgebase build writes `data/teams.md` before the first pull
(introduced in 1.18.1 under a patch bump, corrected here), and a team spelling is
matched longest-first so a short spelling never claims another team's row.**

Fixed: `scripts/check-fills.py` matched each team spelling separately, so a spelling
that is also the start of another team's spelling (a two-letter city code shared by
two clubs) reached the other club's rows and let its figure pass under the first
club's line; the rows are now found in one longest-first pass. The `(Gap ...)` tally
counts the reasoned form `(Gap: <reason>)` as well as the bare one, which the gap-round
procedure writes and the tally previously dropped. The script's exit summary names the
teams-file stop.

Changed: the marker vocabulary defines `(Gap: <reason>)`; the "wrapped sentence" rule
in the script, the reference and this log now says what actually happens (only the
marker's own line is read, so a wrapped sentence is checked on its second half alone);
README states the two ways a figure from an unnamed club can still pass (a name only one
row answers to, and a row naming no team) and says what a build does without Python (the
fills are reported as unchecked, the set is not called complete); refresh step 3 no
longer gates Next Gen Stats behind a subscription, matching the source-table list; the
1.18.0 entry's exclusion list matches the shipped reference; the search-quota sentence
no longer names one harness's number. The 1.18.1 entry now says its teams file was a
rules change.

## [1.18.1] - 2026-09-04

Fixed: the 1.18.0 text used real players as examples in the check script's docstring,
in the 1.18.0 entry below and in one line of the knowledgebase reference. The skill
carries no player names, ever: they date, they are nobody's business in a public file,
and an example that names a player reads as a rule about that player. The examples now
describe the shape (a shared surname, a benchmark player on another club) and the
1.18.0 entry is corrected in place. The same rule covers teams: the check script no
longer carries the league's teams and spellings; it reads them from the knowledgebase's
own `data/teams.md` (one team per line, the profile code first, then every spelling the
pulled tables print), which build step 0 now writes, and it stops with a message when
that file is missing. That file is a new required build output, which by this
changelog's own convention is a rules change; 1.19.0 carries the corrected bump.

## [1.18.0] - 2026-09-03

**Rules changed: a knowledgebase build pulls its source tables once, into a `data/`
folder, before any profile pass runs; a profile cell that says a number was not
reached is a table not yet pulled, never a search to run.**

New in `references/knowledgebase.md`, "Source tables": the map of which table
answers which cell and where each comes from. Draft Sharks Fantasy Points Allowed
(points allowed by position, seasons back to 2021), Historical Stats (opportunity
share, red-zone share, target share, end-zone targets, depth of target, yards per
route, dropbacks, QBR), depth charts (the print-all page) and the annual line
rankings article; Pro Football Reference advanced passing, rushing, receiving and
defense (pressure rate, pocket time, blitzes faced, RPO and play-action volume, yards
before and after contact, broken tackles, depth of target, drops, coverage numbers,
missed tackles); ESPN Analytics win rates (all 32 teams, four rates, with ranks);
Sharp Football coverage schemes and defensive tendencies (man, zone, single-high,
two-high, blitz, box, sub package); Sumer Sports team defense (EPA and success rate).
Each is saved verbatim with its URL, pull date, season and column order, and the
list names what stays out for a visitor (PFF grades, FTN line yards and DVOA, Fantasy
Points Data, Sharp Football's book-only splits, Sumer Sports' paid tier).

New: `scripts/check-fills.py` (Python 3.8 or later): after a fill, every cell marked
"[filled <date>: <data file>]" must cite a file that exists, and the sentence carrying
the marker is checked against that file's rows for the player or team that line is
about, not against the file as a whole. The row is found by player name or team code,
read from the line, the heading above it (a markdown heading, a bold-led bullet, or a
plain label line ending in a colon) and the profile's own file name, and matched through
the spellings `data/teams.md` lists for it (another site's code, the city, the
nickname, the full name). A line in a data file that names three or more
different teams is a league-wide list rather than one subject's row, so it is split on
"; " first and only the entry carrying the anchor is searched; without that, ESPN's
player top twenties put twenty teams' numbers within reach of any one of them. A name
several players answer to is held to the teams the line itself names, or to rows carrying
no team, so a shared first name or surname on one club's line no longer reaches the
other players who carry it on other clubs; a name only one row answers to is already one
player and reaches it either way, which is what lets a surname on its own find a
benchmark player under another club's profile. A word inside a multi-word team spelling
is never a name, so a city word two clubs share cannot carry one club's line into the
other's rows. The teams and their spellings are read from the knowledgebase's own
`data/teams.md`, which the build writes; the script carries no team. An all-capitals token is
never read as a player name: the tables print names in mixed case, so OLB and ADOT are
labels. At least one of the sentence's numbers must be in those rows,
sign included, counting both ends of a hyphenated range and no part of a season span or
an ISO date; a line naming no player or team the table covers fails, and so does a
sentence whose subject and figures sit on the line above its marker, because only the
marker's own line is read. A
citation shaped like a file name is a file citation even
when the file's own name ends in a date, so a misspelled or extensionless name fails
instead of passing as a search fill, and a one-word citation naming no saved file fails
with its own message. A depth-chart citation is checked by player name only, searched
across all 32 teams and having no
numbers worth checking, and a file earns that exemption only by carrying `depth-chart`
in its name AND reading like a depth chart (fewer than one row in ten holding three or
more numbers), so renaming a stats table does not buy it. A bracket carrying the word
"filled" in any other shape fails as a malformed marker, and a set whose `data/` holds
tables but whose profiles hold no well-formed marker fails too, so a drifted vocabulary
cannot pass by hiding every cell from the check. The script prints the counts and every
failing sentence and exits 1 on any failure, and when data/ is missing or no profile is
found.

What a clean exit does not prove is written down beside what it does, in the same words
in the README, the skill, the reference and the script's own docstring: not the column a
figure came from; and not the sentence's other figures, since one correct figure carries
a line past every wrong figure beside it, which makes this a check that thins wrong
numbers out of a set rather than one that clears any single line. What it now does prove
is the third item that used to sit in that list: one subject to a line is no longer only
advice, since a shared name is held to the teams the line names. A line that names two
teams is still checked against both, because the coach and line files quote a
coordinator's previous unit on the same line as his current one and no rule of shape
tells those two apart; name the team beside the number when two are in play. One gap is
left in the scoping and is written down with the rest: a capitalized word that is no
player's name but matches exactly one row is admitted as a name, and that row may belong
to a team the line never mentions. The column labels these tables use are listed as
non-names, so it takes an unlisted one to happen.

Also new, in the marker vocabulary: `(Gap)` is now written in place of a number or fact
the pass could not reach, never omitted; `[gap fill <date>]` narrows to a fact that is
not a number from a table, so any number copied from a table carries the filled form
instead; `[filled <date>: <outlet> <date>]` is the form for a cell filled from a dated
search result, counted and never checked against a table; a filled line has to say
whose number it is; and a number the pass computed rather than read (a rank, a per-game
average, a share) keeps the table's own input beside it, because a computed figure is
in no row.

Also new, the gap-round procedure under build step 7, from the first build's fill:
files are selected by the prose that says a fact is missing, not by the marker, and
progress is measured on that same count; one agent per file per round carries the
previous round's open list and reasons, a fixed search budget, and the rule that an
unanswerable cell is relabeled with its reason in place; a file loops only while a
round fills something; the search quota is per session, so rounds are planned across
sessions after the browser-read tables are pulled; the check script runs after every
round; an agent's fetch narration stays in its return value and never in a profile.
The source-table list gains Next Gen Stats passing, TeamRankings, rbsdm team tiers and
the prior-season PFR pages, with the rule that a page the fetch tool cannot reach is
read in the browser, never left as a gap; Next Gen Stats leaves the exclusion list.

Changed: build step 0 pulls the tables before the first profile pass; refresh step 2
runs the check after the merge and refresh step 4 re-pulls the Draft Sharks
points-allowed table for the current season before the ratings refresh; build step 7
fills the gap round from the saved tables first and gates the set on a clean check;
refresh step 3 collects the weekly usage numbers from the box scores and the free
league-wide tables, with PFF, Fantasy Points and Next Gen Stats used only where the
user holds the subscription; "Agents, models and scripts" counts filling a cell from a
saved table as extraction (lower tier, found by grep, never the folder read whole) and
names the check script as its verification.

Why: the first build left 439 cells reading "not reached" or "paywalled" because 130
agents each tried the same handful of tables through a fetch tool that a bot check, a
truncation cap or a sign-up gate stopped, while every one of those tables opened for a
signed-in browser or a plain page load. Pulling each once and handing the profiles
the file closed the cells that the tables cover in one pass.

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
