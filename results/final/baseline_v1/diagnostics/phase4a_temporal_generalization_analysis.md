# Phase 4A: temporal generalization and threshold diagnosis

Existing seed-42 fitted models only. No fitting, recalibration, preprocessing changes or partition changes were performed. Validation/test probabilities are the saved Phase 4 outputs. Training inference uses the existing read-only model-input cache. All numbers and tables below are generated from diagnostic outputs.

## Scope and safeguards

Every malicious test record belongs to a family absent from training: Bot or Infilteration. Infilteration dominates validation malicious traffic. Known-family test recall is not defined and is not computed. This is binary detection, not multiclass recognition; Bot is an attack family absent from training, not a claimed zero-day attack.

Thresholds were selected exclusively from validation labels/scores, saved in validation_selected_thresholds.csv and bound by validation_threshold_lock.json before any Phase 4A transfer to test. No test result selects a threshold or model. The original Phase 4 test results had already been observed; this is a transparently post-hoc diagnostic phase, not a new untouched confirmatory evaluation.

Frozen temporal cohorts:

| Partition | Dates | Records | First timestamp | Last timestamp |
|---|---|---|---|---|
| train | 2018-02-14, 2018-02-15, 2018-02-16, 2018-02-20, 2018-02-21, 2018-02-22 | 12795136 | 2018-02-14T01:00:00 | 2018-02-22T12:59:59 |
| validation | 2018-02-23, 2018-02-28 | 1652943 | 2018-02-23T01:00:00 | 2018-02-28T12:59:59 |
| test | 2018-03-01, 2018-03-02 | 1374143 | 2018-03-01T01:00:00 | 2018-03-02T12:59:59 |

## Supervised training performance

These are in-sample metrics at threshold 0.5, not unbiased generalization estimates. High aggregate training performance shows learning of the training distribution but does not establish performance on every rare training family.

| Model | ROC-AUC | PR-AUC | AP | Precision | Recall | F1 | Macro-F1 | FPR | FNR |
|---|---|---|---|---|---|---|---|---|---|
| logistic_regression | 0.995084 | 0.957088 | 0.957371 | 0.782023 | 0.999078 | 0.877324 | 0.926104 | 0.0488489 | 0.000922234 |
| random_forest | 0.99999 | 0.999948 | 0.999948 | 0.979681 | 0.999369 | 0.989427 | 0.993775 | 0.0036358 | 0.000630534 |
| xgboost | 0.999992 | 0.99995 | 0.999949 | 0.98177 | 0.99982 | 0.990713 | 0.994533 | 0.00325658 | 0.000179629 |
| mlp | 0.999986 | 0.999896 | 0.999897 | 0.994318 | 0.998618 | 0.996464 | 0.997921 | 0.00100104 | 0.00138152 |

Training malicious recall spans 99.86%–99.98%. Thus the later-period collapse is not a broad inability to fit the aggregate training distribution. This does not rule out overfitting or reliance on date-specific correlations.

## Known-family validation behavior

The validation samples are small: Brute Force -Web has 362 records, Brute Force -XSS 151, and SQL Injection 53. Treat these recalls as descriptive, with limited support. These families also had few training examples. No known-family test recall is reported.

| Model | Family | N | Detected | Missed | Recall | Mean score | Median | p90 | Max |
|---|---|---|---|---|---|---|---|---|---|
| logistic_regression | Brute Force -Web | 362 | 62 | 300 | 0.171271 | 0.118711 | 2.46909e-08 | 0.610743 | 0.982538 |
| logistic_regression | Brute Force -XSS | 151 | 66 | 85 | 0.437086 | 0.304582 | 2.46899e-08 | 0.731837 | 0.750358 |
| logistic_regression | SQL Injection | 53 | 21 | 32 | 0.396226 | 0.447116 | 0.310766 | 0.996534 | 0.999997 |
| random_forest | Brute Force -Web | 362 | 10 | 352 | 0.0276243 | 0.183284 | 0.0276955 | 0.490538 | 0.955056 |
| random_forest | Brute Force -XSS | 151 | 23 | 128 | 0.152318 | 0.382449 | 0.43654 | 0.782202 | 0.835701 |
| random_forest | SQL Injection | 53 | 3 | 50 | 0.0566038 | 0.163296 | 0.117876 | 0.291497 | 0.923409 |
| xgboost | Brute Force -Web | 362 | 69 | 293 | 0.190608 | 0.174432 | 0.0245446 | 0.72861 | 0.905794 |
| xgboost | Brute Force -XSS | 151 | 101 | 50 | 0.668874 | 0.528073 | 0.751156 | 0.828466 | 0.905794 |
| xgboost | SQL Injection | 53 | 2 | 51 | 0.0377358 | 0.0909172 | 0.0389836 | 0.18224 | 0.905794 |
| mlp | Brute Force -Web | 362 | 71 | 291 | 0.196133 | 0.263648 | 0.0233711 | 0.99821 | 0.998296 |
| mlp | Brute Force -XSS | 151 | 98 | 53 | 0.649007 | 0.621588 | 0.608728 | 0.999982 | 0.999983 |
| mlp | SQL Injection | 53 | 4 | 49 | 0.0754717 | 0.0966566 | 0.00376347 | 0.355366 | 0.886203 |

The known-family results also vary substantially and include many misses. Unseen-family status therefore cannot by itself explain all later-period errors.

## Unseen-family validation and test behavior

