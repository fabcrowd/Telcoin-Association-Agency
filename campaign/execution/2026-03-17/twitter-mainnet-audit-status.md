# Twitter Thread: Where Mainnet Stands — A Factual Update
**Account**: @telcoinTAO
**Date**: March 17, 2026
**Format**: 5-tweet thread
**Purpose**: Address community's #1 question ("when is mainnet?") with a verified status update — what is done, what is in progress, what comes next
**Sources used**: `campaign/research/TELCOIN-RESEARCH.md` (roadmap.telcoin.network data, Platform & Treasury Council #26 recap, March 12, 2026)

---

## Thread

---

### Tweet 1 — Hook / Header (with image)

The most common question in this community is "when is mainnet?"

It does not have a date. It has a sequence. Here is where that sequence stands today.

A status update, facts only. 🧵

---

**IMAGE BRIEF — Tweet 1 Header Card**

**Format**: Static image, 1200 x 675px
**Template type**: Thread header card
**Figma layer label**: `thread-header / mainnet-status-2026-03-17`

**Background**: TEL Dark Gradient — `#192E58` to `#090920`, top-left to bottom-right diagonal
**Overlay texture**: Faint hexagonal grid pattern at 8% opacity, in `#3642B2`

**Logo**: Telcoin Association horizontal logo, top-left corner, white version — 1 mark height from top, 1.5 mark widths from left edge

**Headline text** (centered, vertically balanced in lower two-thirds of card):
- Line 1: "Mainnet Status" — New Hero Bold, 52px, `#F1F4FF`
- Line 2: "A Factual Update" — New Hero Regular, 32px, `#14C8FF`

**Subtext** (below headline, 8px gap):
- "March 17, 2026" — New Hero Regular, 18px, `#7393EA`

**Accent element**: Single horizontal rule, 2px, `#3642B2`, spanning 60% of card width, centered, positioned between logo and headline block

**No decorative imagery. No iconography. No AI-generated elements.**

---

### Tweet 2 — Adiri Testnet: What Was Accomplished

The Adiri public testnet gave MNO validators and partners a live environment to exercise the network before mainnet.

Phase 1 is fully complete:
- Initial validator nodes spun up
- Block explorer live at scan.telcoin.network
- Feature complete state reached
- Initial 4-week security assessment finished

Phase 2 hardening is in progress - database infrastructure, p2p networking, sync strategy, stress testing, and tooling for validators to stake and activate.

---

### Tweet 3 — BLS Library and Audit Sequencing

The internal security work is further along than the community may realize.

All internal BLS cryptographic library findings have been resolved.

What comes next is external: security assessments are now being scheduled with top EVM security researchers, a number of whom were identified and approached at ETH Denver.

The sequence is: BLS library assessment first, then comprehensive protocol audits across five domains - cryptography, P2P network, smart contracts, execution layer, and state synchronization.

The timeline is set by researcher fit, not calendar convenience.

---

### Tweet 4 — Why Mainnet Is Not on Cloud Infrastructure

One thing the community consistently underestimates: testnet and mainnet are not just different environments - they are fundamentally different infrastructure.

Testnet runs on distributed cloud data centers (US east and west coasts) plus volunteer nodes globally. That configuration tests wide-area network latency at geographic scale.

Mainnet validators run in private MNO-owned bare-metal data centers sitting alongside existing telecom packet-switching infrastructure. Fiber-optic interconnects capable of streaming tens of gigabits per second. Those performance characteristics do not exist in standard cloud.

Getting into those data centers requires extensive permissions. The protocol must meet their security bar first. The sequencing is not arbitrary - it reflects the requirements of the infrastructure that makes Telcoin Network's validator model credible.

---

### Tweet 5 — What Comes Next + Conversation Invitation (with image)

To summarize the current state:

- Adiri testnet: Phase 1 complete, Phase 2 hardening in progress
- BLS cryptographic library: all internal findings resolved
- External security audits: being scheduled
- Mainnet milestones (all queued): five security assessments → patch findings → launch

No calendar date exists. The launch sequence is milestone-based.

Progress and sequencing are documented at roadmap.telcoin.network

Given the infrastructure and audit sequencing described above, which aspect of the mainnet readiness process is least understood in your view?

---

**IMAGE BRIEF — Tweet 5 Insert Card (Status Tracker)**

**Format**: Static image, 1200 x 675px
**Template type**: Thread insert / status card
**Figma layer label**: `thread-insert / mainnet-sequence-tracker`

**Background**: `#090920` flat fill
**Border**: 1px inset border, `#3642B2`, full card perimeter with 8px corner radius

**Logo**: Telcoin Association mark only (hexagon icon, no wordmark), top-right corner, `#3642B2`, 28px

**Card title** (top-left, below logo baseline):
- "Mainnet Readiness — Current State" — New Hero Bold, 20px, `#F1F4FF`
- "As of March 17, 2026" — New Hero Regular, 14px, `#7393EA`

**Status list** (left-aligned, stacked vertically with 12px row spacing, starting 40px below title block):

Each row follows this structure:
`[STATUS INDICATOR] [ITEM LABEL]`

Row 1: `[COMPLETE]` — Adiri Testnet Phase 1
Row 2: `[IN PROGRESS]` — Adiri Testnet Phase 2 Hardening
Row 3: `[COMPLETE]` — BLS Cryptographic Library (internal findings resolved)
Row 4: `[IN PROGRESS]` — External Audit Scheduling
Row 5: `[QUEUED]` — Cryptography Security Assessment
Row 6: `[QUEUED]` — P2P Network Security Assessment
Row 7: `[QUEUED]` — Smart Contract Security Assessments
Row 8: `[QUEUED]` — Execution Layer Security Assessment
Row 9: `[QUEUED]` — State Synchronization Security Assessment
Row 10: `[QUEUED]` — Patch Security Findings
Row 11: `[QUEUED]` — Mainnet Launch

**Status indicator color coding:**
- `[COMPLETE]` — filled circle, `#14C8FF`, label text `#14C8FF`
- `[IN PROGRESS]` — half-filled circle, `#7393EA`, label text `#F1F4FF`
- `[QUEUED]` — outlined circle, `#424761`, label text `#424761`

**Typography for list items:**
- Status label: New Hero Bold, 13px
- Item label: New Hero Regular, 15px

**Footer** (bottom-right, 16px from edge):
- "roadmap.telcoin.network" — New Hero Regular, 13px, `#3642B2`

**No iconography beyond status circles. No decorative imagery.**

---

## Pre-Publish Checklist

- [ ] Every claim verified against `campaign/research/TELCOIN-RESEARCH.md`
- [ ] No invented timeline or date claims
- [ ] No hype language ("soon", "exciting", "massive")
- [ ] No em dashes in body text
- [ ] No hashtags in body text
- [ ] Conversation invitation uses Neutral Authority framing (Tweet 5 - institutional question, not promotional)
- [ ] roadmap.telcoin.network referenced for timing
- [ ] Image brief included for Tweet 1 (header) and Tweet 5 (insert)
- [ ] No contractions in formal tweet text
- [ ] MNO validator names not published (per research file standing instruction)
- [ ] Brand voice test: reads as appropriate in a regulatory newsletter

## Fact Sources (per tweet)

| Tweet | Claim | Source |
|---|---|---|
| 1 | Thread framing | Context only, no factual claim |
| 2 | Adiri Phase 1 complete, items listed | roadmap.telcoin.network (Mar 10, 2026 screenshots) |
| 2 | Phase 2 hardening in progress | roadmap.telcoin.network (Feb 19, 2026 developer notes) |
| 2 | scan.telcoin.network | TELCOIN-RESEARCH.md |
| 3 | BLS cryptographic library findings resolved | Platform & Treasury Council #26, Mar 12, 2026 |
| 3 | External audits being scheduled, ETH Denver contacts | Platform & Treasury Council #26, Mar 12, 2026 |
| 3 | BLS first, then five-domain audit sequence | roadmap.telcoin.network + Council #26 |
| 4 | Testnet: cloud data centers, US east + west, volunteer nodes | Council #26 recap, TELCOIN-RESEARCH.md |
| 4 | Mainnet: MNO bare-metal, packet-switching, fiber, gigabit speeds | Council #26 recap, TELCOIN-RESEARCH.md |
| 4 | MNO data center access requires permissions + protocol maturity | Council #26 recap |
| 5 | All mainnet milestones queued | roadmap.telcoin.network |
| 5 | Milestone-based, not date-based | roadmap.telcoin.network standing language |
