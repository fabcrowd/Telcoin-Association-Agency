# YouTube Channel Intelligence — @TelcoinTAO
## Compiled: March 20, 2026
## Coverage window: March 13–20, 2026 (7 days)
## Sources: TELCOIN-RESEARCH.md (primary), web search, public X/Twitter posts

---

## ACCESS NOTE

Direct scraping of youtube.com/@TelcoinTAO is blocked (HTTP 403). The channel listing and individual video pages are not publicly crawlable by automated agents. All intelligence below is compiled from:

1. **TELCOIN-RESEARCH.md** — internally documented from live stream watch on March 18, 2026
2. **Web search results** referencing @TelcoinTAO X posts and forum activity
3. **Public X/Twitter announcements** from @TelcoinTAO confirmed via search index

Manual channel check recommended at https://www.youtube.com/@TelcoinTAO/videos to confirm view counts, durations, and comment sections.

---

## VIDEO LIST — Last 7 Days (March 13–20, 2026)

### VIDEO 1 — TELx Council Meeting #19

| Field | Detail |
|---|---|
| **Title** | TELx Council Meeting #19 (working title — exact YouTube title unconfirmed) |
| **URL** | https://www.youtube.com/watch?v=QsDDDLFPr8c |
| **Publish date** | March 18, 2026 |
| **Format** | Live council stream — recurring governance meeting |
| **Duration** | Unconfirmed (council meetings typically 45–90 min) |
| **View count** | Not accessible via scrape — check channel manually |
| **Simulcast** | X Spaces + YouTube (standard format for all council meetings) |

**Topics covered (from documented research, March 18, 2026):**

1. **Merkl integration scoping** — reviewing the Baptiste (Merkl) meeting scheduled for March 19. Leo (technical lead) required to attend; success criteria document being drafted. NDA + services agreement process confirmed by Tim Mahota (General Counsel).

2. **V4 aggregator routing problem identified** — Major finding: OX Protocol and most aggregators route <10% of volume through Uniswap V4 custom-hook pools. Root cause: hooks make swap rate prediction unpredictable; advanced aggregators like Kyberswap can handle it, most cannot. ~90% of Telcoin Wallet-routed volume bypasses the V4 pool as a result.

3. **Hook purpose clarification** — The V4 hook's primary purpose is JIT (just-in-time) liquidity attack prevention via 24-hour position lock, NOT governance/voting. Voting was a secondary integration goal.

4. **Merkl's strategic implication** — If Merkl handles eligibility/subscription externally, the NFT-based hook system may become unnecessary. This could enable migration back to V3 pools for better aggregator routing without losing reward-targeting capability.

5. **Holdings strategic meeting scheduled** — March 23, 2026, 2pm Eastern. Attendees: Paul (CEO), Parker (Executive Director), full TELx Council. Agenda: Post-bank-launch V5 roadmap, eXYZ stablecoin liquidity strategy, TELx Council mission definition for H2 2026.

6. **Operational updates** — V4 staked amount showing N/A (subgraph UI bug, Ty following up with Khalil; added to Trello). Admin rewards dashboard (Derek) in development — position-level breakdown tool for LPs. TX University handover to Leo and Storm underway.

7. **Pool strategy update** — Balancer V3 Reclaim Pools still under evaluation for stable pairs. Monitoring Base potentially leaving OP Stack (Uniswap applications not expected to be impacted). Council member Cody has Base/The Block contacts for intel.

8. **Operational systems confirmed stable** — Reward script issues from prior weeks fully resolved with redundancy in place. Period 29 distribution completed promptly after epoch close.

---

### OTHER CONTENT — Last 7 Days (Unconfirmed as YouTube Uploads)

**DC Blockchain Summit 2026 (March 17–18, Washington DC)**

Telcoin Association was a Bronze Sponsor. Jeff Quigley (EVP, Business Development & Communications) was the floor representative and keynote/panel participant. The summit was livestreamed on the Digital Chamber's YouTube channel (@DigitalChamber), not on @TelcoinTAO directly. It is unknown at this time whether Telcoin Association clipped or reposted Quigley's appearance to their own YouTube channel.

