#!/usr/bin/env python3
"""
Regenerate campaign/analytics/sentiment/dashboard.html from every current source
file under campaign/analytics/. Run from the repo root whenever any source file
changes (a new sentiment day, a fresh price pull, a new Grok spot-check, etc.) -
this is the single place that compiles all of them into the one dashboard.

Sources read (each a self-contained store with its own README/spec):
  campaign/analytics/account-overview/daily.json   - @telcoinTAO measured (X)
  campaign/analytics/sentiment/*.json              - community sentiment (measured only)
  campaign/analytics/NARRATIVE-TAXONOMY.json       - narrative labels + publishable flags
  campaign/analytics/market/tel-price-history.json - $TEL price/market (derived, listen-only)
  campaign/analytics/community-grok/*.json         - Grok manual community spot-check (observed)
  campaign/analytics/web-mentions/weekly.json      - general web presence (derived, weak instrument)
  campaign/analytics/youtube/*.json                - @TelcoinTAO YouTube channel (measured)
  campaign/analytics/restream/, streams/           - Restream (built, shown as "not connected"
                                                      until real files exist - see
                                                      infrastructure/n8n/README.md)

Never hand-edit dashboard.html's data blocks or generated sections directly -
re-run this script instead, so the file always matches its sources exactly.

Usage:
    python3 scripts/build-dashboard.py
"""
import json
import html
from pathlib import Path

ROOT = Path(".")
OUT = ROOT / "campaign/analytics/sentiment/dashboard.html"


def load(path):
    return json.loads((ROOT / path).read_text())


def esc(s):
    return html.escape(str(s), quote=False)


def fmt_int(n):
    return f"{n:,}" if n is not None else "—"


def fmt_price(p):
    return f"${p:.5f}"


def fmt_pct(p):
    return f"{p:.1f}%"


def gather():
    # ---- Own account (X) --------------------------------------------------
    account = load("campaign/analytics/account-overview/daily.json")
    account_raw = [
        {
            "date": d["date"], "impressions": d["impressions"], "engagements": d["engagements"],
            "engagement_rate": d["engagement_rate"], "likes": d["likes"], "replies": d["replies"],
            "reposts": d["reposts"], "profile_visits": d["profile_visits"],
            "new_follows": d["new_follows"], "posts_published": d["posts_published"],
            "tier": d["tier"],
        }
        for d in account["days"]
    ]
    acct_total_impr = sum(d["impressions"] for d in account["days"])
    acct_total_eng = sum(d["engagements"] for d in account["days"])
    acct_peak = max(account["days"], key=lambda d: d["impressions"])
    acct_rate = round(acct_total_eng / acct_total_impr * 100, 1) if acct_total_impr else None

    # ---- Community sentiment (WebSearch daily series) ----------------------
    tax = load("campaign/analytics/NARRATIVE-TAXONOMY.json")
    narrative_labels = {n["id"]: n["label"] for n in tax["narratives"]}
    narrative_publishable = {n["id"]: n["publishable"] for n in tax["narratives"]}

    raw = []
    for p in sorted((ROOT / "campaign/analytics/sentiment").glob("*.json")):
        d = json.loads(p.read_text())
        if d.get("data_status") != "measured":
            continue
        raw.append({
            "date": d["date"], "data_status": d["data_status"],
            "sentiment_score": d["composite"]["sentiment_score"],
            "n_classified": d["composite"]["n_classified"],
            "total_mentions": d["composite"]["total_mentions"],
            "unique_authors": d["composite"]["unique_authors"],
            "top_narrative": d["composite"]["top_narrative"],
            "hour_distribution": d["composite"]["hour_distribution"],
            "narratives": {k: v["community_mentions"] for k, v in d.get("narratives", {}).items()},
            "questions": d.get("questions", []),
            "share_of_voice": d.get("share_of_voice", {}).get("indexed", d.get("share_of_voice", {})),
            "own_account": d.get("own_account", {}),
        })
    raw.sort(key=lambda r: r["date"])
    community_days = len(raw)

    ledger = {}
    for r in raw:
        for nid, count in r["narratives"].items():
            ledger[nid] = ledger.get(nid, 0) + count
    ledger_rows = sorted(ledger.items(), key=lambda kv: -kv[1])

    all_questions = {}
    for r in raw:
        for q in r["questions"]:
            all_questions[q["id"]] = q  # later day's ledger already carries prior days forward
    open_questions = [q for q in all_questions.values() if q["status"] == "open"]

    # ---- $TEL price/market (derived, listen-only) --------------------------
    price = load("campaign/analytics/market/tel-price-history.json")
    price_days = price["days"]
    price_recent = price_days[-180:]
    price_recent_out = [{"date": r["date"], "price_usd": round(r["price_usd"], 6)} for r in price_recent]
    price_ath = max(price_days, key=lambda r: r["price_usd"])
    price_atl = min(price_days, key=lambda r: r["price_usd"])
    price_current = price_days[-1]

    # ---- Community spot-check (Grok manual pull, observed) -----------------
    grok_files = sorted((ROOT / "campaign/analytics/community-grok").glob("*.json"))
    grok = json.loads(grok_files[-1].read_text()) if grok_files else None
    grok_weeks = grok_top = None
    if grok:
        grok_weeks = [
            {"week_start": w["week_start"], "week_end": w["week_end"],
             "sampled_posts": w["sampled_posts"], "positive_pct": w["positive_pct"],
             "combined_engagement": w["combined_engagement"]}
            for w in grok["weekly"]
        ]
        grok_top = [
            {"date": p["date"], "author_handle": p["author_handle"], "likes": p["likes"],
             "sentiment": p["sentiment"], "text_excerpt": p["text_excerpt"]}
            for p in sorted(grok["top_posts"], key=lambda p: -p["likes"])[:5]
        ]

    # ---- General web presence (derived, weak instrument) -------------------
    webm_path = ROOT / "campaign/analytics/web-mentions/weekly.json"
    webm_weeks = load(webm_path)["weeks"] if webm_path.exists() else []

    # ---- YouTube (measured, second own-channel) -----------------------------
    yt_files = sorted((ROOT / "campaign/analytics/youtube").glob("*.json"))
    yt = json.loads(yt_files[-1].read_text()) if yt_files else None
    yt_top = []
    if yt:
        yt_top = [
            {"title": v["title"], "view_count": v["view_count"], "video_id": v["video_id"]}
            for v in sorted(yt["videos"], key=lambda v: -(v.get("view_count") or 0))[:5]
        ]

    # ---- Restream (built, not yet activated - no real data until it is) ----
    restream_dir = ROOT / "campaign/analytics/restream"
    streams_dir = ROOT / "campaign/analytics/streams"
    restream_live = bool(
        (restream_dir.exists() and list(restream_dir.glob("*.json")))
        or (streams_dir.exists() and list(streams_dir.glob("*.json")))
    )

    return dict(
        account_raw=account_raw, acct_total_impr=acct_total_impr, acct_total_eng=acct_total_eng,
        acct_peak=acct_peak, acct_rate=acct_rate,
        raw=raw, community_days=community_days,
        ledger_rows=ledger_rows, narrative_labels=narrative_labels,
        narrative_publishable=narrative_publishable, open_questions=open_questions,
        price_recent=price_recent_out, price_ath=price_ath, price_atl=price_atl,
        price_current=price_current, price_n_days=len(price_days),
        price_period_start=price["period_start"],
        grok=grok, grok_weeks=grok_weeks, grok_top=grok_top,
        webm_weeks=webm_weeks,
        yt=yt, yt_top=yt_top,
        restream_live=restream_live,
    )


