"""Validate generated outputs for expected files and columns."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


REQUIRED_COLUMNS = {
    "data/domain_A_evolution/processed/mutation_rates_per_bp.csv": [
        "organism",
        "scientific_name",
        "rate_per_bp_per_generation",
        "genome_size_bp",
        "source",
    ],
    "data/domain_A_evolution/processed/mutation_rates_per_genome.csv": [
        "organism",
        "mutations_per_genome_per_generation",
        "notes",
        "source",
    ],
    "data/domain_A_evolution/processed/a2_major_transitions_esp_estimates.csv": [
        "transition",
        "esp_low",
        "esp_high",
    ],
    "data/domain_b/processed/domestication_timeline_compilation.csv": [
        "species",
        "scientific_name",
        "domestication_start_bp",
        "location",
        "duration_years",
    ],
    "results/tables/tbl01_cimmyt_esp.csv": [
        "program",
        "esp_breeding",
        "log10_esp_breeding",
    ],
    "results/tables/tbl_d1_directed_evolution_esp.csv": [
        "experiments_tested",
        "successes",
        "esp",
        "log10_esp",
    ],
    "results/tables/tbl_d2_ml_guided_esp.csv": [
        "experiments_tested",
        "successes",
        "esp",
        "log10_esp",
    ],
    "data/domain_e/processed/nnt_database.csv": [
        "intervention",
        "condition",
        "nnt",
        "therapeutic_area",
        "year",
    ],
    "data/domain_e/processed/fda_pivotal_trials.csv": [
        "record_id",
        "therapeutic_area",
        "nnt",
        "total_n",
    ],
    "results/tables/tbl_e1_nnt_summary_by_area.csv": [
        "therapeutic_area",
        "nnt_mean",
        "nnt_median",
    ],
    "results/tables/tbl_e1_nnt_by_year.csv": [
        "year",
        "nnt_mean",
        "nnt_median",
    ],
    "results/tables/tbl_e2_fda_trial_sizes_by_year.csv": [
        "year",
        "mean_total_n",
        "median_total_n",
    ],
    "results/tables/tbl_e2_fda_nnt_by_area.csv": [
        "therapeutic_area",
        "mean_nnt",
        "median_nnt",
    ],
    "results/tables/tbl_e4_gene_therapy_esp.csv": [
        "intervention",
        "n_treated",
        "responders_n",
        "esp",
        "log10_esp",
    ],
}


def _check_csv(path: Path, required_columns: list[str]) -> list[str]:
    """Check that a CSV exists, is non-empty, and has required columns."""
    errors = []
    if not path.exists():
        errors.append(f"Missing output: {path}")
        return errors
    if path.stat().st_size == 0:
        errors.append(f"Empty output: {path}")
        return errors
    df = pd.read_csv(path)
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append(f"Missing columns in {path}: {', '.join(missing)}")
    return errors


def main() -> None:
    """Run output validation checks."""
    errors: list[str] = []
    for rel_path, columns in REQUIRED_COLUMNS.items():
        errors.extend(_check_csv(PROJECT_ROOT / rel_path, columns))

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("All outputs validated.")


if __name__ == "__main__":
    main()
