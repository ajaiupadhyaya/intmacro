# Model Inventory and Canonical Mapping

> Phase 0 deliverable for the dashboard revamp (see [`docs/plans/intmacro-dashboard-revamp.md`](../docs/plans/intmacro-dashboard-revamp.md)).
> One row per *model* (not per file). The "canonical" column points at the notebook that students will see in the sidebar; the "merge sources" column lists files whose best content should be folded in. The "status" column drives the Phase 2 merge queue.

## Legend

- `canonical` — active page in the sidebar; merge target.
- `merge-required` — has high-value material that belongs in the canonical page; merge in Phase 2.
- `keep-as-historical` — preserved verbatim under `content/_archive/` with a provenance note; not in sidebar.
- `superseded` — content already exists in canonical; preserved in `_archive/` only for git history.
- `rename-required` — filename misleads about content (e.g. `humancapital.ipynb` is a Solow-with-tech-progress notebook). Treated as canonical but flagged for a redirect-friendly rename in Phase 4.

## Filename / content mismatches flagged for Phase 4 rename pass

| File | Actual content | Suggested rename |
|---|---|---|
| `content/solow_model.ipynb` | Advanced Solow exercises + case studies | `solow_exercises.ipynb` |
| `content/adas_model.ipynb` | Advanced AD-AS exercises + case studies | `adas_exercises.ipynb` |
| `content/humancapital.ipynb` | Solow growth with labor-augmenting tech progress | `solow_tech_progress.ipynb` |
| `content/solow_bgp.ipynb` | The Solow Growth Model (core intro) | `solow_intro.ipynb` |
| `content/cash_money.ipynb` | Nominal vs Real GDP (overlaps `realvsnom`) | merge into `realvsnom.ipynb` (see below) |

Renames are deferred to Phase 4 so that we don't break the Phase 1 TOC + early Phase 2 merges. They will be done together with redirect aliases in `_config.yml`.

---

## Part 0 — Foundations & Welcome

| Model ID | Canonical | Title (current) | Status | Merge sources | Notes |
|---|---|---|---|---|---|
| `welcome` | `content/Preliminaries_new.ipynb` | 🌍 International Macroeconomics — A Comprehensive Guide | canonical | `Preliminaries_clean.ipynb` (merge best framing) | Becomes the book root and dashboard landing in Phase 1. Heavy link list will be trimmed to part cards. |
| `math_primer` | `content/Preliminaries.ipynb` | 📘 Preliminaries: The Mathematics of Economic Growth | canonical | — | Distinct role from `welcome` — keep as an early chapter, not the root. |
| — | `content/Preliminaries_clean.ipynb` | (alt welcome) | superseded | — | Move to `_archive/Preliminaries_clean.ipynb` after Phase 1 merge. |

## Part 1 — Measurement & National Accounts

| Model ID | Canonical | Title | Status | Merge sources | Notes |
|---|---|---|---|---|---|
| `gdp_expenditure` | `content/measuring_gdp.ipynb` | 📘 Measuring GDP: The Expenditure Approach | canonical | — | Strongest standalone page in this group. |
| `real_vs_nominal_time` | `content/realvsnom.ipynb` | 📘 Real vs. Nominal GDP Over Time | canonical | `cash_money.ipynb` (near-duplicate intro), `_archive/qGDP.ipynb` (quarterly framing), `_archive/real_gdp_growth.ipynb` (price-change framing) | High-overlap cluster — merge into one richer page. |
| `real_gdp_ppp` | `content/realgdpacross.ipynb` | 🌍 Comparing Real GDP Across Countries (PPP) | canonical | `_archive/mgcwrgdp.ipynb` (chain-weighting), `_archive/gabd.ipynb` only if PPP-relevant | — |
| `chain_weighted_gdp` | `content/two_goods_twoperiods.ipynb` | 🛒 Measuring Real GDP with Changing Prices | canonical | `_archive/real_gdp_growth.ipynb` (same topic, simpler), `_archive/mgcwrgdp.ipynb` (chain index theory) | Pair conceptually with `real_vs_nominal_time`. |
| — | `content/cash_money.ipynb` | 💰 Nominal vs. Real GDP | superseded | — | Best content folded into `realvsnom`; archive original. |
| — | `_archive/qGDP.ipynb` | 🗓️ Quarterly GDP Data | merge-required | → `realvsnom` | Quarterly growth-rate annualization worth preserving. |
| — | `_archive/real_gdp_growth.ipynb` | 🛒 Real GDP with Changing Prices | merge-required | → `two_goods_twoperiods` | — |
| — | `_archive/mgcwrgdp.ipynb` | 🧺 Many Goods & Chain-Weighted Real GDP | merge-required | → `two_goods_twoperiods` or `realgdpacross` | Laspeyres/Paasche/chain table is gold; preserve it. |
| — | `_archive/gabd.ipynb` | 📊 Growth Accounting (older variant) | merge-required | → `growth_acc` (Part 2) | Listed here for cross-reference only. |

