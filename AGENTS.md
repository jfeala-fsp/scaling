# AGENTS.md — Research & Data Analysis Guidelines

This document guides AI agents working on this research project. Follow these standards to ensure rigorous, reproducible, and publication-ready work.

---

## Project Overview

Read `research_plan.md` for an overview of the project, after you have reviewed this document.

## Project Tracking

This project uses **bd (beads)** for task tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create issue
- `bd close <id>` - Complete work
- `bd sync` - Sync with git (run at session end)

For full workflow details: `bd prime`

**Workflow norms:**
- Run `bd sync` before `bd ready` to avoid stale assignments.
- Always claim an issue before starting work: `bd update <id> --claim`.

## Project Context

This is a **quantitative/statistical research paper**. All analysis must prioritize:
- Reproducibility
- Statistical rigor
- Clear documentation
- Nature citation standards

---

## Code Standards

### Python
- Use `pandas` for data manipulation, `numpy` for numerical operations
- Use `scipy.stats` or `statsmodels` for statistical tests
- Visualization: prefer `matplotlib` + `seaborn` for publication-quality figures
- Include docstrings for all functions (NumPy style)
- Type hints encouraged for function signatures

```python
def compute_effect_size(group1: np.ndarray, group2: np.ndarray) -> float:
    """
    Calculate Cohen's d effect size between two groups.

    Parameters
    ----------
    group1 : np.ndarray
        Values for the first group.
    group2 : np.ndarray
        Values for the second group.

    Returns
    -------
    float
        Cohen's d effect size.
    """
```

### R
- Follow tidyverse style guide
- Use `tidyverse` for data wrangling, `ggplot2` for visualization
- Use `broom` to tidy model outputs
- Prefer pipes (`|>` or `%>%`) for readable data transformations
- Comment non-obvious statistical choices

```r
# Example: Running a regression with clear documentation
model <- lm(outcome ~ predictor + covariate, data = df)
tidy(model, conf.int = TRUE)  # Extract coefficients with CIs
```

### General
- All scripts must run end-to-end without manual intervention
- Use relative paths from project root
- Set random seeds explicitly for any stochastic operations
- Never hardcode paths to local machines

---

## Statistical Analysis Standards

### Before Any Analysis
1. **State the hypothesis** clearly (null and alternative)
2. **Check assumptions** for the planned test (normality, homoscedasticity, independence)
3. **Determine sample size** considerations and power if applicable

### Reporting Results
Always report:
- Test statistic and degrees of freedom
- Exact p-value (or p < .001 if very small)
- Effect size with confidence interval
- Sample size (n)

