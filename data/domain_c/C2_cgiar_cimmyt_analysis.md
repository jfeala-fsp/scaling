# C2: CGIAR/CIMMYT Historical Analysis

**Task**: Calculate ESP for CGIAR/CIMMYT breeding programs using the ESP_breeding formula.
**Programs**: CIMMYT wheat and CIMMYT maize (1966-2000)
**Sources**: Evenson & Gollin 2003; Duvick 2005; CIMMYT annual reports
**Input file**: `data/domain_c/c2_cimmyt_inputs.csv`
**Output table**: `results/tables/tbl01_cimmyt_esp.csv`

---

## Formula

```
ESP_breeding = (Crosses × Progeny per cross × Selection cycles)
               ──────────────────────────────────────────────
               (Released varieties)
```

## Inputs and Assumptions

Inputs are period averages compiled in C1 (see `/Users/jfeala/gt/scaling/scaling/crew/louis/data/C1_breeding_programs.md`).
- Crosses per year and progeny per cross are averaged across eras for 1966-2000.
- Selection cycles are program-average counts per release.
- Released variety counts use CIMMYT program summaries (named varieties).

[REVIEW] Verify exact counts and definitions in Evenson & Gollin (2003) and Duvick (2005), as the inputs are aggregated program averages.

## Results (1966-2000)

- CIMMYT wheat: ESP_breeding = 552,500 (log10 = 5.74)
- CIMMYT maize: ESP_breeding = 97,143 (log10 = 4.99)

These values match the expected scientific breeding ESP range (10^3 to 10^6) in the research plan.

## Reproducibility

Run:
```
python3 src/analysis/c2_cimmyt_esp.py
```

This script reads the inputs and regenerates `results/tables/tbl01_cimmyt_esp.csv`.
