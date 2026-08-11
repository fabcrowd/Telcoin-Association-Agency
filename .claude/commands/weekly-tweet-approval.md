# /weekly-tweet-approval

Generate the upcoming week's full tweet schedule as a single approval document.

**Cadence**: Run every Wednesday for the Mon–Sun week starting the following day (or next Monday if run Friday–Sunday).
**Output**: Saved to `campaign/execution/[week-start-date]/WEEKLY-APPROVAL.md`
**Arguments**: Optional override for week start date (YYYY-MM-DD). Otherwise auto-calculates.

---

## What you must do

### Step 1 — Gather context (run these agents IN PARALLEL before writing anything)

Launch all three simultaneously:

**Agent A — Data Analytics Reporter** (the Telcoin-tuned one at `agency-agents/data-analytics-reporter.md`, not the generic `support-analytics-reporter.md`)
> Read `campaign/execution/` for all posts published in the prior 7 days, AND the most recent 1-2 `campaign/analytics/sentiment/*.json` files (ignore `_seed-synthetic/` and any file whose `data_status` is not `"measured"`).
>
> Identify: (1) best-performing post by engagement signals or explicit metrics if available, (2) worst performer, (3) any format that underperformed its tier expectation, (4) **from the sentiment JSON**: the current sentiment direction (up/down/flat vs. the prior file, with `n_classified` so a small sample is not over-read) and the top 3 open community questions from the `questions[]` ledger with their `times_observed` counts.
>
> Return a 5-line summary: top post, bottom post, format insight, sentiment direction, top open question. If no analytics data exists yet, return "No prior data — defaulting to Content OS baseline." If sentiment JSON exists but post-performance data does not, still report the sentiment and questions — they are the more actionable signal.

**Agent B — Sprint Prioritizer**
> Read `campaign/research/TELCOIN-RESEARCH.md`, `campaign/execution/LEARNING-PATH-TRACKER.md`, `campaign/AGENCY-MEMORY.md`, `strategy/CONTENT-OS.md`, and the current week's `campaign/research/intel-week-[MONDAY].md` (compute the current week's Monday; if the file is missing, note it and proceed on the static research).
>
> Determine:
> (1) **Learning path status** — check LEARNING-PATH-TRACKER.md for which LP post is next across all active paths (LP1 through LP4). Do not infer from CLAUDE.md — read the tracker directly.
> (2) **Governance events this week** — council cadences: Platform & Treasury and TAN alternate Thursdays 4-5PM EST (fortnightly); TELx alternates Wednesdays 3PM EST (fortnightly). Calculate from today's date to identify which councils meet this week.
> (3) **Embargoes and blockers** — read AGENCY-MEMORY.md Standing Decisions section for any content on hold (e.g., content awaiting confirmation, embargoed topics). Do not schedule embargoed content.
> (4) **Active angles** — check AGENCY-MEMORY.md Angle Bank for `[ ]` items ready to execute. Angle Bank items promoted from the community-question ledger (tagged with a `times_observed` count) get priority — they are what the community is actually asking.
> (5) **Live community signal** — from `intel-week-[MONDAY].md` and Agent A's open-question summary: identify the single highest-recurrence open community question. **The proposed mix MUST include at least one slot that answers it**, unless it maps to a `publishable: false` narrative in `campaign/analytics/NARRATIVE-TAXONOMY.json` (`price`, `banking` — listen-only, never scheduled). If the top question is listen-only, use the next publishable one.
>
> Output a proposed 7-post content mix with day/time (EST), type (Governance/Education/Milestone/Community), topic, and one-line structural rationale for each slot. For any slot answering a community question, say so in its rationale ("answers recurring question, asked Nx"). Apply Content OS volume rules for the week type (Standard/Event/Quiet).

**Agent C — Twitter Engager**
> Read `campaign/research/TELCOIN-RESEARCH.md`, `tasks/lessons.md`, and `strategy/CONTENT-OS.md`. Draft the actual tweet text for each post in the week's proposed mix (use the mix from Agent B).
>
> For each post:
> - Write the complete tweet or thread (all tweets numbered if thread)
> - Apply all tone and style rules from CLAUDE.md Voice Principles: no hype language, no em dashes, no false drama, no invented stats
> - Include one Neutral Authority conversation prompt on all non-Tier-1 posts (never "What do you think?" — institutional framing only)
> - Apply entity check: every claim must be attributable to Telcoin Association, not Holdings. Flag any Holdings-adjacent content with `[NEEDS CONFIRM — Holdings]` rather than drafting it
> - Governance posts (Tier 1): no emojis, no contractions, directional CTA only
> - Council meeting notices: use the canonical format from tasks/lessons.md Lesson 9 — no deviations
>
> Do NOT invent stats, dates, or claims not in TELCOIN-RESEARCH.md.

