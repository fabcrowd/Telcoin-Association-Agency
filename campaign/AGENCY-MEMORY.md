# Agency Memory & Learning Log
## Telcoin Association Marketing Agency

This file is updated automatically after every agency session. It tracks what content performed well, what angles resonated, what to do more of, and standing decisions. The `Agents Orchestrator` reads this at the start of every session before planning the day's work.

---

## Entity Scope — @telcoinTAO Content Boundaries

**This is the most important standing rule.** Every post must pass the entity check before drafting.

### Confirmed entity structure (researched 2026-03-19)
Full brief: `campaign/research/ENTITY-STRUCTURE-BRIEF.md`

**Telcoin Association** = Swiss Verein (protocol governance) — this is @telcoinTAO's voice
**Telcoin Holdings Pte. Ltd.** = Singapore commercial company (incorporated Feb 2022) — owns the products
**TAO (Telcoin Autonomous Ops, Ltd.)** = UK company, wholly owned by TA, is TA's operational arm

### @telcoinTAO speaks for: **Telcoin Association**
- Telcoin Network (L1 blockchain protocol — governed by Platform Council)
- TELx (DeFi liquidity layer — governed by TELx Council)
- TAN (application network — governed by TAN Council)
- TEL token treasury and issuance (governed by the Association)
- All governance: councils, TELIPs, TGIPs, TIPs, snapshot votes
- GSMA MNO validator model and compliance rules
- Adiri testnet / mainnet roadmap milestones

### @telcoinTAO does NOT speak for: **Telcoin Holdings**
- Telcoin Wallet (telco.in) — Holdings product; reference as ecosystem context only
- Telcoin Digital Asset Bank / TDAB — Holdings subsidiary (Telcoin Inc., Nebraska)
- eUSD, eGBP, eJPY, eSGD, eZAR and all eXYZ stablecoins — issued by TDAB
- eXYZ corridor strategy — explicitly described in TELx Council minutes as "Telcoin Holdings corridors"
- Remittance corridor counts (20+ countries, 40+ e-wallets) — Holdings commercial metrics
- Exchange listings and commercial partnerships

### Requires [CONFIRM] from Ryan Neuner before posting:
- Any figure from the MNO pitch deck (`/assets/Telcoin Network Introduction – MNO...pdf`) — that is a Holdings commercial document
- "Digital Cash" as a branded term — likely Holdings branding; not confirmed as TA terminology
- "16 countries", "23+ mobile money platforms", "3 billion people" — Holdings commercial metrics
- Any eUSD reference beyond passing ecosystem context

### About Ryan Neuner
Ryan Neuner = Marketing Associate at **Telcoin Holdings** (not TA staff). He works for the Association under a Shared Services Agreement. He is the right person to clear Holdings-adjacent content before publish.

### Entity QA rule (apply to every post before marking ready-to-publish):
"Is every claim in this post attributable to Telcoin Association — not Telcoin Holdings, not Telcoin Inc., not TDAB?"
If any claim belongs to Holdings: remove it, add entity attribution, or flag `[CONFIRM]` and route to Ryan.

---

## Personal vs. Official Content — Standing Rule (added 2026-07-25)

When the user asks for a tweet (or any social post), **always ask first**: personal account or @telcoinTAO?

- **Personal account**: Brand Guardian disengaged. No entity scope restrictions, no tone policy, no Neutral Authority prompt requirement. User's voice, user's opinions. Price commentary, token fundamentals, personal takes — all permitted.
- **@telcoinTAO (official)**: Full brand policy applies. Entity scope, tone rules, image mandate, Neutral Authority CTAs, all standing editorial directives.

Never assume. Ask every time unless context makes it unambiguous (e.g. user says "tweet for the account" or pastes a draft with @telcoinTAO attribution).

---

## Standing Decisions (never override without user instruction)

