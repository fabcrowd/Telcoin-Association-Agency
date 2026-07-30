# n8n Pipelines

Two workflows commit to this repo. Both follow the same shape — *external source → format →
GitHub commit → next Claude session ingests* — and both keep credentials inside n8n's encrypted
store, never in the repo.

| Workflow | File | Purpose |
|---|---|---|
| Fellow transcripts | `workflow-fellow-to-github.json` | Council meeting notes → `campaign/research/transcripts/` |
| YouTube stats | `workflow-youtube-to-github.json` | Daily channel statistics → `campaign/analytics/youtube/` |

---

## YouTube Channel Stats (`PROD-YOUTUBE-ChannelStats-Pull-v1.0`)

Pulls exact view, like and comment counts for every @TelcoinTAO video once a day and commits them
as JSON. This replaces a `WebFetch` of the channel page that returned 403 every day from March
onward — a user-agent artifact, not a block. Statistics are pulled from the API rather than the
page because YouTube now renders them client-side through a `lockupViewModel`: video IDs still
parse, view counts do not, and the parse fails *silently* when the markup shifts.

**Setup**

1. **API key** — at `console.cloud.google.com`, enable **YouTube Data API v3** and create a key
   **restricted to that single API**. Read-only, free, revocable, cannot post.
2. In n8n: **Credentials → New → Query Auth**, name it `YouTube Data API Key`, set
   Name = `key` and Value = your key.
3. Reuse the existing `GitHub API` credential from the Fellow workflow.
4. **Workflows → Import from file** → `workflow-youtube-to-github.json`.
5. **Reconnect both credentials** — the IDs in the JSON are `REPLACE_ME` placeholders.
6. Save, then activate.

**Quota.** About 4 units per run (2 + one per 50 videos) against a free 10,000/day allowance.
`search.list` is deliberately unused; it costs 100 units for the same result. The workflow aborts
if spend passes 100 units, which would mean something is looping.

**Guarantees.** Writing to a dated path makes re-runs idempotent — a second run overwrites the day
rather than duplicating it. Every external call has an error branch that classifies the failure
and **writes nothing**: a missing day is recoverable, a day of zeros entering the trend line is
not. A reconciliation invariant (`requested == returned`) refuses partial pulls, and absent
metrics are stored as `null`, never `0` — a channel hiding likes is not zero likes.

**Manual fallback.** `python3 scripts/youtube-pull.py` performs the same pull with the same guards
and the same output shape. Use it to backfill or to test before activating the workflow. It reads
`YOUTUBE_API_KEY` from the environment and exits 1 with instructions if unset.

**Re-audit** when the API version or quota changes, the error rate rises, video count grows enough
to change the batch count, or repeated manual fixes appear.

---

# Fellow AI → GitHub Transcript Pipeline

Automates the delivery of Fellow AI meeting notes into this repository.
When a council meeting ends, a note is sent to GitHub via Zapier (one click)
or automatically via n8n webhook. The transcript lands in
`campaign/research/transcripts/` and is ingested automatically at the next
Claude session start via Phase 0D of `daily-agency-run.md`.

---

## Option A — Zapier (active, one click per meeting)

**Status: Live** — Zap ID 356663879 configured and published.

After each council meeting:
1. Open the Fellow note
2. Click **Share → Send → Send via Zapier**
3. Done — transcript commits to the repo within seconds

No Fellow API key required. Uses Zapier's native Fellow OAuth integration.

**Zap flow**: Fellow "Note Sent to Zapier" → GitHub "Create or Update File" → `campaign/research/transcripts/`

---

## Option B — n8n (fully automatic, requires Fellow paid plan)

When upgraded to a Fellow paid plan (Team $7/user/mo+), the n8n webhook path
eliminates the manual click. Fellow fires the webhook automatically when the
AI note generates (~5-10 min after meeting end). See setup steps below.

---

## How It Works

