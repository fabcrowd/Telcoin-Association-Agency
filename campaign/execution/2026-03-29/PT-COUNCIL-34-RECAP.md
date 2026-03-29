# P&T Council #34 — Meeting Recap
**Date**: March 26, 2026
**Meeting**: 34th Platform & Treasury Council recurring meeting
**Source**: Full transcript
**Processed**: March 29, 2026

---

## Chapters

```
00:00:00 Welcome & Mission Overview
00:05:08 Recap: Last Meeting Highlights
00:08:13 Telcoin Network Update — Grant Kee
00:14:29 Unified Web Presence — Nick P
00:19:40 Claude AI TELIP — Hayden
00:23:30 Q&A: MNO Partnerships & Validators
00:31:00 Q&A: Adoption, Security & DApps
00:53:00 Q&A: Mainnet Timeline & TEL Economics
01:07:00 Closing Remarks & Next Meetings
```

---

## Key Announcements

### 1. Adiri Testnet — Soft Launch Confirmed
- **Network is live** with real MNO validators — not simulated, not placeholder nodes
- Limited to an initial cohort of advanced MNO partners (more than 5)
- Described as a long-term parallel to mainnet; expected to be the most stable release yet
- Soft launch = limited audience observation phase before official public announcement
- Official testnet launch: "coming weeks" — full announcement to follow
- Block explorer (Telscan / Dex Guru) not yet updated for soft launch; coordination in progress

### 2. Database Layer Overhaul — Complete
- Full overhaul of the database layer described as "huge foundational improvement"
- Makes the network more reliable and resilient under high-volume conditions

### 3. Layer Zero Integration — Onboarding Started
- Cross-chain messaging and bridging protocol
- Parker met Layer Zero leadership at DOS conference in New York (March 25-26)
- Critical path dependency: TEL exists on other chains but not on Telcoin Network — bridge required for mainnet
- Mutual alignment confirmed

### 4. Claude AI TELIP — Presented by Hayden
- Proposal to provide Telcoin Association access to Claude AI across departments
- Structure: team plan + enterprise consumption-based tier for select users
- Qualifies for nonprofit pricing — reduces cost significantly
- Use cases: compliance, research, code, marketing, forecasting, dashboards
- Compatible with Slack, Trello, GitHub
- Admin controls and usage monitoring included
- Full proposal on forum.telcoin.org

---

## Network Development Update (Grant Kee)

**Completed since last call:**
- Large burst transaction handling — batches of 100+ transactions via RPC scripts
- Direct observer node integration for DApp developers — no third-party RPC subscription required; lowers builder barrier, improves performance
- CLI tooling for validator onboarding and staking transactions
- Decentralized testnet faucet — MNO partners and DApp developers can run independent faucets
- Attestation service — submits on-chain transaction verifying hash of committed code; part of PR feedback loop
- New documentation at docs.telcoin.network: base fees, gas limit penalties, EVM compatibility, epoch boundaries, chain growth concepts

**In progress:**
- Syncing time improvements for new nodes
- Epoch boundary record hardening
- Parallel fee lanes — separate transaction channels so real-world payments don't compete with arbitrage activity for block space
- AI-assisted security scanning and log analysis (tens of thousands of lines); described as significantly improving bug-finding efficiency
- Integration with Spiritbit and Cantina for third-party human security assessments — sequenced after AI scanning phase is exhausted

**Testing:**
- Stress testing ongoing and expanding
- Minor bugs found and resolved in real time — described as "exactly how the process is expected to work"
- Notable finding: default Rust/Ethereum library mempool cap of 16 transactions per address — identified, flagged, resolved
- Extensive end-to-end testing continuously expanding edge case coverage

