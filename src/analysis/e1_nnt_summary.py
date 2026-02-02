from pathlib import Path

import pandas as pd


def main() -> None:
    """Generate summary tables for the historical NNT database."""
    root = Path(__file__).resolve().parents[2]
    data_path = root / "data" / "domain_e" / "processed" / "nnt_database.csv"
    summary_path = root / "results" / "tables" / "tbl_e1_nnt_summary_by_area.csv"
    summary_time_path = (
        root / "results" / "tables" / "tbl_e1_nnt_summary_by_area_time.csv"
    )
    trend_path = root / "results" / "tables" / "tbl_e1_nnt_by_year.csv"

    df = pd.read_csv(data_path)
    df["nnt"] = pd.to_numeric(df["nnt"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "follow_up_bucket" in df.columns:
        df["follow_up_bucket"] = df["follow_up_bucket"].fillna("missing")

    summary = (
        df.groupby("therapeutic_area", dropna=False)
        .agg(
            n_entries=("nnt", "count"),
            n_unique_interventions=("intervention", "nunique"),
            nnt_mean=("nnt", "mean"),
            nnt_median=("nnt", "median"),
            nnt_min=("nnt", "min"),
            nnt_max=("nnt", "max"),
            year_min=("year", "min"),
            year_max=("year", "max"),
        )
        .reset_index()
    )
    summary["nnt_mean"] = summary["nnt_mean"].round(2)
    summary["nnt_median"] = summary["nnt_median"].round(2)
    summary.to_csv(summary_path, index=False)

    if "follow_up_bucket" in df.columns:
        summary_time = (
            df.groupby(["therapeutic_area", "follow_up_bucket"], dropna=False)
            .agg(
                n_entries=("nnt", "count"),
                n_unique_interventions=("intervention", "nunique"),
                nnt_mean=("nnt", "mean"),
                nnt_median=("nnt", "median"),
                nnt_min=("nnt", "min"),
                nnt_max=("nnt", "max"),
                year_min=("year", "min"),
                year_max=("year", "max"),
            )
            .reset_index()
        )
        summary_time["nnt_mean"] = summary_time["nnt_mean"].round(2)
        summary_time["nnt_median"] = summary_time["nnt_median"].round(2)
        summary_time.to_csv(summary_time_path, index=False)

    trend = (
        df.groupby("year", dropna=False)
        .agg(
            n_entries=("nnt", "count"),
            nnt_mean=("nnt", "mean"),
            nnt_median=("nnt", "median"),
            nnt_min=("nnt", "min"),
            nnt_max=("nnt", "max"),
        )
        .reset_index()
        .sort_values("year")
    )
    trend["nnt_mean"] = trend["nnt_mean"].round(2)
    trend["nnt_median"] = trend["nnt_median"].round(2)
    trend.to_csv(trend_path, index=False)


if __name__ == "__main__":
    main()
