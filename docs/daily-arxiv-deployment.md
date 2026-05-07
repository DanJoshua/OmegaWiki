# Deploying `/daily-arxiv` on GitHub Actions

> Deploying the daily-arxiv CI workflow has eight non-obvious gates. Hitting any one of them turns into a silent failure or a rate-limit spiral. This doc lists every gate we've hit, with the log signature you'll see and the fix.
>
> If you're hitting "rate limited", "Authentication failed", "Could not fetch an OIDC token", "Reached maximum number of turns", or "no commit landed despite ingest_status: success" — start at the corresponding row of the troubleshooting table.

## Setup checklist

Run **all** of these before triggering the first dispatch. They're listed in the order CI hits them.

1. **Auth secret** — set one of:
   - `ANTHROPIC_API_KEY` (pay-as-you-go API), or
   - `CLAUDE_CODE_OAUTH_TOKEN` (Pro/Max subscription quota).

   For OAuth, sanitize whitespace before storing:
   ```bash
   TOKEN=$(claude setup-token | tr -d '[:space:]')
   printf '%s' "$TOKEN" | gh secret set CLAUDE_CODE_OAUTH_TOKEN
   unset TOKEN
   ```
   Plain `gh secret set CLAUDE_CODE_OAUTH_TOKEN < <(claude setup-token)` can trap trailing whitespace from the CLI banner or shell line-buffering. Trailing whitespace causes `Authentication failed: Invalid or expired token` *after* OIDC succeeds, which is a confusing signature.

2. **Install the Claude Code GitHub App** on the repo at <https://github.com/apps/claude>. The OAuth token alone is not sufficient — `claude-code-action@v1` exchanges the OIDC token for an app token via this app installation. Without it: `App token exchange failed: 401 Unauthorized — Claude Code is not installed on this repository`.

3. **Mirror the local API keys to GitHub repo secrets.** These look optional in `/setup` and `/daily-arxiv setup` output, but for the daily auto-ingest pipeline they're hard gates (see P5 below):

   ```bash
   gh secret set SEMANTIC_SCHOLAR_API_KEY -b "$(grep ^SEMANTIC_SCHOLAR_API_KEY= .env | cut -d= -f2-)"
   # DeepXiv SDK auto-registers into ~/.env, NOT the project .env:
   gh secret set DEEPXIV_TOKEN -b "$(grep ^DEEPXIV_TOKEN= ~/.env | cut -d= -f2-)"
   ```

