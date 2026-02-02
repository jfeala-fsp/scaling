"""Parse mutation rate tables from Markdown into structured CSV outputs."""
from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_A_evolution" / "mutation_rates_compilation.md"
OUT_DIR = PROJECT_ROOT / "data" / "domain_A_evolution" / "processed"
OUT_PER_BP = OUT_DIR / "mutation_rates_per_bp.csv"
OUT_PER_GENOME = OUT_DIR / "mutation_rates_per_genome.csv"


def _normalize_text(text: str) -> str:
    """Normalize Markdown table text to ASCII-friendly content."""
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u00d7": "x",
        "\u00a0": " ",
    }
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    text = re.sub(r"[*_`]", "", text)
    return text.strip()


def _parse_markdown_table(lines: list[str], start_index: int) -> tuple[list[str], list[dict], int]:
    """Parse a Markdown table starting at the given line index."""
    header_line = lines[start_index]
    headers = [_normalize_text(cell) for cell in header_line.strip().strip("|").split("|")]
    data_rows = []
    index = start_index + 2  # skip header + separator
    while index < len(lines):
        line = lines[index]
        if not line.strip().startswith("|"):
            break
        cells = [_normalize_text(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) == len(headers):
            data_rows.append(dict(zip(headers, cells)))
        index += 1
    return headers, data_rows, index


def _extract_table(lines: list[str], heading: str) -> list[dict]:
    """Extract the first table following a heading."""
    for idx, line in enumerate(lines):
        if line.strip().startswith(heading):
            for table_idx in range(idx + 1, len(lines)):
                if lines[table_idx].strip().startswith("|") and "---" in lines[table_idx + 1]:
                    _, rows, _ = _parse_markdown_table(lines, table_idx)
                    return rows
    return []


def compile_mutation_rates() -> None:
    """Compile mutation rate tables into CSV outputs."""
    text = INPUT_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    per_bp_rows = _extract_table(lines, "## 1. Per Base Pair Per Generation Mutation Rates")
    per_genome_rows = _extract_table(lines, "## 2. Per Genome Per Generation Mutation Rates")

    per_bp_df = pd.DataFrame(per_bp_rows).rename(
        columns={
            "Organism": "organism",
            "Scientific Name": "scientific_name",
            "Rate (per bp per generation)": "rate_per_bp_per_generation",
            "Genome Size (bp)": "genome_size_bp",
            "Source": "source",
        }
    )
    per_bp_df = per_bp_df[
        ["organism", "scientific_name", "rate_per_bp_per_generation", "genome_size_bp", "source"]
    ]

    per_genome_df = pd.DataFrame(per_genome_rows).rename(
        columns={
            "Organism": "organism",
            "Mutations per genome per generation": "mutations_per_genome_per_generation",
            "Notes": "notes",
            "Source": "source",
        }
    )
    per_genome_df = per_genome_df[
        ["organism", "mutations_per_genome_per_generation", "notes", "source"]
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    per_bp_df.to_csv(OUT_PER_BP, index=False)
    per_genome_df.to_csv(OUT_PER_GENOME, index=False)


if __name__ == "__main__":
    compile_mutation_rates()
