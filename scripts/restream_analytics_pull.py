#!/usr/bin/env python3
"""
Pull Restream's full account-level tracking for recent stream events: destinations
(channels), event inventory, per-event viewer analytics, and per-event chat
analytics (aggregate message/chatter counts - NOT individual message text, see
note below). Requires a paid Restream plan - confirmed via research 2026-08-23
that Restream's own docs state "A paid plan is required to access full Analytics.
Free users will see a restricted view."

Writes campaign/analytics/restream/YYYY-MM-DD.json (schema v1, data_status
"measured"). Design rules, matching scripts/youtube-pull.py:
  1. Never invent a number. Missing means null, never 0.
  2. Fail loudly and write nothing on any partial/uncertain pull.
  3. Idempotent - re-running for the same day overwrites, never appends.
  4. Every record carries its provenance (exact requests made).

IMPORTANT - what this does NOT give you: individual chat message text/author.
Researched 2026-08-22/23: Restream's Chat API is WebSocket-only
(wss://chat.api.restream.io) - a live connection held open during the stream.
No REST "chat history" endpoint for retrieving past message text was found
anywhere (official docs nav, a community-built MCP server's actual API calls,
the API-cataloger's machine-readable spec). The REST-accessible chat data is
this script's `chat_analytics` block - aggregate counts only. Real per-message
sentiment classification needs either a live WebSocket listener (a genuinely
different, always-on architecture - not built here) or Restream's own manual
CSV export from the dashboard's Past Streams page (anonymized chatter handles).
Both are separate, unresolved decisions - see infrastructure/n8n/README.md.

UNCONFIRMED ENDPOINT PATHS (this research could not fully render Restream's
JS-based docs site to verify): the destinations and event-history paths below
are best guesses from conflicting secondary sources. The two analytics paths
ARE confirmed against developers.restream.io/analytics directly. If this script
fails on the unconfirmed calls, check developers.restream.io's docs in a
browser for the exact path and update the ENDPOINT constants below - do not
guess further blind.

Requires:
  RESTREAM_ACCESS_TOKEN  - from scripts/restream_oauth_setup.py
  (no refresh flow implemented yet - unconfirmed whether Restream issues
  refresh tokens the way X does; see restream_oauth_setup.py's note)

Usage:
    python3 scripts/restream_analytics_pull.py [--dry-run] [--lookback-days 7]
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API = "https://api.restream.io/v2"
OUT_DIR = "campaign/analytics/restream"
SOURCE_SYSTEM = "restream_api_v2"

# CONFIRMED via developers.restream.io/analytics (2026-08-23):
EP_VIEWER_ANALYTICS = "analytics/event-analytics-viewers"
EP_CHAT_ANALYTICS = "analytics/event-analytics-messages"

# UNCONFIRMED - conflicting secondary sources, see module docstring:
EP_DESTINATIONS = "user/channels"          # community MCP server used this path
EP_EVENTS_HISTORY = "events/events-history"  # only source: this repo's own
                                              # pre-existing (unverified) n8n workflow


class PullError(RuntimeError):
    """Fatal. Nothing gets written."""


class Client:
    def __init__(self, token):
        self.token = token
        self.requests = []

    def get(self, endpoint, **params):
        url = f"{API}/{endpoint}"
        if params:
            url += f"?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:400]
            hint = ""
            if endpoint in (EP_DESTINATIONS, EP_EVENTS_HISTORY):
                hint = (f" This path ({endpoint}) is UNCONFIRMED by research - "
                        f"check developers.restream.io's docs directly for the "
                        f"real path and update the EP_* constant at the top of "
                        f"this script.")
            if e.code == 401:
                raise PullError(
                    f"401 from {endpoint}. Token expired or invalid - "
                    f"re-run scripts/restream_oauth_setup.py.{hint}"
                ) from e
            if e.code == 403:
                raise PullError(
                    f"403 from {endpoint}. Likely a plan-tier restriction - "
                    f"Restream's docs state full Analytics needs a paid plan; "
                    f"confirm this account has one.{hint}"
                ) from e
            if e.code == 404:
                raise PullError(f"404 from {endpoint} - endpoint does not exist "
                                 f"as called.{hint}") from e
            raise PullError(f"HTTP {e.code} from {endpoint}: {detail}{hint}") from e
        except urllib.error.URLError as e:
            raise PullError(f"Network failure reaching {endpoint}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise PullError(f"{endpoint} returned non-JSON: {e}") from e

        self.requests.append(url.replace(self.token, "<TOKEN>"))
        return body


def _num_or_none(d, *keys):
    for k in keys:
        if k in d and d[k] is not None:
            try:
                return float(d[k]) if isinstance(d[k], float) else int(d[k])
            except (TypeError, ValueError):
                return None
    return None


def fetch(client, lookback_days):
    destinations_raw = client.get(EP_DESTINATIONS)
    destinations = [
        {
            "platform": c.get("platform") or c.get("streamingPlatformId"),
            "display_name": c.get("displayName") or c.get("name"),
            "enabled": c.get("enabled", True),
        }
        for c in (destinations_raw.get("items") or destinations_raw or [])
        if isinstance(c, dict)
    ]

    events_raw = client.get(EP_EVENTS_HISTORY)
    events_list = events_raw.get("items") or events_raw if isinstance(events_raw, (list, dict)) else []
    if isinstance(events_list, dict):
        events_list = events_list.get("items", [])
    if not isinstance(events_list, list):
        raise PullError(f"{EP_EVENTS_HISTORY} did not return a list - "
                         f"check the response shape and adjust parsing.")

    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    events = []
    for e in events_list:
        eid = e.get("id") or e.get("eventIdentifier")
        if not eid:
            continue
        started_raw = e.get("scheduledFor") or e.get("startedAt") or e.get("createdAt")
        try:
            started = datetime.fromisoformat(str(started_raw).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            started = None
        if started and started < cutoff:
            continue
        events.append({
            "event_id": eid,
            "title": e.get("title") or e.get("name"),
            "started_at": started.isoformat() if started else None,
        })

    for ev in events:
        viewer_raw = client.get(EP_VIEWER_ANALYTICS, eventId=ev["event_id"])
        ev["viewer_analytics"] = {
            "peak_viewers": _num_or_none(viewer_raw, "peakViewers", "peak"),
            "total_views": _num_or_none(viewer_raw, "totalViews", "views"),
            "by_platform": viewer_raw.get("byPlatform") or viewer_raw.get("platforms"),
            "time_series": viewer_raw.get("timeSeries") or viewer_raw.get("series"),
            "tier": "measured",
        }

        chat_raw = client.get(EP_CHAT_ANALYTICS, eventId=ev["event_id"])
        ev["chat_analytics"] = {
            "total_messages": _num_or_none(chat_raw, "totalMessages", "messages"),
            "unique_chatters": _num_or_none(chat_raw, "uniqueChatters", "uniqueUsers"),
            "time_series": chat_raw.get("timeSeries") or chat_raw.get("series"),
            "tier": "measured",
            "note": "Aggregate counts only - no per-message text/author available "
                    "via this REST endpoint. See module docstring.",
        }

    return destinations, events


def build(date, destinations, events, client, lookback_days):
    return {
        "schema_version": 1,
        "date": date,
        "scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_status": "measured",
        "collection": {
            "method": SOURCE_SYSTEM,
            "lookback_days": lookback_days,
            "requests": client.requests,
            "coverage": "census (of events in the lookback window)",
            "notes": "chat_analytics is aggregate only (total messages, unique "
                     "chatters) - individual message text/author is not available "
                     "via REST (Chat API is WebSocket-only). See module docstring "
                     "in scripts/restream_analytics_pull.py.",
        },
        "destinations": destinations,
        "events": events,
        "_ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_source_system": SOURCE_SYSTEM,
    }


def validate(doc):
    errs = []
    if doc["schema_version"] != 1:
        errs.append("schema_version must be 1")
    if doc["data_status"] != "measured":
        errs.append("data_status must be 'measured'")
    if not doc["collection"]["requests"]:
        errs.append("no provenance recorded")
    ids = [e["event_id"] for e in doc["events"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate event_id")
    return errs


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    lookback_days = 7
    if "--lookback-days" in args:
        lookback_days = int(args[args.index("--lookback-days") + 1])
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    token = os.environ.get("RESTREAM_ACCESS_TOKEN")
    if not token:
        sys.exit(
            "FATAL: RESTREAM_ACCESS_TOKEN is not set.\n"
            "  Run scripts/restream_oauth_setup.py (authorize, then exchange)\n"
            "  to obtain one. Refusing to proceed without it."
        )

    client = Client(token)
    try:
        destinations, events = fetch(client, lookback_days)
    except PullError as e:
        sys.exit(f"FATAL: {e}\nNothing written.")

    doc = build(date, destinations, events, client, lookback_days)
    errs = validate(doc)
    if errs:
        sys.exit("FATAL: validation failed:\n  " + "\n  ".join(errs) + "\nNothing written.")

    print(f"{len(events)} event(s) in the last {lookback_days} day(s), "
          f"{len(destinations)} destination(s)")
    for ev in events:
        va, ca = ev["viewer_analytics"], ev["chat_analytics"]
        print(f"  {ev['event_id']} ({ev.get('title')}): "
              f"peak_viewers={va['peak_viewers']}, "
              f"total_messages={ca['total_messages']}, "
              f"unique_chatters={ca['unique_chatters']}")

    if dry:
        print("--dry-run: not writing")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{date}.json")
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
