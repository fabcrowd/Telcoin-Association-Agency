#!/usr/bin/env python3
"""
Import an analytics.x.com "Tweet activity" CSV export into own_account{} on each
matching day's campaign/analytics/sentiment/YYYY-MM-DD.json file.

Why this exists: the sentiment pipeline's `measured` tier (real impressions,
engagement, link clicks - the platform's own analytics for an account we control)
has no automated path in. Browser automation against a stored login is a real
account-suspension risk (X's ToS bans automated dashboard access) and there's no
way for a cloud session to drive a locally-authenticated Chrome profile. The CSV
export is the sanctioned path: the user logs into analytics.x.com themselves,
downloads the "Tweet activity" export (X Premium required for dashboard access;
covers roughly the trailing 90 days), and this script does the rest.

Usage:
    python3 scripts/x-analytics-import.py path/to/tweet_activity_export.csv

For each row's date:
- If campaign/analytics/sentiment/YYYY-MM-DD.json already exists, its own_account{}
  is filled in (narratives are matched against that day's own posts[] by URL when
  the community scraper already recorded the same tweet).
- If no file exists for that date (common - the daily scraper only started
  2026-08-01, but this CSV can reach back ~90 days), a new file is created with
  data_status: "partial" - real, dated performance data with no community layer,
  never conflated with a full "measured" day. The dashboard excludes "partial"
  files from its trend series and counts them only in the collected-days tally,
  per scripts/sentiment-scraper.md Step 5.
"""
import csv
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

SENTIMENT_DIR = Path("campaign/analytics/sentiment")
TAXONOMY_PATH = Path("campaign/analytics/NARRATIVE-TAXONOMY.json")


def find_col(fieldnames, *candidates):
    lower = {f.lower().strip(): f for f in fieldnames}
    for cand in candidates:
        for lf, orig in lower.items():
            if cand in lf:
                return orig
    return None


def parse_number(v):
    if v is None or v == "":
        return None
    v = v.replace(",", "").strip().rstrip("%")
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return None


def parse_time(raw):
    raw = raw.strip()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M %z", "%Y-%m-%d %H:%M", "%m/%d/%y %H:%M"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def empty_composite():
    return {
        "total_mentions": 0,
        "n_classified": 0,
        "sentiment_score": 0.0,
        "unique_authors": 0,
        "top_narrative": None,
        "hour_distribution": {str(h): 0 for h in range(24)} | {"unknown": 0},
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 x-analytics-import.py <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("CSV had no rows - nothing to import.")
        return

    fieldnames = rows[0].keys()
    col_time = find_col(fieldnames, "time", "date")
    col_url = find_col(fieldnames, "permalink", "tweet permalink", "url")
    col_text = find_col(fieldnames, "tweet text", "text")
    col_impr = find_col(fieldnames, "impressions")
    col_eng = find_col(fieldnames, "engagements")
    col_rate = find_col(fieldnames, "engagement rate")
    col_linkclicks = find_col(fieldnames, "url clicks", "link clicks")
    col_profileclicks = find_col(fieldnames, "user profile clicks", "profile visits", "profile clicks")

    missing = [n for n, c in [("time", col_time), ("permalink/url", col_url)] if c is None]
    if missing:
        print(f"Could not find required column(s): {missing}. Columns present: {list(fieldnames)}",
              file=sys.stderr)
        sys.exit(1)

    by_day = {}
    skipped_rows = 0
    for row in rows:
        dt = parse_time(row.get(col_time, ""))
        if dt is None:
            skipped_rows += 1
            continue
        date_key = dt.astimezone(timezone.utc).date().isoformat()
        by_day.setdefault(date_key, []).append({
            "url": row.get(col_url),
            "published_at": dt.astimezone(timezone.utc).isoformat(),
            "narratives": [],
            "layer": None,
            "impressions": parse_number(row.get(col_impr)) if col_impr else None,
            "engagements": parse_number(row.get(col_eng)) if col_eng else None,
            "engagement_rate": parse_number(row.get(col_rate)) if col_rate else None,
            "link_clicks": parse_number(row.get(col_linkclicks)) if col_linkclicks else None,
            "profile_visits": parse_number(row.get(col_profileclicks)) if col_profileclicks else None,
            "_text_excerpt": (row.get(col_text) or "")[:200] if col_text else None,
        })

    updated, created, empty_narratives_dict = 0, 0, None
    if TAXONOMY_PATH.exists():
        empty_narratives_dict = {}

    for date_key, posts in sorted(by_day.items()):
        f = SENTIMENT_DIR / f"{date_key}.json"
        if f.exists():
            data = json.loads(f.read_text())
            existing_by_url = {p.get("url"): p for p in data.get("posts", []) if p.get("is_own_post")}
            for post in posts:
                match = existing_by_url.get(post["url"])
                if match:
                    post["narratives"] = match.get("narratives", [])
                del post["_text_excerpt"]
            data["own_account"] = {
                "followers": data.get("own_account", {}).get("followers"),
                "as_of": datetime.now(timezone.utc).isoformat(),
                "source": "x_native_analytics_csv",
                "tier": "measured",
                "posts": posts,
            }
            f.write_text(json.dumps(data, indent=2) + "\n")
            updated += 1
            print(f"Updated {f} with {len(posts)} own-account post(s)")
        else:
            for post in posts:
                del post["_text_excerpt"]
            data = {
                "schema_version": 2,
                "date": date_key,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "data_status": "partial",
                "collection": {
                    "method": "x_native_analytics_csv_import",
                    "queries_run": [],
                    "results_seen": 0,
                    "coverage": "own_account_only",
                    "notes": "No community scraper ran this day - this file carries only "
                             "real own-account performance data recovered from a later CSV "
                             "export. data_status is 'partial' precisely because the "
                             "community layer (sentiment, narratives, mentions) is genuinely "
                             "absent, not zeroed - never conflate the two.",
                },
                "posts": [],
                "questions": [],
                "narratives": empty_narratives_dict or {},
                "own_account": {
                    "followers": None,
                    "as_of": datetime.now(timezone.utc).isoformat(),
                    "source": "x_native_analytics_csv",
                    "tier": "measured",
                    "posts": posts,
                },
                "share_of_voice": {},
                "composite": empty_composite(),
            }
            f.write_text(json.dumps(data, indent=2) + "\n")
            created += 1
            print(f"Created {f} (partial - own-account performance only, {len(posts)} post(s))")

    if skipped_rows:
        print(f"\n{skipped_rows} row(s) had an unparseable time column and were skipped.",
              file=sys.stderr)
    print(f"\n{updated} day-file(s) updated, {created} new partial day-file(s) created.")


if __name__ == "__main__":
    main()
