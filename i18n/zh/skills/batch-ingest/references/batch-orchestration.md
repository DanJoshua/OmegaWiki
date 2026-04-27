# /batch-ingest 编排

一次批量运行如何切片、fan-out、fan-in。准备进入 SKILL.md 的 step 3 或 step 4 时打开本文。

## 为什么要分批

`/init` 把所有论文一次性 fan-out，再一次性 fan-in。这能跑得通，是因为 `/init` 控制输入规模（≤10 篇），跨论文一致性的代价对 bootstrap 来说可以接受。

`/batch-ingest` 面对的是长尾：5 篇也行，50 篇也行。一次性 fan-out 在兄弟 worktree 之间无法共享 `find-similar-concept`——每个 worktree 都从同一个 commit 出发，看到的是同一份 wiki。结果就是重复的 concept、重复的 claim、缺失的 paper-paper edge。

修法是顺序批次。批内并行（便宜、隔离），批间父进程把 worktree merge 回主分支，并在下一批 fan-out 前**把 `BASE_COMMIT` 推进到新的 HEAD**。下一批的 worktree 就从一棵已经包含了前面所有批次 slug 的 tree 出发，subagent 内的 `find-similar-*` 自然能看到，倾向于合并而不是新建。

这就是 SKILL.md 中批次循环为什么是顺序而不是并行的原因。略过 `BASE_COMMIT` 的推进就把整个设计的支柱抽掉了。

## 为什么按时间排序

切批之前，先把论文按时间从旧到新排序。原因是去重的偏向：当两篇论文给出重叠的 claim 时，`/ingest` 的去重逻辑会保留已有 claim 并把新证据追加上去。先 ingest 旧的，意味着新的 claim 贡献会落在已有结构之上对其进行**精炼**——这与人类研究图景一致：旧文献是底，新文献是不断细化它的修正。倒过来则是新 claim 被当作基线，旧文献的证据被当作事后补丁——读起来像是历史在倒放。

年份缺失的论文排到**队首**，不是队尾。理由是缺 S2 年份的论文通常是更早于 S2 语料库的老作品，而不是未发表的草稿。前置它们等于把它们当作最古老的层，与现实相符，并保持去重偏向的一致性。

## Batch size

默认 `B = max(ceil(sqrt(N)), 4)`，其中 `N` 是 prepare 后的 source 数量。

| N   | B  | batches |
|-----|----|---------|
| 4   | 4  | 1       |
| 9   | 4  | 3       |
| 16  | 4  | 4       |
| 25  | 5  | 5       |
| 100 | 10 | 10      |

两个维度都随 `N` 缓慢增长，所以 100 篇是 10 批 × 10，而不是 25 批 × 4（fan-in 太频繁）或 4 批 × 25（批内冲突太多）。用户可用 `--batch-size N` 覆盖。

## Fan-out 前的安全协议

与 `/init` 的 parallel ingest 流程一致，把 `init-*.json` 路径换成 `batch-ingest-*.json`：

1. `git status --short`。把 `wiki/`、`raw/tmp/`、`raw/discovered/`、`.checkpoints/batch-ingest-*.json` 视为 scaffold；其它脏文件 stash 掉。
2. 检查 `.gitattributes` 中 `wiki/log.md`、`wiki/graph/edges.jsonl`、`wiki/graph/citations.jsonl`、`wiki/index.md` 都声明了 `merge=union`。否则每批 fan-in 都会冲突。
3. 拒绝 detached HEAD。停下让用户切到或新建命名分支。
4. 在 fan-out 前把 scaffold（step 2 创建的 topic 壳）与 manifest commit，使 `BASE_COMMIT` 携带 subagent 必须继承的状态：

   ```bash
   git add wiki/ raw/tmp/ raw/discovered/ .checkpoints/batch-ingest-sources.json
   git commit -m "batch-ingest: scaffold before parallel ingest" --no-gpg-sign
   BASE_COMMIT=$(git rev-parse HEAD)
   BASE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
   ```

5. 通过 `tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...` 记录 `stash_ref`、`base_branch`、`base_commit`。

## Worktree 创建

对当前批次的每篇论文：

