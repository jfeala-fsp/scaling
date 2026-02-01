# Domain D: ML-guided protein design outcomes (2020-present)

## Scope
This folder tracks ML-guided protein design success rates and derived ESP values.
Entries focus on experimental validation outcomes where the number of designs tested
and the number of successful designs are explicitly reported.

## Files
- ml_guided_design_outcomes.csv: structured table of ML-guided design outcomes

## Extraction notes
- MLD-2025-01 (PMC12704715, PNAS 2025)
  - "A total of 25 designs ... were manually selected" and "9 of these designs could be isolated by SEC".
  - "all 9 designs isolated by SEC bound to L9".
  - ESP uses 25 tested designs and 9 successes (binding by ELISA after SEC).

- MLD-2025-02 and MLD-2025-03 (PMC12626006, PNAS 2025)
  - "select 88 designs for experimental characterization" and reported "6/88 designs (7%)" with
    accurate assembly (C-alpha RMSD 1.6 to 2.2 A).
  - "filtered approximately 2,200 designs ... selected 13 for experimental characterization";
    "11 secreted ... and bound monoclonal antibodies (mAbs)".
  - ESP uses experimentally characterized designs as the denominator.

## Caveats
- Several pipelines involve in silico filtering before experimental characterization; the CSV
  uses the number of experimentally characterized designs as the ESP denominator.
- Additional 2020-2024 ML-guided design outcomes should be added as sources are located.

