# Phase 1 Comprehensive Review (A1/A2, B1, C1/C2/C3, D1/D2, E1/E2/E4)

Date: 2026-02-02
Reviewer: scaling/polecats/thunder

## Scope
Review Phase 1 outputs for:
- A1/A2: Evolution data (mutation rates, major transitions ESP)
- B1: Domestication timelines (wheat, maize, dogs, cattle)
- C1/C2/C3: Breeding programs (CIMMYT/CGIAR, speed breeding)
- D1/D2: Protein engineering (directed evolution, ML-guided design)
- E1/E2/E4: Medical interventions (NNT database, FDA pivotal trials, gene therapy/CAR-T)

## Executive Summary
- A1/A2 deliver strong literature coverage and a structured A2 CSV, but A1 lacks a machine-readable dataset and A2 relies on coarse assumptions that diverge from the mutation-based ESP formula in the research plan.
- B1 provides structured CSV/JSON with ESP estimates and citations; unit consistency (BP/BCE) and trait-fixation ranges need normalization.
- C1 is well documented but not yet in a structured dataset; C2 is reproducible via script and inputs, but the inputs are period averages that should be traceable to source tables.
- C3 is strong and well documented; baseline generation assumptions should be crop-specific or handled via sensitivity analysis.
- D1 and D2 have structured datasets; D1 is narrow (3 recent studies), and D2 mixes experimental-denominator ESP with heavy in silico pre-filtering without a parallel "full design space" denominator.
- E1/E2/E4 are reproducible and documented; however, E1 relies on TheNNT summaries with missing time horizons/CIs, E2 includes single-arm "NNT" values based on 0 baseline assumptions, and E4 endpoints vary across therapies, which complicates cross-comparison.

## Domain Reviews

### A1: Evolution literature review
Evidence:
- `data/domain_A_evolution/A1_evolution_literature_review.md`

Quality: Strong annotated bibliography with citations and a compact summary table.
Completeness: Partial for analysis; the integrated data table is not stored in a structured CSV.
Methodology: Clear narrative, but numeric fields are not consistently sourced to a machine-readable table.
Consistency: Units and uncertainty are noted, but not standardized for downstream analysis.
Readiness: Provisional.
Key issues:
- A1 data table needs to be exported to a CSV (taxon, mutation rate, Ne, generation time, innovation time).
- Several entries use "Unknown" or estimates without explicit error ranges.

### A2: Major transitions data extraction
Evidence:
- `data/domain_A_evolution/A2_major_transitions_data_extraction.md`
- `data/domain_A_evolution/a2_major_transitions_esp_estimates.csv`

Quality: Structured CSV with transparent assumptions and clear [VERIFY]/[REVIEW] flags.
Completeness: Moderate; covers all eight transitions but relies on broad ranges.
Methodology: Uses ESP = Ne * generations (individual-based), which diverges from the mutation-rate ESP formula in the research plan.
Consistency: Coarse estimates are internally consistent, but not harmonized to mutation-based ESP.
Readiness: Provisional.
Key issues:
- Align A2 with the plan by adding a mutation-based ESP column (Ne * generations * mutation rate * sites), or formally justify a separate "individual-based ESP" track.
- Several transitions (multicellularity, eusociality, language) need multi-origin or cultural evolution adjustments.

### B1: Domestication timelines
Evidence:
- `data/domain_b/domestication_timeline_compilation.csv`
- `data/domain_b/domestication_data.json`
- `data/domain_b/B1_domestication_timeline_compilation.md`

Quality: Good; structured datasets with citations and ESP calculations.
Completeness: Good for core species (wheat, maize, dogs, cattle).
Methodology: ESP calculations are documented; trait fixation ranges are broad but appropriate for order-of-magnitude estimates.
Consistency: Mixed time formats (BP, BCE) and ranges should be normalized for analysis.
Readiness: Provisional.
Key issues:
- Standardize time fields (use BP or BCE consistently) and include explicit numeric bounds.
- Dogs show unusually low ESP; ensure this is tied to specific traits, not aggregated domestication outcomes.

### C1: Breeding program data acquisition
Evidence:
- `data/domain_c/C1_breeding_programs.md`

Quality: Strong narrative compilation with explicit calculations.
Completeness: Moderate; private-sector data are limited and values are often "program averages."
Methodology: ESP formula is correctly applied and documented.
Consistency: Data are not in a structured dataset, limiting reproducibility and downstream analysis.
Readiness: Provisional.
Key issues:
- Convert C1 quantitative tables into a CSV with explicit fields and source citations.
- Separate public vs private program data in structured form.

### C2: CGIAR/CIMMYT historical analysis
Evidence:
- `data/domain_c/c2_cimmyt_inputs.csv`
- `src/analysis/c2_cimmyt_esp.py`
- `results/tables/tbl01_cimmyt_esp.csv`
- `data/domain_c/C2_cgiar_cimmyt_analysis.md`

Quality: Good; reproducible via script and stored inputs.
Completeness: Good for CIMMYT wheat and maize; depends on C1 averages.
Methodology: Clear and consistent with ESP formula.
Consistency: Inputs reflect aggregated averages; source traceability should be strengthened.
Readiness: Ready for Phase 2 with minor verification.
Key issues:
- Validate inputs against Evenson & Gollin (2003) and Duvick (2005) source tables.
- Consider adding era-specific inputs (1970s vs 1990s) to capture improvements.

### C3: Speed breeding
Evidence:
- `data/domain_c_breeding/C3_speed_breeding_literature_review.md`
- `data/domain_c_breeding/speed_breeding_data.json`

