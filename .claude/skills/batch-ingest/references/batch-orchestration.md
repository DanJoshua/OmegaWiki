# /batch-ingest Orchestration

The mechanics of how a batch run is sliced, fanned out, and merged back. Open this when you are about to run step 3 or step 4 of `SKILL.md`.

## Why batches at all

`/init` fans out every paper at once and merges them all in a single fan-in. That works because `/init` controls the input set tightly (≤10 papers) and the tradeoff against cross-paper consistency is acceptable for bootstrap.

`/batch-ingest` is the long-tail case: maybe 5 papers, maybe 50. A single fan-out cannot use `find-similar-concept` across siblings — every worktree branches from the same commit and sees the same prior wiki state. The result is duplicate concepts, claims, and missing paper-paper edges.

The fix is sequential batches. Within a batch, papers run in parallel (cheap, isolated). Between batches, the parent merges the worktrees into the main branch and **advances `BASE_COMMIT` to the new HEAD** before the next batch fans out. The next batch's worktrees branch from a tree that already contains every previous batch's slugs, so `find-similar-*` inside subagents naturally sees them and merges into them rather than creating duplicates.

This is why the batch loop in `SKILL.md` is sequential, not parallel, between batches. Skipping the `BASE_COMMIT` advance defeats the design.

## Why chronological order

We sort papers oldest → newest before slicing into batches. The reason is dedup bias: when two papers contribute overlapping claims, `/ingest`'s dedup logic keeps the existing claim and appends the new evidence. Ingesting older papers first means later (newer) papers' claim contributions land on top, refining what came before. Reversing the order means newer claims get treated as the base, and older papers' evidence gets bolted on as an afterthought — the wiki ends up reading like history is happening backwards.

Unknown-year papers go to the **front** of the queue, not the back. The reasoning is that papers without an S2 year are usually antique works pre-dating the S2 corpus, not unsubmitted manuscripts. Front-loading them treats them as the oldest layer, which matches typical reality and keeps the dedup bias coherent.

## Batch size

Default is `B = max(ceil(sqrt(N)), 4)` where `N` is the number of prepared sources.

| N   | B  | batches |
|-----|----|---------|
| 4   | 4  | 1       |
| 9   | 4  | 3       |
| 16  | 4  | 4       |
| 25  | 5  | 5       |
| 100 | 10 | 10      |

Both dimensions grow slowly with `N`, so a 100-paper run is 10 batches of 10 rather than 25 batches of 4 (too much fan-in overhead) or 4 batches of 25 (too much in-batch collision risk). The user can override via `--batch-size N`.

## Pre-fan-out safety

Same protocol as `/init`'s parallel ingest, with `batch-ingest-*.json` paths in place of `init-*.json`:

1. `git status --short`. Treat files under `wiki/`, `raw/tmp/`, `raw/discovered/`, and `.checkpoints/batch-ingest-*.json` as scaffold; stash everything else.
2. Verify `.gitattributes` declares `merge=union` for `wiki/log.md`, `wiki/graph/edges.jsonl`, `wiki/graph/citations.jsonl`, and `wiki/index.md`. Without these, fan-in conflicts on every batch.
3. Refuse detached HEAD. Stop and ask the user to switch to or create a named branch.
4. Commit the scaffold (topic shells from step 2) and the manifest before fan-out so `BASE_COMMIT` carries everything subagents must inherit:

   ```bash
   git add wiki/ raw/tmp/ raw/discovered/ .checkpoints/batch-ingest-sources.json
   git commit -m "batch-ingest: scaffold before parallel ingest" --no-gpg-sign
   BASE_COMMIT=$(git rev-parse HEAD)
   BASE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
   ```

5. Record `stash_ref`, `base_branch`, and `base_commit` via `tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...`.

## Worktree creation

For each paper in the current batch:

```bash
WT_BRANCH="batch-${BASE_BRANCH//\//-}-${b}-${ingest_rank}-${paper_slug}"
WT_PATH="../.worktrees/$WT_BRANCH"
git worktree add -b "$WT_BRANCH" "$WT_PATH" "$BASE_COMMIT"
```

- Branch from the **current** `BASE_COMMIT`, not from `BASE_BRANCH` directly. Git will refuse `worktree add` against a branch already checked out elsewhere.
- Order papers within a batch by `ingest_rank` from the manifest, not by rescanning raw directories.

## Subagent prompt contract

Each subagent runs exactly one `/ingest` for one paper, in BATCH MODE. The prompt must:

- name the canonical source path **with relative paths only** (no absolute paths from the parent's environment)
- explicitly state `BATCH MODE` so the subagent picks up the right skip-list
- direct the subagent to commit its result inside the worktree before exiting

BATCH MODE skip-list inside `/ingest` (identical in spirit to INIT MODE):

- skip `fetch_s2.py citations`
- skip `fetch_s2.py references`
- skip per-subagent `rebuild-index`
- skip per-subagent `rebuild-context-brief`
- skip per-subagent `rebuild-open-questions`
- skip conflict-prone topic creation (the parent already created shells in step 2)
- treat `raw/` as strictly read-only — do not write to `raw/tmp/` or `raw/discovered/` from inside a subagent

Full reference: `skills/ingest/references/batch-mode.md`.

## Per-batch fan-in

After every worktree in the current batch has committed:

1. Switch the main workspace back to `BASE_BRANCH` if needed.
2. Merge each worktree branch sequentially in `ingest_rank` order:

   ```bash
   git merge --no-ff "$WT_BRANCH" --no-edit
   ```

3. Resolve concept/claim conflicts conservatively. When two worktrees both created `concepts/foo.md`, prefer the earlier-merged version and re-run `find-similar-concept` on the loser's content to merge it in.
4. Run the cheap dedup pass:

   ```bash
   "$PYTHON_BIN" tools/research_wiki.py dedup-edges wiki/
   "$PYTHON_BIN" tools/research_wiki.py dedup-citations wiki/
   ```

5. Tear down worktrees:

   ```bash
   git worktree remove "$WT_PATH"
   git branch -d "$WT_BRANCH"
   ```

6. **Advance `BASE_COMMIT`**:

   ```bash
   BASE_COMMIT=$(git rev-parse HEAD)
   ```

   Persist via `checkpoint-set-meta` so resume can pick up.

The expensive rebuilds (`rebuild-index`, `rebuild-context-brief`, `rebuild-open-questions`) and `lint.py --fix` run once after the **last** batch, not per batch. Running them per batch is correct but wasteful — the cross-batch invariant is that derived files are valid at the end of the run, not at every intermediate step.

## Checkpoint and resume

Two files together describe run state:

- `.checkpoints/batch-ingest-sources.json` — the full manifest. Immutable for the duration of one run.
- `.checkpoints/batch-ingest-state.json` — `{"last_completed_batch": N, "base_commit": "<sha>", "stash_ref": "...", "base_branch": "..."}`. Updated after every batch fan-in.

On `/batch-ingest` re-invocation with the same input:

- if both files exist and the manifest matches the input, jump to batch `last_completed_batch + 1` using the stored `base_commit`
- if the user passes a different input or the manifest is missing, treat as a fresh run

`tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...` is the durable record; the `.checkpoints/batch-ingest-state.json` file is a convenience mirror so the skill can read state without invoking the tool.

## What `/batch-ingest` does not do

- does not commit inside subagents — that is the subagent's contract
- does not rebuild derived graph files between batches — only after the last
- does not create `Summary/` pages — defer to `/edit`
- does not call the discovery planner — that is `/init`'s job
- does not write to `raw/papers/`, `raw/notes/`, or `raw/web/`
