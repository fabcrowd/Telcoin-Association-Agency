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
