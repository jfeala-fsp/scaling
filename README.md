# ESP Research Project

This repository consolidates quantitative evidence for Experiments per Specified
Phenotype (ESP) across evolution, domestication, breeding, protein engineering,
and medicine.

The unified table lives at `data/master_esp_table.csv`.

Phenotype complexity normalization is defined in `data/phenotype_complexity_score.md`,
with assignments in `data/pcs_assignments.csv` and computed columns added by
`src/analysis/master_esp_table.py`.

## Quality Score Rubric (1-5)

- 5: Primary data with explicit denominators, direct counts, and clear endpoints.
- 4: Strong secondary sources with explicit counts; minor estimation required.
- 3: Mixed sources or moderate estimation; some parameters inferred.
- 2: High uncertainty or order-of-magnitude estimates; coarse inputs.
- 1: Speculative or placeholder values; requires primary-source verification.

Notes:
- Domain A mutation-rate rows define ESP as expected genomes per mutation event
  (1 / per-genome mutation rate), enabling direct comparison on log10 scale.
- Speed-breeding rows use time-normalized ESP derived from CIMMYT wheat ESP and
  reported cycle-time speedups; per-cycle ESP is unchanged.

## Reproducible Build

This repository uses Make to reproduce preprocessing and analysis outputs from raw inputs.

### Prerequisites

- Python 3.11+
- Install packages from `requirements.txt`:
  - `numpy`
  - `pandas`
- Network access is required to fetch TheNNT data during the build.

### Build

Run:
```bash
make build
```

`make build` reproduces all analysis outputs from raw data and standardized inputs.

### Validation

Run:
```bash
make test
```

This checks that generated outputs exist, are non-empty, and include required columns.

### Cleanup

Run:
```bash
make clean
```

This removes generated outputs so the build can be re-run from a clean state.
