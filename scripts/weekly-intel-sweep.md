# Weekly Intel Sweep — Telcoin Association Agency

Runs once a week as a scheduled trigger. Replaces the old daily Phase 0 (0A/0B/0C) in
`scripts/daily-agency-run.md`, which was never actually triggered — the session-start hook does
not invoke it, and it only ran when a human happened to type "run standup." The dreaming pass run
on 2026-08-01 found zero intel files across the 7 most recent active sessions, confirming this.

Output is ONE file per week, organized by day. "Organized by day" means: **wherever genuine
per-day data exists, section it by day; wherever only a single current-state snapshot is
possible, say so plainly rather than inventing day-by-day granularity that isn't there.**
That rule comes directly from `tasks/lessons.md` Lesson 11 — never manufacture a value (or a
day-attribution) you don't actually have.

## Why this doesn't duplicate `scripts/sentiment-scraper.md`

The daily sentiment scraper already collects X/Reddit/News data with a per-post narrative
taxonomy and writes real, dated JSON to `campaign/analytics/sentiment/YYYY-MM-DD.json`. This
sweep does **not** re-run those searches. It reads that JSON (when present) and synthesizes it
into a readable weekly digest. Same relationship for YouTube: `scripts/youtube-pull.py` /
`infrastructure/n8n/workflow-youtube-to-github.json` pull exact per-video statistics into
`campaign/analytics/youtube/YYYY-MM-DD.json`; this sweep reads that rather than re-fetching the
channel page for numbers it can't reliably parse anyway.

