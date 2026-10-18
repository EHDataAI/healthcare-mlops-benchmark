# WDBC · ERL v2 — Scientific research notebook

**Development-only machine-learning benchmark and probability calibration analysis.**
**Idioma del informe: español.** This notebook is a read-only report, **not** a screening, diagnosis, or clinical decision-support tool.

## Explore the report

- [Research notebook — source, methodology and audit controls](WDBC_ERLV2_Research_Report_v0_1_1.ipynb)
- [Static visual report — HTML preview with figures](preview/WDBC_ERLV2_Research_Report_v0_1_1.html) — download and open locally in a browser. GitHub may display HTML as source rather than rendering the report.

The source `.ipynb` intentionally contains **no executed outputs**. The HTML is a static snapshot of the previously audited report, including visualizations; it is not an interactive application. GitHub's notebook renderer may sanitize embedded HTML/CSS, so its appearance can differ from the HTML preview.

## Scope and scientific design

The **Wisconsin Diagnostic Breast Cancer (WDBC)** dataset contains 569 records and 30 numeric morphometric features derived from **fine-needle aspirate (FNA)** images. It is **not a mammography dataset**. Malignant is encoded as the positive class (`1`).

The analysis uses **455 development records** with five outer cross-validation folds. It reports a seven-family exploratory benchmark (ERL-02D/03B) and a paired **RAW versus SIGMOID** calibration study for logistic regression and CatBoost (ERL-03C), using out-of-fold predictions and the Brier score, log-loss, and classification-error summaries.

The original **114-record historical holdout was previously examined**, and therefore is **excluded** from this report; it is not presented as a new independent test or external validation set. The illustrative malignant sensitivity target of **95%** governs an internal threshold-selection objective, not a guaranteed sensitivity on new patients or in any clinical setting.

In the development-only comparison, sigmoid calibration slightly improved the logistic-regression Brier score and log-loss, but worsened those scores for CatBoost. These are descriptive findings on the same development data: they do **not** establish statistical superiority, clinical utility, generalizability, or regulatory compliance.

## Reproducibility boundary

The notebook **does not download data, fit models or regenerate experiments**. Before creating figures, it checks the SHA256 fingerprints of **eight previously frozen JSON/CSV evidence files** from ERL-02, ERL-03B and ERL-03C. The corresponding original experiment artifacts are **not distributed** in this minimal public release.

Consequently:

1. You can inspect the notebook code, methods, reporting logic and the published static HTML without those files.
2. **A fresh clone alone cannot execute the notebook end-to-end.** Re-execution requires the exact eight original evidence files, their original paths, a compatible Python scientific environment and successful SHA256 validation.
3. For authorized local re-execution, configure `HEALTHCARE_MLOPS_WORK` to the directory holding the frozen `results/erl02`, `results/erl03b` and `results/erl03c` trees. The notebook intentionally fails closed if a source is missing or altered.
4. The historical holdout is not used by this reporting notebook. A fresh research benchmark, external validation, or model deployment requires a separate approved protocol.

## Validation status and limits

The r2 notebook passed the full local Ruff configuration and the Windows release test suite (**12 tests, 0 failures, 0 errors, 0 skips**), with a recorded JUnit XML and integrity checks on the frozen inputs. A Gitleaks working-tree scan reported no findings before publication preparation. These checks establish **local engineering QA**, not third-party replication or clinical validation.

The eight original scientific inputs, the QA history, negative tests and signed release process are managed separately from this minimal public artifact. No patient-level predictions, training exports, local environment credentials, or internal QA directories are intentionally included here.

**Use restriction:** educational and methodological research only; no diagnostic, triage, treatment, patient-selection or medical-device use.

## Version

Notebook design edition `0.1.1`; controlled Ruff hotfix `r2`; Engineering Reasoning Loop (ERL) v2. The hotfix preserved the scientific interpretation and corrected style/static-analysis issues. Detailed ERL-03D/MLflow work belongs to a separate future experiment, not a prerequisite for this publication.