| Model | Partition | Family | N | Detected at .5 | Recall at .5 | Mean | Median | p75 | p90 | p95 | p99 | Max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| logistic_regression | validation | Infilteration | 68857 | 4998 | 0.0725852 | 0.0654626 | 0.00274038 | 0.0061683 | 0.23858 | 0.595807 | 0.779898 | 0.999996 |
| logistic_regression | test | Infilteration | 93040 | 3042 | 0.0326956 | 0.0350118 | 0.00188463 | 0.00443299 | 0.0106151 | 0.187483 | 0.779819 | 1 |
| logistic_regression | test | Bot | 282310 | 0 | 0 | 0.0699656 | 0.00035675 | 0.142044 | 0.144721 | 0.146992 | 0.149042 | 0.164885 |
| random_forest | validation | Infilteration | 68857 | 137 | 0.00198963 | 0.0161357 | 0 | 0.00153776 | 0.0626865 | 0.110024 | 0.219554 | 0.935716 |
| random_forest | test | Infilteration | 93040 | 235 | 0.0025258 | 0.0202717 | 0 | 0.0157652 | 0.0844612 | 0.110024 | 0.234584 | 0.996004 |
| random_forest | test | Bot | 282310 | 0 | 0 | 0.102001 | 0.021384 | 0.193266 | 0.206871 | 0.207395 | 0.209103 | 0.291775 |
| xgboost | validation | Infilteration | 68857 | 719 | 0.0104419 | 0.0192312 | 0.00866424 | 0.00878884 | 0.00914232 | 0.01692 | 0.529589 | 0.971225 |
| xgboost | test | Infilteration | 93040 | 1201 | 0.0129084 | 0.0224297 | 0.00866424 | 0.00880863 | 0.00914232 | 0.0197506 | 0.740252 | 0.982612 |
| xgboost | test | Bot | 282310 | 0 | 0 | 0.0329345 | 0.00858869 | 0.0628868 | 0.0628868 | 0.0628868 | 0.0628868 | 0.0755567 |
| mlp | validation | Infilteration | 68857 | 240 | 0.00348548 | 0.00603672 | 3.68431e-12 | 2.13177e-07 | 0.00200428 | 0.0161058 | 0.0812609 | 0.999998 |
| mlp | test | Infilteration | 93040 | 504 | 0.00541702 | 0.0073377 | 5.60116e-13 | 4.34371e-10 | 0.000101582 | 0.0137885 | 0.0809495 | 0.999998 |
| mlp | test | Bot | 282310 | 0 | 0 | 0.000165549 | 2.41367e-09 | 0.000358933 | 0.00038929 | 0.00041663 | 0.000443354 | 0.000939129 |

## Ranking versus fixed-threshold performance

ROC-AUC evaluates ranking across thresholds; average precision and trapezoidal PR-AUC are distinct summaries and are both retained. AP is compared with the partition malicious prevalence; PR comparisons across partitions must account for their different prevalences. Ranking skill does not guarantee useful detection at threshold 0.5.

| Model | Partition | ROC-AUC | PR-AUC | AP | Prevalence | AP / prevalence | Recall at .5 |
|---|---|---|---|---|---|---|---|
| logistic_regression | validation | 0.499304 | 0.0419201 | 0.0419332 | 0.0419996 | 0.998419 | 0.0741397 |
| logistic_regression | test | 0.551386 | 0.344731 | 0.345175 | 0.273152 | 1.26367 | 0.00810444 |
| random_forest | validation | 0.497345 | 0.0482271 | 0.0500907 | 0.0419996 | 1.19265 | 0.00249197 |
| random_forest | test | 0.832852 | 0.677675 | 0.67716 | 0.273152 | 2.47906 | 0.000626082 |
| xgboost | validation | 0.547849 | 0.0483679 | 0.0498494 | 0.0419996 | 1.1869 | 0.0128344 |
| xgboost | test | 0.553878 | 0.397613 | 0.531589 | 0.273152 | 1.94613 | 0.00319968 |
| mlp | validation | 0.550251 | 0.0586124 | 0.0586904 | 0.0419996 | 1.3974 | 0.00594904 |
| mlp | test | 0.774968 | 0.512284 | 0.51274 | 0.273152 | 1.87712 | 0.00134275 |

**logistic_regression:** validation ROC-AUC 0.4993, test ROC-AUC 0.5514, test AP 0.3452. At 0.5, test recall is 0.810%. The validation maximum-F1 threshold transfers to test recall 54.22%, precision 22.49%, and FPR 70.24%. This describes the preselected operating point; it is not selected from test.

**random_forest:** validation ROC-AUC 0.4973, test ROC-AUC 0.8329, test AP 0.6772. At 0.5, test recall is 0.063%. The validation maximum-F1 threshold transfers to test recall 39.38%, precision 87.09%, and FPR 2.19%. This describes the preselected operating point; it is not selected from test.

**xgboost:** validation ROC-AUC 0.5478, test ROC-AUC 0.5539, test AP 0.5316. At 0.5, test recall is 0.320%. The validation maximum-F1 threshold transfers to test recall 41.23%, precision 62.79%, and FPR 9.18%. This describes the preselected operating point; it is not selected from test.

**mlp:** validation ROC-AUC 0.5503, test ROC-AUC 0.7750, test AP 0.5127. At 0.5, test recall is 0.134%. The validation maximum-F1 threshold transfers to test recall 41.93%, precision 53.96%, and FPR 13.44%. This describes the preselected operating point; it is not selected from test.

Random Forest retains materially useful test ranking despite poor classification at 0.5; its validation ranking is much weaker. MLP also has a substantial test ranking/fixed-threshold gap. The other models have weaker overall test ROC ranking. Per-family ranking against benign traffic from the same partition is below; this separates changes in family mixture from a single pooled metric.

| Model | Partition | Family | ROC-AUC vs benign | AP vs benign | Comparison prevalence |
|---|---|---|---|---|---|
| logistic_regression | validation | Infilteration | 0.499345 | 0.0414636 | 0.0416715 |
| logistic_regression | test | Infilteration | 0.455436 | 0.0758953 | 0.0852145 |
| logistic_regression | test | Bot | 0.583008 | 0.324363 | 0.220365 |
| random_forest | validation | Infilteration | 0.494161 | 0.0485553 | 0.0416715 |
| random_forest | test | Infilteration | 0.595946 | 0.130863 | 0.0852145 |
| random_forest | test | Bot | 0.910928 | 0.736168 | 0.220365 |
| xgboost | validation | Infilteration | 0.545913 | 0.0483168 | 0.0416715 |
| xgboost | test | Infilteration | 0.548197 | 0.106781 | 0.0852145 |
| xgboost | test | Bot | 0.555751 | 0.563992 | 0.220365 |
| mlp | validation | Infilteration | 0.548461 | 0.0558412 | 0.0416715 |
| mlp | test | Infilteration | 0.467051 | 0.0979346 | 0.0852145 |
| mlp | test | Bot | 0.876447 | 0.525301 | 0.220365 |

