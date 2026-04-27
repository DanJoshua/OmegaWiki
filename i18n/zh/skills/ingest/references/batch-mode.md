# /ingest BATCH MODE

当 `/ingest` 由 `/batch-ingest` 作为并行 subagent 调起时，打开本文。BATCH MODE 与 INIT MODE 共用相同的并行安全机制，差别在于哪份 manifest 驱动运行、父进程的 fan-in 节奏不同。

## BATCH MODE 何时生效

源路径来自 `.checkpoints/batch-ingest-sources.json` 时，BATCH MODE 生效。父进程 `/batch-ingest` 在隔离的 git worktree 内一篇论文跑一次 `/ingest`，按时间分批；父进程的协议见 `skills/batch-ingest/references/batch-orchestration.md`。

BATCH MODE 下：

- 源是 `/batch-ingest` 已经准备好的 `canonical_ingest_path`（用户本地 PDF 对应 `raw/tmp/...`，arXiv URL 对应 `raw/discovered/...`）
- `raw/` 严格只读——不要在 `raw/tmp/`、`raw/discovered/` 或其它 `raw/` 子目录下写
- **跳过** `fetch_s2.py citations <arxiv-id>` 与 `fetch_s2.py references <arxiv-id>`——citation 由父进程在 fan-in 时统一处理
- **跳过** per-subagent 的 `rebuild-context-brief`、`rebuild-open-questions`、`rebuild-index`——父进程在最后一批之后跑一次
- **跳过**所有 topic 写入——包括对现有 topic 页面的追加。父进程在 scaffold 阶段可能已经建好壳，但单篇论文带来的内容更新留给 fan-in 之后的 `/edit` 处理。多个兄弟 subagent 并发追加会触发 merge 冲突；在 topic 写入这一点上与 INIT MODE 对齐能保持并行安全协议简洁，且与 `/check`/`/edit` 已经承担的批量后处理一致。

其它一切——paper 页面创建、用 `find-similar-*` 做 concept/claim 去重、people 页面规则、paper 的 `## Related` 链接、concept/claim/foundation 的 graph edge——都按正常方式跑。

## 如何识别 BATCH MODE

`/batch-ingest` 在 subagent prompt 里给出 canonical 路径并显式声明 BATCH MODE。出现以下任一信号即识别为 BATCH MODE：

- 源路径以 `raw/tmp/` 或 `raw/discovered/` 开头，**且** `.checkpoints/batch-ingest-sources.json` manifest 中有该路径
- subagent prompt 中显式写了 `BATCH MODE`

两个信号都没有，但 `init-sources.json` 中有该路径——那是 INIT MODE，见 `references/init-mode.md`。两个 manifest 都不匹配时，把这次调用当成用户直接调用。

## 为什么独立成一个 mode

INIT MODE 与 BATCH MODE 在 `/ingest` 内部跳过的步骤集合相同，差别在父进程：

- `/init` 一次大 fan-out + 一次 fan-in，重型 rebuild 跑一次
- `/batch-ingest` 顺序分批 fan-out，批之间推进 `BASE_COMMIT`，重型 rebuild 留到最后一批之后

从 `/ingest` 的视角看两种 mode 一样；保留两个名字是为了让两个父 skill 各自演进 fan-in 策略时不互相打架。日后若发现某行为只在某一种 mode 下需要，倾向于把它加在那一种 mode 里，而不是把两个名字合并掉。

## 并行写入安全

INIT MODE 的三条规则同样适用（详见 `references/init-mode.md`）：

1. **所有共享文件写入都通过工具。** `graph/edges.jsonl`、`graph/citations.jsonl`、`index.md`、`log.md` 经由 `tools/research_wiki.py add-edge`、`add-citation`、index 更新、`log` 写入。工具层使用 append 语义；`.gitattributes` 对这些路径声明了 `merge=union`。
2. **slug 由 `tools/research_wiki.py slug "<title>"` 确定性分配。** 两个 worktree 拿到相同 title 会拿到相同 slug，冲突由父进程在 fan-in 解决。
3. **绝不锁定或就地重写共享文件。**

## 跨批次 slug 冲突

`/batch-ingest` 跨批次去重的机制在于每批之间把 `BASE_COMMIT` 推进，所以第二批中的论文已经能看到第一批创建的 concept slug。从 `/ingest` 的视角，这与 ingest 一个已填充的 wiki 没有区别——`find-similar-concept` 会返回已有 slug，按合并去重的常规规则处理，无需特殊代码。

批内仍可能两个兄弟 subagent 都要新建同一个 concept。`/ingest` 的单篇创建上限（见 `references/dedup-policy.md`）已经把这个面减到最小；`/batch-ingest` 的批内 fan-in 会按保守策略合并冲突。

## `/ingest` 不替 `/batch-ingest` 做的事

- 不 commit（subagent prompt 自己负责在 worktree 内 commit）
- 不 stash、不切分支
- 不 merge worktree、不推进 `BASE_COMMIT`、不跑 `dedup-edges` / `dedup-citations` / `rebuild-*`——这些是 `/batch-ingest` 的 fan-in 操作