Quality: Strong; clear citations and structured data.
Completeness: Good for Phase 1.
Methodology: Transparent; uses baseline 2-3 generations/year.
Consistency: Assumes uniform baseline across crops.
Readiness: Ready with a sensitivity check.
Key issues:
- Use crop-specific baseline generation rates or explicitly treat baseline as a parameter in sensitivity analysis.

### D1: Directed evolution outcomes
Evidence:
- `data/domain_d/directed_evolution_outcomes.csv`
- `src/analysis/d1_directed_evolution_esp.py`
- `results/tables/tbl_d1_directed_evolution_esp.csv`
- `data/domain_d/README.md`

Quality: Good documentation and reproducible ESP calculations.
Completeness: Low; only three recent studies (2025-2026).
Methodology: Straightforward ESP calculation from experiments and successes.
Consistency: Success definitions vary by study, but noted.
Readiness: Not ready for Phase 2 curve fitting due to limited temporal coverage.
Key issues:
- Add historical directed evolution datasets (1990s-2010s, classic Arnold lab and related datasets).
- Clarify multi-round screening totals (per-round vs cumulative) in the data notes.

### D2: ML-guided protein design
Evidence:
- `data/domain_d/ml_guided_design_outcomes.csv`
- `data/domain_d/README.md`

Quality: Good primary sources with explicit experimental denominators.
Completeness: Moderate; 2021-2025 coverage, limited pre-2021.
Methodology: ESP values computed in the CSV; no dedicated script to regenerate ESP.
Consistency: Uses experimentally characterized designs as denominator, excluding in silico filtering steps.
Readiness: Provisional.
Key issues:
- Add a reproducible ESP computation script (parallel to D1).
- Consider recording both "experimental ESP" and "full pipeline ESP" (including in silico filtering counts) for consistent cross-domain comparison.

### E1: Historical NNT database
Evidence:
- `data/domain_e/processed/nnt_database.csv`
- `src/preprocessing/extract_thennt_nnt.py`
- `src/analysis/e1_nnt_summary.py`
- `results/tables/tbl_e1_nnt_summary_by_area.csv`
- `results/tables/tbl_e1_nnt_by_year.csv`

Quality: Reproducible extraction; consistent schema.
Completeness: Moderate; TheNNT coverage is broad but not exhaustive.
Methodology: NNT values are extracted from TheNNT summaries; time horizons and CIs are often missing.
Consistency: Mixes benefit and harm outcomes in a single table.
Readiness: Provisional.
Key issues:
- Prioritize verification of time horizons and exact NNT definitions via primary sources.
- Separate benefit and harm analyses for ESP interpretation, or filter to benefit outcomes for curve fitting.

### E2: FDA pivotal trial outcomes
Evidence:
- `data/domain_e/processed/fda_pivotal_trials.csv`
- `src/preprocessing/compile_fda_pivotal_trials.py`
- `src/analysis/e2_fda_summary.py`
- `results/tables/tbl_e2_fda_trial_sizes_by_year.csv`
- `results/tables/tbl_e2_fda_nnt_by_area.csv`

Quality: Structured, reproducible, and traceable to label sections.
Completeness: Limited sample size; not a comprehensive FDA catalog.
Methodology: Difference-based NNT for randomized trials; single-arm trials compute NNT using a 0-baseline assumption.
Consistency: Endpoints and response metrics vary across therapies.
Readiness: Provisional.
Key issues:
- Flag single-arm "NNT" values as ESP-like response rates, not true NNTs.
- Standardize endpoints or stratify analyses by endpoint type (ORR, CR, SVR12, etc.).

### E4: Gene therapy and CAR-T outcomes
Evidence:
- `data/domain_e/processed/e4_gene_therapy_cart_outcomes.csv`
- `data/domain_e/E4_gene_therapy_cart_notes.md`

Quality: High; extracted from FDA labels with explicit denominators.
Completeness: Limited to four therapies.
Methodology: ESP computed as 1/response rate (single-arm).
Consistency: Endpoint definitions vary across therapies.
Readiness: Provisional.
Key issues:
- Expand to additional approved gene therapies and CAR-Ts.
- Harmonize endpoint definitions or provide a mapping to comparable outcome classes.

## Critical Issues and Gaps
1. Missing structured datasets for A1 and C1 prevent direct integration into Phase 2 analysis.
2. D1 coverage is too narrow for curve fitting; historical data are required.
3. E1 relies on TheNNT summaries with missing time horizons and CIs; primary-source verification is needed for high-quality analysis.
4. E2/E4 include single-arm "NNT" values based on 0-baseline assumptions, which are not comparable to randomized-trial NNTs without explicit labeling.

## Recommendations for Phase 2
1. Export A1 and C1 tables to CSV with consistent units, source citations, and data-quality scores.
2. Add a mutation-based ESP column to A2 (or justify dual ESP definitions).
3. Expand D1 and D2 to include historical and pre-2021 datasets; add a reproducible ESP script for D2.
4. Standardize clinical endpoints and separate randomized-trial NNT from single-arm ESP-like values.
5. Prioritize source verification for E1 entries flagged [VERIFY] and add CIs/time horizons where available.

## Overall Readiness for F2
- Ready: C2, C3
- Provisional: A1/A2, B1, C1, D2, E1, E2, E4
- Not ready: D1 (insufficient temporal coverage)

## Sign-off Status
Not signed off for F2 curve fitting. Proceed after:
- Structured A1/C1 datasets are added,
- D1 historical coverage is expanded,
- E1 verification and E2/E4 endpoint labeling are completed.
