# Quarantined — synthetic seed data. Do not cite.

The 14 JSON files in this directory (2026-07-17 through 2026-07-30) were **generated**, not
collected. They were written on 2026-07-30 as a schema and dashboard demonstration while the
sentiment pipeline was being built. No social scrape ever produced them.

They are quarantined rather than deleted so the record is auditable. Nothing in this directory
may be cited, plotted, reported to the client, or used to fit a baseline.

## Forensic proof

Three independent signatures confirm generation. All are reproducible from the files themselves.

**1. Every file disagrees with its own post count.** `hour_distribution` is defined as a count
of posts by UTC hour, so it must sum to `total_mentions`. It never does — it exceeds it by
24-51%, averaging 40%:

| date | total_mentions | hour_distribution sum | ratio |
|---|---|---|---|
| 2026-07-17 | 71 | 101 | 1.42 |
| 2026-07-20 | 28 | 38 | 1.36 |
| 2026-07-23 | 108 | 145 | 1.34 |
| 2026-07-26 | 37 | 46 | 1.24 |
| 2026-07-29 | 98 | 137 | 1.40 |
| 2026-07-30 | 104 | 140 | 1.35 |

A file cannot be both a census of posts by hour and disagree with its own count of posts. This
alone rules out salvaging the data as an approximation.

**2. Sentiment tracks volume at r = 0.9662.** Across all 14 days, `total_mentions` and
`sentiment_score` correlate at 0.966. Real sentiment does not follow conversation volume that
tightly; a busy day is not reliably a happy day. This is the signature of both series being
drawn from one underlying curve.

**3. All 14 files carry `scraped_at` = `T09:00:00Z` exactly**, and all were added in a single
commit (`b8bd64d`). Fourteen independent daily runs do not land on the same second.

Additionally, `notable_posts[]` and `articles[]` are `[]` in all 14 files — no post was ever
captured, so the aggregate counts have no underlying records to have been derived from.

## Root cause

`scripts/sentiment-scraper.md:104` instructed: *"If hour not visible for a post, distribute
evenly."* Search results rarely expose post timestamps, so this rule manufactured the hour grid
on nearly every run. It has been removed and replaced with an explicit `unknown` bucket.

## Reproduce

```bash
python3 -c "
import json,glob,statistics
fs=sorted(glob.glob('campaign/analytics/sentiment/_seed-synthetic/*.json'))
ms=[];ss=[]
for f in fs:
    c=json.load(open(f))['composite']
    hs=sum(int(v) for v in c['hour_distribution'].values())
    print(c['total_mentions'], hs, round(hs/c['total_mentions'],2))
    ms.append(c['total_mentions']); ss.append(c['sentiment_score'])
n=len(ms); mm=statistics.mean(ms); sm=statistics.mean(ss)
r=(sum((a-mm)*(b-sm) for a,b in zip(ms,ss))/n)/(statistics.pstdev(ms)*statistics.pstdev(ss))
print('corr:', round(r,4))
"
```

## Why this matters

The agency enforces a rule on every piece of client content: *"The Telcoin Association does not
chase engagement. It earns credibility."* That standard applies to the agency's own deliverables
first. A council member citing "community sentiment 0.67 on governance" from a fabricated file,
or a comms team escalating on an invented negative-sentiment spike, would cost more than any
number of blank days on a chart.

Real collection starts fresh. Schema v2 adds a `data_status` field, and the dashboard loader
refuses to plot anything not marked `measured`.