If neither JSON pipeline has data for the week yet (true on first run — both were only built
2026-07-30/31 and haven't accumulated history), this sweep falls back to a single fresh
WebSearch/WebFetch read, explicitly labeled as a **snapshot, not attributable to a specific day.**

---

## Step 0 — Determine the week and find/create this week's file

```bash
TODAY=$(date -u +%Y-%m-%d)
DOW=$(date -u +%u)                                    # 1=Monday .. 7=Sunday
MONDAY=$(date -u -d "$TODAY -$(( DOW - 1 )) days" +%Y-%m-%d)
WEEK_FILE="campaign/research/intel-week-$MONDAY.md"
echo "Week of $MONDAY -> $WEEK_FILE (today: $TODAY)"
```

If `$WEEK_FILE` does not exist, create it with the header template (Step 4). If it exists, check
whether today's day-section (`## $TODAY`) is already present:

```bash
grep -q "^## $TODAY" "$WEEK_FILE" 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If today's section exists and the file's last edit is under 12 hours old, **skip straight to
Step 6 and report "This week's intel is current."** Otherwise continue.

This makes the sweep idempotent regardless of how often the trigger actually fires — if it fires
weekly as scheduled, one section gets added; if a session runs `/weekly-intel` manually mid-week,
it appends that day's section to the same file rather than creating a duplicate.

---

## Step 1 — X/$TEL Community Sentiment (synthesize, don't re-collect)

Check for today's structured data first:

```bash
ls campaign/analytics/sentiment/$TODAY.json 2>/dev/null && echo "HAS_DATA" || echo "NO_DATA"
```

**If `HAS_DATA`**: read the file. Pull `composite.sentiment_score` + `composite.n_classified`
(report both together, never the score alone — a 0.70 from 7 posts and a 0.70 from 200 posts are
different facts), `composite.top_narrative`, any `questions[]` with `status: "open"`, and any
`data_status` other than `"measured"` (flag it, don't use it). This is real, dated, per-day data —
write it under today's `## $TODAY` heading.

**If `NO_DATA`**: check whether ANY sentiment JSON exists for the other 6 days of this week. If
none exist at all, run a single fallback sweep — the original 3 WebSearch calls:
1. `"$TEL" OR "Telcoin" site:twitter.com OR x.com` — last 24h
2. `"@telcoinTAO"` — last 24h
3. One topical search based on what's active

Write the result under a section labeled **"Current-state read (not day-attributed) — $TODAY"**,
not under a day heading that implies it's part of a day-by-day series it isn't part of.

---

## Step 2 — YouTube

Check for today's structured data:

```bash
ls campaign/analytics/youtube/$TODAY.json 2>/dev/null && echo "HAS_DATA" || echo "NO_DATA"
```

**If `HAS_DATA`**: read it. Report new uploads since the last recorded day (compare against the
prior day's file if one exists this week), with real `view_count`/`like_count`/`comment_count` —
never estimated. Cross-reference `campaign/AGENCY-MEMORY.md` YouTube Content Log; skip anything
already logged as repurposed.

**If `NO_DATA`**: the `WebFetch` tool does not work for this — verified 2026-08-01. It converts
the page to markdown before returning it, which strips the JSON data blob the page's content
actually lives in, so it returns nothing but footer/legal boilerplate. If a raw HTTP fetch is
available (`curl` with a normal browser user-agent, not the bare default — that bare-UA 403 was
the cause of seven months of false "blocked" diagnoses, corrected 2026-07-31), video IDs parse
from the `ytInitialData` blob, but titles and view counts still do not — they render client-side
via a `lockupViewModel` and the parse fails silently when YouTube's markup shifts. **Do not rely
on either path for real numbers.** If no structured JSON exists for the week, report plainly that
YouTube data is unavailable this week rather than guessing from a partial page fetch.

---

## Step 3 — Market & Ecosystem (once per week, not per day)

This section is inherently a snapshot — market and competitor news doesn't have the kind of
per-day granularity the sentiment/YouTube JSON does, and running the same broad sweep daily was
wasted overhead. Run this **once per week file**, not once per day-section.

Launch ONE `Trend Researcher` agent in background:

> "Search for the latest news on:
> - Telcoin and TEL token (any press, listings, partnerships, announcements)
> - Stablecoin regulation news (especially bank-issued or CBDC adjacent)
> - Mobile money / remittance market (M-Pesa, Wave, Western Union, Wise)
> - GSMA and telecom blockchain initiatives
> - Competing L1/L2 projects positioning in financial inclusion space (Celo, Stellar, XRP)
>
> Output: 5-8 bullet intelligence items. For each: headline, what it means for Telcoin's
> positioning, and whether it's a content opportunity or a threat to address."

Write the result once, under a single `## Market & Ecosystem — this week (as of $TODAY)` section
near the top of the file. Do not re-run this for every day-section within the same week.

---

## Step 4 — Council transcripts processed this week

```bash
find campaign/research/transcripts/processed -maxdepth 1 -type f -newer "$WEEK_FILE" 2>/dev/null
```

(Or, on the week's first run when `$WEEK_FILE` was just created: list any processed transcript
whose filename date falls within `$MONDAY` through `$TODAY`.) For each, note the meeting name,
date, and what content it unlocked. This has genuine per-day dates — attribute correctly.

Note: transcript ingestion itself (Phase 0D in `daily-agency-run.md`) still runs whenever a
session starts and finds an unprocessed file — that stays event-driven, not weekly, since a
governance transcript sitting unprocessed for days defeats the point of the fast Fellow pipeline.
This step only surfaces a weekly summary of what already got processed.

---

## Step 5 — Write / Append the Week File

Template for a new file:

```markdown
# Weekly Intel — Week of [MONDAY]

## Market & Ecosystem — this week (as of [TODAY])
[Step 3 output]

## Council Activity This Week
[Step 4 output, or "None processed this week."]

---

## Day-by-Day

## [MONDAY]
[if this is today: Step 1 + Step 2 output for this day]

## [TUESDAY]
...
```

Only emit a `## [date]` heading for a day that actually has content (today's, plus any prior days
in the week that already have entries from earlier runs). Do not pre-create empty headings for
future days in the week — that would visually imply data exists where it doesn't.

If today's fallback path was used in Step 1 or Step 2 (`NO_DATA` with nothing to synthesize from),
still create today's `## [TODAY]` heading, but the content under it must say plainly that this is
a snapshot read, not derived from the structured daily pipelines, per the "never manufacture
day-attribution you don't have" rule at the top of this file.

---

## Step 6 — Commit and Push

```bash
SESSION_URL="https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/cse_/session_}"
git add "$WEEK_FILE"
git commit -m "Weekly intel: week of $MONDAY, $TODAY update

$SESSION_URL"
git push origin claude/campaign-iLgt5
```

---

## Step 7 — Report

Output:
- Week file path and whether it was created or appended
- Which sections used real structured JSON vs. a fallback snapshot read
- Any open questions surfaced from the sentiment `questions[]` ledger
- Any new YouTube content flagged for repurposing
- Council transcripts processed this week
- If this was a fallback-only run (no JSON pipelines have data yet): say so, and note that
  richer day-by-day sections will appear automatically once `sentiment-scraper.md` and
  `youtube-pull.py` have run for a few days.

---

## Constraints

- Never coerce a missing value to a fabricated one. `null`/"no data" beats a guess — this is the
  rule Lesson 11 exists to enforce, and it applies here as much as it did to the sentiment schema.
- Never attribute a current-state snapshot to a specific day it wasn't actually observed on.
- Market & Ecosystem intel runs once per week file, not once per day-section — this was previously
  the most expensive step in the daily version and its subject matter doesn't need daily cadence.
- Do not duplicate collection that `sentiment-scraper.md` or `youtube-pull.py` already do. Read
  their output; don't re-run their searches.
