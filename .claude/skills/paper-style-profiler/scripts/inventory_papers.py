#!/usr/bin/env python3
"""Inventory repository PDFs without retaining extracted source text."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
}

MANUSCRIPT_HINTS = {
    "manuscript",
    "submission",
    "camera-ready",
    "draft",
    "rebuttal",
    "response",
    "paper-main",
    "main-paper",
}

NON_PAPER_HINTS = {
    "slides",
    "poster",
    "presentation",
    "thesis",
    "dissertation",
    "report",
    "template",
    "review-form",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_title(value: str) -> str:
    value = value.casefold().replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def run_text_command(command: list[str], timeout: int) -> tuple[bool, str, str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, "", str(exc)
    return completed.returncode == 0, completed.stdout, completed.stderr.strip()


def pdf_metadata(path: Path) -> tuple[dict[str, object], str | None]:
    if shutil.which("pdfinfo") is None:
        return {}, "pdfinfo unavailable"
    ok, stdout, stderr = run_text_command(["pdfinfo", str(path)], timeout=20)
    if not ok:
        return {}, stderr or "pdfinfo failed"
    parsed: dict[str, object] = {}
    keys = {
        "Title": "title",
        "Author": "author",
        "Subject": "subject",
        "Creator": "creator",
        "Producer": "producer",
        "Pages": "pages",
    }
    for line in stdout.splitlines():
        if ":" not in line:
            continue
        raw_key, raw_value = line.split(":", 1)
        key = keys.get(raw_key.strip())
        if key is None:
            continue
        value = raw_value.strip()
        if key == "pages":
            try:
                parsed[key] = int(value)
            except ValueError:
                parsed[key] = value
        elif value:
            parsed[key] = value
    return parsed, None


def extraction_signal(path: Path) -> dict[str, object]:
    if shutil.which("pdftotext") is None:
        return {
            "status": "tool_unavailable",
            "sample_pages": 0,
            "readable_characters": 0,
            "word_count": 0,
            "full_text_candidate": False,
        }
    ok, stdout, stderr = run_text_command(
        ["pdftotext", "-f", "1", "-l", "3", "-nopgbrk", str(path), "-"],
        timeout=30,
    )
    if not ok:
        return {
            "status": "failed",
            "sample_pages": 3,
            "readable_characters": 0,
            "word_count": 0,
            "full_text_candidate": False,
            "error": stderr or "pdftotext failed",
        }
    clean = re.sub(r"\s+", " ", stdout).strip()
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", clean)
    readable_chars = len(re.sub(r"\s", "", clean))
    return {
        "status": "ok",
        "sample_pages": 3,
        "readable_characters": readable_chars,
        "word_count": len(words),
        "full_text_candidate": readable_chars >= 1500 and len(words) >= 200,
    }


def path_flags(relative_path: str) -> list[str]:
    lowered = relative_path.casefold()
    flags: list[str] = []
    if any(hint in lowered for hint in MANUSCRIPT_HINTS):
        flags.append("possible_project_manuscript")
    if any(hint in lowered for hint in NON_PAPER_HINTS):
        flags.append("possible_non_article_material")
    if any(part in {"output", "outputs", "generated", "rendered"} for part in Path(lowered).parts):
        flags.append("possible_generated_copy")
    return flags


def git_candidates(root: Path) -> list[Path] | None:
    if shutil.which("git") is None:
        return None
    ok, stdout, _ = run_text_command(
        ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "--", "*.pdf", "*.PDF"],
        timeout=30,
    )
    if not ok:
        return None
    return [root / line for line in stdout.splitlines() if line.strip()]


def walked_candidates(root: Path, scopes: list[Path]) -> list[Path]:
    found: list[Path] = []
    for scope in scopes:
        if scope.is_file() and scope.suffix.casefold() == ".pdf":
            found.append(scope)
            continue
        if not scope.is_dir():
            continue
        for current, dirs, files in os.walk(scope, followlinks=False):
            dirs[:] = [name for name in dirs if name not in EXCLUDED_DIRS]
            for name in files:
                if name.casefold().endswith(".pdf"):
                    found.append(Path(current) / name)
    return found


def inside_scope(path: Path, scopes: list[Path]) -> bool:
    for scope in scopes:
        try:
            path.relative_to(scope)
            return True
        except ValueError:
            if path == scope:
                return True
    return False


def discover_pdfs(root: Path, scope_values: list[str], include_ignored: bool) -> list[Path]:
    scopes = [(root / value).resolve() for value in (scope_values or ["."])]
    for scope in scopes:
        try:
            scope.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"scope escapes repository root: {scope}") from exc

    candidates = None if include_ignored else git_candidates(root)
    if candidates is None:
        candidates = walked_candidates(root, scopes)
    else:
        candidates = [path for path in candidates if inside_scope(path.resolve(), scopes)]

    unique: dict[str, Path] = {}
    for path in candidates:
        resolved = path.resolve()
        if not resolved.is_file() or resolved.suffix.casefold() != ".pdf":
            continue
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError:
            continue
        unique[relative] = resolved
    return [unique[key] for key in sorted(unique)]


def make_inventory(root: Path, pdfs: list[Path]) -> dict[str, object]:
    records: list[dict[str, object]] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    titles: dict[str, list[str]] = defaultdict(list)

    for path in pdfs:
        relative = path.relative_to(root).as_posix()
        digest = sha256_file(path)
        metadata, metadata_error = pdf_metadata(path)
        fallback_title = re.sub(r"[_-]+", " ", path.stem).strip()
        normalized = normalize_title(str(metadata.get("title", "")) or fallback_title)
        record: dict[str, object] = {
            "path": relative,
            "sha256": digest,
            "bytes": path.stat().st_size,
            "normalized_title": normalized,
            "metadata": metadata,
            "extraction": extraction_signal(path),
            "path_flags": path_flags(relative),
            "source_class": "unresolved",
            "eligibility": "unresolved",
            "decision_reason": "Requires human review",
        }
        if metadata_error:
            record["metadata_error"] = metadata_error
        records.append(record)
        hashes[digest].append(relative)
        if normalized:
            titles[normalized].append(relative)

    duplicate_groups = {
        "exact_hash": [paths for paths in hashes.values() if len(paths) > 1],
        "normalized_title": [paths for title, paths in titles.items() if len(title) >= 8 and len(paths) > 1],
    }
    return {
        "schema": "paper_style_inventory_v1",
        "generated_at": utc_now(),
        "repository_root": ".",
        "tooling": {
            "pdfinfo": bool(shutil.which("pdfinfo")),
            "pdftotext": bool(shutil.which("pdftotext")),
            "note": "Extraction signals are derived from the first three pages; no source text is retained.",
        },
        "records": records,
        "duplicate_groups": duplicate_groups,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository_root", help="Repository root containing candidate PDFs")
    parser.add_argument("--scope", action="append", default=[], help="Repository-relative path to scan; repeatable")
    parser.add_argument("--include-ignored", action="store_true", help="Walk scoped paths even when Git ignores them")
    parser.add_argument("--output", required=True, help="Destination JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repository_root).expanduser().resolve()
    if not root.is_dir():
        print(f"repository root not found: {root}", file=sys.stderr)
        return 2
    try:
        pdfs = discover_pdfs(root, args.scope, args.include_ignored)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = make_inventory(root, pdfs)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "pdf_count": len(pdfs), "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
