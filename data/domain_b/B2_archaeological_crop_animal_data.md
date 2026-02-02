# B2: Archaeological Crop/Animal Data

**Task**: Extract archaeological data on crop yield proxies and animal trait changes during domestication. Calculate ESP_domestication values.
**ESP Domain**: Domain B - Domestication and Early Breeding
**Date**: February 2026
**Status**: Data Compiled

---

## Executive Summary

This document compiles archaeological trait-change evidence for key domesticated crops and animals used in Domain B ESP calculations. The data focus on measurable morphological proxies (grain size, cob length, body size) and qualitative domestication traits (non-shattering, naked kernels). ESP values are re-stated for the same species to keep archaeological evidence aligned with the domestication denominators.

**Key finding**: Archaeological trait shifts are consistent with prolonged selection spans (hundreds to thousands of generations), supporting ESP values in the 10^5 to 10^7 range for domestication-era outcomes.

---

## 1. Archaeological Trait-Change Dataset

**File**: `data/domain_b/archaeological_crop_animal_data.csv`

**Columns**:
- species
- category
- trait
- baseline_value
- domesticated_value
- change_description
- archaeological_proxy
- time_span_years
- generations_estimate
- source_reference
- data_quality
- notes

### Notes on Interpretation

1. **Yield proxies**: Direct crop yield measurements are unavailable archaeologically. Grain size, ear length, and kernel row number are used as yield proxies. These are labeled explicitly in the dataset.
2. **Temporal uncertainty**: Trait fixation estimates represent broad ranges derived from archaeobotanical sequences and ancient DNA studies.
3. **Behavioral traits**: Behavioral traits (e.g., docility) are inferred from proxies such as brain size reduction and should be treated as lower-confidence estimates.

---

## 2. ESP_domestication Calculations (Species-Level)

The ESP calculations below use the same denominators as the Domain B core dataset (`data/domain_b/domestication_data.json`). They are included here to align archaeological trait evidence with the species-level ESP values.

### Wheat (Triticum spp.)

**Inputs**:
- Population: 32,500 (effective Ne, wild)
- Generations: 2,500
- Phenotypic outcomes: 10

**Calculation**:
```
ESP = (32,500 × 2,500) / 10 = 8,125,000
log10(ESP) = 6.9
```

### Maize (Zea mays)

**Inputs**:
- Population: 2,500 (average Ne during domestication)
- Generations: 3,700
- Phenotypic outcomes: 5

**Calculation**:
```
ESP = (2,500 × 3,700) / 5 = 1,850,000
log10(ESP) = 6.3
```

### Dogs (Canis familiaris)

**Inputs**:
- Population: 2,000 (initial domestication phase)
- Generations: 200
- Phenotypic outcomes: 12

**Calculation**:
```
ESP = (2,000 × 200) / 12 = 33,333
log10(ESP) = 4.5
```

### Cattle (Bos taurus / Bos indicus)

**Inputs**:
- Population: 2,000 (geometric mean during early domestication)
- Generations: 750
- Phenotypic outcomes: 6

**Calculation**:
```
ESP = (2,000 × 750) / 6 = 250,000
log10(ESP) = 5.4
```

---

## 3. Data Quality Assessment

| Species | Trait evidence quality | Notes |
| --- | --- | --- |
| Wheat | 3 | Archaeobotanical grain size and rachis evidence are strong, regional timing uncertain |
| Maize | 3 | Cob and kernel traits well documented, fixation timing variable |
| Dogs | 2 | Behavioral traits inferred from proxy evidence; archaeological signals mixed |
| Cattle | 4 | Body size reduction and founder bottleneck well supported |

---

## 4. References (Selected)

1. Purugganan MD, Fuller DQ. The nature of selection during plant domestication. Nature (2009).
2. Allaby RG et al. Domestication in plants: a genomic perspective. Phil Trans R Soc B (2017).
3. Matsuoka Y et al. A single domestication for maize. PNAS (2002).
4. Tenaillon MI et al. The origin of maize: evidence from genome diversity. Mol Biol Evol (2004).
5. Ramos-Madrigal J et al. Genome sequence of a 5,310-year-old maize cob. Curr Biol (2016).
6. Murray C et al. Cattle domestication: archaeological and genetic evidence. Philos Trans R Soc B (2010).
7. Bollongino R et al. Modern taurine cattle descended from small number of founders. Mol Biol Evol (2012).
8. Larson G, Fuller DQ. The evolution of animal domestication. Annu Rev Ecol Evol Syst (2014).

---

*Document prepared for ESP Research Project - Task B2*
