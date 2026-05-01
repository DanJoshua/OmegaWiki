# Daily arXiv Automation Scaffold

The GitHub Actions workflow is the current production path for `/daily-arxiv`.
It proves the daily collection, deduplication, artifact, and SMTP notification
loop without letting CI mutate the wiki.

## Schedule and dispatch

- Scheduled run: `17 0 * * *` UTC, which is 08:17 Beijing time.
- Manual run: `workflow_dispatch` with `hours`, `categories`, `max_items`, and `send_email`.
- Use a non-zero minute to avoid GitHub's top-of-hour scheduled-workflow congestion.
- Keep `permissions: contents: read` while the workflow is inform-only.

## Secrets

SMTP delivery reads these repository secrets:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `DAILY_ARXIV_EMAIL_TO`

`ANTHROPIC_API_KEY` is not needed for the scaffold because the workflow does not
run Claude Code. If recommendation later uses an LLM, add that as a separate
optional recommender dependency.

## Artifacts

Each run uploads:

- `feed.json` — raw arXiv RSS result after `tools/fetch_arxiv.py`
- `digest.md` — human-readable e-mail body
- `digest.json` — machine-readable scaffold payload

The workflow also writes `digest.md` to the GitHub Actions job summary. Do not
commit daily artifacts until auto-ingest exists and repository writes are
explicitly enabled.

## Failure behavior

- Missing SMTP secrets fail only when `send_email=true`.
- `send_email=false` manual runs are valid dry runs and still upload artifacts.
- Empty feeds and fully deduplicated feeds are successful runs with empty digest
sections.
- Fetch failures should fail the run before e-mail is attempted.