```bash
WT_BRANCH="batch-${BASE_BRANCH//\//-}-${b}-${ingest_rank}-${paper_slug}"
WT_PATH="../.worktrees/$WT_BRANCH"
git worktree add -b "$WT_BRANCH" "$WT_PATH" "$BASE_COMMIT"
```

- 从**当前** `BASE_COMMIT` 拉分支，不要直接从 `BASE_BRANCH` 拉。git 会拒绝 `worktree add` 到一个已经在主工作区被 check out 的分支。
- 批内顺序按 manifest 中的 `ingest_rank`，不要重新扫描 raw 目录。

## Subagent prompt 协议

每个 subagent 在 BATCH MODE 下对一篇论文跑一次 `/ingest`。prompt 必须：

- 给出 canonical 源路径，**只用相对路径**（不要带父进程环境的绝对路径）
- 显式声明 `BATCH MODE`，以便 subagent 拿到正确的 skip-list
- 要求 subagent 在退出前在 worktree 内 commit

`/ingest` 在 BATCH MODE 下的 skip 列表（与 INIT MODE 精神一致）：

- 跳过 `fetch_s2.py citations`
- 跳过 `fetch_s2.py references`
- 跳过 per-subagent `rebuild-index`
- 跳过 per-subagent `rebuild-context-brief`
- 跳过 per-subagent `rebuild-open-questions`
- 跳过容易冲突的 topic 创建（父进程已经在 step 2 把壳准备好了）
- 把 `raw/` 视为严格只读——不要在 subagent 内写 `raw/tmp/` 或 `raw/discovered/`

完整参考：`skills/ingest/references/batch-mode.md`。

## 每批的 fan-in

当前批次所有 worktree 都已 commit 之后：

1. 必要时把主工作区切回 `BASE_BRANCH`。
2. 按 `ingest_rank` 顺序依次 merge 各 worktree 分支：

   ```bash
   git merge --no-ff "$WT_BRANCH" --no-edit
   ```

3. 保守解决 concept/claim 冲突。两个 worktree 都创建了 `concepts/foo.md` 时，保留先 merge 的版本，对落败者重新 `find-similar-concept` 把内容并入。
4. 跑轻量 dedup：

   ```bash
   "$PYTHON_BIN" tools/research_wiki.py dedup-edges wiki/
   "$PYTHON_BIN" tools/research_wiki.py dedup-citations wiki/
   ```

5. 拆 worktree：

   ```bash
   git worktree remove "$WT_PATH"
   git branch -d "$WT_BRANCH"
   ```

6. **推进 `BASE_COMMIT`**：

   ```bash
   BASE_COMMIT=$(git rev-parse HEAD)
   ```

   通过 `checkpoint-set-meta` 落地，保证 resume 能用。

重型 rebuild（`rebuild-index`、`rebuild-context-brief`、`rebuild-open-questions`）与 `lint.py --fix` 在**最后一批**之后跑一次，不每批跑。每批跑也对，但浪费——跨批次的不变量是"运行结束时 derived 文件正确"，不是"每个中间步骤都正确"。

## Checkpoint 与 resume

两份文件共同描述运行状态：

- `.checkpoints/batch-ingest-sources.json` —— 完整的 manifest。一次运行内不可变。
- `.checkpoints/batch-ingest-state.json` —— `{"last_completed_batch": N, "base_commit": "<sha>", "stash_ref": "...", "base_branch": "..."}`。每批 fan-in 后更新。

当用户用同一输入再次调用 `/batch-ingest`：

- 两份文件都在且 manifest 与输入匹配——从 `last_completed_batch + 1` 起，使用记录中的 `base_commit`
- 用户传了不同输入，或 manifest 缺失——按全新一次跑处理

`tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...` 是耐久记录；`.checkpoints/batch-ingest-state.json` 是给 skill 直接读取的便捷镜像。

## `/batch-ingest` 不做的事

- 不在 subagent 里 commit——那是 subagent 自己的协议
- 不在批之间 rebuild derived graph 文件——只在最后一批之后做
- 不创建 `Summary/` 页面——交给 `/edit`
- 不调用 discovery planner——那是 `/init` 的活儿
- 不写 `raw/papers/`、`raw/notes/`、`raw/web/`