- Check for clips: https://www.youtube.com/@DigitalChamber
- Search: "Telcoin" or "Jeff Quigley" in DC Blockchain Summit 2026 recordings
- This is a high-priority repurposing target if a clip is available

---

## UPCOMING LIVESTREAMS — Confirmed

| Meeting | Date | Time | Format |
|---|---|---|---|
| Platform & Treasury Council (P&T) | March 26, 2026 | 4PM EST | YouTube + X Spaces (standard) |
| TELx Council #20 | April 1, 2026 | 3PM EST | YouTube + X Spaces (standard) |
| TAN Council | April 2, 2026 | 5PM EST | YouTube + X Spaces (standard) |

Note: TELx Council #20 is expected ~2 weeks from March 18 per council-confirmed schedule. The Holdings strategy meeting (March 23) is an internal session — not expected to be streamed publicly.

---

## KEY INSIGHTS — From TELx Council #19

### 1. The V4 aggregator routing problem is significant and underreported externally

The finding that <10% of aggregator volume routes through V4 custom-hook pools — and that ~90% of Telcoin Wallet-routed swaps bypass the TELx V4 pool — has not been communicated publicly. This is a material technical constraint currently being addressed via the Merkl evaluation and potential V3 migration path. It is **not** appropriate for public post material in its current form (the council is in active problem-solving mode). However, once Merkl is live and the solution is in place, this becomes a strong "problem → solution" narrative.

### 2. Merkl is a governance-defining decision

This is the TELx Council's first external vendor engagement. It redefines how rewards are calculated, opens up dynamic per-pool incentive allocation, and could enable the council to rapidly onboard new pools (especially eXYZ stablecoins). The April 2026 go-live is a milestone worth tracking for content.

### 3. The Holdings strategy meeting (March 23) defines H2 2026 direction

The outcome of the Paul + Parker + TELx Council session will shape the eXYZ stablecoin liquidity roadmap and clarify the council's mandate for the second half of the year. Watch for outputs from this meeting that unlock content.

### 4. TX University is close to launch

The educational content platform (TX University) is in final handover to Leo and Storm — "final licensing + content polish before launch." This is a community content event that warrants a launch announcement post when confirmed.

### 5. Admin rewards dashboard (Derek) is a builder story

A position-level LP breakdown tool that allows council members (and eventually users) to understand why they earned more or less on any given week. When integrated into the unified web project, this becomes a transparency and tooling story worth publishing.

---

## REPURPOSING OPPORTUNITIES

### From TELx Council #19

**Opportunity 1 — "Why Telcoin chose Uniswap V4" explainer thread**
The council discussed V4 vs V3 tradeoffs in detail. When the Merkl + routing situation resolves, this becomes a strong technical explainer: what V4 enables (JIT attack prevention, concentrated liquidity), what the tradeoffs are (aggregator routing friction), and how TELx is addressing it. Thread: 4–5 posts.

**Opportunity 2 — Merkl go-live announcement (target: April 2026)**
When Merkl goes live on the Base V4 TEL/ETH pool, post a single-tweet milestone: first external vendor integration, first dynamic incentive system, test framework running in parallel. Image card: Merkl x TELx. No hype framing — factual milestone.

**Opportunity 3 — TX University launch announcement**
When the final launch date is confirmed, a launch tweet + short thread explaining what TX University is and why it matters. Format: explainer, institutional tone.

**Opportunity 4 — "The Council that builds" — TELx Council profile**
Opportunity for a forum post or long-form content profiling the TELx Council's governance role. Uses real decision examples from the March 18 session: the Merkl vote, the V4 pool analysis, the NDA process. Demonstrates that governance is substantive, not ceremonial.

**Opportunity 5 — V4 staking bug transparency note (when fixed)**
Short update tweet when the N/A staked amount UI bug is resolved. Tone: direct, factual. Builds trust through transparency.

