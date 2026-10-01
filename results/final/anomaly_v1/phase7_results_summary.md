# Phase 7 seed-42 anomaly branch results

Selected autoencoder: **autoencoder_B**, hidden layers [128, 32, 128], epoch 3, benign-validation MSE 0.114440833. Both candidate architectures visited all **10,885,643 benign TRAIN records in every executed epoch**, with no AE subsampling. Architecture and checkpoint selection minimized benign-validation reconstruction error; no malicious validation scores selected the representation.

The frozen baseline_v1 chronological split, preprocessing, feature definitions and labels were reused exactly. TRAIN spans Feb 14–22, validation Feb 23 and Feb 28, and test Mar 1–2. No Phase 4/4A/5/6 artifacts were modified. Seed 42 is development only; no statistical significance or final multi-seed result is claimed.

## Primary benign-only calibration (Protocol A)

Thresholds use only benign validation scores at empirical FPR caps 5%, 1%, 0.5% and 0.1%. Tied scores are handled conservatively using an upper order statistic and the next representable greater value, with detection defined as score ≥ threshold. Every Protocol-A threshold was frozen before malicious validation/test scoring. These are empirical validation caps, not a guarantee of test/population FPR.

| model | criterion | recall | precision | f1 | macro_f1 | false_positive_rate | false_negative_rate | roc_auc | pr_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| autoencoder_B | benign_fpr_at_most_0.05 | 0.045246 | 0.266705 | 0.077367 | 0.450980 | 0.046750 | 0.954754 | 0.653807 | 0.395266 | 0.395369 |
| autoencoder_B | benign_fpr_at_most_0.01 | 0.007934 | 0.251818 | 0.015383 | 0.426963 | 0.008859 | 0.992066 | 0.653807 | 0.395266 | 0.395369 |
| autoencoder_B | benign_fpr_at_most_0.005 | 0.002414 | 0.167840 | 0.004759 | 0.422352 | 0.004497 | 0.997586 | 0.653807 | 0.395266 | 0.395369 |
| autoencoder_B | benign_fpr_at_most_0.001 | 0.000314 | 0.128400 | 0.000627 | 0.421049 | 0.000802 | 0.999686 | 0.653807 | 0.395266 | 0.395369 |
| isolation_forest | benign_fpr_at_most_0.05 | 0.008778 | 0.066590 | 0.015512 | 0.417752 | 0.046243 | 0.991222 | 0.417151 | 0.230016 | 0.259323 |
| isolation_forest | benign_fpr_at_most_0.01 | 0.001686 | 0.062071 | 0.003284 | 0.420320 | 0.009577 | 0.998314 | 0.417151 | 0.230016 | 0.259323 |
| isolation_forest | benign_fpr_at_most_0.005 | 0.000930 | 0.066236 | 0.001834 | 0.420686 | 0.004926 | 0.999070 | 0.417151 | 0.230016 | 0.259323 |
| isolation_forest | benign_fpr_at_most_0.001 | 0.000136 | 0.054662 | 0.000271 | 0.420839 | 0.000883 | 0.999864 | 0.417151 | 0.230016 | 0.259323 |

## Test attack families absent from TRAIN

| model | criterion | attack_family | N | detected | missed | recall |
| --- | --- | --- | --- | --- | --- | --- |
| autoencoder_B | benign_fpr_at_most_0.05 | Bot | 282310 | 5322 | 276988 | 0.018852 |
| autoencoder_B | benign_fpr_at_most_0.05 | Infilteration | 93040 | 11661 | 81379 | 0.125333 |
| autoencoder_B | benign_fpr_at_most_0.01 | Bot | 282310 | 181 | 282129 | 0.000641 |
| autoencoder_B | benign_fpr_at_most_0.01 | Infilteration | 93040 | 2797 | 90243 | 0.030062 |
| autoencoder_B | benign_fpr_at_most_0.005 | Bot | 282310 | 163 | 282147 | 0.000577 |
| autoencoder_B | benign_fpr_at_most_0.005 | Infilteration | 93040 | 743 | 92297 | 0.007986 |
| autoencoder_B | benign_fpr_at_most_0.001 | Bot | 282310 | 78 | 282232 | 0.000276 |
| autoencoder_B | benign_fpr_at_most_0.001 | Infilteration | 93040 | 40 | 93000 | 0.000430 |
| isolation_forest | benign_fpr_at_most_0.05 | Bot | 282310 | 8 | 282302 | 0.000028 |
| isolation_forest | benign_fpr_at_most_0.05 | Infilteration | 93040 | 3287 | 89753 | 0.035329 |
| isolation_forest | benign_fpr_at_most_0.01 | Bot | 282310 | 0 | 282310 | 0.000000 |
| isolation_forest | benign_fpr_at_most_0.01 | Infilteration | 93040 | 633 | 92407 | 0.006804 |
| isolation_forest | benign_fpr_at_most_0.005 | Bot | 282310 | 0 | 282310 | 0.000000 |
| isolation_forest | benign_fpr_at_most_0.005 | Infilteration | 93040 | 349 | 92691 | 0.003751 |
| isolation_forest | benign_fpr_at_most_0.001 | Bot | 282310 | 0 | 282310 | 0.000000 |
| isolation_forest | benign_fpr_at_most_0.001 | Infilteration | 93040 | 51 | 92989 | 0.000548 |

