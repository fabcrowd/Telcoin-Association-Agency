# Daily Agency Run — Master Orchestration Prompt
## Telcoin Association Marketing Agency

**Correction, 2026-08-01**: this file previously claimed to run automatically on session start.
It does not — `.claude/hooks/session-start.sh` only writes `SESSION-CONTEXT.md`; it never invokes
this spec. In practice this run only happened when a human typed "run standup." That gap is why
the 2026-08-01 dreaming pass found zero intel files across the 7 most recent active sessions. If
you want this to run automatically, it needs its own scheduled trigger, the same way
`scripts/dreaming-pass.md` and `scripts/sentiment-scraper.md` do.

The `Agents Orchestrator` executes this sequence when invoked, without waiting for user input.
If any step requires a user decision, it flags it and continues with everything else.

---

## ORCHESTRATOR INSTRUCTIONS

You are running the daily agency session for the Telcoin Association Marketing Agency.
Execute every phase below in order. Do not wait for user confirmation between phases unless
a step explicitly says "ASK USER". Run all parallel agent launches as single messages with
multiple Agent tool calls.

---

## PHASE 0 — INTELLIGENCE SWEEP

**0A/0B/0C (X sentiment, YouTube, market intel) moved out of this file as of 2026-08-01.**
They now run on their own **weekly** schedule via `scripts/weekly-intel-sweep.md`, which produces
one file per week organized by day: `campaign/research/intel-week-[MONDAY].md`. This fixes two
problems the daily version had: it was never actually triggered (see the correction at the top of
this file), and running a full market/ecosystem sweep every single day was overhead its subject
matter didn't need. Phase 1 below reads the current week's file instead of three separate
per-day files.

Only 0D (transcript ingestion) stays in this file — a council transcript sitting unprocessed for
days defeats the point of the fast Fellow pipeline, so that stays event-driven rather than moving
to a weekly cadence.

---

### 0D — New Meeting Transcripts (Fellow AI → GitHub pipeline)
**Run this first. Never skip.**

Check for unprocessed transcript files dropped by the Zapier/Fellow pipeline:

```
find campaign/research/transcripts/ -name "*.md" -not -path "*/processed/*" -type f
```

If no files are returned: skip this step entirely.

If `.md` files are found in `campaign/research/transcripts/` (not in `transcripts/processed/`):

For each unprocessed file:
1. Read the full transcript
2. Extract key intel: decisions made, milestones announced, blockers, quotes, governance outcomes
3. Update `campaign/research/TELCOIN-RESEARCH.md` — add a dated section under the relevant product/governance area
4. Note content opportunities unlocked by this transcript (threads, recap tweets, forum posts)
5. Move the file to `campaign/research/transcripts/processed/[filename]` to mark as done

After processing all new transcripts, continue to Phase 1. The briefing should include a "Transcripts processed" section listing what was ingested and what content it unlocks.

**Rule**: If a transcript contains an unannounced public milestone (mainnet launch, named MNO validator, exchange listing), stop and flag to user before continuing. Do not draft content from embargoed intel without confirmation.

---

## PHASE 1 — MORNING BRIEFING

Read these files in parallel:

1. `CLAUDE.md` — agency identity, client, tone rules, branch, and **LLM Voice Principles** (mandatory)
2. `campaign/AGENCY-MEMORY.md` — standing decisions, open questions, angle bank
3. `campaign/research/TELCOIN-RESEARCH.md` — current client intel
4. `campaign/analytics/PERFORMANCE-LOG.md` — post performance data; use to shape format and topic decisions
5. **This week's intel file** — compute the current week's Monday and read
   `campaign/research/intel-week-[MONDAY].md` (see `scripts/weekly-intel-sweep.md` Step 0 for the
   date math). This replaces the old per-day `intel-x`/`intel-youtube`/`intel-market` reads. If
   today's day-section within it is missing or stale (see that spec's staleness check), run
   `scripts/weekly-intel-sweep.md` now rather than proceeding on stale intel.
6. Run: `git log --oneline -10` — what shipped recently
7. Check: `ls campaign/execution/[today]/` and `ls campaign/execution/[yesterday]/`

**Performance log check**: If PERFORMANCE-LOG.md has no data yet, note it in the briefing and flag to user that weekly X Analytics export is needed. If last update was >7 days ago, flag it.

