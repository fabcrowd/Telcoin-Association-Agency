# TEL Sentiment Scraper — Social Intelligence

**Cadence: daily — every 24 hours** (reverted from twice-weekly 2026-08-02; user explicitly wants
a continuous historical backlog and accepts the ~3x token cost of daily per-post LLM classification
over the Mon/Thu schedule). Each run collects the trailing 24 hours only — see the Setup section's
existing-file check, which still skips a run if today's file already exists. Everything downstream
degrades gracefully on any day a run is missed: the dashboard plots only `measured`/`measured_backfill`
files, and the weekly digest labels gaps rather than inventing them (never fabricate a missing day —
see `tasks/lessons.md` Lesson 11).

**Automation**: a daily cron trigger runs this spec automatically. If the trigger ever misfires,
run it manually via this file — the existing-file check makes re-runs safe.

Scrapes social sentiment for $TEL / Telcoin across X/Twitter, Reddit, and crypto news. Outputs
structured JSON and regenerates the heat map artifact.

**Price/market context comes from the CoinGecko MCP, not WebSearch.** The `coingecko` server in
`.mcp.json` (free, no key) returns TEL price, market cap, and volume as a structured call — use it
for any price figure this run needs instead of spending WebSearch tokens on it. Note the standing
rule still applies: this data is for *listening context only*; @telcoinTAO never publishes price
commentary (`price` is a `publishable: false` narrative).

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

## Step 0b — Backfill Mode (one-time)

Run this once to seed a historical backlog, then never again — daily runs from Step 1 onward
build the archive forward in real time.

**What backfill can and cannot do.** WebSearch only returns what is currently indexed and live.
There is no way to query "what did sentiment look like on a past date" — that data was never
captured at the time and cannot be reconstructed after the fact. A backfilled day is therefore
**not equivalent to a daily `measured` run** and must never be presented as one. This is the same
failure mode `tasks/lessons.md` Lesson 11 quarantined 14 files for (fabricated-looking completeness)
— the fix here is honest labeling, not another synthetic dataset.

What backfill *can* honestly do: run the normal Step 1/2/3 searches now, and for any result that
happens to expose a **real, visible historical timestamp** (Reddit shows post dates; some X/Twitter
snippets show an absolute or resolvable relative date), file that post under its true historical
date instead of today's file. This recovers a sparse, survivorship-biased sample of durable/
high-engagement old content still sitting in the index — real posts, real dates, but a floor on
that day's actual volume, never a census.

**Procedure:**
1. Run the Step 1 (X/Twitter) and Step 2 (Reddit) search queries as written. Do not run Step 3
   (News) for backfill — dated news either has a real publish date already or doesn't qualify;
   there's nothing backfill-specific to add there.
2. For each result, check `posted_at`. If there is no real, verifiable date, **discard it from
   backfill** — do not file it under today either; an undated post backfilled into today would
   corrupt today's real sample with old content.
3. If a real date resolves: group results by their UTC date. For each date that gets at least one
   post, build a JSON file exactly per Step 4's rules (same schema, same invariants — hour buckets
   still must sum to `total_mentions`), but set:
   - `data_status: "measured_backfill"` (not `"measured"`)
   - `collection.method` including the literal string `"backfill"` so it's traceable
   - `backfill_note`: one sentence stating this is a sparse, timestamp-verified sample, not a full
     day's volume
