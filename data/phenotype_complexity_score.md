# Phenotype Complexity Score (PCS)

This rubric standardizes phenotypic complexity for ESP normalization.

## PCS Levels

| Level | Description | Example | PCS |
| --- | --- | --- | --- |
| 1 | Single quantitative trait shift | Yield increase, BP reduction | 1 |
| 2 | Single qualitative trait | Disease resistance, responder vs non-responder | 2 |
| 3 | Multiple coordinated traits | Domestication syndrome, stress-tolerance suite | 4 |
| 4 | Novel function (existing parts) | New enzyme activity from existing scaffold | 8 |
| 5 | Novel pathway | Engineered biosynthetic pathway | 16 |
| 6 | Novel body plan element | New tissue type | 32 |
| 7 | Major transition | Multicellularity, eukaryogenesis | 64 |

## Normalization

ESP is normalized as:

```
ESP_normalized = ESP / PCS
```

## Assignment Strategy

Assignments live in `data/pcs_assignments.csv` and are applied via
`src/analysis/master_esp_table.py`. The mapping uses domain and subdomain
patterns to set `PCS_level`, `PCS_score`, and `PCS_method`, with notes for any
assumptions.

## Alternative Information-Theoretic PCS

As a sensitivity check, PCS can be defined as:

```
PCS = log2(distinguishable phenotypic states)
```

This alternative is not yet implemented in the master table and should be
reported alongside the rubric-based PCS when used.
