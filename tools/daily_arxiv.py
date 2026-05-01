#!/usr/bin/env python3
"""Deterministic helpers for the /daily-arxiv workflow.

The current GitHub Actions scaffold is intentionally inform-only: it reads a
fetched arXiv feed, filters papers already known to the wiki, and writes a
Markdown digest plus machine-readable JSON. Recommendation and auto-ingest can
fill the reserved score/signal/decision fields later without changing the
workflow envelope.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARXIV_ID_RE = re.compile(r"(?<![\w./-])(\d{4}\.\d{4,5})(?:v\d+)?(?![\w.-])")
ARXIV_URL_RE = re.compile(
    r"https?://arxiv\.org/(?:abs|pdf)/([A-Za-z0-9./-]+)", re.IGNORECASE
)


def _normalize_arxiv_id(value: str) -> str:
    """Return an arXiv ID without URL wrappers or version suffixes."""
    text = (value or "").strip()
    if not text:
        return ""
    url_match = ARXIV_URL_RE.search(text)
    if url_match:
        text = url_match.group(1)
    text = text.removesuffix(".pdf").rstrip("/")
    text = re.sub(r"^arxiv:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"v\d+$", "", text)
    return text


def _extract_arxiv_ids(text: str) -> set[str]:
    ids = {_normalize_arxiv_id(match.group(1)) for match in ARXIV_ID_RE.finditer(text)}
    ids.update(_normalize_arxiv_id(match.group(1)) for match in ARXIV_URL_RE.finditer(text))
    return {aid for aid in ids if aid}


def _known_arxiv_ids(wiki_root: Path) -> set[str]:
    """Collect arXiv IDs already represented in the wiki."""
    known: set[str] = set()
    if not wiki_root.exists():
        return known

    index_path = wiki_root / "index.md"
    if index_path.exists():
        known.update(_extract_arxiv_ids(index_path.read_text(encoding="utf-8", errors="ignore")))

    papers_dir = wiki_root / "papers"
    if papers_dir.exists():
        for path in papers_dir.glob("*.md"):
            known.update(_extract_arxiv_ids(path.read_text(encoding="utf-8", errors="ignore")))

    return known


def _load_feed(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"expected a list of papers in {path}")
    return [item for item in data if isinstance(item, dict)]


def _paper_url(paper: dict[str, Any], arxiv_id: str) -> str:
    url = str(paper.get("arxiv_url") or paper.get("url") or "").strip()
    if url:
        return url
    return f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""


def _abstract_preview(text: str, limit: int = 360) -> str:
    compact = re.sub(r"\s+", " ", (text or "").strip())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "..."


def _normalize_authors(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    authors: list[str] = []
    for item in value:
        if isinstance(item, str):
            name = item.strip()
        elif isinstance(item, dict):
            name = str(item.get("name") or "").strip()
        else:
            name = ""
        if name:
            authors.append(name)
    return authors


def _candidate_record(paper: dict[str, Any], known_ids: set[str]) -> dict[str, Any]:
    arxiv_id = _normalize_arxiv_id(str(paper.get("arxiv_id") or paper.get("arxiv_url") or ""))
    title = re.sub(r"\s+", " ", str(paper.get("title") or "").strip())
    category = str(paper.get("category") or "").strip()
    known = bool(arxiv_id and arxiv_id in known_ids)
    return {
        "arxiv_id": arxiv_id,
        "title": title or "(untitled)",
        "authors": _normalize_authors(paper.get("authors")),
        "arxiv_url": _paper_url(paper, arxiv_id),
        "category": category,
        "published": str(paper.get("published") or "").strip(),
        "abstract_preview": _abstract_preview(str(paper.get("abstract") or paper.get("summary") or "")),
        "is_known": known,
        "mode": "inform_only",
        "decision": "already_in_wiki" if known else "inform",
        "score": None,
        "signals": {
            "arxiv_rss": True,
            "semantic_scholar": None,
            "deepxiv": None,
            "llm": None,
        },
        "rationale": (
            "Already represented in the wiki."
            if known
            else "Unranked scaffold candidate; recommendation is not enabled yet."
        ),
    }


def build_digest(feed_path: Path, wiki_root: Path, max_items: int) -> dict[str, Any]:
    papers = _load_feed(feed_path)
    known_ids = _known_arxiv_ids(wiki_root)
    candidates = [_candidate_record(paper, known_ids) for paper in papers]
    new_candidates = [paper for paper in candidates if not paper["is_known"]]
    category_counts = Counter(
        paper["category"] or "unknown" for paper in new_candidates
    )
    listed = new_candidates[: max(0, max_items)]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "inform_only",
        "recommendation_enabled": False,
        "auto_ingest_enabled": False,
        "feed_path": str(feed_path),
        "wiki_root": str(wiki_root),
        "counts": {
            "feed_total": len(candidates),
            "already_in_wiki": len(candidates) - len(new_candidates),
            "new_candidates": len(new_candidates),
            "listed": len(listed),
        },
        "category_counts": dict(sorted(category_counts.items())),
        "candidates": candidates,
        "listed_candidates": listed,
        "notes": [
            "This scaffold does not score, recommend, download, ingest, or mutate the wiki.",
            "Future recommendation can fill score, signals, rationale, and decision fields.",
        ],
    }


def _format_authors(authors: list[str], limit: int = 3) -> str:
    if not authors:
        return "unknown authors"
    shown = authors[:limit]
    suffix = " et al." if len(authors) > limit else ""
    return ", ".join(shown) + suffix


def format_markdown(payload: dict[str, Any]) -> str:
    counts = payload["counts"]
    lines = [
        "# Daily arXiv Digest",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Feed papers scanned: {counts['feed_total']}",
        f"- Already in wiki: {counts['already_in_wiki']}",
        f"- New candidates: {counts['new_candidates']}",
        f"- Listed in this digest: {counts['listed']}",
        "- Mode: inform-only scaffold; recommendation and auto-ingest are disabled",
        "",
    ]

    if payload["category_counts"]:
        lines.extend(["## New Candidates by Category", ""])
        for category, count in payload["category_counts"].items():
            lines.append(f"- `{category}`: {count}")
        lines.append("")

    lines.extend(["## New arXiv Candidates", ""])
    listed = payload["listed_candidates"]
    if not listed:
        lines.append("No new candidates after wiki deduplication.")
    else:
        for index, paper in enumerate(listed, start=1):
            title = paper["title"]
            url = paper["arxiv_url"]
            arxiv_id = paper["arxiv_id"] or "unknown-id"
            category = paper["category"] or "unknown"
            authors = _format_authors(paper["authors"])
            lines.append(f"{index}. **{title}**")
            lines.append(f"   - arXiv: [{arxiv_id}]({url})")
            lines.append(f"   - Category: `{category}`")
            lines.append(f"   - Authors: {authors}")
            if paper["published"]:
                lines.append(f"   - Published: {paper['published']}")
            if paper["abstract_preview"]:
                lines.append(f"   - Abstract: {paper['abstract_preview']}")
            lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- This digest is unranked. It only proves the daily collection, deduplication, artifact, and e-mail path.",
            "- Future recommendation can fill the JSON `score`, `signals`, `rationale`, and `decision` fields.",
            "- Future auto-ingest should add a workflow mode and repository write permissions after selection is implemented.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cmd_digest(args: argparse.Namespace) -> None:
    payload = build_digest(args.feed, args.wiki_root, args.max_items)
    markdown = format_markdown(payload)

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(markdown, encoding="utf-8")
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        "daily-arxiv digest: "
        f"{payload['counts']['new_candidates']} new / "
        f"{payload['counts']['feed_total']} scanned -> {args.out_md}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OmegaWiki daily arXiv helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    digest = sub.add_parser("digest", help="Build an inform-only daily arXiv digest")
    digest.add_argument("--feed", type=Path, required=True, help="JSON feed from tools/fetch_arxiv.py")
    digest.add_argument("--wiki-root", type=Path, default=Path("wiki"), help="Wiki root for deduplication")
    digest.add_argument("--out-md", type=Path, required=True, help="Markdown digest output path")
    digest.add_argument("--out-json", type=Path, required=True, help="Machine-readable digest output path")
    digest.add_argument("--max-items", type=int, default=20, help="Maximum new candidates to list")
    digest.set_defaults(func=cmd_digest)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