def build_html(d):
    community_days = d["community_days"]
    status_text = f"Community {community_days}/14 &middot; 6 sources tracked"

    account_kpis = f"""
      <div class="kpi"><span class="label">Impressions</span><span class="value">{fmt_int(d['acct_total_impr'])}</span><span class="hint">{len(d['account_raw'])} days</span></div>
      <div class="kpi"><span class="label">Engagements</span><span class="value">{fmt_int(d['acct_total_eng'])}</span><span class="hint">{d['acct_rate']}% rate</span></div>
      <div class="kpi"><span class="label">Peak day</span><span class="value">{fmt_int(d['acct_peak']['impressions'])}</span><span class="hint">{d['acct_peak']['date']} &middot; {fmt_int(d['acct_peak']['engagements'])} eng</span></div>
"""

    yt_section = ""
    if d["yt"]:
        yt = d["yt"]
        yt_rows = "".join(
            f'<li><span class="mini-list-val">{fmt_int(v["view_count"])}</span><span class="mini-list-label">{esc(v["title"][:64])}</span></li>'
            for v in d["yt_top"]
        )
        yt_section = f"""
  <section class="chart-card">
    <div class="card-head">
      <h4>YouTube channel &mdash; @TelcoinTAO</h4>
      <span class="card-meta">measured &middot; YouTube Data API v3</span>
    </div>
    <div class="kpis">
      <div class="kpi"><span class="label">Subscribers</span><span class="value">{fmt_int(yt['channel']['subscribers'])}</span><span class="hint">{fmt_int(yt['channel']['video_count'])} videos</span></div>
      <div class="kpi"><span class="label">Total views</span><span class="value">{fmt_int(yt['channel']['total_views'])}</span><span class="hint">lifetime, all videos</span></div>
    </div>
    <p class="chart-note">Top videos by view count:</p>
    <ul class="mini-list">{yt_rows}</ul>
    <p class="chart-note" style="margin-top:2px">Second own-channel measured source, alongside X above &mdash; same tier, same
      "platform's own analytics" standard. See <code>campaign/analytics/youtube/</code>.</p>
  </section>
"""

    price_pts = d["price_recent"]
    pmin = min(r["price_usd"] for r in price_pts)
    pmax = max(r["price_usd"] for r in price_pts)
    W, H, padT, padB, padL, padR = 960, 160, 12, 28, 8, 8
    innerW, innerH = W - padL - padR, H - padT - padB
    n = len(price_pts)

    def px(i):
        return padL + (i / max(n - 1, 1)) * innerW

    def py(v):
        if pmax == pmin:
            return padT + innerH / 2
        return padT + innerH - ((v - pmin) / (pmax - pmin)) * innerH

    poly_points = " ".join(f"{px(i):.1f},{py(r['price_usd']):.2f}" for i, r in enumerate(price_pts))
    area_points = f"{px(0):.1f},{padT+innerH:.1f} " + poly_points + f" {px(n-1):.1f},{padT+innerH:.1f}"
    label_idx = [0, (n - 1) // 2, n - 1]
    price_labels = "".join(
        f'<text x="{px(i):.1f}" y="{H-8}" text-anchor="middle" fill="#6a719f" font-size="10" font-family="ui-monospace,monospace">{price_pts[i]["date"][5:]}</text>'
        for i in label_idx
    )

    price_section = f"""
  <section class="chart-card">
    <div class="card-head">
      <h4>$TEL price &amp; market context</h4>
      <span class="card-meta">derived &middot; CoinGecko, listen-only</span>
    </div>
    <div class="kpis">
      <div class="kpi"><span class="label">Price</span><span class="value">{fmt_price(d['price_current']['price_usd'])}</span><span class="hint">{d['price_current']['date']}</span></div>
      <div class="kpi"><span class="label">Market cap</span><span class="value">${fmt_int(round(d['price_current']['market_cap_usd']))}</span><span class="hint">24h vol ${fmt_int(round(d['price_current']['volume_usd']))}</span></div>
      <div class="kpi"><span class="label">All-time high</span><span class="value">{fmt_price(d['price_ath']['price_usd'])}</span><span class="hint">{d['price_ath']['date']}</span></div>
      <div class="kpi"><span class="label">All-time low</span><span class="value">{fmt_price(d['price_atl']['price_usd'])}</span><span class="hint">{d['price_atl']['date']}</span></div>
    </div>
    <svg class="line-chart" viewBox="0 0 960 160" preserveAspectRatio="none" role="img" aria-label="TEL price, trailing 180 days">
      <polygon points="{area_points}" fill="rgba(20,200,255,.12)" stroke="none"></polygon>
      <polyline points="{poly_points}" fill="none" stroke="#14c8ff" stroke-width="1.5"></polyline>
      {price_labels}
    </svg>
    <p class="chart-note">Trailing 180 days shown &mdash; full history back to listing
      ({d['price_period_start']}, {d['price_n_days']:,} days) lives in
      <code>campaign/analytics/market/tel-price-history.json</code>.
      <strong>Listen-only</strong>: price is a <code>publishable: false</code> narrative &mdash;
      @telcoinTAO never comments on price action or market cap. This panel is internal
      context, paired against sentiment below to spot correlation or divergence, never a
      source for a public post.</p>
  </section>
"""

    notice_lines = "<br>\n      ".join(
        f"{r['date']}: {r['total_mentions']} community mentions, sentiment {r['sentiment_score']:.2f} (n={r['n_classified']})"
        for r in d["raw"]
    ) or "No measured community days yet."

    ledger_rows_html = "".join(
        f"""<div class="ledger-row{' listen-only' if d['narrative_publishable'].get(nid) is False else ''}">
        <span class="ledger-label">{esc(d['narrative_labels'].get(nid, nid))}</span>
        <span class="ledger-bar-track"><span class="ledger-bar" style="width:{(count / max(c for _, c in d['ledger_rows']) * 100):.0f}%"></span></span>
        <span class="ledger-count">{count}</span>
      </div>"""
        for nid, count in d["ledger_rows"]
    )

    questions_html = "".join(
        f"""<div class="q-row">
        <span class="q-text">{esc(q['text_canonical'])}</span>
        <span class="q-meta">asked {q['times_observed']}&times; &middot; since {q['first_seen']}</span>
      </div>"""
        for q in d["open_questions"]
    ) or '<p class="chart-note">No open questions recorded yet.</p>'

    narrative_ledger_panel = f"""
      <div class="slot lead wide">
        <div class="slot-top"><h4>Narrative ledger</h4><span class="card-meta">{community_days} measured day{'s' if community_days != 1 else ''}</span></div>
        <p>Community mentions by subject, summed across every measured day so far. Subjects the
          Association doesn't publish on (price, banking) are shown but marked listen-only.</p>
        <div class="ledger">{ledger_rows_html}</div>
      </div>""" if d["ledger_rows"] else """
      <div class="slot lead"><div class="slot-top"><h4>Narrative ledger</h4><span class="pend">day 1</span></div>
      <p>Each narrative in one row: what the community is discussing, against what we published and how far it travelled.</p></div>"""

    open_questions_panel = f"""
      <div class="slot lead wide">
        <div class="slot-top"><h4>Open questions</h4><span class="card-meta">{len(d['open_questions'])} open</span></div>
        <p>Questions the community keeps asking that haven't been answered yet.</p>
        <div class="q-list">{questions_html}</div>
      </div>""" if d["raw"] else """
      <div class="slot lead"><div class="slot-top"><h4>Open questions</h4><span class="pend">day 1</span></div>
      <p>Questions the community keeps asking, how often, and how long each has gone unanswered.</p></div>"""

    gated7 = community_days < 7
    gated14 = community_days < 14
    who_talking = f'<span class="pend">day 7 &middot; {community_days}/7</span>' if gated7 else '<span class="card-meta">live</span>'
    coverage_gap = f'<span class="pend">day 7 &middot; {community_days}/7</span>' if gated7 else '<span class="card-meta">live</span>'
    momentum = f'<span class="pend">day 14 &middot; {community_days}/14</span>' if gated14 else '<span class="card-meta">live</span>'
    sentiment_time = f'<span class="pend">day 14 &middot; {community_days}/14</span>' if gated14 else '<span class="card-meta">live</span>'

    grok_section = ""
    if d["grok"]:
        g = d["grok"]["sentiment"]
        grok_rows = "".join(
            f'<tr><td>{w["week_start"]}&ndash;{w["week_end"][5:]}</td><td>{w["sampled_posts"]}</td>'
            f'<td>{fmt_pct(w["positive_pct"])}</td><td>{fmt_int(w["combined_engagement"])}</td></tr>'
            for w in d["grok_weeks"]
        )
        grok_top_rows = "".join(
            f'<li><span class="mini-list-val">{p["likes"]}&#9825;</span><span class="mini-list-label">@{esc(p["author_handle"])}: {esc(p["text_excerpt"][:70])}</span></li>'
            for p in d["grok_top"]
        )
        grok_section = f"""
  <section class="chart-card">
    <div class="card-head">
      <h4>Community spot-check &mdash; Grok manual pull</h4>
      <span class="card-meta">observed &middot; manual, periodic</span>
    </div>
    <p class="chart-note">A richer, larger-sample cross-check pulled by hand via Grok's live X
      access ({d['grok']['total_sampled_posts']} posts, {d['grok']['unique_authors_approx']} unique
      authors, {d['grok']['period_start']} &rarr; {d['grok']['period_end']}) &mdash;
      not the automated daily series above, and not blended with it. Manual because Grok's
      API access has a real per-call cost, against the standing $0 budget; free inside X
      Premium+ as an occasional check.</p>
    <div class="kpis">
      <div class="kpi"><span class="label">Our formula</span><span class="value">{g['our_sentiment_score']:.2f}</span><span class="hint">positive/(pos+neu+neg)</span></div>
      <div class="kpi"><span class="label">Grok's own score</span><span class="value">{g['grok_bullish_score']:.2f}</span><span class="hint">different formula, not blended</span></div>
    </div>
    <div class="tbl-wrap">
      <table class="mini-table">
        <thead><tr><th>Week</th><th>Posts</th><th>Positive</th><th>Engagement</th></tr></thead>
        <tbody>{grok_rows}</tbody>
      </table>
    </div>
    <p class="chart-note" style="margin-top:6px">Top engaged posts this period:</p>
    <ul class="mini-list">{grok_top_rows}</ul>
  </section>
"""

    webm_section = ""
    if d["webm_weeks"]:
        webm_week = d["webm_weeks"][-1]
        webm_n = len(d["webm_weeks"])
        per_q_rows = "".join(
            f'<li><span class="mini-list-val">{v["results_returned"]}</span><span class="mini-list-label">"{esc(q)}" &middot; {v["distinct_domains"]} domains'
            + (f' &middot; {v["filtered_out"]} filtered ({v.get("filter_note","")[:40]}...)' if v.get("filtered_out") else '')
            + '</span></li>'
            for q, v in webm_week["per_query"].items()
        )
        webm_section = f"""
  <section class="chart-card">
    <div class="card-head">
      <h4>General web presence</h4>
      <span class="card-meta">derived &middot; weak instrument</span>
    </div>
    <p class="chart-note">How visible "Telcoin"/"$TEL" is across the open web generally &mdash;
      a different question from social-platform mentions above. WebSearch-based (never a raw
      scraper against a search engine &mdash; see <code>scripts/web-mentions-scraper.md</code>
      for why). Weekly cadence; {webm_n} week{'s' if webm_n != 1 else ''} collected so far.</p>
    <div class="kpis">
      <div class="kpi"><span class="label">This week</span><span class="value">{webm_week['total_results_returned']}</span><span class="hint">indexed {webm_week['indexed_to_first_week']:.0f} vs. week 1</span></div>
    </div>
    <ul class="mini-list">{per_q_rows}</ul>
    {'<p class="chart-note">Trend line unlocks once more weeks accumulate &mdash; one point is a reading, not a trend.</p>' if webm_n < 4 else ''}
  </section>
"""

    restream_panel = """
      <div class="slot">
        <div class="slot-top"><h4>Stream analytics (Restream)</h4><span class="pend">not connected</span></div>
        <p>Built and tested (<code>scripts/restream_analytics_pull.py</code>, weekly GitHub Actions
          workflow) but needs a one-time OAuth connection before real data flows &mdash;
          see <code>infrastructure/n8n/README.md</code> for setup. Past-stream analytics only
          (viewer counts, aggregate chat stats); individual chat message text needs a separate,
          not-yet-built path.</p>
      </div>""" if not d["restream_live"] else """
      <div class="slot"><div class="slot-top"><h4>Stream analytics (Restream)</h4><span class="card-meta">live</span></div>
      <p>Per-event viewer and chat analytics now flowing &mdash; see campaign/analytics/restream/.</p></div>"""

    account_raw_json = json.dumps(d["account_raw"], indent=2)
    raw_json = json.dumps(d["raw"], indent=2)
    price_recent_json = json.dumps(d["price_recent"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>TEL Social Intelligence</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#090920;
  --panel:#101029;
  --panel-2:#14142f;
  --border:#22224a;
  --border-soft:#1b1b3d;
  --ink:#dfe2ff;
  --ink-dim:#9aa0cc;
  --muted:#6a719f;
  --tel:#14c8ff;
  --royal:#3642b2;
  --amber:#e0a33a;
  --pos:#199e70;
  --neg:#e66767;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",sans-serif;
  color-scheme:dark;
}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6;
  -webkit-font-smoothing:antialiased;
  background-image:radial-gradient(ellipse 80% 50% at 50% -10%,rgba(54,66,178,.22),transparent 70%)}}
