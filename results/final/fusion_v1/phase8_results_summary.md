# Phase 8 supervised + anomaly risk-fusion development experiment

Seed 42 only. Frozen Phase-4 RF probabilities and Phase-7 autoencoder_B reconstruction MSE; no retraining. All validation/test rows use the original baseline_v1 membership and order.

## Transformations and calibration

A_norm = count(benign validation AE scores <= current score) / N, with N = 1583520. This right-continuous empirical CDF uses only benign validation observations, includes ties at their upper rank, maps below-minimum values to 0 and above-maximum values to 1. It is validation-dependent by the requested protocol, not a train/validation-independent transformation or a calibrated malicious probability. RF probabilities remain unchanged. Raw AE scores are retained for standalone thresholds and OR decisions.

MAX and weighted alpha 0.25/0.50/0.75 are all reported. Protocol A uses benign-only validation order-statistic thresholds at 5%, 1%, 0.5%, 0.1%, with >= detection and nextafter tie handling. Normalization and calibration reuse the same benign sample; caps are empirical, not population/test guarantees. Standalone RF is additionally recalibrated benign-only in the complete metric tables. Protocol B selects maximum validation macro-F1 for each score rule, ties favoring the highest threshold; this uses Infilteration labels and is non-strict. Neither protocol selects a winning method or alpha from test outcomes. Locks were saved before this run loaded test scores/labels.

OR reuses frozen Phase-4A label-aware RF and Phase-7 benign-only AE thresholds at paired 1%, 0.5%, 0.1% caps. No saved 5% RF operating threshold exists, so no 5% OR threshold was invented. OR is a mixed-protocol comparator, not benign-only Protocol A. Two component caps do not impose the same cap on their union. OR ranking metrics use its binary decision (a coarse two-level ranking); its AP is not directly equivalent to continuous-score AP.

## Critical 1% comparison

RF alone uses its frozen Phase-4A threshold; AE alone uses its frozen Phase-7 Protocol-A threshold. The four score fusions use new benign-only validation thresholds. OR uses the two frozen component thresholds.

| method | protocol | actual_test_fpr | aggregate_malicious_recall | precision | f1 | AP | Bot_recall | Infilteration_recall | ranking_basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random_forest | frozen_existing | 0.008302 | 0.342744 | 0.939448 | 0.502250 | 0.677160 | 0.449612 | 0.018476 | continuous score |
| autoencoder | frozen_existing | 0.008859 | 0.007934 | 0.251818 | 0.015383 | 0.395369 | 0.000641 | 0.030062 | continuous score |
| max | A_benign_only | 0.008860 | 0.007937 | 0.251860 | 0.015388 | 0.401314 | 0.000641 | 0.030073 | continuous score |
| weighted_0.25 | A_benign_only | 0.008491 | 0.012719 | 0.360166 | 0.024570 | 0.411515 | 0.000007 | 0.051290 | continuous score |
| weighted_0.50 | A_benign_only | 0.008653 | 0.009010 | 0.281247 | 0.017461 | 0.434207 | 0.000007 | 0.036328 | continuous score |
| weighted_0.75 | A_benign_only | 0.008593 | 0.006477 | 0.220719 | 0.012584 | 0.599550 | 0.000007 | 0.026107 | continuous score |
| or | frozen_existing | 0.016747 | 0.350241 | 0.887125 | 0.502208 | 0.488191 | 0.450253 | 0.046776 | binary decision |

Changes versus frozen RF (fractions, not percentage points):

| method | delta_actual_test_fpr | delta_aggregate_malicious_recall | delta_Bot_recall | delta_Infilteration_recall |
| --- | --- | --- | --- | --- |
| max | 0.000558 | -0.334808 | -0.448971 | 0.011597 |
| weighted_0.25 | 0.000189 | -0.330025 | -0.449605 | 0.032814 |
| weighted_0.50 | 0.000351 | -0.333734 | -0.449605 | 0.017853 |
| weighted_0.75 | 0.000291 | -0.336267 | -0.449605 | 0.007631 |
| or | 0.008445 | 0.007497 | 0.000641 | 0.028300 |