## Validation-only threshold selection and transfer

The search exhausts distinct validation scores with prediction rule score >= threshold and includes an all-negative point just above the maximum score. Maximum-F1 and maximum-macro-F1 ties prefer the higher threshold. For FPR constraints, maximize validation recall subject to the cap, then minimize false positives and prefer the higher threshold. No minimum recall is assumed. A validation FPR cap is not a guarantee about future FPR.

| Model | Validation objective | Threshold | Val precision | Val recall | Val F1 | Val macro-F1 | Val FPR |
|---|---|---|---|---|---|---|---|
| logistic_regression | maximum_binary_f1 | 0.000447581 | 0.0429703 | 0.714331 | 0.0810642 | 0.270573 | 0.697488 |
| logistic_regression | maximum_macro_f1 | 0.548742 | 0.0471742 | 0.0664909 | 0.0551912 | 0.502419 | 0.0588777 |
| logistic_regression | fpr_at_most_0.01 | 0.983158 | 0.01999 | 0.00462383 | 0.00751044 | 0.490583 | 0.00993799 |
| logistic_regression | fpr_at_most_0.005 | 0.992523 | 0.0158383 | 0.00177175 | 0.00318698 | 0.489678 | 0.00482659 |
| logistic_regression | fpr_at_most_0.001 | 0.998332 | 0.0423497 | 0.000893076 | 0.00174926 | 0.489938 | 0.000885369 |
| random_forest | maximum_binary_f1 | 0.106964 | 0.13589 | 0.095199 | 0.111962 | 0.539537 | 0.0265396 |
| random_forest | maximum_macro_f1 | 0.106964 | 0.13589 | 0.095199 | 0.111962 | 0.539537 | 0.0265396 |
| random_forest | fpr_at_most_0.01 | 0.173709 | 0.0793531 | 0.0196477 | 0.0314968 | 0.50272 | 0.00999356 |
| random_forest | fpr_at_most_0.005 | 0.291775 | 0.0666116 | 0.00812411 | 0.014482 | 0.495351 | 0.00499078 |
| random_forest | fpr_at_most_0.001 | 0.765834 | 0.0379902 | 0.000893076 | 0.00174513 | 0.489909 | 0.000991462 |
| xgboost | maximum_binary_f1 | 0.00913401 | 0.0651887 | 0.16133 | 0.0928567 | 0.510726 | 0.101425 |
| xgboost | maximum_macro_f1 | 0.00913401 | 0.0651887 | 0.16133 | 0.0928567 | 0.510726 | 0.101425 |
| xgboost | fpr_at_most_0.01 | 0.0944726 | 0.0711593 | 0.0174006 | 0.0279633 | 0.500939 | 0.00995756 |
| xgboost | fpr_at_most_0.005 | 0.41608 | 0.110829 | 0.0138139 | 0.0245658 | 0.500486 | 0.0048588 |
| xgboost | fpr_at_most_0.001 | 0.874227 | 0.223691 | 0.00609308 | 0.011863 | 0.495039 | 0.000927049 |
| mlp | maximum_binary_f1 | 2.07041e-08 | 0.0733853 | 0.293303 | 0.117397 | 0.506964 | 0.162363 |
| mlp | maximum_macro_f1 | 0.00346634 | 0.0992216 | 0.0951126 | 0.0971237 | 0.529198 | 0.0378555 |
| mlp | fpr_at_most_0.01 | 0.0590479 | 0.0944238 | 0.0237817 | 0.0379942 | 0.506011 | 0.00999924 |
| mlp | fpr_at_most_0.005 | 0.0968262 | 0.0909614 | 0.0113795 | 0.0202284 | 0.49826 | 0.00498573 |
| mlp | fpr_at_most_0.001 | 0.812089 | 0.153105 | 0.00411967 | 0.00802345 | 0.49308 | 0.00099904 |

Frozen-threshold test transfer:

