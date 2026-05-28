#!/usr/bin/env python3
"""Validate that _toc.yml, content/, and content/MODELS.md agree.

Failures:
  1. A file referenced in _toc.yml does not exist on disk.
  2. A canonical .ipynb under content/ (not in _archive/) is missing from
     _toc.yml AND is not the book root.
  3. A file referenced in _toc.yml is inside content/_archive/ (archive
     notebooks must never be in the active TOC).

Warnings (do not fail CI):
  - A canonical chapter is missing from content/MODELS.md.

Exit code is non-zero on failures. Designed to be the first CI step.
"""
from __future__ import annotations

import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOC = REPO_ROOT / "_toc.yml"
CONTENT = REPO_ROOT / "content"
ARCHIVE = CONTENT / "_archive"
MODELS_MD = CONTENT / "MODELS.md"


def collect_toc_files(toc_yaml: dict) -> list[str]:
    """Return every 'file:' value from a Jupyter Book TOC, including the root."""
    files: list[str] = []
    if "root" in toc_yaml:
        files.append(toc_yaml["root"])
    for part in toc_yaml.get("parts", []):
        for chapter in part.get("chapters", []):
            if "file" in chapter:
                files.append(chapter["file"])
    # Flat (non-part) format fallback
    for chapter in toc_yaml.get("chapters", []):
        if "file" in chapter:
            files.append(chapter["file"])
    return files


def main() -> int:
    with TOC.open() as f:
        toc = yaml.safe_load(f)

    toc_files = collect_toc_files(toc)
    failures: list[str] = []
    warnings: list[str] = []

    # 1. Every TOC entry must resolve to an existing file (.ipynb or .md).
    for entry in toc_files:
        candidates = [
            REPO_ROOT / f"{entry}.ipynb",
            REPO_ROOT / f"{entry}.md",
            REPO_ROOT / entry,
        ]
        if not any(p.exists() for p in candidates):
            failures.append(f"TOC references missing file: {entry}")

    # 3. No archive files in TOC.
    for entry in toc_files:
        if "_archive/" in entry:
            failures.append(f"TOC references archived file: {entry}")

    # 2. Every canonical .ipynb under content/ must appear in TOC (or be the root).
    toc_set = {Path(e).name for e in toc_files}
    canonical_notebooks = [
        p for p in CONTENT.glob("*.ipynb")
        if ARCHIVE not in p.parents
    ]
    for nb in canonical_notebooks:
        stem = nb.stem
        if stem not in toc_set:
            failures.append(
                f"Canonical notebook missing from _toc.yml: content/{nb.name}"
            )

    # Warning: MODELS.md mentions
    if MODELS_MD.exists():
        models_text = MODELS_MD.read_text()
        for nb in canonical_notebooks:
            if nb.name not in models_text and nb.stem not in models_text:
                warnings.append(
                    f"Canonical notebook missing from content/MODELS.md: {nb.name}"
                )

    # Report
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        print()
        print(f"{len(failures)} consistency failure(s). Fix _toc.yml or the file tree.")
        return 1

    print(f"OK: {len(toc_files)} TOC entries, {len(canonical_notebooks)} canonical notebooks consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