max: Bot recall 0.064% versus RF 44.961%; Infilteration recall 3.007% versus 1.848%; actual FPR 0.886% versus 0.830%. These family and false-alarm changes must be considered together.

weighted_0.25: Bot recall 0.001% versus RF 44.961%; Infilteration recall 5.129% versus 1.848%; actual FPR 0.849% versus 0.830%. These family and false-alarm changes must be considered together.

weighted_0.50: Bot recall 0.001% versus RF 44.961%; Infilteration recall 3.633% versus 1.848%; actual FPR 0.865% versus 0.830%. These family and false-alarm changes must be considered together.

weighted_0.75: Bot recall 0.001% versus RF 44.961%; Infilteration recall 2.611% versus 1.848%; actual FPR 0.859% versus 0.830%. These family and false-alarm changes must be considered together.

or: Bot recall 45.025% versus RF 44.961%; Infilteration recall 4.678% versus 1.848%; actual FPR 1.675% versus 0.830%. These family and false-alarm changes must be considered together.

## Complementary detection behavior

Frozen component 1% operating points; Jaccard = both / (RF only + AE only + both), undefined for an empty union.

| attack_family | N | rf_only | ae_only | both | neither | jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| Bot | 282310 | 126930 | 181 | 0 | 155199 | 0.000000 |
| Infilteration | 93040 | 1555 | 2633 | 164 | 88688 | 0.037684 |

## Interpretation of the operating-point tradeoffs

At these predeclared 1% operating points, the score-fusion rules do not show an overall improvement over frozen RF: their aggregate recall and F1 are lower. Weighted fusion improves Infilteration recall but sacrifices nearly all Bot detection. MAX behaves almost like the AE alone. The percentile transform places ordinary benign AE observations across [0,1], while RF probabilities have a different distribution; sharing numerical bounds does not give the two signals equal calibration. OR preserves RF detections and adds complementary AE detections, but approximately doubles actual FPR and does not improve F1. The evidence supports complementary detection behavior, not superiority under comparable false-alarm control. These observations do not select a winning method or alpha.

## Score relationships

Pearson and Spearman use every record in each group, with average ranks for ties. Figures use a deterministic seed-42 sample of at most 30,000 rows per group only for display.

| partition | group | N | anomaly_signal | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| validation | Benign | 1583520 | raw_ae | 0.004220 | 0.292755 |
| validation | Benign | 1583520 | normalized_ae | 0.108465 | 0.292755 |
| validation | Infilteration | 68857 | raw_ae | 0.393725 | 0.450237 |
| validation | Infilteration | 68857 | normalized_ae | 0.279048 | 0.450238 |
| test | Benign | 998793 | raw_ae | 0.005864 | 0.293667 |
| test | Benign | 998793 | normalized_ae | 0.123117 | 0.293667 |
| test | Bot | 282310 | raw_ae | -0.256281 | -0.695887 |
| test | Bot | 282310 | normalized_ae | -0.989018 | -0.696643 |
| test | Infilteration | 93040 | raw_ae | 0.037409 | 0.645138 |
| test | Infilteration | 93040 | normalized_ae | 0.310261 | 0.645138 |

## Scope and outputs

Complete validation/test tables include accuracy, precision, recall, F1, macro-F1, FPR, FNR, ROC-AUC, trapezoidal PR-AUC, AP and confusion counts. family_metrics.csv reports counts and recall for each present malicious family and every operating point. Figures cover score relationships, ROC, PR and family comparison. All integrity checks passed; prior artifacts remain unchanged.

This is a post-hoc seed-42 development experiment on attack families absent from training. The test cohort was observed in earlier phases. No statistical significance, confirmatory improvement, zero-day detection or general unseen-threat superiority is claimed. The frozen preprocessing was fitted on all TRAIN classes; the AE model itself was fitted on benign rows. No GATv2, Transformer, graph+temporal integration, explainability or new features were introduced. Stop after Phase 8.
