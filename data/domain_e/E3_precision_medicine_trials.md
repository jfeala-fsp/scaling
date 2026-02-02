# Task E3: Precision Medicine Trial Outcomes

## Overview
This dataset compiles response rates for biomarker-stratified treatments used in
precision oncology. It includes key precision-medicine programs (IMPACT and
NCI-MATCH), a tumor-agnostic approval (larotrectinib), and representative
biomarker-drug pairs requested in the research plan. The primary output is:

- `data/domain_e/processed/e3_precision_medicine_trials.csv`

## Field Notes
- `experiments_tested` and `successes` reflect matched cohorts when reported.
- `response_rate_matched` is recorded as a proportion (0-1).
- `effective_nnt` and `esp` are computed as `1 / response_rate_matched`.
- Rows flagged with `[VERIFY]` require confirmation of exact denominators or
  subgroup response rates from the primary trial tables.

## Sources (Primary, Open Access)
1. Tsimberidou AM, et al. Long-term overall survival and prognostic score
   predicting survival: the IMPACT study in precision medicine. *J Hematol
   Oncol* **12**, 145 (2019). DOI: 10.1186/s13045-019-0835-1.
   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6937824/
2. Salama AKS, et al. Phase II Study of Dabrafenib and Trametinib in Patients
   With Tumors With BRAF V600E Mutations: Updated Results From NCI-MATCH
   ECOG-ACRIN Trial (EAY131) Subprotocol H. *JCO Precis Oncol* (2026).
   DOI: 10.1200/po-25-00338.
   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12810769/
3. Drilon A, et al. Efficacy of Larotrectinib in TRK Fusion-Positive Cancers in
   Adults and Children. *N Engl J Med* **378**, 731-739 (2018).
   DOI: 10.1056/NEJMoa1714448.
   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5857389/

## Sources (Require Verification)
- KEYNOTE-158 MSI-H/dMMR pooled analysis (Pembrolizumab).
- Slamon et al. 2001 HER2+ metastatic breast cancer trial (Trastuzumab).
- IPASS EGFR-mutant NSCLC subgroup (Gefitinib).
- PROFILE 1001 ALK+ NSCLC (Crizotinib).
- BRIM-3 BRAF V600E melanoma (Vemurafenib).
- IRIS chronic-phase CML (Imatinib).
- KEYNOTE-024 PD-L1 high NSCLC (Pembrolizumab).

These rows are flagged `[VERIFY]` in the dataset and should be updated with
exact subgroup denominators and response rates from the primary trial tables.