- **Pre-meeting council notice format (all councils)**: Bulleted agenda format. List ALL agenda items exactly as provided — do not collapse, summarize, or omit any item. No speaker names. Footer link = youtube.com/@TelcoinTAO. Observation CTA = "Observe via @TelcoinTAO on X or Google Meet." (use Discord if that is the only stream). Character limit is not a constraint. Reference pattern: P&T Council #34 notice, 2026-03-25.
- All mainnet timing language references roadmap.telcoin.network only — never invent dates
- Bridge partner = LayerZero (Axelar no longer active)
- Wallet version = V5 (not V4)
- Primary X/Twitter account = @telcoinTAO
- Tone = professional, factual, crypto-native — no hype, no rockets, no moons
- **Content scope**: @telcoinTAO posts cover Telcoin Network (L1 infrastructure), TELx, governance, and Telcoin Association initiatives. Banking/stablecoin/TDAB content is out of scope for this account.
- **TDAB (Telcoin Digital Asset Bank)**: Do NOT draft or produce any TDAB-focused content. Fine to mention in research/internal files. No public posts on TDAB, ever, without explicit user instruction.
- **eXYZ stablecoins** (eUSD, eGBP, eJPY, eSGD, eZAR, eEUR): Incidental mentions in infrastructure context are OK. Posts *about* eXYZ stablecoins require user confirmation before publishing.
- **"Digital dollars"**: Do NOT use this phrase in any public post without explicit user instruction.
- **eUSD** as a stablecoin product post: requires user confirmation. eUSD as a passing reference in a Telcoin Network/TELx post is acceptable.
- **Stablecoin liquidity roadmap** (e.g. TELx Council agenda items referencing eXYZ liquidity): OK to mention as council/governance context — no confirmation needed.
- **Block explorer URL**: Do NOT reference telscan.io or any specific block explorer URL in published content. Use generic language ("the network's block explorer", "on-chain", "block times on the network") until a canonical explorer URL is officially confirmed for mainnet.
- **Fact verification ownership**: Agents must attempt web search verification of any technical claim before flagging it as [CONFIRM] for the user. [CONFIRM] is reserved for information that cannot be found publicly (internal decisions, unannounced partnerships, unreleased roadmap items). Published benchmarks, public audit results, public partnership announcements — all require agent-side web search verification, not user follow-up.

---

## Standing Intelligence Sources (weekly sweep, organized by day)

**Changed 2026-08-01.** These used to be documented as "monitored daily, Phase 0" — but nothing
actually triggered that daily run (the session-start hook never invoked it, and it depended on a
human typing "run standup"). The 2026-08-01 dreaming pass confirmed zero intel files existed
across the 7 most recent active sessions. Replaced with `scripts/weekly-intel-sweep.md`, which:

- Runs on its own **weekly** scheduled trigger (or manually via `/weekly-intel`)
- Writes **one file per week**: `campaign/research/intel-week-[MONDAY].md`
- Organizes that file **by day** — but only where genuine per-day data exists (from the daily
  `sentiment-scraper.md` and `youtube-pull.py` JSON pipelines). A single snapshot never gets
  faked into day-by-day sections it isn't part of; see Lesson 11 in `tasks/lessons.md`.

### X/Twitter — $TEL Social Listening
- **Search terms**: `$TEL`, `Telcoin`, `@telcoinTAO`, `Telcoin Network`, `eUSD Telcoin`
- **Purpose**: Community sentiment, unanswered questions, narratives forming, content gaps
- **Source of truth**: `campaign/analytics/sentiment/YYYY-MM-DD.json` (daily, from
  `scripts/sentiment-scraper.md`) — the weekly sweep synthesizes this rather than re-searching.
  Falls back to a fresh WebSearch, clearly labeled as a snapshot, only if no JSON exists for the
  week yet.
- **Output**: `campaign/research/intel-week-YYYY-MM-DD.md` (day-sectioned)
- **Rule**: Community questions surfaced here get turned into content the same day when possible

### YouTube — @TelcoinTAO Streams & Videos
- **Channel**: https://www.youtube.com/@TelcoinTAO (`UCs5IFXnrKliqRA6U4o_VD2Q`)
- **Purpose**: Repurpose streams into threads, forum posts, and social clips. Monitor for
  new uploads, council recordings, AMAs, and announcements.
- **Source of truth**: `campaign/analytics/youtube/YYYY-MM-DD.json` (daily, from
  `scripts/youtube-pull.py` / the n8n workflow) — real view/like/comment counts, never scraped.
- **Output**: `campaign/research/intel-week-YYYY-MM-DD.md` (day-sectioned)
- **Rule**: Every new stream or video must be repurposed into at least 2 content pieces
  (thread + forum post minimum). Council recordings always get a recap thread.
