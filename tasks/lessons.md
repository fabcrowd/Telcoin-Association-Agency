# Agency Self-Improvement Log
## Telcoin Association Marketing Agency

**Purpose**: Every time the user corrects an output or changes instructions, that correction is logged here as a structured lesson. The pattern is: what was produced → what the user said → what changed → the rule derived. This file is read at every session start and before every content task.

**Update rule**: After ANY user correction, add a new entry at the top of the Active Lessons section immediately. Do not batch corrections. One entry per correction.

**Read rule**: CLAUDE.md Session Startup Checklist step references this file. Read it before producing any content.

---

## Active Lessons (newest first)

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
