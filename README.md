# WDBC · ERL v2 — Scientific research notebook

**Development-only machine-learning benchmark and probability calibration analysis.**
**Idioma del informe: español.** This notebook is a read-only report, **not** a screening, diagnosis, or clinical decision-support tool.

## Explore the report

- [Research notebook — source, methodology and audit controls](WDBC_ERLV2_Research_Report_v0_1_1.ipynb)
- [Static visual report — HTML preview with figures](preview/WDBC_ERLV2_Research_Report_v0_1_1.html) — download and open locally in a browser. GitHub may display HTML as source rather than rendering the report.

The source `.ipynb` intentionally contains **no executed outputs**. The HTML is a static snapshot of the previously audited report, including visualizations; it is not an interactive application. GitHub's notebook renderer may sanitize embedded HTML/CSS, so its appearance can differ from the HTML preview.

## Static report hosting (GitHub Pages)

This repository includes a **proposed** static GitHub Pages publication under `docs/`. GitHub Pages is **not declared live** until its deployment has been enabled and visually verified by a guest visitor. The static page does not train models, score patients, or download the eight private frozen evidence files.

- [Static landing page source](docs/index.html)
- [Frozen visual report in the Pages source folder](docs/wdbc-report.html)
- [Unchanged original HTML evidence](preview/WDBC_ERLV2_Research_Report_v0_1_1.html)
- [Fail-closed report audit](scripts/verify_static_report.py)

The Pages HTML copy is **byte-identical** to the previously published static visual report. The notebook remains intentionally source-only. Before enabling public hosting, review the Draft PR, confirm all checks and inspect the page layout. After merging, use **Settings > Pages > Build and deployment > Deploy from a branch > main > /docs > Save**. Only when GitHub confirms a successful deployment, the expected address is `https://ehdataai.github.io/healthcare-mlops-benchmark/`. This is a publicly available research report, **not** a clinical or medical-device service.

## Landing v2: evidence-first reading

The static landing under `docs/index.html` uses an editorial sequence: study scope, three methodological questions, two original frozen-figure previews, interpretation guide and explicit validity limits. Its layout adapts to desktop and mobile; fonts and assets are local, with no JavaScript, analytics or third-party tracking. The figure files under `docs/assets/` are extracted **byte-for-byte** from the five PNGs already embedded in the frozen report and validated against those source bytes by CI. The two figures are curated previews, **not** new simulations or results.

A repository-wide `.gitattributes` policy keeps the scientific notebook and HTML in LF encoding during Windows checkout. Static-report QA now runs under both Linux and Windows and rejects changed frozen report bytes, unexpected asset references and active HTML.

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
