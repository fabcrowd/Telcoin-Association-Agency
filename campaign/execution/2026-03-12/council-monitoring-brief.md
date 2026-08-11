# Council Monitoring Brief — March 12, 2026
## Platform & Treasury Council | 4:00 PM EST
## TAN Council | 5:00 PM EST

**Prepared by**: Marketing Agency
**Prepared at**: March 12, 2026 — pre-session (before 3:45 PM EST)
**Classification**: Internal use only

---

## PUBLISH-READY CHECKLIST

- [x] This document is internal — no sign-off required for the monitoring brief itself
- [ ] Any live tweet drafted during streams must be reviewed by a second set of eyes before posting
- [ ] Do not post speculative, unconfirmed, or price-adjacent commentary in real time
- [ ] Quotes must be attributed correctly — speaker name or "team" — never put words in anyone's mouth
- [ ] All tweets from @telcoinTAO must comply with brand voice rules: no hype language, no timeline claims without citing roadmap.telcoin.network
- [ ] If a major unannounced milestone drops during the stream, hold the tweet — draft it, flag it, do not post until confirmed with the team

---

## SECTION 1 — TOP 5 COMMUNITY QUESTIONS & COUNCIL ROUTING

The following questions are the highest-frequency and highest-urgency signals from the X/Twitter community intelligence report (March 10–12, 2026). Each is mapped to the council stream most likely to address it today.

---

### Q1. "When is mainnet launching — can we get an actual date or range?"

**Source**: Most-cited question across X, Reddit r/Telcoin, and forum threads. Community is treating "sometime in 2026" as insufficient.

**Council routing**: Platform & Treasury Council (4 PM EST) — primary

The Platform & Treasury Council owns testnet infrastructure and mainnet readiness sequencing. Any update on p2p networking hardening completion, syncing strategy finalization, or security assessment scheduling will directly feed a response to this question. Listen for language around how many Phase 2 tasks remain open vs. closed, and whether any milestone gate is within weeks rather than months.

**What to capture**: Any framing around sequence clarity — even "X is the last task before we can schedule the BLS assessment" is quotable and useful.

---

### Q2. "Why is the price down -66% if the fundamentals are so strong?"

**Source**: X posts from @BSCNews, community holders, inferred from sentiment score of 5/10 in the intel report.

**Council routing**: Neither council will address price directly — and they should not. However, the TAN Council (5 PM EST) may surface relevant context indirectly.

The TAN Council is most likely to produce content that counters the underlying anxiety: TANIP-1 implementation confirmation (real utility, real mechanics), builder demos (evidence of ecosystem growth), and TELx University launch timeline (tangible product ready for users). These are the factual anchors that reframe the price-frustration narrative without commenting on price.

**What to capture**: Any concrete deliverable, shipped feature, or measurable milestone that can be communicated as proof of progress — regardless of which council surfaces it.

---

### Q3. "What does eUSD actually do for TEL token value — is there a real utility link?"

**Source**: Community accounts on X (notably @ItsTheJuggler) are building their own unofficial utility thesis. No official counter-narrative exists.

**Council routing**: TAN Council (5 PM EST) — primary; Platform & Treasury (4 PM EST) — secondary

TANIP-1 mechanics are the clearest bridge here. If the rebate program is confirmed operational today, the loop becomes: eUSD/Wallet activity generates fees → staked TEL determines rebate percentage → more staking = more TEL locked → demand signal. The Platform & Treasury Council may also surface validator-level economics that connect network activity to TEL utility.

**What to capture**: Any direct statement linking staking mechanics, fee flow, or on-chain activity to TEL demand. This is the raw material for a future utility explainer thread.

---

### Q4. "How does TEL compare to XRP and RLUSD — why should I hold TEL instead?"

**Source**: X community comparisons, @BSCNews framing, competitor monitoring in intel report. Ripple's RLUSD is the most pressing narrative threat.

**Council routing**: Platform & Treasury Council (4 PM EST) — primary (GSMA MNO validator updates are Telcoin's clearest differentiator from Ripple's institutional model)