Bot and Infilteration are absent from the original TRAIN partition. They are reported as unseen attack families, not zero-day attacks. KNOWN/UNSEEN in validation diagnostics refers to presence in the full frozen TRAIN partition; the anomaly estimators themselves fit only benign rows. Benign diagnostic detection counts mean false alarms, with benign FPR reported instead of malicious-family recall.

## Label-aware calibration (Protocol B; comparison only)

Protocol B selects maximum macro-F1 and maximum binary F1 from scored validation records and their labels. Infilteration appears in this calibration, so these are **not strict development-held-out Infilteration results**. Test labels never selected thresholds. Protocol B did not change the autoencoder architecture or model weights.

| model | criterion | recall | precision | f1 | macro_f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| autoencoder_B | maximum_macro_f1 | 0.021995 | 0.306721 | 0.041047 | 0.438309 | 0.018684 | 0.653807 | 0.395369 |
| autoencoder_B | maximum_binary_f1 | 0.432743 | 0.622690 | 0.510624 | 0.681607 | 0.098541 | 0.653807 | 0.395369 |
| isolation_forest | maximum_macro_f1 | 0.006333 | 0.076426 | 0.011696 | 0.420082 | 0.028760 | 0.417151 | 0.259323 |
| isolation_forest | maximum_binary_f1 | 0.061495 | 0.093787 | 0.074283 | 0.401893 | 0.223300 | 0.417151 | 0.259323 |

## Comparison at validation-calibrated 1% FPR

| model | actual_test_fpr | aggregate_malicious_recall | precision | f1 | AP | Bot_recall | Infilteration_recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| autoencoder_B | 0.008859 | 0.007934 | 0.251818 | 0.015383 | 0.395369 | 0.000641 | 0.030062 |
| isolation_forest | 0.009577 | 0.001686 | 0.062071 | 0.003284 | 0.259323 | 0.000000 | 0.006804 |
| logistic_regression | 0.007876 | 0.001154 | 0.052175 | 0.002257 | 0.345175 | 0.000000 | 0.004654 |
| random_forest | 0.008302 | 0.342744 | 0.939448 | 0.502250 | 0.677160 | 0.449612 | 0.018476 |
| xgboost | 0.008595 | 0.005563 | 0.195634 | 0.010818 | 0.531589 | 0.000000 | 0.022442 |
| mlp | 0.007696 | 0.004907 | 0.193305 | 0.009572 | 0.512740 | 0.000000 | 0.019798 |

Anomaly rows use **benign-only Protocol A**. Supervised rows reuse the existing **label-aware Phase 4A thresholds** and frozen Phase 4 predictions, selected to maximize validation recall under a 1% validation FPR constraint. These calibration protocols are different and should not be presented as equivalent. Every row evaluates exactly the full same test membership; Phase 4 was not retrained and Phase 5 sampled cohorts were not substituted. Actual test FPR, not the validation target alone, determines whether a method controls false alarms after temporal transfer.

## Score distributions and runtime

