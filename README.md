# Cloud Intrusion Detection under Distribution Shift

This repository contains the code, experiment specifications, reproducibility
documentation, and derived results supporting the manuscript:

**“Evaluating Graph, Temporal, and Anomaly Learning for Cloud Intrusion Detection under Distribution Shift.”**

The study evaluates whether increasingly complex intrusion-detection approaches
provide reproducible incremental value under chronological and attack-family
distribution shift. The experiments compare conventional supervised flow
classifiers, endpoint graph learning, explicit temporal context, benign-trained
reconstruction, and simple decision-level fusion on the CSE-CIC-IDS2018 dataset.

Rather than proposing a single integrated architecture, the study evaluates
individual components using matched controls, frozen experimental protocols,
validation-selected operating points, and five fixed training seeds.

## Methodology

See the [preparation methodology](docs/methodology/BASELINE_PIPELINE.md),
[frozen protocol](experiments/final_spec/README.md), and
[metric definitions](experiments/final_spec/metric_definitions.md).

### Research questions

The experimental design addresses six research questions:

- **RQ1:** How do supervised flow-based classifiers perform under chronological
  train, validation, and test partitions?
- **RQ2:** How well do frozen models detect attack families absent from the
  training partition, specifically Bot and Infilteration?
- **RQ3:** What incremental contribution does relational message passing provide
  over matched edge-only and self-only controls on the February 20 endpoint-graph
  benchmark?
- **RQ4:** Does longer explicit temporal context provide incremental predictive
  value over matched minimal-context controls?
- **RQ5:** Does benign-trained reconstruction provide complementary detection
  behavior relative to the supervised baseline, and does simple RF-AE fusion
  improve detection without an unfavorable false-positive tradeoff?
- **RQ6:** What computational overhead accompanies the evaluated model
  components?

Three principles guide the evaluation:

1. Threshold-free ranking metrics and thresholded operating-point metrics are
   reported separately.
2. Component contributions are evaluated using matched controls and within-seed
   differences rather than inferred from absolute performance alone.
3. Variation across five fixed seeds represents training stochasticity on a
   fixed dataset split, not uncertainty across independently sampled datasets.

The final reruns use previously observed fixed splits. They are not a new
untouched confirmatory holdout.

### Dataset

The study uses the **CSE-CIC-IDS2018** intrusion-detection benchmark.

The experimental inventory contains ten processed machine-learning CSV files
used for the principal flow experiments. Before cleaning, these files contain
approximately **16.23 million records**, including approximately **13.48 million
benign** and **2.75 million malicious** records.

The original dataset is not redistributed through this repository.
Reviewers must acquire the ten CSE-CIC-IDS2018 processed machine-learning CSV
files separately. The [dataset inventory](results/dataset_summary.csv) identifies
the source files; the [historical acquisition and audit guide](archive/docs/history/phase1_audit_history.md)
describes local placement. Derived caches, predictions and model checkpoints
are also omitted from this document-only artifact.

The data-quality audit identified:

| Finding | Result |
|---|---:|
| Raw records | 16,233,002 |
| Explicit NaN cells | 59,721 |
| Infinite cells | 131,799 |
| Repeated-header records | 59 |
| Non-header exact duplicates removed | 410,707 |
| Year-1970 timestamp anomalies | 14 |

Infinite values are converted to missing values, affected numerical features are
imputed using training-fitted statistics, repeated headers and exact duplicates
are removed, and the 14 anomalous year-1970 records are quarantined from
temporal experiments.

The dataset spelling **`Infilteration`** is intentionally preserved throughout
the project.

### Experimental Cohorts

The study deliberately separates chronological generalization from graph and
temporal component evaluation.

| Cohort | Train / Validation / Test | Purpose |
|---|---|---|
| **Full chronological dataset** | 12,795,136 / 1,652,943 / 1,374,143 | Supervised flow models, anomaly detection, RF-AE fusion, and later-period attack-family analysis |
| **Phase-5 matched temporal cohort** | 99,962 / 206,603 / 171,753 | Transformer-L64 versus capacity-matched Transformer-L1 |
| **February-20 matched graph cohort** | 172,984 / 88,782 / 212,591 | GATv2, edge-MLP, self-only GAT, and graph-temporal comparisons |

Results from these cohorts should **not** be interpreted as interchangeable
component ablations.

### Chronological Full-Data Split

The principal flow experiment preserves chronological ordering.

| Partition | Dates | Benign | Malicious | Total |
|---|---|---:|---:|---:|
| Train | Feb. 14–22, 2018 | 10,885,643 | 1,909,493 | 12,795,136 |
| Validation | Feb. 23 & 28, 2018 | 1,583,520 | 69,423 | 1,652,943 |
| Test | Mar. 1–2, 2018 | 998,793 | 375,350 | 1,374,143 |

All malicious test records belong to two attack families absent from training:

- **Bot:** 282,310 test records
- **Infilteration:** 93,040 test records

Bot is absent from both training and validation.

Infilteration is absent from training but appears in validation. It is therefore
**training-unseen**, but not fully development-held-out.

These are benchmark measurements of attack-family distribution shift.

### Evaluated Models

#### Supervised flow models

The full-data supervised evaluation includes:

- Logistic Regression (LR)
- Random Forest (RF)
- XGBoost (XGB)
- Multilayer Perceptron (MLP)

All final models are evaluated using five fixed training seeds: 42, 123, 456, 789, and 1024.