Any update on MNO validator onboarding readiness, GSMA collaboration status, or DC Blockchain Summit presence will sharpen the differentiation story. The GSMA angle — only blockchain where licensed, accountable telecom operators run the validation layer — is the most defensible moat against XRP/RLUSD comparisons and it is Platform & Treasury territory.

**What to capture**: Specific MNO collaboration language (even if non-specific on names), any validator onboarding timeline, any language about the telecom infrastructure distinction.

---

### Q5. "What is Merkl and when does the incentivized liquidity program go live?"

**Source**: DeFi-aware X holders and forum discussions. The Merkl trial passed 6/6 unanimous vote on March 10 but has not been publicly explained on X.

**Council routing**: TAN Council (5 PM EST) — primary (TELx governance crossover; Leo is the key contact point on Merkl-adjacent governance updates)

The TAN Council is likely to reference Merkl in the context of TANIP-1 and TELx incentive structure updates. Any governance update touching on how the Merkl trial interacts with the rebate program or staking incentives should be captured. The TELx Council on March 18 will be the deeper dive — but today's TAN session may produce the first post-vote public language on implementation.

**What to capture**: Any reference to Merkl implementation timeline, Base V4 pool setup language, or governance coordination between TAN and TELx on incentives.

---

## SECTION 2 — PLATFORM & TREASURY COUNCIL (4:00 PM EST)
### What to Listen For

This is the 27th recurring Platform & Treasury Council. Based on the research file (last updated March 11, 2026) and the "3 Weeks of Progress" video intel, the following items are actively in motion and likely to surface. Monitor for updates, not assumptions.

---

#### FLAG 1 — P2P Networking Hardening: Completion Status

**Context**: "Production harden p2p networking" is listed as In Progress on the roadmap as of February 19, 2026. It is one of the remaining open Phase 2 tasks blocking the path to network relaunch and the subsequent Phase 3 work.

**What to listen for**:
- Has p2p networking hardening been completed, or is it still actively in development?
- Is there a specific remaining blocker — e.g., stress testing results, latency benchmarks, geographic node coverage?
- Any language connecting p2p hardening completion to the timeline for the BLS external security assessment

**Why it matters**: P2p networking completion is a precondition for stress testing the network at scale, which is a precondition for external audits. A completion signal here compresses the perceived distance to mainnet meaningfully.

**Quote signal**: Listen for Grant (leads security strategy) describing the state of p2p in past vs. present tense. "We are hardening" vs. "we hardened" is a meaningful distinction.

---

#### FLAG 2 — BLS External Security Assessment: Scheduling Status

**Context**: From the research file (Platform & Treasury Council recap, week of Mar 10): all internal BLS cryptographic library findings are resolved. The next step is scheduling the external assessment with top EVM security researchers, many of whom were identified/approached at ETH Denver.

**What to listen for**:
- Has the external BLS security assessment been formally scheduled with a named firm or researcher?
- Is there a timeframe for the assessment to begin — even a range (e.g., "Q2 2026", "within 6 weeks")?
- Any update on the sequencing: BLS assessment first, then comprehensive protocol audits — is that ordering still confirmed?
- Any language about researcher availability, exclusivity windows, or scope agreement

**Why it matters**: The BLS external assessment is the first audit in the chain leading to mainnet. Its scheduling is a concrete milestone that can be communicated externally without revealing timeline commitments. Even "we have engaged a firm" is meaningful.

**Quote signal**: Any mention of a named security partner, a signed engagement, or a date range for assessment commencement.

---

#### FLAG 3 — TANIP-1 Implementation Status (Platform Layer)

**Context**: TANIP-1 passed snapshot vote and moved into implementation. The platform layer must support the rebate mechanics — specifically, the on-chain accounting for fee flows and rebate calculations tied to staked TEL position.

