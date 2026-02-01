# C3: Speed Breeding Literature Review

## Deliverable for Task scaling-1da
**Status**: Complete
**Date**: February 2026

---

## 1. Annotated Bibliography (Key Papers)

1. **Watson, A. et al. (2018)** "Speed breeding is a powerful tool to accelerate crop research and breeding" *Nature Plants* 4:23-29. https://doi.org/10.1038/s41477-017-0083-8
   - Core speed breeding protocol (extended photoperiod and controlled environment).
   - Quantitative throughput: up to 6 generations per year for wheat, barley, chickpea, pea; 4 for canola, vs 2-3 under normal glasshouse conditions.

2. **Ghosh, S. et al. (2018)** "Speed breeding in growth chambers and glasshouses for crop breeding and model plant research" *Nature Protocols* 13:2944-2963. https://doi.org/10.1038/s41596-018-0072-z
   - Detailed protocol guidance (light regime, temperature, plant density, SSD steps).
   - Emphasizes reproducible generation cycling for multiple crop species.

3. **Hickey, L. T. et al. (2019)** "Breeding crops to feed 10 billion" *Nature Biotechnology* 37:744-754. https://doi.org/10.1038/s41587-019-0152-9
   - Positions speed breeding as a platform that amplifies genomic selection, editing, and phenotyping.
   - Conceptual link: cycle-time compression increases realized genetic gain per unit time.

4. **Zheng, Z. et al. (2013)** "A procedure allowing up to eight generations of wheat and nine generations of barley per annum" *Euphytica* 191:311-316. https://doi.org/10.1007/s10681-013-0909-z
   - Embryo culture plus environmental controls achieve 8 (wheat) and 9 (barley) generations per year.
   - Demonstrates the upper bound of cycle compression with intensive protocols.

5. **Yao, Y. et al. (2016)** "How to advance up to seven generations of canola (Brassica napus L.) per annum for the production of pure line populations?" *Euphytica* 209:113-119. https://doi.org/10.1007/s10681-016-1643-0
   - Compares "all soil" vs embryo culture plus soil methods.
   - Reports 5 generations per year (all soil) and 7 (embryo culture plus soil).

6. **O'Connor, D. J. et al. (2013)** "Development and application of speed breeding technologies in a commercial peanut breeding program" *Peanut Science* 40:107-114.
   - Real-world program demonstrating deployment and scaling of speed breeding in a commercial crop.

---

## 2. Quantitative Cycle-Time Compression

**Baseline assumption**: normal glasshouse conditions yield ~2-3 generations per year (Watson et al. 2018). Speedup factors below are calculated against this baseline.

| Crop | Method/setting | Speed gens/year | Baseline gens/year | Cycle length (days/gen) | Speedup vs baseline | Source |
|---|---|---:|---:|---:|---:|---|
| Wheat | Controlled-environment speed breeding | 6 | 2-3 | 60.8 | 2.0-3.0x | Watson et al. 2018 |
| Wheat | Embryo culture + optimized environment | 8 | 2-3 | 45.6 | 2.7-4.0x | Zheng et al. 2013 |
| Barley | Controlled-environment speed breeding | 6 | 2-3 | 60.8 | 2.0-3.0x | Watson et al. 2018 |
| Barley | Embryo culture + optimized environment | 9 | 2-3 | 40.6 | 3.0-4.5x | Zheng et al. 2013 |
| Chickpea | Controlled-environment speed breeding | 6 | 2-3 | 60.8 | 2.0-3.0x | Watson et al. 2018 |
| Pea | Controlled-environment speed breeding | 6 | 2-3 | 60.8 | 2.0-3.0x | Watson et al. 2018 |
| Canola | Controlled-environment speed breeding | 4 | 2-3 | 91.3 | 1.3-2.0x | Watson et al. 2018 |
| Canola | Embryo culture + soil (single pod) | 7 | 2-3 | 52.1 | 2.3-3.5x | Yao et al. 2016 |

**Note**: If crop-specific baseline cycles differ from the generic 2-3 generations/year, speedup factors should be recalculated.

---

## 3. Impact on ESP (Time-Normalized)

Speed breeding primarily compresses **calendar time**, not the number of selection cycles required for a phenotype. The ESP definition uses cycles, so the **per-cycle ESP** is unchanged, but the **time to reach the same ESP** drops in proportion to the cycle-rate increase.

Let:
- `ESP = (crosses * progeny * cycles) / released varieties`
- `cycles_per_year = c`

A time-normalized throughput metric can be written as:
```
ESP_per_year = (crosses * progeny * cycles_per_year) / released varieties
```
Thus, throughput scales linearly with `c`.

**Implication**: increasing from 2-3 to 6 generations per year (wheat/barley/chickpea/pea) yields a 2.0-3.0x increase in time-normalized ESP throughput. The most aggressive protocols (8-9 generations/year) raise throughput by 2.7-4.5x.

---

## 4. Key Findings and Notes

1. Speed breeding reliably delivers 2-3x cycle-time compression for several staple crops (Watson et al. 2018).
2. Embryo culture plus environmental control can push cereals to 8-9 generations/year (Zheng et al. 2013).
3. Canola demonstrates both moderate gains (4 gen/year) and high gains (7 gen/year) depending on protocol intensity (Watson et al. 2018; Yao et al. 2016).
4. Hickey et al. (2019) frames speed breeding as a multiplier for genomic selection, editing, and phenotyping pipelines.
5. [REVIEW] Crop-specific baseline generation times may differ from the 2-3 gen/year assumption; adjust speedup factors if local baselines are available.

---

## 5. Files Generated

- `data/domain_c_breeding/speed_breeding_data.json`
- `data/domain_c_breeding/C3_speed_breeding_literature_review.md`

*Task C3 Complete*