**Example (Nature style):**
> Scores increased significantly from pre-test (4.2 ± 1.1) to post-test (5.8 ± 1.3; paired t-test, t₄₂ = 3.67, P < 0.001, Cohen's d = 0.56, 95% CI: 0.31–0.81).

### Common Pitfalls to Avoid
- Never p-hack or run multiple tests without correction
- Report all conducted analyses, not just significant ones
- Check for outliers and document handling decisions
- Verify assumptions before parametric tests
- Use appropriate corrections for multiple comparisons (Bonferroni, FDR, etc.)

---

## Data Handling

### Data Integrity
- Never modify raw data files—always create processed versions
- Document all cleaning steps in code comments or a separate log
- Track missing data: report counts and handling method (listwise deletion, imputation, etc.)

### File Organization
```
data/
├── raw/           # Original, untouched data
├── processed/     # Cleaned, analysis-ready data
├── codebook.md    # Variable definitions and coding schemes

src/               # Production-ready analysis scripts
├── analysis/      # Main analysis scripts
├── preprocessing/ # Data cleaning and transformation
├── utils/         # Shared helper functions

notebooks/         # Exploratory analysis (Jupyter/Quarto/Rmd)
├── exploration/   # Initial data exploration, prototyping
├── archive/       # Completed exploratory work (reference only)

results/
├── figures/       # Publication-ready plots
├── tables/        # Exported tables (CSV, LaTeX)
├── models/        # Saved model objects, fitted parameters
```

### Notebook → Script Workflow
1. **Explore** in `notebooks/exploration/` — iterate quickly, visualize, test ideas
2. **Validate** findings are reproducible and worth keeping
3. **Migrate** finalized code to `src/` as clean, documented scripts
4. **Archive** the notebook to `notebooks/archive/` with a note on what was learned

Notebooks are for discovery; scripts are for reproducibility. Never cite notebook outputs in the paper—always regenerate from `src/`.

---

## Figures & Tables

### Figures
- Save to `results/figures/`
- Minimum 300 DPI for publication
- Use colorblind-friendly palettes (viridis, ColorBrewer)
- Include clear axis labels with units
- Add informative captions that can stand alone
- Save as both `.png` (for drafts) and `.pdf` or `.svg` (for publication)

### Tables
- Save to `results/tables/`
- Follow Nature table guidelines (minimal horizontal lines, no vertical lines)
- Include notes explaining abbreviations below the table
- Report descriptive statistics (mean ± s.d.) alongside inferential statistics
- Align decimal points in numeric columns
- Use sentence-case for column headers

---

## Citations & References

### In-Text (Nature Style)
- Use superscript numbers in order of appearance: "Recent studies¹ have shown..."
- Multiple citations: use comma-separated superscripts (¹,²,³) or ranges (¹⁻³)
- Numbers appear after punctuation: "...as previously reported.⁴"
- Do not use author names in citations unless necessary for context

### Reference List (Nature Format)
- Number references in order of first appearance
- Author(s). Title of article. *Journal Name* **volume**, page range (year).
- List up to 5 authors, then "et al." for more
- Include DOIs when available

**Example:**
> 1. Smith, A. B., Jones, C. D. & Lee, E. F. Statistical methods for behavioral research. *Nature Methods* **15**, 234–241 (2023).

### Journal Abbreviations
- Use standard Index Medicus abbreviations
- *Nature* (not *Nature Journal*)
- *Proc. Natl Acad. Sci. USA*
- *J. Am. Stat. Assoc.*

### When Adding Citations
- Verify the source exists and is accurately represented
- Prefer peer-reviewed sources
- Include page numbers for specific claims
- Flag any citation that needs verification with `[VERIFY]`

---

## Reproducibility Checklist

Before finalizing any analysis:

- [ ] All code in `src/` runs from a clean environment
- [ ] Random seeds are set and documented
- [ ] All data transformations are scripted (not manual)
- [ ] Package versions are recorded (`requirements.txt` / `renv.lock`)
- [ ] Results match between reruns
- [ ] All figures in `results/figures/` regenerate from `src/` scripts
- [ ] No notebook outputs are cited—only outputs from `src/`
- [ ] Statistical assumptions are tested and documented

---

## Quality Assurance

### Self-Check Before Submitting Work
1. **Accuracy**: Do the numbers in prose match the code output?
2. **Completeness**: Are all requested analyses included?
3. **Clarity**: Would another researcher understand the approach?
4. **Assumptions**: Are statistical assumptions met and documented?
5. **Interpretation**: Are conclusions supported by the evidence?

### When Uncertain
- State uncertainty explicitly: "This result should be interpreted with caution because..."
- Flag items needing human review with `[REVIEW]`
- Propose alternative approaches if assumptions are violated
- Ask clarifying questions rather than make assumptions

---

## Communication Style

When presenting findings:
- Lead with the key insight, then support with details
- Use precise language (avoid "significant" unless statistically tested)
- Distinguish between statistical and practical significance
- Quantify rather than qualify ("increased by 23%" vs "increased substantially")
- Acknowledge limitations directly

---

## File Naming Conventions

Use git for version control—no version numbers in filenames.

```
src/analysis/[description].py           # Python scripts
src/analysis/[description].R            # R scripts
results/figures/fig[number]_[desc].png  # Figures
results/tables/tbl[number]_[desc].csv   # Tables
notebooks/exploration/[date]_[topic].ipynb  # Notebooks
```

Examples:
- `src/analysis/regression_main.py`
- `src/preprocessing/clean_survey_data.R`
- `results/figures/fig01_descriptive_boxplots.png`
- `results/tables/tbl02_correlation_matrix.csv`
- `notebooks/exploration/2026-01-15_outlier_investigation.ipynb`

---

## Git Commit Messages

Use clear, descriptive commit messages:
```
feat: add multilevel regression analysis
fix: correct standard error calculation in bootstrap
docs: update methods section with effect size rationale
data: add cleaned survey responses (n=342)
```

---

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
