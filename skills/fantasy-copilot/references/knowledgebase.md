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
4. The NFL-wide cross-cuts are built independently of the dossiers, so they can
   disagree with them; a disagreement is a finding, not an error to smooth over.
5. A critic reads the whole set and lists what is missing or thin, most severe first;
   a gap round fills the high and medium items.
6. A media pass: themed sweeps (sleepers, breakouts, busts and risky picks, rookies and
   up-and-comers, preseason usage and rest, coach statements on roles, injury risk and
   timelines, handcuffs to own), each reading many whole articles, merged into every
   dossier's Media read section, then skeptic-checked.
7. README and the first refresh-log line.

## Refresh (a delta)

Weekly, the morning after the week's last game and before waivers clear; and before
every draft, lineup lock, trade decision, waiver or free-agent move, and roster move.

1. Sweep: per team, "what changed since <last refresh date>", same ground rules, same
   headings, editing in place and marking changed lines with the date. The NFL files
   get the same treatment.
2. Verify: a skeptic re-checks every changed high-impact claim; a patch applies
   corrections.
3. Overlay: for every player whose role changed, read the engine's current value and
   rest-of-season projection (war room or Team Dashboard) and write the gap between the
   new role and the number into the team's Watch list. That gap is the edge; it closes
   within days. Nothing is written back into the engine.
4. Log one line in refresh-log.md: date, trigger, what changed.

The pre-draft sweep in section 6 step 9 becomes: refresh, then search only for what is
newer than the refresh, within the step's own recency window, and read every target
against the successor map, the rookies file and the media read before it earns a band.

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
