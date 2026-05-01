# Daily arXiv Recommendation and Ingest Policy

本 reference 面向后续 `/daily-arxiv` 推荐层。当前 inform-only scaffold 尚未实现这些能力。

## Phase boundary

保持 pipeline 阶段清晰：

1. 收集新的 arXiv 论文。
2. 按 wiki 已有论文去重。
3. 用可选外部信号增强候选。
4. 打分并选择候选。
5. 通过 digest 通知。
6. 只有 mode 允许时，才可选地 ingest 选中论文。

workflow 与邮件层不应关心具体由哪个 recommender 填充 `digest.json` 中的 `score`、`signals`、`rationale` 或 `decision`。

## Recommendation signals

新增逻辑前先使用已有集成：

- Semantic Scholar：recommendations、citations、references、citation counts、influential citation counts、fields of study、作者元数据。
- DeepXiv：trending papers、TLDR、keywords、social impact、论文结构。
- Wiki context：已有 topics、concepts、open questions、recent ingests。

优先批量打分。除非有明确质量收益和 rate-limit 预算，不要逐篇调用 LLM。

## Decision modes

- `inform`：默认。只发送推荐，不下载、不 ingest。
- `auto-ingest`：后续 opt-in 模式。把选中论文下载到 `raw/discovered/`，将 canonical path 交给 `/ingest`，并提交生成的 wiki 变更。

不要从 repository 状态推断 `auto-ingest`。必须由用户或 workflow input 显式选择。

## Auto-ingest guardrails

- `/ingest` 负责所有论文纳入。`/daily-arxiv` 不得手写 paper pages、concepts、claims、people、graph files 或 index entries。
- 外部论文 artifact 只能下载到 `raw/discovered/`。
- 不要触碰 `raw/papers/`、`raw/notes/`、`raw/web/`、`raw/tmp/`。
- 只有 auto-ingest 实现后，workflow 才能添加 `contents: write`。
- 真正发生 ingest 时，应同时提交 `wiki/` 和 `raw/discovered/` 的变更。
- 每次 auto-ingest 数量必须有上限，并在 digest 中保留失败项，不要静默隐藏。

## Relationship to `/discover`

`/discover` 回答用户主动提出的 “what should I read next?”，来源可以是 anchors、topic 或 wiki。`/daily-arxiv` 监听 fresh-paper stream。后续两者可以共享确定性 scoring helpers，但入口和用户意图不同。
