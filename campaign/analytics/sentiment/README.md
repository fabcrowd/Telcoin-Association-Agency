# TEL Sentiment Data Store — schema v2

One file per UTC day: `YYYY-MM-DD.json`. The dashboard reads all files to render history.

**This store is the only irreplaceable asset in the pipeline.** No social platform returns
metric *history* — APIs and search both return current values only. A day not snapshotted is
gone permanently. Never delete a measured file.

Quarantined pre-v2 data lives in `_seed-synthetic/` and must never be cited. See its
`PROVENANCE.md`.

---

## The two rules that govern every field

**1. `null` means unknown. It is never coerced to `0`.**
A missing timestamp, an unavailable like count, an unknown follower count — all `null`. Zero
means "we looked and there were none." Conflating the two is what produced the quarantined data.

**2. Every quantity carries a tier.**

| Tier | Meaning |
|---|---|
| `measured` | Platform's own analytics for an account we control |
| `observed` | Count literally visible on a third-party post we saw |
| `derived` | Computed from the above by a stated formula |
| `unavailable` | Known gap, rendered as a gap |

The dashboard loader refuses to plot any file whose `data_status` is not `measured`.

---

## Schema

```json
{
  "schema_version": 2,
  "date": "YYYY-MM-DD",
  "scraped_at": "ISO-8601 UTC",
  "data_status": "measured | partial | seed_synthetic",

  "collection": {
    "method": "websearch",
    "queries_run": ["..."],
    "results_seen": 0,
    "coverage": "sample",
    "notes": "Anything that would change how a reader interprets the counts."
  },

  "posts": [
    {
      "id": "platform:native_id_or_hash",
      "platform": "twitter | reddit | news",
      "url": null,
      "author_handle": null,
      "author_followers": null,
      "text_excerpt": "first ~200 chars",
      "posted_at": null,
      "posted_hour_known": false,
      "metrics": {
        "likes": null, "reposts": null, "replies": null,
        "score": null, "comments": null, "impressions": null
      },
      "metrics_tier": "observed | unavailable",
      "sentiment": "positive | neutral | negative",
      "sentiment_confidence": "high | low",
      "narratives": ["mainnet"],
      "is_question": false,
      "question_text": null,
      "is_own_post": false
    }
  ],

  "questions": [
    {
      "id": "slugified-canonical-form",
      "text_canonical": "When is mainnet launching?",
      "first_seen": "YYYY-MM-DD",
      "last_seen": "YYYY-MM-DD",
      "times_observed": 1,
      "narratives": ["mainnet"],
      "status": "open | answered | out_of_scope",
      "answered_by_post_url": null,
      "answered_at": null
    }
  ],

  "narratives": {
    "mainnet": {
      "community_mentions": 0,
      "sentiment": { "positive": 0, "neutral": 0, "negative": 0 },
      "unique_authors": 0,
      "by_platform": { "twitter": 0, "reddit": 0, "news": 0 },
      "tier": "observed"
    }
  },

  "own_account": {
    "followers": null,
    "as_of": null,
    "source": "x_native_analytics",
    "tier": "measured",
    "posts": [
      {
        "url": "...", "published_at": "...",
        "narratives": ["governance"], "layer": "governance",
        "impressions": 0, "engagements": 0, "engagement_rate": 0.0,
        "link_clicks": null, "profile_visits": null
      }
    ]
  },

  "share_of_voice": {
    "tier": "derived",
    "method": "search result volume proxy, indexed to series start = 100",
    "raw_counts": { "telcoin": 0, "xrp": 0, "stellar": 0, "celo": 0 }
  },

  "composite": {
    "total_mentions": 0,
    "n_classified": 0,
    "sentiment_score": 0.0,
    "unique_authors": 0,
    "top_narrative": null,
    "hour_distribution": { "0": 0, "23": 0, "unknown": 0 }
  }
}
```

---

## Field notes

**`composite.sentiment_score`** — `positive / n_classified`, clamped 0.01–0.99. **Never report it
without `n_classified`.** A 0.70 from 7 posts and a 0.70 from 200 posts are different facts.

**`composite.unique_authors`** — distinct `author_handle` values. For a governance audience this
may matter more than sentiment: it answers whether a reading reflects a broad community or six
accounts. `null` when handles were not capturable.

**`composite.top_narrative`** — set only when the leader clears second place by more than
sampling noise. Otherwise `null`. A coin-flip leader reported as fact is how a dashboard starts
lying.

**`composite.hour_distribution`** — includes a required `"unknown"` bucket. All buckets including
`unknown` must sum to exactly `total_mentions`; if they do not, the file is invalid and must not
be written. **Never estimate an hour.** Expect `unknown` to dominate until a source with real
timestamps is wired in.

**`activity_score`** — removed in v2. It was normalized against an invented historical max of
120, making it unitless. Report raw counts.

**`topic_scores`** — removed in v2, replaced by `narratives{}`. The old formula blended platform
weights into one float, which destroyed auditability, and included an engagement term that always
evaluated to zero because engagement was never captured.

**`narratives`** — keys must exist in `campaign/analytics/NARRATIVE-TAXONOMY.json`. A post may
carry several. Every post lands on at least one; use `other` rather than dropping it, and treat a
rising `other` count as a signal the taxonomy needs extending.

**`own_account`** — the `measured` tier, sourced from the analytics.x.com CSV export. This is the
only place "impressions" and "reach" are valid words. Community data never uses them.

**`questions`** — the ledger. Carried forward day to day: increment `times_observed` and update
`last_seen` when a question recurs rather than creating a duplicate. Recurrence over time is the
dimension prose intel files cannot carry — a question asked 40 times across 90 days is a
different object than one asked once. Derived from this: **answer latency**, the median days from
`first_seen` to `answered_at` per narrative.

---

## Validating a file before writing it

```bash
python3 - "$FILE" <<'PY'
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
print("OK", d["date"], c["total_mentions"], "mentions,", len(d.get("posts",[])), "posts captured")
PY
```