| model | group | N | mean | median | p75 | p90 | p95 | p99 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| autoencoder_B | Train benign | 10885643 | 0.014877 | 0.001418 | 0.005897 | 0.019384 | 0.032956 | 0.086429 | 30949.346576 |
| autoencoder_B | Validation Benign | 1583520 | 0.114441 | 0.001481 | 0.005379 | 0.016158 | 0.036910 | 0.298963 | 139592.524560 |
| autoencoder_B | Validation Infilteration | 68857 | 0.036171 | 0.001463 | 0.009279 | 0.051626 | 0.292894 | 0.453234 | 8.665242 |
| autoencoder_B | Test Benign | 998793 | 0.049757 | 0.001326 | 0.003929 | 0.012742 | 0.034202 | 0.296433 | 32635.068665 |
| autoencoder_B | Test Infilteration | 93040 | 0.049571 | 0.003323 | 0.008341 | 0.068273 | 0.291923 | 0.301876 | 621.959001 |
| autoencoder_B | Test Bot | 282310 | 0.010496 | 0.016711 | 0.016790 | 0.016791 | 0.016791 | 0.055225 | 4.144717 |
| isolation_forest | Train benign | 10885643 | 0.405431 | 0.388826 | 0.426158 | 0.502280 | 0.561475 | 0.623464 | 0.752673 |
| isolation_forest | Validation Benign | 1583520 | 0.411125 | 0.388499 | 0.429602 | 0.545807 | 0.564453 | 0.633539 | 0.744674 |
| isolation_forest | Validation Infilteration | 68857 | 0.407467 | 0.385149 | 0.431650 | 0.504596 | 0.554859 | 0.623042 | 0.740084 |
| isolation_forest | Test Benign | 998793 | 0.408984 | 0.391106 | 0.424564 | 0.542377 | 0.564059 | 0.631386 | 0.754203 |
| isolation_forest | Test Infilteration | 93040 | 0.400908 | 0.377292 | 0.425147 | 0.501259 | 0.551531 | 0.621667 | 0.731368 |
| isolation_forest | Test Bot | 282310 | 0.380538 | 0.410759 | 0.413368 | 0.413501 | 0.413880 | 0.414985 | 0.598275 |

Histogram and ECDF figures show log10(1 + raw score) for readability; metrics and thresholds always use raw scores. AE scores are per-record feature-mean reconstruction MSE; Isolation Forest uses negative score_samples so larger values mean greater anomaly. Scores are not malicious probabilities. PR-AUC is trapezoidal precision-recall area; AP is reported separately. Train-benign distributions use all benign TRAIN records for both models, even though Isolation Forest was fitted on a sample.

Benign calibration scores are retained exactly in the full validation score array after an exact checkpoint replay using the original batch layout. Small float32 reconstruction differences from mixed-partition batch layouts are checked and recorded in scoring manifests; they do not change the frozen thresholds.

Isolation Forest fit on a deterministic seed-42 uniform sample of 250,000 benign TRAIN records without replacement. It uses 100 trees with 256 records per tree; 24,358 distinct sampled records participated across trees. Sampling limits memory and CPU use; sample IDs and hashes are saved. No validation/test row enters fitting.

Runtime tables separate training, benign-validation scoring/selection, inference, prediction-only compute and milliseconds per 1,000 scored records. End-to-end validation/test inference includes frozen transformation and checksum verification; training-benign scoring reads the existing verified feature cache. Peak memory is process high-water RSS/working set, and serialized size is checkpoint bytes. Training values repeat by scoring partition and must not be summed repeatedly. AE scoring includes conversion of reconstruction differences to float64 before averaging; training uses float32 MSE and AdamW with gradient clipping at 10.

## Interpretation limits

The four-epoch budget is deliberately bounded. Frozen preprocessing was originally fitted on all TRAIN classes, including known malicious traffic, as required by the unchanged baseline protocol; only anomaly-model fitting is benign-only. Thus this is a benign-trained anomaly branch on a shared frozen representation, not a wholly benign-fitted preprocessing pipeline. Benign labels are necessarily used to identify fitting and calibration cohorts, but neither binary nor family labels enter the model input or reconstruction objective.

Protocol A keeps Infilteration malicious scores/labels out of representation selection and threshold fitting. Protocol B explicitly uses validation Infilteration labels. Prior phases have already exposed this test cohort, so these development results are not a fresh confirmatory test or proof of general unseen-threat detection. The optional temporal autoencoder was deferred. No graph model, graph+temporal integration, explainability, risk fusion or full AIGT-CTD was introduced. Work stops after this seed-42 Phase 7.