- **Repurposing formats**:
  - Long stream → 5-tweet thread (key insight) + forum.telcoin.org recap post
  - AMA / Q&A → community Q&A content (answer the top 3 questions publicly)
  - Short announcement video → single tweet + image brief for visual team
  - Council recording → governance recap thread for @telcoinTAO

### Market & Ecosystem
- **Topics**: TEL token news, stablecoin regulation, remittance market, GSMA blockchain, competing L1s
- **Cadence**: once per week file, not once per day — this subject matter doesn't need daily
  granularity, and running the full sweep daily was pure overhead
- **Output**: `campaign/research/intel-week-YYYY-MM-DD.md`, single section near the top
- **Rule**: Competitor moves get positioning content (no direct attacks, anchor to Telcoin strengths)

### Trigger setup (manual step — no API access to create/edit scheduled triggers from a session)
At code.claude.com → Settings → Triggers → New trigger: repository
`fabcrowd/telcoin-association-agency`, branch `claude/campaign-iLgt5`, schedule e.g. `23 8 * * 1`
(Monday mornings), prompt: `Follow the instructions in scripts/weekly-intel-sweep.md`.

---

## YouTube Content Log

*(Track what's been repurposed so we don't duplicate. Updated each session.)*

| Video/Stream Title | Upload Date | Repurposed? | Output Files |
|---|---|---|---|
| Platform & Treasury Council #26 | ~Mar 12, 2026 | Not yet repurposed | Opportunity: mainnet infrastructure sequencing thread, BLS resolution tweet |
| TELx Council #19 | Mar 18, 2026 | Not yet repurposed | Opportunity: Merkl trial explainer, TELx governance recap |
| Platform & Treasury Council #34 | Mar 26, 2026 | Partial — transcript processed | Research updated; council recap thread to be drafted (2026-03-27/twitter-pt34-recap.md) |

---

## Content Performance Log

*(Updated after each session. Format: date | content type | topic | what worked / what to repeat)*

| Date | Type | Topic | Notes |
|---|---|---|---|
| 2026-03-17 | Twitter threads | eUSD/CBDC, mainnet status, GSMA whitepaper, TELx preview, eUSD vs USDC | Drafted; pending QC and publish |

---

## Angle Bank (ideas to revisit)

Ideas generated but not yet executed. Pull from here when planning daily output.

**New items from April 1, 2026 intel sweep:**
- [ ] Regulatory clarity positioning — eUSD as first-mover in GENIUS/CLARITY Acts framework. TL: "Regulated digital cash is now the standard. Telcoin predicted it."
- [ ] GSMA execution layer — Position Telcoin as settlement rail for GSMA stablecoin vision. Window: 12-18 months before competitors build against spec.
- [ ] Case study: Telcoin Network for existing remittance corridors (US-Mexico, Asia-Pacific). Partner story: How blockchain acceleration benefits Wise/Western Union integration paths.
- [ ] Comparative positioning: Regulated digital banking (eUSD + TDAB + MNO L1) vs. Celo's L2 + unregulated stablecoin. Angle: "Financial inclusion requires regulatory alignment."
- [ ] Validator recruitment education — Identified gap in Phase 0A (no community discussion). Thread: ConsensusNFT, CVV/NVV/OV roles, entry/exit process. Demystify "permissioned" vs. "open."
- [ ] Mainnet timing narrative — SWIFT launches mid-2026, Telcoin mainnet in hardening phase (Q1 target). Angle: "Narrow window for Telcoin differentiation." Competitive urgency without hype.
- [ ] Partnership case studies — Powerhive (energy finance), Game Company (gaming micropayments). Proof of use case expansion beyond remittance.
- [ ] Thread: "Why telecoms are the right validators for a financial blockchain" — MNO infrastructure story
- [x] ~~Thread: "What eUSD actually means"~~ — out of scope; TDAB/stablecoin product not @telcoinTAO territory
- [ ] Thread: "Building on Telcoin Network now" — developer onboarding, EVM-compatible, start on Base
- [ ] Video concept: "The problem with sending money abroad" — remittance pain point, then Telcoin solution
- [ ] Infographic: Remittance fee comparison — Telcoin 2% vs Western Union 3–8% vs bank wire $25–$45
- [ ] Thread: "What happened at MWC Barcelona" — private MNO meetings, what it means for mainnet
- [x] 2026-03-17 Post: Merkl trial approval — governance milestone, what it means for liquidity miners
- [ ] Builder spotlight: Cody's random square game — fun, accessible, TAN ecosystem growth
- [ ] Thread: "The Telcoin Name Service" — .tel addresses, what it means for UX
- [ ] Charity NFT concept post — Leo's vision, on-chain transparency in giving
- [ ] Thread: "Phase 1 complete — here's what the Adiri testnet accomplished"
- [ ] Post: LayerZero integration — why decentralized bridge validators align with GSMA MNO model
- [ ] Thread: eUSD "how to use it right now" step-by-step guide (top community question)
- [ ] Post: Named telecom validator disclosure (if/when available)
- [ ] Post: TANIP1 activation timing — what users need to do and when
- [ ] Thread: TEL vs. XRP vs. XLM differentiation (preempt the comparison narrative)
- [ ] Post: DC Blockchain Summit rapid response (hold for Jeff Quigley signal)
- [ ] Post: "Coinmetro cancellation" transparency note (low priority, addresses lingering skepticism)
- [ ] Performance-numbers credibility framing (from Build Series Part 4 draft, 2026-07-24): state plainly that any throughput/latency/cost figures are simulated load-test results, not live mainnet data, rather than implying otherwise — "a network that hasn't proven itself under simulated load has no business claiming it'll hold up under real load." Positioned as a trust-building move, not a hedge. Apply this framing before publishing any performance-numbers content.

