# $TEL community sentiment — Grok manual pulls

Periodic manual spot-checks of $TEL/Telcoin discussion on X, pulled by the user
via Grok inside X Premium+ (real live access to X's post index — better sample
size and real engagement/dates than this pipeline's WebSearch-based scraper can
get on its own).

**Not automated, by design.** Grok chat inside X Premium+ has no API access
included, and the automatable equivalent — xAI's separate developer API with a
live X-search tool (~$5/1,000 calls) — was evaluated and parked against the
user's $0 budget (`campaign/AGENCY-MEMORY.md`). Treat a new file landing here
the same way as an `analytics.x.com` CSV export: a welcome, occasional, manual
top-up, not a standing pipeline a script keeps current.

**One file per pull**, named `<period_start>_to_<period_end>.json`. Each file
is self-contained: overall summary, weekly breakdown (real weekly windows, never
disaggregated into fake daily numbers — the source data doesn't have daily
granularity, and inventing it would repeat the exact mistake `tasks/lessons.md`
Lesson 11 quarantined data for), and a top-posts list with real dates/authors/
engagement (no permalinks — Grok didn't report them, so `url` stays `null`
rather than guessed).

**Tier: `observed`**, same as the rest of this pipeline's community layer — a
sample of engaged/visible discussion, not a census. Grok's own reported
`bullish_score` is kept separate from this pipeline's standard
`positive/(positive+neutral+negative)` formula (`our_sentiment_score`) — they're
different formulas and will disagree; that's expected, not an error.

Weekly `narrative_tags_best_effort` are this session's own interpretation of
Grok's free-text themes against `campaign/analytics/NARRATIVE-TAXONOMY.json` —
Grok did not classify narratives itself. Treat as approximate context.

Not yet wired into `dashboard.html` — that file was substantially rewritten by
a separate concurrent session; wiring this in is a deliberate next step, not
done automatically here.
