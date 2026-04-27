---
description: Ingest many papers into the wiki at once, with chronological ordering and small parallel batches that share state across the run. Trigger when the user points at a directory of PDFs under `raw/papers/` or a `.md` / `.txt` file of arXiv URLs and asks to ingest them as a set, says "batch ingest", "fold these papers in", or hands over a paper bundle that is too big for a single `/ingest`.
argument-hint: <pdf-dir-or-url-list-file> [--batch-size N]
---

# /batch-ingest

Orchestrate many `/ingest` runs as a managed batch. Each batch fans out a small set of papers to parallel `/ingest` subagents inside isolated git worktrees; the parent merges the batch back, then the next batch starts from the merged commit. Cross-paper consistency that an isolated `/ingest` cannot see — paper-to-paper edges, concept and claim dedup across the bundle — is mostly produced for free by the chronological ordering and the sequential fan-in between batches.

`/batch-ingest` is the orchestration layer. The actual page writing always happens through `/ingest` running in **BATCH MODE** — see `skills/ingest/references/batch-mode.md`.

Use these local references on demand:

- `references/inputs.md` — accepted input forms (PDF directory vs URL list file) and recovery rules
- `references/batch-orchestration.md` — chronological sort rationale, batching, worktree contract, fan-in cadence, checkpoint/resume

## Inputs

- `<pdf-dir-or-url-list-file>` — exactly one of:
  - a directory under `raw/papers/` containing `.pdf` files (recursive scan)
  - a `.md` or `.txt` file with one arXiv URL per line (anywhere in the project)
- `--batch-size N` (optional): override the default `max(ceil(sqrt(N)), 4)`

`/batch-ingest` does not run discovery, does not call the planner, and does not seed provisional notes/web pages — those belong to `/init`. It also does not create `wiki/Summary/` pages in v1; defer those to `/edit`.

## Outputs

- One fully-wired paper page per input, plus all linked entities created via `/ingest`
- Graph edges and citations appended via `tools/research_wiki.py`
- `.checkpoints/batch-ingest-sources.json` — chronological manifest, single source of truth for ingest order
- `.checkpoints/batch-ingest-state.json` — last completed batch index, for resume
- Updated `wiki/index.md`, `wiki/log.md`, `wiki/graph/*`
- Final report grouping per-batch results and any skipped papers

## Wiki Interaction

### Reads

- The input directory or URL list file
- `wiki/index.md` and existing pages for duplicate avoidance
- `.checkpoints/batch-ingest-sources.json` and `.checkpoints/batch-ingest-state.json` for resume

### Writes

- `raw/tmp/` — prepared local sidecars for user-owned PDFs
- `raw/discovered/` — fetched arXiv sources for URL-list inputs
- `wiki/topics/{slug}.md` — CREATE topic shells when ≥2 input papers obviously share a topic and no page exists yet (scaffold step only)
- `wiki/index.md`, `wiki/log.md`, `wiki/graph/*` — updated through `tools/research_wiki.py` and through `/ingest` subagents
- `.checkpoints/batch-ingest-sources.json`, `.checkpoints/batch-ingest-state.json`, and `batch-ingest-session` checkpoint metadata

### Graph edges created

- `/batch-ingest` itself creates no edges. All paper-driven edges are delegated to `/ingest`.

## Workflow

**Pre-condition**: working directory is the project root containing `wiki/`, `raw/`, and `tools/`. Set `WIKI_ROOT=wiki/`. Resolve `PYTHON_BIN` once and reuse it throughout:

```bash
# Find the project root via git so worktree subagents can still locate .venv.
# .venv is gitignored, so a subagent whose cwd is ../.worktrees/<branch>/
# doesn't have one — without this lookup it falls back to system python3 and
# misses the .env-loaded API keys plus the installed deps (deepxiv-sdk etc.).
# git rev-parse --git-common-dir returns the main repo's .git regardless of
# which worktree the shell is in; its parent is the project root.
GIT_COMMON_DIR=$(git rev-parse --git-common-dir 2>/dev/null || true)
PROJECT_ROOT=""
if [ -n "$GIT_COMMON_DIR" ]; then
  PROJECT_ROOT=$(cd "$(dirname "$GIT_COMMON_DIR")" 2>/dev/null && pwd)
fi

if   [ -x "$PROJECT_ROOT/.venv/bin/python" ];         then PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
elif [ -x "$PROJECT_ROOT/.venv/Scripts/python.exe" ]; then PYTHON_BIN="$PROJECT_ROOT/.venv/Scripts/python.exe"
elif [ -x .venv/bin/python ];                         then PYTHON_BIN=.venv/bin/python
elif [ -x .venv/Scripts/python.exe ];                 then PYTHON_BIN=.venv/Scripts/python.exe
else                                                       PYTHON_BIN=python3
fi
export PYTHON_BIN
```

