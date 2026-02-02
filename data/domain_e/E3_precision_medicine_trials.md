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
- Objective response rates and denominators are pulled from primary trial
  abstracts or ClinicalTrials.gov results tables when subgroup counts are
  not stated in the abstract.

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

## Sources (Additional, Open Access)
4. Marabelle A, et al. Pembrolizumab in patients with MSI-H/dMMR cancers
   (KEYNOTE-158). *J Clin Oncol* **38**, 1-10 (2020).
   DOI: 10.1200/JCO.19.02652. PMID: 31682550.
5. Slamon DJ, et al. Use of chemotherapy plus a monoclonal antibody against
   HER2 for metastatic breast cancer. *N Engl J Med* **344**, 783-792 (2001).
   DOI: 10.1056/NEJM200103153441101. PMID: 11248153.
6. O'Brien SG, et al. Imatinib compared with interferon and low-dose cytarabine
   for newly diagnosed chronic-phase chronic myeloid leukemia. *N Engl J Med*
   **348**, 994-1004 (2003). DOI: 10.1056/NEJMoa021119. PMID: 12637609.

## Sources (ClinicalTrials.gov Results Tables)
- NCT00322452 (IPASS): Objective tumor response rate by RECIST (ITT population).
- NCT00585195 (PROFILE 1001): RP2D ALK-positive NSCLC cohort ORR.
- NCT01006980 (BRIM-3): Best overall response counts by arm.
- NCT02142738 (KEYNOTE-024): Objective response rate by arm.

ClinicalTrials.gov results tables are cited where the peer-reviewed abstract
does not list subgroup denominators or response counts.