```
Meeting ends
    ↓
Fellow generates AI note (~5-10 min)
    ↓
Fellow fires webhook to n8n
    ↓
n8n Code node formats content as markdown
    ↓
n8n GitHub node commits to campaign/research/transcripts/
    ↓
Next Claude session: Phase 0D ingests file → updates TELCOIN-RESEARCH.md → moves to processed/
```

---

## Prerequisites

- **Fellow paid plan** (Team $7/user/mo minimum — free plan has no API access)
- **Docker** installed on your machine or server
- **Publicly reachable URL** for n8n — Fellow must be able to POST to it
- **GitHub Personal Access Token** with `repo` scope

---

## Step 1 — Get a Public URL for n8n

n8n's webhook listener must be reachable from Fellow's servers.

**Option A — ngrok (local dev, free)**

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5678
# Copy the https://xxxx.ngrok-free.app URL — use it as N8N_WEBHOOK_URL below
```

Ngrok free URLs change on restart. For a stable URL, use a paid ngrok plan or Option B.

**Option B — Run on a server (production)**

Deploy this directory on any VPS (Hetzner, DigitalOcean, Render, Railway).
Use your server's domain as `N8N_WEBHOOK_URL`.

---

## Step 2 — Configure Environment

```bash
cd infrastructure/n8n
cp .env.example .env
```

Edit `.env`:

```
N8N_ENCRYPTION_KEY=    # run: openssl rand -hex 32
N8N_WEBHOOK_URL=       # your ngrok or server URL (trailing slash required)
```

Never commit `.env` — it is gitignored.

---

## Step 3 — Start n8n

```bash
cd infrastructure/n8n
docker compose up -d
```

Open `http://localhost:5678` and complete the initial account setup.

---

## Step 4 — Install the Fellow Community Node

1. In n8n: **Settings → Community Nodes → Install**
2. Package name (exact, scoped): `@fellow/n8n-nodes-fellow`
3. Check the risk acknowledgment → click **Install**
4. n8n restarts automatically (~30 seconds)

---

## Step 5 — Add Credentials

### Fellow API credential

1. In Fellow: **avatar → Settings → API, MCP & Webhooks → Generate key**
   - Note: a workspace admin must first enable API access in **Workspace Settings → Security**
2. In n8n: **Credentials → New → search "Fellow API"**
   - Subdomain: your workspace prefix (e.g. `acme` from `acme.fellow.app`)
   - API Key: the key you just generated
3. Save

### GitHub API credential

1. On GitHub: **Settings → Developer settings → Personal access tokens → Tokens (classic)**
   - Generate new token → select `repo` scope → copy it
2. In n8n: **Credentials → New → search "GitHub API"**
   - Access Token: your PAT
   - Username: your GitHub username
3. Save

---

## Step 6 — Import the Workflow

1. In n8n: **Workflows → ⋯ → Import from file**
2. Select `workflow-fellow-to-github.json` from this directory
3. The workflow opens with 3 nodes: Fellow Trigger → Format as Markdown → Commit to GitHub

**Reconnect credentials** (required after import — credential IDs in the JSON are placeholders):

- Click **Fellow Trigger** → Credentials → select your "Fellow API" credential
- Click **Commit to GitHub** → Credentials → select your "GitHub API" credential

4. Click **Save** (top right)
5. **Activate the workflow** — toggle the "Active" switch top right

---

## Step 7 — Verify Webhook Registration

After activating, n8n registers a webhook with Fellow automatically.

To confirm:
1. In Fellow: **avatar → Settings → API, MCP & Webhooks**
2. You should see an active webhook entry pointing to your n8n URL
3. If nothing appears, check the n8n execution log for errors

---

## Step 8 — Test It

**Manual test (no Fellow meeting required):**

