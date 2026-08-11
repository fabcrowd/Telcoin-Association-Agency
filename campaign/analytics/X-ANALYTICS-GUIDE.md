# X Analytics Export Guide
## How to Feed Performance Data Into the Agency

This guide explains what to pull from X Analytics and how to paste it into `PERFORMANCE-LOG.md` so agents can use it to refine strategy.

---

## Where to Find Your Analytics

**URL**: analytics.twitter.com (must be logged into @telcoinTAO)

If you don't see analytics.twitter.com, use: X → Profile → More → Creator Studio → Analytics

---

## What to Export Weekly (5 minutes, every Friday or Monday)

### 1. Account Overview (monthly snapshot)
Found on the main analytics dashboard. Capture:
- Total impressions for the period
- Profile visits
- New followers
- Mentions

### 2. Individual Tweet Performance
Found under: Tweets tab → select date range → last 7 days

For each post, note:
- Date / time published
- Impressions
- Engagements
- Engagement rate
- Link clicks (if post had a link)
- Detail expands (a proxy for "read more" interest)

**You do not need to export every post.** Prioritize:
- Any post with unusually high or low impressions relative to recent average
- Posts where you ran the 60-minute launch window
- Governance notices (to understand if Tier 1 posts generate profile visits)
- Threads (to compare multi-tweet vs single tweet performance)

### 3. Top Tweet of the Week
X Analytics surfaces this automatically. Always capture the top post — note what type it was and why you think it performed.

---

## How to Paste Into PERFORMANCE-LOG.md

Open `campaign/analytics/PERFORMANCE-LOG.md` and add rows to the Weekly Performance Log table.

Example row format:
```
| 2026-03-27 | Education | GSMA $2T mobile money | 4,200 | 187 | 4.5% | 43 | Strong first hour |
```

Then update:
- Top Performers if any post beats the running best
- Format Performance Patterns if you have enough data to average by format
- Audience Response Patterns with any observations

---

## How Often

**Minimum**: Once per week (ideally Monday morning, covering the prior week)
**Ideal**: After every priority post (milestone, key education) — update within 48h while the launch window data is fresh

---

## What Agents Do With This Data

During every standup and content production session, agents read `PERFORMANCE-LOG.md` and:

- Prefer formats with higher average engagement rates
- Lean toward topics and framings that historically drive replies
- Avoid angles or structures that consistently underperform
- Adjust conversation prompt strategy based on which prompts generate substantive replies
- Flag if the log is stale (>7 days) so you know to update it

---

## Sentiment Tracking (X Community)

Separate from your account analytics, agents also run targeted searches for community $TEL sentiment during each session. This is done via 2-3 direct searches in the main session context — not via a subagent — to avoid rate limits.

Searches run each session:
- `$TEL Telcoin` (recent posts, last 24-48h)
- `@telcoinTAO` (mentions and replies)
- `Telcoin Network testnet` or other topical term based on what's active

Results are synthesized into the daily briefing. If the community is asking a question we haven't answered — it becomes content that day.

---

## Optional: X API for Programmatic Search

If you want deeper search access (more than 2-3 results per query, historical data), X Basic API at $100/month can be wired in as an MCP server. This would let agents pull actual tweets with engagement counts rather than relying on search snippets.

To set this up: create developer account at developer.twitter.com, generate API keys, and we add the MCP server config to `.mcp.json`. Ask the agency to configure this when ready.