| Model | Validation objective | Threshold | Test precision | Test recall | Test F1 | Test FPR | FP | FN | Bot recall | Infilteration recall |
|---|---|---|---|---|---|---|---|---|---|---|
| logistic_regression | maximum_binary_f1 | 0.000447581 | 0.224878 | 0.542235 | 0.317911 | 0.702379 | 701531 | 171822 | 0.495696 | 0.683448 |
| logistic_regression | maximum_macro_f1 | 0.548742 | 0.0661807 | 0.00742507 | 0.0133521 | 0.0393725 | 39325 | 372563 | 0 | 0.0299549 |
| logistic_regression | fpr_at_most_0.01 | 0.983158 | 0.052175 | 0.00115359 | 0.00225727 | 0.00787551 | 7866 | 374917 | 0 | 0.00465391 |
| logistic_regression | fpr_at_most_0.005 | 0.992523 | 0.0783066 | 0.000753963 | 0.00149355 | 0.00333503 | 3331 | 375067 | 0 | 0.0030417 |
| logistic_regression | fpr_at_most_0.001 | 0.998332 | 0.238024 | 0.000423605 | 0.000845704 | 0.000509615 | 509 | 375191 | 0 | 0.00170894 |
| random_forest | maximum_binary_f1 | 0.106964 | 0.870927 | 0.393832 | 0.542394 | 0.0219345 | 21908 | 227525 | 0.492232 | 0.0952601 |
| random_forest | maximum_macro_f1 | 0.106964 | 0.870927 | 0.393832 | 0.542394 | 0.0219345 | 21908 | 227525 | 0.492232 | 0.0952601 |
| random_forest | fpr_at_most_0.01 | 0.173709 | 0.939448 | 0.342744 | 0.50225 | 0.00830202 | 8292 | 246701 | 0.449612 | 0.0184759 |
| random_forest | fpr_at_most_0.005 | 0.291775 | 0.123001 | 0.00172106 | 0.00339462 | 0.00461157 | 4606 | 374704 | 3.54221e-06 | 0.0069325 |
| random_forest | fpr_at_most_0.001 | 0.765834 | 0.063263 | 0.000151858 | 0.000302989 | 0.00084502 | 844 | 375293 | 0 | 0.00061264 |
| xgboost | maximum_binary_f1 | 0.00913401 | 0.627908 | 0.412343 | 0.49779 | 0.0918278 | 91717 | 220577 | 0.495392 | 0.16035 |
| xgboost | maximum_macro_f1 | 0.00913401 | 0.627908 | 0.412343 | 0.49779 | 0.0918278 | 91717 | 220577 | 0.495392 | 0.16035 |
| xgboost | fpr_at_most_0.01 | 0.0944726 | 0.195634 | 0.00556281 | 0.010818 | 0.00859537 | 8585 | 373262 | 0 | 0.022442 |
| xgboost | fpr_at_most_0.005 | 0.41608 | 0.230558 | 0.00334887 | 0.00660186 | 0.00420007 | 4195 | 374093 | 0 | 0.0135103 |
| xgboost | fpr_at_most_0.001 | 0.874227 | 0.511759 | 0.00144931 | 0.00289044 | 0.000519627 | 519 | 374806 | 0 | 0.00584695 |
| mlp | maximum_binary_f1 | 2.07041e-08 | 0.539588 | 0.419257 | 0.471872 | 0.134439 | 134277 | 217982 | 0.492661 | 0.196528 |
| mlp | maximum_macro_f1 | 0.00346634 | 0.200488 | 0.0173065 | 0.0318626 | 0.0259363 | 25905 | 368854 | 0 | 0.0698194 |
| mlp | fpr_at_most_0.01 | 0.0590479 | 0.193305 | 0.00490742 | 0.00957184 | 0.00769629 | 7687 | 373508 | 0 | 0.0197979 |
| mlp | fpr_at_most_0.005 | 0.0968262 | 0.13981 | 0.00176369 | 0.00348343 | 0.00407792 | 4073 | 374688 | 0 | 0.00711522 |
| mlp | fpr_at_most_0.001 | 0.812089 | 0.248062 | 0.000937791 | 0.00186852 | 0.00106829 | 1067 | 374998 | 0 | 0.00378332 |

At the threshold selected under validation FPR <= 1%, Random Forest test recall is 34.27% at FPR 0.83%; Bot recall is 44.96% and Infilteration recall 1.85%. This supports a threshold mismatch for part of its test performance, while the remaining missed attacks show that threshold adjustment is not a complete solution.

The separate threshold curves use a predeclared grid from 0 to 1 in steps of 0.005 and are POST-HOC DESCRIPTIVE ONLY. No optimum is extracted from those test curves.

## Probability calibration

Reliability diagrams use 20 equal-width validation score bins; empty bins are omitted, with counts retained in calibration_bins.csv. ECE is weighted absolute bin calibration error and depends on binning. The constant-prevalence Brier reference uses the observed validation prevalence only as a descriptive reference, not a fitted replacement model. Negative Brier skill means worse Brier score than that reference.

| Model | Brier | Reference Brier | Brier skill | ECE | Mean predicted | Observed prevalence |
|---|---|---|---|---|---|---|
| logistic_regression | 0.079184 | 0.0402357 | -0.968006 | 0.0913752 | 0.0679818 | 0.0419996 |
| random_forest | 0.0433647 | 0.0402357 | -0.0777688 | 0.038803 | 0.0113875 | 0.0419996 |
| xgboost | 0.0431493 | 0.0402357 | -0.0724145 | 0.03586 | 0.0141845 | 0.0419996 |
| mlp | 0.0427102 | 0.0402357 | -0.0614999 | 0.0421303 | 0.00301772 | 0.0419996 |

All four models have negative validation Brier skill. Reliability gaps and mismatches between mean predicted risk and observed prevalence support poor probability calibration in this later period. Brier score also reflects discrimination and prevalence; it is not an isolated calibration test. Class-weighted fitting may affect probability interpretation, but these diagnostics do not identify a unique cause. No recalibration was fitted.

## Temporal feature distribution shift

All 80 frozen input dimensions are covered: 77 numerical features in cleaned native units before imputation, plus the three fixed Protocol one-hot inputs. Numeric summaries use every finite observed value; missing rates are measured before imputation. Population standard deviation uses ddof=0. Quantiles and KS statistics are exact, with no row sampling. Because scaling is a fixed positive affine transform, it does not change the observed-value KS comparisons. Missingness and its imputation effects should be considered separately; these are not post-imputation summaries. Excluded identifiers are not analyzed.

PSI uses reference-group decile cut points with duplicate cuts removed, unbounded outer bins, an explicit missing bin, and probability floor 1e-6 followed by renormalization. Constant references get a dedicated constant-value bin with lower/upper tails. For overall comparisons the reference is train; family comparisons use the indicated training group, or validation Infilteration for its temporal comparison. KS excludes missing values; PSI includes missingness. PSI depends on binning and smoothing. No significance p-values or universal shift cutoffs are used.

Features are ranked by KS, with PSI as a tie-breaker. These marginal shifts are descriptive and are not causal feature importance; class/family mixture and acquisition differences can contribute.

### Top 20: train to validation

