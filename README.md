# International Macroeconomics — Interactive Dashboard

A Jupyter Book of working macroeconomic models, originally built for the intermediate macroeconomics course at the University of Virginia. Each chapter is a self-contained notebook with the relevant math, an interactive simulator, and a short economic interpretation.

**Live site:** https://ajaiupadhyaya.github.io/intmacro/
**Live in-browser kernel (JupyterLite):** https://ajaiupadhyaya.github.io/intmacro/lite/lab/index.html

## What's in the book

Five tracks, organized in [`_toc.yml`](./_toc.yml):

1. **Foundations** — math primer (growth rates, log approximation).
2. **Measurement & National Accounts** — GDP, real vs. nominal, PPP, chain-weighted indices.
3. **Growth & Long-Run Dynamics** — Solow, Romer, hybrid, growth accounting, convergence, scale effects, CES.
4. **Intertemporal Choice & Labor** — two-period consumption, labor-leisure, Tobin's q.
5. **Business Cycles & Policy Dynamics** — IS curve, dynamic AD-AS with Taylor rule, Lucas Island, equilibrium business cycles, RBC.

The full canonical inventory (one row per model, including the merge map for archive material) lives in [`content/MODELS.md`](./content/MODELS.md).

## Running locally

```bash
git clone https://github.com/ajaiupadhyaya/intmacro
cd intmacro
python -m venv .venv && source .venv/bin/activate   # or your preferred env
pip install -r requirements.txt

# Build the static site
jupyter-book build .

# Open the result
open _build/html/index.html   # macOS
```

To rebuild from scratch:

```bash
jupyter-book clean . --all
jupyter-book build .
```

To build the in-browser JupyterLite app (matches the deployed `/lite/` workspace):

```bash
jupyter lite build --contents content --output-dir _build/html/lite
```

## Deploy flow

A single GitHub Actions workflow ([`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)) builds the book and the JupyterLite workspace on every push to `main`, then deploys to GitHub Pages. Pull requests trigger the build (so warnings/errors surface in CI) but do not deploy.

The deploy is intentionally strict: `jupyter-book build --warningiserror`. Cross-reference rot, broken images, and unresolvable links fail CI rather than silently shipping.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the expected structure of a model notebook, the archive policy, and the TOC-consistency check that runs in CI.

## Repository layout

```
.
├── _config.yml                # Jupyter Book config (theme, extensions, MathJax)
├── _toc.yml                   # Canonical part-based table of contents
├── jupyter-lite.json          # JupyterLite app config
├── requirements.txt           # Python deps for build + JupyterLite
├── clean_notebooks.py         # Notebook cleanliness helper (outputs/metadata)
├── scripts/
│   └── check_toc.py           # CI guardrail: TOC ↔ filesystem consistency
├── _static/
│   └── custom.css             # Theme overrides
├── content/
│   ├── MODELS.md              # Canonical inventory + archive merge map
│   ├── Preliminaries_new.ipynb  # Dashboard landing (book root)
│   ├── Preliminaries.ipynb    # Math primer
│   ├── <30 canonical model notebooks>
│   └── _archive/              # Historical variants, preserved with provenance
│       └── <16 archive notebooks>
├── docs/
│   └── plans/
│       └── intmacro-dashboard-revamp.md   # The revamp plan that produced this layout
└── .github/
    └── workflows/
        └── deploy.yml
```

## Credits

Built and maintained by [Ajai Upadhyaya](https://github.com/ajaiupadhyaya). Reuse for teaching is welcome — issues and pull requests are open.
