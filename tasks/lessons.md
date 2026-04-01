# Agency Self-Improvement Log
## Telcoin Association Marketing Agency

**Purpose**: Every time the user corrects an output or changes instructions, that correction is logged here as a structured lesson. The pattern is: what was produced → what the user said → what changed → the rule derived. This file is read at every session start and before every content task.

**Update rule**: After ANY user correction, add a new entry at the top of the Active Lessons section immediately. Do not batch corrections. One entry per correction.

**Read rule**: CLAUDE.md Session Startup Checklist step references this file. Read it before producing any content.

---

## Active Lessons (newest first)

---

### Lesson 9 — Council meeting reminder post format

**Date**: 2026-04-01
**Session**: claude/campaign-iLgt5

**What was produced**:
A meeting reminder tweet that listed agenda items with presenters, used a table-based Figma card spec, and omitted the YouTube link, listen-in call to action, and next meetings section.

**What the user said**:
"This is the correct format you should always follow" — then provided the canonical format.

**What was changed**:
- Canonical council meeting reminder format established (see rule below)
- Applied immediately to TELx Council April 1 reminder post

**Rule derived**:
Council meeting reminder posts follow this exact format — no deviations:

```
[Council Name]
[Day], [Month Date], [Year] - [Time] EST / [Time] UTC

Agenda:
- [Item 1]
- [Item 2]
- [Item n]

Listen in on the council call here on X
@TelcoinTAO
or Youtube at http://youtube.com/@TelcoinTAO

Next meetings:
[Council Name]
- [Date] - [Time] EST / [Time] UTC
[Council Name]
- [Date] - [Time] EST / [Time] UTC
```

Rules:
- No presenters listed next to agenda items in the public post
- No emojis, no contractions, no enthusiasm language (Tier 1 governance)
- No conversation prompt
- Always include X + YouTube listen-in links
- Always include next 2-3 upcoming council meetings at the bottom
- Times in EST and UTC
- All councils meet on a 2-week cadence — use this to calculate "next meetings" dates without asking the user

---

### Lesson 8 — Agents must verify facts via web search, not defer to human confirmation

**Date**: 2026-03-31
**Session**: claude/campaign-iLgt5

**What was produced**:
Technical thread produced with [CONFIRM] flags for benchmark figures (HotStuff TPS, Narwhal TPS, Bullshark TPS, Cantina prize pool, findings count) — deferring verification to the user.

**What the user said**:
"Your agents should always be the ones that verify the information with web searches"

**What was changed**:
- Going forward: before marking any technical claim as [CONFIRM], agents must first attempt verification via web search (Trend Researcher or general-purpose agent with WebSearch tool)
- [CONFIRM] flags are for claims that cannot be verified by web search (e.g., internal team decisions, unreleased roadmap details) — not for published academic benchmarks, public competition results, or public partnership announcements
- Cantina competition details, Narwhal/Bullshark benchmark figures, HotStuff fault-tolerance data, Neura Protocol fork status — all verifiable via web search and should be verified before the thread is drafted, not flagged for user follow-up

**Rule derived**:
Agents must run web searches to verify technical claims before flagging them as [CONFIRM]. [CONFIRM] is reserved for information that cannot be found publicly (internal decisions, unannounced partnerships, unreleased roadmap items). Never push a verification task back to the user when a web search can resolve it.

---

### Lesson 7 — Block explorer URL referenced in content before finalization

**Date**: 2026-03-31
**Session**: claude/campaign-iLgt5

**What was produced**:
Tweet 7 referenced "telscan.io" by URL in the published thread.

**What the user said**:
"Don't mention telscan.io as we might use a diff block explorer"

**What was changed**:
- telscan.io removed from tweet 7; replaced with generic "approximately one-second block times on the network"
- Standing rule added: do not reference telscan.io or any specific block explorer URL in published content until the final explorer is confirmed for mainnet

**Rule derived**:
Never reference telscan.io or any specific block explorer URL in content intended for publication. Use generic language ("the network's block explorer", "on-chain") until a canonical explorer URL is officially confirmed for mainnet. This applies to all posts, threads, and forum content.

---

### Lesson 6 — Council transcript received: full workflow
**Date**: 2026-03-29
**Session**: claude/campaign-iLgt5

**What was produced**:
User shared the full P&T Council #34 transcript. A structured recap was produced and committed.

**What the user said**:
"build a recap and commit this to your lessons"

