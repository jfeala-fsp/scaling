# A2: Major Transitions Data Extraction

**Task**: Extract quantitative data on major evolutionary transitions using Maynard Smith and Szathmary framework, and estimate ESP for major phenotypic innovations.
**Status**: Draft estimates (order-of-magnitude)
**Date**: February 2026
**Inputs**: `data/domain_A_evolution/A1_evolution_literature_review.md`
**Output table**: `data/domain_A_evolution/a2_major_transitions_esp_estimates.csv`

---

## Scope and Method

This table summarizes the eight major transitions listed by Maynard Smith and Szathmary (1995), with order-of-magnitude estimates for:

- Duration of the transition (time window from earliest evidence to stabilization)
- Effective population size (Ne)
- Generation time
- Total generations in the window
- ESP estimate using **individuals per successful transition**:

```
ESP_individuals = Ne * generations
```

These are **coarse, uncertainty-heavy estimates** meant to anchor the expected ESP range (10^15 to 10^20) for deep-time transitions. The values are intended as inputs for later sensitivity analysis. Where estimates are particularly speculative, they are flagged below.

**Important**: This approach does *not* explicitly multiply by mutation rate or genome size; it treats each individual as an "experiment". A mutation-based ESP would be lower by a factor roughly equal to per-genome mutation rate per generation. For deep-time transitions, we keep the individual-based ESP to match the expected range.

---

## Summary Table (Order-of-Magnitude)

See `data/domain_A_evolution/a2_major_transitions_esp_estimates.csv` for full numeric values and log10 ranges. Key highlights:

- **Origin of life / chromosomes / genetic code**: ESP_individuals ~10^17 to 10^20
- **Eukaryotes and sex**: ESP_individuals ~10^15 to 10^18
- **Multicellularity**: ESP_individuals ~10^14 to 10^16 (lower bound below expected range)
- **Eusociality**: ESP_individuals ~10^13 to 10^16 (lower bound below expected range)
- **Language**: ESP_individuals ~10^7 to 10^9 (strong outlier; likely dominated by cultural evolution) [REVIEW]

---

## Assumptions and Notes

1. **Time windows** are approximated from the paleontological literature and Maynard Smith and Szathmary timelines. These should be tightened with specific stratigraphic references. [VERIFY]
2. **Ne ranges** for deep-time microbial populations are approximate (10^7 to 10^9) based on modern microbial Ne estimates and drift-barrier arguments. [VERIFY]
3. **Generation times** for early microbial life are set to 0.001-0.01 years (0.4-3.7 days). Early eukaryotes are set to 0.01-0.1 years. [VERIFY]
4. **Multicellularity and eusociality** likely involve multiple independent origins. The ESP formula here treats each transition as a single success; a multi-origin correction could reduce ESP by a factor equal to the number of origins. [REVIEW]
5. **Language** is heavily influenced by cultural transmission; genetic ESP estimates may not be appropriate for this transition. [REVIEW]

---

## References (Selected)

1. Maynard Smith, J. and Szathmary, E. *The Major Transitions in Evolution*. Oxford University Press (1995).
2. Szathmary, E. Toward major evolutionary transitions theory 2.0. *Proc. Natl Acad. Sci. USA* **112**, 10104-10111 (2015).
3. Lee, M. S. Y., Soubrier, J. and Edgecombe, G. D. Rates of phenotypic and genomic evolution during the Cambrian Explosion. *Curr. Biol.* **23**, 1889-1895 (2013).
4. Wagner, G. P. and Altenberg, L. Complex adaptations and the evolution of evolvability. *Evolution* **50**, 967-976 (1996).

[VERIFY] Provide exact page ranges or DOI where possible before final write-up.

---

## Files Generated

- `data/domain_A_evolution/a2_major_transitions_esp_estimates.csv`
- `data/domain_A_evolution/A2_major_transitions_data_extraction.md`

---

*Task A2 Draft Complete (estimates pending verification)*
