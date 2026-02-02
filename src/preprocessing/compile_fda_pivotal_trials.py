import numpy as np
import pandas as pd

RAW_PATH = "data/domain_e/raw/fda_pivotal_trials_extracted.csv"
OUT_PATH = "data/domain_e/processed/fda_pivotal_trials.csv"


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """
    Safely divide two pandas Series with NaN handling.

    Parameters
    ----------
    numerator : pd.Series
        Numerator values.
    denominator : pd.Series
        Denominator values.

    Returns
    -------
    pd.Series
        Division results with NaN where denominator is missing or zero.
    """
    if not isinstance(numerator, pd.Series):
        numerator = pd.Series(numerator, index=denominator.index)
    return numerator.where(denominator.notna() & (denominator != 0)) / denominator


def compile_fda_pivotal_trials() -> pd.DataFrame:
    """
    Compile FDA pivotal trial data with derived response rates and NNT.

    Returns
    -------
    pd.DataFrame
        Processed FDA pivotal trial dataset.
    """
    df = pd.read_csv(RAW_PATH)

    numeric_cols = [
        "treatment_n",
        "control_n",
        "treatment_response_count",
        "control_response_count",
        "response_rate_treatment",
        "response_rate_control",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["response_rate_treatment"] = df["response_rate_treatment"].fillna(
        _safe_divide(df["treatment_response_count"], df["treatment_n"])
    )
    df["response_rate_control"] = df["response_rate_control"].fillna(
        _safe_divide(df["control_response_count"], df["control_n"])
    )

    df["response_rate_diff"] = df["response_rate_treatment"] - df["response_rate_control"]

    df["nnt_type"] = pd.NA
    df.loc[df["response_rate_control"].notna(), "nnt_type"] = "difference-based"
    df.loc[
        df["response_rate_control"].isna() & df["response_rate_treatment"].notna(),
        "nnt_type",
    ] = "single-arm (assumes 0 baseline)"

    df["nnt"] = np.where(
        df["nnt_type"] == "difference-based",
        _safe_divide(1.0, df["response_rate_diff"]),
        np.where(
            df["nnt_type"] == "single-arm (assumes 0 baseline)",
            _safe_divide(1.0, df["response_rate_treatment"]),
            np.nan,
        ),
    )

    df["total_n"] = df["treatment_n"].fillna(0) + df["control_n"].fillna(0)
    df.loc[df["total_n"] == 0, "total_n"] = np.nan

    df.to_csv(OUT_PATH, index=False)
    return df


if __name__ == "__main__":
    compile_fda_pivotal_trials()
