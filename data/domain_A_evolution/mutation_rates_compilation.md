# Mutation Rate Data Across Taxa

## Compilation of Quantitative Mutation Rate Data from Peer-Reviewed Literature

---

## 1. Per Base Pair Per Generation Mutation Rates

| Organism | Scientific Name | Rate (per bp per generation) | Genome Size (bp) | Source |
|----------|-----------------|------------------------------|------------------|--------|
| **Bacteria (E. coli)** | *Escherichia coli* | ~5.4 x 10^-10 | 4.6 x 10^6 | Drake et al. 1998; Lee et al. 2012 |
| **Yeast** | *Saccharomyces cerevisiae* | ~1.7-3.3 x 10^-10 | 1.2 x 10^7 | Lynch et al. 2008; Zhu et al. 2014 |
| **Nematode** | *Caenorhabditis elegans* | ~2.7 x 10^-9 | 1.0 x 10^8 | Denver et al. 2009; Lynch et al. 2008 |
| **Fruit fly** | *Drosophila melanogaster* | ~2.8-5.4 x 10^-9 | 1.4 x 10^8 | Keightley et al. 2009; Haag-Liautard et al. 2007 |
| **Mouse** | *Mus musculus* | ~5.4 x 10^-9 | 2.8 x 10^9 | Uchimura et al. 2015; Lindsay et al. 2019 |
| **Human** | *Homo sapiens* | ~1.0-2.5 x 10^-8 | 3.2 x 10^9 | Kong et al. 2012; Nachman & Crowell 2000; BioNumbers |

---

## 2. Per Genome Per Generation Mutation Rates

| Organism | Mutations per genome per generation | Notes | Source |
|----------|-------------------------------------|-------|--------|
| **Bacteria (E. coli)** | ~0.0025-0.003 | ~1 mutation per 300-400 generations | Drake 1991; Drake et al. 1998 |
| **Yeast** | ~0.002-0.004 | Similar to bacteria despite larger genome | Lynch et al. 2008 |
| **Nematode (C. elegans)** | ~0.4-2.1 | Per sexual generation | Denver et al. 2009 |
| **Fruit fly (Drosophila)** | ~0.5-1.5 | Per generation | Keightley et al. 2009 |
| **Mouse** | ~12-50 | Per generation; varies with parental age | Uchimura et al. 2015 |
| **Human** | ~50-175 | 60-80 typical; ~175 per diploid genome | Kong et al. 2012; BioNumbers |

---

## 3. Key Papers and Findings

### Drake's Classic Work on Microbial Mutation Rates

**Drake, J.W. (1991)** "A constant rate of spontaneous mutation in DNA-based microbes" *PNAS* 88:7160-7164
- Established that DNA-based microbes have remarkably constant genomic mutation rates
- **Key finding**: ~0.003 mutations per genome per replication across diverse microbes
- This constancy holds across 4 orders of magnitude in genome size

**Drake, J.W., Charlesworth, B., Charlesworth, D., Crow, J.F. (1998)** "Rates of Spontaneous Mutation" *Genetics* 148:1667-1686
- Comprehensive review of mutation rate data
- **Key finding**: Per base pair rates vary ~1000-fold across organisms
- Per genome rates much more constrained (~0.003 for microbes, 0.1-100 for higher eukaryotes)
- Proposed that mutation rates are optimized by selection

### Lynch's Work on Eukaryotic Mutation Rates

**Lynch, M. (2010)** "Evolution of the mutation rate" *Trends in Genetics* 26:345-352
- Reviews mechanisms underlying mutation rate variation
- Argues that genetic drift constrains selection on mutation rate modifiers
- Smaller population sizes in eukaryotes permit higher mutation rates

**Lynch, M., Sung, W., Morris, K., et al. (2008)** "A genome-wide view of the spectrum of spontaneous mutations in yeast" *PNAS* 105:9272-9277
- Direct estimate from mutation accumulation experiments
- **Yeast rate**: ~3.3 x 10^-10 per bp per generation
- Identified biases in mutation spectrum

**Lynch, M. (2010)** "Rate, molecular spectrum, and consequences of human mutation" *PNAS* 107:961-968
- Comprehensive analysis of human mutation rate
- **Human rate**: ~1.1 x 10^-8 per base per generation
- Discusses implications for evolution and disease

### Additional Key Papers

**Denver, D.R., Dolan, P.C., Wilhelm, L.J., et al. (2009)** "A genome-wide view of Caenorhabditis elegans base-substitution mutation processes" *PNAS* 106:16310-16314
- **C. elegans rate**: ~2.7 x 10^-9 per bp per generation
- Mutation accumulation study with direct sequencing

**Keightley, P.D., Trivedi, U., Thomson, M., et al. (2009)** "Analysis of the genome sequences of three Drosophila melanogaster spontaneous mutation accumulation lines" *Genome Research* 19:1195-1201
- **Drosophila rate**: ~5.4 x 10^-9 per bp per generation
- First direct whole-genome estimate for Drosophila

