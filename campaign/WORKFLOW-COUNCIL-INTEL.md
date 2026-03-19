# Council-to-Agent Workflow
## How real-world intel reaches the agency

---

## The Core Problem

The agency drafts content from a research file. But the most timely, high-value content comes from live events: council sessions, governance votes, executive appearances, regulatory developments. These happen outside the repo. This document defines exactly how that external intel reaches agents so no time is lost.

---

## Trigger 1 — Council Meeting Recap

**When**: After any Telcoin Association council meeting concludes (TELx Council, P&T Council, TAN Council)

**How to route intel to the agent:**

1. **Preferred**: Paste the recap directly into the chat. Even 3-5 bullet points is enough to activate the recap draft agent. Example format:
   ```
   TELx Council #19 (Mar 18) — key points:
   - Merkl trial approved for Base V4 pool, starts April 2026
   - Fee rebate contract redeployment target: late March
   - Next session: April 1, 3PM EST
   - [anything else notable]
   ```
2. **Also works**: Paste the forum.telcoin.org summary URL if a post-session write-up is published
3. **Also works**: Share the YouTube recording timestamp/URL — agent will extract key points

**What happens next:**
- Agent reads the recap and flags what's publishable vs. what requires confirmation
- Recap tweet draft is produced within the session
- Research file (`TELCOIN-RESEARCH.md`) is updated with any new confirmed intel
- LP Tracker is checked to see if the intel unlocks any learning path posts

**Default hold policy**: Nothing posts without user confirmation on final copy. The workflow produces a draft + recommendation, not an auto-publish.

---

## Trigger 2 — Executive Appearance / External Event

**When**: Jeff Quigley (or another executive) appears at a conference, is quoted in press, or posts publicly about Telcoin Association

**How to route:**
1. Share the quote, article URL, or X link in the chat
2. Or share a screenshot of the post/article

**What happens next:**
- Agent assesses: is this Tier 3 milestone (post immediately), or context (update research, inform future content)?
- If immediate: rapid-response draft produced for user review
- If context: research file updated, note added to angle bank

**Jeff Quigley monitoring** (DC Blockchain Summit model):
When Quigley is known to be at an event, the agency should be explicitly told:
- "Jeff is at [event] [dates] — monitoring for signal"
- Agent then treats any Quigley X posts or press coverage as a live trigger during that window

---

## Trigger 3 — Governance Vote / Snapshot Result

**When**: A snapshot vote passes or fails, or a new governance proposal goes live

**How to route:**
1. Share the snapshot.org URL or forum post link
2. Or simply describe: "TANIP vote passed — [result summary]"

**What happens next:**
- If passed: Milestone post drafted (Tier 2)
- If failed or contentious: Flag to user — governance outcomes that divide the community should not be posted without human judgment call
- Research file updated

---

## Trigger 4 — New Regulatory Development

**When**: CLARITY Act moves, GENIUS Act amended, SEC guidance shifts, foreign regulatory news that affects Telcoin Association's positioning

**How to route:**
1. Share the news URL or article text
2. Or describe: "CLARITY Act passed Senate — [summary]"

**What happens next:**
- Agent cross-references with existing briefs (DC Summit rapid-response template, GENIUS Act notes in research file)
- Rapid-response draft produced if Telcoin Association has a verifiable, direct connection to the development
- No post goes out speculating on outcomes — only confirmed developments

---

## Trigger 5 — New Intel from Ryan Neuner / Commercial Team

**When**: Commercial team shares guidance on what TA can speak to publicly, entity boundary clarifications, or approved messaging on sensitive topics

**How to route:**
1. Share the guidance directly in chat ("Ryan says: TA can refer to Telcoin Network infrastructure; Holdings products are off-limits")
2. Agent immediately updates:
   - `AGENCY-MEMORY.md` (standing decisions)
   - `campaign/research/TELCOIN-RESEARCH.md` (research file)
   - Any active drafts that touch the affected topic

---

## Flow Summary (visual)

```
Real-world event
      ↓
User routes to agent
(paste recap / share URL / describe event)
      ↓
Agent reads + assesses:
  - What is confirmed fact?
  - What is publishable?
  - What needs commercial/user review?
      ↓
Draft produced (never auto-published)
      ↓
User reviews + approves
      ↓
Post goes live
      ↓
LP Tracker updated
TELCOIN-RESEARCH.md updated
AGENCY-MEMORY.md updated if standing rules change
```

---

## What the Agent Will NOT Do Without Routing

- Draft a council recap from memory or assumptions
- Publish rapid-response content based on rumor or unverified X posts
- Update the research file with intel not explicitly confirmed by the user
- Make assumptions about what was discussed at a meeting that was not recapped

If information is not routed, the agent will flag the gap in the standup and note what is needed to activate the blocked content.

---

## Council Schedule Reference (as of March 2026)

| Council | Cadence | Next date |
|---|---|---|
| TELx Council | ~Every 2 weeks | April 1, 2026 — 3:00 PM EST |
| Platform & Treasury Council | ~Every 2 weeks | March 26, 2026 — 4:00 PM EST |
| TAN Council | ~Every 2 weeks | April 2, 2026 — 5:00 PM EST |
| Miner Assembly | As needed | TBD |

After each session, route the recap using Trigger 1 above.
