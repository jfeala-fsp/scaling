"""Normalize major transitions ESP estimates into processed outputs."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_A_evolution" / "a2_major_transitions_esp_estimates.csv"
OUT_DIR = PROJECT_ROOT / "data" / "domain_A_evolution" / "processed"
OUTPUT_PATH = OUT_DIR / "a2_major_transitions_esp_estimates.csv"


def compile_major_transitions() -> None:
    """Copy and normalize major transitions ESP estimates into processed data."""
    df = pd.read_csv(INPUT_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    compile_major_transitions()