---

## Audience Segments & What They Respond To

*(Updated as we learn more. Start with research-based assumptions.)*

### TEL Holders / Crypto Community
- Want: Progress updates, governance transparency, staking info, roadmap milestones
- Respond to: Specific milestone completions, concrete numbers, honest timeline communication
- Avoid: Vague hype, moon talk, competitor attacks
- **Active questions (as of 2026-03-17)**:
  - "When is mainnet?" — #1 question; factual status thread produced 2026-03-17
  - "What can I do with eUSD right now?" — usage guide needed; partial answer in CBDC thread
  - "Who are the actual telecom validators?" — credibility gap; named list needed when available
  - "Is TANIP1 live yet?" — post-vote silence generating anxiety

### Telecom / MNO Executives
- Want: Revenue model clarity, regulatory credibility, technical readiness proof
- Respond to: GSMA alignment, Nebraska bank charter, institutional-grade security approach
- Avoid: Crypto slang, speculative pricing, NFT/meme content

### Crypto-Curious Retail (not yet holding TEL)
- Want: Simple explanation of what Telcoin does and why it matters
- Respond to: Remittance fee comparison, real-world use case stories, ease of entry
- Avoid: Technical jargon, complex governance explanations

### Developers
- Want: EVM compatibility, open-source access, clear documentation
- Respond to: GitHub links, technical specifics, build-now messaging
- Avoid: Marketing fluff, vague "ecosystem" language

---

## Campaign History

*(Log of campaigns completed. Updated each session.)*

| Campaign | Status | Deliverables | Date Completed |
|---|---|---|---|
| Agency OS setup | Complete | CLAUDE.md, AGENTS.md, WORKFLOW.md, DESIGN-TEAM.md | Mar 11, 2026 |
| Research foundation | Complete | TELCOIN-RESEARCH.md (fully populated) | Mar 11, 2026 |

---

## Open Questions for User

*(Things the agency needs clarification on. Ask in next session if not resolved.)*

