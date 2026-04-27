"""Shared environment loader for OmegaWiki tools.

Loads environment variables from .env files so that API keys configured
by the user are available even when Claude Code spawns a fresh shell.

Load order (later files do NOT override earlier ones):
  1. ~/.env                   (global, e.g. DEEPXIV_TOKEN auto-registered here)
  2. <project_root>/.env      (the .env next to tools/, regardless of cwd —
                               so worktree subagents still find the project
                               .env even when cwd is a worktree path)
  3. ./.env                   (cwd-relative, kept for back-compat)
  4. os.environ               (always takes precedence — already-set vars are
                               never overwritten)

Usage in any tool:
    import _env  # noqa: F401  (side-effect import, loads env vars)
"""

from __future__ import annotations

import os
import pathlib

_LOADED = False
# Project root is the parent of tools/, where this file lives.
_PROJECT_ROOT_ENV = pathlib.Path(__file__).resolve().parent.parent / ".env"


def load() -> None:
    """Load .env files into os.environ (idempotent)."""
    global _LOADED
    if _LOADED:
        return
    _LOADED = True

    candidates = [
        pathlib.Path.home() / ".env",
        _PROJECT_ROOT_ENV,
        pathlib.Path(".env"),
    ]
    seen: set[pathlib.Path] = set()
    for env_path in candidates:
        try:
            resolved = env_path.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        try:
            for line in resolved.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # Never override existing env vars
                if key and key not in os.environ:
                    os.environ[key] = value
        except OSError:
            pass


# Auto-load on import
load()
