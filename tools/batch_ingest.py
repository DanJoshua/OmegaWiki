#!/usr/bin/env python3
"""Source preparation for /batch-ingest.

Resolves a user-supplied input (a directory of PDFs under ``raw/papers/``,
or a ``.md`` / ``.txt`` file listing arXiv URLs), prepares each paper's
canonical ingest path, looks up publication year via Semantic Scholar,
sorts the queue chronologically (unknown-year papers first), computes a
batch size of ``max(ceil(sqrt(N)), 4)``, and writes a manifest compatible
with ``/ingest`` BATCH MODE.

Usage:
    python3 tools/batch_ingest.py prepare \\
        --input raw/papers/my-batch/ \\
        --output-manifest .checkpoints/batch-ingest-sources.json

    python3 tools/batch_ingest.py prepare \\
        --input urls.md \\
        --output-manifest .checkpoints/batch-ingest-sources.json

The manifest is read by /batch-ingest itself for batch slicing and by
/ingest as the BATCH MODE source-of-truth (analogous to INIT MODE's
``init-sources.json``).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import _env  # noqa: F401 — load .env files for API keys

import prepare_paper_source as paper_source
from fetch_arxiv import extract_id as arxiv_extract_id
from fetch_s2 import paper as s2_paper
from init_discovery import download_to_discovered

ARXIV_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf|html)/([^/?\s]+)",
    re.IGNORECASE,
)


def _project_root(raw_root: Path) -> Path:
    return raw_root.resolve().parent


def _relative_to_project(path: Path, raw_root: Path) -> str:
    project_root = _project_root(raw_root)
    try:
        return str(path.resolve().relative_to(project_root))
    except ValueError:
        return str(path)


def _ingest_format_from_path(path_str: str) -> str:
    suffix = Path(path_str).suffix.lower().lstrip(".")
    if suffix == "tex":
        return "tex"
    if suffix == "pdf":
        return "pdf"
    if suffix:
        return suffix
    return "directory"


def _scan_pdf_dir(input_dir: Path) -> list[Path]:
    """Return all *.pdf files under ``input_dir`` (recursive), sorted."""
    if not input_dir.is_dir():
        raise SystemExit(f"input directory not found: {input_dir}")
    pdfs = sorted(p for p in input_dir.rglob("*.pdf") if p.is_file())
    if not pdfs:
        raise SystemExit(f"no .pdf files found under {input_dir}")
    return pdfs


def _read_url_list(input_file: Path) -> list[str]:
    """Read URLs from a .md/.txt file, one per line. Blanks and #-comments skipped."""
    if not input_file.is_file():
        raise SystemExit(f"input file not found: {input_file}")
    urls: list[str] = []
    for raw_line in input_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        # Allow lines like "- https://..." in markdown lists.
        line = line.lstrip("-*").strip()
        # If a markdown link [text](url), pull the URL.
        md_link = re.search(r"\(([^)]+)\)", line)
        if md_link and md_link.group(1).startswith("http"):
            line = md_link.group(1)
        # Find any embedded URL.
        match = ARXIV_URL_PATTERN.search(line)
        if match:
            urls.append(match.group(0))
            continue
        if line.startswith("http"):
            urls.append(line)
    if not urls:
        raise SystemExit(f"no URLs found in {input_file}")
    return urls


def _lookup_year(arxiv_id: str, warnings: list[str]) -> int | None:
    """Return S2 year for the paper, or None if unavailable."""
    if not arxiv_id:
        return None
    try:
        data = s2_paper(arxiv_id)
    except Exception as exc:  # network, rate limit, missing record
        warnings.append(f"S2 year lookup failed for {arxiv_id}: {exc}")
        return None
    year = data.get("year")
    if isinstance(year, int) and 1900 < year < 2100:
        return year
    return None


def _prepare_local_source(pdf_path: Path, raw_root: Path, warnings: list[str]) -> dict[str, Any] | None:
    """Run prepare_paper_source for a user-owned PDF; return a sources entry or None."""
    try:
        result = paper_source.prepare_paper_source(pdf_path, raw_root)
    except ValueError as exc:
        # prepare_paper_source requires path to live under raw_root
        warnings.append(f"skipped {pdf_path}: {exc}")
        return None
    except Exception as exc:
        warnings.append(f"prepare failed for {pdf_path}: {exc}")
        return None

    warnings.extend(result.get("warnings") or [])
    if not result.get("usable"):
        warnings.append(f"unusable source: {pdf_path}")
        return None

    canonical = result["canonical_ingest_path"]
    return {
        "candidate_id": result["candidate_id"],
        "origin": "user_local",
        "canonical_ingest_path": canonical,
        "prepared_path": result.get("prepared_path"),
        "discovered_path": None,
        "source_path": result["source_path"],
        "ingest_format": result.get("ingest_format") or _ingest_format_from_path(canonical),
        "title": result.get("title", ""),
        "arxiv_id": result.get("arxiv_id", ""),
    }


