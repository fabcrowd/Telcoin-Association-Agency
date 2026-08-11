#!/usr/bin/env python3
"""
Pull @TelcoinTAO YouTube statistics via the YouTube Data API v3.

Writes campaign/analytics/youtube/YYYY-MM-DD.json (schema v2, data_status "measured").

Design rules, in order of importance:
  1. Never invent a number. Missing means null, never 0.
  2. Fail loudly and write nothing. A missing day is recoverable; a day of
     zeros silently entering a trend line is not.
  3. Idempotent. Re-running for the same day overwrites, never appends.
  4. Every record carries its provenance.

Requires YOUTUBE_API_KEY (a key restricted to YouTube Data API v3).

Usage:
    python3 scripts/youtube-pull.py [--dry-run] [--date YYYY-MM-DD]
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CHANNEL_ID = "UCs5IFXnrKliqRA6U4o_VD2Q"  # @TelcoinTAO, verified 2026-07-30
API = "https://www.googleapis.com/youtube/v3"
SOURCE_SYSTEM = "youtube_data_api_v3"
OUT_DIR = "campaign/analytics/youtube"
QUOTA_WARN = 100  # a full channel pull should cost well under 20 units


class PullError(RuntimeError):
    """Fatal. Nothing gets written."""


class Client:
    def __init__(self, key):
        self.key = key
        self.units = 0
        self.requests = []

    def get(self, endpoint, cost=1, **params):
        params["key"] = self.key
        url = f"{API}/{endpoint}?" + urllib.parse.urlencode(params)
        redacted = url.replace(self.key, "<KEY>")
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                body = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:400]
            if e.code == 403:
                raise PullError(
                    f"403 from {endpoint}. Quota exhausted, or the key is not "
                    f"authorized for YouTube Data API v3.\n{detail}"
                ) from e
            raise PullError(f"HTTP {e.code} from {endpoint}: {detail}") from e
        except urllib.error.URLError as e:
            raise PullError(f"Network failure reaching {endpoint}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise PullError(f"{endpoint} returned non-JSON: {e}") from e

        self.units += cost
        self.requests.append(redacted)
        if self.units > QUOTA_WARN:
            raise PullError(
                f"Quota spend hit {self.units} units - far above the ~20 a full "
                f"pull should cost. Refusing to continue; something is looping."
            )
        return body


def _int_or_none(d, key):
    """Absent means unknown. A channel hiding likes is not zero likes."""
    v = d.get(key)
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def fetch(client):
    ch = client.get("channels", part="contentDetails,statistics,snippet", id=CHANNEL_ID)
    items = ch.get("items") or []
    if not items:
        raise PullError(f"Channel {CHANNEL_ID} returned no items. Wrong ID, or key lacks access.")
    channel = items[0]
    uploads = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    video_ids, page = [], None
    while True:
        kw = {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}
        if page:
            kw["pageToken"] = page
        pl = client.get("playlistItems", **kw)
        video_ids += [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        page = pl.get("nextPageToken")
        if not page:
            break

    if not video_ids:
        raise PullError("Uploads playlist is empty - unexpected for this channel.")
    if len(video_ids) != len(set(video_ids)):
        raise PullError("Duplicate video IDs returned; refusing to write a corrupt pull.")

    videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        vs = client.get("videos", part="snippet,statistics,contentDetails", id=",".join(batch))
        for v in vs.get("items", []):
            st, sn = v.get("statistics", {}), v.get("snippet", {})
            videos.append({
                "video_id": v["id"],
                "title": sn.get("title"),
                "published_at": sn.get("publishedAt"),
                "duration": v.get("contentDetails", {}).get("duration"),
                "view_count": _int_or_none(st, "viewCount"),
                "like_count": _int_or_none(st, "likeCount"),
                "comment_count": _int_or_none(st, "commentCount"),
                "narratives": [],   # tagged downstream against NARRATIVE-TAXONOMY.json
                "layer": None,
                "tier": "measured",
            })

    # Reconciliation invariant: every requested ID is accounted for.
    returned = {v["video_id"] for v in videos}
    missing = set(video_ids) - returned
    if missing:
        raise PullError(
            f"{len(missing)} of {len(video_ids)} videos did not come back "
            f"(e.g. {sorted(missing)[:3]}). Refusing a partial pull."
        )

    stats = channel.get("statistics", {})
    return channel, videos, {
        "subscribers": _int_or_none(stats, "subscriberCount"),
        "subscribers_hidden": stats.get("hiddenSubscriberCount", False),
        "total_views": _int_or_none(stats, "viewCount"),
        "video_count": _int_or_none(stats, "videoCount"),
    }


def check_monotonic(videos, out_dir):
    """View counts are cumulative. A decrease means a bad pull, not a real drop."""
    try:
        prior = sorted(f for f in os.listdir(out_dir) if f.endswith(".json"))
    except FileNotFoundError:
        return []
    if not prior:
        return []
    with open(os.path.join(out_dir, prior[-1])) as f:
        last = json.load(f)
    before = {v["video_id"]: v.get("view_count") for v in last.get("videos", [])}
    regressions = [
        f"{v['video_id']}: {before[v['video_id']]} -> {v['view_count']}"
        for v in videos
        if v["view_count"] is not None
        and before.get(v["video_id"]) is not None
        and v["view_count"] < before[v["video_id"]]
    ]
    return regressions


def build(date, channel, videos, chan_stats, client):
    return {
        "schema_version": 2,
        "date": date,
        "scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_status": "measured",
        "collection": {
            "method": "youtube_data_api_v3",
            "channel_id": CHANNEL_ID,
            "handle": "@TelcoinTAO",
            "requests": client.requests,
            "quota_units_spent": client.units,
            "coverage": "census",
            "notes": "Full uploads playlist. Platform-reported figures, not a sample.",
        },
        "channel": chan_stats,
        "videos": videos,
        "_ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_source_system": SOURCE_SYSTEM,
    }


def validate(doc):
    errs = []
    if doc["schema_version"] != 2:
        errs.append("schema_version must be 2")
    if doc["data_status"] != "measured":
        errs.append("data_status must be 'measured'")
    if not doc["videos"]:
        errs.append("no videos")
    ids = [v["video_id"] for v in doc["videos"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate video_id")
    for v in doc["videos"]:
        if v["view_count"] is not None and v["view_count"] < 0:
            errs.append(f"negative view_count on {v['video_id']}")
        if not v.get("title"):
            errs.append(f"missing title on {v['video_id']}")
    if not doc["collection"]["requests"]:
        errs.append("no provenance recorded")
    return errs


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    date = (args[args.index("--date") + 1] if "--date" in args
            else datetime.now(timezone.utc).strftime("%Y-%m-%d"))

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit(
            "FATAL: YOUTUBE_API_KEY is not set.\n"
            "  Create a key at console.cloud.google.com, enable YouTube Data API v3,\n"
            "  restrict the key to that API, then add it as an environment secret.\n"
            "  Refusing to scrape statistics as a fallback - scraped counts break\n"
            "  silently, and silent failure is what produced the quarantined data."
        )

    client = Client(key)
    try:
        channel, videos, chan_stats = fetch(client)
    except PullError as e:
        sys.exit(f"FATAL: {e}\nNothing written.")

    regressions = check_monotonic(videos, OUT_DIR)
    if regressions:
        sys.exit(
            "FATAL: view counts went backwards, which cannot happen for real:\n  "
            + "\n  ".join(regressions[:5])
            + "\nThis indicates a bad pull. Nothing written."
        )

    doc = build(date, channel, videos, chan_stats, client)
    errs = validate(doc)
    if errs:
        sys.exit("FATAL: validation failed:\n  " + "\n  ".join(errs) + "\nNothing written.")

    total = sum(v["view_count"] for v in videos if v["view_count"] is not None)
    print(f"{len(videos)} videos | {total:,} total views | {client.units} quota units")

    if dry:
        print("--dry-run: not writing")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{date}.json")
    with open(path, "w") as f:                       # overwrite = idempotent
        json.dump(doc, f, indent=2)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
