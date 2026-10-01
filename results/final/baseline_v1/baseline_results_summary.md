# Binary baseline development results

Seed 42 only. These are development results; final five-seed experiments have not been run. Mean and standard deviation are therefore not estimated.

The frozen baseline_v1 data, chronological membership and fitted preprocessing are unchanged. The training cache reproduces the frozen float64 preprocessing checksum before casting model inputs to float32. Target: 0 benign, 1 malicious. Attack labels are used only for diagnostics.

## Pre-training distribution

| Partition | Benign | Malicious | Total |
|---|---:|---:|---:|
| train | 10,885,643 | 1,909,493 | 12,795,136 |
| validation | 1,583,520 | 69,423 | 1,652,943 |
| test | 998,793 | 375,350 | 1,374,143 |

| Original family | Train | Validation | Test |
|---|---:|---:|---:|
| Benign | 10,885,643 | 1,583,520 | 998,793 |
| Bot | 0 | 0 | 282,310 |
| Brute Force -Web | 249 | 362 | 0 |
| Brute Force -XSS | 79 | 151 | 0 |
| DDOS attack-HOIC | 668,461 | 0 | 0 |
| DDOS attack-LOIC-UDP | 1,730 | 0 | 0 |
| DDoS attacks-LOIC-HTTP | 576,191 | 0 | 0 |
| DoS attacks-GoldenEye | 41,455 | 0 | 0 |
| DoS attacks-Hulk | 434,873 | 0 | 0 |
| DoS attacks-SlowHTTPTest | 19,462 | 0 | 0 |
| DoS attacks-Slowloris | 10,285 | 0 | 0 |
| FTP-BruteForce | 39,352 | 0 | 0 |
| Infilteration | 0 | 68,857 | 93,040 |
| SQL Injection | 34 | 53 | 0 |
| SSH-Bruteforce | 117,322 | 0 | 0 |

Unseen in validation: Infilteration.
Unseen in test: Bot, Infilteration.

## Evaluation

All checkpoint selection uses validation macro-F1 with a fixed probability threshold of 0.5. All four selected models are checksum-locked before any test inference. Test scores do not select configurations. PR-AUC is trapezoidal precision-recall area; average precision is also reported separately. Undefined precision/F1 denominators are assigned zero.

| Model | Partition | Accuracy | Precision | Recall | F1 | Macro-F1 | ROC-AUC | PR-AUC | FPR | FNR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| logistic_regression | validation | 0.891289 | 0.042691 | 0.074140 | 0.054183 | 0.498256 | 0.499304 | 0.041920 | 0.072886 | 0.925860 |
| random_forest | validation | 0.954687 | 0.029710 | 0.002492 | 0.004598 | 0.490707 | 0.497345 | 0.048227 | 0.003568 | 0.997508 |
| xgboost | validation | 0.954226 | 0.111083 | 0.012834 | 0.023010 | 0.499787 | 0.547849 | 0.048368 | 0.004503 | 0.987166 |
| mlp | validation | 0.956969 | 0.163177 | 0.005949 | 0.011480 | 0.494743 | 0.550251 | 0.058612 | 0.001338 | 0.994051 |
| logistic_regression | test | 0.692382 | 0.056918 | 0.008104 | 0.014189 | 0.415973 | 0.551386 | 0.344731 | 0.050464 | 0.991896 |
| random_forest | test | 0.724700 | 0.068673 | 0.000626 | 0.001241 | 0.420794 | 0.832852 | 0.677675 | 0.003191 | 0.999374 |
| xgboost | test | 0.724874 | 0.234846 | 0.003200 | 0.006313 | 0.423323 | 0.553878 | 0.397613 | 0.003918 | 0.996800 |
| mlp | test | 0.726360 | 0.300179 | 0.001343 | 0.002674 | 0.422049 | 0.774968 | 0.512284 | 0.001176 | 0.998657 |

At the fixed threshold, validation malicious recall ranges from 0.25% to 7.41%. Read accuracy together with malicious recall and false-negative counts; it does not summarize attack detection on its own.

At the fixed threshold, test malicious recall ranges from 0.06% to 0.81%. Read accuracy together with malicious recall and false-negative counts; it does not summarize attack detection on its own.

## Infilteration and Bot binary detection

