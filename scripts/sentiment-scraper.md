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

Run WebSearch (substitute the current year for `$YEAR` — do not hardcode it):
- `Telcoin news $YEAR`
- `"TEL token" news`
- `Telcoin blockchain`

Collect article titles and snippets from: CoinDesk, CoinTelegraph, Decrypt, The Block, Benzinga, Business Wire, PRNewswire, crypto news outlets.

Exclude: results older than 7 days. Classify sentiment of headline + snippet.

---

## Step 4 — Build and Save JSON

Count totals across all collected posts. Compute:

**sentiment_score** = (positive_count) / (positive_count + neutral_count + negative_count)
- Clamp to 0.01–0.99
- Always record `n` (the total classified) alongside it. A 0.70 from 7 posts and a 0.70 from
  200 posts are different facts; the score is meaningless without its sample size.

**activity_score** — REMOVED. It was normalized against an invented "historical max" of 120,
which made it unitless and uninterpretable. Report `total_mentions` as a raw observed count
with its collection method instead. Do not reintroduce a 0–10 composite.

**hour_distribution** = count of posts by UTC hour (0–23), plus an `"unknown"` bucket.

Record a post's hour ONLY if the timestamp is actually visible. If it is not, increment
`"unknown"`. Never estimate, interpolate, or distribute posts across hours — a manufactured
hour grid is worse than an empty one. The sum of all buckets including `"unknown"` must equal
`total_mentions` exactly; if it does not, the file is wrong and must not be written.

Search results rarely expose timestamps, so expect `"unknown"` to dominate until a source with
real timestamps (Reddit API) is wired in. That is the honest state and the dashboard renders it
as such.

**narrative counts** = for each narrative in `campaign/analytics/NARRATIVE-TAXONOMY.json`,
record the raw count of posts tagged with it, split by platform, plus its own
positive/neutral/negative tally and its unique-author count.

Do not compute a weighted "topic score". The previous formula included a term
(+0.5 per high-engagement post) that always evaluated to zero because engagement was never
captured, and blending platform weights into a single float destroyed the ability to audit
where a number came from. Store the counts; derive shares at render time.

**top_narrative** = narrative with the highest community mention count. Record it only when
the leader is separated from second place by more than the sampling noise; otherwise write
`null`.

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

Build the complete artifact HTML with all historical data embedded.

**Do not author the artifact from scratch.** Fetch the current published artifact with WebFetch
against ARTIFACT_URL, replace only the `RAW` data constant with the recompiled series, and
republish. The chart code, styling, and panel structure carry forward unchanged. If the fetch
fails, the artifact source of record is the last version committed under
`campaign/analytics/sentiment/dashboard.html`.

**Never plot a file whose `data_status` is not `"measured"`.** Files marked `seed_synthetic` or
`partial` are excluded from the series and counted only in the "days collected" tally.

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