| Rank | Feature | KS | PSI | Train missing | Target missing |
|---|---|---|---|---|---|
| 1 | Pkt Len Std | 0.0925153 | 0.0537606 | 0 | 0 |
| 2 | Pkt Len Var | 0.0925065 | 0.0548967 | 0 | 0 |
| 3 | Fwd Header Len | 0.0898387 | 0.0916751 | 0 | 0 |
| 4 | Dst Port | 0.0886142 | 0.0999464 | 0 | 0 |
| 5 | Fwd Seg Size Min | 0.083535 | 0.00999839 | 0 | 0 |
| 6 | Fwd IAT Max | 0.0791517 | 0.123885 | 0 | 0 |
| 7 | Fwd IAT Tot | 0.0787003 | 0.143397 | 0 | 0 |
| 8 | Fwd IAT Mean | 0.0732972 | 0.123364 | 0 | 0 |
| 9 | Bwd IAT Min | 0.0719874 | 0.0394543 | 0 | 0 |
| 10 | Pkt Len Max | 0.0694459 | 0.284387 | 0 | 0 |
| 11 | Bwd Pkt Len Std | 0.0679993 | 0.0374728 | 0 | 0 |
| 12 | Flow IAT Min | 0.0668797 | 0.127347 | 0 | 0 |
| 13 | Bwd Pkt Len Max | 0.0662597 | 0.158557 | 0 | 0 |
| 14 | Fwd Seg Size Avg | 0.0634084 | 0.0531086 | 0 | 0 |
| 15 | Fwd Pkt Len Mean | 0.0634084 | 0.0531033 | 0 | 0 |
| 16 | Flow Duration | 0.0632684 | 0.08445 | 0 | 0 |
| 17 | Pkt Len Mean | 0.0625447 | 0.085555 | 0 | 0 |
| 18 | Fwd IAT Min | 0.0624372 | 0.0635161 | 0 | 0 |
| 19 | Fwd Pkt Len Std | 0.0623977 | 0.0532694 | 0 | 0 |
| 20 | Tot Fwd Pkts | 0.0617948 | 0.0623583 | 0 | 0 |

### Top 20: train to test

| Rank | Feature | KS | PSI | Train missing | Target missing |
|---|---|---|---|---|---|
| 1 | Dst Port | 0.221769 | 0.383618 | 0 | 0 |
| 2 | Fwd IAT Tot | 0.132549 | 0.112853 | 0 | 0 |
| 3 | Fwd IAT Max | 0.13045 | 0.177145 | 0 | 0 |
| 4 | Bwd Pkt Len Mean | 0.120125 | 0.0904214 | 0 | 0 |
| 5 | Bwd Seg Size Avg | 0.120125 | 0.0904214 | 0 | 0 |
| 6 | Flow IAT Mean | 0.118252 | 0.159129 | 0 | 0 |
| 7 | Init Fwd Win Byts | 0.11676 | 0.228535 | 0 | 0 |
| 8 | Pkt Size Avg | 0.111481 | 0.102222 | 0 | 0 |
| 9 | Fwd IAT Mean | 0.110954 | 0.134653 | 0 | 0 |
| 10 | Flow Pkts/s | 0.11091 | 0.0971449 | 0.00601002 | 0.0050657 |
| 11 | Bwd Pkt Len Std | 0.104093 | 0.0808231 | 0 | 0 |
| 12 | Pkt Len Mean | 0.0995658 | 0.146536 | 0 | 0 |
| 13 | Pkt Len Var | 0.099457 | 0.0854857 | 0 | 0 |
| 14 | Flow IAT Min | 0.0974509 | 0.172933 | 0 | 0 |
| 15 | Bwd Pkt Len Max | 0.0958506 | 0.26162 | 0 | 0 |
| 16 | Fwd Pkts/s | 0.0927369 | 0.091498 | 0 | 0 |
| 17 | TotLen Bwd Pkts | 0.0916132 | 0.151688 | 0 | 0 |
| 18 | Subflow Bwd Byts | 0.0916132 | 0.151688 | 0 | 0 |
| 19 | Pkt Len Std | 0.0911674 | 0.0858301 | 0 | 0 |
| 20 | Flow IAT Max | 0.0905191 | 0.0934557 | 0 | 0 |

## Family-level feature shift

The following features maximize the smaller of KS against training benign and KS against training malicious, requiring a large shift from both reference populations. Complete per-reference comparisons and both PSI values are in family_feature_shift.csv and family_shift_against_both_rankings.csv.

### validation_Infilteration

| Rank | Feature | KS vs benign | KS vs malicious | Minimum KS |
|---|---|---|---|---|
| 1 | Fwd Pkt Len Std | 0.154918 | 0.1871 | 0.154918 |
| 2 | Bwd IAT Min | 0.149058 | 0.145392 | 0.145392 |
| 3 | Pkt Len Var | 0.144454 | 0.396627 | 0.144454 |
| 4 | Down/Up Ratio | 0.139052 | 0.292873 | 0.139052 |
| 5 | Init Bwd Win Byts | 0.138891 | 0.228836 | 0.138891 |
| 6 | TotLen Bwd Pkts | 0.138251 | 0.313516 | 0.138251 |
| 7 | Subflow Bwd Byts | 0.138251 | 0.313516 | 0.138251 |
| 8 | Fwd Header Len | 0.135769 | 0.502128 | 0.135769 |
| 9 | Fwd Pkt Len Max | 0.135426 | 0.550757 | 0.135426 |
| 10 | Bwd Pkt Len Max | 0.135364 | 0.313516 | 0.135364 |

### test_Infilteration

| Rank | Feature | KS vs benign | KS vs malicious | Minimum KS |
|---|---|---|---|---|
| 1 | Pkt Len Var | 0.268147 | 0.252153 | 0.252153 |
| 2 | Pkt Len Std | 0.251289 | 0.252153 | 0.251289 |
| 3 | Fwd Seg Size Min | 0.243811 | 0.318256 | 0.243811 |
| 4 | Tot Fwd Pkts | 0.237328 | 0.488844 | 0.237328 |
| 5 | Subflow Fwd Pkts | 0.237328 | 0.488844 | 0.237328 |
| 6 | Fwd IAT Tot | 0.237261 | 0.554513 | 0.237261 |
| 7 | Fwd IAT Mean | 0.237261 | 0.550956 | 0.237261 |
| 8 | Fwd IAT Max | 0.237261 | 0.555443 | 0.237261 |
| 9 | Fwd IAT Min | 0.234251 | 0.597845 | 0.234251 |
| 10 | Fwd Header Len | 0.223664 | 0.588586 | 0.223664 |

### test_Bot

