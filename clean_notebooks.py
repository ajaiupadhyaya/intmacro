#!/usr/bin/env python3
"""Normalize notebook metadata and (optionally) clear outputs.

Default: walk content/ and content/_archive/, normalize JSON formatting and
strip volatile metadata that creates noisy git diffs (execution counts,
kernel-specific UUIDs, transient widget state).

Outputs are NOT stripped by default — this book ships pre-executed (see
_config.yml execute_notebooks: "off"). Pass --strip-outputs to clear them.

Usage:
    python clean_notebooks.py                  # normalize all under content/
    python clean_notebooks.py path/to/nb.ipynb # one file
    python clean_notebooks.py --strip-outputs  # also clear cell outputs
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_TARGETS = [REPO_ROOT / "content"]

# Top-level notebook metadata keys that are useful to keep.
KEEP_METADATA = {"kernelspec", "language_info"}


def clean_notebook(path: Path, strip_outputs: bool) -> None:
    nb = nbformat.read(path, as_version=4)

    # Prune top-level metadata to a small allow-list.
    nb.metadata = {k: v for k, v in nb.metadata.items() if k in KEEP_METADATA}

    for cell in nb.cells:
        # Drop cell-level UUIDs and ephemeral metadata.
        if "id" in cell:
            # Keep cell ids (nbformat 4.5+ requires them), but drop other noise.
            pass
        cell.metadata = {
            k: v for k, v in cell.metadata.items()
            if k in {"tags", "scrolled"}  # keep tags (used for archive-provenance)
        }
        if cell.cell_type == "code":
            cell.execution_count = None
            if strip_outputs:
                cell.outputs = []

    nbformat.write(nb, path)


def iter_notebooks(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for t in targets:
        if t.is_file() and t.suffix == ".ipynb":
            files.append(t)
        elif t.is_dir():
            files.extend(sorted(t.rglob("*.ipynb")))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories to clean (default: content/)",
    )
    parser.add_argument(
        "--strip-outputs",
        action="store_true",
        help="Also clear cell outputs (use sparingly — book ships pre-executed)",
    )
    args = parser.parse_args()

    targets = args.paths or DEFAULT_TARGETS
    files = iter_notebooks(targets)
    if not files:
        print("No notebooks found.")
        return 0

    for nb_path in files:
        try:
            clean_notebook(nb_path, strip_outputs=args.strip_outputs)
            print(f"cleaned: {nb_path.relative_to(REPO_ROOT)}")
        except Exception as e:
            print(f"  ERROR {nb_path}: {e}", file=sys.stderr)
            return 1

    print(f"\nDone — {len(files)} notebook(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
