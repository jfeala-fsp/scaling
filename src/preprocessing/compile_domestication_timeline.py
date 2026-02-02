"""Compile domestication timeline data from JSON into a CSV table."""
from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "domain_b" / "domestication_data.json"
OUT_DIR = PROJECT_ROOT / "data" / "domain_b" / "processed"
OUTPUT_PATH = OUT_DIR / "domestication_timeline_compilation.csv"


TRAIT_LABELS = {
    "non_shattering_rachis": "Non-shattering",
    "larger_grain_size": "larger grain",
    "free_threshing": "free-threshing",
    "reduced_seed_dormancy": "reduced dormancy",
    "single_stalk_tb1": "tb1 (single stalk)",
    "naked_kernels_tga1": "tga1 (naked kernels)",
    "non_shattering": "non-shattering",
    "kernel_row_number": "kernel rows",
    "larger_ear_size": "larger ear size",
    "reduced_fear_humans": "Reduced fear",
    "floppy_ears": "floppy ears",
    "curly_tails": "curly tails",
    "piebald_spotting": "piebald",
    "size_variation": "size",
    "coat_color_diversity": "coat color diversity",
    "body_size_reduction": "Body size reduction",
    "docility": "docility",
    "polled_trait": "polled",
    "milk_production": "milk yield",
}


def _format_number(value: Any) -> str:
    """Format numbers and ranges into consistent strings."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    return str(value)


def _format_range(values: Any) -> str:
    """Format a two-element list as a range string."""
    if not values:
        return ""
    if isinstance(values, (list, tuple)) and len(values) == 2:
        return f"{_format_number(values[0])}-{_format_number(values[1])}"
    return _format_number(values)


def _format_population(population: dict[str, Any]) -> tuple[str, str]:
    """Format founder population estimates and ranges."""
    founder_ne = ""
    founder_range = ""
    if "effective_ne_wild" in population:
        wild = _format_number(population.get("effective_ne_wild"))
        dom = population.get("effective_ne_domesticated")
        founder_ne = f"{wild} (wild)"
        if dom is not None:
            founder_ne = f"{founder_ne}; {_format_number(dom)} (dom)"
        wild_ci = _format_range(population.get("effective_ne_wild_ci"))
        dom_ci = _format_range(population.get("effective_ne_domesticated_ci"))
        founder_range = f"{wild_ci} (wild)" if wild_ci else ""
        if dom_ci:
            founder_range = f"{founder_range}; {dom_ci} (dom)" if founder_range else f"{dom_ci} (dom)"
    elif "bottleneck_minimum_ne" in population:
        bottleneck = _format_number(population.get("bottleneck_minimum_ne"))
        avg = _format_number(population.get("average_ne_during_domestication"))
        parts = [f"{bottleneck} (bottleneck)"] if bottleneck else []
        if avg:
            parts.append(f"{avg} (avg)")
        founder_ne = "; ".join(parts)
    elif "founder_ne" in population:
        founder_ne = _format_number(population.get("founder_ne"))
        founder_range = _format_range(population.get("founder_ne_range"))
    elif "taurine_founder_females" in population:
        females = _format_number(population.get("taurine_founder_females"))
        total = _format_number(population.get("taurine_founder_total"))
        if total:
            founder_ne = f"{females} founder females (~{total} total)"
        else:
            founder_ne = females
    return founder_ne, founder_range


def _format_population_under_selection(population: dict[str, Any]) -> str:
    """Format selection population estimates."""
    if "estimate_low" in population:
        low = _format_number(population.get("estimate_low"))
        high = _format_number(population.get("estimate_high"))
        return f"{low}-{high}" if low and high else low or high
    if "estimate" in population:
        return _format_number(population.get("estimate"))
    if "geometric_mean_estimate" in population:
        return f"~{_format_number(population.get('geometric_mean_estimate'))} (geom mean)"
    parts = []
    for key, label in [
        ("initial_domestication", "initial"),
        ("early_diversification", "early"),
        ("breed_formation", "breed era"),
        ("initial", "initial"),
        ("after_expansion", "after expansion"),
    ]:
        if key in population:
            parts.append(f"{_format_number(population.get(key))} ({label})")
    return "; ".join(parts)


def _trait_fixation_notes(traits: dict[str, Any]) -> str:
    """Format trait fixation notes into a compact summary string."""
    notes = []
    for trait_key, entry in traits.items():
        label = TRAIT_LABELS.get(trait_key, trait_key.replace("_", " "))
        generations = (
            entry.get("generations")
            or entry.get("generations_to_fix")
            or entry.get("major_gains_generations")
        )
        if generations is None:
            continue
        gen_text = _format_number(generations)
        if "gen" not in gen_text and "generation" not in gen_text:
            gen_text = f"{gen_text} gen"
        notes.append(f"{label}: {gen_text}")
    return "; ".join(notes)


def _format_references(references: list[dict[str, Any]]) -> str:
    """Format key references as 'Author year' entries."""
    formatted = []
    for ref in references:
        authors = ref.get("authors", "")
        year = ref.get("year", "")
        label = f"{authors} {year}".strip()
        if label:
            formatted.append(label)
    return "; ".join(formatted)


def compile_domestication_timeline() -> None:
    """Compile domestication timeline data into a CSV table."""
    with INPUT_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)
    species_data = data.get("species", {})

    rows = []
    for species_key, values in species_data.items():
        timeline = values.get("domestication_timeline", {})
        founder_ne, founder_range = _format_population(values.get("founder_population", {}))
        population_selection = _format_population_under_selection(values.get("population_under_selection", {}))
        traits = _trait_fixation_notes(values.get("trait_fixation", {}))
        references = _format_references(values.get("key_references", []))

        rows.append(
            {
                "species": species_key.capitalize(),
                "scientific_name": values.get("scientific_name", ""),
                "domestication_start_bp": _format_number(timeline.get("start_date_bp")),
                "domestication_start_bce": _format_number(timeline.get("start_date_bce")),
                "location": timeline.get("location", ""),
                "duration_years": _format_number(timeline.get("duration_years")),
                "generation_time_years": _format_number(values.get("generation_time_years")),
                "founder_ne": founder_ne,
                "founder_ne_range": founder_range,
                "population_under_selection": population_selection,
                "trait_fixation_notes": traits,
                "key_references": references,
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df = df[
        [
            "species",
            "scientific_name",
            "domestication_start_bp",
            "domestication_start_bce",
            "location",
            "duration_years",
            "generation_time_years",
            "founder_ne",
            "founder_ne_range",
            "population_under_selection",
            "trait_fixation_notes",
            "key_references",
        ]
    ]
    df.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    compile_domestication_timeline()
