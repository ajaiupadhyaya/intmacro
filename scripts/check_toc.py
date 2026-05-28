#!/usr/bin/env python3
"""Validate that every file referenced in _quarto.yml's website.sidebar exists.

Exit non-zero on any missing file. First CI step.
  python scripts/check_toc.py --root .
"""
from __future__ import annotations
import argparse, pathlib, sys
import yaml

def collect_files(node, acc):
    if isinstance(node, dict):
        if "contents" in node:
            collect_files(node["contents"], acc)
        for key in ("href", "file"):
            if key in node and isinstance(node[key], str):
                acc.append(node[key])
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, str):
                acc.append(item)
            else:
                collect_files(item, acc)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    cfg = yaml.safe_load((root / "_quarto.yml").read_text())
    sidebar = (((cfg or {}).get("website") or {}).get("sidebar") or {})
    refs = []
    collect_files(sidebar.get("contents", []), refs)

    failures = []
    for ref in refs:
        if ref.startswith("http"):
            continue
        if not (root / ref).exists():
            failures.append(ref)

    if failures:
        print("FAILURES — sidebar entries with no file on disk:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"OK: {len(refs)} sidebar entries all resolve.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