## Part 2 — Growth & Long-Run Dynamics

| Model ID | Canonical | Title | Status | Merge sources | Notes |
|---|---|---|---|---|---|
| `levels_vs_growth` | `content/foundations_growth.ipynb` | 📘 Foundations of Growth: Levels vs. Growth Rates | canonical | — | Best opener for this part. |
| `cobb_douglas` | `content/cobb_d_prod.ipynb` | 📘 Cobb-Douglas Production Function | canonical | `_archive/cd_crsrevised.ipynb` (cleaner CRS framing) | — |
| `solow_intro` | `content/solow_bgp.ipynb` | 📈 The Solow Growth Model | canonical | `_archive/solowmodel.ipynb` (balanced-growth derivation), `_archive/solow_constantabar&l.ipynb` (no-tech baseline) | Core Solow intro. Despite filename `solow_bgp`, this is the main intro. Rename in Phase 4. |
| `solow_transition` | `content/solow_transition.ipynb` | Solow Transition with Constant L and A | canonical | `_archive/solow_constantabar&l.ipynb` | Currently very thin (1 md cell) — must be enriched in Phase 2. |
| `solow_pop_tech` | `content/solow_pop&_tech_growth.ipynb` | 📘 Solow Model with Population + Tech Growth | canonical | — | URL-unfriendly filename — Phase 4 rename to `solow_pop_tech_growth.ipynb`. |
| `solow_tech_progress` | `content/humancapital.ipynb` | 📚 Solow Growth Model with Technological Progress | rename-required | — | Filename misleads (says "humancapital", content is Solow+g). Phase 4 rename. |
| `solow_exercises` | `content/solow_model.ipynb` | 🎯 Advanced Exercises and Case Studies (Solow) | rename-required | — | Capstone exercises for the Solow block. |
| `romer` | `content/romer_model.qmd` | The Romer Model of Endogenous Growth | canonical | `_archive/romer_model_endogen.ipynb`, `_archive/romerendogenous.ipynb` | ✅ 2026-07-03: converted to v2 OJS chapter; v1 notebook archived. Archive-variant merges still pending. |
| `romer_scale` | `content/scale_effects.ipynb` | 📈 Scale Effects in the Romer Model | canonical | — | — |
| `solow_romer_hybrid` | `content/hybrid_model.ipynb` | 🧬 Solow-Romer Hybrid Growth Model | canonical | `_archive/solow_romer_hybrid.ipynb` | — |
| `growth_accounting` | `content/growth_acc.qmd` | Growth Accounting | canonical | `_archive/gabd.ipynb` | ✅ 2026-07-03: converted to v2 OJS chapter (decomposition + residual calculator; live-FRED section noted in math toggle, can't run statically); v1 notebook archived. `gabd` merge still pending. |
| `convergence` | `content/convergence_hypo.ipynb` | 📉 Convergence Hypothesis | canonical | — | — |
| `slowing_growth` | `content/slowinggrowth.ipynb` | 📉 Slowing Growth? Declining TFP Advancement | canonical | — | — |
| `robots_ces` | `content/robots.ipynb` | 🤖 Robots vs. Labor: CES Production | canonical | — | — |

## Part 3 — Intertemporal Choice & Labor

| Model ID | Canonical | Title | Status | Merge sources | Notes |
|---|---|---|---|---|---|
| `two_period_consumption` | `content/2_period_consump.ipynb` | ⏳ Trading Off Today for Tomorrow: Intertemporal Choice | canonical | `content/2_period_consump_backup.ipynb` (apparent duplicate — diff check needed), `content/two_period_model.ipynb` (cleaner equation walkthrough) | High overlap cluster. Backup file is almost certainly an exact duplicate of canonical; if so, drop. |
| — | `_archive/two_period_model_v1.ipynb` | ⏳ The Two-Period Consumption Model | superseded | — | ✅ 2026-07-02: Euler interpretation + geometric reading merged into `two_period_consumption.qmd`; archived with provenance. |
| — | `content/2_period_consump_backup.ipynb` | (apparent dup) | superseded | → diff against canonical | If identical, delete in Phase 2; else merge unique cells. |
| `labor_leisure` | `content/labor_leisure_model.qmd` | The Labor-Leisure Choice Model | canonical | — | ✅ 2026-07-02: converted to v2 OJS chapter; v1 notebook archived. |
| `tobin_q` | `content/tobin_q_model.qmd` | Investment & Tobin's q | canonical | — | ✅ 2026-07-02: converted to v2 OJS chapter; `_archive/mpk_tobin.ipynb` framing merged; v1 notebook archived. |

## Part 4 — Business Cycles & Policy Dynamics

| Model ID | Canonical | Title | Status | Merge sources | Notes |
|---|---|---|---|---|---|
| `is_curve` | `content/is_curve_model.qmd` | The IS Curve | canonical | — | ✅ 2026-07-02: converted to v2 OJS chapter; `_archive/iscurve.ipynb` intuition merged; v1 notebook archived. |
| `adas_sim` | `content/adassim.qmd` | Dynamic AD-AS with Monetary Policy | canonical | — | Primary AD-AS simulator. ✅ 2026-07-02: shock typology + impulse-response sim merged in from `dynamicshock`. |
| `adas_shocks` | `_archive/dynamicshock_v1.ipynb` | AD-AS Shocks and Dynamic Adjustment | superseded | — | ✅ 2026-07-02: merged into `adassim.qmd`; archived with provenance. |
| `adas_exercises` | `content/adas_model.ipynb` | 🎯 Advanced AD-AS Exercises and Case Studies | rename-required | — | Capstone exercises for AD-AS block. |
| `lucas_island` | `content/lucas_island_model.qmd` | The Lucas Island Model | canonical | — | ✅ 2026-07-03: converted to v2 OJS chapter (AD-AS surprise diagram + seeded islands sim); v1 notebook archived. |
| `eq_business_cycles` | `content/equilibrium_model.qmd` | Equilibrium Business Cycles with Persistence | canonical | — | ✅ 2026-07-03: converted to v2 OJS chapter; v1 notebook archived. Paired after Lucas in TOC. |
| `rbc` | `content/rbc_simulation.qmd` | The Real Business Cycle Model | canonical | — | ✅ 2026-07-03: converted to v2 OJS chapter. v1 code's consumption-smoothing rule was non-convergent (capital fell below old SS after a positive shock); v2 implements the capital partial-adjustment rule the v1 *text* specified — disclosed in the chapter's math toggle. v1 notebook archived. |

## Archive disposition summary

| Archive file | Disposition |
|---|---|
| `_archive/intro.ipynb` | empty stub — keep-as-historical, do not merge |
| `_archive/cd_crsrevised.ipynb` | merge-required → `cobb_d_prod` |
| `_archive/gabd.ipynb` | merge-required → `growth_acc` |
| `_archive/iscurve.ipynb` | ✅ merged into `is_curve_model.qmd` 2026-07-02 |
| `_archive/mgcwrgdp.ipynb` | merge-required → `two_goods_twoperiods` (and cross-ref `realgdpacross`) |
| `_archive/mpk_tobin.ipynb` | ✅ merged into `tobin_q_model.qmd` 2026-07-02 |
| `_archive/qGDP.ipynb` | merge-required → `realvsnom` |
| `_archive/real_gdp_growth.ipynb` | merge-required → `two_goods_twoperiods` |
| `_archive/romer_model_endogen.ipynb` | merge-required → `romer_model` |
| `_archive/romerendogenous.ipynb` | merge-required → `romer_model` |
| `_archive/solow_constantabar&l.ipynb` | merge-required → `solow_transition` (and `solow_intro`) |
| `_archive/solow_romer_hybrid.ipynb` | merge-required → `hybrid_model` |
| `_archive/solowmodel.ipynb` | merge-required → `solow_intro` |

Per direction: **no archive file is deleted**. After merge, each `_archive/*` file gets a provenance admonition at the top noting which canonical page absorbed its material.

## Merge wave order (Phase 2)

1. **Preliminaries cluster** — pick canonical landing, archive the rest. (Tied into Phase 1.)
2. **Two-period cluster** — small, high-confusion. Quick win.
3. **AD-AS cluster** — three overlapping notebooks; cleanup unlocks the business-cycle section.
4. **GDP measurement cluster** — `realvsnom` ↔ `cash_money` ↔ `_archive/qGDP` + `two_goods_twoperiods` ↔ archive variants.
5. **Growth cluster** — Solow + Romer + their five archive variants.
6. **Remaining single-archive merges** — `cobb_d_prod`, `growth_acc`, `is_curve_model`, `tobin_q_model`.

Each wave: enrich the canonical, stamp provenance on the archive, update `_toc.yml` only if structure changed.