**What to listen for**:
- What is the platform infrastructure status for TANIP-1? Is the smart contract layer ready, in testing, or pending deployment?
- Any coordination notes between the Platform Council and TAN Council on TANIP-1 go-live timing
- Any flag on the sliding scale mechanism — how is staked TEL position read by the rebate contract? Is there an oracle or on-chain lookup?
- Any risk flags or open issues that could delay TANIP-1 from hitting its late March 2026 target

**Why it matters**: The TANIP-1 rebate program (up to 100% TEL rebates on trading fees, sliding scale tied to staked TEL) is the most direct user-benefit story in current development. A confirmed go-live date is high-value content.

**Quote signal**: Any mention of deployment target, contract audit status, or "we are ready to deploy" language.

---

#### FLAG 4 — DC Blockchain Summit: Team Presence and Talking Points

**Context**: Telcoin Association is a confirmed Bronze Sponsor at the DC Blockchain Summit, March 17–18, 2026 in Washington DC. The team is attending. Based on prior MWC Barcelona pattern (private MNO meetings, no public mainnet reveal — intentional), the Summit may follow a similar strategy.

**What to listen for**:
- Who from the team is attending? Named individuals = humanizes the brand and enables pre-event content
- What is the strategic objective for the Summit — institutional networking, MNO outreach, press presence, regulatory conversations?
- Are there any scheduled speaking slots, panel appearances, or side meetings that can be surfaced publicly?
- What is the approved public message for the Summit — what can @telcoinTAO amplify during the event?
- Any coordination instructions for the agency on real-time coverage vs. post-event recap

**Why it matters**: The Summit is five days away. Pre-event content activation should start no later than March 13. Any team messaging guidance captured today directly informs the Summit content plan.

**Quote signal**: Names of attendees, any approved "what we're bringing to DC" framing, any explicit ask for social amplification from the team.

---

## SECTION 3 — TAN COUNCIL (5:00 PM EST)
### What to Listen For

The TAN Council governs the TAN (Telcoin Association Node) ecosystem — staking, builder programs, developer onboarding, and protocol improvement proposals. TANIP-1 is the live item. Based on research file intel from the week of March 10, 2026 and the YouTube intel file.

---

#### FLAG 1 — TELx University: Launch Timeline

**Context**: TELx University is described as ~95% complete in the research file. Five refinement areas remain: AI voice pacing, diagram quality, navigation links, closing recap video, and NFT gamification finalization. Leo and Storm are leading the handover.

**What to listen for**:
- Is there a confirmed launch date or week? Even "by end of March" or "before the Merkl trial goes live" would be a quotable milestone
- What is the status of the five open refinement items — have any been completed since the last recap?
- Is the NFT gamification component a hard dependency for launch, or will University launch without it and add it post-launch?
- Any community access logistics — is it gated, open, subscriber-based?

**Why it matters**: TELx University is a tangible, community-facing product that demonstrates ecosystem maturity and reduces the LP complexity friction that is currently limiting participation. Its launch is a standalone content moment.

**Quote signal**: Any specific launch date, access model, or "we're cutting X feature to ship sooner" language.

---

#### FLAG 2 — TANIP-1 Rebate Mechanics: Exact Staked TEL to Rebate Percent Curve

**Context**: TANIP-1 passed snapshot and is in implementation. The approved structure is a sliding scale: staked TEL position determines the percentage of trading fees rebated, up to 100% TEL rebates. The specific curve — the formula or tier table mapping staked TEL amounts to rebate percentages — has not been publicly documented in detail.

**What to listen for**:
- Is there a published or discussed tier table? Example structure: 0–10K TEL staked = X% rebate; 10K–100K = Y%; 100K+ = 100%?
- Is the curve linear, stepped, or formula-based?
- What is the minimum staking threshold to qualify for any rebate?
- Is the rebate calculated on cumulative fees or per-transaction?
- What is the total TEL budget allocated to rebate distribution per period?
- Any cap per user per period, or is it uncapped at 100%?
- Deployment timeline for the rebate contracts — is late March 2026 still the target?

**Why it matters**: The rebate curve is the single most actionable piece of information for a TEL staker making decisions right now. Publishing a clear explainer with actual numbers will drive more staking behavior than any amount of narrative content. This is the raw data needed for a community-facing explainer.