- [ ] **CRITICAL — Entity boundary**: Need guidance from Ryan Neuner / commercial team: what can @telcoinTAO claim that originates from the MNO deck? Digital Cash currency counts, country license numbers, 3-billion-person targets — are these TA claims or Holdings claims?
- [ ] **CRITICAL — "Digital Cash" branding**: Is "Digital Cash" a Telcoin Association term or Telcoin Holdings term?
- [ ] Is there a preferred posting schedule / frequency for @telcoinTAO?
- [ ] Are there any topics / events that are embargoed or not to be discussed publicly?
- [ ] Who approves content before it posts? (user only, or council review needed?)
- [ ] Do we have access to @telcoinTAO for direct publishing, or are we drafting for someone else to post?
- [ ] What's the priority ranking: X/Twitter > YouTube > TikTok > Instagram? Or different?
- [ ] Are there any paid promotion budgets (for boosted posts, sponsored content)?
- [ ] GSMA whitepaper URL — confirm for first-reply placement on GSMA thread
- [ ] LP2 Post 4 — next post is TAN / Telcoin Wallet (eUSD/TDAB retired). Confirm before drafting.
- [ ] Jeff Quigley — next public appearance? Flag when known so rapid-response monitoring window opens.
- [ ] **@telcoinTAO follower baseline is unverified.** `campaign/04-ANALYTICS-FRAMEWORK.md` carries a 111,000-follower baseline (and every target/projection derived from it — the 10M+ impressions OKR, +29,000 follower target) with no source. The only measured figure on record is 4,573 (`intel-x-2026-03-30.md:17`), ~24x lower. Either the 111,000 figure describes a different, Holdings-operated account and must be relabeled, or it was assumed and the projection model needs rebuilding from a fresh `analytics.x.com` export. Flagged void as of 2026-07-30; not yet resolved.
- [ ] YouTube stats pipeline (`scripts/youtube-pull.py`, `infrastructure/n8n/workflow-youtube-to-github.json`) needs `YOUTUBE_API_KEY` set as an environment secret before it can run. Built and tested against fixtures 2026-07-31; not yet live.
- [ ] TELpets.xyz testnet-stress tweet (`campaign/execution/2026-04-03/twitter-telpets-testnet-stress.md`) is drafted but blocked: needs a `/tweet-card-brief` image spec, and confirmation of whether a TELpets X account exists to tag. The "120,000+ transactions" stat in the draft has no cited source — do not treat it as verified until sourced; it was not added to TELCOIN-RESEARCH.md for this reason.
- [ ] "Telcoin Network Build Series" Part 4 (`campaign/execution/2026-07-24/tel-network-build-series/`) is a skeleton only — contains `[PLACEHOLDER]` markers for throughput, latency, cost-per-tx, validator count, and comparison-chain numbers. Do not publish until real load-test figures replace the placeholders. Parts 1, 2, 3, 5 of the series are drafted and clean.

---

## Jeff Quigley Monitoring Protocol

When Quigley is at a conference or event, user should flag: "Jeff is at [event] — monitoring for signal"
- Agent monitors X for @jeffquigley posts, event hashtags, and press coverage during the window
- Any confirmed quote or policy development triggers a rapid-response draft within 2-4 hours
- Nothing posts without user review
- **Current status**: DC Blockchain Summit window closed (event ended Mar 18). No signal. Next event: TBD.

---

## Last Session Summary

*(Overwritten each session by Agents Orchestrator)*

**Date range processed by this dreaming pass**: 2026-04-03 through 2026-08-01 (7 session folders — first-run guard applied, since `.last-dream` had never been written despite 26 execution folders existing and two prior rounds of dreaming-pass bug fixes)
**What was produced**: Mostly infrastructure, not content, in this window. TELpets stress-test tweet drafted (2026-04-03, blocked on image spec). 5-part "Telcoin Network Build Series" drafted (2026-07-24; Part 4 is placeholder-only, not publishable). 2026-07-25/26/08-01 produced no content — execution folders contain only auto-generated SESSION-CONTEXT.md. 2026-07-30/31 rebuilt the sentiment analytics pipeline: found and quarantined 14 fabricated data files (see Lesson 11 in tasks/lessons.md), fixed an agent-roster routing bug (Analytics Reporter was pointed at the generic upstream file instead of the Telcoin-tuned one), corrected a wrong "YouTube blocks scraping" diagnosis from seven prior intel files, and built a YouTube stats + Restream council-chat pipeline via n8n.
**Key intel**: No new client/governance facts surfaced in this window — no intel files exist for any of the 7 dates processed (the standing Phase 0 intel sweep did not run on any of these days). This is itself a gap: `campaign/AGENCY-MEMORY.md`'s Standing Intelligence Sources section calls for a daily X/YouTube/market sweep, and none of the 7 processed sessions produced one.
**Blocked**: @telcoinTAO follower baseline unverified (111,000 vs. measured 4,573 — see Open Questions); YouTube pipeline needs `YOUTUBE_API_KEY`; TELpets tweet needs image spec + account confirmation; Build Series Part 4 needs real load-test numbers; Adiri public tweet (hold for official launch); GENIUS Act/eUSD angle (Ryan Neuner entity QA); TELx reward distribution (embargoed 3-6 months)
