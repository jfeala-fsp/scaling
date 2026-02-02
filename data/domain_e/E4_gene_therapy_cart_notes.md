# Domain E4: Gene therapy and CAR-T outcomes

This note documents source extraction for gene therapy and CAR-T outcomes
used to compute ESP values for the precision medicine era.

## Sources

All outcomes are taken from FDA prescribing information accessed via the
OpenFDA label API. Each data row links to the exact query used.

## Extraction notes

- Kymriah (tisagenlecleucel), Study 1 (ELIANA; NCT02435849)
  - Endpoint: CR/CRi within 3 months after infusion.
  - Label text reports 63 infused patients with 52 (83%) achieving CR/CRi.

- Yescarta (axicabtagene ciloleucel), ZUMA-1 (NCT02348216)
  - Endpoint: complete remission (CR) rate.
  - Label text reports N=101 with CR 52 (51%).

- Zolgensma (onasemnogene abeparvovec), Study 1 (NCT03306277)
  - Endpoint: event-free survival at 14 months (alive without permanent ventilation).
  - Label text reports 19 of 21 patients alive without permanent ventilation.

- Luxturna (voretigene neparvovec), Study 2 (NCT00999609)
  - Endpoint: MLMT score change >=2 at Year 1 (both eyes).
  - Label text reports 11 of 21 (52%) achieving this threshold.

## Caveats

- Endpoints reflect label-defined primary efficacy metrics, which differ
  across therapies. ESP values are calculated using the labeled endpoint.
- Label updates can change wording; if values differ, confirm against the
  current label and original trial publication.