Verify the wiki is initialized (`wiki/index.md` and `wiki/graph/` exist). If not, ask the user to run `/init` first — `/batch-ingest` does not bootstrap an empty wiki.

### Step 1: Prepare the manifest

```bash
"$PYTHON_BIN" tools/batch_ingest.py prepare \
  --input <pdf-dir-or-url-list-file> \
  --raw-root raw \
  --output-manifest .checkpoints/batch-ingest-sources.json
```

The tool resolves each input, prepares user-owned PDFs into `raw/tmp/` and downloads URL-list arXiv sources into `raw/discovered/`, looks up publication year via Semantic Scholar, sorts chronologically (unknown-year papers go to the front — see `references/batch-orchestration.md`), and computes the default batch size. The manifest is the single source of truth for ingest order; do not rescan inputs after this step.

If the user passed `--batch-size N`, overwrite `manifest["batch_size"]` and recompute `manifest["batch_count"]` before continuing. If the manifest reports zero usable sources, stop and report.

### Step 2: Pre-fan-out scaffold

Look at the manifest's `title` fields and group papers by obvious shared topic. For each group of ≥2 papers where no `wiki/topics/{slug}.md` exists yet, create a minimal topic shell (frontmatter only — `name`, `tags`, an empty `## Overview`). Slugs come from `tools/research_wiki.py slug`. Do **not** populate the shell with paper rows; subagents do not append to topics in BATCH MODE (`skills/ingest/references/batch-mode.md`) and the per-paper content update is deferred to `/edit`. Do **not** create `Summary/` pages in v1 — defer those to `/edit`.

This step is conservative: skip groups with thin signal. A wrong topic shell is harder to undo than a missing one.

### Step 3: Pre-fan-out safety

Follow the same protocol as `/init`'s parallel ingest (see `references/batch-orchestration.md` for full details). Highlights:

- Stash unrelated dirty files outside `wiki/`, `raw/`, and `.checkpoints/batch-ingest-*.json`
- Verify `.gitattributes` declares `merge=union` for `wiki/log.md`, `wiki/graph/edges.jsonl`, `wiki/graph/citations.jsonl`, and `wiki/index.md`
- Refuse detached HEAD; require a named branch
- Commit the scaffold + manifest before fan-out so `BASE_COMMIT` carries the topic shells and the manifest that every worktree must inherit
- Record `stash_ref`, `base_branch`, and `base_commit` via `tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...`

### Step 4: Per-batch loop

For each batch index `b` in `[0, batch_count)`, in order:

1. Resume check: read `.checkpoints/batch-ingest-state.json` (if present); if `b <= last_completed_batch`, skip.
2. Take the next `manifest["batch_size"]` sources from the manifest (in `ingest_rank` order).
3. For each source in the batch, in parallel:
   - Create a worktree from the **current** `BASE_COMMIT`:

     ```bash
     WT_BRANCH="batch-${BASE_BRANCH//\//-}-${b}-${ingest_rank}-${paper_slug}"
     WT_PATH="../.worktrees/$WT_BRANCH"
     git worktree add -b "$WT_BRANCH" "$WT_PATH" "$BASE_COMMIT"
     ```

   - Spawn a subagent that runs `/ingest` in BATCH MODE on the source's `canonical_ingest_path`. Subagent contract is identical to INIT MODE: skip per-subagent rebuilds, skip topic writes, commit inside the worktree before exiting. See `skills/ingest/references/batch-mode.md`.
4. Fan-in this batch:
   - Merge each worktree branch into `BASE_BRANCH` sequentially (`git merge --no-ff --no-edit`).
   - Resolve true concept/claim conflicts conservatively — merge, do not multiply near-duplicates.
   - Run the cheap dedup pass:

     ```bash
     "$PYTHON_BIN" tools/research_wiki.py dedup-edges wiki/
     "$PYTHON_BIN" tools/research_wiki.py dedup-citations wiki/
     ```

   - Skip `rebuild-context-brief`, `rebuild-open-questions`, and `rebuild-index` between batches; defer to step 5.
   - Remove worktrees and branches: `git worktree remove "$WT_PATH" && git branch -d "$WT_BRANCH"`.
