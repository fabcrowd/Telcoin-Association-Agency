# TEL Sentiment Scraper — Daily Social Intelligence

Runs daily as a scheduled trigger. Scrapes social sentiment for $TEL / Telcoin across
X/Twitter, Reddit, and crypto news. Outputs structured JSON and regenerates the heat map artifact.

This is not a content production session. The sole purpose is data collection, sentiment
classification, and artifact refresh.

## Artifact URL (update this line when the artifact is recreated)

ARTIFACT_URL: https://claude.ai/code/artifact/bef233aa-60df-4736-936c-ff7663cfdf20

## Setup

```bash
cd /home/user/Telcoin-Association-Agency
git fetch origin claude/campaign-iLgt5
git checkout claude/campaign-iLgt5
git pull origin claude/campaign-iLgt5
```

Get today's date:
```bash
TODAY=$(date -u +%Y-%m-%d)
echo "Running sentiment scraper for $TODAY"
```

Check if today's file already exists — if yes, skip scraping and go to Step 5 (artifact refresh):
```bash
ls campaign/analytics/sentiment/$TODAY.json 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

---

## Step 1 — Scrape X/Twitter

Run WebSearch for each of the following queries. Collect all visible results.

Search queries (run each separately):
- `$TEL crypto site:twitter.com OR site:x.com`
- `Telcoin site:twitter.com OR site:x.com`
- `"Telcoin Network" site:twitter.com OR site:x.com`
- `@telcoinTAO`

For each result found, record:
- Post text (first 200 chars)
- Estimated engagement weight (1.0 = average, 2.0+ = high engagement based on visible reply/RT signals)
- Sentiment classification (see Sentiment Rules below)
- Time of post (UTC hour if visible)

**Sentiment Rules:**
- **Positive**: price optimism, milestone celebration, technical achievement praise, project support, "bullish", buying signals, governance approval
- **Negative**: price frustration, FUD, project criticism, "wen", "dead", "dump", sell signals, governance dissatisfaction
- **Neutral**: factual updates, news shares, technical questions, price observation without opinion, governance observation

**Topic Tags** — tag each post with all that apply:
- `mainnet` — references to mainnet launch, launch timing, Adiri testnet, hardening
- `governance` — council meetings, proposals, votes, TELIPs, TANIPs
- `price` — price action, market cap, exchange listings, buy/sell
- `staking` — TAN staking, TANIP, reward distribution, staking mechanics
- `validators` — MNO validators, GSMA, ConsensusNFT, validator onboarding
- `tel_upgrade` — TEL token upgrade, 18 decimals, migration
- `layerzero` — bridge, cross-chain, LayerZero V2
- `telx` — TELx liquidity, liquidity mining, Merkl, pools

---

## Step 2 — Scrape Reddit

Run WebSearch:
- `Telcoin site:reddit.com`
- `"$TEL" site:reddit.com`
- `"TEL coin" site:reddit.com`

Target subreddits: r/Telcoin, r/CryptoCurrency, r/CryptoMoonShots, r/altcoin

For each result: post title, subreddit, sentiment, topic tags. Apply same sentiment rules as Step 1.

---

## Step 3 — Scrape News

Run WebSearch:
- `Telcoin news 2024`
- `"TEL token" news`
- `Telcoin blockchain`

Collect article titles and snippets from: CoinDesk, CoinTelegraph, Decrypt, The Block, Benzinga, Business Wire, PRNewswire, crypto news outlets.

Exclude: results older than 7 days. Classify sentiment of headline + snippet.

---

## Step 4 — Build and Save JSON

Count totals across all collected posts. Compute:

**sentiment_score** = (positive_count) / (positive_count + neutral_count + negative_count)
- Clamp to 0.01–0.99

**activity_score** = normalize(total_mentions, 0, 120, 0, 10)
- 120 = approximate historical max. If total > 120, score = 10.

**hour_distribution** = count of posts by UTC hour (0–23). If hour not visible for a post, distribute evenly.

**topic_scores** = for each topic tag, sum: 1.0 per mention + 0.5 per high-engagement post (weight ≥ 2.0) + 0.3 per Reddit post + 0.5 per news article.
Clamp each to 0–10.

**top_narrative** = topic with highest topic_score.

Save output to:
```bash
campaign/analytics/sentiment/$TODAY.json
```

---

## Step 5 — Regenerate Heat Map Artifact

Read all JSON files:
```bash
ls campaign/analytics/sentiment/*.json | sort
```

Compile all data into a single JavaScript constant. For each file, extract:
- date
- composite.sentiment_score
- composite.activity_score
- composite.total_mentions
- composite.hour_distribution
- composite.topic_scores

Build the complete artifact HTML with all historical data embedded (see artifact template in
`campaign/analytics/sentiment/ARTIFACT_TEMPLATE_NOTE.md`).

Call the Artifact tool to update the artifact at ARTIFACT_URL (see top of this file).
The artifact title is "TEL Social Intelligence" and favicon is "📊".

If ARTIFACT_URL is not set or returns an error, create a new artifact and update the
ARTIFACT_URL line in this file.

---

## Step 6 — Commit and Push

```bash
SESSION_URL="https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/cse_/session_}"
git add campaign/analytics/sentiment/$TODAY.json
git commit -m "Sentiment scrape $TODAY: $(cat campaign/analytics/sentiment/$TODAY.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(f\"{d[\"composite\"][\"total_mentions\"]} mentions, sentiment {d[\"composite\"][\"sentiment_score\"]:.2f}\")')

$SESSION_URL"
git push origin claude/campaign-iLgt5
```

---

## Step 7 — Report

Output:
- Date scraped
- Total mentions found (by platform)
- Sentiment score
- Activity score
- Top narrative
- Artifact updated: yes/no