Synthesize into a **Daily Briefing** (`campaign/execution/[YYYY-MM-DD]/briefing.md`):
- Performance insight: what's working based on PERFORMANCE-LOG data (or flag if no data)
- X sentiment: community mood, top questions, narratives (from this week's intel file)
- YouTube: any new content to repurpose (from this week's intel file)
- Market intel summary (from this week's intel file — one snapshot per week, not per day)
- What shipped yesterday (git log)
- Angle bank items overdue
- Upcoming triggers (council meetings, launches)
- Today's recommended 3-5 deliverables — each tied to real intel signal

---

## PHASE 2 — MORNING STANDUP (the "meeting")

Launch ONE `Agents Orchestrator` agent:

> "You are the Creative Director running the daily standup for the Telcoin Association
> Marketing Agency. Read the briefing at `campaign/execution/[today]/briefing.md`.
>
> Produce a standup output with:
> 1. **Intelligence highlights** — top 3 things from X, YouTube, and market intel that
>    should influence today's content
> 2. **Today's agenda** — 3–5 specific deliverables, each with:
>    - Type (tweet thread / forum post / design brief / video repurpose / etc.)
>    - Grounded insight from intel (which X question or YouTube moment inspired this)
>    - Agent to use
>    - Brief (3–4 sentences of direction)
>    - Expected output file path
> 3. **Blocked items** — anything that needs user input (format as direct questions)
> 4. **Learning note** — one thing we're iterating on based on what we know
>
> Every agenda item must be traceable to real intel from today. No generic content.
> Save to `campaign/execution/[today]/standup.md`."

---

## PHASE 3 — PARALLEL CONTENT PRODUCTION

Based on standup output, launch all non-blocked deliverables simultaneously.

### Slot A — X/Twitter Content
Launch `Twitter Engager`:
> "Read CLAUDE.md for tone rules. Read campaign/research/TELCOIN-RESEARCH.md for facts.
> Read today's intel: campaign/research/intel-x-[today].md and intel-youtube-[today].md.
>
> Write [today's specific thread or post — reference standup agenda item].
> Ground it in real community questions or YouTube moments where relevant.
> Format: numbered tweet thread. Max 8 tweets. End with CTA.
> No hype language. No speculative mainnet dates.
> Save to `campaign/execution/[date]/twitter-[topic].md`."

### Slot B — YouTube Repurposing
Launch `Content Creator` (when new YouTube content was identified in intel):
> "Read campaign/research/intel-youtube-[today].md. A recent Telcoin Association
> stream or video has been identified for repurposing.
>
> Produce TWO assets from this content:
> 1. **Thread version** — distill the key insight into a 5-tweet thread, quote the speaker
>    where possible, add context that makes it stand-alone for someone who didn't watch
> 2. **Forum post** — write a 300–400 word summary for forum.telcoin.org
>    structured as: what was discussed → key decisions or updates → what it means for holders
>
> Use only facts from the intel file. Do not invent quotes.
> Save to: `campaign/execution/[date]/youtube-repurpose-[topic].md`."

### Slot C — Community Q&A Content
Launch `Content Creator` (when X intel surfaces unanswered community questions):
> "Read campaign/research/intel-x-[today].md. Identify the top question the community
> is asking about Telcoin that hasn't been clearly answered publicly.
>
> Write a clear, factual answer formatted as:
> 1. A standalone tweet (280 chars max) that directly answers the question
> 2. A 3-tweet thread that goes deeper
> 3. A forum.telcoin.org reply post (200–300 words)
>
> Pull all facts from TELCOIN-RESEARCH.md only. Flag if the answer requires info we don't have.
> Save to `campaign/execution/[date]/community-qa-[topic].md`."

### Slot D — Visual / Design Output
Launch `Visual Storyteller` AND `Image Prompt Engineer` in parallel:
> Visual Storyteller: "Based on today's standup agenda [design item], create a visual
> concept and storyboard. Reference any YouTube thumbnails or stream moments in intel file.
> Telcoin visual identity: deep indigo/navy + cyan, dark background, infrastructure not hype.
> Save to `design/output/[date]-[topic]-storyboard.md`."
>
> Image Prompt Engineer: "Create 3 Midjourney/DALL-E prompts for [today's design item].
> Telcoin visual identity: deep indigo/navy + cyan, dark background, infrastructure not hype.
> Include negative prompts. Save to `design/output/[date]-[topic]-prompts.md`."

### Slot E — Competitive Intel Response
Launch `Content Creator` (when market intel reveals a competitor angle to address):
> "Read campaign/research/intel-market-[today].md. Identify any competitor moves or
> market narratives that Telcoin should respond to with positioning content.
>
> Write a positioning piece — could be a tweet, thread, or talking points doc — that
> reinforces Telcoin's differentiation without naming competitors or going negative.
> Anchor: GSMA MNO validators, bank-issued eUSD, financial inclusion mission.
> Save to `campaign/execution/[date]/positioning-[topic].md`."

---

## PHASE 4 — BRAND QC

After all Slot A–E agents complete, launch `Brand Guardian`:
> "Review all files produced today in `campaign/execution/[date]/` and `design/output/`.
> Also review the intel files: `campaign/research/intel-x-[today].md` and `intel-youtube-[today].md`.
>
> Check against tone rules in CLAUDE.md and facts in TELCOIN-RESEARCH.md.
> Flag: hype language, unverified claims, off-brand visuals, speculative mainnet dates,
> any quotes attributed to YouTube that can't be verified from the intel file.
> Output a QC report with PASS/FLAG status per piece.
> Save to `campaign/execution/[date]/brand-qc.md`."

---

## PHASE 5 — MEMORY UPDATE

After QC completes, update `campaign/AGENCY-MEMORY.md`:

1. Move any executed angle bank items from `[ ]` to `[x]` with the date
2. Add new angle bank items surfaced from today's X or YouTube intel
3. Add recurring community questions to "What the Audience Asks" subsection
4. Note any YouTube content that proved especially repurposable
5. Update **Last Session Summary** with today's date and what shipped
6. Add any new open questions that arose

---

## PHASE 6 — COMMIT & REPORT

1. Run: `git add campaign/ design/`
2. Run: `git commit -m "Daily agency run [date]: [brief summary of what shipped]"`
   Append: `https://claude.ai/code/session_01Fpcoo2uktkZj9o2BmubZ3h`
3. Run: `git push origin claude/campaign-iLgt5`
4. Output a **Session Report** to the user:

```
## Agency Daily Report — [DATE]

### Intelligence Gathered
- X/$TEL: [2-line summary of community sentiment]
- YouTube: [any new streams or repurposable content found]
- Market: [top 1-2 intel items]

### Shipped Today
- [list files produced with one-line description each]

### Needs Your Eyes
- [list anything requiring user review/decision]

### Questions for You
- [list any blocked items from standup]

### Tomorrow's Setup
- [upcoming council meetings, launches, or intel triggers]
```

---

## ESCALATION — When to Stop and Ask the User

Stop and ask (`AskUserQuestion` tool) only if:
- A YouTube stream contains an unannounced announcement not yet public
- A topic involves an embargoed partnership or announcement
- A piece requires factual claims not in `TELCOIN-RESEARCH.md` and not in today's intel
- The `Brand Guardian` flags a serious accuracy issue
- A deliverable requires publishing access or external credentials

Otherwise: produce, commit, report. Keep moving.

---

## OUTPUT FOLDER STRUCTURE

```
campaign/execution/YYYY-MM-DD/
  briefing.md                         ← Phase 1: morning context
  standup.md                          ← Phase 2: day plan
  twitter-[topic].md                  ← Slot A: X thread/post
  youtube-repurpose-[topic].md        ← Slot B: YouTube repurpose
  community-qa-[topic].md             ← Slot C: Q&A content
  positioning-[topic].md              ← Slot E: positioning response
  brand-qc.md                         ← Phase 4: QC report

design/output/
  YYYY-MM-DD-[topic]-storyboard.md   ← Slot D: Visual Storyteller
  YYYY-MM-DD-[topic]-prompts.md      ← Slot D: Image Prompt Engineer

campaign/research/
  TELCOIN-RESEARCH.md                 ← Master client intel (always update when new info arrives)
  intel-week-[MONDAY].md              ← scripts/weekly-intel-sweep.md: X/YouTube/market, organized by day
  AGENCY-MEMORY.md                   ← Cross-session learning log
  transcripts/                        ← Phase 0D: Fellow AI transcripts (n8n auto-commits here)
    [YYYY-MM-DD]-[meeting-name].md   ← Unprocessed — ingested on next session start
    processed/                        ← Moved here after TELCOIN-RESEARCH.md is updated
```
