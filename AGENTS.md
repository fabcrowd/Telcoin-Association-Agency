# AGENTS.md

## Cursor Cloud specific instructions

This repo ("The Agency") is a curated collection of Markdown AI-agent definitions under category dirs
(`design/`, `engineering/`, `marketing/`, `product/`, `testing/`, etc.). Each agent file starts with YAML
frontmatter (`name`, `description`, `color`) followed by the agent body. There is **no compiled application
and no language/package runtime** — the tooling is three Bash scripts and relies only on `bash` plus standard
coreutils (`awk`, `sed`, `grep`, `find`, `tr`, `mktemp`), all preinstalled. Nothing needs to be installed.

The three scripts (see their header comments for full usage) act as the lint/build/run surface:

- Lint / test: `./scripts/lint-agents.sh` — validates frontmatter + structure across all agent dirs.
- Build: `./scripts/convert.sh` — regenerates tool-specific integration files into `integrations/<tool>/`.
- Run / install: `./scripts/install.sh` — copies converted agents into a tool's config location.

Non-obvious gotchas:

- `lint-agents.sh` exits non-zero only on ERRORs (missing frontmatter delimiter/fields). "WARN" lines
  (missing recommended sections, short body) are expected for some files and do NOT fail the run. CI
  (`.github/workflows/lint-agents.yml`) only lints files changed in the PR, not the whole tree.
- `install.sh` with a TTY and no `--tool` launches a **blocking interactive selector**. In automation always
  pass `--tool <name> --no-interactive` (e.g. `./scripts/install.sh --tool cursor --no-interactive`).
- `install.sh` targets differ by tool: `opencode`, `cursor`, `aider`, `windsurf` write into the **current
  working directory** (`$PWD`), while `claude-code`, `copilot`, `antigravity`, `gemini-cli` write into
  `$HOME`. To avoid dirtying the repo, run project-scoped installs from a scratch dir (e.g. `cd /tmp/x`).
- `convert.sh` output is git-ignored (see `.gitignore`) — regenerated integration files are not committed,
  so a clean `git status` after building is expected.
