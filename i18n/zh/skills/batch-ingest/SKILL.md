---
description: 批量把多篇论文 ingest 进 wiki，按时间顺序排队，分成小批次并行运行，并在批次之间共享状态。当用户指向 `raw/papers/` 下的一个 PDF 目录或一个包含 arXiv URL 的 `.md` / `.txt` 文件，要求批量加入、说 "batch ingest"、"把这些论文都收进来"，或者交付一个对单次 `/ingest` 来说太大的论文集合时触发。
argument-hint: <pdf-dir-or-url-list-file> [--batch-size N]
---

# /batch-ingest

把多次 `/ingest` 编排成一次批量任务。每个批次把一小组论文 fan-out 到并行的 `/ingest` subagent 中，subagent 各自在独立的 git worktree 内运行；父进程把这一批 merge 回主分支后，下一批从新的合并 commit 出发再次 fan-out。批次之间的顺序处理与按时间排序天然地解决了单次 `/ingest` 看不到的跨论文一致性问题——paper-to-paper edge、概念去重、claim 去重大都在这种结构下自动收敛。

`/batch-ingest` 只负责编排，所有写页面的工作都通过 `/ingest` 在 **BATCH MODE** 下完成，参见 `skills/ingest/references/batch-mode.md`。

按需打开下列本地参考文件：

- `references/inputs.md` —— 支持的输入形式（PDF 目录 vs URL 列表文件）与恢复规则
- `references/batch-orchestration.md` —— 时间排序的理由、分批策略、worktree 协议、fan-in 节奏、checkpoint 与 resume

## Inputs

- `<pdf-dir-or-url-list-file>` —— 二选一：
  - `raw/papers/` 下的一个目录，含若干 `.pdf`（递归扫描）
  - 一个 `.md` 或 `.txt` 文件，每行一条 arXiv URL（可放在项目任意位置）
- `--batch-size N`（可选）：覆盖默认值 `max(ceil(sqrt(N)), 4)`

`/batch-ingest` 不做 discovery，不调用 planner，不写 notes/web 衍生的临时页面——这些是 `/init` 的职责。v1 也不创建 `wiki/Summary/`，需要时交给 `/edit`。

## Outputs

- 每篇输入论文一个完整连接的 paper 页面，加上 `/ingest` 创建的所有相关实体
- 经 `tools/research_wiki.py` 追加的 graph edges 与 citations
- `.checkpoints/batch-ingest-sources.json` —— 按时间排序的 manifest，是 ingest 顺序的唯一真理
- `.checkpoints/batch-ingest-state.json` —— 最后一个完成的 batch 序号，用于 resume
- 更新后的 `wiki/index.md`、`wiki/log.md`、`wiki/graph/*`
- 终端汇总报告，按批次分组并列出跳过的论文

## Wiki Interaction

### Reads

- 输入目录或 URL 列表文件
- `wiki/index.md` 与已有页面用于查重
- `.checkpoints/batch-ingest-sources.json` 与 `.checkpoints/batch-ingest-state.json` 用于 resume

### Writes

- `raw/tmp/` —— 用户本地 PDF 的 prepared sidecar
- `raw/discovered/` —— URL 列表对应的 arXiv 源
- `wiki/topics/{slug}.md` —— 当输入中至少有 2 篇论文明显属于同一 topic 且对应页面尚未存在时 CREATE 一个 topic 壳（仅 scaffold 阶段）
- `wiki/index.md`、`wiki/log.md`、`wiki/graph/*` —— 通过 `tools/research_wiki.py` 与 `/ingest` subagent 间接更新
- `.checkpoints/batch-ingest-sources.json`、`.checkpoints/batch-ingest-state.json`、以及 `batch-ingest-session` checkpoint metadata

### Graph edges created

- `/batch-ingest` 自身不创建 edge；所有论文驱动的 edge 委托给 `/ingest`。

## Workflow

**Pre-condition**：当前工作目录是项目根目录，包含 `wiki/`、`raw/`、`tools/`。设置 `WIKI_ROOT=wiki/`。一次性解析 `PYTHON_BIN` 并在整个 workflow 中复用：