.wrap{{max-width:1000px;margin:0 auto;padding:40px 20px 72px;display:flex;flex-direction:column;gap:28px}}

header{{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;
  padding-bottom:24px;border-bottom:1px solid var(--border)}}
.brand{{display:flex;flex-direction:column;gap:6px}}
h1{{font-size:1.5rem;font-weight:700;letter-spacing:-.01em;color:#fff;text-wrap:balance}}
.sub{{font-size:.82rem;color:var(--muted);font-family:var(--mono)}}
.status-chip{{display:inline-flex;align-items:center;gap:8px;background:rgba(20,200,255,.1);
  border:1px solid rgba(20,200,255,.4);color:var(--tel);
  padding:7px 14px;border-radius:999px;font-size:.75rem;font-weight:600;
  letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}}
.dot{{width:7px;height:7px;border-radius:50%;background:var(--tel);flex:none}}
.status-chip.warn{{background:rgba(224,163,58,.1);border-color:rgba(224,163,58,.4);color:var(--amber)}}
.status-chip.warn .dot{{background:var(--amber)}}
@media(prefers-reduced-motion:no-preference){{
  .dot{{animation:pulse 2.4s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
}}

.notice{{background:var(--panel);border:1px solid var(--border);
  border-left:3px solid var(--amber);border-radius:6px;padding:24px 26px;
  display:flex;flex-direction:column;gap:14px}}
.notice h2{{font-size:1rem;font-weight:650;color:#fff;letter-spacing:-.005em}}
.notice p{{font-size:.88rem;color:var(--ink-dim);max-width:68ch}}
.notice p strong{{color:var(--ink);font-weight:600}}

.progress-block{{display:flex;flex-direction:column;gap:10px;margin-top:4px}}
.progress-head{{display:flex;justify-content:space-between;align-items:baseline;font-size:.78rem;
  color:var(--muted);font-family:var(--mono);letter-spacing:.02em}}
.progress-head b{{color:var(--tel);font-size:1.05rem;font-variant-numeric:tabular-nums}}
.track{{height:6px;background:var(--panel-2);border:1px solid var(--border-soft);
  border-radius:3px;overflow:hidden;display:flex;gap:2px;padding:1px}}
.track i{{flex:1;background:var(--border);border-radius:1px}}
.track i.on{{background:var(--tel)}}

h3.sec{{font-size:.72rem;font-weight:650;color:var(--muted);text-transform:uppercase;
  letter-spacing:.12em;padding-bottom:10px;border-bottom:1px solid var(--border-soft)}}

.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}
.kpi{{background:var(--panel);border:1px solid var(--border-soft);border-radius:6px;padding:16px 18px;
  display:flex;flex-direction:column;gap:4px}}
.kpi .label{{font-size:.65rem;font-family:var(--mono);color:var(--muted);letter-spacing:.08em;text-transform:uppercase}}
.kpi .value{{font-size:1.35rem;font-weight:700;color:#fff;font-variant-numeric:tabular-nums;letter-spacing:-.02em}}
.kpi .hint{{font-size:.72rem;color:var(--ink-dim)}}

.chart-card{{background:var(--panel);border:1px solid var(--border);border-radius:6px;padding:22px 24px;
  display:flex;flex-direction:column;gap:16px}}
.chart-card .card-head{{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}}
.chart-card h4{{font-size:.95rem;font-weight:650;color:#fff}}
.chart-card .card-meta{{font-size:.72rem;font-family:var(--mono);color:var(--muted)}}
.chart-note{{font-size:.8rem;color:var(--ink-dim);max-width:70ch}}
#imp-chart,#eng-chart,.line-chart{{width:100%;height:160px;display:block}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;font-size:.72rem;font-family:var(--mono);color:var(--muted)}}
.legend span{{display:inline-flex;align-items:center;gap:6px}}
.legend i{{width:10px;height:10px;border-radius:2px;display:inline-block}}
.legend .imp{{background:var(--tel)}}
.legend .eng{{background:var(--pos)}}

.mini-list{{list-style:none;display:flex;flex-direction:column;gap:6px}}
.mini-list li{{display:flex;gap:10px;font-size:.82rem;color:var(--ink-dim);align-items:baseline}}
.mini-list-val{{font-family:var(--mono);color:var(--tel);font-weight:600;flex:none;min-width:52px;text-align:right}}
.mini-list-label{{color:var(--ink-dim)}}

.tbl-wrap{{overflow-x:auto}}
.mini-table{{width:100%;border-collapse:collapse;font-size:.8rem}}
.mini-table th{{text-align:left;font-family:var(--mono);font-size:.65rem;letter-spacing:.06em;
  text-transform:uppercase;color:var(--muted);padding:6px 10px;border-bottom:1px solid var(--border-soft)}}
.mini-table td{{padding:7px 10px;border-bottom:1px solid var(--border-soft);color:var(--ink-dim)}}

.ledger{{display:flex;flex-direction:column;gap:8px;margin-top:6px}}
.ledger-row{{display:grid;grid-template-columns:120px 1fr 32px;gap:10px;align-items:center;font-size:.8rem}}
.ledger-row.listen-only .ledger-label{{color:var(--muted)}}
.ledger-row.listen-only .ledger-label::after{{content:" \\1F441";font-size:.7em}}
.ledger-label{{color:var(--ink-dim)}}
.ledger-bar-track{{height:8px;background:var(--panel-2);border-radius:3px;overflow:hidden}}
.ledger-bar{{display:block;height:100%;background:var(--tel);border-radius:3px}}
.ledger-count{{font-family:var(--mono);color:var(--ink);text-align:right}}

.q-list{{display:flex;flex-direction:column;gap:8px;margin-top:6px}}
.q-row{{display:flex;flex-direction:column;gap:2px;padding:8px 0;border-bottom:1px solid var(--border-soft)}}
.q-row:last-child{{border-bottom:none}}
.q-text{{font-size:.83rem;color:var(--ink)}}
.q-meta{{font-size:.7rem;font-family:var(--mono);color:var(--muted)}}

.tiers{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:1px;
  background:var(--border-soft);border:1px solid var(--border-soft);border-radius:6px;overflow:hidden}}
.tier{{background:var(--panel);padding:18px 20px;display:flex;flex-direction:column;gap:7px}}
.tier-key{{display:flex;align-items:center;gap:9px}}
.swatch{{width:26px;height:14px;border-radius:2px;flex:none}}
.s-t1{{background:var(--tel)}}
.s-t2{{background:transparent;border:1.5px solid var(--tel)}}
.s-t3{{background:repeating-linear-gradient(45deg,var(--royal) 0 3px,transparent 3px 6px);
  border:1px solid var(--royal)}}
.s-t0{{background:var(--panel-2);border:1px dashed var(--muted)}}
.tier-name{{font-size:.73rem;font-weight:700;letter-spacing:.09em;font-family:var(--mono);color:var(--ink)}}
.tier p{{font-size:.79rem;color:var(--muted);line-height:1.5}}

.panels{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:12px}}
.slot{{background:var(--panel);border:1px solid var(--border-soft);border-radius:6px;
  padding:18px 20px;display:flex;flex-direction:column;gap:8px;min-height:112px}}
.slot-top{{display:flex;justify-content:space-between;align-items:center;gap:12px}}
.slot h4{{font-size:.88rem;font-weight:640;color:var(--ink)}}
.pend{{font-size:.62rem;font-family:var(--mono);color:var(--muted);border:1px solid var(--border);
  padding:2px 7px;border-radius:3px;letter-spacing:.06em;white-space:nowrap}}
.slot p{{font-size:.79rem;color:var(--muted);line-height:1.5}}
.slot.lead{{border-color:var(--royal);background:linear-gradient(var(--panel),var(--panel)) padding-box,
  linear-gradient(150deg,var(--royal),transparent 60%) border-box;border:1px solid transparent}}
.slot.lead h4{{color:var(--tel)}}
.slot.wide{{grid-column:1 / -1}}

.method{{background:var(--panel);border:1px solid var(--border-soft);border-radius:6px;padding:24px 26px;
  display:flex;flex-direction:column;gap:18px}}
.method-row{{display:flex;flex-direction:column;gap:5px}}
.method-row dt{{font-size:.7rem;font-family:var(--mono);color:var(--tel);letter-spacing:.08em;
  text-transform:uppercase}}
.method-row dd{{font-size:.85rem;color:var(--ink-dim);max-width:70ch}}
.method-row dd b{{color:var(--ink);font-weight:600}}

footer{{font-size:.74rem;color:var(--muted);font-family:var(--mono);line-height:1.7;
  padding-top:20px;border-top:1px solid var(--border-soft)}}
@media(max-width:620px){{.wrap{{padding:28px 16px 48px}}h1{{font-size:1.3rem}}}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand">
      <h1>TEL Social Intelligence</h1>
      <p class="sub">Telcoin Association &middot; community listening + @telcoinTAO measured performance + market context</p>
    </div>
    <span class="status-chip"><span class="dot"></span>{status_text}</span>
  </header>

  <section>
    <h3 class="sec">@telcoinTAO measured account performance (X)</h3>
    <p class="chart-note" style="margin-bottom:14px">
      Source: analytics.x.com <strong>Account Overview</strong> export. Tier: <strong>MEASURED</strong>.
      Day totals only &mdash; per-post permalinks need a Tweet-activity (Export by Tweet) CSV.
    </p>
    <div class="kpis">{account_kpis}
    </div>
  </section>

  <section class="chart-card">
    <div class="card-head">
      <h4>Daily impressions</h4>
      <span class="card-meta">measured &middot; account overview</span>
    </div>
    <svg id="imp-chart" viewBox="0 0 960 160" preserveAspectRatio="none" role="img" aria-label="Daily impressions bar chart"></svg>
    <div class="legend"><span><i class="imp"></i>Impressions</span></div>
  </section>

  <section class="chart-card">
    <div class="card-head">
      <h4>Daily engagements</h4>
      <span class="card-meta">measured &middot; account overview</span>
    </div>
    <svg id="eng-chart" viewBox="0 0 960 160" preserveAspectRatio="none" role="img" aria-label="Daily engagements bar chart"></svg>
    <div class="legend"><span><i class="eng"></i>Engagements</span></div>
  </section>
{yt_section}
{price_section}
  <section class="notice">
    <h2>Community listening (X/Reddit/news) &mdash; still collecting</h2>
    <p>
      Trend panels (sentiment over time, narrative momentum) stay locked until fourteen
      <strong>measured</strong> community days accumulate. Narrative ledger and open questions
      unlock at day 1 and are live below. Synthetic seed data stays quarantined.
    </p>
    <div class="progress-block">
      <div class="progress-head"><span>Verified community days collected</span><b>{community_days} / 14</b></div>
      <div class="track">{"".join('<i class="on"></i>' if i < community_days else '<i></i>' for i in range(14))}</div>
    </div>
    <p class="chart-note" style="margin-top:14px">
      {notice_lines}
    </p>
  </section>

  <section>
    <h3 class="sec">How to read every number here</h3>
    <div class="tiers">
      <div class="tier">
        <div class="tier-key"><span class="swatch s-t1"></span><span class="tier-name">MEASURED</span></div>
        <p>Reported by the platform's own analytics for an account we control. Our post impressions, engagements, link clicks.</p>
      </div>
      <div class="tier">
        <div class="tier-key"><span class="swatch s-t2"></span><span class="tier-name">OBSERVED</span></div>
        <p>Counts visible on a third-party post we actually saw. A sample of the conversation, never a census of it.</p>
      </div>
      <div class="tier">
        <div class="tier-key"><span class="swatch s-t3"></span><span class="tier-name">DERIVED</span></div>
        <p>Calculated from the two above by a stated formula. Always shown with a range or an approximation mark.</p>
      </div>
      <div class="tier">
        <div class="tier-key"><span class="swatch s-t0"></span><span class="tier-name">UNAVAILABLE</span></div>
        <p>Known gaps, drawn as gaps. An unknown is never quietly rendered as a zero.</p>
      </div>
    </div>
  </section>

  <section>
    <h3 class="sec">Community panels</h3>
    <div class="panels">{narrative_ledger_panel}
{open_questions_panel}
      <div class="slot">
        <div class="slot-top"><h4>Coverage gap</h4>{coverage_gap}</div>
        <p>Where community attention and our published output diverge, in either direction.</p>
      </div>
      <div class="slot">
        <div class="slot-top"><h4>Narrative momentum</h4>{momentum}</div>
        <p>Which subjects are rising, steady, or fading against the prior seven days.</p>
      </div>
      <div class="slot">
        <div class="slot-top"><h4>Sentiment over time</h4>{sentiment_time}</div>
        <p>Daily positive share with its sample size. Thin days are shaded rather than drawn as confident points.</p>
      </div>
      <div class="slot">
        <div class="slot-top"><h4>Who is talking</h4>{who_talking}</div>
        <p>Unique authors and concentration &mdash; whether a reading reflects a broad community or a handful of accounts.</p>
      </div>
{restream_panel}
    </div>
  </section>
{grok_section}
{webm_section}
  <section class="method">
    <h3 class="sec">What this can and cannot see</h3>
    <div class="method-row">
      <dt>The hard limit</dt>
      <dd>Impressions and reach describe <b>our own posts only</b>. For everyone else's posts we
        report conversation volume from an observed sample. Link clicks and profile clicks on a
        third party's post are not obtainable at any price, and are never estimated here.</dd>
    </div>
    <div class="method-row">
      <dt>Sample, not census</dt>
      <dd>Community collection runs on public search, which returns a portion of the conversation
        rather than all of it. Every community figure carries its sample size. Treat direction and
        change as meaningful; treat absolute totals as a floor.</dd>
    </div>
    <div class="method-row">
      <dt>Sources</dt>
      <dd>X/Twitter, Reddit, and crypto news outlets for daily community signal (WebSearch); a
        periodic manual Grok spot-check for a larger sample; general web presence (WebSearch,
        no site restriction). Our own performance: X native analytics (Account Overview / Tweet
        activity) and the YouTube Data API. Market context: CoinGecko. Stream analytics: Restream
        (built, not yet connected).</dd>
    </div>
    <div class="method-row">
      <dt>Classification</dt>
      <dd>Each post is read and tagged for sentiment and subject against a fixed taxonomy. Subjects
        the Association does not publish on, such as price and banking, are tracked for listening
        and marked accordingly (&#128065; in the narrative ledger) &mdash; they never generate a
        recommendation to publish.</dd>
    </div>
    <div class="method-row">
      <dt>Deliberately absent</dt>
      <dd>No single composite score. A blended 0&ndash;10 number hides which input moved and cannot
        be audited, and this page is read by people who will act on it. Grok's own "bullish score"
        is shown alongside this pipeline's formula, never merged into it.</dd>
    </div>
  </section>

  <footer>
    Telcoin Association &middot; Autonomous Ops<br>
    Source records: <code>campaign/analytics/sentiment/</code> (community + own-account),
    <code>account-overview/</code>, <code>market/</code>, <code>community-grok/</code>,
    <code>web-mentions/</code>, <code>youtube/</code>, <code>restream/</code><br>
    Withdrawn data retained under <code>_seed-synthetic/</code> with full provenance.
  </footer>
</div>

<script>
/*
  Compiled from every source file under campaign/analytics/ by scripts/build-dashboard.py.
  ACCOUNT_RAW/RAW drive the two bar charts and community panels below; PRICE_RECENT drives
  the price line chart. Never hand-edit these blocks - re-run the build script instead.
*/
const ACCOUNT_RAW = {account_raw_json};
const RAW = {raw_json};
const PRICE_RECENT = {price_recent_json};
window.__TEL_ACCOUNT_RAW__ = ACCOUNT_RAW;
window.__TEL_SENTIMENT_RAW__ = RAW;
window.__TEL_PRICE_RAW__ = PRICE_RECENT;

(function renderAccountCharts(){{
  function bars(svgId, key, color){{
    const svg = document.getElementById(svgId);
    if (!svg || !ACCOUNT_RAW.length) return;
    const W = 960, H = 160, padT = 12, padB = 28, padL = 8, padR = 8;
    const innerW = W - padL - padR, innerH = H - padT - padB;
    const vals = ACCOUNT_RAW.map(d => Number(d[key] || 0));
    const max = Math.max(...vals, 1);
    const n = vals.length;
    const gap = 2;
    const bw = Math.max(2, (innerW - gap * (n - 1)) / n);
    let out = '';
    vals.forEach((v, i) => {{
      const h = (v / max) * innerH;
      const x = padL + i * (bw + gap);
      const y = padT + (innerH - h);
      out += `<rect x="${{x.toFixed(2)}}" y="${{y.toFixed(2)}}" width="${{bw.toFixed(2)}}" height="${{h.toFixed(2)}}" fill="${{color}}" opacity="0.9"><title>${{ACCOUNT_RAW[i].date}}: ${{v.toLocaleString()}}</title></rect>`;
    }});
    const labelIdx = [0, Math.floor((n-1)/2), n-1];
    labelIdx.forEach(i => {{
      const x = padL + i * (bw + gap) + bw/2;
      out += `<text x="${{x.toFixed(1)}}" y="${{H-8}}" text-anchor="middle" fill="#6a719f" font-size="10" font-family="ui-monospace,monospace">${{ACCOUNT_RAW[i].date.slice(5)}}</text>`;
    }});
    svg.innerHTML = out;
  }}
  bars('imp-chart', 'impressions', '#14c8ff');
  bars('eng-chart', 'engagements', '#199e70');
}})();
</script>
</body>
</html>
"""


def main():
    data = gather()
    out = build_html(data)
    OUT.write_text(out)
    print(f"wrote {OUT}, {len(out):,} bytes")
    print(f"  account days: {len(data['account_raw'])}")
    print(f"  community measured days: {data['community_days']}")
    print(f"  narrative ledger entries: {len(data['ledger_rows'])}")
    print(f"  open questions: {len(data['open_questions'])}")
    print(f"  price recent window: {len(data['price_recent'])} of {data['price_n_days']} total days")
    print(f"  grok weeks: {len(data['grok_weeks']) if data['grok_weeks'] else 0}")
    print(f"  web-mentions weeks: {len(data['webm_weeks'])}")
    print(f"  youtube: {'yes' if data['yt'] else 'no'}")
    print(f"  restream live: {data['restream_live']}")


if __name__ == "__main__":
    main()
