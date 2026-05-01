---
description: 每日 arXiv 收集、wiki 去重、digest 生成与邮件通知；推荐和可选 auto-ingest 留作后续阶段
argument-hint: "[--hours 24] [--categories <cat...>] [--max-items 20] [--send-email true|false]"
---

# /daily-arxiv

> 监听每日 arXiv 时间窗口，按 wiki 已有论文去重，生成简洁 digest，并通过邮件通知用户。当前自动化 scaffold 只负责 inform：不打分、不下载、不 ingest、不修改 wiki。

按需读取这些本地 reference：

- `references/automation-scaffold.md` — GitHub Actions scaffold、SMTP secrets、artifacts 与失败行为
- `references/recommendation-and-ingest-policy.md` — 后续推荐信号、决策模式与 auto-ingest 约束

## Inputs

- `--hours N`：拉取最近 N 小时的论文（默认 24）
- `--categories <cat...>`：覆盖默认 arXiv 分类（`cs.LG cs.CV cs.CL cs.AI stat.ML`）
- `--max-items N`：digest 中最多展示的新候选论文数（默认 20）
- `--send-email true|false`：workflow 专用的 SMTP 发送开关；手动 dry run 可设为 `false`

## Outputs

- GitHub Actions artifacts：`feed.json`、`digest.md`、`digest.json`
- 包含 Markdown digest 的 GitHub Actions job summary
- 可选的 SMTP 邮件，正文与 `digest.md` 相同

当前 scaffold 不写 `wiki/`、不写 `raw/`、不提交 commit。后续 auto-ingest 必须显式 opt-in，并且所有论文纳入都要交给 `/ingest`。

## Wiki Interaction

### Reads

- `wiki/index.md` 与 `wiki/papers/*.md` — 用 arXiv URL / ID 做去重

### Writes

- 当前 scaffold 不写任何 wiki 文件

### Graph edges created

- 无。图谱和实体变更属于 `/ingest`。

## Workflow

1. 拉取 feed：

   ```bash
   python3 tools/fetch_arxiv.py --hours <hours> [-o <feed.json>] [--categories <cat...>]
   ```

2. 生成 digest：

   ```bash
   python3 tools/daily_arxiv.py digest --feed <feed.json> --wiki-root wiki --out-md <digest.md> --out-json <digest.json> --max-items <N>
   ```

3. 启用邮件时发送：

   ```bash
   python3 tools/send_email.py --subject "<subject>" --body-file <digest.md>
   ```

4. 查看 artifact 或邮件。不要从当前 scaffold 调用 `/ingest`。

## Relationship to Neighboring Skills

- `/discover` 是基于用户给定 anchor、topic 或当前 wiki 状态的主动推荐。它只给 next-read 建议，永不自动 ingest。
- `/daily-arxiv` 是时间窗口流处理器，从新 arXiv 论文出发，目标是每日通知。
- `/ingest` 仍然是唯一负责把选定论文纳入 `wiki/`、`raw/discovered/` 和图谱文件的 skill。

## Constraints

- CI 保持 deterministic：scaffold workflow 不调用 Claude Code，也不需要 `ANTHROPIC_API_KEY`。
- 推荐策略不要写进 workflow YAML；确定性逻辑放在 `tools/`，编排策略放在 references。
- 在 selection 已实现、显式 opt-in、并受 workflow mode 保护之前，不要 auto-ingest。
- scaffold 只支持 SMTP 作为通知方式。
- 当前运行历史来自 GitHub Actions artifacts，而不是每日 commits。

## Error Handling

- **RSS 拉取失败**：在生成 digest 前让 workflow 失败。
- **SMTP secrets 缺失**：当 `--send-email true` 时给出清晰配置错误；手动 `send_email=false` 仍应生成 artifacts。
- **RSS 为空或全部已去重**：生成合法的空 digest 和 artifact，运行成功。
- **后续外部 API 不可用**：在 digest 中保留 degraded-mode 说明，不要把缺失 enrichment 当作 ingest 依据。

## Dependencies

### Tools

- `tools/fetch_arxiv.py` — arXiv RSS 收集
- `tools/daily_arxiv.py digest` — 确定性的 inform-only digest
- `tools/send_email.py` — SMTP 发送

### Future tools / APIs

- `tools/fetch_s2.py` — Semantic Scholar 元数据与推荐信号
- `tools/fetch_deepxiv.py` — DeepXiv trending、TLDR 与 social-impact 信号
- `/ingest` — 仅用于后续 opt-in 的论文纳入
