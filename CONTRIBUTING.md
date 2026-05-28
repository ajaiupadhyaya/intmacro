# Contributing

Thanks for helping keep this book healthy. The goals are: keep the student experience coherent, keep the build green, and don't lose historical material.

## Quick rules

1. **One canonical notebook per model.** If you're adding new material that overlaps an existing chapter, *enrich the canonical page* rather than creating a parallel one. Use [`content/MODELS.md`](./content/MODELS.md) to find the canonical file.
2. **Never delete from `content/_archive/`.** Archive files are preserved verbatim with provenance notes. If you find an unstamped archive notebook, add a top-of-file admonition pointing to the canonical page that absorbed it.
3. **Edit `_toc.yml` and `content/MODELS.md` together.** A canonical notebook is one whose path appears in `_toc.yml`; the manifest must agree. The CI guardrail (`scripts/check_toc.py`) fails the build on disagreement.
4. **Notebooks ship with pre-executed outputs** (we set `execute_notebooks: "off"` in `_config.yml`). Run your notebook end-to-end before committing — broken or stale plots will go live as-is. Use `python clean_notebooks.py` to normalize metadata before committing.
5. **`jupyter-book build --warningiserror` must pass.** Local check: `jupyter-book clean . --all && jupyter-book build . --warningiserror --keep-going`. Common failure modes: broken cross-references, missing alt text, unresolved `:link:` targets in `grid-item-card` directives.

## Recommended notebook structure

Not strictly enforced, but the most successful chapters follow this rhythm:

```
1. Title + 2–3 sentence motivation
2. Learning goals (3–5 bullets — what the student will be able to do)
3. Core intuition (no equations yet)
4. Math: model statement, key derivations, steady state if applicable
5. Interactive simulator (ipywidgets / plotly — at least one parameter to play with)
6. Economic interpretation (what the simulator just showed)
7. Self-check questions (2–4 questions, ideally with collapsible answers)
8. Cross-references to related chapters
```

A page that has *only* math or *only* a simulator usually drifts off the dashboard's "interactive model" promise.

## Adding a new model

1. Create the notebook in `content/<model_id>.ipynb`. Use lowercase, underscore-separated names; avoid `&` and other URL-unfriendly characters.
2. Add the file to the appropriate `parts:` section of [`_toc.yml`](./_toc.yml). If a custom display title is needed (the filename is ambiguous), use the `title:` field.
3. Add a row to [`content/MODELS.md`](./content/MODELS.md): model ID, canonical path, merge sources (if any), status.
4. Run the TOC guardrail locally: `python scripts/check_toc.py`.
5. Build the book: `jupyter-book build . --warningiserror --keep-going`.

## Replacing or restructuring an existing chapter

1. **Do not delete the existing file.** Move it to `content/_archive/<old_name>.ipynb` with a top-of-file admonition naming the canonical replacement and the archive date. This keeps inbound links and search results pointed somewhere useful.
2. Update `_toc.yml` to reference the new canonical file.
3. Update the relevant row in `content/MODELS.md` (status: `superseded` for the archived file, `canonical` for the new one).

## CI guardrails

GitHub Actions runs on every push and PR (see [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)):

1. `python scripts/check_toc.py` — every file listed in `_toc.yml` exists; every canonical `.ipynb` outside `_archive/` is either in `_toc.yml` or is the book root.
2. `jupyter-book build . --warningiserror --keep-going` — all Sphinx warnings (broken refs, missing images, etc.) become errors.
3. `jupyter lite build` — the JupyterLite workspace builds successfully with all canonical notebooks.

PRs that fail any of these will not merge. The deploy step only runs on `push` to `main`.

## Local quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/check_toc.py         # quick structural check
jupyter-book clean . --all
jupyter-book build . --warningiserror --keep-going
open _build/html/index.html
```