| Rank | Feature | KS vs benign | KS vs malicious | Minimum KS |
|---|---|---|---|---|
| 1 | Dst Port | 0.788576 | 0.999086 | 0.788576 |
| 2 | Fwd IAT Min | 0.548144 | 0.60715 | 0.548144 |
| 3 | Flow Pkts/s | 0.543724 | 0.679727 | 0.543724 |
| 4 | Flow IAT Mean | 0.541623 | 0.727259 | 0.541623 |
| 5 | Fwd Pkts/s | 0.541258 | 0.597046 | 0.541258 |
| 6 | Fwd IAT Tot | 0.518604 | 0.761112 | 0.518604 |
| 7 | Fwd IAT Max | 0.516816 | 0.750575 | 0.516816 |
| 8 | Flow Duration | 0.508652 | 0.561717 | 0.508652 |
| 9 | Flow IAT Max | 0.507793 | 0.566431 | 0.507793 |
| 10 | Fwd IAT Mean | 0.501993 | 0.741404 | 0.501993 |

## Infilteration across later periods

This family is absent from training but appears in both validation and test. The same validation-selected thresholds are applied to both periods; no family-specific threshold is optimized. Changes in scores and recall across these periods are distinct from the fact that the family was initially unseen.

| Model | Partition | Threshold source | Threshold | Infilteration recall | Mean score | Median score |
|---|---|---|---|---|---|---|
| logistic_regression | validation | fixed_0_5 | 0.5 | 0.0725852 | 0.0654626 | 0.00274038 |
| logistic_regression | validation | maximum_binary_f1 | 0.000447581 | 0.715991 | 0.0654626 | 0.00274038 |
| logistic_regression | validation | maximum_macro_f1 | 0.548742 | 0.0650479 | 0.0654626 | 0.00274038 |
| logistic_regression | validation | fpr_at_most_0.01 | 0.983158 | 0.00451661 | 0.0654626 | 0.00274038 |
| logistic_regression | validation | fpr_at_most_0.005 | 0.992523 | 0.00165561 | 0.0654626 | 0.00274038 |
| logistic_regression | validation | fpr_at_most_0.001 | 0.998332 | 0.000871371 | 0.0654626 | 0.00274038 |
| logistic_regression | test | fixed_0_5 | 0.5 | 0.0326956 | 0.0350118 | 0.00188463 |
| logistic_regression | test | maximum_binary_f1 | 0.000447581 | 0.683448 | 0.0350118 | 0.00188463 |
| logistic_regression | test | maximum_macro_f1 | 0.548742 | 0.0299549 | 0.0350118 | 0.00188463 |
| logistic_regression | test | fpr_at_most_0.01 | 0.983158 | 0.00465391 | 0.0350118 | 0.00188463 |
| logistic_regression | test | fpr_at_most_0.005 | 0.992523 | 0.0030417 | 0.0350118 | 0.00188463 |
| logistic_regression | test | fpr_at_most_0.001 | 0.998332 | 0.00170894 | 0.0350118 | 0.00188463 |
| random_forest | validation | fixed_0_5 | 0.5 | 0.00198963 | 0.0161357 | 0 |
| random_forest | validation | maximum_binary_f1 | 0.106964 | 0.0914649 | 0.0161357 | 0 |
| random_forest | validation | maximum_macro_f1 | 0.106964 | 0.0914649 | 0.0161357 | 0 |
| random_forest | validation | fpr_at_most_0.01 | 0.173709 | 0.0156702 | 0.0161357 | 0 |
| random_forest | validation | fpr_at_most_0.005 | 0.291775 | 0.00460374 | 0.0161357 | 0 |
| random_forest | validation | fpr_at_most_0.001 | 0.765834 | 0.0005083 | 0.0161357 | 0 |
| random_forest | test | fixed_0_5 | 0.5 | 0.0025258 | 0.0202717 | 0 |
| random_forest | test | maximum_binary_f1 | 0.106964 | 0.0952601 | 0.0202717 | 0 |
| random_forest | test | maximum_macro_f1 | 0.106964 | 0.0952601 | 0.0202717 | 0 |
| random_forest | test | fpr_at_most_0.01 | 0.173709 | 0.0184759 | 0.0202717 | 0 |
| random_forest | test | fpr_at_most_0.005 | 0.291775 | 0.0069325 | 0.0202717 | 0 |
| random_forest | test | fpr_at_most_0.001 | 0.765834 | 0.00061264 | 0.0202717 | 0 |
| xgboost | validation | fixed_0_5 | 0.5 | 0.0104419 | 0.0192312 | 0.00866424 |
| xgboost | validation | maximum_binary_f1 | 0.00913401 | 0.156702 | 0.0192312 | 0.00866424 |
| xgboost | validation | maximum_macro_f1 | 0.00913401 | 0.156702 | 0.0192312 | 0.00866424 |
| xgboost | validation | fpr_at_most_0.01 | 0.0944726 | 0.014305 | 0.0192312 | 0.00866424 |
| xgboost | validation | fpr_at_most_0.005 | 0.41608 | 0.011415 | 0.0192312 | 0.00866424 |
| xgboost | validation | fpr_at_most_0.001 | 0.874227 | 0.00588175 | 0.0192312 | 0.00866424 |
| xgboost | test | fixed_0_5 | 0.5 | 0.0129084 | 0.0224297 | 0.00866424 |
| xgboost | test | maximum_binary_f1 | 0.00913401 | 0.16035 | 0.0224297 | 0.00866424 |
| xgboost | test | maximum_macro_f1 | 0.00913401 | 0.16035 | 0.0224297 | 0.00866424 |
| xgboost | test | fpr_at_most_0.01 | 0.0944726 | 0.022442 | 0.0224297 | 0.00866424 |
| xgboost | test | fpr_at_most_0.005 | 0.41608 | 0.0135103 | 0.0224297 | 0.00866424 |
| xgboost | test | fpr_at_most_0.001 | 0.874227 | 0.00584695 | 0.0224297 | 0.00866424 |
| mlp | validation | fixed_0_5 | 0.5 | 0.00348548 | 0.00603672 | 3.68431e-12 |
| mlp | validation | maximum_binary_f1 | 2.07041e-08 | 0.289745 | 0.00603672 | 3.68431e-12 |
| mlp | validation | maximum_macro_f1 | 0.00346634 | 0.0903612 | 0.00603672 | 3.68431e-12 |
| mlp | validation | fpr_at_most_0.01 | 0.0590479 | 0.0194897 | 0.00603672 | 3.68431e-12 |
| mlp | validation | fpr_at_most_0.005 | 0.0968262 | 0.00729047 | 0.00603672 | 3.68431e-12 |
| mlp | validation | fpr_at_most_0.001 | 0.812089 | 0.002222 | 0.00603672 | 3.68431e-12 |
| mlp | test | fixed_0_5 | 0.5 | 0.00541702 | 0.0073377 | 5.60116e-13 |
| mlp | test | maximum_binary_f1 | 2.07041e-08 | 0.196528 | 0.0073377 | 5.60116e-13 |
| mlp | test | maximum_macro_f1 | 0.00346634 | 0.0698194 | 0.0073377 | 5.60116e-13 |
| mlp | test | fpr_at_most_0.01 | 0.0590479 | 0.0197979 | 0.0073377 | 5.60116e-13 |
| mlp | test | fpr_at_most_0.005 | 0.0968262 | 0.00711522 | 0.0073377 | 5.60116e-13 |
| mlp | test | fpr_at_most_0.001 | 0.812089 | 0.00378332 | 0.0073377 | 5.60116e-13 |