**Kong, A., Frigge, M.L., Masson, G., et al. (2012)** "Rate of de novo mutations and the importance of father's age to disease risk" *Nature* 488:471-475
- Human trio sequencing study
- **Human rate**: ~1.2 x 10^-8 per bp per generation
- Key finding: paternal age effect (~2 mutations per year of father's age)

**Nachman, M.W. & Crowell, S.L. (2000)** "Estimate of the mutation rate per nucleotide in humans" *Genetics* 156:297-304
- Classic comparative genomics estimate
- **Human rate**: ~2.5 x 10^-8 per bp per generation

---

## 4. Drake's Rule: Constant Genomic Mutation Rate

A key insight from Drake's work is that DNA-based microorganisms maintain a nearly constant genomic mutation rate of approximately 0.003 mutations per genome per replication, despite genome sizes varying by 10,000-fold.

| Organism | Genome Size (bp) | Rate per bp | Rate per genome |
|----------|------------------|-------------|-----------------|
| Bacteriophage lambda | 4.9 x 10^4 | 7.7 x 10^-8 | 0.0038 |
| Bacteriophage T4 | 1.7 x 10^5 | 2.4 x 10^-8 | 0.0040 |
| *E. coli* | 4.6 x 10^6 | 5.4 x 10^-10 | 0.0025 |
| *S. cerevisiae* | 1.2 x 10^7 | 2.2 x 10^-10 | 0.0027 |
| *N. crassa* | 4.2 x 10^7 | 7.2 x 10^-11 | 0.0030 |

**Interpretation**: This suggests strong selection pressure to maintain optimal mutation rates - high enough to allow adaptation but low enough to prevent excessive genetic load.

---

## 5. Relationship Between Genome Size and Mutation Rate

The data reveal an inverse relationship between genome size and per-base mutation rate:

```
Per-bp rate  x  Genome size  approximately equals  Constant (for microbes ~0.003)
```

For higher eukaryotes, this relationship breaks down, with per-genome rates increasing substantially:

| Category | Genome Size | Per-bp rate | Per-genome rate |
|----------|-------------|-------------|-----------------|
| DNA viruses/phages | 10^4 - 10^5 | ~10^-7 - 10^-8 | ~0.003 |
| Bacteria | ~10^6 - 10^7 | ~10^-9 - 10^-10 | ~0.003 |
| Unicellular eukaryotes | ~10^7 | ~10^-10 | ~0.003-0.005 |
| Multicellular eukaryotes | 10^8 - 10^10 | ~10^-8 - 10^-9 | ~1-100 |

---

## 6. Summary Table: Consensus Values

| Organism | Per bp per generation | Per genome per generation | Effective genome size |
|----------|----------------------|---------------------------|----------------------|
| E. coli | 5 x 10^-10 | 0.003 | 4.6 Mb |
| S. cerevisiae (yeast) | 2 x 10^-10 | 0.003 | 12 Mb |
| C. elegans | 2.7 x 10^-9 | 2.1 | 100 Mb |
| D. melanogaster | 3.5 x 10^-9 | 0.5-1.5 | 140 Mb |
| M. musculus (mouse) | 5.4 x 10^-9 | 15-50 | 2.8 Gb |
| H. sapiens (human) | 1.2 x 10^-8 | 60-80 (haploid); 120-175 (diploid) | 3.2 Gb |

---

## 7. Important Caveats

1. **Per replication vs. per generation**: Rates differ significantly. Humans have ~200-400 cell divisions in male germline by age 30, so per-replication rates are ~1000x lower than per-generation rates.

2. **Mutation type variation**: The rates above primarily refer to single nucleotide substitutions. Indels occur at roughly 10-20% of the SNV rate.

3. **Regional variation**: Mutation rates vary across the genome by 2-3 fold depending on local sequence context, replication timing, and chromatin state.

4. **Parental age effects**: In humans and other mammals, mutation rate increases with paternal age (~1-2 additional mutations per year of father's age).

5. **Sex differences**: Males typically contribute more mutations due to more germline cell divisions.

---

## 8. Data Sources

### Primary Literature
- Drake, J.W. (1991) PNAS 88:7160-7164
- Drake, J.W. et al. (1998) Genetics 148:1667-1686
- Lynch, M. et al. (2008) PNAS 105:9272-9277
- Lynch, M. (2010) Trends in Genetics 26:345-352
- Lynch, M. (2010) PNAS 107:961-968
- Denver, D.R. et al. (2009) PNAS 106:16310-16314
- Keightley, P.D. et al. (2009) Genome Research 19:1195-1201
- Kong, A. et al. (2012) Nature 488:471-475
- Nachman, M.W. & Crowell, S.L. (2000) Genetics 156:297-304
- Uchimura, A. et al. (2015) Genome Research 25:1125-1132
- Zhu, Y.O. et al. (2014) Genome Research 24:300-311

### Databases
- BioNumbers (https://bionumbers.hms.harvard.edu)
- Cell Biology by the Numbers (https://book.bionumbers.org)

---

*Compiled: February 2026*
*Note: Values represent consensus estimates from mutation accumulation experiments and direct sequencing studies. Individual studies may report somewhat different values depending on methodology and specific strains used.*