The endpoint graph model is **GATv2**, with **Edge MLP** and **Self-only GAT** controls on the February-20 **Benign versus DDoS attacks-LOIC-HTTP** benchmark. Temporal comparisons are **Transformer-L1 versus Transformer-L64** on the Phase-5 matched cohort and **graph-temporal L1 versus L8** on the February-20 cohort. The graph-temporal heads reuse a same-seed frozen graph encoder.

The anomaly model is a **benign-trained autoencoder using shared preprocessing fitted on the complete training partition**. Preprocessing is frozen and is not refitted per seed or on validation/test records. Final fusion is **same-seed RF + AE OR decision fusion**. Earlier development calibration and fusion variants are historical experiments, not substitutes for this frozen comparison. Explainability was outside the completed evaluation.

Threshold rules are frozen in the [experimental specification](experiments/final_spec/final_experiment_spec.json).
Numeric thresholds are selected separately for each seed using only the relevant
validation cohort, then frozen before test evaluation. Supervised comparisons
include fixed 0.5 and validation-FPR operating points; matched component tables
also report validation maximum macro-F1. AE uses benign-only validation
calibration, with a primary 1% false-positive cap. Final OR fusion combines the
same-seed RF and AE decisions at their component 1% validation operating points.
Neither validation caps nor those component caps guarantee a 1% test or OR-union
false-positive rate. The retained per-seed tables record selected thresholds.

## Results

The tables below provide the final five-seed results and matched comparisons supporting the manuscript.

| Evidence | Phase 11A: full and matched temporal cohorts | Phase 11B: February-20 graph cohort |
|---|---|---|
| Completion | [Phase 11A report](results/final/phase11a/PHASE_11A_EXECUTION_SUMMARY.md) | [Phase 11B report](results/final/phase11b/PHASE_11B_EXECUTION_SUMMARY.md) |
| Per-seed metrics | [Metrics](results/final/phase11a/per_seed_metrics.csv) | [Metrics](results/final/phase11b/per_seed_metrics.csv) |
| Mean and sample SD | [Five-seed aggregate](results/final/phase11a/five_seed_mean_sample_sd.csv) | [Aggregate](results/final/phase11b/aggregate_metrics.csv) |
| Paired comparisons | [Temporal differences](results/final/phase11a/paired_mean_sample_sd.csv) | [Component differences](results/final/phase11b/paired_aggregate_differences.csv) |
| Family results | [Family metrics](results/final/phase11a/per_seed_family_metrics.csv) | [Family metrics](results/final/phase11b/per_seed_family_metrics.csv) |
| Runtime | [Runtime](results/final/phase11a/runtime.csv) | [Runtime](results/final/phase11b/runtime_metrics.csv) |
| Integrity | [Final verification record](results/final/phase11a/audit/final_verification.json) | [Integrity report](results/final/phase11b/integrity_report.md) |

Additional evidence: [Bot/Infilteration diagnostics](results/final/phase11a/bot_infilteration_diagnostics.csv), [RF/AE/OR comparison](results/final/phase11a/rf_ae_or_comparison.csv), and [RF/AE overlap](results/final/phase11a/rf_ae_overlap.csv).

The [figures](results/figures/) include PDF, PNG, and SVG versions, with
[plotted values](results/figures/plotted_values.csv) and
[input provenance](results/figures/provenance.json).

## Reproduction and availability

1. Obtain the ten processed CSE-CIC-IDS2018 CSV files listed in the
   [dataset inventory](results/dataset_summary.csv).
2. Consult the [preparation guide](docs/methodology/BASELINE_PIPELINE.md) and
   [recorded environment](docs/reproducibility/ENVIRONMENT.md) for data preparation,
   package versions, and execution prerequisites.
3. Use the [frozen run plan](experiments/final_spec/final_run_plan.md) and
   [experiment specification](experiments/final_spec/final_experiment_spec.json)
   to identify the cohorts, models, seeds, and validation rules for each comparison.

Research implementations are in [src/](src/); the final specifications are in
[experiments/final_spec/](experiments/final_spec/), and reported results are in
[results/final/](results/final/). The [artifact manifest](docs/reproducibility/final_artifacts.csv)
records the bundled evidence and checksums.

To verify bundled artifact hashes, figure input provenance, and documentation
links, run this read-only check from the repository root:

```shell
python -B scripts/verification/verify_release.py
```

This check uses only the Python standard library. It does not run models or
recalculate metrics.

Raw data, derived arrays, saved predictions, model checkpoints, and package
overlays are not bundled. The checkout supports inspection of reported evidence;
it is not a self-contained executable reproduction package. Research runners and
the plotter retain historical path assumptions and require adaptation before
reuse. A fresh-environment end-to-end reproduction has not been verified.

## Limitations

- The study uses one benchmark dataset and fixed splits previously examined during
  development. Final reruns are not a new untouched confirmatory holdout.
- Five-seed sample standard deviations describe training variability on those
  splits, not uncertainty across independently sampled datasets.
- Full-data, matched temporal, and February-20 graph results use distinct cohorts.
  The graph benchmark covers Benign versus DDoS attacks-LOIC-HTTP on one day.
- Bot is absent from training and validation; Infilteration is absent from training
  but appears in validation. These results measure attack-family distribution
  shift and do not establish general zero-day detection.
- Validation-selected false-positive caps do not guarantee the same test FPR or
  the FPR of OR fusion. Runtime comparisons require matching cohorts and stages.
- Explainability was outside the completed evaluation.

## License

The repository code is available under the [MIT License](LICENSE).
The CSE-CIC-IDS2018 dataset is distributed separately under its own terms.
