# Phase 5 seed-42 development results

Selected length 64, d_model 64, 2 encoder layers, 4 attention heads, dropout 0.1; epoch 1, validation macro-F1 0.544573. Four temporal configurations were evaluated, followed by one capacity-matched Transformer-L1 control. All configurations used at most three epochs, patience two, AdamW and class weighting derived only from training targets.

Validation malicious traffic is dominated by UNSEEN Infilteration. Selection therefore measures later-period temporal generalization, not ordinary IID classification. Test outcomes were not used for model, sequence-length, epoch or threshold selection.

## Matched-cohort test comparison

| model | criterion | recall | precision | f1 | false_positive_rate | roc_auc | average_precision | Bot_recall | Infilteration_recall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logistic_regression | fixed_0_5 | 0.008390 | 0.059670 | 0.014712 | 0.049754 | 0.551978 | 0.347629 | 0.000000 | 0.033872 |
| logistic_regression | fpr_at_most_0.01 | 0.001256 | 0.055089 | 0.002457 | 0.008109 | 0.551978 | 0.347629 | 0.000000 | 0.005072 |
| random_forest | fixed_0_5 | 0.000831 | 0.095823 | 0.001647 | 0.002949 | 0.832675 | 0.676428 | 0.000000 | 0.003353 |
| random_forest | fpr_at_most_0.01 | 0.349653 | 0.939571 | 0.509646 | 0.008462 | 0.832675 | 0.676428 | 0.457595 | 0.021836 |
| xgboost | fixed_0_5 | 0.003599 | 0.267405 | 0.007102 | 0.003710 | 0.555924 | 0.532898 | 0.000000 | 0.014529 |
| xgboost | fpr_at_most_0.01 | 0.005984 | 0.209233 | 0.011635 | 0.008510 | 0.555924 | 0.532898 | 0.000000 | 0.024157 |
| mlp | fixed_0_5 | 0.001618 | 0.319328 | 0.003221 | 0.001298 | 0.776280 | 0.516340 | 0.000000 | 0.006534 |
| mlp | fpr_at_most_0.01 | 0.004089 | 0.170819 | 0.007986 | 0.007468 | 0.776280 | 0.516340 | 0.000000 | 0.016506 |
| transformer_L64_d64_n2_p01 | fixed_0_5 | 0.026939 | 0.479167 | 0.051010 | 0.011018 | 0.720339 | 0.421357 | 0.003878 | 0.096974 |
| transformer_L64_d64_n2_p01 | fpr_at_most_0.01 | 0.014694 | 0.417929 | 0.028390 | 0.007701 | 0.720339 | 0.421357 | 0.000000 | 0.059319 |

## Transformer-L1 control at threshold 0.5

| model | partition | recall | precision | f1 | macro_f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| transformer_L64_d64_n2_p01 | test | 0.026939 | 0.479167 | 0.051010 | 0.445432 | 0.011018 | 0.720339 | 0.421357 |
| transformer_L64_d64_n2_p01 | validation | 0.083121 | 0.193514 | 0.116290 | 0.544573 | 0.015072 | 0.542771 | 0.060457 |
| transformer_L1_control | test | 0.022360 | 0.395331 | 0.042327 | 0.440328 | 0.012869 | 0.761902 | 0.456778 |
| transformer_L1_control | validation | 0.081844 | 0.174462 | 0.111418 | 0.541672 | 0.016849 | 0.514076 | 0.059133 |

Temporal minus L1 test differences at 0.5: recall +0.004579, macro-F1 +0.005105, AP -0.035421. These descriptive differences do not establish a reliable temporal-context benefit or statistical significance.

## Interpretation and measurement limits

This bounded, CPU-only, single-seed development run uses sparse target coverage and a three-epoch budget. Findings are conditional on that budget and cohort; they do not establish an optimized Transformer result. Family diagnostics mark training presence as KNOWN/UNSEEN and leave absent-family recall blank. Unseen families are not characterized as zero-day attacks. All five operating points are in validation_metrics.csv and test_metrics.csv; PR-AUC is trapezoidal precision-recall area, while AP is reported separately. Confusion-matrix columns are TN, FP, FN and TP.

runtime_metrics.csv separates training, validation selection, feature loading and inference. Inference latency is milliseconds per 1,000 evaluated target flows, including historical-window processing; end-to-end timing additionally includes frozen feature transformation. Peak memory is process peak working set/RSS, not parameter memory, and includes loaded feature arrays. Serialized size is checkpoint bytes. Training measurements repeat across the two evaluation partitions and must not be summed twice.

All tables and figures are generated programmatically from saved experiment outputs. No Phase 4/4A artifacts were modified. No graph, GATv2, anomaly branch, explainability, risk fusion, full AIGT-CTD or final five-seed experiment was introduced.
