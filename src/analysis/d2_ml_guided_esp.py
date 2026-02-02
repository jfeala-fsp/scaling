"""Compute ESP values for ML-guided protein design outcomes."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_d" / "ml_guided_design_outcomes.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "tables" / "tbl_d2_ml_guided_esp.csv"


def compute_esp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ESP values from experiments tested and successes.

    Parameters
    ----------
    df : pd.DataFrame
        Input data with experiments_tested and successes columns.

    Returns
    -------
    pd.DataFrame
        Dataframe with computed ESP and log10(ESP).
    """
    df = df.copy()
    successes = df["successes"].replace(0, np.nan)
    df["esp"] = df["experiments_tested"] / successes
    df["log10_esp"] = np.log10(df["esp"])
    return df


def main() -> None:
    """Load inputs, compute ESP values, and write the output table."""
    df = pd.read_csv(INPUT_PATH)
    df_out = compute_esp(df)
    df_out.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