| Model | Partition | Family | Status | Total | Detected | Missed | Detection recall |
|---|---|---|---|---:|---:|---:|---:|
| logistic_regression | validation | Bot | UNSEEN | 0 | 0 | 0 | absent |
| logistic_regression | validation | Infilteration | UNSEEN | 68,857 | 4,998 | 63,859 | 0.072585 |
| logistic_regression | test | Bot | UNSEEN | 282,310 | 0 | 282,310 | 0.000000 |
| logistic_regression | test | Infilteration | UNSEEN | 93,040 | 3,042 | 89,998 | 0.032696 |
| random_forest | validation | Bot | UNSEEN | 0 | 0 | 0 | absent |
| random_forest | validation | Infilteration | UNSEEN | 68,857 | 137 | 68,720 | 0.001990 |
| random_forest | test | Bot | UNSEEN | 282,310 | 0 | 282,310 | 0.000000 |
| random_forest | test | Infilteration | UNSEEN | 93,040 | 235 | 92,805 | 0.002526 |
| xgboost | validation | Bot | UNSEEN | 0 | 0 | 0 | absent |
| xgboost | validation | Infilteration | UNSEEN | 68,857 | 719 | 68,138 | 0.010442 |
| xgboost | test | Bot | UNSEEN | 282,310 | 0 | 282,310 | 0.000000 |
| xgboost | test | Infilteration | UNSEEN | 93,040 | 1,201 | 91,839 | 0.012908 |
| mlp | validation | Bot | UNSEEN | 0 | 0 | 0 | absent |
| mlp | validation | Infilteration | UNSEEN | 68,857 | 240 | 68,617 | 0.003485 |
| mlp | test | Bot | UNSEEN | 282,310 | 0 | 282,310 | 0.000000 |
| mlp | test | Infilteration | UNSEEN | 93,040 | 504 | 92,536 | 0.005417 |

These results measure binary detection. Successful detection of a family absent from training is neither multiclass classification nor proof of zero-day detection. Absent families have no recall estimate.

## Resource measurements

runtime_metrics.csv reports fitting time separately from validation selection and total training-stage time. Inference includes batched loading and frozen preprocessing; prediction-only time is also supplied. Latency is amortized milliseconds per 1,000 records. Peak memory is worker RSS/Windows peak working set, including imported libraries and data; model size is the serialized artifact size. Training measurements repeated on validation/test rows refer to the same fit.

## Reproducibility and development limits

Run `python -m src.phase4.run` from the repository using the documented workspace-local runtime. Completed model stages are reused only when their configuration and artifact hashes match. An interrupted model stage restarts that model; this is not a mid-epoch recovery mechanism.

Logistic regression uses SGDClassifier with logistic loss, L2 regularization and incremental fitting. MLP uses weighted incremental Adam fitting. Every epoch visits every training row; optimizer shuffling stays inside the fixed training partition. Random Forest uses the full training pool with a capped bootstrap draw per tree. XGBoost uses a quantile matrix and CPU histogram trees. All models use training-derived class/sample weighting. No validation/test oversampling occurs.

Exact hyperparameters and checkpoint budgets are in configs/phase4_seed42.json. Per-model selection histories, environment versions, executed and selected steps, timing and model hashes are persisted in metrics/. Configuration/model locks are in development_configs_frozen.json. These bounded development configurations are not an exhaustive search.

Final seeds 42, 123, 456, 789 and 1024 remain deferred. After final configuration freeze, all final runs must be executed before reporting mean ± standard deviation. Do not select further configurations using these test results.

![Confusion matrices](figures/confusion_matrices_seed42.png)

## Measured runtime

| Model | Partition | Fit seconds | Inference seconds | ms / 1,000 | Peak GiB | Model MiB |
|---|---|---:|---:|---:|---:|---:|
| logistic_regression | validation | 65.19 | 10.30 | 6.231 | 4.342 | 0.0014 |
| logistic_regression | test | 65.19 | 7.67 | 5.583 | 4.342 | 0.0014 |
| random_forest | validation | 399.23 | 12.99 | 7.860 | 4.953 | 0.7533 |
| random_forest | test | 399.23 | 12.54 | 9.123 | 4.953 | 0.7533 |
| xgboost | validation | 324.43 | 9.80 | 5.927 | 6.838 | 0.1163 |
| xgboost | test | 324.43 | 8.71 | 6.338 | 6.838 | 0.1163 |
| mlp | validation | 98.01 | 9.01 | 5.453 | 4.341 | 0.1117 |
| mlp | test | 98.01 | 7.33 | 5.334 | 4.341 | 0.1117 |
