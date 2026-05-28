#!/usr/bin/env python3
"""Generate _glossary.qmd (alphabetical reference) from _includes/glossary.yml.

Run by Quarto pre-render. Standalone:
  python scripts/build_glossary.py --glossary _includes/glossary.yml --out _glossary.qmd
"""
from __future__ import annotations
import argparse, pathlib, sys
import yaml

HEADER = """---
title: "Glossary"
---

Key terms used across the book. Each links back to the chapter where it first appears.

"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glossary", default="_includes/glossary.yml")
    ap.add_argument("--out", default="_glossary.qmd")
    args = ap.parse_args()
    entries = yaml.safe_load(pathlib.Path(args.glossary).read_text()) or []
    entries.sort(key=lambda e: e["term"].lower())
    lines = [HEADER]
    for e in entries:
        aka = ""
        if e.get("aka"):
            aka = " _(also: " + ", ".join(e["aka"]) + ")_"
        fm = e.get("first_mention", "")
        link = f" — [↪ first used in {fm}](content/{fm}.html)" if fm else ""
        lines.append(f"### {e['term']}{aka}\n\n{e['short']}{link}\n")
    pathlib.Path(args.out).write_text("\n".join(lines))
    print(f"build_glossary: {len(entries)} terms -> {args.out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
