import json
import re
import urllib.request
from html import unescape
from pathlib import Path

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

    ordered_cols = [
        "intervention",
        "condition",
        "comparator",
        "outcome",
        "time_horizon",
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
