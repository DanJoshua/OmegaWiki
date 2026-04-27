# /batch-ingest 输入

`/batch-ingest` 每次调用只接受一种输入。形式由后缀和文件类型决定，不做混合自动识别。

## 形式 A：PDF 目录（用户本地）

`raw/papers/` 下的一个目录，含一个或多个 `.pdf`。扫描是**递归**的，所以 `raw/papers/2025-survey/*.pdf` 与 `raw/papers/2025-survey/sub/*.pdf` 都会被纳入。

规则：

- 目录必须位于 `raw/papers/` 下。`tools/batch_ingest.py prepare` 内部调用 `prepare_paper_source.prepare_paper_source(...)`，要求每个输入路径都能解析到项目 `raw_root` 之下。
- 每个 PDF 都视为用户拥有的资产。`/batch-ingest` 会在 `raw/tmp/` 下写入 prepared sidecar（恢复出的 TeX 或合成 TeX），但不会复制、移动或改写原始 PDF。
- arXiv ID 恢复尽力而为，按以下顺序尝试：文件名 / 上层路径 → `prepare_paper_source` 的 PDF metadata 启发式 → Semantic Scholar 标题搜索。即便 arXiv ID 恢复失败，论文仍会被 ingest，只是缺 S2 metadata。这类条目年份为 `null`，会被排到队首。
- manifest 中这类条目的 `origin` 为 `"user_local"`，`canonical_ingest_path` 优先指向 `raw/tmp/` 下的 prepared sidecar，没有时回退到 `raw/papers/...`。

典型场景：用户丢过来一堆 PDF（arXiv 抓取、workshop proceedings 下载、个人阅读列表），希望一次性吸收。

## 形式 B：URL 列表文件

一个 `.md` 或 `.txt` 文件（位置随意），每行一条 arXiv URL。解析比较宽松：

- 空行和以 `#` 开头的行被跳过
- markdown 列表项（`- ...`、`* ...`）的引导符号会被剥掉
- markdown 链接 `[label](https://arxiv.org/abs/...)` 接受，从中抽 URL
- 裸 URL 接受

v1 只识别 arXiv URL（`arxiv.org/abs/...`、`arxiv.org/pdf/...`、`arxiv.org/html/...`）。其它 URL 静默忽略——会出现在 warnings 中但不阻塞流程。

规则：

- arXiv 源压缩包下载到 `raw/discovered/{slug}/`（优先 TeX，回退 PDF）——与 `/init` 处理 introduced 论文使用同一份策略。
- discovered slug 用到的标题来自 Semantic Scholar；S2 不可用时回退为 `arxiv-{id}`，依然能 ingest。
- manifest 中这类条目的 `origin` 为 `"introduced"`，`canonical_ingest_path` 指向 `raw/discovered/` 下下载得到的源。

典型场景：用户已经整理好一份阅读清单（`survey.md`、Slack 导出、随手的 `urls.txt`），希望 wiki 把它们吸收进来。

## 混用两种形式

v1 不支持在一次调用里混用本地 PDF 与 URL。两条路径的 prepare 成本不同，失败模式不同（文件系统 vs 网络），可用的排序信号也不同（文件 mtime 回退 vs 无）。需要两种都做时分两次跑 `/batch-ingest`——第二次仍能享受跨批次一致性，因为它会从第一次合并好的 commit 出发。

## 单条输入失败时怎么办

`tools/batch_ingest.py prepare` 在单篇失败时不中断，把警告写入 `manifest["warnings"]`。skill 应当：

- 如果**全部**失败，停止并报告——`/batch-ingest` 在空 manifest 上跑没有意义
- 如果只有部分失败，继续运行，把警告反映到最终报告里，方便用户后续单篇重试（通常用直接的 `/ingest`）

每篇内部的恢复策略见 `skills/ingest/references/error-handling.md`，`/batch-ingest` 不重复实现。