**Agent D — Image Prompt Engineer** *(launch simultaneously with Agent C)*
> Read `strategy/BRAND-GUIDE.md`. For each post in the week's mix (use the topic list from Agent B), generate a Midjourney/Flux/DALL-E prompt for the accompanying image. Every post requires an image — no exceptions. Single tweet posts: one 1200x675px card prompt. Thread posts: one header prompt (1200x675px) + one insert prompt per 2-3 tweets. Apply brand rules: TEL Black #090920 background, Royal Blue #3642B2, TEL Blue #14C8FF highlights, hexagon motifs, glass effects. Include negative prompt. No text in generated images. Format as a compact one-liner per post (not the full 3-variant output from /brand-image-prompt — just the primary dark variant).

### Step 2 — Assemble the approval document

Wait for all three agents to complete, then write the approval document to:
`campaign/execution/[week-start-date]/WEEKLY-APPROVAL.md`

Use EXACTLY the format below.

---

## Output format

```markdown
# Week of [Mon DATE] — Tweet Approval

**Generated**: Wednesday [DATE]
**Week type**: [Standard / Event / Quiet] — [one-line reason, e.g., "TELx Council Tuesday, no major milestone"]
**Total posts**: [N]
**Content mix**: [N] Governance · [N] Education · [N] Milestone · [N] Community
**Learning path progress**: [read from LEARNING-PATH-TRACKER.md — e.g., "LP2 Post 4/10 — LP3/LP4 not started"]

---

## Last Week — Performance Signal

> [4-line summary from Analytics Reporter, or "No prior data — defaulting to Content OS baseline."]
>
> **Applying to this week**: [one sentence on how analytics informed this week's mix or timing]

---

## Schedule at a Glance

| # | Day | Time (EST) | Layer | Format | Topic | Approve? |
|---|---|---|---|---|---|---|
| 1 | Mon [date] | 10:00am | Education | Thread | [topic] | ☐ |
| 2 | Tue [date] | 9:00am | Governance | Single | [topic] | ☐ |
| 3 | ... | | | | | ☐ |

*Check the box or write EDIT/SKIP next to each row, then return this table.*

---

## Structural Rationale

**Why this mix**: [2–3 sentences. Explain the week's overall content logic: why this learning path post comes now, why governance takes X slots, how the mix responds to last week's analytics signal. Be specific — reference the actual posts, not generic principles.]

**Analytics adjustment**: [One sentence. What changed from default Content OS cadence based on last week's data, or "No adjustment — insufficient prior data."]

**Scheduling logic**: [One sentence on timing choices — e.g., "Governance post leads Tuesday to align with 3pm TELx Council; education posts mid-morning Monday/Wednesday/Friday for consistent cadence."]

---

## Posts for Approval

---

### Post 1 — Monday [DATE], 10:00am EST

**Layer**: Education · [LP reference, e.g., LP2 Post 4 of 6]
**Tier**: 2
**Format**: [Single tweet / Thread (N tweets) / Quote tweet]
**Graphic**: REQUIRED — [card type: Header 1200x675 / Insert 1080x1080 / Thread pack]
**Rationale**: [One sentence: why this topic now, why this format]
**60-min launch window**: [Yes — priority post | No]

> **Tweet 1/[N]**
> [Full tweet text]

> **Tweet 2/[N]** *(if thread)*
> [Full tweet text]

> *[Continue for all tweets in thread]*

**Decision**: ☐ APPROVE  ☐ EDIT (note below)  ☐ SKIP
> *Edit note*:

---

### Post 2 — [DAY DATE], [TIME] EST

[Same structure repeated for each post]

---

## Standing Instructions (applied to every post)

- All non-Tier-1 posts include one Neutral Authority conversation prompt (never "What do you think?")
- No hype language, no invented stats, no timing claims without roadmap.telcoin.network link
- No em dashes — use hyphens or rewrite the sentence
- Tier 1 governance: no emojis, no contractions, directional CTAs only
- Council meeting notices: canonical format only (Lesson 9 in tasks/lessons.md)
- Priority posts (Milestones, Votes, Key Education): 60-min launch window applies
- Graphics: use `/tweet-card-brief` for single cards, `/thread-visual-pack` for threads
- Entity check: every post must be attributable to Telcoin Association only — not Holdings, not TDAB
- Block explorer: never reference telscan.io or any specific explorer URL — use generic language

---

## Bulk Approval

To approve all posts as written, sign here:

**APPROVED AS WRITTEN**: _________________________ Date: _____________

*Or mark individual posts above and return this file.*

---

## Analytics Tracking (fill in after publishing)

| # | Published? | Impressions | Engagements | Top reply | Note |
|---|---|---|---|---|---|
| 1 | ☐ | | | | |
| 2 | ☐ | | | | |

*This table feeds next Wednesday's performance signal.*
```

---

## After generating the file

1. Report to the user: "Weekly approval doc ready: `campaign/execution/[week-start-date]/WEEKLY-APPROVAL.md`"
2. Print the **Schedule at a Glance** table directly in the chat response so the user can do a fast scan without opening the file
3. Note any posts that required assumptions (missing research data, ambiguous LP status) so the user can flag corrections
4. Do NOT ask for approval in the chat — the file is the approval mechanism

## Wednesday reminder note

If today is not Wednesday, add a note at the top of the output:
> ⚠ Generated [today's day] — standard cadence is Wednesday. Week assignments may shift if run again on Wednesday.

$ARGUMENTS
