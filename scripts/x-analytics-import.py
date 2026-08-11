#!/usr/bin/env python3
"""
Import an analytics.x.com CSV export into the campaign analytics store.

Accepts two export types from analytics.x.com:

1. Tweet activity / Export by Tweet (per-post rows with permalink)
   -> fills own_account.posts[] on each matching day's
      campaign/analytics/sentiment/YYYY-MM-DD.json file
   -> creates data_status: "partial" files for dates with no host file yet

2. Account Overview / Export by day (daily account totals, no permalink)
   -> writes campaign/analytics/account-overview/daily.json (measured day series)
   -> attaches own_account.daily rollup onto existing sentiment day files
   -> does NOT invent per-post rows (those require a Tweet-activity export)

Why this exists: the sentiment pipeline's `measured` tier (real impressions,
engagement, link clicks - the platform's own analytics for an account we control)
has no safe automated path in. Browser automation against a stored login is a real
account-suspension risk (X's ToS bans automated dashboard access). The CSV export
is the sanctioned path.

Usage:
    python3 scripts/x-analytics-import.py path/to/export.csv
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SENTIMENT_DIR = Path("campaign/analytics/sentiment")
ACCOUNT_OVERVIEW_DIR = Path("campaign/analytics/account-overview")
TAXONOMY_PATH = Path("campaign/analytics/NARRATIVE-TAXONOMY.json")


def find_col(fieldnames: list[str] | Any, *candidates: str) -> str | None:
    """Return the original column name matching a candidate.

    Exact (case-insensitive) match wins first, then substring match. Preferring
    exact avoids ``posts`` incorrectly binding to ``Reposts``.
    """
    lower = {f.lower().strip(): f for f in fieldnames}
    for cand in candidates:
        key = cand.lower().strip()
        if key in lower:
            return lower[key]
    for cand in candidates:
        key = cand.lower().strip()
        for lf, orig in lower.items():
            if key in lf:
                return orig
    return None


def parse_number(v: str | None) -> int | float | None:
    """Parse a metric cell; empty -> None; never coerce missing to 0."""
    if v is None or v == "":
        return None
    v = v.replace(",", "").strip().rstrip("%")
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return None


def parse_time(raw: str) -> datetime | None:
    """Parse Tweet-activity timestamps and Account Overview day labels."""
    raw = raw.strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in (
        "%Y-%m-%d %H:%M %z",
        "%Y-%m-%d %H:%M",
        "%m/%d/%y %H:%M",
        "%a %b %d %Y",  # Account Overview: "Tue Jul 14 2026"
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def empty_composite() -> dict[str, Any]:
    """Schema-v2 empty composite for partial day files."""
    return {
        "total_mentions": 0,
        "n_classified": 0,
        "sentiment_score": 0.0,
        "unique_authors": 0,
        "top_narrative": None,
        "hour_distribution": {str(h): 0 for h in range(24)} | {"unknown": 0},
    }


def detect_format(fieldnames: list[str] | Any) -> str:
    """Return 'tweet_activity' or 'account_overview' based on columns present."""
    col_url = find_col(fieldnames, "permalink", "tweet permalink", "url")
    col_date = find_col(fieldnames, "date", "time")
    col_impr = find_col(fieldnames, "impressions")
    # Account Overview has Date + Impressions and no permalink/url column.
    if col_url is None and col_date is not None and col_impr is not None:
        return "account_overview"
    if col_url is not None and col_date is not None:
        return "tweet_activity"
    return "unknown"


def import_tweet_activity(rows: list[dict[str, str]], fieldnames: list[str] | Any) -> None:
    """Import per-post Tweet activity export into own_account.posts[]."""
    col_time = find_col(fieldnames, "time", "date")
    col_url = find_col(fieldnames, "permalink", "tweet permalink", "url")
    col_text = find_col(fieldnames, "tweet text", "text")
    col_impr = find_col(fieldnames, "impressions")
    col_eng = find_col(fieldnames, "engagements")
    col_rate = find_col(fieldnames, "engagement rate")
    col_linkclicks = find_col(fieldnames, "url clicks", "link clicks")
    col_profileclicks = find_col(
        fieldnames, "user profile clicks", "profile visits", "profile clicks"
    )

    missing = [n for n, c in [("time", col_time), ("permalink/url", col_url)] if c is None]
    if missing:
        print(
            f"Could not find required column(s): {missing}. Columns present: {list(fieldnames)}",
            file=sys.stderr,
        )
        sys.exit(1)

    by_day: dict[str, list[dict[str, Any]]] = {}
    skipped_rows = 0
    for row in rows:
        dt = parse_time(row.get(col_time or "", ""))
        if dt is None:
            skipped_rows += 1
            continue
        date_key = dt.astimezone(timezone.utc).date().isoformat()
        by_day.setdefault(date_key, []).append(
            {
                "url": row.get(col_url or ""),
                "published_at": dt.astimezone(timezone.utc).isoformat(),
                "narratives": [],
                "layer": None,
                "impressions": parse_number(row.get(col_impr)) if col_impr else None,
                "engagements": parse_number(row.get(col_eng)) if col_eng else None,
                "engagement_rate": parse_number(row.get(col_rate)) if col_rate else None,
                "link_clicks": parse_number(row.get(col_linkclicks)) if col_linkclicks else None,
                "profile_visits": (
                    parse_number(row.get(col_profileclicks)) if col_profileclicks else None
                ),
                "_text_excerpt": (row.get(col_text) or "")[:200] if col_text else None,
            }
        )

    updated, created = 0, 0
    empty_narratives_dict: dict[str, Any] | None = {} if TAXONOMY_PATH.exists() else None

    for date_key, posts in sorted(by_day.items()):
        f = SENTIMENT_DIR / f"{date_key}.json"
        if f.exists():
            data = json.loads(f.read_text())
            existing_by_url = {
                p.get("url"): p for p in data.get("posts", []) if p.get("is_own_post")
            }
            for post in posts:
                match = existing_by_url.get(post["url"])
                if match:
                    post["narratives"] = match.get("narratives", [])
                del post["_text_excerpt"]
            prev = data.get("own_account", {}) or {}
            data["own_account"] = {
                "followers": prev.get("followers"),
                "as_of": datetime.now(timezone.utc).isoformat(),
                "source": "x_native_analytics_csv",
                "tier": "measured",
                "daily": prev.get("daily"),
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
                    "notes": (
                        "No community scraper ran this day - this file carries only "
                        "real own-account performance data recovered from a later CSV "
                        "export. data_status is 'partial' precisely because the "
                        "community layer (sentiment, narratives, mentions) is genuinely "
                        "absent, not zeroed - never conflate the two."
                    ),
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
            SENTIMENT_DIR.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(data, indent=2) + "\n")
            created += 1
            print(f"Created {f} (partial - own-account performance only, {len(posts)} post(s))")

    if skipped_rows:
        print(
            f"\n{skipped_rows} row(s) had an unparseable time column and were skipped.",
            file=sys.stderr,
        )
    print(f"\n{updated} day-file(s) updated, {created} new partial day-file(s) created.")


def import_account_overview(rows: list[dict[str, str]], fieldnames: list[str] | Any) -> None:
    """Import Account Overview (by-day) export into the measured account-overview store."""
    col_date = find_col(fieldnames, "date")
    col_impr = find_col(fieldnames, "impressions")
    col_likes = find_col(fieldnames, "likes")
    col_eng = find_col(fieldnames, "engagements")
    col_bookmarks = find_col(fieldnames, "bookmarks")
    col_shares = find_col(fieldnames, "share")
    col_follows = find_col(fieldnames, "new follows", "follows")
    col_replies = find_col(fieldnames, "replies")
    col_reposts = find_col(fieldnames, "reposts")
    col_visits = find_col(fieldnames, "profile visits", "profile clicks")
    col_posts = find_col(fieldnames, "posts")
    col_video = find_col(fieldnames, "video views")
    col_media = find_col(fieldnames, "media views")

    if col_date is None or col_impr is None:
        print(
            f"Account Overview export missing Date/Impressions. Columns: {list(fieldnames)}",
            file=sys.stderr,
        )
        sys.exit(1)

    days: list[dict[str, Any]] = []
    skipped_rows = 0
    for row in rows:
        dt = parse_time(row.get(col_date, ""))
        if dt is None:
            skipped_rows += 1
            continue
        date_key = dt.astimezone(timezone.utc).date().isoformat()
        impressions = parse_number(row.get(col_impr)) if col_impr else None
        engagements = parse_number(row.get(col_eng)) if col_eng else None
        eng_rate = None
        if (
            isinstance(impressions, (int, float))
            and isinstance(engagements, (int, float))
            and impressions > 0
        ):
            eng_rate = round(float(engagements) / float(impressions), 6)

        days.append(
            {
                "date": date_key,
                "impressions": impressions,
                "likes": parse_number(row.get(col_likes)) if col_likes else None,
                "engagements": engagements,
                "engagement_rate": eng_rate,
                "bookmarks": parse_number(row.get(col_bookmarks)) if col_bookmarks else None,
                "shares": parse_number(row.get(col_shares)) if col_shares else None,
                "new_follows": parse_number(row.get(col_follows)) if col_follows else None,
                "replies": parse_number(row.get(col_replies)) if col_replies else None,
                "reposts": parse_number(row.get(col_reposts)) if col_reposts else None,
                "profile_visits": parse_number(row.get(col_visits)) if col_visits else None,
                "posts_published": parse_number(row.get(col_posts)) if col_posts else None,
                "video_views": parse_number(row.get(col_video)) if col_video else None,
                "media_views": parse_number(row.get(col_media)) if col_media else None,
                "tier": "measured",
                "source": "x_native_analytics_account_overview_csv",
            }
        )

    days.sort(key=lambda d: d["date"])
    as_of = datetime.now(timezone.utc).isoformat()
    payload = {
        "schema_version": 1,
        "account": "@telcoinTAO",
        "export_type": "account_overview",
        "as_of": as_of,
        "period_start": days[0]["date"] if days else None,
        "period_end": days[-1]["date"] if days else None,
        "n_days": len(days),
        "totals": {
            "impressions": sum(int(d["impressions"] or 0) for d in days),
            "engagements": sum(int(d["engagements"] or 0) for d in days),
            "likes": sum(int(d["likes"] or 0) for d in days),
            "new_follows": sum(int(d["new_follows"] or 0) for d in days),
            "profile_visits": sum(int(d["profile_visits"] or 0) for d in days),
            "posts_published": sum(int(d["posts_published"] or 0) for d in days),
            "replies": sum(int(d["replies"] or 0) for d in days),
            "reposts": sum(int(d["reposts"] or 0) for d in days),
        },
        "days": days,
        "notes": (
            "Day-level account totals from analytics.x.com Account Overview export. "
            "This is measured-tier data for @telcoinTAO. It does NOT include per-post "
            "permalinks — for own_account.posts[] use a Tweet-activity (Export by Tweet) CSV."
        ),
    }

    ACCOUNT_OVERVIEW_DIR.mkdir(parents=True, exist_ok=True)
    out = ACCOUNT_OVERVIEW_DIR / "daily.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {out} ({len(days)} measured day(s), {payload['period_start']} → {payload['period_end']})")

    # Attach daily rollup onto any existing sentiment day files (do not create partials —
    # Account Overview alone must not inflate the community "days collected" tally).
    attached = 0
    for day in days:
        f = SENTIMENT_DIR / f"{day['date']}.json"
        if not f.exists():
            continue
        data = json.loads(f.read_text())
        prev = data.get("own_account", {}) or {}
        data["own_account"] = {
            "followers": prev.get("followers"),
            "as_of": as_of,
            "source": "x_native_analytics_account_overview_csv",
            "tier": "measured",
            "daily": {k: v for k, v in day.items() if k != "date"},
            "posts": prev.get("posts", []),
        }
        f.write_text(json.dumps(data, indent=2) + "\n")
        attached += 1
        print(f"Attached own_account.daily rollup to {f}")

    if skipped_rows:
        print(
            f"\n{skipped_rows} row(s) had an unparseable date and were skipped.",
            file=sys.stderr,
        )
    print(
        f"\nAccount Overview import complete: {len(days)} day(s) stored, "
        f"{attached} existing sentiment day-file(s) updated with daily rollup."
    )
    print(
        "Note: per-post own_account.posts[] still requires a Tweet-activity "
        "(Export by Tweet) CSV from analytics.x.com → Posts tab."
    )


def main() -> None:
    """Detect CSV export type and dispatch to the matching importer."""
    if len(sys.argv) != 2:
        print("Usage: python3 x-analytics-import.py <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("CSV had no rows - nothing to import.")
        return

    fieldnames = list(rows[0].keys())
    fmt = detect_format(fieldnames)
    print(f"Detected export type: {fmt}")
    print(f"Columns: {fieldnames}")

    if fmt == "tweet_activity":
        import_tweet_activity(rows, fieldnames)
    elif fmt == "account_overview":
        import_account_overview(rows, fieldnames)
    else:
        print(
            "Unrecognized CSV format. Expected either:\n"
            "  - Tweet activity (needs Date/Time + Permalink/URL), or\n"
            "  - Account Overview (needs Date + Impressions, no permalink).",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
