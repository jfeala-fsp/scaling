PYTHON ?= python3

DOMAIN_A_OUTPUTS = \
	data/domain_A_evolution/processed/mutation_rates_per_bp.csv \
	data/domain_A_evolution/processed/mutation_rates_per_genome.csv \
	data/domain_A_evolution/processed/a2_major_transitions_esp_estimates.csv

DOMAIN_B_OUTPUTS = \
	data/domain_b/processed/domestication_timeline_compilation.csv

DOMAIN_C_OUTPUTS = \
	results/tables/tbl01_cimmyt_esp.csv

DOMAIN_D_OUTPUTS = \
	results/tables/tbl_d1_directed_evolution_esp.csv \
	results/tables/tbl_d2_ml_guided_esp.csv

DOMAIN_E_OUTPUTS = \
	data/domain_e/raw/thennt_nnt_extracted.csv \
	data/domain_e/processed/nnt_database.csv \
	data/domain_e/processed/fda_pivotal_trials.csv \
	results/tables/tbl_e1_nnt_summary_by_area.csv \
	results/tables/tbl_e1_nnt_by_year.csv \
	results/tables/tbl_e2_fda_trial_sizes_by_year.csv \
	results/tables/tbl_e2_fda_nnt_by_area.csv \
	results/tables/tbl_e4_gene_therapy_esp.csv

BUILD_OUTPUTS = \
	$(DOMAIN_A_OUTPUTS) \
	$(DOMAIN_B_OUTPUTS) \
	$(DOMAIN_C_OUTPUTS) \
	$(DOMAIN_D_OUTPUTS) \
	$(DOMAIN_E_OUTPUTS)

CLEAN_OUTPUTS = $(BUILD_OUTPUTS)

.PHONY: build clean test

build: $(BUILD_OUTPUTS)

test:
	$(PYTHON) src/utils/validate_outputs.py

clean:
	rm -f $(CLEAN_OUTPUTS)

data/domain_A_evolution/processed:
	mkdir -p $@

data/domain_b/processed:
	mkdir -p $@

data/domain_e/raw:
	mkdir -p $@

data/domain_e/processed:
	mkdir -p $@

results/tables:
	mkdir -p $@

data/domain_A_evolution/processed/mutation_rates_per_bp.csv data/domain_A_evolution/processed/mutation_rates_per_genome.csv: \
	src/preprocessing/compile_mutation_rates.py data/domain_A_evolution/mutation_rates_compilation.md | data/domain_A_evolution/processed
	$(PYTHON) src/preprocessing/compile_mutation_rates.py

data/domain_A_evolution/processed/a2_major_transitions_esp_estimates.csv: \
	src/preprocessing/compile_major_transitions_esp.py data/domain_A_evolution/a2_major_transitions_esp_estimates.csv | data/domain_A_evolution/processed
	$(PYTHON) src/preprocessing/compile_major_transitions_esp.py

data/domain_b/processed/domestication_timeline_compilation.csv: \
	src/preprocessing/compile_domestication_timeline.py data/domain_b/domestication_data.json | data/domain_b/processed
	$(PYTHON) src/preprocessing/compile_domestication_timeline.py

results/tables/tbl01_cimmyt_esp.csv: \
	src/analysis/c2_cimmyt_esp.py data/domain_c/c2_cimmyt_inputs.csv | results/tables
	$(PYTHON) src/analysis/c2_cimmyt_esp.py

results/tables/tbl_d1_directed_evolution_esp.csv: \
	src/analysis/d1_directed_evolution_esp.py data/domain_d/directed_evolution_outcomes.csv | results/tables
	$(PYTHON) src/analysis/d1_directed_evolution_esp.py

results/tables/tbl_d2_ml_guided_esp.csv: \
	src/analysis/d2_ml_guided_esp.py data/domain_d/ml_guided_design_outcomes.csv | results/tables
	$(PYTHON) src/analysis/d2_ml_guided_esp.py

data/domain_e/raw/thennt_nnt_extracted.csv data/domain_e/processed/nnt_database.csv: \
	src/preprocessing/extract_thennt_nnt.py data/domain_e/raw/thennt_pages.csv | data/domain_e/raw data/domain_e/processed
	$(PYTHON) src/preprocessing/extract_thennt_nnt.py

data/domain_e/processed/fda_pivotal_trials.csv: \
	src/preprocessing/compile_fda_pivotal_trials.py data/domain_e/raw/fda_pivotal_trials_extracted.csv | data/domain_e/processed
	$(PYTHON) src/preprocessing/compile_fda_pivotal_trials.py

results/tables/tbl_e1_nnt_summary_by_area.csv results/tables/tbl_e1_nnt_by_year.csv: \
	src/analysis/e1_nnt_summary.py data/domain_e/processed/nnt_database.csv | results/tables
	$(PYTHON) src/analysis/e1_nnt_summary.py

results/tables/tbl_e2_fda_trial_sizes_by_year.csv results/tables/tbl_e2_fda_nnt_by_area.csv: \
	src/analysis/e2_fda_summary.py data/domain_e/processed/fda_pivotal_trials.csv | results/tables
	$(PYTHON) src/analysis/e2_fda_summary.py

results/tables/tbl_e4_gene_therapy_esp.csv: \
	src/analysis/e4_gene_therapy_esp.py data/domain_e/processed/e4_gene_therapy_cart_outcomes.csv | results/tables
	$(PYTHON) src/analysis/e4_gene_therapy_esp.py
