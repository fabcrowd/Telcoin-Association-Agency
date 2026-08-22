# Web Mentions Tracker — General Search-Engine Presence for $TEL / Telcoin

**Cadence: weekly.** This is a coarse, weak-instrument metric — daily noise would swamp any real
signal, and running it more often adds no value while adding token cost for nothing.

Tracks how much general web presence "Telcoin" / "$TEL" has, independent of the social-platform
community pipeline (`scripts/sentiment-scraper.md`, which is X/Reddit/news specific). This answers
a different question: not "what is the community saying," but "how visible is Telcoin across the
open web generally."

## Why this is WebSearch-based, not a raw scraper

A raw HTTP scraper against a search engine's results page was considered and rejected. Tested
2026-08-22: DuckDuckGo's HTML endpoint (`html.duckduckgo.com`) resets the TLS connection outright —
blocked. Bing's results page (`bing.com/search`) *is* technically reachable and returns real
content, but scraping either directly means automating access to a search engine outside its
official API, the same category of ToS risk this pipeline already rejected for X's analytics
dashboard (`scripts/sentiment-scraper.md` Step 3d). Being reachable once in a test isn't the same
as being sanctioned, and a fragile, ToS-questionable scraper is worse than the tool this entire
pipeline already trusts for exactly this job. WebSearch is Anthropic's own sanctioned search
capability, used everywhere else in this pipeline (community mentions, news, share-of-voice) for
the same reason — it's the consistent choice, not a new exception.

## Step 1 — Run the searches

Three broad WebSearch queries, **no site: restriction** (this is the point — general web presence,
not social-platform-specific):
- `Telcoin`
- `$TEL`
- `"Telcoin Network"`

For each query, record:
- `results_returned` — count of distinct results the tool actually returned. This is a **weak,
  bounded proxy**, not a true index size — WebSearch (like Google/Bing's own UI) does not expose a
  real total-match count, only a page of results. Never present this as "X million mentions."
- `distinct_domains` — count of distinct root domains among the returned results, a rough breadth-
  of-coverage signal (is this the same 3 sites every week, or genuinely spreading).
- `notable_new_urls` — any URL that did not appear in the prior week's file, listed for a human to
  glance at. Not a used metric, just a "what's new" pointer.

## Step 2 — Build and save

Store one row per ISO week in a single consolidated series file (matching the pattern in
`campaign/analytics/account-overview/` and `campaign/analytics/market/` — a coarse weekly metric
doesn't need one-file-per-day the way daily sentiment does).

```json
{
  "schema_version": 1,
  "tier": "derived",
  "method_note": "WebSearch result-volume proxy, weak instrument - see scripts/web-mentions-scraper.md for why this is not a raw scraper and not a true index-size measurement.",
  "queries": ["Telcoin", "$TEL", "\"Telcoin Network\""],
  "weeks": [
    {
      "week_start": "YYYY-MM-DD",
      "week_end": "YYYY-MM-DD",
      "per_query": {
        "Telcoin": { "results_returned": 0, "distinct_domains": 0 },
        "$TEL": { "results_returned": 0, "distinct_domains": 0 },
        "Telcoin Network": { "results_returned": 0, "distinct_domains": 0 }
      },
      "total_results_returned": 0,
      "indexed_to_first_week": 100.0,
      "notable_new_urls": []
    }
  ]
}
```

`indexed_to_first_week` — same convention as `share_of_voice` in the sentiment schema: report
`total_results_returned` indexed to 100 at the series' first week, so the file shows *change over
time*, not an absolute count that reads as noise. Compute as
`100 * this_week_total / first_week_total`.

Save to `campaign/analytics/web-mentions/weekly.json`. If the file already exists, append the new
week (do not overwrite prior weeks) unless re-running the same week, which overwrites just that row.

**Validate before writing:**
```bash
python3 - campaign/analytics/web-mentions/weekly.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d["schema_version"] == 1
weeks = d["weeks"]
assert weeks, "no weeks recorded"
first_total = weeks[0]["total_results_returned"]
for w in weeks:
    per_q = w["per_query"]
    computed_total = sum(v["results_returned"] for v in per_q.values())
    assert computed_total == w["total_results_returned"], (
        f"{w['week_start']}: per-query sum {computed_total} != total_results_returned {w['total_results_returned']}"
    )
    if first_total:
        expected_idx = round(100 * w["total_results_returned"] / first_total, 2)
        assert abs(w["indexed_to_first_week"] - expected_idx) < 0.01, (
            f"{w['week_start']}: indexed value doesn't match its own formula"
        )
print(f"OK - {len(weeks)} week(s), most recent {weeks[-1]['week_start']}")
PY
```

## Step 3 — Report

- Total results this week, per query
- Indexed value vs. the series' first week (up/down/flat)
- Distinct domains this week
- Any notable new URLs

## Step 4 — Commit and push

```bash
git add campaign/analytics/web-mentions/weekly.json
git commit -m "Web mentions tracker: week of <week_start>"
git push origin claude/campaign-iLgt5
```

---

**Not wired into `dashboard.html`** — that file was substantially rewritten by a separate
concurrent session (2026-08-22); wiring this series in is a deliberate next step, not assumed here.

**Do not disaggregate this into daily numbers.** The source data's real grain is weekly (WebSearch
result pages don't carry meaningful daily granularity); inventing daily numbers from a weekly
snapshot would repeat the exact mistake `tasks/lessons.md` Lesson 11 quarantined data for.
