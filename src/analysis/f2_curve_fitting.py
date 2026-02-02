"""
Fit candidate learning-curve models to ESP data and export comparison tables.

Outputs
-------
results/tables/tbl_f2_analysis_dataset.csv
results/tables/tbl_f2_model_fits.csv
results/tables/tbl_f2_piecewise_fits.csv
results/tables/tbl_f2_extrapolations.csv
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RNG = np.random.default_rng(20260202)


@dataclass
class FitResult:
    """Container for model fit results."""

    domain: str
    model: str
    n: int
    params: Dict[str, float]
    param_ci_low: Dict[str, float]
    param_ci_high: Dict[str, float]
    r2: Optional[float]
    aic: Optional[float]
    bic: Optional[float]
    notes: str


def _parse_number_range(text: str) -> Optional[Tuple[float, float]]:
    values = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", text)
    if not values:
        return None
    numbers = [float(v) for v in values]
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    return min(numbers), max(numbers)


def parse_time_period(time_period: str) -> Optional[float]:
    """
    Parse time period strings into a calendar year estimate.

    Notes
    -----
    - BP/kya/ga/ma are converted to calendar year using the 1950 BP convention.
    - Returns None for "modern"/"unknown" or unparseable strings.
    """

    if not isinstance(time_period, str):
        return None
    text = time_period.strip().lower()
    if not text or "unknown" in text or "modern" in text:
        return None
    if "ga" in text:
        value_range = _parse_number_range(text)
        if not value_range:
            return None
        mid_ga = sum(value_range) / 2.0
        return 1950.0 - mid_ga * 1e9
    if "ma" in text:
        value_range = _parse_number_range(text)
        if not value_range:
            return None
        mid_ma = sum(value_range) / 2.0
        return 1950.0 - mid_ma * 1e6
    if "kya" in text:
        value_range = _parse_number_range(text)
        if not value_range:
            return None
        mid_kya = sum(value_range) / 2.0
        return 1950.0 - mid_kya * 1e3
    if "bp" in text:
        value_range = _parse_number_range(text)
        if not value_range:
            return None
        mid_bp = sum(value_range) / 2.0
        return 1950.0 - mid_bp
    range_match = re.match(r"^\s*(\d{3,4})\s*-\s*(\d{3,4})\s*$", text)
    if range_match:
        start = float(range_match.group(1))
        end = float(range_match.group(2))
        return (start + end) / 2.0
    year_match = re.search(r"(19|20)\d{2}", text)
    if year_match:
        return float(year_match.group(0))
    return None


def _prepare_dataset() -> pd.DataFrame:
    path = ROOT / "data/master_esp_table.csv"
    if not path.exists():
        from src.analysis.master_esp_table import main as build_master

        build_master()
    df = pd.read_csv(path)
    df["year"] = df["Time_period"].apply(parse_time_period)
    df["log10_ESP"] = df["ESP"].apply(lambda value: float(np.log10(value)))
    df["time_note"] = np.where(df["year"].isna(), "unparsed", "ok")
    return df


def _linear_fit(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, float]:
    x_mean = float(np.mean(x))
    x_centered = x - x_mean
    slope, intercept_centered = np.polyfit(x_centered, y, 1)
    intercept = float(intercept_centered - slope * x_mean)
    y_pred = intercept + slope * x
    sse = float(np.sum((y - y_pred) ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - sse / sst if sst > 0 else math.nan
    return intercept, slope, sse, r2


def _bootstrap_linear_ci(x: np.ndarray, y: np.ndarray, n_boot: int = 500) -> Tuple[Dict[str, float], Dict[str, float]]:
    params = []
    for _ in range(n_boot):
        idx = RNG.integers(0, len(x), len(x))
        x_boot = x[idx]
        y_boot = y[idx]
        if np.std(x_boot) <= 0:
            continue
        try:
            intercept, slope, _, _ = _linear_fit(x_boot, y_boot)
        except np.linalg.LinAlgError:
            continue
        params.append([intercept, slope])
    if not params:
        nan_bounds = {"intercept": math.nan, "slope": math.nan}
        return nan_bounds, nan_bounds
    params = np.asarray(params)
    lower = np.percentile(params, 2.5, axis=0)
    upper = np.percentile(params, 97.5, axis=0)
    return {"intercept": float(lower[0]), "slope": float(lower[1])}, {
        "intercept": float(upper[0]),
        "slope": float(upper[1]),
    }


def _aic_bic_from_sse(sse: float, n: int, k: int) -> Tuple[float, float]:
    if sse <= 0 or n <= 0:
        return math.nan, math.nan
    aic = n * math.log(sse / n) + 2 * k
    bic = n * math.log(sse / n) + k * math.log(n)
    return aic, bic


def fit_exponential(domain: str, x: np.ndarray, y: np.ndarray) -> FitResult:
    intercept, slope, sse, r2 = _linear_fit(x, y)
    ci_low, ci_high = _bootstrap_linear_ci(x, y)
    aic, bic = _aic_bic_from_sse(sse, len(x), 2)
    params = {"intercept": intercept, "slope": slope}
    return FitResult(
        domain=domain,
        model="exponential",
        n=len(x),
        params=params,
        param_ci_low=ci_low,
        param_ci_high=ci_high,
        r2=r2,
        aic=aic,
        bic=bic,
        notes="log10_ESP ~ intercept + slope * year",
    )


def fit_wright(domain: str, x: np.ndarray, y: np.ndarray) -> FitResult:
    order = np.argsort(x)
    n = np.arange(1, len(x) + 1)
    x_w = np.log10(n.astype(float))
    y_w = y[order]
    intercept, slope, sse, r2 = _linear_fit(x_w, y_w)
    ci_low, ci_high = _bootstrap_linear_ci(x_w, y_w)
    aic, bic = _aic_bic_from_sse(sse, len(x_w), 2)
    params = {"intercept": intercept, "slope": slope}
    return FitResult(
        domain=domain,
        model="wright",
        n=len(x_w),
        params=params,
        param_ci_low=ci_low,
        param_ci_high=ci_high,
        r2=r2,
        aic=aic,
        bic=bic,
        notes="log10_ESP ~ intercept + slope * log10(cumulative_points)",
    )


def _logistic_weight(x: np.ndarray, k: float, x0: float) -> np.ndarray:
    exponent = np.clip(k * (x - x0), -700, 700)
    return 1.0 / (1.0 + np.exp(exponent))


def fit_logistic(domain: str, x: np.ndarray, y: np.ndarray) -> Optional[FitResult]:
    if np.any(y < 0):
        return None
    k_grid = np.logspace(-4, -1, 25)
    x0_grid = np.linspace(np.min(x), np.max(x), 25)
    best = None
    for k in k_grid:
        for x0 in x0_grid:
            w = _logistic_weight(x, k, x0)
            denom = float(np.sum(w * w))
            if denom == 0:
                continue
            l_max = float(np.sum(w * y) / denom)
            if l_max < 0:
                continue
            y_pred = l_max * w
            sse = float(np.sum((y - y_pred) ** 2))
            if best is None or sse < best["sse"]:
                best = {"sse": sse, "l_max": l_max, "k": float(k), "x0": float(x0)}
    if best is None:
        return None
    aic, bic = _aic_bic_from_sse(best["sse"], len(x), 3)
    return FitResult(
        domain=domain,
        model="logistic",
        n=len(x),
        params={"l_max": best["l_max"], "k": best["k"], "x0": best["x0"]},
        param_ci_low={},
        param_ci_high={},
        r2=None,
        aic=aic,
        bic=bic,
        notes="Grid-search logistic fit: log10_ESP = L / (1 + exp(k*(year - x0)))",
    )


def fit_piecewise(domain: str, x: np.ndarray, y: np.ndarray, min_points: int = 3) -> Optional[FitResult]:
    order = np.argsort(x)
    x_sorted = x[order]
    y_sorted = y[order]
    best = None
    for idx in range(min_points, len(x_sorted) - min_points + 1):
        x_left, y_left = x_sorted[:idx], y_sorted[:idx]
        x_right, y_right = x_sorted[idx:], y_sorted[idx:]
        if np.std(x_left) <= 0 or np.std(x_right) <= 0:
            continue
        try:
            left_intercept, left_slope, left_sse, _ = _linear_fit(x_left, y_left)
            right_intercept, right_slope, right_sse, _ = _linear_fit(x_right, y_right)
        except np.linalg.LinAlgError:
            continue
        sse = left_sse + right_sse
        aic, bic = _aic_bic_from_sse(sse, len(x_sorted), 4)
        if best is None or aic < best["aic"]:
            best = {
                "aic": aic,
                "bic": bic,
                "breakpoint": float(x_sorted[idx]),
                "left_intercept": left_intercept,
                "left_slope": left_slope,
                "right_intercept": right_intercept,
                "right_slope": right_slope,
                "sse": sse,
            }
    if best is None:
        return None
    return FitResult(
        domain=domain,
        model="piecewise_exponential",
        n=len(x_sorted),
        params={
            "breakpoint": best["breakpoint"],
            "left_intercept": best["left_intercept"],
            "left_slope": best["left_slope"],
            "right_intercept": best["right_intercept"],
            "right_slope": best["right_slope"],
        },
        param_ci_low={},
        param_ci_high={},
        r2=None,
        aic=best["aic"],
        bic=best["bic"],
        notes="Two-segment log10_ESP linear fit with breakpoint search.",
    )


def _fit_domain_models(domain: str, df: pd.DataFrame) -> List[FitResult]:
    fits: List[FitResult] = []
    x = df["year"].to_numpy(dtype=float)
    y = df["log10_ESP"].to_numpy(dtype=float)
    if len(x) < 5 or np.std(x) <= 0:
        return fits
    fits.append(fit_exponential(domain, x, y))
    fits.append(fit_wright(domain, x, y))
    piecewise = fit_piecewise(domain, x, y)
    if piecewise:
        fits.append(piecewise)
    logistic = fit_logistic(domain, x, y)
    if logistic:
        fits.append(logistic)
    return fits


def _fit_extrapolations(df: pd.DataFrame, fits: Iterable[FitResult]) -> pd.DataFrame:
    rows = []
    for fit in fits:
        if fit.model != "exponential":
            continue
        slope = fit.params["slope"]
        intercept = fit.params["intercept"]
        if slope == 0:
            continue
        for target_log10 in (1.0, 0.0):
            year = (target_log10 - intercept) / slope
            rows.append(
                {
                    "domain": fit.domain,
                    "model": fit.model,
                    "target_esp": 10 ** target_log10,
                    "target_log10_esp": target_log10,
                    "projected_year": year,
                }
            )
    return pd.DataFrame(rows)


def _half_life_years(fit: FitResult) -> Optional[float]:
    if fit.model != "exponential":
        return None
    slope = fit.params["slope"]
    if slope == 0:
        return None
    return float(math.log10(0.5) / slope)


def _results_to_frame(fits: Iterable[FitResult]) -> pd.DataFrame:
    rows = []
    for fit in fits:
        row = {
            "domain": fit.domain,
            "model": fit.model,
            "n": fit.n,
            "r2": fit.r2,
            "aic": fit.aic,
            "bic": fit.bic,
            "notes": fit.notes,
            "half_life_years": _half_life_years(fit),
        }
        for key, value in fit.params.items():
            row[f"param_{key}"] = value
        for key, value in fit.param_ci_low.items():
            row[f"param_ci_low_{key}"] = value
        for key, value in fit.param_ci_high.items():
            row[f"param_ci_high_{key}"] = value
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    df = _prepare_dataset()
    analysis_df = df[df["year"].notna()].copy()
    analysis_df["year"] = analysis_df["year"].astype(float)
    analysis_df = analysis_df.sort_values(["Domain", "year"]).reset_index(drop=True)
    output_dir = ROOT / "results/tables"
    output_dir.mkdir(parents=True, exist_ok=True)
    analysis_df.to_csv(output_dir / "tbl_f2_analysis_dataset.csv", index=False)

    fits = []
    for domain, group in analysis_df.groupby("Domain"):
        fits.extend(_fit_domain_models(domain, group))

    fits_df = _results_to_frame(fits)
    fits_df.to_csv(output_dir / "tbl_f2_model_fits.csv", index=False)

    extrap_df = _fit_extrapolations(analysis_df, fits)
    extrap_df.to_csv(output_dir / "tbl_f2_extrapolations.csv", index=False)

    piecewise_rows = []
    for fit in fits:
        if fit.model != "piecewise_exponential":
            continue
        piecewise_rows.append(
            {
                "domain": fit.domain,
                "breakpoint": fit.params["breakpoint"],
                "left_intercept": fit.params["left_intercept"],
                "left_slope": fit.params["left_slope"],
                "right_intercept": fit.params["right_intercept"],
                "right_slope": fit.params["right_slope"],
                "aic": fit.aic,
                "bic": fit.bic,
            }
        )
    pd.DataFrame(piecewise_rows).to_csv(output_dir / "tbl_f2_piecewise_fits.csv", index=False)


if __name__ == "__main__":
    main()
