"""Compute ESP metrics for gene therapy and CAR-T outcomes."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_e" / "processed" / "e4_gene_therapy_cart_outcomes.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "tables" / "tbl_e4_gene_therapy_esp.csv"


def compute_gene_therapy_esp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ESP and log10(ESP) for gene therapy outcomes.

    Parameters
    ----------
    df : pd.DataFrame
        Gene therapy outcomes with treated and responder counts.

    Returns
    -------
    pd.DataFrame
        Dataset with computed response rates and ESP values.
    """
    df = df.copy()
    df["n_treated"] = pd.to_numeric(df["n_treated"], errors="coerce")
    df["responders_n"] = pd.to_numeric(df["responders_n"], errors="coerce")

    response_rate = df["responders_n"] / df["n_treated"]
    df["response_rate"] = df["response_rate"].fillna(response_rate)

    df["esp"] = df["n_treated"] / df["responders_n"].replace(0, np.nan)
    df["log10_esp"] = np.log10(df["esp"])
    return df


def main() -> None:
    """Load inputs, compute ESP values, and write the output table."""
    df = pd.read_csv(INPUT_PATH)
    df_out = compute_gene_therapy_esp(df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