**Security path to mainnet (Grant's summary):**
- Current: AI penetration testing stack + security experts using TEL tokens to run scans — still finding value
- Next: Spiritbit and Cantina human assessments — hundreds of thousands of dollars committed
- Goal: pass security assessments with no meaningful findings before mainnet

---

## Unified Web Presence Update (Nick P)

- Completing 4-5 week UX research phase — "almost at the finish line"
- Building phase begins March 27, 2026 (day after council meeting)
- Three tailored user journeys from homepage: retail/DeFi users, MNO validators, developers
- Pages: mobile homepage, MNO landing page, developer landing page with links to docs.telcoin.network
- SEO and GEO (AI-indexed content) addressed
- Analytics monitoring planned
- Council had a preview on Wednesday with positive internal feedback
- Target: launch before mainnet, or at mainnet at latest
- Demo site expected in approximately 4 weeks

---

## TELx Update (Ty Akemi)

- Evaluating new reward distribution model — details not public
- In direct communication with Holdings about new pools
- 3-6 month timeline before changes are visible publicly
- TELx Council call — Wednesday 3PM EST — teased an announcement worth attending

---

## Q&A Summary

**MNO partnerships beyond 5:**
- More than 5 partners total; soft launch limited to advanced partners comfortable with bug-finding
- Additional MNOs prepared to join post-official launch
- Official onboarding in progress; full network partner expansion follows official testnet launch

**TEL required for all transactions:**
- Confirmed — TEL is the native gas token for every transaction on Telcoin Network (analogous to ETH on Ethereum)

**Mainnet timeline:**
- Grant's goal: end of Q2 2026
- Three dependencies: MNO onboarding, LayerZero bridge, third-party security assessments
- Milestone-based; no committed date
- Phrasing to use: "Grant's goal is end of Q2" — never publish as a firm date

**Why MNOs choose Telcoin Network over other chains:**
- Ethereum/Bitcoin prioritize anonymity and decentralization at cost of scalability
- Telcoin Network trades theoretical open-validator decentralization for high hardware standards — enables maximum transaction throughput
- MNO consortium familiar with industry-standard coordination — already operates the world's largest networks
- Regulatory fit: MNOs are among the most regulated industries globally; anonymous validator sets create compliance conflict
- Telcoin Network provides a blockchain standard that folds into existing MNO infrastructure and workflow

**MNOs in governance:**
- Grant: expects MNO council participation "sooner than later"
- Exploring dedicated Telcoin Network Council comprised entirely of MNO participants
- TAO holds full administrative authority until 10 validators are live on mainnet — by design, for operational efficiency

**DApps on Telcoin Network:**
- Stablecoin payments and real-world payments confirmed as primary use cases discussed with MNO partners at MWC
- GSMA published a white paper on stablecoin importance
- Telcoin Wallet (Telcoin Holdings) is the first DApp developer on TAN
- Developer incentives tied to Telcoin Network transactions, not other chains (Polygon, Ethereum, etc.)

**V5 / Telcoin Wallet:**
- P&T Council has no knowledge of V5 development timeline or scope — separate Telcoin Holdings product
- Cannot and will not speculate on V5 launch timing relative to mainnet

**Security audits:**
- AI scanning currently providing significant value at low cost — "quickly running out of valid findings"
- Human assessments (Spiritbit, Cantina) follow once AI scans are exhausted
- Security is continuous — audits don't stop after mainnet

---

## Upcoming Dates

| Event | Date | Time |
|---|---|---|
| TELx Council #20 | Wednesday, April 1 | 3PM EST |
| TAN Council | Thursday, April 2 | 5PM EST |
| P&T Council #35 | Thursday, April 9 | TBD |
| P&T Council #36 | Thursday, April 23 | TBD |
| P&T Council #37 | Thursday, May 7 | TBD |

**TAN Council April 2 note**: Teased announcement — "stuff cooking in the kitchen." Nick also flagged the TELx call as worth attending.

---

## Content Unlocked by This Recap

**Cleared to publish (after research file confirm):**
- Adiri testnet soft launch — confirmed, real MNOs, major milestone — use carefully (soft launch framing only; do not overstate as full launch)
- Layer Zero integration started — factual, no speculation needed
- Unified web presence moving to build phase — factual update
- Parallel fee lanes development — strong technical differentiator post for LP2 or standalone

**Hold until official announcement:**
- TELx reward changes (3-6 months out, no public details)
- Any specific MNO names not already publicly disclosed
- V5 / Telcoin Wallet timeline

**Governance content:**
- Validator compliance seat election ended March 27 — compliance approval window now open (30 days)
- Claude AI TELIP proposal — on forum, can reference publicly

---

## Quotes (Usable with Attribution)

> "Telcoin stood as the only blockchain network at MWC Barcelona with over 100,000 attendees."
— James, P&T Council #34

> "Real MNOs are validators during this phase of testing."
— Confirmed on call, Derek + Grant

> "We're quickly running out of valid findings [from AI security scans]."
— Grant Kee, on AI penetration testing progress

> "If we get to those audits and we find fundamental issues that's going to significantly delay the project. What the benefit of using the AI scans right now is doing is helping us catch these types of bugs early."
— Grant Kee

> "This is not supposed to take months. This is, we're quickly moving towards an official launch here."
— Grant Kee, on testnet-to-mainnet timeline