4. If a date file already exists (e.g. today's own file, or a prior backfill run), do not overwrite
   it — this step runs once. Skip dates that already have a file.
5. Run the Step 4 validator against every new backfill file. The arithmetic invariants apply
   unconditionally regardless of `data_status`.
6. Report which dates were recovered and how many posts landed in each — the gaps are informative,
   not a defect to hide.

---

## Step 1 — Scrape X/Twitter

Run WebSearch for each of the following queries. Collect all visible results.

Search queries (run each separately):
- `$TEL crypto site:twitter.com OR site:x.com`
- `Telcoin site:twitter.com OR site:x.com`
- `"Telcoin Network" site:twitter.com OR site:x.com`
- `@telcoinTAO`

**Record one row in `posts[]` per result.** Aggregate counts are derived from these rows at the
end — never counted separately, so the totals can always be traced back to the records that
produced them.

Per post, capture what is actually visible and set everything else to `null`:
- `text_excerpt` — first ~200 chars
- `author_handle` — if the result exposes it
- `posted_at` + `posted_hour_known` — only if a real timestamp is shown. **Never infer an hour.**
- `metrics` — likes/reposts/replies only if literal numbers are visible. Search snippets almost
  never show these, so expect `null` and set `metrics_tier: "unavailable"`. A guess is not a
  metric; the previous version's "estimated engagement weight" is abolished.
- `sentiment` + `sentiment_confidence` — mark `low` when the snippet is too short to judge
- `narratives[]` — see the taxonomy, below
- `is_question` / `question_text` — see Step 3b

**Sentiment Rules:**
- **Positive**: price optimism, milestone celebration, technical achievement praise, project support, "bullish", buying signals, governance approval
- **Negative**: price frustration, FUD, project criticism, "wen", "dead", "dump", sell signals, governance dissatisfaction
- **Neutral**: factual updates, news shares, technical questions, price observation without opinion, governance observation

**Narrative tags** — read `campaign/analytics/NARRATIVE-TAXONOMY.json` and tag each post with
every narrative it genuinely discusses. Match against each entry's `aliases`.

Do not hardcode the tag list here. The taxonomy file is the single source of truth, and it
carries policy the scraper must respect: entries with `publishable: false` (currently `price`
and `banking`) are tracked for listening but never generate a recommendation to publish.

Every post lands on at least one narrative. If nothing fits, use `other` — never drop a post.
If `other` is climbing across days, the taxonomy needs a new entry.

---

## Step 2 — Scrape Reddit

Run WebSearch:
- `Telcoin site:reddit.com`
- `"$TEL" site:reddit.com`
- `"TEL coin" site:reddit.com`

Target subreddits: r/Telcoin, r/CryptoCurrency, r/CryptoMoonShots, r/altcoin

Record `posts[]` rows exactly as in Step 1. Reddit search results usually DO expose a score and
comment count — capture them as `metrics.score` and `metrics.comments` with
`metrics_tier: "observed"`. This is currently the only platform where real engagement numbers
are reachable without a paid API.

---

## Step 3 — Scrape News

**Changed 2026-08-01** (user feedback, confirmed empirically the same day): the original
outlet-targeted queries (`Telcoin news $YEAR`, `"TEL token" news`, `Telcoin blockchain`) mostly
surface evergreen explainer pages, not dated news — measuring "news" by hitting named outlets
doesn't work well via WebSearch. Replaced with plain broad searches:

- `Telcoin`
- `$TEL` — **use with caution**: this bare ticker collides heavily with TE Connectivity (NYSE:
  TEL), an unrelated stock, and returns mostly noise. Prefer `Telcoin` alone; only add `$TEL` if
  `Telcoin` alone returns too little to assess, and filter out anything obviously about the
  NYSE-listed company.

Collect whatever surfaces — news articles, press releases, blog posts. Exclude results older than
7 days (this is a genuine exclusion, not a formality: reference pages like CoinMarketCap/CoinGecko
price trackers, the official site, and Medium's blog homepage are NOT dated news and don't count
even though they'll appear in every run). Classify sentiment of headline + snippet.

**A `news.article_count: 0` is a legitimate, honest result**, not a failed search — Telcoin does
not generate fresh news every single run, and reporting 0 is correct on days it doesn't.

---

## Step 3b — Question ledger

Standing rule (`campaign/analytics/X-ANALYTICS-GUIDE.md:91`): *if the community is asking a
question we haven't answered, it becomes content that day.* This step is what gives that rule a
memory.

For every captured post that asks something, set `is_question: true` and record `question_text`.
Then fold it into the ledger:

1. Read the most recent prior day's file and carry its `questions[]` forward.
2. For each question found today, canonicalise it to its underlying ask — "wen mainnet", "any
   date for launch?" and "when is mainnet going live" are all one entry, not three.
3. If it matches an existing entry: increment `times_observed`, update `last_seen`. **Do not
   create a duplicate** — recurrence is the whole point.
4. If it is new: add it with `first_seen` = today, `status: "open"`.
5. If a @telcoinTAO post has since answered it, set `status: "answered"`, `answered_at`, and
   `answered_by_post_url`.
6. Mark `out_of_scope` for questions the Association will not answer (Holdings products, price
   predictions, validator names) so they stop resurfacing as content prompts.

A question asked forty times over ninety days is a different object than one asked once. That
distinction is invisible in prose intel files and is the reason this ledger exists.

---

## Step 3c — Share of voice

Three additional WebSearch queries, for relative volume only:
- `XRP remittance`
- `Stellar XLM remittance`
- `Celo mobile payments`

Record the result volume for each alongside Telcoin's in `share_of_voice.raw_counts`.

This is a **weak instrument** and must be labelled `derived`. Search result volume is a proxy for
conversation, not a measurement of it. Report the series **indexed to 100 at its start** so the
dashboard shows *change in relative share* — absolute share against XRP will always read as a
rounding error and tells the reader nothing.

---

## Step 3d — Own-account performance (X native analytics)

`own_account{}` is the pipeline's only `measured`-tier field — real impressions, engagement, and
link clicks for our own posts, as opposed to the `observed` samples in the rest of this file.

- **No browser automation against a stored login.** X's ToS bans automated access to the
  analytics dashboard, and this manages a real production account (@telcoinTAO) — an account
  suspension is not a risk worth trading for one metric. (Researched and confirmed 2026-08-02:
  there is also no technical bridge from a cloud-hosted session to a locally-authenticated Chrome
  profile — "Claude in Chrome" is tied to the machine it runs on.)

**Standing path — decided 2026-08-10: manual CSV export, by explicit choice.** The X API route
(`scripts/x_api_fetch.py` + `scripts/x_oauth_setup.py`) was built and works, but costs a small
per-read fee (roughly $0.15-0.45/month at this posting volume — X removed its free developer
tier in Feb 2026) and requires a one-time OAuth connection step. Weighed against that: periodic
CSV export from analytics.x.com is genuinely $0 in API cost and needs no developer app or OAuth
setup at all — just the X Premium subscription the account already needs for dashboard access
either way. The user chose this as the one acceptable manual step in the whole pipeline. Do not
"fix" this by pushing the OAuth path again without being asked; the tradeoff was made knowingly.

To refresh measured own-account performance:
1. Log into X as @telcoinTAO (switch accounts first if using delegated/team access).
2. On analytics.x.com, export **either or both**:
   - **Account Overview** (by day) — day totals → `campaign/analytics/account-overview/daily.json`
     and attaches `own_account.daily` onto existing sentiment day files. Also refreshes
     `campaign/analytics/PERFORMANCE-LOG.md` when the agent recalculates after import.
   - **Posts / Tweet activity** (Export by Tweet) — per-post rows with permalinks → fills
     `own_account.posts[]` on matching day files (and creates `data_status: "partial"` files
     for dates with no community host file yet).
3. Run:
   ```bash
   python3 scripts/x-analytics-import.py path/to/exported.csv
   ```
   The importer auto-detects which export type it received.
Re-run whenever a fresh export is pulled — safe to re-run, later exports overwrite measured
fields with `as_of` bumped to the import time. The export covers roughly the trailing 90 days, so an
occasional pull (not necessarily daily) keeps the record current; a gap between exports just means
own-account data lags, which is honestly a lesser problem than the community layer's day-to-day
gaps this file already tolerates.

**`x_api_fetch.py` / `x_oauth_setup.py` remain in the repo as a ready, tested-but-unused upgrade
path** — if the calculus changes (posting volume grows, or the manual export becomes a burden
after all), connecting them is a one-time step, not a rebuild.

Either path fills `own_account{}` on every matching day-file (matching narratives against that
day's own posts by URL where the community scraper already recorded the same tweet), and creates
a new `data_status: "partial"` file for any date with data but no host file yet — real, dated
performance data with no community layer, never conflated with a full `measured` day.

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

Set `data_status: "measured"` and fill `collection{}` with the method, every query actually run,
and the raw result count. That block is what makes each number auditable back to its source.

Save output to `campaign/analytics/sentiment/$TODAY.json`, then **validate before continuing**:

```bash
python3 - campaign/analytics/sentiment/$TODAY.json <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
tax={n["id"] for n in json.load(open("campaign/analytics/NARRATIVE-TAXONOMY.json"))["narratives"]}
c=d["composite"]
hs=sum(int(v) for v in c["hour_distribution"].values())
assert d["schema_version"]==2, "wrong schema version"
assert hs==c["total_mentions"], f"hour buckets {hs} != total_mentions {c['total_mentions']}"
assert set(d.get("narratives",{})) <= tax, f"unknown narrative: {set(d['narratives'])-tax}"
assert c["n_classified"]>0 or c["total_mentions"]==0, "sentiment without a sample size"
for p in d.get("posts",[]):
    assert p["narratives"], f"untagged post {p['id']}"
print("OK", d["date"], c["total_mentions"], "mentions,", len(d.get("posts",[])), "posts")
PY
```

If validation fails, fix the data — do not relax the check. The hour-bucket invariant is
specifically what would have caught the fabricated data now quarantined in `_seed-synthetic/`.

---

## Step 5 — Regenerate the Dashboard

**Canonical tool: `python3 scripts/build-dashboard.py`.** This reads every source file under
`campaign/analytics/` fresh (community sentiment, account-overview, price history, the Grok
spot-check, web-mentions, YouTube, Restream if live) and writes the complete
`campaign/analytics/sentiment/dashboard.html`. Run it whenever any source file changes — it is
the single place that compiles all of them, added 2026-08-23 when the dashboard grew from one
series to seven. **Never hand-edit dashboard.html's data blocks or generated sections** — re-run
the script instead, so the file always matches its sources exactly. Extend `gather()`/`build_html()`
in that script when a new source is added, rather than writing a one-off regeneration by hand.

The script already encodes the rules that used to live only here:
- Skips any sentiment file whose `data_status` is `"seed_synthetic"` or `"partial"` (fabricated
  or incomplete — never plotted). Only `"measured"` community days feed the narrative ledger,
  open questions, and the day-count gates.
- Community trend panels (sentiment over time, narrative momentum) stay gated until 14 measured
  days exist; narrative ledger and open questions unlock at day 1 and render live below that.
  Gates read `community_days` directly off however many measured sentiment files actually exist —
  no manual counting.
- `account-overview/daily.json` (own-account X performance) plots independently of the community
  gate, whenever it exists.
- Price/market context is explicitly `publishable: false` — the dashboard marks it "listen-only"
  and pairs it against sentiment, never presents it as something to post about.
- The Grok spot-check's own `bullish_score` is shown next to this pipeline's `sentiment_score`
  formula, never blended into one number — see `campaign/analytics/community-grok/README.md`.
- Restream renders as a "not connected" pending panel until real files exist under
  `campaign/analytics/restream/` or `streams/`.

After running the script, validate the output before publishing (a headless-browser render check
catches embedded-JSON and layout errors a text diff won't):
```bash
python3 -c "
import re, json
html = open('campaign/analytics/sentiment/dashboard.html').read()
for name in ['ACCOUNT_RAW', 'RAW', 'PRICE_RECENT']:
    m = re.search(rf'const {name} = (\[.*?\]);\n', html, re.DOTALL)
    assert m, f'{name} not found'
    json.loads(m.group(1))  # raises if malformed
print('embedded JSON blocks valid')
"
```

Then call the Artifact tool to update the artifact at ARTIFACT_URL (see top of this file), passing
the generated `dashboard.html` as `file_path` and the URL as `url` so it updates in place rather
than minting a new one. Title "TEL Social Intelligence", favicon "📊". If the tool reports the live
version wasn't yet viewed, read it first (its content will be an older snapshot — this pipeline's
sources are strictly additive, so there is nothing to lose by superseding it) and then republish.

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
