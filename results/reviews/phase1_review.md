# Phase 1 Review (D1, C1, C2, C3, D2)

Date: 2026-02-01
Reviewer: scaling/polecats/fury

## Scope
Review Phase 1 outputs for:
- D1 Directed evolution
- C1 Breeding programs
- C2 CGIAR/CIMMYT historical analysis
- C3 Speed breeding
- D2 ML-guided protein design

## Executive Summary
- C3 is complete and documented with citations and a structured JSON dataset.
- C2 is reproducible via script and has inputs + outputs, but depends on C1 inputs that are not present in-repo.
- D2 is documented but limited to three 2025 studies; coverage is incomplete for 2020-2024.
- D1 and C1 datasets are not present in this repository, which blocks full Phase 2 analysis.

## Task-by-Task Assessment

### D1: Directed evolution
Evidence located: None in-repo.
- No D1 data files or compiled datasets found under `data/`.
- No analysis scripts or tables found in `src/analysis/` or `results/`.

Quality: Not assessable (missing).
Completeness: Incomplete.
Readiness for Phase 2: Not ready.
Action: Compile directed evolution datasets (library size, hits, success rates) into `data/` with clear sources and a reproducible script to compute ESP.

### C1: Breeding programs
Evidence located: None in-repo.
- C2 analysis references C1 inputs in an absolute path outside this repo.

Quality: Not assessable (missing).
Completeness: Incomplete.
Readiness for Phase 2: Not ready.
Action: Add C1 breeding program data into `data/` and update references to use repo-relative paths.

### C2: CGIAR/CIMMYT historical analysis
Evidence located:
- Inputs: `data/domain_c/c2_cimmyt_inputs.csv`
- Analysis: `src/analysis/c2_cimmyt_esp.py`
- Results: `results/tables/tbl01_cimmyt_esp.csv`
- Documentation: `data/domain_c/C2_cgiar_cimmyt_analysis.md`

Quality: Good structure, reproducible via script.
Completeness: Partial (depends on missing C1 inputs).
Readiness for Phase 2: Provisional.
Notes:
- [REVIEW] C2 analysis cites a C1 file at an absolute path not present in-repo; this breaks reproducibility and should be replaced with a repo-relative source.
- [REVIEW] Confirm C1 aggregated inputs against Evenson and Gollin (2003) and Duvick (2005).

### C3: Speed breeding
Evidence located:
- Literature review: `data/domain_c_breeding/C3_speed_breeding_literature_review.md`
- Structured data: `data/domain_c_breeding/speed_breeding_data.json`

Quality: Strong; includes citations, quantitative table, and a structured JSON dataset.
Completeness: Good for a Phase 1 literature review.
Readiness for Phase 2: Ready, with one caveat.
Notes:
- [REVIEW] Speedup calculations assume a 2-3 generations/year baseline across crops; adjust if crop-specific baselines are available.

### D2: ML-guided protein design
Evidence located:
- Dataset: `data/domain_d/ml_guided_design_outcomes.csv`
- Documentation: `data/domain_d/README.md`

Quality: Good documentation and traceability to primary sources.
Completeness: Partial (only three studies, all 2025).
Readiness for Phase 2: Provisional.
Notes:
- Coverage should be expanded to 2020-2024 ML-guided design outcomes.
- Consider adding a script to recompute ESP from `experiments_tested` and `successes` to improve reproducibility.

## Overall Readiness for Phase 2
- Ready: C3 (speed breeding).
- Provisional: C2 (dependent on missing C1 data), D2 (limited coverage).
- Not ready: D1, C1 (missing in-repo datasets).

## Recommended Follow-ups
1. Add C1 breeding program datasets to `data/` and update C2 references to repo-relative paths.
2. Compile D1 directed evolution datasets with reproducible ESP calculations.
3. Expand D2 dataset with additional studies (2020-2024) and add a reproducible ESP script.