4. **SMTP secrets** if `email.enabled: true` in `config/daily-arxiv.yml`:
   `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `DAILY_ARXIV_EMAIL_TO`.

5. **Verify with one manual dispatch** before relying on the cron:
   ```bash
   gh workflow run daily-arxiv.yml --ref main
   gh run watch
   ```
   If it succeeds end-to-end and an auto-ingest commit lands on `main` (only when there's a high-confidence pick), the pipeline is live.

## Pitfalls

| # | Log signature | Root cause | Fix | Where applied |
|---|---|---|---|---|
| P1 | `Action failed with error: Could not fetch an OIDC token. Did you remember to add 'id-token: write'…` | `claude-code-action@v1` needs the workflow to grant OIDC. | Add `id-token: write` to `permissions:` block. | `.github/workflows/daily-arxiv.yml` |
| P2 | `App token exchange failed: 401 Unauthorized - Claude Code is not installed on this repository` | OIDC token is valid, but no Claude Code GitHub App installation exists for this repo. | Install <https://github.com/apps/claude> on the repo. | Repo settings (manual). |
| P3 | `Authentication failed: Invalid or expired token` (right after OIDC step succeeds) | OAuth secret has trailing whitespace, banner text, or other contamination from how it was piped into `gh secret set`. | Strip whitespace on the way in (see step 1 above). Token doesn't actually expire on its own. | Operator. |
| P4 | `Rate limited, waiting 60s/120s/180s... (attempt N/3)` from `tools/fetch_s2.py`; `Prepare recommendation context` runs 50+ minutes per dispatch | `gh secret set <KEY>` was run, but the workflow didn't expose the secret as an env var to the Python step. `fetch_s2.py` reads `os.environ.get("SEMANTIC_SCHOLAR_API_KEY","")`, gets `""`, and runs anonymous (1 req per 3 s, no `x-api-key` header). With ~1000 daily candidates the step blows past any reasonable budget. **This is not "slower but works." It's broken.** | Add `SEMANTIC_SCHOLAR_API_KEY` and `DEEPXIV_TOKEN` to the job-level `env:` block, sourced from `secrets`. | `.github/workflows/daily-arxiv.yml` |
| P5 | Mirror script reads the project `.env` and extracts empty value for `DEEPXIV_TOKEN` | The DeepXiv SDK auto-registers and writes the token to `~/.env`, not the project `.env`. The project `.env.example` template just has `DEEPXIV_TOKEN=` (empty placeholder). | When mirroring to a GH secret, source from `~/.env`: `grep ^DEEPXIV_TOKEN= ~/.env`. | Operator (or step 3 above). |
| P6 | `Reached maximum number of turns (20)` (or 60) from `claude-code-action` | The action's default `--max-turns 20` is far too low for an auto-ingest run. A single `/ingest` cycle takes ~40–50 tool calls (paper page + 3–5 concepts + 1–2 claims + people + graph edges + S2/DeepXiv enrichment + commit). The decision step over the day's candidates adds 5–10 more. | Set `--max-turns 100` in the action's `claude_args:` to leave headroom for one paper. Increase further if `max_auto_ingest > 1`. | `.github/workflows/daily-arxiv.yml` |
| P7 | `fatal: Authentication failed for 'https://github.com/<owner>/<repo>.git/'` exit 128 in the commit step, after Claude action and digest finalize succeed | `actions/checkout@v4` with `persist-credentials: true` installs an auth header in `.git/config`. The intervening `claude-code-action` step unsets that header as part of its own cleanup. The commit step inherits a remote URL with no credentials. | Before `git push`, re-embed the token in the remote URL: `git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"`. The step needs `GITHUB_TOKEN` in its `env:` block. | `.github/workflows/daily-arxiv.yml` |
| P8 | Run finishes green. `digest.md` and `llm-decisions.json` show `Decision: ingest`, `ingest_status: success`. But `git pull` shows no auto-ingest commit on `main`, no new `wiki/papers/<slug>.md` exists | The action's `--allowedTools` is `Read,Write,Edit,Bash`. None of those let Claude invoke the `/ingest` skill — that requires the `Skill` tool. Claude writes the structured `ingest_status: success` because the prompt's schema asks for it, but never actually invokes `/ingest`. The commit step's `git diff --cached --quiet` is true (nothing changed), so it exits 0 with a "no changes were staged" summary. | Add `Skill,TodoWrite,Agent` to `--allowedTools` so the skill can run, sub-tasks can be tracked, and `/ingest`'s subagent fan-out works. | `.github/workflows/daily-arxiv.yml` |

## Systemic gotchas

- **Pro/Max OAuth quota is shared.** The same OAuth token authenticates your local Claude Code session *and* CI's auto-ingest. Heavy local use (e.g. running `/init` against a large set of papers) burns the same 5-hour rolling window CI relies on. If CI auth fails for ~hours, check whether you've been hammering Claude Code locally.
- **Missing API keys are not "optional polish" for daily ingestion.** `/daily-arxiv setup` and `/daily-arxiv status` previously labeled S2/DeepXiv as optional. Treat them as required for any daily-cadence pipeline; the rate-limit math doesn't work without them.
- **`gh run watch --exit-status` returns 0 on cancellation, not just success.** Don't read its exit code as "the run succeeded" — read `gh run view <id> --json conclusion`.
- **In-progress job logs return HTTP 404.** `gh api .../jobs/<id>/logs` only works after the job finishes. Don't trust an empty log fetch as "no errors yet."

## Why the workflow looks the way it does

Each non-obvious snippet in `.github/workflows/daily-arxiv.yml` exists because of one of the above. Inline comments cross-reference back here.

## Verifying a clean pipeline

A successful end-to-end run produces:
1. ✓ All steps green in the GitHub Actions UI.
2. `digest.md` artifact with a populated **Strong Recommendations** section.
3. SMTP digest e-mail in your inbox (if `email.enabled`).
4. *Either* a new commit on `main` titled `daily-arxiv auto-ingest` *or* the step summary line "no wiki/raw changes were staged" — depending on whether any candidate cleared the high-confidence ingest gate that day. Both are valid green-pipeline outcomes.

## Reference commits

The fixes for P1–P7 were applied in the following order while debugging this pipeline:

| Commit | Pitfall fixed |
|---|---|
| `5b412f4` | P1 (id-token: write) |
| `c47d35c` | P4 (S2/DeepXiv env passthrough) |
| `458ce16` → `b887ac5` | P6 (max-turns 20 → 60 → 100) |
| `e12e3db` | P7 (re-auth git push) |

P8 was identified after run #17 and the fix lands together with this doc.