5. **Advance `BASE_COMMIT` to the new `HEAD`.** This is the cross-batch dedup mechanism: the next batch's worktrees branch from a tree that already contains every previous batch's slugs, so `find-similar-concept` and `find-similar-claim` inside subagents naturally see them.
6. Update the state checkpoint:

   ```bash
   "$PYTHON_BIN" tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session last_completed_batch "$b"
   ```

   Also write `.checkpoints/batch-ingest-state.json` with `{"last_completed_batch": b, "base_commit": "<sha>"}` for resume.

### Step 5: Final rebuild

After the last batch:

```bash
"$PYTHON_BIN" tools/research_wiki.py rebuild-index wiki/
"$PYTHON_BIN" tools/research_wiki.py rebuild-context-brief wiki/
"$PYTHON_BIN" tools/research_wiki.py rebuild-open-questions wiki/
"$PYTHON_BIN" tools/lint.py wiki/ --fix
```

If `stash_ref` exists, pop it. If pop fails, keep the checkpoint and report the manual recovery step.

### Step 6: Report

Emit one compact summary covering:

- total papers in the batch, by origin (`user_local` from `raw/tmp/`, `introduced` from `raw/discovered/`)
- per-batch breakdown: ingested, skipped, failed
- topic shells created in step 2
- pages created and updated by `/ingest` (aggregated across subagents)
- any contradictions or high-citation external references the subagents surfaced

Close with:

```
Wiki: +{P} papers, +{C} claims, +{K} concepts, +{E} edges across {B} batches
```

## Constraints

- Inputs are mutually exclusive: one directory of PDFs **or** one URL list file per invocation. Mixing the two requires two separate runs.
- The PDF directory must live under `raw/papers/` so `prepare_paper_source.py` can compute relative paths into `raw/tmp/`. URL list files may live anywhere.
- `/batch-ingest` may write generated prepared local sidecars under `raw/tmp/` and externally fetched papers under `raw/discovered/`. It must not touch `raw/papers/`, `raw/notes/`, or `raw/web/`.
- `wiki/Summary/` creation is out of scope for v1.
- All paper ingest must run through `/ingest` BATCH MODE subagents in worktrees. Do not bypass `/ingest`.
- Step 4 must read paper inputs from `.checkpoints/batch-ingest-sources.json`, not by ad hoc folder scanning.
- `BASE_COMMIT` must advance after each batch — this is the cross-batch dedup mechanism, not an optimization. Skipping it defeats the design.

## Error Handling

- **Detached HEAD before fan-out**: stop and ask the user to switch to or create a named branch.
- **Single paper preparation fails**: record the warning in the manifest and continue with the rest. The skipped paper appears in the final report.
- **Single paper ingest fails inside a worktree**: do not block fan-in for that batch; skip the failed worktree's merge and list the paper in the report. Resume can re-attempt by removing the manifest entry and rerunning.
- **S2 outage during prepare**: years come back as `null`; affected papers cluster at the front of the queue. The pipeline still proceeds; flag the degraded ordering in the report.
- **Concurrent slug collision inside a batch**: rare due to the per-paper concept/claim creation limit in `/ingest`; resolve at fan-in by picking the earlier merge and re-running `find-similar-*` on the loser. Same protocol as `/init` parallel ingest.
- **Stash pop fails at the end**: keep the checkpoint so the user can recover manually.

## Dependencies

### Tools (via Bash)

- `"$PYTHON_BIN" tools/batch_ingest.py prepare --input <path> --raw-root raw --output-manifest .checkpoints/batch-ingest-sources.json`
- `"$PYTHON_BIN" tools/research_wiki.py slug "<title>"`
- `"$PYTHON_BIN" tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session <key> <value>`
- `"$PYTHON_BIN" tools/research_wiki.py dedup-edges wiki/`
- `"$PYTHON_BIN" tools/research_wiki.py dedup-citations wiki/`
- `"$PYTHON_BIN" tools/research_wiki.py rebuild-index wiki/`
- `"$PYTHON_BIN" tools/research_wiki.py rebuild-context-brief wiki/`
- `"$PYTHON_BIN" tools/research_wiki.py rebuild-open-questions wiki/`
- `"$PYTHON_BIN" tools/research_wiki.py log wiki/ "<message>"`
- `"$PYTHON_BIN" tools/lint.py wiki/ --fix`

### Skills

- `/ingest` — runs in BATCH MODE inside each worktree subagent (`skills/ingest/references/batch-mode.md`)
- `/init` — separate skill for first-time wiki bootstrap; `/batch-ingest` assumes `/init` has already run

### External APIs used by `tools/batch_ingest.py`

- Semantic Scholar (`paper`) for year lookup and discovered-paper titles
- arXiv source download (via `init_discovery.download_to_discovered`)
