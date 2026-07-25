# Dreaming Pass — Telcoin Association Agency

Out-of-band memory consolidation. Runs nightly as a scheduled Routine and on demand via `/dream`.

This is not a content production session. The sole purpose is to read session output files
(the "transcripts" of what happened in recent sessions), extract what's new and verified,
and write it back into the agency's canonical memory files.

## Role in the Memory Architecture

This pass is the **only process authorized to promote working memory to org knowledge**.

- **Reads from (ephemeral / read-write tier)**: `campaign/execution/YYYY-MM-DD/` folders, `campaign/research/intel-*.md` files
- **Writes to (permanent / read-only tier)**: `TELCOIN-RESEARCH.md`, `AGENCY-MEMORY.md`, `tasks/lessons.md`, `LEARNING-PATH-TRACKER.md`, `PERFORMANCE-LOG.md`
- **Versioning**: Every write committed with timestamp to `.last-dream` and session attribution in the git commit message — full write history inspectable
- **Concurrency protection**: Step 1 reads all 5 memory files in full before any writes begin — no blind overwrites, no concurrent write conflicts
- **Portability**: All memory lives in git — dreaming pass output is immediately available to any agent in any future session

Full permission model: `campaign/MEMORY-ARCHITECTURE.md`

---

## Memory Store ($MEM)

The 5 files that constitute the agency's live memory. These are the input AND output of the dreaming pass.

| File | Contents |
|---|---|
| `campaign/research/TELCOIN-RESEARCH.md` | Verified client intel — facts, products, governance, roadmap |
| `campaign/AGENCY-MEMORY.md` | Standing decisions, angle bank, open questions, entity rules |
| `tasks/lessons.md` | Operational lessons from session corrections |
| `campaign/execution/LEARNING-PATH-TRACKER.md` | Content tracker — published, drafted, pending |
| `campaign/analytics/PERFORMANCE-LOG.md` | Post performance data |

## Session Output Files (Source Transcripts)

For each date folder `campaign/execution/YYYY-MM-DD/`:
- `briefing.md` — morning intel synthesis
- `standup.md` — day plan and deliverables
- `twitter-*.md`, `community-qa-*.md`, `positioning-*.md` — content produced
- `brand-qc.md` — QC findings

Intel files in `campaign/research/`:
- `intel-x-YYYY-MM-DD.md` — X/Twitter community sentiment
- `intel-youtube-YYYY-MM-DD.md` — YouTube content intel
- `intel-market-YYYY-MM-DD.md` — market/competitor intel

---

## Orchestration Steps

### Step 0 — Find Sessions to Process

Run:
```bash
cat campaign/research/.last-dream 2>/dev/null || echo "NOT SET"
```

Then list execution folders:
```bash
find campaign/execution -maxdepth 1 -type d -name "????-??-??" | sort
```

If `.last-dream` exists: process only folders dated AFTER that timestamp.
If `.last-dream` does not exist: process all folders in `campaign/execution/`.
If no new folders exist since last dream:
```bash
SESSION_URL="https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/cse_/session_}"
date -u +%Y-%m-%dT%H:%M:%SZ > campaign/research/.last-dream
git add campaign/research/.last-dream
git commit -m "Dreaming pass $(date -u +%Y-%m-%d): no new sessions — marker updated

$SESSION_URL"
git push origin claude/campaign-iLgt5
```
Report: "Memory is current — no new sessions to process." and stop. **Do not skip this commit. The marker must be written on every exit path.**

Note the date range of sessions you will process.

### Step 1 — Read the Full Memory Store

Read all 5 memory files completely. These are your baseline ($MEM). Do not modify them yet — build up the changes in working notes, then apply in Step 4.

### Step 2 — Parallel Subagents (one per session folder)

For each session folder identified in Step 0, launch ONE subagent simultaneously with this prompt:

