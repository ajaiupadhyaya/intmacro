# Intermediate Macroeconomics — Interactive Dashboard

A [Quarto](https://quarto.org) website of working macroeconomic models,
originally built for the intermediate macroeconomics course at the University
of Virginia. Each chapter pairs the relevant math with a live, in-browser
simulator (Observable JS) and a short economic interpretation.

**Live site:** https://ajaiupadhyaya.github.io/intmacro/

## What's in the site

Five tracks, organized in the sidebar of [`_quarto.yml`](./_quarto.yml):

1. **Foundations** — math primer (growth rates, log approximation).
2. **Measurement & National Accounts** — GDP, real vs. nominal, PPP, chain-weighted indices.
3. **Growth & Long-Run Dynamics** — Solow, Romer, hybrid, growth accounting, convergence, scale effects.
4. **Intertemporal Choice & Labor** — two-period consumption, labor-leisure, Tobin's q.
5. **Business Cycles & Policy Dynamics** — IS curve, dynamic AD-AS with Taylor rule, Lucas Island, equilibrium business cycles, RBC.

Chapters come in two generations while the v2 migration is in progress:

- **v2 `.qmd` chapters** — the current template: hand-authored Quarto pages
  whose simulators run client-side via Observable JS (`{ojs}` cells with
  `Inputs.range` sliders + `Plot.plot`). These are fully interactive on the
  static deployed site.
- **v1 `.ipynb` chapters** — legacy notebooks rendered statically (their
  `ipywidgets` interactivity does not run in the browser). These are being
  converted to the v2 template chapter by chapter.

The canonical inventory (one row per model, including the merge map for
archive material) lives in [`content/MODELS.md`](./content/MODELS.md).
Superseded material is preserved in [`content/_archive/`](./content/_archive/)
— see the archive policy in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Running locally

Requires [Quarto](https://quarto.org/docs/get-started/) (CI uses 1.9.x) and
Python 3.11+.

```bash
git clone https://github.com/ajaiupadhyaya/intmacro
cd intmacro

# Python deps (notebook execution + build scripts)
uv venv && uv pip install -r requirements.txt   # or: pip install -r requirements.txt

# Generate nav partials + glossary, then preview with live reload
uv run scripts/build_nav.py
uv run scripts/build_glossary.py
quarto preview
```

`quarto render` writes the static site to `_site/`.

## Checks

```bash
uv run scripts/check_toc.py   # sidebar ↔ filesystem consistency
uv run pytest tests/          # build-script tests
```

Both run in CI on every push and pull request.

## Deploy flow

A single GitHub Actions workflow
([`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)) runs the
checks, generates nav/glossary partials, renders the site, and deploys
`_site/` to GitHub Pages on every push to `main`. Pull requests trigger the
build (so errors surface in CI) but do not deploy.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the expected chapter structure,
the archive policy, and the TOC-consistency check that runs in CI.

## Repository layout

```
.
├── _quarto.yml                # Quarto config: render list, sidebar, themes
├── index.qmd                  # Landing page
├── _glossary.qmd              # Generated glossary page
├── requirements.txt           # Python deps for notebook execution + scripts
├── theme/                     # Design system
│   ├── intmacro-light.scss    #   light theme tokens
│   ├── intmacro-dark.scss     #   dark theme tokens
│   ├── components.scss        #   shared component layer (sim-hero, MCQ, …)
│   ├── glossary-tooltips.js   #   hover definitions
│   └── widget-fallback.js     #   legacy-widget fallback notice
├── content/
│   ├── MODELS.md              # Canonical inventory + archive merge map
│   ├── *.qmd                  # v2 interactive chapters (Observable JS)
│   ├── *.ipynb                # v1 legacy chapters (static, pending conversion)
│   └── _archive/              # Historical variants, preserved with provenance
├── tracks/                    # Track overview pages
├── _includes/                 # Glossary/prereq data + generated partials
├── scripts/
│   ├── check_toc.py           # CI guardrail: sidebar ↔ filesystem consistency
│   ├── build_nav.py           # Generates prereq/related-chapter partials
│   └── build_glossary.py      # Generates glossary page + tooltip JSON
├── tests/                     # Tests for the build scripts
├── docs/                      # Design specs and plans (v1 + v2)
└── .github/workflows/
    └── deploy.yml             # Checks → render → GitHub Pages
```

## Credits

Built and maintained by [Ajai Upadhyaya](https://github.com/ajaiupadhyaya).
Reuse for teaching is welcome — issues and pull requests are open.
