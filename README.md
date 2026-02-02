# Scaling Research Build Guide

This repository uses Make to reproduce preprocessing and analysis outputs from raw inputs.

## Prerequisites

- Python 3.11+
- Install packages from `requirements.txt`:
  - `numpy`
  - `pandas`
- Network access is required to fetch TheNNT data during the build.

## Reproducible Build

Run:
```bash
make build
```

`make build` reproduces all analysis outputs from raw data and standardized inputs.

## Validation

Run:
```bash
make test
```

This checks that generated outputs exist, are non-empty, and include required columns.

## Cleanup

Run:
```bash
make clean
```

This removes generated outputs so the build can be re-run from a clean state.
