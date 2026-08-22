#!/usr/bin/env python3
"""
Pull $TEL's full historical price/market-cap/volume series from CoinGecko's free
public API (no key required) for the dashboard.

Why this and not historical sentiment: real historical mentions/sentiment data
from X cannot be recovered for free - WebSearch only sees what's currently
indexed, not a time machine, and the 2026-08-02 backfill attempt confirmed this
empirically (zero historical days recovered, see scripts/sentiment-scraper.md
Step 0b). $TEL's market history, by contrast, genuinely exists back to token
launch and CoinGecko publishes it for free with no signup - this is the best
"historical $TEL data" the dashboard can show without spending anything, per the
user's $0 budget (campaign/AGENCY-MEMORY.md, confirmed 2026-08-22).

This is LISTEN-ONLY / dashboard-context data. Per campaign/analytics/
NARRATIVE-TAXONOMY.json, `price` is publishable: false - @telcoinTAO never
comments on price action or market cap. This script's output feeds internal
dashboard context alongside sentiment, never a public post.

IMPORTANT - public API history cap: CoinGecko's plain public endpoint (what this
script calls - no key, no signup) only returns the trailing 365 days; asking for
more returns HTTP 401 ("Public API users are limited to querying historical data
within the past 365 days"). The full 2018-onward history in
campaign/analytics/market/tel-price-history.json was seeded ONCE (2026-08-22) via
the CoinGecko MCP available inside Claude sessions, which has broader access than
an unauthenticated script does. This script MERGES its (capped) results into the
existing file rather than overwriting it, specifically so a routine re-run never
destroys that deep history - never change this to a blind overwrite.

Usage:
    python3 scripts/tel-price-history.py            # trailing 365 days (max the
                                                      # public API allows)
    python3 scripts/tel-price-history.py --days 90   # shorter window, faster/lighter

Writes/updates campaign/analytics/market/tel-price-history.json, merging by date -
safe and cheap to re-run any time.
"""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

COINGECKO_ID = "telcoin"
API_URL = f"https://api.coingecko.com/api/v3/coins/{COINGECKO_ID}/market_chart"
OUT_DIR = Path("campaign/analytics/market")
OUT_FILE = OUT_DIR / "tel-price-history.json"


def fetch(days):
    url = f"{API_URL}?vs_currency=usd&days={days}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"CoinGecko request failed ({e.code}): {body}", file=sys.stderr)
        if e.code == 429:
            print("Rate limited - CoinGecko's free public tier allows only a "
                  "modest request rate. Wait a minute and retry.", file=sys.stderr)
        sys.exit(1)


def to_daily_series(chart):
    """Collapse whatever granularity CoinGecko returns (hourly for recent history,
    daily further back) to one row per UTC date, taking that day's last sample -
    a standard daily-close rollup, never a fabricated or interpolated value."""
    prices = {int(t): v for t, v in chart.get("prices", [])}
    caps = {int(t): v for t, v in chart.get("market_caps", [])}
    vols = {int(t): v for t, v in chart.get("total_volumes", [])}

    by_day = {}
    for ts_ms in sorted(prices):
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        date_key = dt.date().isoformat()
        by_day[date_key] = {
            "date": date_key,
            "price_usd": prices.get(ts_ms),
            "market_cap_usd": caps.get(ts_ms),
            "volume_usd": vols.get(ts_ms),
            "as_of_timestamp": dt.isoformat(),
        }
    return [by_day[d] for d in sorted(by_day)]


def main():
    days = "365"
    if len(sys.argv) > 1 and sys.argv[1] == "--days":
        days = sys.argv[2] if len(sys.argv) > 2 else "365"

    chart = fetch(days)
    fresh = to_daily_series(chart)
    if not fresh:
        print("No data returned - nothing written.", file=sys.stderr)
        sys.exit(1)

    existing = {}
    source = "coingecko_public_api"
    if OUT_FILE.exists():
        prev = json.loads(OUT_FILE.read_text())
        existing = {d["date"]: d for d in prev.get("days", [])}
        # A file seeded by the deeper MCP backfill stays labeled that way even as
        # its recent tail gets refreshed by this public-API script - the label
        # describes how the bulk of the history was obtained, not the latest edit.
        if prev.get("source") == "coingecko_mcp_one_time_deep_backfill":
            source = prev["source"]

    for row in fresh:
        existing[row["date"]] = row  # fresh rows overwrite stale ones by date
    merged = [existing[d] for d in sorted(existing)]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "asset": "$TEL",
        "coingecko_id": COINGECKO_ID,
        "tier": "measured",
        "publishable": False,
        "listen_only_reason": "Standing rule: @telcoinTAO does not comment on "
                               "price action or market cap. Dashboard context "
                               "only, never a public post.",
        "source": source,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "period_start": merged[0]["date"],
        "period_end": merged[-1]["date"],
        "n_days": len(merged),
        "days": merged,
    }
    OUT_FILE.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {OUT_FILE}: {len(merged)} days total "
          f"({len(fresh)} refreshed from this run), "
          f"{merged[0]['date']} -> {merged[-1]['date']}")


if __name__ == "__main__":
    main()
