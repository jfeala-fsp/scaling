"""
Generate publication-ready figures for the ESP learning-curve paper.

Outputs
-------
results/figures/fig01_esp_framework_diagram.(png|pdf)
results/figures/fig02_evolution_esp_vs_time.(png|pdf)
results/figures/fig03_domestication_breeding_esp_vs_time.(png|pdf)
results/figures/fig04_molecular_biotech_esp_vs_time.(png|pdf)
results/figures/fig05_medicine_esp_vs_time.(png|pdf)
results/figures/fig06_unified_curve_overlay.(png|pdf)
results/figures/fig07_doubling_time_analysis.(png|pdf)
results/figures/fig08_projection_to_esp1.(png|pdf)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
PRESENT_YEAR = 2026


def _extract_numbers(text: str) -> Iterable[float]:
    return [float(value) for value in re.findall(r"\d+\.\d+|\d+", text)]


def _parse_range(values: Iterable[float]) -> Optional[Tuple[float, float]]:
    vals = list(values)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0], vals[0]
    return vals[0], vals[1]


def _parse_time_period(value: str) -> Dict[str, Optional[float]]:
    if not isinstance(value, str):
        return {"year_ce": None, "years_bp": None}
    text = value.strip()
    if not text or text.lower() in {"unknown", "modern"}:
        return {"year_ce": None, "years_bp": None}

    cleaned = text.replace("~", "").replace("ca.", "").strip()

    year_range = re.search(r"(\d{4})\s*-\s*(\d{4})", cleaned)
    if year_range:
        start = float(year_range.group(1))
        end = float(year_range.group(2))
        year = (start + end) / 2.0
        return {"year_ce": year, "years_bp": PRESENT_YEAR - year}

    if re.fullmatch(r"\d{4}", cleaned):
        year = float(cleaned)
        return {"year_ce": year, "years_bp": PRESENT_YEAR - year}

    if "BP" in cleaned:
        numbers = _extract_numbers(cleaned)
        parsed = _parse_range(numbers)
        if parsed:
            years_bp = sum(parsed) / 2.0
            return {"year_ce": PRESENT_YEAR - years_bp, "years_bp": years_bp}

    if "kya" in cleaned.lower():
        numbers = _extract_numbers(cleaned)
        parsed = _parse_range(numbers)
        if parsed:
            years_bp = (sum(parsed) / 2.0) * 1_000.0
            return {"year_ce": PRESENT_YEAR - years_bp, "years_bp": years_bp}

    if "Ma" in cleaned:
        numbers = _extract_numbers(cleaned)
        parsed = _parse_range(numbers)
        if parsed:
            years_bp = (sum(parsed) / 2.0) * 1_000_000.0
            return {"year_ce": PRESENT_YEAR - years_bp, "years_bp": years_bp}

    if "Ga" in cleaned:
        numbers = _extract_numbers(cleaned)
        parsed = _parse_range(numbers)
        if parsed:
            years_bp = (sum(parsed) / 2.0) * 1_000_000_000.0
            return {"year_ce": PRESENT_YEAR - years_bp, "years_bp": years_bp}

    return {"year_ce": None, "years_bp": None}


def _load_master_table() -> pd.DataFrame:
    path = ROOT / "data/master_esp_table.csv"
    if not path.exists():
        from src.analysis.master_esp_table import build_master_table

        df = build_master_table()
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
    return pd.read_csv(path)


def _add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    parsed = df["Time_period"].apply(_parse_time_period)
    df = df.copy()
    df["year_ce"] = parsed.apply(lambda record: record["year_ce"])
    df["years_bp"] = parsed.apply(lambda record: record["years_bp"])
    return df


def _save_figure(fig: plt.Figure, name: str) -> None:
    output_dir = ROOT / "results/figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"{name}.png"
    pdf_path = output_dir / f"{name}.pdf"
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)


def _figure_framework_diagram() -> None:
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")

    boxes = [
        (0.05, 0.55, "Molecular", "Variants tested"),
        (0.37, 0.55, "Organismal", "Individuals screened"),
        (0.69, 0.55, "Clinical", "Patients treated"),
    ]
    for x, y, title, subtitle in boxes:
        patch = FancyBboxPatch(
            (x, y),
            0.26,
            0.3,
            boxstyle="round,pad=0.02",
            linewidth=1.2,
            facecolor="#DDECF7",
            edgecolor="#2B4C6F",
        )
        ax.add_patch(patch)
        ax.text(x + 0.13, y + 0.2, title, ha="center", va="center", fontsize=11)
        ax.text(x + 0.13, y + 0.1, subtitle, ha="center", va="center", fontsize=9)

    ax.annotate(
        "ESP = experiments / successes",
        xy=(0.5, 0.42),
        xytext=(0.5, 0.32),
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-|>", "lw": 1.2},
        fontsize=11,
    )

    ax.text(
        0.5,
        0.15,
        "Learning curve across domains",
        ha="center",
        va="center",
        fontsize=12,
        weight="bold",
    )
    _save_figure(fig, "fig01_esp_framework_diagram")


def _figure_evolution(df: pd.DataFrame) -> None:
    subset = df[(df["Domain"] == "Evolution") & df["years_bp"].notna()]
    if subset.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(
        data=subset,
        x="years_bp",
        y="log10_ESP",
        s=60,
        color="#2A9D8F",
        ax=ax,
    )
    ax.set_xscale("log")
    ax.set_xlabel("Years before present (log scale)")
    ax.set_ylabel("log10(ESP)")
    ax.set_title("Evolution: ESP vs. time")
    _save_figure(fig, "fig02_evolution_esp_vs_time")


def _figure_domestication_breeding(df: pd.DataFrame) -> None:
    subset = df[df["Domain"].isin(["Domestication", "Breeding"]) & df["year_ce"].notna()]
    if subset.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(
        data=subset,
        x="year_ce",
        y="log10_ESP",
        hue="Domain",
        palette="colorblind",
        s=60,
        ax=ax,
    )
    ax.set_xlabel("Year (CE; negative = BCE)")
    ax.set_ylabel("log10(ESP)")
    ax.set_title("Domestication and breeding: ESP vs. time")
    ax.legend(title="Domain", frameon=False)
    _save_figure(fig, "fig03_domestication_breeding_esp_vs_time")


def _figure_molecular(df: pd.DataFrame) -> None:
    subset = df[(df["Domain"] == "Protein engineering") & df["year_ce"].notna()]
    if subset.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(
        data=subset,
        x="year_ce",
        y="log10_ESP",
        hue="Subdomain",
        palette="colorblind",
        s=60,
        ax=ax,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("log10(ESP)")
    ax.set_title("Molecular biotechnology: ESP vs. time")
    ax.legend(title="Subdomain", frameon=False)
    _save_figure(fig, "fig04_molecular_biotech_esp_vs_time")


def _figure_medicine(df: pd.DataFrame) -> None:
    subset = df[(df["Domain"] == "Medicine") & df["year_ce"].notna()]
    if subset.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(
        data=subset,
        x="year_ce",
        y="log10_ESP",
        hue="Subdomain",
        palette="colorblind",
        s=60,
        ax=ax,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("log10(ESP)")
    ax.set_title("Clinical medicine: ESP vs. time")
    ax.legend(title="Subdomain", frameon=False)
    _save_figure(fig, "fig05_medicine_esp_vs_time")


def _figure_unified_curve(df: pd.DataFrame) -> None:
    subset = df[df["years_bp"].notna()]
    if subset.empty:
        return
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    sns.scatterplot(
        data=subset,
        x="years_bp",
        y="log10_ESP",
        hue="Domain",
        palette="colorblind",
        s=55,
        ax=ax,
    )
    ax.set_xscale("log")
    ax.set_xlabel("Years before present (log scale)")
    ax.set_ylabel("log10(ESP)")
    ax.set_title("Unified ESP learning curve")
    ax.legend(title="Domain", frameon=False)
    _save_figure(fig, "fig06_unified_curve_overlay")


def _fit_domain_trend(df: pd.DataFrame, domain: str) -> Optional[Tuple[float, float]]:
    subset = df[(df["Domain"] == domain) & df["year_ce"].notna()]
    if len(subset) < 3:
        return None
    x = subset["year_ce"].to_numpy(dtype=float)
    y = subset["log10_ESP"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def _figure_doubling_time(df: pd.DataFrame) -> None:
    domains = sorted(df["Domain"].dropna().unique())
    records = []
    for domain in domains:
        trend = _fit_domain_trend(df, domain)
        if not trend:
            continue
        slope, _ = trend
        if slope >= 0:
            continue
        halving_years = np.log10(0.5) / slope
        if halving_years <= 0:
            continue
        records.append({"Domain": domain, "Halving_time_years": halving_years})
    if not records:
        return
    plot_df = pd.DataFrame(records).sort_values("Halving_time_years")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(
        data=plot_df,
        x="Halving_time_years",
        y="Domain",
        hue="Domain",
        palette="colorblind",
        legend=False,
        ax=ax,
    )
    ax.set_xlabel("Years to halve ESP")
    ax.set_ylabel("Domain")
    ax.set_title("ESP improvement rates by domain")
    _save_figure(fig, "fig07_doubling_time_analysis")


def _figure_projection(df: pd.DataFrame) -> None:
    domains = sorted(df["Domain"].dropna().unique())
    records = []
    for domain in domains:
        trend = _fit_domain_trend(df, domain)
        if not trend:
            continue
        slope, intercept = trend
        if slope >= 0:
            continue
        year_esp1 = -intercept / slope
        records.append({"Domain": domain, "Year_ESP1": year_esp1})
    if not records:
        return
    plot_df = pd.DataFrame(records).sort_values("Year_ESP1")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(
        data=plot_df,
        x="Year_ESP1",
        y="Domain",
        hue="Domain",
        palette="colorblind",
        legend=False,
        ax=ax,
    )
    ax.axvline(PRESENT_YEAR, color="#555555", linestyle="--", linewidth=1)
    ax.set_xlabel("Projected year for ESP = 1 (linear trend)")
    ax.set_ylabel("Domain")
    ax.set_title("Projected convergence to ESP = 1")
    _save_figure(fig, "fig08_projection_to_esp1")


def main() -> None:
    sns.set_theme(style="whitegrid", font_scale=1.0)
    df = _add_time_columns(_load_master_table())
    _figure_framework_diagram()
    _figure_evolution(df)
    _figure_domestication_breeding(df)
    _figure_molecular(df)
    _figure_medicine(df)
    _figure_unified_curve(df)
    _figure_doubling_time(df)
    _figure_projection(df)


if __name__ == "__main__":
    main()
