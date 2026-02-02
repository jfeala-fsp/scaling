import pandas as pd

INPUT_PATH = "data/domain_e/processed/fda_pivotal_trials.csv"
OUT_TRIAL_SIZES = "results/tables/tbl_e2_fda_trial_sizes_by_year.csv"
OUT_NNT_BY_AREA = "results/tables/tbl_e2_fda_nnt_by_area.csv"


def summarize_fda_trials() -> None:
    """
    Generate summary tables for FDA pivotal trial sizes and NNT values.
    """
    df = pd.read_csv(INPUT_PATH)

    trial_sizes = (
        df.dropna(subset=["total_n"])
        .groupby("year", as_index=False)
        .agg(
            n_trials=("record_id", "count"),
            mean_total_n=("total_n", "mean"),
            median_total_n=("total_n", "median"),
            min_total_n=("total_n", "min"),
            max_total_n=("total_n", "max"),
        )
        .sort_values("year")
    )

    nnt_by_area = (
        df.dropna(subset=["nnt"])
        .groupby("therapeutic_area", as_index=False)
        .agg(
            n_trials=("record_id", "count"),
            mean_nnt=("nnt", "mean"),
            median_nnt=("nnt", "median"),
            min_nnt=("nnt", "min"),
            max_nnt=("nnt", "max"),
        )
        .sort_values("therapeutic_area")
    )

    trial_sizes.to_csv(OUT_TRIAL_SIZES, index=False)
    nnt_by_area.to_csv(OUT_NNT_BY_AREA, index=False)


if __name__ == "__main__":
    summarize_fda_trials()