```bash
# Create a dummy transcript in the repo
echo "# Test Meeting\n**Date**: $(date +%Y-%m-%d)\n\nThis is a test transcript." \
  > campaign/research/transcripts/$(date +%Y-%m-%d)-test.md
git add campaign/research/transcripts/
git commit -m "test: add dummy transcript for Phase 0D"
git push origin claude/campaign-iLgt5
```

Start a new Claude session. Phase 0D will:
1. Detect the file in `transcripts/`
2. Extract intel and update `TELCOIN-RESEARCH.md`
3. Move the file to `transcripts/processed/`

**Live test:**

Run any council meeting with Fellow recording active. After the meeting:
- Wait 5-15 minutes for Fellow to generate the AI note
- Check the repo: `git pull && ls campaign/research/transcripts/`
- A `.md` file with today's date should appear

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Fellow node not found after install | Restart n8n: `docker compose restart` |
| Webhook not registering | Confirm `N8N_WEBHOOK_URL` is publicly reachable; test with `curl $N8N_WEBHOOK_URL` |
| "AI Note Generated" never fires | Check Fellow plan includes API; check admin enabled API in Workspace Settings |
| Transcript payload missing transcript text | Check n8n execution log for raw payload — Fellow may send note ID only; see note below |
| GitHub commit fails | Verify PAT has `repo` scope; confirm branch name matches |
| Ngrok URL changed | Update `N8N_WEBHOOK_URL` in `.env` and restart: `docker compose down && docker compose up -d` |
| Zapier commits files to nested subdirectories | See fix below |

### Fix: Zapier file path format

**Symptom**: Transcripts land at `campaign/research/transcripts/03/28/26 06:08PM-Title.md` instead of `campaign/research/transcripts/2026-03-28-title.md`. Zapier's default date token (`{{zap_meta_human_now}}`) outputs `MM/DD/YY HH:MMam` — the slashes become directory separators in the GitHub file path.

**Fix** (do this in the Zapier editor):

1. Open the Zap: https://zapier.com/editor/356663879
2. Click the **GitHub — Create or Update File** step
3. Find the **File Path** field
4. Replace the current value with:
   ```
   campaign/research/transcripts/{{zap_meta_human_now|date:Y-m-d}}-{{1__title|lower|replace: ,:_|replace: ,:_}}.md
   ```
   Or use a **Formatter by Zapier** step before the GitHub step:
   - Action: Text → Format → set `{{zap_meta_human_now}}` with format `YYYY-MM-DD`
   - Use the output as the date prefix in the file path
5. Save and re-publish the Zap
6. Test by sending a note — verify the file path in the resulting GitHub commit

The simplest reliable value for the File Path field:
```
campaign/research/transcripts/{{zap_meta_human_now|date:Y-m-d}}-fellow-note.md
```
This produces `campaign/research/transcripts/2026-03-29-fellow-note.md` — flat, unambiguous, Phase 0D will find it.

### Note on transcript payload content

The webhook payload structure is not fully documented by Fellow. If the `aiNoteGenerated` payload contains only a note ID (not full text), the Format as Markdown node's fallback (`Raw Payload` section) will still commit the JSON. Phase 0D can parse it.

If you need to confirm what Fellow sends, check the n8n execution log after the first live meeting: **Executions → click the run → Fellow Trigger → Output tab**.

---

## File Locations in This Repo

```
infrastructure/n8n/
  docker-compose.yml              — Docker setup for n8n
  .env.example                    — Environment variable template (copy to .env)
  workflow-fellow-to-github.json  — Importable n8n workflow
  README.md                       — This file

campaign/research/transcripts/
  [YYYY-MM-DD]-[meeting].md       — Unprocessed (Phase 0D reads these)
  processed/                      — Moved here after TELCOIN-RESEARCH.md update
```

---

## Updating the Workflow

If the workflow needs changes (different branch, different repo path, formatting changes):

1. Edit in n8n GUI → make changes → Save
2. Export: **⋯ → Download** → overwrite `workflow-fellow-to-github.json`
3. Commit the updated JSON to the repo