**Quote signal**: Any numbers attached to staking tiers, any mention of the contract design for the sliding scale, any "you need to stake at least X TEL to receive any rebate" framing.

---

#### FLAG 3 — Builder Demos

**Context**: From research file and YouTube intel, confirmed active builders in the TAN Council ecosystem include:
- Cody: Random square guessing game (no-loss lottery micro-app, ~$1 entry, 10% to TAN treasury, 90% prize pot, Chainlink VRF integration planned, will migrate to Telcoin Network at mainnet)
- Telcoin Name Service: .tel human-readable addresses (e.g., cody.tel, dolly.tel) — ENS equivalent for the Telcoin ecosystem
- Leo: Charity NFT Subscription — revokable NFTs tied to streamed on-chain donations

**What to listen for**:
- Any live demo or update from Cody on the guessing game — is Chainlink VRF integration complete? Is there a playable version?
- Telcoin Name Service status: is there a testnet deployment, a resolution contract, or a UI in development?
- Leo's Charity NFT: any named charity org being approached, any timeline for the first NFT mint?
- Any new builder appearing for the first time — this would be a signal of ecosystem growth worth capturing
- Any discussion of a builder grant program, funding allocation from the 350M TEL TAN budget, or formal onboarding process for new builders

**Why it matters**: Builder demos are the most concrete proof of ecosystem activity. Each one is a standalone content story that counters the "nothing is happening" price-frustration narrative with specific, verifiable evidence.

**Quote signal**: "We deployed X to testnet," "we have Y users," "the first mint happens when Z" — anything concrete and quotable.

---

#### FLAG 4 — Merkl-Adjacent Governance Updates

**Context**: The Merkl trial was approved 6/6 unanimous vote in the TELx Council on March 10, 2026. The trial is scoped to the Base V4 TEL/ETH pool, running in parallel against the current hook system (~April 2026 live, mid-May analysis). However, TAN Council governance intersects with TELx on staking economics, TANIP-1 rebate flows, and how the Merkl per-position gating interacts with TAN staking tiers.

**What to listen for**:
- Any TAN Council discussion of Merkl's interaction with the staking rebate program — are stakers who provide liquidity treated differently under Merkl vs. the hook system?
- Any governance proposal or discussion about whether Merkl should eventually replace the hook system entirely — is this on the TAN Council's radar?
- Any language about how new pools (eXYZ stablecoins, Telcoin Holdings corridors) will be governed for incentives as they are added — does TANIP-1 need an amendment to accommodate Merkl-distributed rewards?
- Any timeline confirmation for the Merkl trial going live (~April 2026 is the current estimate — has this been reconfirmed or shifted?)

**Why it matters**: The Merkl trial is the most significant TELx governance development since the Uniswap V4 migration. Its governance implications for TAN stakers are not yet publicly documented. Any clarification today will directly feed the pre-launch Merkl explainer content.

**Quote signal**: Any framing of "how Merkl changes what stakers can expect," any governance vote anticipated before the April live date, any language about the trial evaluation criteria being set by TAN vs. TELx.

---

## SECTION 4 — LIVE-TWEET TEMPLATE

Use these five template slots during either stream. Fill in the blanks in real time. Review before posting — do not auto-post from notes without a read-through.

**Brand voice reminders before posting**:
- No hype language. "This is significant" beats "this is massive."
- No timeline claims without linking roadmap.telcoin.network
- Attribution matters — "according to [speaker]" or "in today's council" — not stated as fact if it is a council discussion point
- Keep under 280 characters per tweet where possible; use thread format if more context is needed

---

### TWEET SLOT 1 — Opening / Framing Tweet (Post at stream start or first notable statement)

```
[LIVE] Platform & Treasury Council / TAN Council is underway.

Today's agenda: [1-2 items most likely to be discussed based on this brief].

Watching and will share key updates. Full recording will be on youtube.com/@TelcoinTAO.
```

