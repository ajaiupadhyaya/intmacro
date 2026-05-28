# intmacro Dashboard v2 — Design Spec

> Brainstormed 2026-05-28. Status: approved through aesthetic + chapter template; remaining sections approved in batch.
> Builds on the v1 revamp (see `docs/plans/intmacro-dashboard-revamp.md`), which unified the TOC, slimmed the landing, and shipped a Jupyter Book site to GitHub Pages.

## Goal

Turn the intmacro Jupyter Book into a sleek, modern, self-study dashboard that students in intermediate macroeconomics actually reach for. The 30 canonical models are the core of the class and are retained; their math/simulator logic may be edited only to make them clearer or cleaner.

## Locked-in decisions

| Dimension | Decision |
|---|---|
| Primary use moment | Self-study outside class |
| Top pain points | (1) Wall-of-equations + buried simulators; (2) no way to test understanding |
| Chapter scope | Full structural redesign per chapter |
| Platform | Migrate Jupyter Book → **Quarto** |
| Aesthetic | **Hybrid** — dashboard chrome (sidebar, search, dark/light) wrapping scholarly chapter pages with sim-as-hero |
| Self-check format | Mix: multiple-choice questions + simulator challenges |
| Navigation additions | Concept glossary + inline tooltips; prerequisite chips + "if confused, see"; related-chapters footer + per-track maps |
| Rollout | **Showcase first** — 3 flagship chapters, validate, then scale to remaining 27 |

## Section 1 — End-state vision

A self-study dashboard on GitHub Pages. Landing is a calm, fast, app-like dashboard: search, dark/light toggle, the 5 tracks as cards with progress affordances. Sidebar reflects canonical structure but stays unobtrusive.

Each chapter is a single-screen first impression: title, prereq chips, the interactive simulator above the fold, a one-paragraph "what this model says," and a "show the math" toggle. Below the fold: derivations, interpretation, common confusions, self-check (MCQs + simulator challenges), and a related-chapters footer following the canonical order.

Cross-cutting: hover any glossary term anywhere for a tooltip; a standalone Glossary page lists all terms with backlinks; each track has a Track Map visualizing its prerequisite DAG.

Under the hood: Quarto-rendered HTML + in-browser execution via `quarto-live` (Pyodide). Source stays `.ipynb` so model logic carries over. CI builds + deploys to GitHub Pages on push to main.

## Section 2 — Platform & repo layout

Quarto replaces Jupyter Book in the build toolchain. Source notebooks unchanged.

```
intmacro/
├── _quarto.yml              # Replaces _config.yml + _toc.yml
├── index.qmd                # Dashboard landing (replaces Preliminaries_new.ipynb)
├── theme/
│   ├── _tokens.scss         # Shared design tokens
│   ├── intmacro.scss        # Light theme
│   ├── intmacro-dark.scss   # Dark theme
│   └── components.scss      # MCQ cards, prereq chips, sim-hero, track maps, etc.
├── _extensions/
│   └── quarto-live/         # In-browser Pyodide execution (vendored)
├── content/
│   ├── *.ipynb              # Same 30 canonical notebooks
│   ├── _archive/            # Untouched; excluded from render
│   └── MODELS.md            # Untouched
├── _includes/
│   ├── glossary.yml         # term → short def + first-mention chapter + aka
│   └── prereqs.yml          # chapter → {track, prereqs[]}
├── _glossary.qmd            # Auto-generated alphabetical reference
├── tracks/                  # One .qmd per track for the Track Map page
├── scripts/
│   ├── check_toc.py         # Updated for _quarto.yml
│   ├── build_glossary.py    # Walks notebooks, generates _glossary.qmd + tooltip JSON
│   ├── check_math.py        # Flags equations that fail MathJax parse
│   └── render_track_maps.py # Validates DAG vs prereqs.yml
├── .github/workflows/deploy.yml   # quarto render + deploy
└── _site/                   # Quarto output (replaces _build/)
```

- `_quarto.yml` is one file → the fragmented-TOC problem can't recur.
- Notebooks stay `.ipynb`; new prose-heavy pages (landing, glossary, track maps) are `.qmd`.
- `_includes/*.yml` are the single source of truth for cross-references.

Removed: `_config.yml`, `_toc.yml` → `_quarto.yml`; `_build/` → `_site/`; `Preliminaries_new.ipynb` → `index.qmd`.
Kept: every `.ipynb`, `clean_notebooks.py`, `scripts/check_toc.py` (updated), the GH Pages deploy mechanism.