| Model | Validation-to-test score KS |
|---|---|
| logistic_regression | 0.115064 |
| random_forest | 0.17372 |
| xgboost | 0.0868436 |
| mlp | 0.133027 |

Largest within-Infilteration feature shifts:

| Feature | KS | PSI |
|---|---|---|
| Fwd Seg Size Min | 0.18967 | 0.241736 |
| Dst Port | 0.181558 | 0.238643 |
| PSH Flag Cnt | 0.146933 | 0.0880664 |
| Flow Byts/s | 0.146673 | 0.101709 |
| Fwd Pkt Len Max | 0.145754 | 0.105436 |
| Fwd Pkt Len Mean | 0.145309 | 0.0985228 |
| Fwd Seg Size Avg | 0.145309 | 0.0985228 |
| Init Fwd Win Byts | 0.145108 | 0.234308 |
| TotLen Fwd Pkts | 0.145099 | 0.0968678 |
| Subflow Fwd Byts | 0.145099 | 0.0968678 |
| Pkt Len Max | 0.144899 | 0.139706 |
| Pkt Len Std | 0.144719 | 0.117823 |
| Pkt Len Var | 0.144719 | 0.117823 |
| Pkt Len Mean | 0.144515 | 0.120963 |
| Pkt Size Avg | 0.144515 | 0.114007 |
| Bwd Pkts/s | 0.143242 | 0.155308 |
| Bwd Header Len | 0.12863 | 0.163209 |
| Init Bwd Win Byts | 0.127671 | 0.182782 |
| Bwd Pkt Len Mean | 0.115867 | 0.0801404 |
| Bwd Seg Size Avg | 0.115867 | 0.0801404 |

## Bot: attack family absent from training

Bot occurs only in test. Score statistics are in unseen_attack_score_diagnostics.csv and bot_analysis.csv. All four models miss Bot at threshold 0.5. Some validation-selected lower thresholds detect a portion of Bot; the table retains the corresponding threshold source rather than selecting on Bot outcomes. Strongest feature differences from both training populations are listed above; separate reference rankings follow.

| Model | Validation objective / fixed | Threshold | Bot recall | Mean score | Median | Maximum |
|---|---|---|---|---|---|---|
| logistic_regression | fixed_0_5 | 0.5 | 0 | 0.0699656 | 0.00035675 | 0.164885 |
| logistic_regression | maximum_binary_f1 | 0.000447581 | 0.495696 | 0.0699656 | 0.00035675 | 0.164885 |
| logistic_regression | maximum_macro_f1 | 0.548742 | 0 | 0.0699656 | 0.00035675 | 0.164885 |
| logistic_regression | fpr_at_most_0.01 | 0.983158 | 0 | 0.0699656 | 0.00035675 | 0.164885 |
| logistic_regression | fpr_at_most_0.005 | 0.992523 | 0 | 0.0699656 | 0.00035675 | 0.164885 |
| logistic_regression | fpr_at_most_0.001 | 0.998332 | 0 | 0.0699656 | 0.00035675 | 0.164885 |
| random_forest | fixed_0_5 | 0.5 | 0 | 0.102001 | 0.021384 | 0.291775 |
| random_forest | maximum_binary_f1 | 0.106964 | 0.492232 | 0.102001 | 0.021384 | 0.291775 |
| random_forest | maximum_macro_f1 | 0.106964 | 0.492232 | 0.102001 | 0.021384 | 0.291775 |
| random_forest | fpr_at_most_0.01 | 0.173709 | 0.449612 | 0.102001 | 0.021384 | 0.291775 |
| random_forest | fpr_at_most_0.005 | 0.291775 | 3.54221e-06 | 0.102001 | 0.021384 | 0.291775 |
| random_forest | fpr_at_most_0.001 | 0.765834 | 0 | 0.102001 | 0.021384 | 0.291775 |
| xgboost | fixed_0_5 | 0.5 | 0 | 0.0329345 | 0.00858869 | 0.0755567 |
| xgboost | maximum_binary_f1 | 0.00913401 | 0.495392 | 0.0329345 | 0.00858869 | 0.0755567 |
| xgboost | maximum_macro_f1 | 0.00913401 | 0.495392 | 0.0329345 | 0.00858869 | 0.0755567 |
| xgboost | fpr_at_most_0.01 | 0.0944726 | 0 | 0.0329345 | 0.00858869 | 0.0755567 |
| xgboost | fpr_at_most_0.005 | 0.41608 | 0 | 0.0329345 | 0.00858869 | 0.0755567 |
| xgboost | fpr_at_most_0.001 | 0.874227 | 0 | 0.0329345 | 0.00858869 | 0.0755567 |
| mlp | fixed_0_5 | 0.5 | 0 | 0.000165549 | 2.41367e-09 | 0.000939129 |
| mlp | maximum_binary_f1 | 2.07041e-08 | 0.492661 | 0.000165549 | 2.41367e-09 | 0.000939129 |
| mlp | maximum_macro_f1 | 0.00346634 | 0 | 0.000165549 | 2.41367e-09 | 0.000939129 |
| mlp | fpr_at_most_0.01 | 0.0590479 | 0 | 0.000165549 | 2.41367e-09 | 0.000939129 |
| mlp | fpr_at_most_0.005 | 0.0968262 | 0 | 0.000165549 | 2.41367e-09 | 0.000939129 |
| mlp | fpr_at_most_0.001 | 0.812089 | 0 | 0.000165549 | 2.41367e-09 | 0.000939129 |

