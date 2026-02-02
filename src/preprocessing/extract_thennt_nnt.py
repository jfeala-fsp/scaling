import json
import re
import urllib.request
from html import unescape
from pathlib import Path
from typing import Optional

import pandas as pd


def fetch_html(url: str) -> str:
    """Fetch HTML content with a standard browser user-agent."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_page_meta(slug: str) -> dict:
    """Fetch TheNNT page metadata from the WordPress JSON API."""
    url = f"https://thennt.com/wp-json/wp/v2/nnt-review?slug={slug}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        data = json.load(response)
    if not data:
        return {}
    return data[0]


def extract_rows(html: str, label: str) -> list[dict]:
    """Extract NNT rows from the Benefits (A) or Harms (B) section."""
    section_match = re.search(
        rf'<article class="ben_har ben_har_{label} .*?>.*?</article>',
        html,
        flags=re.S,
    )
    if not section_match:
        return []
    section = section_match.group(0)
    container_match = re.search(
        r'<div class="info__container">(.*?)</div>\s*<!-- create info container but with %',
        section,
        flags=re.S,
    )
    if not container_match:
        return []
    container = container_match.group(1)
    rows = re.findall(
        r'<div class="row__container">\s*<div>(.*?)</div>\s*<div>(.*?)</div>\s*</div>',
        container,
        flags=re.S,
    )
    extracted = []
    for nnt_raw, text_raw in rows:
        nnt_text = unescape(re.sub(r"<[^>]+>", "", nnt_raw)).strip()
        outcome_text = normalize_ascii(unescape(re.sub(r"<[^>]+>", "", text_raw)).strip())
        if nnt_text.isdigit():
            extracted.append(
                {
                    "nnt_value": int(nnt_text),
                    "outcome_text": outcome_text,
                }
            )
    return extracted


def normalize_ascii(text: str) -> str:
    """Normalize common non-ASCII punctuation for consistent CSV output."""
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2009": " ",
        "\u00a0": " ",
    }
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    return text


def duration_to_months(value: float, unit: str) -> float:
    """Convert a duration to months using a 30-day month convention."""
    unit = unit.lower()
    if unit.startswith("day"):
        return value / 30
    if unit.startswith("week"):
        return value * 7 / 30
    if unit in {"mo", "mos"} or unit.startswith("month"):
        return value
    if unit in {"yr", "yrs"} or unit.startswith("year"):
        return value * 12
    if unit in {"h", "hr", "hrs"} or unit.startswith("hour"):
        return value / 24 / 30
    return value


def parse_follow_up_months(text: str) -> Optional[float]:
    """Extract follow-up duration from text and return months."""
    if text is None:
        return None
    if not isinstance(text, str):
        return None
    if not text:
        return None
    cleaned = normalize_ascii(text).lower()
    range_pattern = re.compile(
        r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*"
        r"(day|days|week|weeks|month|months|year|years|yr|yrs|hour|hours|hr|hrs|h|mo|mos)\b"
    )
    single_pattern = re.compile(
        r"(\d+(?:\.\d+)?)\s*"
        r"(day|days|week|weeks|month|months|year|years|yr|yrs|hour|hours|hr|hrs|h|mo|mos)\b"
    )
    candidates = []
    for match in range_pattern.finditer(cleaned):
        upper = float(match.group(2))
        unit = match.group(3)
        candidates.append(duration_to_months(upper, unit))
    for match in single_pattern.finditer(cleaned):
        value = float(match.group(1))
        unit = match.group(2)
        candidates.append(duration_to_months(value, unit))
    if not candidates:
        return None
    return max(candidates)


def bucket_follow_up(months: Optional[float]) -> str:
    """Bucket follow-up duration into standard time horizons."""
    if months is None:
        return "missing"
    if months <= 1:
        return "1mo"
    if months <= 6:
        return "6mo"
    if months <= 12:
        return "1yr"
    if months <= 60:
        return "5yr"
    return "over_5yr"


def main() -> None:
    """Extract NNT data from TheNNT pages listed in the raw pages CSV."""
    root = Path(__file__).resolve().parents[2]
    pages_path = root / "data" / "domain_e" / "raw" / "thennt_pages.csv"
    raw_output_path = root / "data" / "domain_e" / "raw" / "thennt_nnt_extracted.csv"
    processed_output_path = root / "data" / "domain_e" / "processed" / "nnt_database.csv"

    pages_df = pd.read_csv(pages_path)
    rows = []

    for _, row in pages_df.iterrows():
        slug = row["page_slug"]
        page_url = row["url"]
        html = fetch_html(page_url)
        meta = fetch_page_meta(slug)
        page_title = normalize_ascii(meta.get("title", {}).get("rendered", "") or "")
        year = ""
        if meta.get("date"):
            year = meta["date"].split("-")[0]

        for nnt_type, label in (("benefit", "A"), ("harm", "B")):
            for entry in extract_rows(html, label):
                follow_up_months = parse_follow_up_months(row["time_horizon"])
                follow_up_source = "time_horizon" if follow_up_months is not None else ""
                if follow_up_months is None:
                    follow_up_months = parse_follow_up_months(entry["outcome_text"])
                    if follow_up_months is not None:
                        follow_up_source = "outcome_text"
                follow_up_bucket = bucket_follow_up(follow_up_months)
                follow_up_status = "missing" if follow_up_months is None else "clear"
                rows.append(
                    {
                        "page_slug": slug,
                        "page_title": page_title,
                        "page_url": page_url,
                        "year": year,
                        "nnt_type": nnt_type,
                        "nnt_value": entry["nnt_value"],
                        "outcome_text": entry["outcome_text"],
                        "intervention": row["intervention"],
                        "condition": row["condition"],
                        "comparator": row["comparator"],
                        "therapeutic_area": row["therapeutic_area"],
                        "time_horizon": row["time_horizon"],
                        "follow_up_months": follow_up_months,
                        "follow_up_bucket": follow_up_bucket,
                        "follow_up_status": follow_up_status,
                        "follow_up_source": follow_up_source,
                        "notes": row["notes"],
                    }
                )

    raw_df = pd.DataFrame(rows)
    raw_df.to_csv(raw_output_path, index=False)

    processed_df = raw_df.rename(
        columns={
            "outcome_text": "outcome",
            "nnt_value": "nnt",
        }
    )
    processed_df["nnt_ci"] = ""
    processed_df["source"] = "TheNNT"
    processed_df["source_url"] = processed_df["page_url"]
    processed_df["data_quality_score"] = 3
    processed_df["follow_up_months"] = pd.to_numeric(
        processed_df["follow_up_months"], errors="coerce"
    ).round(2)

    ordered_cols = [
        "intervention",
        "condition",
        "comparator",
        "outcome",
        "time_horizon",
        "follow_up_months",
        "follow_up_bucket",
        "follow_up_status",
        "follow_up_source",
        "nnt",
        "nnt_ci",
        "nnt_type",
        "therapeutic_area",
        "year",
        "source",
        "source_url",
        "data_quality_score",
        "notes",
        "page_slug",
        "page_title",
        "page_url",
    ]
    processed_df = processed_df[ordered_cols]
    processed_df.to_csv(processed_output_path, index=False)


if __name__ == "__main__":
    main()