> "You are a memory extraction agent for the Telcoin Association Marketing Agency.
>
> Read all files in `campaign/execution/[YYYY-MM-DD]/` and the corresponding intel files
> for the same date:
> - `campaign/research/intel-x-[YYYY-MM-DD].md`
> - `campaign/research/intel-youtube-[YYYY-MM-DD].md`
> - `campaign/research/intel-market-[YYYY-MM-DD].md`
>
> Skip any file that doesn't exist.
>
> Extract ONLY information that is factual and specific — not general observations:
>
> **1. New client facts** — announcements, decisions, milestones, numbers from intel files.
>    Include the source file and date for each fact.
>
> **2. Content status** — for each piece of content found: topic, type (thread/tweet/qa/etc),
>    whether it was drafted or published, any QC flags from brand-qc.md.
>
> **3. Community intel** — specific questions being asked by the @telcoinTAO community,
>    sentiment signals, recurring narratives from X intel.
>
> **4. Lessons and corrections** — any operational pattern or correction documented in
>    standup.md or visible from session behavior.
>
> **5. New content angles** — specific ideas for content that were surfaced in intel but
>    not yet in the angle bank.
>
> **6. Open questions / blockers** — anything flagged as requiring user confirmation.
>
> Return structured output with these 6 sections. Be specific. Quote source files where possible.
> If a folder is empty or files don't exist, return: 'No extractable intel for [date].'"

Collect all subagent outputs before proceeding to Step 3.

### Step 3 — Orchestrator Merges and Verifies

After all subagents complete:

**Deduplicate**: If the same fact appears in multiple sessions, keep it once with the earliest date.

**Verify**: Cross-check every new fact against the existing TELCOIN-RESEARCH.md.
- If the fact is already there: skip it.
- If it contradicts existing content: flag it as `[CONFLICT — verify with user]`, do not overwrite.
- If it's genuinely new: include it.

**Organize** all extracted intel into 5 buckets:
- Client facts → TELCOIN-RESEARCH.md update
- Content status changes → LEARNING-PATH-TRACKER.md update
- Lessons → tasks/lessons.md update
- Angles + open questions → AGENCY-MEMORY.md update
- Performance data → PERFORMANCE-LOG.md update

### Step 4 — Update Memory Files ($MEM_OUT)

Apply net-new information to each memory file. Rules per file:

**`campaign/research/TELCOIN-RESEARCH.md`**
- Add new facts as dated sections under the correct product or governance area.
- Preserve all existing content. Never delete verified facts.
- Contradictions: add a `[CONFLICT — verify with user]` note inline.
- New sections go at the bottom of the relevant area; add the date.

**`tasks/lessons.md`**
- Append new lessons with: date, category, first output → correction → rule derived.
- Update the Pattern Summary table at the top of the file.
- Do not modify existing lessons.

**`campaign/AGENCY-MEMORY.md`**
- Add new angle bank items with `[ ]` prefix.
- Add new open questions to the Open Questions section.
- Update Last Session Summary to reflect the date range processed.
- Mark any angles as `[x]` if evidence in session files shows they were executed.

**`campaign/execution/LEARNING-PATH-TRACKER.md`**
- Update post status only when there is explicit evidence: a file named `twitter-[topic].md` exists → DRAFTED; a standup or QC file explicitly says "published" → PUBLISHED.
- Never infer publication from a draft alone.

**`campaign/analytics/PERFORMANCE-LOG.md`**
- Add performance data only if session files contain explicit metrics (impressions, engagement rates).
- Do not add placeholder or estimated rows.

### Step 5 — Write Dream Marker

```bash
date -u +%Y-%m-%dT%H:%M:%SZ > campaign/research/.last-dream
```

### Step 6 — Commit and Push

Build the session URL from the environment — do not use the hardcoded URL in CLAUDE.md, which belongs to the human working session, not this automated pass:

```bash
SESSION_URL="https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/cse_/session_}"
git add campaign/ tasks/
git commit -m "Dreaming pass $(date -u +%Y-%m-%d): memory consolidated from [N] sessions ([date-range])

$SESSION_URL"
git push origin claude/campaign-iLgt5
```

### Step 7 — Report

Output:
- Sessions processed (count and date range)
- Net-new entries added to each memory file
- Any conflicts flagged
- Any open questions surfaced
- Timestamp written to .last-dream

---

## Constraints

- This pass only consolidates what already happened. It does not produce new content, new research, or new intel.
- Never delete existing verified facts from TELCOIN-RESEARCH.md.
- Never change a post to PUBLISHED status without explicit evidence in session files.
- Do not infer or extrapolate — extract only what is present.
- Contradictions get flagged, not silently resolved.
- Entity boundary: @telcoinTAO = Telcoin Association only. Do not log Holdings content (Wallet corridors, eXYZ, TDAB) as TA-published material.
- If `.last-dream` does not exist and there are 10+ session folders, process the most recent 7 first, then set the marker. Prevents runaway first-run.
