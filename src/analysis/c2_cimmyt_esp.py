"""Compute CGIAR/CIMMYT ESP breeding estimates from compiled inputs."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_c" / "c2_cimmyt_inputs.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "tables" / "tbl01_cimmyt_esp.csv"


def compute_esp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ESP metrics for breeding programs.

    Parameters
    ----------
    df : pd.DataFrame
        Input data with crosses, progeny, selection cycles, and releases.

    Returns
    -------
    pd.DataFrame
        Dataframe with derived totals and ESP estimates.
    """
    df = df.copy()
    df["total_crosses"] = df["crosses_per_year"] * df["years"]
    df["total_experiments"] = (
        df["total_crosses"] * df["progeny_per_cross"] * df["selection_cycles"]
    )
    df["esp_breeding"] = df["total_experiments"] / df["released_varieties"]
    df["log10_esp_breeding"] = np.log10(df["esp_breeding"])
    return df


def main() -> None:
    """Load inputs, compute ESP values, and write the output table."""
    df = pd.read_csv(INPUT_PATH)
    df_out = compute_esp(df)
    df_out.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