**Format notes**: Sets audience expectation. Signals that @telcoinTAO is present and engaged. Do not make claims about what will be announced — frame as "what we're watching."

---

### TWEET SLOT 2 — Infrastructure / Technical Milestone Quote

```
"[EXACT QUOTE FROM SPEAKER]" — [Speaker name or role], Platform & Treasury Council

[1-sentence context line explaining why this matters — no jargon, no hype.]

More at roadmap.telcoin.network
```

**Format notes**: Quote first — the speaker's words carry more weight than our framing. Context line is for the non-technical follower. Link to roadmap when the quote touches on mainnet readiness or security assessment progress. Ideal for a Grant or Steve quote on p2p hardening, BLS assessment scheduling, or database infrastructure.

---

### TWEET SLOT 3 — Governance / Product Update Quote

```
"[EXACT QUOTE FROM SPEAKER]" — [Speaker name or role], TAN Council

[1-sentence plain-language translation of what this means for TEL holders or stakers.]

Details: forum.telcoin.org
```

**Format notes**: Quote first. Translation line should answer "what does this mean for me?" without being promotional. Link to forum for full governance context. Ideal for TANIP-1 rebate mechanics confirmation, TELx University launch date, or builder demo updates.

---

### TWEET SLOT 4 — Community Question Response (Use if a council speaker directly addresses a community question)

```
Community has been asking: [paraphrase of the community question from Section 1 of this brief]

From today's [Platform & Treasury / TAN] Council: "[EXACT QUOTE OR CLOSE PARAPHRASE FROM SPEAKER]"

[1 sentence on what this means going forward.]
```

**Format notes**: Framing this as a community question being answered closes the loop with the people asking. It signals that the team is listening. Only use this slot if the speaker's language is genuinely responsive — do not force a connection that is not there. Ideal if mainnet sequencing, TANIP-1 mechanics, or eUSD/TEL utility is directly addressed.

---

### TWEET SLOT 5 — Closing / Recap Tweet (Post within 30 minutes of stream ending)

```
Today's [Platform & Treasury / TAN] Council wrap-up:

- [Bullet: 1 technical/infrastructure update]
- [Bullet: 1 governance/product update]
- [Bullet: 1 ecosystem/builder update]

Full recording: youtube.com/@TelcoinTAO
Next up: [next scheduled council or event — e.g., TELx Council March 18, DC Blockchain Summit March 17-18]
```

**Format notes**: Bullet format for scannability. Three bullets maximum — this is a summary, not a transcript. Each bullet should be one verifiable fact from the session. End with the YouTube link and the next event to maintain forward momentum in the feed. Do not speculate on what the updates mean for price or token value.

---

## MONITORING NOTES SECTION (Fill in live during sessions)

Use this space for raw notes during the streams. These notes are internal only — do not post raw notes.

### Platform & Treasury Council — 4:00 PM EST

**P2P Networking Hardening**:


**BLS External Security Assessment**:


**TANIP-1 Implementation (Platform Layer)**:


**DC Blockchain Summit Team & Talking Points**:


**Other notable items**:


---

### TAN Council — 5:00 PM EST

**TELx University Launch Timeline**:


**TANIP-1 Rebate Curve (staked TEL to rebate % data)**:


**Builder Demos**:


**Merkl-Adjacent Governance**:


**Other notable items**:


---

## POST-SESSION CHECKLIST

After both streams complete:

- [ ] Update `campaign/research/TELCOIN-RESEARCH.md` with any new confirmed facts, dates, or statements from either council
- [ ] Flag any content unlocked by today's sessions — list the posts, threads, or explainers that can now be written with verified information
- [ ] Note any open questions that remain unresolved — these become monitoring priorities for the next session
- [ ] If TANIP-1 rebate curve numbers were confirmed, brief the agency team immediately — this is the highest-urgency content item currently outstanding
- [ ] Confirm DC Blockchain Summit content plan is activated by end of day March 12 — event is March 17–18

---

*Brief prepared: March 12, 2026. Internal use only. No distribution without agency team review.*
