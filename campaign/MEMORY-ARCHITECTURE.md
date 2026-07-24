# Agency Memory Architecture

Based on Anthropic's multi-agent production memory model.

---

## The Model

```
┌─────────────────────────────────────────────────┐
│              READ-ONLY (org knowledge)          │
│  campaign/research/TELCOIN-RESEARCH.md          │
│  strategy/BRAND-GUIDE.md                        │
│  campaign/AGENCY-MEMORY.md                      │
│  tasks/lessons.md                               │
│  campaign/execution/LEARNING-PATH-TRACKER.md    │
└──────────────────┬──────────────────────────────┘
                   ▲  dreaming pass only (/dream)
                   │  promotes verified output to org knowledge
┌──────────────────┴──────────────────────────────┐
│             READ-WRITE (working memory)         │
│  campaign/execution/YYYY-MM-DD/  ← all agents  │
│  campaign/research/intel-*.md    ← Trend Researcher │
│  campaign/analytics/PERFORMANCE-LOG.md ← Analytics Reporter │
│  tasks/todo.md                   ← session tracking │
│  campaign/execution/SESSION-CONTEXT.md          │
└─────────────────────────────────────────────────┘
```

---

## Four Properties

### 1. Permissioning
- **Read-only tier**: Shared org knowledge. No session agent writes here directly. This is what every agent reads at session start to orient itself.
- **Read-write tier**: Working memory. Session agents write all output here. Ephemeral by design — cleaned up by the dreaming pass.
- **Special writes**: Two agents have limited write access outside execution/: Trend Researcher writes dated intel files; Analytics Reporter writes PERFORMANCE-LOG.md. Both are still read by dreaming pass and promoted.

### 2. Versioning
Every write is attributed to an author (session), a time (commit timestamp), and a session URL (appended to commit message). Full history inspectable via `git log`. Any write can be rolled back. Never rewrite history.

### 3. Concurrency
Read the current state of any file before writing — the `Read → Edit` pattern enforces this. Git's conflict detection surfaces concurrent writes between sessions. Dreaming pass reads all 5 memory files in full before modifying any (Step 1) — no blind overwrites.

### 4. Portability
All memory is files in the git repo. Portable across sessions, agents, environments, and CI. A fresh session with no prior context can reconstruct the full agency state by reading the 5 memory files.

---

## File Permission Map

| File | Permission | Who writes | Notes |
|---|---|---|---|
| `campaign/research/TELCOIN-RESEARCH.md` | Read-only (session) | Dreaming pass | Verified client intel; promoted from intel files + session output |
| `strategy/BRAND-GUIDE.md` | Read-only | Explicit user decision only | Never edited from session or dreaming pass |
| `campaign/AGENCY-MEMORY.md` | Read-only (session) | Dreaming pass | Angles, standing decisions, open questions |
| `tasks/lessons.md` | Read-only (session) | Dreaming pass + immediate logging | New lessons appended immediately on correction |
| `campaign/execution/LEARNING-PATH-TRACKER.md` | Read-only (session) | Dreaming pass | Status updated only when dreaming pass finds explicit evidence |
| `campaign/analytics/PERFORMANCE-LOG.md` | Read-write | Analytics Reporter | Weekly analytics signal; also promoted by dreaming pass |
| `campaign/research/intel-*.md` | Read-write | Trend Researcher | Dated intel files; dreaming pass reads and promotes |
| `campaign/execution/YYYY-MM-DD/` | Read-write | All session agents | All working output — drafts, briefs, threads, QC notes |
| `campaign/execution/SESSION-CONTEXT.md` | Read-write | Session startup | Auto-written by session-start hook |
| `tasks/todo.md` | Read-write | Session tracking | Task list for current work; not part of dreaming pass |

---

## The Dreaming Pass

`/dream` (`scripts/dreaming-pass.md`) is the **only** process that promotes working memory to org knowledge. It:

1. Reads all session output from `campaign/execution/YYYY-MM-DD/` folders since `.last-dream`
2. Runs parallel extraction subagents (one per session folder)
3. Merges, deduplicates, and verifies against existing read-only files
4. Writes net-new verified intel to the 5 memory files
5. Commits with full attribution and updates `.last-dream` timestamp

Result: memory files are always current at session start. No manual curation required.

---

## What Agents Must Never Do

- Write directly to `TELCOIN-RESEARCH.md` or `AGENCY-MEMORY.md` during a session (use execution/ folder; dreaming pass promotes it)
- Modify `BRAND-GUIDE.md` (immutable except by explicit user decision)
- Mark LP posts PUBLISHED in `LEARNING-PATH-TRACKER.md` without explicit session evidence (dreaming pass only)
- Skip reading the memory files before producing content (stale context = scope violations)
