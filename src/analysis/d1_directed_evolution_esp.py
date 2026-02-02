"""Compute ESP metrics for directed evolution outcomes."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_d" / "directed_evolution_outcomes.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "tables" / "tbl_d1_directed_evolution_esp.csv"


def compute_esp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ESP metrics for directed evolution datasets.

    Parameters
    ----------
    df : pd.DataFrame
        Directed evolution dataset with experiments tested and successes.

    Returns
    -------
    pd.DataFrame
        Dataset with ESP and log10(ESP) columns added.
    """
    df = df.copy()
    df["experiments_tested"] = pd.to_numeric(df["experiments_tested"], errors="coerce")
    df["successes"] = pd.to_numeric(df["successes"], errors="coerce")
    df["esp"] = df["experiments_tested"] / df["successes"]
    df["log10_esp"] = np.log10(df["esp"])
    return df


def main() -> None:
    """Load inputs, compute ESP values, and write the output table."""
    df = pd.read_csv(INPUT_PATH)
    df_out = compute_esp(df)
    df_out.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