Bot vs training_benign:

| Feature | KS | PSI |
|---|---|---|
| Dst Port | 0.788576 | 9.97675 |
| Bwd Pkt Len Mean | 0.686046 | 7.14026 |
| Bwd Seg Size Avg | 0.686046 | 7.14026 |
| Pkt Size Avg | 0.608358 | 5.9835 |
| Fwd IAT Min | 0.548144 | 3.32635 |
| Flow Pkts/s | 0.543724 | 6.05791 |
| Flow IAT Mean | 0.541623 | 6.71831 |
| Fwd Pkts/s | 0.541258 | 5.45899 |
| Fwd IAT Tot | 0.518604 | 9.67029 |
| Init Fwd Win Byts | 0.518194 | 2.95448 |

Bot vs training_malicious:

| Feature | KS | PSI |
|---|---|---|
| Dst Port | 0.999086 | 0.430186 |
| Fwd IAT Tot | 0.761112 | 5.17671 |
| Fwd IAT Max | 0.750575 | 4.91183 |
| Fwd IAT Mean | 0.741404 | 5.50359 |
| Flow IAT Mean | 0.727259 | 5.23045 |
| Flow Pkts/s | 0.679727 | 5.0826 |
| Fwd IAT Min | 0.60715 | 6.46406 |
| Flow IAT Min | 0.599556 | 7.08098 |
| Fwd Pkts/s | 0.597046 | 5.20651 |
| Flow IAT Max | 0.566431 | 5.7735 |

## Interpretation and limits

- **Supervised training:** high aggregate in-sample ranking and recall rule out an aggregate failure to learn the training data; they do not establish generalization or learning of every rare family.
- **Known-family validation:** small samples show variable and often low recall, so failure is not restricted to families absent from training.
- **Unseen-family validation:** Infilteration has low fixed-threshold recall and generally weak discrimination against validation benign traffic.
- **Unseen-family test:** all attacks are from absent training families. Bot and Infilteration must be assessed separately; pooled metrics depend strongly on this mixture.
- **Ranking versus threshold:** especially for Random Forest, useful test ordering coexists with scores below 0.5. Validation-selected thresholds can recover detection with explicit false-positive tradeoffs; this is partial recovery, not a full solution.
- **Calibration:** validation probabilities are unreliable by the reported reliability/Brier diagnostics. No calibration model was fitted, and no test labels were used for calibration.
- **Feature shift:** exact marginal comparisons document distribution changes. They do not prove that any particular shifted feature caused the performance gap, and correlated features may repeat the same signal.
- **Causal attribution:** unseen-family composition, temporal shift, calibration/threshold mismatch and possible overfitting are not independently controlled here. The evidence supports a combination, not a uniquely identified cause. No new model or operating threshold is recommended based on test outcomes.

## Reproduction and outputs

Run `python -m src.phase4a.run` using the existing Phase 4 runtime. No `.fit` or `.partial_fit` call occurs in this phase. Completed training-inference and per-feature checkpoints can be reused. The input manifest and final integrity report protect pre-existing baseline artifacts. All requested CSVs reside in this directory; extra support tables retain threshold-grid values, reliability-bin counts, family ranking, full group summaries and feature rankings.

Histograms use fixed 0.01 score bins normalized within group and log frequency. ECDF displays use up to 4,000 deterministic order-statistic points per group with a symlog score axis (linear below 1e-12) to reveal low-score structure; numerical score summaries use all records. ROC and PR curves use full saved predictions.

### logistic_regression figures

![Score histograms](figures/score_distributions/logistic_regression_histograms.png)
![Score ECDF](figures/score_distributions/logistic_regression_ecdf.png)
![ROC](figures/roc_curves/logistic_regression.png)
![Precision recall](figures/pr_curves/logistic_regression.png)
![Validation calibration](figures/calibration/logistic_regression.png)
![Post-hoc test thresholds](figures/threshold_curves/logistic_regression.png)

### random_forest figures

![Score histograms](figures/score_distributions/random_forest_histograms.png)
![Score ECDF](figures/score_distributions/random_forest_ecdf.png)
![ROC](figures/roc_curves/random_forest.png)
![Precision recall](figures/pr_curves/random_forest.png)
![Validation calibration](figures/calibration/random_forest.png)
![Post-hoc test thresholds](figures/threshold_curves/random_forest.png)

### xgboost figures

![Score histograms](figures/score_distributions/xgboost_histograms.png)
![Score ECDF](figures/score_distributions/xgboost_ecdf.png)
![ROC](figures/roc_curves/xgboost.png)
![Precision recall](figures/pr_curves/xgboost.png)
![Validation calibration](figures/calibration/xgboost.png)
![Post-hoc test thresholds](figures/threshold_curves/xgboost.png)

### mlp figures

![Score histograms](figures/score_distributions/mlp_histograms.png)
![Score ECDF](figures/score_distributions/mlp_ecdf.png)
![ROC](figures/roc_curves/mlp.png)
![Precision recall](figures/pr_curves/mlp.png)
![Validation calibration](figures/calibration/mlp.png)
![Post-hoc test thresholds](figures/threshold_curves/mlp.png)