def _prepare_introduced_source(url: str, raw_root: Path, warnings: list[str]) -> dict[str, Any] | None:
    """Download an arXiv URL into raw/discovered/ and return a sources entry."""
    arxiv_id = arxiv_extract_id(url)
    if not arxiv_id:
        warnings.append(f"could not extract arXiv ID from URL: {url}")
        return None

    # Pull a title from S2 so the discovered slug is informative.
    title = ""
    try:
        meta = s2_paper(arxiv_id)
        title = (meta.get("title") or "").strip()
    except Exception as exc:
        warnings.append(f"S2 title lookup failed for {arxiv_id}: {exc}")

    if not title:
        title = f"arxiv-{arxiv_id}"

    result = download_to_discovered(raw_root, arxiv_id, title, candidate_id=f"arxiv:{arxiv_id}")
    if result.get("status") in {"failed", "skipped_no_arxiv"}:
        warnings.append(f"download failed for {url}: {result.get('error') or result.get('status')}")
        return None

    rel_path = _relative_to_project(Path(result["canonical_ingest_path"]), raw_root)
    return {
        "candidate_id": result["candidate_id"],
        "origin": "introduced",
        "canonical_ingest_path": rel_path,
        "prepared_path": None,
        "discovered_path": rel_path,
        "source_path": None,
        "ingest_format": result.get("ingest_format") or _ingest_format_from_path(rel_path),
        "title": title,
        "arxiv_id": arxiv_id,
    }


def _sort_chronologically(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort papers oldest → newest. Unknown-year papers go to the front
    (more likely antique pre-S2 work). Tie-break alphabetically by title."""
    def key(item: dict[str, Any]) -> tuple[int, int, str]:
        year = item.get("year")
        if isinstance(year, int):
            return (1, year, (item.get("title") or "").lower())
        return (0, 0, (item.get("title") or "").lower())

    return sorted(sources, key=key)


def _compute_batch_size(n_papers: int) -> int:
    return max(math.ceil(math.sqrt(n_papers)), 4)


def cmd_prepare(args: argparse.Namespace) -> int:
    raw_root = Path(args.raw_root)
    raw_root.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input)
    warnings: list[str] = []
    sources: list[dict[str, Any]] = []

    if input_path.is_dir():
        for pdf in _scan_pdf_dir(input_path):
            entry = _prepare_local_source(pdf, raw_root, warnings)
            if entry:
                sources.append(entry)
    elif input_path.is_file():
        for url in _read_url_list(input_path):
            entry = _prepare_introduced_source(url, raw_root, warnings)
            if entry:
                sources.append(entry)
    else:
        raise SystemExit(f"input must be a directory or file: {input_path}")

    if not sources:
        raise SystemExit("no usable papers prepared; aborting")

    # Look up year for each prepared source.
    for entry in sources:
        entry["year"] = _lookup_year(entry.get("arxiv_id", ""), warnings)

    sources = _sort_chronologically(sources)

    # Stamp ingest_rank in chronological order — same role as init's shortlist_rank.
    for idx, entry in enumerate(sources):
        entry["ingest_rank"] = idx

    batch_size = _compute_batch_size(len(sources))

    manifest = {
        "status": "ok",
        "input": str(input_path),
        "raw_root": str(raw_root),
        "total_papers": len(sources),
        "batch_size": batch_size,
        "batch_count": math.ceil(len(sources) / batch_size),
        "sources": sources,
        "warnings": warnings,
    }

    output_path = Path(args.output_manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "manifest": str(output_path),
        "total_papers": len(sources),
        "batch_size": batch_size,
        "batch_count": manifest["batch_count"],
        "warnings_count": len(warnings),
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser(
        "prepare",
        help="Resolve inputs, sort chronologically, and write a BATCH MODE manifest",
    )
    p_prepare.add_argument(
        "--input",
        required=True,
        help="Directory of PDFs under raw/papers/, OR a .md/.txt file with arXiv URLs",
    )
    p_prepare.add_argument("--raw-root", default="raw")
    p_prepare.add_argument("--output-manifest", required=True)
    p_prepare.set_defaults(func=cmd_prepare)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
