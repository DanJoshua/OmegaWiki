# /batch-ingest Inputs

`/batch-ingest` accepts exactly one input per invocation. Pick the form by extension and filesystem type — there is no auto-detection across mixed inputs.

## Form A: directory of PDFs (user-local)

A directory under `raw/papers/` containing one or more `.pdf` files. The scan is **recursive**, so `raw/papers/2025-survey/*.pdf` and `raw/papers/2025-survey/sub/*.pdf` both contribute.

Rules:

- The directory must live under `raw/papers/`. `tools/batch_ingest.py prepare` calls `prepare_paper_source.prepare_paper_source(...)`, which requires every input path to resolve under the project's `raw_root`.
- Each PDF is treated as user-owned. `/batch-ingest` writes prepared sidecars (recovered TeX or synthetic TeX) under `raw/tmp/` but never copies, moves, or rewrites the original PDF.
- arXiv-ID recovery is best-effort, in this order: filename / containing path → `prepare_paper_source` PDF metadata heuristics → Semantic Scholar title search. PDFs whose arXiv ID cannot be recovered still ingest, just without S2 metadata. Their year will be `null` and they will sort to the front of the queue.
- Each entry shows up in the manifest with `origin: "user_local"` and a `canonical_ingest_path` that points at the prepared sidecar in `raw/tmp/` when one was produced, or back at `raw/papers/...` otherwise.

Typical use: the user dropped a folder of PDFs they collected (e.g. an arXiv firehose, a workshop proceedings download, a personal reading list) and wants them all folded in.

## Form B: URL list file

A `.md` or `.txt` file (anywhere in the project) listing arXiv URLs, one per line. The file is parsed loosely:

- blank lines and lines starting with `#` are skipped
- markdown bullets (`- ...`, `* ...`) are stripped
- markdown links `[label](https://arxiv.org/abs/...)` are accepted; the URL is pulled out
- bare URLs are accepted

Only arXiv URLs are recognized in v1 (`arxiv.org/abs/...`, `arxiv.org/pdf/...`, `arxiv.org/html/...`). Other URLs are silently ignored — they show up in the warnings list but do not block the run.

Rules:

- arXiv source archives are downloaded into `raw/discovered/{slug}/` (TeX preferred, PDF fallback) — the same location and policy `/init` uses for introduced papers.
- Titles for the discovered slug come from Semantic Scholar; if S2 is unavailable, the slug falls back to `arxiv-{id}` and the entry still ingests.
- Each entry shows up in the manifest with `origin: "introduced"` and a `canonical_ingest_path` pointing at the downloaded source under `raw/discovered/`.

Typical use: the user has a curated reading list (a `survey.md`, a Slack export, a quick `urls.txt`) and wants the wiki to absorb it.

## Mixing the two

Mixing local PDFs and URLs in one run is intentionally not supported in v1. The two paths have different prepare costs, different failure modes (filesystem vs network), and different ordering signals (file mtime fallback vs none). If the user wants both, run `/batch-ingest` twice — once per form. Cross-batch consistency still works because the second run branches off the first run's merged commits.

## What to do when an input fails

`tools/batch_ingest.py prepare` continues past per-paper failures and records them in `manifest["warnings"]`. The skill should:

- if **zero** sources prepared, stop and report — `/batch-ingest` cannot meaningfully run on an empty manifest
- if some sources prepared, continue and surface the warnings in the final report so the user can re-attempt failed papers later (typically with a direct `/ingest`)

Refer to `skills/ingest/references/error-handling.md` for the per-paper recovery patterns `/ingest` itself uses; `/batch-ingest` does not duplicate them.
