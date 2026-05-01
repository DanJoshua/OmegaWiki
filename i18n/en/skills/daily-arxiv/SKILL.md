---
description: Daily arXiv collection, wiki deduplication, digest generation, and e-mail notification; recommendation and optional auto-ingest are staged for later
argument-hint: "[--hours 24] [--categories <cat...>] [--max-items 20] [--send-email true|false]"
---

# /daily-arxiv

> Monitor a daily arXiv time window, deduplicate against the wiki, produce a concise digest, and notify the user by e-mail. The current automation scaffold is inform-only: it does not score, download, ingest, or mutate the wiki.

Use these local references on demand:

- `references/automation-scaffold.md` — GitHub Actions scaffold, SMTP secrets, artifacts, and failure behavior
- `references/recommendation-and-ingest-policy.md` — future recommendation signals, decision modes, and auto-ingest guardrails

## Inputs

- `--hours N`: pull papers from the last N hours (default 24)
- `--categories <cat...>`: override default arXiv categories (`cs.LG cs.CV cs.CL cs.AI stat.ML`)
- `--max-items N`: maximum new candidates shown in the digest (default 20)
- `--send-email true|false`: workflow-only switch for SMTP delivery; manual dry runs can set `false`

## Outputs

- GitHub Actions artifacts: `feed.json`, `digest.md`, `digest.json`
- GitHub Actions job summary containing the Markdown digest
- Optional SMTP e-mail with the same Markdown digest

The scaffold writes no `wiki/` pages, no `raw/` files, and no commits. Future auto-ingest must be explicit opt-in and route all paper incorporation through `/ingest`.

## Wiki Interaction

### Reads

- `wiki/index.md` and `wiki/papers/*.md` — arXiv URL / ID deduplication

### Writes

- none in the current scaffold

### Graph edges created

- none. Graph and entity mutations belong to `/ingest`.

## Workflow

1. Fetch the feed:

   ```bash
   python3 tools/fetch_arxiv.py --hours <hours> [-o <feed.json>] [--categories <cat...>]
   ```

2. Build the digest:

   ```bash
   python3 tools/daily_arxiv.py digest --feed <feed.json> --wiki-root wiki --out-md <digest.md> --out-json <digest.json> --max-items <N>
   ```

3. Send e-mail when enabled:

   ```bash
   python3 tools/send_email.py --subject "<subject>" --body-file <digest.md>
   ```

4. Review the artifact or e-mail. Do not run `/ingest` from this scaffold.

## Relationship to Neighboring Skills

- `/discover` is deliberate recommendation from user-provided anchors, a topic, or current wiki state. It proposes next reads and never ingests.
- `/daily-arxiv` is a time-window stream processor. It starts from new arXiv papers and is designed to notify daily.
- `/ingest` remains the only skill that incorporates a selected paper into `wiki/`, `raw/discovered/`, and graph files.

## Constraints

- Keep CI deterministic: do not call Claude Code or require `ANTHROPIC_API_KEY` in the scaffold workflow.
- Keep recommendation policy out of the workflow YAML; put deterministic pieces in `tools/` and orchestration policy in references.
- Do not auto-ingest until selection is implemented, opt-in, and guarded by a workflow mode.
- SMTP is the only supported notification transport in the scaffold.
- GitHub Actions artifacts, not commits, are the run history for now.

## Error Handling

- **RSS fetch fails**: fail the workflow before digest generation.
- **SMTP secrets missing**: fail with a clear configuration error when `--send-email true`; manual `send_email=false` runs should still produce artifacts.
- **Empty RSS or no new candidates**: produce a valid empty digest and artifact.
- **Future external APIs unavailable**: preserve degraded-mode notes in the digest instead of treating missing enrichment as ingest authority.

## Dependencies

### Tools

- `tools/fetch_arxiv.py` — arXiv RSS collection
- `tools/daily_arxiv.py digest` — deterministic inform-only digest
- `tools/send_email.py` — SMTP delivery

### Future tools / APIs

- `tools/fetch_s2.py` — Semantic Scholar metadata and recommendation signals
- `tools/fetch_deepxiv.py` — DeepXiv trending, TLDR, and social-impact signals
- `/ingest` — future opt-in paper incorporation only