```bash
# 通过 git 找到项目根，让 worktree 中的 subagent 也能定位 .venv。
# .venv 被 gitignore，subagent 的 cwd 在 ../.worktrees/<branch>/ 时本地没有
# .venv——若不解析项目根，PYTHON_BIN 会回退到系统 python3，既丢失 .env 里的
# API key，也丢失安装的依赖（deepxiv-sdk 等）。
# git rev-parse --git-common-dir 无论 cwd 位于哪个 worktree 都返回主仓库的
# .git 目录；其父目录即项目根。
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

确认 wiki 已经初始化（`wiki/index.md` 与 `wiki/graph/` 存在）。如未初始化，请先要求用户运行 `/init`——`/batch-ingest` 不负责 bootstrap 一个空 wiki。

### Step 1: 准备 manifest

```bash
"$PYTHON_BIN" tools/batch_ingest.py prepare \
  --input <pdf-dir-or-url-list-file> \
  --raw-root raw \
  --output-manifest .checkpoints/batch-ingest-sources.json
```

工具会解析每个输入：把用户本地 PDF prepare 到 `raw/tmp/`，把 URL 列表中的 arXiv 源下载到 `raw/discovered/`，通过 Semantic Scholar 查询发表年份，按时间排序（年份缺失的论文被排到最前——见 `references/batch-orchestration.md`），并计算默认 batch size。manifest 是 ingest 顺序的唯一真理；此后不再重新扫描输入。

如果用户指定 `--batch-size N`，覆盖 `manifest["batch_size"]` 并重新计算 `manifest["batch_count"]`，再继续。如果 manifest 中可用源数量为 0，停止并报告。

### Step 2: Fan-out 前的 scaffold

读取 manifest 中各条目的 `title`，按明显共享的 topic 分组。对每个至少含 2 篇论文且尚无 `wiki/topics/{slug}.md` 的组，创建一个最小 topic 壳（仅 frontmatter——`name`、`tags`、空的 `## Overview`）。slug 来自 `tools/research_wiki.py slug`。**不要**往壳里塞论文行：subagent 在 BATCH MODE 下不写 topic（见 `skills/ingest/references/batch-mode.md`），单篇内容更新交给 fan-in 之后的 `/edit`。v1 **不**创建 `Summary/` 页面，同样交给 `/edit`。

这一步要保守：信号弱的组宁可跳过。错误的 topic 壳比缺失的 topic 壳更难撤销。

### Step 3: Fan-out 前的安全协议

与 `/init` 的 parallel ingest 流程相同（完整细节见 `references/batch-orchestration.md`）。要点：

- stash 与 `wiki/`、`raw/`、`.checkpoints/batch-ingest-*.json` 无关的脏文件
- 检查 `.gitattributes` 中 `wiki/log.md`、`wiki/graph/edges.jsonl`、`wiki/graph/citations.jsonl`、`wiki/index.md` 都声明了 `merge=union`
- 拒绝 detached HEAD；要求当前在命名分支上
- 在 fan-out 之前 commit scaffold（topic 壳）+ manifest，使 `BASE_COMMIT` 携带每个 worktree 必须继承的状态
- 通过 `tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session ...` 记录 `stash_ref`、`base_branch`、`base_commit`

### Step 4: 批次循环

按顺序遍历 batch index `b` ∈ `[0, batch_count)`：

1. Resume 检查：读取 `.checkpoints/batch-ingest-state.json`（若存在）；若 `b <= last_completed_batch`，跳过。
2. 从 manifest 中按 `ingest_rank` 顺序取出接下来 `manifest["batch_size"]` 个 source。
3. 对该批次内每个 source 并行处理：
   - 从**当前** `BASE_COMMIT` 创建 worktree：

     ```bash
     WT_BRANCH="batch-${BASE_BRANCH//\//-}-${b}-${ingest_rank}-${paper_slug}"
     WT_PATH="../.worktrees/$WT_BRANCH"
     git worktree add -b "$WT_BRANCH" "$WT_PATH" "$BASE_COMMIT"
     ```

   - Spawn subagent，让它在 BATCH MODE 下对该 source 的 `canonical_ingest_path` 跑 `/ingest`。subagent 协议与 INIT MODE 完全一致：跳过 per-subagent rebuild、跳过 topic 写入、退出前在 worktree 内 commit。详见 `skills/ingest/references/batch-mode.md`。
4. 对当前批次执行 fan-in：
   - 按 `ingest_rank` 顺序把每个 worktree 分支 merge 回 `BASE_BRANCH`（`git merge --no-ff --no-edit`）。
   - 对真正的 concept/claim 冲突保守处理——合并，不要让近似重复增殖。
   - 跑轻量 dedup：

     ```bash
     "$PYTHON_BIN" tools/research_wiki.py dedup-edges wiki/
     "$PYTHON_BIN" tools/research_wiki.py dedup-citations wiki/
     ```

   - 在批次之间**不**跑 `rebuild-context-brief`、`rebuild-open-questions`、`rebuild-index`，留给 step 5。
   - 拆 worktree：`git worktree remove "$WT_PATH" && git branch -d "$WT_BRANCH"`。