**What was changed**:
- Produced `campaign/execution/2026-03-29/PT-COUNCIL-34-RECAP.md` with chapters, key announcements, Q&A summary, content flags, and usable quotes
- Confirmed research file (`TELCOIN-RESEARCH.md`) already contained P&T #34 intel (updated in a prior session); no additional update needed this pass
- Added this lesson entry

**Rule derived**:
When a council transcript is shared: (1) check if TELCOIN-RESEARCH.md already has the intel — if not, update it first; (2) always produce a structured recap file to `campaign/execution/[today]/[COUNCIL-NAME]-RECAP.md`; (3) include chapters, key announcements, Q&A summary, content flags (cleared vs. hold), and direct quotes; (4) commit both files.

---

### Lesson 5 — Published content not detected during standup review
**Date**: 2026-03-26
**Session**: claude/campaign-iLgt5

**What was produced**:
Standup was run and the P&T Council #34 pre-council notice was listed as "ready to post" — even though the user had already posted it before the standup. The status was never verified.

**What the user said**:
"i already posted the pre council notice and you should have picked that up when we ran standup"

**What was changed**:
- Added to prerequisite review protocol: before producing standup output, check if any content listed as "ready to post" has already been published by checking with the user or reviewing execution files for publish confirmations.

**Rule derived**:
Never mark content as "ready to post" in a standup without asking the user if it has already gone out. If publish status is unknown, flag it explicitly: "Has [post] been published? Marking as pending confirmation."

---

### Lesson 4 — Manual standup run instead of full 6-phase daily agency run
**Date**: 2026-03-26
**Session**: claude/campaign-iLgt5

**What was produced**:
When user typed "run daily standup", a manual standup was produced directly — no Phase 0 intel agents launched, no briefing written, no content production triggered. The full `scripts/daily-agency-run.md` orchestration was skipped entirely.

**What the user said**:
"you should be running all the agents needed for daily standup including the X scraping agent. are you sure you're doing that?"

**What was changed**:
- Confirmed that "run standup" or "run daily standup" means execute `scripts/daily-agency-run.md` in full — all 6 phases — not just produce a text standup summary.
- Phase 0 (3 parallel Trend Researcher agents: X listening, YouTube monitor, market intel) must always run before the briefing.

**Rule derived**:
"Run standup" = full 6-phase daily-agency-run.md. Never shortcut to a text summary. Always launch Phase 0 agents first, then proceed through all phases in sequence.

---

### Lesson 3 — Self-improvement loop was configured but never instantiated
**Date**: 2026-03-25
**Session**: claude/campaign-iLgt5

**What was produced**:
CLAUDE.md referenced `tasks/lessons.md` in the Self-Improvement Loop section since agency setup (March 11). The file was never created. No corrections from any session were being captured.

**What the user said**:
"do you have a self-improvement model taking into context all of my comments? there should be something comparing the first set of outputs, then the 2nd set of outputs and what i asked to change and what you did to change it. this should create a self-improving feedback loop."

**What was changed**:
- Created this file (`tasks/lessons.md`) with all reconstructed lessons from session history
- Added it to CLAUDE.md Session Startup Checklist as a required read
- Added it to the Manual Standup Protocol read list

**Rule derived**:
After EVERY user correction - no matter how small - add an entry here before continuing. The pattern is always: first output → feedback → change → rule. Never let a correction go unlogged.

---

### Lesson 2 — Standup produced without reading context first
**Date**: 2026-03-25
**Session**: claude/campaign-iLgt5

**What was produced**:
When user typed "run standup", the standup was produced using whatever was in the current context window - without explicitly reading SESSION-CONTEXT.md, TELCOIN-RESEARCH.md, LEARNING-PATH-TRACKER.md, and AGENCY-MEMORY.md first.

**What the user said**:
"when i ask to run standup, it needs to research that and context first"

**What was changed**:
- Added "Manual Standup Protocol" section to CLAUDE.md defining exactly what to read before producing a standup: SESSION-CONTEXT, TELCOIN-RESEARCH, LEARNING-PATH-TRACKER, AGENCY-MEMORY, git log, recent execution files

**Rule derived**:
Any standup (manual or automated) must read the full context stack first. No standup from memory. The standup is only as good as the context it's built from.

---

### Lesson 1 — Voice principles not applied to content output
**Date**: 2026-03-25
**Session**: claude/campaign-iLgt5

**What was produced**:
Multiple content pieces drafted (P&T Council pre-post, Adiri release announcement, TAN Council pre-post, TANIP-1 restart announcement) without referencing `assets/LLM Voice principles.docx`. The voice principles were not in any required-read list.

