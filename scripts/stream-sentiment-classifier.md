# Stream Chat Sentiment Classifier

Fills in sentiment classification on Restream council-stream chat that the n8n workflow
(`infrastructure/n8n/workflow-restream-to-github.json`) already captured but deliberately left
unclassified. Same division of labor as the Fellow transcript pipeline: n8n ingests raw data and
commits it; a Claude session enriches it with real judgment. n8n has no LLM call in it and none
should be added there — that would need a paid API key, against the standing $0 budget
(`campaign/AGENCY-MEMORY.md`). This routine uses the Claude session already running instead, at no
incremental cost.

**Trigger**: run this whenever new files exist under `campaign/analytics/streams/` with any message
carrying `sentiment: null`. Check for this at session start alongside the other Phase 0 ingestion
steps (Fellow transcripts, etc.) — do not wait for the user to ask.

## Step 1 — Find unclassified files

```bash
for f in campaign/analytics/streams/*.json; do
  python3 -c "
import json,sys
d = json.load(open('$f'))
unclassified = sum(1 for m in d.get('messages', []) if m.get('sentiment') is None)
if unclassified:
    print(f'$f: {unclassified} unclassified message(s)')
"
done
```

If nothing prints, there is nothing to do — stop here.

## Step 2 — Classify each message

For every message with `sentiment: null`, read `text` and classify using the **same sentiment
rules as `scripts/sentiment-scraper.md`** (do not invent a separate standard):

- **Positive**: price optimism, milestone celebration, technical achievement praise, project
  support, "bullish", governance approval
- **Negative**: price frustration, FUD, project criticism, "wen", "dead", governance dissatisfaction
- **Neutral**: factual questions, observations without opinion, procedural governance comments

Set `sentiment_confidence: "low"` when the message is too short/ambiguous to judge confidently
(a single emoji, "gm", a bare link).

Tag `narratives` against `campaign/analytics/NARRATIVE-TAXONOMY.json`, exactly as the sentiment
scraper does for community posts — every message lands on at least one narrative; use `other`
rather than dropping one.

This is a **live governance chat, not a search sample** — every message is present (the workflow's
`coverage: "census"`), so there is no sampling caveat to attach, but the honesty rules are
otherwise identical: never guess a value, never coerce absent data to zero, never fabricate a
classification for a message whose text is empty or unintelligible (leave `sentiment: null` with a
one-line reason in that case — a stuck classification is more honest than a guessed one).

## Step 3 — Fold questions into the ledger

Every message with `is_question: true` follows the **same ledger procedure as
`scripts/sentiment-scraper.md` Step 3b**: canonicalize, check the most recent prior ledger entry
(community `questions[]` files and this stream's own event carry separate ledgers — do not merge
them; a governance question asked live during a council stream is a different signal than one
asked cold on X), increment `times_observed` on a match, add new otherwise.

## Step 4 — Compute the event composite and write back

Add to the file (alongside the existing `event`/`viewers`/`messages` fields):

```json
"composite": {
  "total_messages": 0,
  "n_classified": 0,
  "sentiment_score": 0.0,
  "top_narrative": null,
  "questions_asked": 0,
  "questions_answered_live": 0
}
```

Same formula as the rest of the pipeline: `sentiment_score = positive / (positive + neutral +
negative)`, always paired with `n_classified`. `top_narrative` only when the leader clears second
place by more than sampling noise — same rule, even though this is a census not a sample; a
council chat can still be dominated by one or two vocal accounts.

Validate before writing:
```bash
python3 - "$FILE" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
tax = {n["id"] for n in json.load(open("campaign/analytics/NARRATIVE-TAXONOMY.json"))["narratives"]}
classified = [m for m in d["messages"] if m.get("sentiment") is not None]
c = d["composite"]
assert c["n_classified"] == len(classified), "n_classified must match actually-classified messages"
for m in classified:
    assert set(m["narratives"]) <= tax, f"unknown narrative on message {m['id']}"
    assert m["narratives"], f"classified message {m['id']} has no narrative tag"
print(f"OK - {d['event']['event_id']}: {len(classified)}/{len(d['messages'])} classified")
PY
```

## Step 5 — Commit and push

```bash
git add campaign/analytics/streams/
git commit -m "Classify stream chat sentiment: <event title>"
git push origin claude/campaign-iLgt5
```

---

**Activation is separate from this.** This routine only runs once real files exist under
`campaign/analytics/streams/`, which requires the n8n workflow itself to be live. That workflow is
currently **inactive** and unverified — see `infrastructure/n8n/README.md`'s existing
`VERIFY_BEFORE_ACTIVATING` checklist (API base URL, response field shapes, whether Restream access
needs a paid tier, chat retention window). Activating an n8n instance and connecting real Restream
OAuth credentials happens on the user's own infrastructure — not something this Claude session has
access to do directly.