5. **把 `BASE_COMMIT` 推进到新的 `HEAD`**。这就是跨批次去重的核心机制：下一批 worktree 从已经包含前面所有批次 slug 的 tree 出发，subagent 内的 `find-similar-concept`、`find-similar-claim` 自然能看到它们。
6. 更新 state checkpoint：

   ```bash
   "$PYTHON_BIN" tools/research_wiki.py checkpoint-set-meta wiki/ batch-ingest-session last_completed_batch "$b"
   ```

   同时把 `.checkpoints/batch-ingest-state.json` 写为 `{"last_completed_batch": b, "base_commit": "<sha>"}`，便于 resume。

### Step 5: 最终 rebuild

最后一批结束后：

```bash
"$PYTHON_BIN" tools/research_wiki.py rebuild-index wiki/
"$PYTHON_BIN" tools/research_wiki.py rebuild-context-brief wiki/
"$PYTHON_BIN" tools/research_wiki.py rebuild-open-questions wiki/
"$PYTHON_BIN" tools/lint.py wiki/ --fix
```

如果存在 `stash_ref`，pop 它。pop 失败则保留 checkpoint 并报告需要手动恢复的步骤。

### Step 6: 报告

输出一份精简汇总，覆盖：

- 总论文数，按 origin 分组（`user_local` 来自 `raw/tmp/`，`introduced` 来自 `raw/discovered/`）
- 每个批次的明细：成功 ingest、跳过、失败
- step 2 创建的 topic 壳
- `/ingest` 累计创建与更新的页面数
- subagent 浮现出来的矛盾或高被引外部参考文献

最后一行收束：

```
Wiki: +{P} papers, +{C} claims, +{K} concepts, +{E} edges across {B} batches
```

## Constraints

- 输入互斥：每次调用要么是 PDF 目录，要么是 URL 列表文件，不混用。需要混用时分两次跑。
- PDF 目录必须位于 `raw/papers/` 下，因为 `prepare_paper_source.py` 要求路径相对于项目 `raw_root`。URL 列表文件可以放在项目任意位置。
- `/batch-ingest` 可以写 `raw/tmp/` 下的 prepared sidecar 与 `raw/discovered/` 下的外部抓取产物，但绝不能写 `raw/papers/`、`raw/notes/`、`raw/web/`。
- v1 不创建 `wiki/Summary/`。
- 所有论文 ingest 必须通过 `/ingest` BATCH MODE 子代理在 worktree 内执行，不可绕过 `/ingest`。
- Step 4 必须从 `.checkpoints/batch-ingest-sources.json` 读取输入，不准临时扫描目录。
- 每批结束后**必须**推进 `BASE_COMMIT`——这是跨批次去重的机制本身，不是优化。跳过它就把整个设计打废了。

## Error Handling

- **Fan-out 前处于 detached HEAD**：停下，让用户切到或新建命名分支。
- **某篇论文 prepare 失败**：在 manifest 中记录 warning，继续其它论文。被跳过的论文出现在最终报告中。
- **某篇论文在 worktree 内 ingest 失败**：不阻塞当前批次的 fan-in；跳过失败 worktree 的 merge，把这篇论文列入报告。Resume 时可移除对应 manifest 条目后重跑。
- **Prepare 阶段 S2 不可用**：年份会变成 `null`，受影响的论文聚集在队首；流水线照常推进；在报告中标记排序质量下降。
- **批次内 slug 冲突**：因 `/ingest` 的单篇创建上限而很罕见；fan-in 时按先到先得的策略保留先合并的版本，对落败者重新 `find-similar-*`，与 `/init` 一致。
- **结尾 stash pop 失败**：保留 checkpoint，让用户手动恢复。

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

- `/ingest` —— 在每个 worktree 子代理内以 BATCH MODE 运行（`skills/ingest/references/batch-mode.md`）
- `/init` —— 首次 wiki bootstrap 的独立 skill；`/batch-ingest` 假定 `/init` 已经跑过

### External APIs used by `tools/batch_ingest.py`

- Semantic Scholar (`paper`) 用于年份查询与 discovered 论文的标题
- arXiv 源下载（通过 `init_discovery.download_to_discovered`）
