# Weekly Intel — Week of 2026-07-27

First run of the new weekly sweep (`scripts/weekly-intel-sweep.md`, replacing the daily
Phase 0 that was never actually triggered). Neither `campaign/analytics/sentiment/` nor
`campaign/analytics/youtube/` has any data yet for this week — both pipelines were only built
2026-07-30/31 and haven't had a scheduled run. Everything below is a **fallback snapshot read**,
not derived from the structured daily pipelines, and is labeled as such throughout. Richer
day-by-day sections should appear automatically once those pipelines accumulate a few days of
real data.

## Market & Ecosystem — this week (as of 2026-08-01)

- **Telcoin Wallet v5 launched regulated on-chain bank accounts (June 23, 2026)**: US users can open an FDIC-path bank account tied to eUSD, via Battle Creek State Bank, building on TDAB's November 2025 charter. Content opportunity — a Learning Path or Tier 1 post confirming the live feature with verified specifics.
- **TEL listed on Kraken for US access (January 26, 2026)** — supports the institutional-credibility narrative. Low-key factual mention, not hype-driven.
- **Mainnet still tracking Q1 2026, no new date** — Feb 19 roadmap update shows P2P streaming, DB hardening, custom RPC progress; Adiri remains the active public environment. No change to current messaging.
- **MWC Doha speaking slot — date unverified** (search results conflict: July 23 vs. November 2026). Do not draft content from this until the date is confirmed.
- **Stablecoin regulation has reached critical mass under the GENIUS Act** — banks broadly launching their own products in 2026, OCC overseeing a growing field of issuers. **Threat**: the "first bank-issued on-chain stablecoin" claim in `TELCOIN-RESEARCH.md` needs re-verification against the now-normalized landscape — consider whether it needs a date-stamped qualifier.
- **Western Union launched USDPT** (dollar stablecoin on Solana with Anchorage Digital, March 2026), piloting settlement across 360,000 cash payout points. **Threat**: a legacy remittance incumbent moving directly into stablecoin rails — the differentiation story (LP3, not started) needs to account for incumbents adopting stablecoins, not only crypto-native competitors.
- **Visa + M-Pesa piloting stablecoin cross-border settlement in DR Congo (July 2026)**; separately, ADI Foundation partnering with M-Pesa across 8 African countries. **Threat**: this is the exact mobile-money corridor Telcoin's financial-inclusion thesis targets, and competitors are securing distribution first. LP3 differentiation content should have a specific answer for what the telecom-validator model offers that a Visa/M-Pesa stablecoin bolt-on does not.
- **Stellar's tokenized RWA value grew from $796M to $2B+ (end of 2025 → mid-April 2026)**, Q1 payment volume up 72% YoY. **Threat**: Stellar has clearer, larger recent adoption numbers than Telcoin currently has. LP3/LP4 content should have a specific, factual "why Telcoin vs. Stellar" answer ready.

*Sources: [Crowdfund Insider](https://www.crowdfundinsider.com/2026/06/287418-telcoin-enables-regulated-on-chain-bank-accounts-for-us-consumers/), [Forbes — Western Union](https://www.forbes.com/sites/digital-assets/2026/05/29/western-unions-stablecoin-automates-the-end-of-its-own-margin/), [Visa/M-Pesa — Bitcoin.com News](https://news.bitcoin.com/visa-launches-stablecoin-pilot-with-m-pesa-in-drc-to-test-cross-border-transfers/), [ADI Foundation/M-Pesa — Decrypt](https://decrypt.co/353935/adi-foundation-partners-with-m-pesa-to-bring-60-million-mobile-money-platform-users-onchain)*

## Council Activity This Week

None processed this week. Only a March 2026 test transcript exists in `transcripts/processed/`.

---

## Day-by-Day

## 2026-08-01

**X/$TEL sentiment — current-state read (not day-attributed).** No `campaign/analytics/sentiment/2026-08-01.json` exists, so this is a single WebSearch snapshot, not a per-day measurement, and the sample is whatever the search engine surfaced rather than a systematic 24h capture.

- Sentiment reads as steady/neutral-positive: recent activity centers on the Kraken listing, Base support, and the Uphold exchange listing rather than any visible controversy.
- **Notable — connects to an open blocker**: a TAN Council meeting notice (agenda dated April 2, 2026) and a P&T Council notice (April 9, 2026) both list **"TELpets" / "TEL Pets Demo"** as an agenda item. This is independent evidence a TELpets product exists and has council visibility — relevant to the blocked TELpets stress-test tweet in `AGENCY-MEMORY.md` Open Questions (still needs an image spec and confirmation of a TELpets X account; this does not resolve either, but confirms the product is real and council-visible).
- A TELx Council notice references a prospective $eMXN/$USDC pool on Polygon with a ~2.4M TEL/month incentive under discussion — not yet in `TELCOIN-RESEARCH.md`; needs confirmation before use in content.
- No visible negative-sentiment spike or unanswered-question cluster in this snapshot. Not a substitute for the structured daily read once `sentiment-scraper.md` is running.

**YouTube — no data available this week.** No `campaign/analytics/youtube/2026-08-01.json` exists. The `WebFetch` tool was tested against `youtube.com/@TelcoinTAO/videos` and confirmed to return only page boilerplate — it converts the page to markdown before returning it, which strips the JSON the video list actually lives in. No reliable fallback exists without the API key; reporting the gap rather than guessing. **Blocker**: `YOUTUBE_API_KEY` still needs to be set as an environment secret (tracked in `AGENCY-MEMORY.md`).
