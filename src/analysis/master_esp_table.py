"""
Build the master ESP table by consolidating all domain datasets.

Outputs
-------
data/master_esp_table.csv
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PCS_ASSIGNMENTS_PATH = ROOT / "data/pcs_assignments.csv"


def _log10(value: float) -> float:
    if value <= 0:
        raise ValueError(f"ESP must be positive; got {value}")
    return float(np.log10(value))


def _format_sources(refs: Iterable[Dict[str, Any]], max_items: int = 3) -> str:
    items = []
    for ref in refs:
        authors = ref.get("authors", "").strip()
        year = ref.get("year", "")
        if authors and year:
            items.append(f"{authors} {year}")
        elif authors:
            items.append(authors)
    return "; ".join(items[:max_items]) if items else "Unknown"


def _extract_year(text: str) -> str:
    match = re.search(r"(19|20)\d{2}", text or "")
    return match.group(0) if match else "unknown"


def _load_pcs_assignments() -> List[Dict[str, Any]]:
    if not PCS_ASSIGNMENTS_PATH.exists():
        raise FileNotFoundError(f"Missing PCS assignments: {PCS_ASSIGNMENTS_PATH}")
    df = pd.read_csv(PCS_ASSIGNMENTS_PATH)
    assignments: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        domain = str(row.get("Domain", "")).strip()
        pattern = str(row.get("Subdomain_pattern", "")).strip()
        if not domain or not pattern:
            continue
        assignments.append(
            {
                "domain": domain,
                "pattern": re.compile(pattern),
                "pcs_level": int(row.get("PCS_level")),
                "pcs_score": float(row.get("PCS_score")),
                "pcs_method": str(row.get("PCS_method", "")).strip() or "rubric",
                "pcs_notes": str(row.get("PCS_notes", "")).strip() or None,
            }
        )
    return assignments


def _match_pcs(domain: str, subdomain: str, assignments: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for assignment in assignments:
        assignment_domain = assignment["domain"]
        if assignment_domain not in {"*", "ANY", "Any", "any"} and assignment_domain != domain:
            continue
        if assignment["pattern"].search(subdomain):
            return assignment
    return None


def _apply_pcs_assignments(df: pd.DataFrame) -> pd.DataFrame:
    assignments = _load_pcs_assignments()
    pcs_levels: List[int | None] = []
    pcs_scores: List[float | None] = []
    pcs_methods: List[str | None] = []
    pcs_notes: List[str | None] = []
    esp_normalized: List[float | None] = []
    log10_esp_normalized: List[float | None] = []

    for _, row in df.iterrows():
        match = _match_pcs(str(row["Domain"]), str(row["Subdomain"]), assignments)
        if match is None:
            pcs_levels.append(None)
            pcs_scores.append(None)
            pcs_methods.append(None)
            pcs_notes.append(None)
            esp_normalized.append(None)
            log10_esp_normalized.append(None)
            continue
        pcs_score = float(match["pcs_score"])
        pcs_levels.append(int(match["pcs_level"]))
        pcs_scores.append(pcs_score)
        pcs_methods.append(match["pcs_method"])
        pcs_notes.append(match["pcs_notes"])
        if pcs_score > 0:
            esp_norm = float(row["ESP"]) / pcs_score
            esp_normalized.append(esp_norm)
            log10_esp_normalized.append(_log10(esp_norm))
        else:
            esp_normalized.append(None)
            log10_esp_normalized.append(None)

    return df.assign(
        PCS_level=pcs_levels,
        PCS_score=pcs_scores,
        PCS_method=pcs_methods,
        PCS_notes=pcs_notes,
        ESP_normalized=esp_normalized,
        log10_ESP_normalized=log10_esp_normalized,
    )


def _rows_domain_a_major_transitions() -> List[Dict[str, Any]]:
    path = ROOT / "data/domain_A_evolution/a2_major_transitions_esp_estimates.csv"
    df = pd.read_csv(path)
    rows: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        log10_low = row.get("log10_esp_low")
        log10_high = row.get("log10_esp_high")
        if pd.notna(log10_low) and pd.notna(log10_high):
            log10_esp = float((log10_low + log10_high) / 2.0)
            esp = 10 ** log10_esp
        else:
            esp_low = row.get("esp_low")
            esp_high = row.get("esp_high")
            if pd.isna(esp_low) or pd.isna(esp_high):
                continue
            esp = math.sqrt(float(esp_low) * float(esp_high))
            log10_esp = _log10(esp)
        rows.append(
            {
                "Domain": "Evolution",
                "Subdomain": f"Major transition: {row['transition']}",
                "Time_period": row.get("time_window_notes", "unknown"),
                "ESP": esp,
                "log10_ESP": log10_esp,
                "Quality_score": 2,
                "Source": "Maynard Smith & Szathmary 1995; A2 major transitions",
            }
        )
    return rows


def _rows_domain_a_mutation_rates() -> List[Dict[str, Any]]:
    # Per-genome mutation rates summarized in mutation_rates_compilation.md.
    # ESP defined here as expected genomes per mutation event (1 / rate).
    entries = [
        {
            "label": "Mutation rate baseline: E. coli",
            "rate_per_genome": 0.003,
            "source": "Drake 1991; Drake et al. 1998; Lee et al. 2012",
        },
        {
            "label": "Mutation rate baseline: S. cerevisiae",
            "rate_per_genome": 0.003,
            "source": "Lynch et al. 2008; Zhu et al. 2014",
        },
        {
            "label": "Mutation rate baseline: C. elegans",
            "rate_per_genome": 2.1,
            "source": "Denver et al. 2009",
        },
        {
            "label": "Mutation rate baseline: D. melanogaster",
            "rate_per_genome": 1.0,
            "source": "Keightley et al. 2009",
        },
        {
            "label": "Mutation rate baseline: Mouse",
            "rate_per_genome": 30.0,
            "source": "Uchimura et al. 2015; Lindsay et al. 2019",
        },
        {
            "label": "Mutation rate baseline: Human",
            "rate_per_genome": 80.0,
            "source": "Kong et al. 2012; BioNumbers",
        },
    ]
    rows: List[Dict[str, Any]] = []
    for entry in entries:
        esp = 1.0 / float(entry["rate_per_genome"])
        rows.append(
            {
                "Domain": "Evolution",
                "Subdomain": entry["label"],
                "Time_period": "modern",
                "ESP": esp,
                "log10_ESP": _log10(esp),
                "Quality_score": 4,
                "Source": entry["source"],
            }
        )
    return rows


def _rows_domain_b_domestication() -> List[Dict[str, Any]]:
    path = ROOT / "data/domain_b/domestication_data.json"
    data = json.loads(path.read_text())
    summary = data.get("summary", {}).get("esp_estimates", {})
    rows: List[Dict[str, Any]] = []
    for species_key, species in data.get("species", {}).items():
        esp_info = summary.get(species_key, {})
        esp = esp_info.get("esp")
        log10_esp = esp_info.get("log10_esp")
        if esp is None or log10_esp is None:
            continue
        timeline = species.get("domestication_timeline", {})
        if "start_date_bp" in timeline:
            time_period = f"{timeline['start_date_bp']} BP"
        elif "genetic_estimate_kya" in timeline:
            time_period = f"{timeline['genetic_estimate_kya']} kya"
        else:
            time_period = "unknown"
        quality = species.get("data_quality", {})
        quality_scores = [float(v) for v in quality.values() if isinstance(v, (int, float))]
        quality_score = int(round(float(np.mean(quality_scores)))) if quality_scores else 3
        rows.append(
            {
                "Domain": "Domestication",
                "Subdomain": f"Domestication: {species_key}",
                "Time_period": time_period,
                "ESP": float(esp),
                "log10_ESP": float(log10_esp),
                "Quality_score": quality_score,
                "Source": _format_sources(species.get("key_references", [])),
            }
        )
    return rows


def _rows_domain_c_breeding() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    c2_path = ROOT / "results/tables/tbl01_cimmyt_esp.csv"
    df = pd.read_csv(c2_path)
    for _, row in df.iterrows():
        rows.append(
            {
                "Domain": "Breeding",
                "Subdomain": row["program"],
                "Time_period": f"{int(row['period_start'])}-{int(row['period_end'])}",
                "ESP": float(row["esp_breeding"]),
                "log10_ESP": float(row["log10_esp_breeding"]),
                "Quality_score": int(row["data_quality"]),
                "Source": row["sources"],
            }
        )
    rows.extend(
        [
            {
                "Domain": "Breeding",
                "Subdomain": "US soybean (public programs)",
                "Time_period": "1960-2000",
                "ESP": 1.8e6,
                "log10_ESP": 6.3,
                "Quality_score": 3,
                "Source": "Specht & Williams 1984; Wilcox 2001; Rincker et al. 2014",
            },
            {
                "Domain": "Breeding",
                "Subdomain": "US dairy cattle",
                "Time_period": "1970-2000",
                "ESP": 3.6e4,
                "log10_ESP": 4.6,
                "Quality_score": 5,
                "Source": "VanRaden 2004; Shook 2006; USDA AIPL",
            },
        ]
    )
    return rows


def _rows_domain_c_speed_breeding() -> List[Dict[str, Any]]:
    data_path = ROOT / "data/domain_c_breeding/speed_breeding_data.json"
    data = json.loads(data_path.read_text())
    cimmyt_path = ROOT / "results/tables/tbl01_cimmyt_esp.csv"
    cimmyt = pd.read_csv(cimmyt_path)
    wheat_row = cimmyt[cimmyt["program"].str.contains("wheat", case=False)].iloc[0]
    baseline_esp = float(wheat_row["esp_breeding"])
    rows: List[Dict[str, Any]] = []
    for record in data.get("records", []):
        if record.get("crop") != "wheat":
            continue
        speedup = record.get("speedup_vs_baseline", {})
        speedup_mid = (float(speedup["min"]) + float(speedup["max"])) / 2.0
        esp = baseline_esp / speedup_mid
        source_bits = [record.get("source", "").strip(), record.get("doi", "").strip()]
        source = "; ".join([bit for bit in source_bits if bit])
        rows.append(
            {
                "Domain": "Breeding",
                "Subdomain": f"Speed breeding (wheat; {record['method']})",
                "Time_period": _extract_year(record.get("source", "")),
                "ESP": esp,
                "log10_ESP": _log10(esp),
                "Quality_score": 3,
                "Source": source,
            }
        )
    return rows


def _rows_domain_d_protein_engineering() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    d1_path = ROOT / "results/tables/tbl_d1_directed_evolution_esp.csv"
    d1 = pd.read_csv(d1_path)
    for _, row in d1.iterrows():
        source = row.get("doi")
        if pd.isna(source) or not str(source).strip():
            source = row.get("source_url", "")
        rows.append(
            {
                "Domain": "Protein engineering",
                "Subdomain": "Directed evolution",
                "Time_period": str(int(row["year"])),
                "ESP": float(row["esp"]),
                "log10_ESP": float(row["log10_esp"]),
                "Quality_score": int(row["data_quality_score"]),
                "Source": source,
            }
        )
    d2_path = ROOT / "results/tables/tbl_d2_ml_guided_esp.csv"
    d2 = pd.read_csv(d2_path)
    for _, row in d2.iterrows():
        source = row.get("doi")
        if pd.isna(source) or not str(source).strip():
            source = row.get("source_url", "")
        rows.append(
            {
                "Domain": "Protein engineering",
                "Subdomain": "ML-guided protein design",
                "Time_period": str(int(row["year"])),
                "ESP": float(row["esp"]),
                "log10_ESP": float(row["log10_esp"]),
                "Quality_score": int(row["data_quality_score"]),
                "Source": source,
            }
        )
    return rows


def _rows_domain_e_medicine() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    nnt_path = ROOT / "data/domain_e/processed/nnt_database.csv"
    nnt = pd.read_csv(nnt_path)
    for _, row in nnt.iterrows():
        esp = float(row["nnt"])
        rows.append(
            {
                "Domain": "Medicine",
                "Subdomain": "NNT (TheNNT)",
                "Time_period": str(int(row["year"])) if not pd.isna(row["year"]) else "unknown",
                "ESP": esp,
                "log10_ESP": _log10(esp),
                "Quality_score": int(row["data_quality_score"]),
                "Source": row.get("source_url", ""),
            }
        )
    fda_path = ROOT / "data/domain_e/processed/fda_pivotal_trials.csv"
    fda = pd.read_csv(fda_path)
    for _, row in fda.iterrows():
        esp = float(row["nnt"])
        rows.append(
            {
                "Domain": "Medicine",
                "Subdomain": "FDA pivotal trials",
                "Time_period": str(int(row["year"])) if not pd.isna(row["year"]) else "unknown",
                "ESP": esp,
                "log10_ESP": _log10(esp),
                "Quality_score": int(row["data_quality_score"]),
                "Source": row.get("source_url", ""),
            }
        )
    e4_path = ROOT / "data/domain_e/processed/e4_gene_therapy_cart_outcomes.csv"
    e4 = pd.read_csv(e4_path)
    for _, row in e4.iterrows():
        esp = float(row["esp"])
        rows.append(
            {
                "Domain": "Medicine",
                "Subdomain": "Gene therapy/CAR-T",
                "Time_period": str(int(row["year"])) if not pd.isna(row["year"]) else "unknown",
                "ESP": esp,
                "log10_ESP": _log10(esp),
                "Quality_score": int(row["data_quality_score"]),
                "Source": row.get("source_url", ""),
            }
        )
    return rows


def build_master_table() -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    rows.extend(_rows_domain_a_major_transitions())
    rows.extend(_rows_domain_a_mutation_rates())
    rows.extend(_rows_domain_b_domestication())
    rows.extend(_rows_domain_c_breeding())
    rows.extend(_rows_domain_c_speed_breeding())
    rows.extend(_rows_domain_d_protein_engineering())
    rows.extend(_rows_domain_e_medicine())
    df = pd.DataFrame(rows)
    df = _apply_pcs_assignments(df)
    df = df[
        [
            "Domain",
            "Subdomain",
            "Time_period",
            "ESP",
            "log10_ESP",
            "PCS_level",
            "PCS_score",
            "PCS_method",
            "PCS_notes",
            "ESP_normalized",
            "log10_ESP_normalized",
            "Quality_score",
            "Source",
        ]
    ]
    df = df.replace({np.nan: None})
    return df


def main() -> None:
    df = build_master_table()
    output_path = ROOT / "data/master_esp_table.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