**What the user said**:
"all tweets written need to follow the assets/llm voice principles.docx - this should always be the case and always needs to be in the reference file"

**What was changed**:
- Full voice principles from `assets/LLM Voice principles.docx` embedded inline in CLAUDE.md as a new "LLM Voice Principles" section
- Memory Protocol updated: step 2 now requires reading voice principles before any client task
- Session Startup Checklist updated: step 3 now requires reading voice principles
- `scripts/daily-agency-run.md` Phase 1 updated to explicitly call out voice principles section
- File path `assets/LLM Voice principles.docx` noted as canonical source

**Rule derived**:
Voice principles are non-negotiable for every piece of written content. They are not a style guide to consult occasionally - they are a filter applied before anything is written. If a line would fail "would a real CEO write this?", rewrite it before it leaves the draft.

---

### Lesson 0 — eUSD / TDAB content produced for @telcoinTAO (entity boundary violation)
**Date**: ~2026-03-19
**Session**: claude/campaign-iLgt5

**What was produced**:
LP2 Post 4 was originally planned as an eUSD/TDAB explainer post for @telcoinTAO. Content was drafted or planned covering eUSD and Telcoin Digital Asset Bank.

**What the user said**:
eUSD/TDAB content is out of scope for @telcoinTAO. That account speaks for Telcoin Association (the Swiss Verein), not Telcoin Holdings (the commercial entity that owns TDAB and issues eXYZ stablecoins). Scope updated to TAN / Telcoin Wallet as LP2 Post 4.

**What was changed**:
- LP2 Post 4 topic changed from eUSD/TDAB to TAN / Telcoin Wallet
- LEARNING-PATH-TRACKER.md updated with note: "eUSD/TDAB content is out of scope for @telcoinTAO"
- AGENCY-MEMORY.md updated with full entity structure brief and standing rules on eUSD/TDAB
- `campaign/research/ENTITY-STRUCTURE-BRIEF.md` created with full entity mapping
- Standing decision added: "TDAB (Telcoin Digital Asset Bank): Do NOT draft or produce any TDAB-focused content."

**Rule derived**:
Before drafting any post for @telcoinTAO, run the entity check: "Is every claim in this post attributable to Telcoin Association - not Telcoin Holdings, not Telcoin Inc., not TDAB?" Holdings content (Telcoin Wallet commercial metrics, eXYZ stablecoins as products, corridor counts) requires explicit confirmation. When in doubt, flag `[CONFIRM]` rather than proceeding.

---

## Pattern Summary (update this after each new lesson)

| # | Category | Core Rule |
|---|---|---|
| 0 | Entity boundaries | @telcoinTAO = Telcoin Association only. Holdings content requires explicit confirmation. |
| 1 | Voice principles | Apply LLM Voice Principles to every piece of content. Read before writing, not after. |
| 2 | Standup context | Always read the full context stack before producing a standup. Never from memory. |
| 3 | Self-improvement loop | Log every correction immediately. Never let a lesson go uncaptured. |
| 4 | Daily run protocol | "Run standup" = full 6-phase daily-agency-run.md. Always launch Phase 0 agents first. |
| 5 | Publish status tracking | Never assume content status. Always confirm with user whether a post has gone out. |
| 6 | Council transcript workflow | Transcript received → check research file → produce structured recap → commit both. Recap must include chapters, key announcements, Q&A summary, content flags, usable quotes. |
| 7 | Block explorer references | Never reference telscan.io or any specific block explorer URL in published content. Use generic language until mainnet explorer is officially confirmed. |
| 8 | Fact verification ownership | Agents verify technical claims via web search before flagging as [CONFIRM]. [CONFIRM] is only for information that cannot be found publicly. Never push verifiable facts back to the user. |
| 9 | Council meeting reminder format | Use the canonical format: council name + date/times, agenda bullets (no presenters), listen-in links (X + YouTube), next meetings. No deviations. |

---

## How to Add a New Lesson

Copy this template and add at the top of Active Lessons:

```
### Lesson N — [Short description of the error]
**Date**: YYYY-MM-DD
**Session**: [branch name]

**What was produced**:
[What the agent/session produced before the correction]

**What the user said**:
[Exact or paraphrased user feedback]

**What was changed**:
[List of files modified, rules added, processes updated]

**Rule derived**:
[The one-sentence rule that prevents this mistake from recurring]
```

Then update the Pattern Summary table.
