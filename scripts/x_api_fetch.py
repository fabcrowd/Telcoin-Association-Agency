#!/usr/bin/env python3
"""
Fully automated pull of @telcoinTAO's own-post performance from the X API v2 -
real impressions, engagement, and link clicks (the "measured" tier in
campaign/analytics/sentiment/*.json). Meant to run daily, right alongside the
community scraper (scripts/sentiment-scraper.md), with zero human involvement.

Requires a one-time account connection (scripts/x_oauth_setup.py) done once.
After that, this script refreshes its own access token on every run using a
stored refresh token, and X rotates that refresh token on every use - this
script rewrites its stored copy each run so the chain never breaks on its own.

Env vars / secrets required:
  X_CLIENT_ID, X_CLIENT_SECRET   - from the X Developer App
  X_USER_ID                      - numeric X user id for @telcoinTAO (fetch once
                                    via GET /2/users/by/username/telcoinTAO with
                                    any bearer token, then hardcode - it never
                                    changes)
  X_REFRESH_TOKEN                - only used to seed X_REFRESH_TOKEN_FILE the
                                    very first run if that file doesn't exist yet
  X_REFRESH_TOKEN_FILE           - defaults to .x_refresh_token next to this
                                    script; point it at a real persistent secret
                                    store in production, not a plain file

Known API limit: X only returns organic_metrics/non_public_metrics for tweets
created in roughly the last 30 days. This script's 24h lookback window is
always well inside that limit, so it never bites the daily automated run - it
would only matter if this were repurposed for a longer backfill (use
scripts/x-analytics-import.py against a manual CSV export for that instead).
"""
import json
import os
import sys
import base64
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

TOKEN_URL = "https://api.x.com/2/oauth2/token"
API_BASE = "https://api.x.com/2"
SENTIMENT_DIR = Path("campaign/analytics/sentiment")
REFRESH_FILE = Path(os.environ.get("X_REFRESH_TOKEN_FILE", ".x_refresh_token"))


def env(name, required=True):
    v = os.environ.get(name)
    if required and not v:
        print(f"Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return v


def http_post_form(url, data, headers):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(),
                                  method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"POST {url} failed ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def http_get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"GET {url} failed ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def refresh_access_token():
    client_id = env("X_CLIENT_ID")
    client_secret = env("X_CLIENT_SECRET")
    if REFRESH_FILE.exists():
        refresh_token = REFRESH_FILE.read_text().strip()
    else:
        refresh_token = env("X_REFRESH_TOKEN")

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    tokens = http_post_form(TOKEN_URL, {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }, {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}",
    })
    # X invalidates the previous refresh token the moment a new one is issued -
    # persist immediately so the next run doesn't retry a dead token.
    REFRESH_FILE.write_text(tokens["refresh_token"])
    return tokens["access_token"]


def fetch_recent_own_posts(access_token, user_id, since):
    params = {
        "max_results": "100",
        "start_time": since.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tweet.fields": "created_at,public_metrics,organic_metrics,non_public_metrics",
    }
    url = f"{API_BASE}/users/{user_id}/tweets?{urllib.parse.urlencode(params)}"
    result = http_get(url, {"Authorization": f"Bearer {access_token}"})
    return result.get("data", [])


def to_own_account_post(t):
    pub = t.get("public_metrics") or {}
    org = t.get("organic_metrics") or t.get("non_public_metrics") or {}

    impressions = org.get("impression_count")
    engagement_fields = ("like_count", "retweet_count", "reply_count", "quote_count")
    engagements = (
        sum(pub.get(k, 0) or 0 for k in engagement_fields)
        if any(k in pub for k in engagement_fields) else None
    )
    engagement_rate = (
        round(engagements / impressions * 100, 2)
        if engagements is not None and impressions else None
    )

    return {
        "url": f"https://x.com/telcoinTAO/status/{t['id']}",
        "published_at": t["created_at"],
        "narratives": [],
        "layer": None,
        "impressions": impressions,
        "engagements": engagements,
        "engagement_rate": engagement_rate,
        "link_clicks": org.get("url_link_clicks"),
        "profile_visits": org.get("user_profile_clicks"),
    }


def main():
    user_id = env("X_USER_ID")
    access_token = refresh_access_token()
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    raw_posts = fetch_recent_own_posts(access_token, user_id, since)

    by_day = {}
    for t in raw_posts:
        created = datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
        by_day.setdefault(created.date().isoformat(), []).append(to_own_account_post(t))

    if not by_day:
        print("No own posts in the last 24h - nothing to write.")
        return

    for date_key, day_posts in sorted(by_day.items()):
        f = SENTIMENT_DIR / f"{date_key}.json"
        if not f.exists():
            print(f"No host file for {date_key} yet - the daily community scraper "
                  f"runs first, own_account attaches to its output. Skipping.",
                  file=sys.stderr)
            continue
        data = json.loads(f.read_text())
        existing_by_url = {p.get("url"): p for p in data.get("posts", []) if p.get("is_own_post")}
        for post in day_posts:
            match = existing_by_url.get(post["url"])
            if match:
                post["narratives"] = match.get("narratives", [])
        data["own_account"] = {
            "followers": data.get("own_account", {}).get("followers"),
            "as_of": datetime.now(timezone.utc).isoformat(),
            "source": "x_api_v2_oauth",
            "tier": "measured",
            "posts": day_posts,
        }
        f.write_text(json.dumps(data, indent=2) + "\n")
        print(f"Updated {f} with {len(day_posts)} own-account post(s) from the X API")


if __name__ == "__main__":
    main()