**Opportunity 6 — DC Blockchain Summit clip (if available)**
If Jeff Quigley's appearance at DC Blockchain Summit was captured on the Digital Chamber's YouTube channel, clip the Telcoin-relevant segment and post to @telcoinTAO. Potential tweet: "Telcoin at DC Blockchain Summit, March 2026 — [clip or quote]." Check: https://www.youtube.com/@DigitalChamber

---

## UNANSWERED VIEWER QUESTIONS

Unable to access YouTube comments via scrape. The following questions are inferred from known community activity on X and the forum as of March 2026 — these are recurring community questions this channel should address in future content or stream Q&A:

1. **"When mainnet?"** — The most persistent community question. The channel should reinforce milestone-based framing consistently: not a date, but a checklist. Reference roadmap.telcoin.network.

2. **"Why is my staked TEL showing N/A on telx.network?"** — The V4 UI bug noted in Council #19. Will generate user questions until resolved. A brief update post or in-stream acknowledgment appropriate.

3. **"What happened to the reward script issues?"** — Council confirmed fully resolved with redundancy in place. Has not been communicated publicly. A brief operational update tweet is warranted.

4. **"What is TX University?"** — Community awareness of this product is low. When it launches, it needs an educational announcement.

5. **"Will TELx stay on V4 or move back to V3?"** — The aggregator routing discussion from Council #19 is the context. No public statement has been made. Not ready to address publicly while council is evaluating Merkl's implications.

6. **"What pools are getting incentives and how much?"** — TELx pool allocation is council-governed and changes. The admin rewards dashboard (Derek's tool) will eventually make this self-service. Until then, periodic pool update posts reduce inbound questions.

---

## CHANNEL OBSERVATIONS (Structural)

Based on available intelligence:

- **Content frequency**: Council streams dominate the channel. No evidence of standalone short-form or educational content published in the last 7 days beyond the March 18 council stream.
- **Publishing pattern**: Content uploads align almost entirely with live council meetings (bi-weekly cadence per council). There is no observed standalone explainer, short-form, or highlight clip cadence.
- **Gap**: No YouTube Shorts, highlight clips, or evergreen educational content has been observed on this channel. This is a significant gap — council streams are 45–90 minutes; no extracted clips create a barrier to casual audience discovery.
- **Comment engagement**: Not accessible via scrape — manual review recommended for each council stream within 48 hours of upload to identify viewer questions.

---

## ACTION ITEMS FOR MARKETING TEAM

| Priority | Action | Owner | Timeline |
|---|---|---|---|
| High | Manually review TELx Council #19 (https://youtu.be/QsDDDLFPr8c) — confirm exact title, duration, view count, and comments | Marketing | This week |
| High | Check Digital Chamber YouTube for Jeff Quigley / Telcoin segment from DC Blockchain Summit March 17–18 | Marketing | Immediate |
| Medium | Draft Merkl go-live announcement tweet + image brief (publish when live, ~April 2026) | Content Creator agent | Now — hold for trigger |
| Medium | Draft TX University launch announcement (hold for launch date confirmation) | Content Creator agent | Now — hold for trigger |
| Medium | Establish post-stream comment review workflow within 48 hours of each council stream | Marketing ops | Standing process |
| Low | Evaluate YouTube Shorts strategy — extract 60–90 second highlights from council streams | Content Creator + Visual Storyteller agents | Q2 2026 |
| Low | Confirm exact duration and view counts for Council #19 by visiting channel directly | Marketing | This week |

---

## SOURCES

- TELx Council #19 stream (March 18, 2026): https://www.youtube.com/watch?v=QsDDDLFPr8c
- TELCOIN-RESEARCH.md (primary source, last updated March 19, 2026)
- @TelcoinTAO X announcement (TELx Council #18 reference): https://x.com/TelcoinTAO/status/1948054405325983879
- DC Blockchain Summit 2026: https://www.dcblockchainsummit.com/
- TELxIP Merkl POC forum thread: https://forum.telcoin.org/t/telxip-merkl-proof-of-concept-evaluation-for-telx-base-tel-eth-v4-pool/838
- Telcoin Association YouTube channel: https://www.youtube.com/@TelcoinTAO
