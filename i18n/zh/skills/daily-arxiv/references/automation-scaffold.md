# Daily arXiv Automation Scaffold

GitHub Actions workflow 是当前 `/daily-arxiv` 的生产自动化路径。它只验证每日收集、去重、artifact 与 SMTP 通知闭环，不允许 CI 修改 wiki。

## Schedule and dispatch

- 定时运行：`17 0 * * *` UTC，即北京时间 08:17。
- 手动运行：`workflow_dispatch`，支持 `hours`、`categories`、`max_items`、`send_email`。
- 使用非整点分钟，降低 GitHub scheduled workflow 在整点高峰延迟或丢弃的概率。
- workflow 仍是 inform-only 时保持 `permissions: contents: read`。

## Secrets

SMTP 发送读取这些 repository secrets：

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `DAILY_ARXIV_EMAIL_TO`

当前 scaffold 不运行 Claude Code，因此不需要 `ANTHROPIC_API_KEY`。如果后续推荐层使用 LLM，应把它作为单独的可选 recommender 依赖。

## Artifacts

每次运行上传：

- `feed.json` — `tools/fetch_arxiv.py` 之后的原始 arXiv RSS 结果
- `digest.md` — 人类可读邮件正文
- `digest.json` — 机器可读 scaffold payload

workflow 也会把 `digest.md` 写入 GitHub Actions job summary。在 auto-ingest 实现并显式开启 repo 写权限前，不要提交每日 artifacts。

## Failure behavior

- 只有 `send_email=true` 时，缺少 SMTP secrets 才会让 workflow 失败。
- `send_email=false` 的手动运行是合法 dry run，仍会上传 artifacts。
- 空 feed 或全部被去重的 feed 是成功运行，digest 对应小节为空。
- fetch 失败应在尝试发送邮件前让运行失败。
