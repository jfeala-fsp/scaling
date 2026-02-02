# Domain D: Molecular biotechnology outcomes

## Scope
This folder tracks molecular biotechnology success rates and derived ESP values.
Entries focus on experimental validation outcomes where the number of designs tested
and the number of successful designs are explicitly reported.

## Files
- directed_evolution_outcomes.csv: structured table of directed evolution outcomes
- ml_guided_design_outcomes.csv: structured table of ML-guided design outcomes

## Extraction notes
### Directed evolution
- DE-2025-01 (PMC12514840, Protein Sci 2025)
  - "Approximately 5 x 10^5 clones were screened at each temperature, and three blaC clones were found on the plate incubated at 30C."
  - ESP uses 500,000 screened clones and 3 blaC clones as successes.

- DE-2025-02 (PMC12723733, ACS Synth Biol 2025)
  - "This library, consisting of over 1 x 10^8 unique clones..."
  - "identified six unique scFv clones ... exhibiting specific binding in the final round."
  - ESP uses 100,000,000 library size and 6 binding clones as successes.

- DE-2026-01 (PMC12657606, Synth Syst Biotechnol 2026)
  - "screened over 10,000 clones through three rounds of directed evolution and developed DepoPETase."
  - ESP uses 10,000 clones and 1 final DepoPETase variant as success (reported in a summary citation).

### ML-guided protein design
- MLD-2020-01 (bioRxiv 2020)
  - "129 hallucinated sequences ... selected for experimental testing" and "27 folded to monomeric stable structures."
  - Preprint version of the 2021 Nature study; avoid double counting if aggregating.
- MLD-2021-01 (PMC9293396, Nature 2021)
  - "found that 27 folded to monodisperse species with circular dichroism spectra consistent with the hallucinated structures."
  - 129 designs were experimentally tested; ESP uses 129 tested designs and 27 folded designs.

- MLD-2022-01 (PMC9621694, Science 2022)
  - "We expressed 37 hallucinated RSV-F site V scaffolds ... and found that three bound the neutralizing antibody hRSV90."
  - ESP uses 37 tested scaffolds and 3 binding designs.

- MLD-2023-01 (PMC10204179, Protein Sci 2023)
  - "In vitro validation showed that 7 out of 39 designs were folded and stable in solution with high melting temperatures."
  - ESP uses 39 tested designs and 7 folded, stable designs.

- MLD-2023-02 (PMC10089152, PNAS 2023)
  - "71 were selected for experimental characterization ... 28 ... monomers by SEC."
  - ESP uses 71 tested designs and 28 monomeric designs by SEC.

- MLD-2024-01 (PMC11510650, Molecules 2024)
  - "four selected generative sequences" were synthesized; Z1 and Z2 showed similar function to parental Protein A.
  - ESP uses 4 tested sequences and 2 functional sequences (Z1, Z2).

- MLD-2024-02 (PMC11081422, Protein Sci 2024)
  - "six designs were selected for experimental characterization" and all were soluble; five showed monomeric SEC-MALS peaks.
  - ESP uses 6 tested designs and 5 monomeric designs.

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
