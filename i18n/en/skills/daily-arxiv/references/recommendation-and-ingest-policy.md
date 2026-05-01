# Daily arXiv Recommendation and Ingest Policy

This reference is for the future `/daily-arxiv` recommendation layer. It is not
implemented by the current inform-only scaffold.

## Phase boundary

Keep the pipeline split into explicit phases:

1. Collect new arXiv papers.
2. Deduplicate against the wiki.
3. Enrich candidates with optional external signals.
4. Score and select candidates.
5. Notify by digest.
6. Optionally ingest selected papers when the mode permits it.

The workflow and e-mail layer should not care which recommender fills `score`,
`signals`, `rationale`, or `decision` in `digest.json`.

## Recommendation signals

Use existing integrations before adding new logic:

- Semantic Scholar: recommendations, citations, references, citation counts,
  influential citation counts, fields of study, author metadata.
- DeepXiv: trending papers, TLDR, keywords, social impact, paper structure.
- Wiki context: existing topics, concepts, open questions, and recent ingests.

Batch scoring is preferred. Avoid per-paper LLM calls unless there is a clear
quality reason and a rate-limit budget.

## Decision modes

- `inform`: default. Send recommendations only; do not download or ingest.
- `auto-ingest`: future opt-in mode. Download selected papers into
  `raw/discovered/`, pass the canonical path to `/ingest`, and commit the
  resulting wiki changes.

Do not infer `auto-ingest` from repository state. The user or workflow input
must choose it explicitly.

## Auto-ingest guardrails

- `/ingest` owns all paper incorporation. `/daily-arxiv` must not hand-write
  paper pages, concepts, claims, people, graph files, or index entries.
- Download external paper artifacts only under `raw/discovered/`.
- Keep `raw/papers/`, `raw/notes/`, `raw/web/`, and `raw/tmp/` untouched.
- Add `contents: write` to the workflow only when auto-ingest is implemented.
- Commit both `wiki/` and `raw/discovered/` changes when ingest actually occurs.
- Cap the number of auto-ingested papers per run and preserve failures in the
  digest instead of hiding them.

## Relationship to `/discover`

`/discover` answers deliberate "what should I read next?" requests from anchors,
topics, or the wiki. `/daily-arxiv` watches a fresh-paper stream. They can share
deterministic scoring helpers later, but their entry points and user intent are
different.
