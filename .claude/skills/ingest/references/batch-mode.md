# /ingest BATCH MODE

Open this reference when `/ingest` is invoked by `/batch-ingest` as a parallel subagent. BATCH MODE shares its parallel-safety mechanics with INIT MODE — the differences are in which manifest drives the run and how the parent paces fan-in.

## When BATCH MODE is active

BATCH MODE is active for any `/ingest` invocation whose source path originates from `.checkpoints/batch-ingest-sources.json`. The parent `/batch-ingest` runs one `/ingest` per paper inside an isolated `git worktree`, batching papers in chronological groups; see `skills/batch-ingest/references/batch-orchestration.md` for the parent's contract.

In BATCH MODE:

- the source is a `canonical_ingest_path` already prepared by `/batch-ingest` (a `raw/tmp/...` path for user-owned PDFs, or a `raw/discovered/...` path for arXiv-URL inputs)
- `raw/` is strictly read-only — do not write to `raw/tmp/`, `raw/discovered/`, or anywhere else under `raw/`
- `fetch_s2.py citations <arxiv-id>` and `fetch_s2.py references <arxiv-id>` are **skipped** — the parent owns citation handling at fan-in
- `rebuild-context-brief`, `rebuild-open-questions`, and `rebuild-index` are **skipped** per subagent — the parent runs them once after the final batch
- topic writes are **skipped** entirely — including appends to existing topic pages. The parent may have created topic shells in its scaffold step, but content updates from individual papers go through `/edit` after fan-in. Concurrent appends from sibling subagents would merge-conflict; aligning with INIT MODE on this point keeps the parallel-safety contract simple and matches what `/check`/`/edit` already handle for batch follow-ups.

Everything else — paper page creation, concept/claim dedup via `find-similar-*`, people-page rules, paper `## Related` links, graph edges for concept/claim/foundation — runs normally per subagent.

## Detecting BATCH MODE

`/batch-ingest` passes the canonical path in the subagent prompt and explicitly names BATCH MODE. Recognize BATCH MODE by either of:

- the source path starts with `raw/tmp/` or `raw/discovered/` **and** the `.checkpoints/batch-ingest-sources.json` manifest references it
- the subagent prompt explicitly states `BATCH MODE`

When both signals are absent and `init-sources.json` is the matching manifest, that is INIT MODE — see `references/init-mode.md`. When neither manifest matches, treat the invocation as a direct user call.

## Why a separate mode

INIT MODE and BATCH MODE skip the same set of steps inside `/ingest`. They differ in what the parent does:

- `/init` does one big fan-out and one fan-in, then runs the heavy rebuilds once
- `/batch-ingest` does sequential batches, advances `BASE_COMMIT` between them, and defers the heavy rebuilds until after the last batch

From `/ingest`'s perspective both modes look identical, but keeping the names distinct lets each parent skill evolve its fan-in policy without breaking the other. If you find yourself adding a mode-specific behavior inside `/ingest`, prefer adding it to one mode rather than collapsing the two.

## Parallel-safe writes

The same three rules from INIT MODE apply (see `references/init-mode.md` for the long form):

1. **Every shared-file write goes through a tool.** `graph/edges.jsonl`, `graph/citations.jsonl`, `index.md`, and `log.md` are written via `tools/research_wiki.py add-edge`, `add-citation`, index updates, and `log`. The tool layer uses append semantics; `.gitattributes` declares `merge=union` for these paths.
2. **Slugs are allocated deterministically** via `tools/research_wiki.py slug "<title>"`. Two worktrees that pick the same title will pick the same slug, and the parent resolves the collision at fan-in.
3. **Never lock or in-place-rewrite a shared file.**

## Slug collisions across batches

The cross-batch dedup mechanism in `/batch-ingest` advances `BASE_COMMIT` between batches, so a paper in batch 2 sees concept slugs that batch 1 created. From `/ingest`'s perspective this looks the same as ingesting into a populated wiki — `find-similar-concept` will return the existing slug and dedup-by-merge applies normally. No special handling required.

Within a batch, two sibling subagents may still collide on a freshly-introduced concept. The per-paper concept/claim creation limit in `references/dedup-policy.md` keeps the surface small; `/batch-ingest`'s per-batch fan-in resolves the collision by merging conservatively.

## What `/ingest` does not do for `/batch-ingest`

- it does not commit (the subagent prompt is responsible for the commit inside the worktree)
- it does not stash or switch branches
- it does not merge worktrees, advance `BASE_COMMIT`, or run `dedup-edges` / `dedup-citations` / `rebuild-*` — those are fan-in operations owned by `/batch-ingest`