## Section 3 — Chapter template (hero deliverable)

Every canonical chapter follows this 10-section structure:

| # | Section | Contents | Purpose |
|---|---|---|---|
| 1 | Chapter header | Title, tagline, prereq chips, track label | Context in 5s |
| 2 | TL;DR | 2-3 sentence plain answer to "what does this model say?" | Fast refresher |
| 3 | Learning goals | 3 bullets | Explicit expectations |
| 4 | 🚀 Try it (sim hero) | Interactive simulator, above the fold, with "drag X to see Y" caption | Fixes buried-simulator pain |
| 5 | Core intuition | Economic story, no equations | Intuition before formalism |
| 6 | Model & math *(collapsible)* | Full derivation behind "Show the math" toggle, collapsed by default | Fixes wall-of-equations |
| 7 | What the simulator showed | Calls back to step 4, connects play to theory | Closes the loop |
| 8 | Common confusions | 2-3 callouts on typical misreadings | Pre-empts FAQs |
| 9 | Self-check | 2-3 MCQs (reveal explanations) + 1-2 simulator challenges | Active learning |
| 10 | Related chapters | 3 cards: prereq (back), sibling (lateral), next (forward) | Curriculum motion |

Structural rules:
- Simulator is the first content after the header — never buried.
- Math is always collapsed by default; opt-in via toggle.
- Steps 7 and 9 reference the same simulator instance from step 4.
- MCQ/sim-challenge components use Quarto callouts styled custom; light JS for reveal-on-click only.

Explicitly excluded: model biography/history, external "further reading," verbatim simulator code listing (available via "Show code" in the live cell).

## Section 4 — Hybrid theme system

Two-file SCSS theme with shared tokens. Light is default; dark is a one-click toggle, persisted per-device.

- **Tokens** (`theme/_tokens.scss`): 8px spacing scale; radius sm/md/lg; type scale xs→2xl; three font families (`--font-ui` Inter, `--font-math` STIX Two Math, `--font-mono` JetBrains Mono); motion easing + durations.
- **Light palette**: `--bg-page #fcfcfb`, `--bg-surface #ffffff`, `--fg-primary #0f172a`, `--accent #5b6cff`, `--sim #10b981`, `--warn #f59e0b`, `--danger #ef4444`.
- **Dark palette**: `--bg-page #0b0d12`, `--bg-surface #14171f`, `--fg-primary #e6e8ee`, `--accent #7aa2f7`, `--sim #34d399`, `--warn #fbbf24`, `--danger #f87171`.

Component classes (in `theme/components.scss`): `.im-prereq-chip`, `.im-tldr`, `.im-sim-hero`, `.im-math-toggle`, `.im-confusion`, `.im-mcq`, `.im-sim-challenge`, `.im-related-cards`, `.im-glossary-term`, `.im-track-map`. Identical in both modes; only colors swap.

Typography: Inter 16px/1.6 body; STIX Two Math for display + inline math; JetBrains Mono for code; chapter titles Inter 600 at 2rem (not a display serif — rejected as too editorial).

Dark mode: toggle saves to `localStorage.theme`; first visit defaults to `prefers-color-scheme`; inline `<head>` script prevents flash-of-wrong-theme. All transitions 120ms ease-out (math toggle 300ms); `prefers-reduced-motion` zeroes transitions.

## Section 5 — Navigation features

- **Glossary**: `_includes/glossary.yml` (~40-60 curated terms: `term`, `short`, `first_mention`, `aka`). `scripts/build_glossary.py` generates `_glossary.qmd` + a tooltip JSON manifest. Dotted-underlined terms show a 2-line tooltip with "→ full entry."
- **Prereq chips**: `_includes/prereqs.yml` maps `chapter → {track, prereqs[]}`. Quarto shortcode `{{< prereqs >}}` renders chips in the header; click → popover with the prereq's TL;DR.
- **Related-chapters footer**: derived from `prereqs.yml` `track` + `prereqs` fields; shortcode renders the 3-card grid (prereq/sibling/next).
- **Track maps**: `tracks/<track>.qmd` use a Mermaid DAG with clickable nodes; validated in CI against `prereqs.yml`.

## Section 6 — Showcase plan

Three flagship chapters, chosen for traffic, curriculum centrality, and stylistic range:

1. `solow_bgp.ipynb` → renamed `solow_intro` — diff-eq dynamics, transition-path simulator. Tests math-toggle + sim-hero.
2. `2_period_consump.ipynb` — intertemporal optimization, indifference-curve sim. Tests common-confusions callouts.
3. `adassim.ipynb` — dynamic AD-AS + Taylor rule, multi-panel time-series sim. Tests heavy widget + simulator-challenge self-checks.

"Done" per chapter: all 10 template sections populated; MCQ reveals work; prereq chips link to valid targets; related-chapters footer renders; math toggle works; clean `quarto render`.

Validation gate: deploy the 3 to a preview URL; user walks one as a student; iterate template until approved. Only then scale to the remaining 27.

## Section 7 — Migration & deploy

> **Revised 2026-05-28 after technical verification.** `ipywidgets.interact()` requires a live Python kernel and does **not** run in static Quarto/quarto-live output (confirmed by Quarto team + quarto-live maintainers). The interactivity layer is therefore reimplemented in **Observable JS (OJS) + Plotly**, which is fully client-side, instant, and theme-aware. The economic model (equations, parameters, behavior) is retained; only the widget/render layer changes language from Python+ipywidgets to JS+OJS. This satisfies the "retain the models, may edit for clarity" constraint.

- **Quarto setup**: install via `quarto-dev/quarto-actions/setup@v2` (Quarto is a binary, not a pip package), pinned ≥ 1.5.
- **In-browser interactivity**: each simulator is an OJS block — `viewof` `Inputs.range(...)` sliders driving a reactive `Plot`/Plotly figure. No kernel, no Pyodide, no separate tab. Showcase chapters are authored as `.qmd` (OJS lives natively in `.qmd`); the original `.ipynb` moves to `content/_archive/` with a provenance note (per the established archive policy).
- **Static-output notebooks**: the 27 non-showcase chapters keep rendering their committed `.ipynb` plot output statically in this milestone; their OJS conversion is a later plan. JupyterLite at `/lite/` is retained for now as the "run the original Python" escape hatch for those, and removed once all chapters are converted.
- **Deploy workflow** (`.github/workflows/deploy.yml`): setup Quarto → `pip install -r requirements.txt` → `python scripts/check_toc.py` → `python scripts/build_glossary.py` → `quarto render` (→ `_site/`) → `configure-pages@v5` + `upload-pages-artifact@v3` + `deploy-pages@v4`.
- **Redirects**: meta-refresh + canonical-link pages at old URLs (e.g., `/content/Preliminaries_new.html` → `/`, `/content/solow_bgp.html` → `/content/solow_intro.html`).
- **Branch**: single `v2/dashboard-rebuild`; PR to `main` after showcase validation.

## Section 8 — Risks & mitigations

| Risk | Mitigation |
|---|---|
| OJS reimplementation of a simulator diverges numerically from the original Python model | Port the model's closed-form/iterative equations 1:1; add a check that spot-values (e.g., Solow k* at known params) match the Python original within tolerance. Document the source equation next to the OJS code. |
| A simulator is too complex to port to OJS cleanly (e.g., adassim's multi-panel dynamics) | Showcase order is Solow first (simplest), then 2-period, then adassim. If adassim resists OJS, fall back to static plot + JupyterLite "run live" button for that one chapter only. |
| MathJax/KaTeX differences break an equation | `scripts/check_math.py` renders each page and flags math that fails to parse. |
| 30-chapter restructure → merge conflicts | Single-author work on one feature branch; merge once; README banner during rebuild. |
| Dark mode mismatches baked-in plot colors on static (non-showcase) chapters | OJS/Plotly sims in showcase chapters are theme-aware by construction. Static `.ipynb` plots may mismatch in dark mode — accepted for now; resolved when each chapter is converted to OJS. |
| Glossary tooltips become noise | Curate `glossary.yml` to ~40-60 key concepts, not every noun. |

## Success criteria

- All 30 canonical models retained and reachable.
- Each showcase chapter: simulator above the fold, math collapsible, working self-checks.
- Glossary, prereq chips, related-chapters footer, and track maps functional.
- Dark/light toggle works and persists; no flash-of-wrong-theme.
- `quarto render` builds clean in CI; site deploys to GitHub Pages.
- A first-time student can land, find a model, play the simulator, and self-test without confusion.

## Out of scope (this round)

- Migrating all 27 non-showcase chapters (happens after showcase validation).
- cmd-K search palette (Quarto built-in search is sufficient).
- Live FRED data integration, instructor-companion notes, auto-graded code challenges (future bets).
