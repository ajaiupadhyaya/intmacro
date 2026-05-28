#!/usr/bin/env python3
"""Pre-render: generate prereq-chip + related-chapter Markdown partials and a
glossary tooltip JSON from _includes/{prereqs,glossary}.yml.

Outputs to _includes/generated/:
  <chapter>-prereqs.md      — prereq chips for the chapter header
  <chapter>-related.md      — 3-card related-chapters footer
  glossary-tooltips.json    — term -> {short, aka} for client-side tooltips

Run automatically by Quarto via project.pre-render. Also runnable standalone:
  python scripts/build_nav.py --includes _includes --out _includes/generated
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import yaml

def chip(chap_id: str, meta: dict) -> str:
    title = meta.get("title", chap_id)
    tldr = (meta.get("tldr", "") or "").replace('"', "&quot;")
    return (f'<a class="im-prereq-chip" href="{chap_id}.html" '
            f'title="{tldr}">requires: {title}</a>')

def build_prereq_partial(chap_id: str, data: dict) -> str:
    meta = data[chap_id]
    prereqs = meta.get("prereqs", []) or []
    if not prereqs:
        return '<div class="im-prereq-chips"><span class="im-prereq-chip">core model</span></div>\n'
    chips = "\n".join(chip(p, data[p]) for p in prereqs if p in data)
    return f'<div class="im-prereq-chips">\n{chips}\n</div>\n'

def related_card(role: str, chap_id: str, meta: dict) -> str:
    return (f'<a class="im-related-card" href="{chap_id}.html">'
            f'<div class="im-role">{role}</div>'
            f'<strong>{meta.get("title", chap_id)}</strong></a>')

def build_related_partial(chap_id: str, data: dict) -> str:
    meta = data[chap_id]
    cards = []
    prereqs = meta.get("prereqs", []) or []
    if prereqs and prereqs[0] in data:
        cards.append(related_card("prereq", prereqs[0], data[prereqs[0]]))
    nexts = [cid for cid, m in data.items()
             if chap_id in (m.get("prereqs", []) or [])]
    used = set(prereqs[:1]) | set(nexts[:1]) | {chap_id}
    siblings = [cid for cid, m in data.items()
                if m.get("track") == meta.get("track") and cid not in used]
    if siblings:
        cards.append(related_card("sibling", siblings[0], data[siblings[0]]))
    if nexts:
        cards.append(related_card("next", nexts[0], data[nexts[0]]))
    return f'<div class="im-related-cards">\n' + "\n".join(cards) + "\n</div>\n"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--includes", default="_includes")
    ap.add_argument("--out", default="_includes/generated")
    args = ap.parse_args()
    inc = pathlib.Path(args.includes)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    data = yaml.safe_load((inc / "prereqs.yml").read_text()) or {}
    for chap_id in data:
        (out / f"{chap_id}-prereqs.md").write_text(build_prereq_partial(chap_id, data))
        (out / f"{chap_id}-related.md").write_text(build_related_partial(chap_id, data))

    gloss = yaml.safe_load((inc / "glossary.yml").read_text()) or []
    tip = {e["term"]: {"short": e["short"], "aka": e.get("aka", [])} for e in gloss}
    (out / "glossary-tooltips.json").write_text(json.dumps(tip, indent=2))
    print(f"build_nav: {len(data)} chapters, {len(gloss)} glossary terms -> {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
