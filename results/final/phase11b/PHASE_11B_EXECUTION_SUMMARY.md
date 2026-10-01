# Phase 11B execution summary

Status: **COMPLETE**. 20 mandatory and 5 self-only fits completed.

All five seeds were fitted freshly. Same-seed frozen GAT encoders supplied both temporal heads. No development fits substituted.

Independent metric/threshold/cohort/checkpoint verification passed. Protected artifacts unchanged.

Mean ± sample SD (ddof=1), test metrics; five completed seeds. Positive paired FPR differences mean more false alarms.

## gatv2 versus edge_mlp

| Operating point | Metric | Model mean ± SD | Control mean ± SD | Paired difference mean ± SD |
| --- | --- | --- | --- | --- |
| fixed_0_5 | recall | 0.993058 ± 0.010155 | 0.978233 ± 0.007097 | 0.014825 ± 0.009474 |
| fixed_0_5 | precision | 0.999719 ± 0.000119 | 0.995421 ± 0.002193 | 0.004299 ± 0.002156 |
| fixed_0_5 | f1 | 0.996357 ± 0.005163 | 0.986736 ± 0.002835 | 0.009621 ± 0.004972 |
| fixed_0_5 | macro_f1 | 0.998005 ± 0.002828 | 0.992735 ± 0.001550 | 0.005270 ± 0.002722 |
| fixed_0_5 | false_positive_rate | 0.000027 ± 0.000011 | 0.000435 ± 0.000213 | -0.000408 ± 0.000209 |
| fixed_0_5 | roc_auc | 0.999999 ± 0.000002 | 0.999963 ± 0.000013 | 0.000035 ± 0.000014 |
| fixed_0_5 | average_precision | 0.999984 ± 0.000017 | 0.999571 ± 0.000178 | 0.000413 ± 0.000189 |
| fpr_at_most_0.01 | recall | 0.966349 ± 0.008106 | 0.999968 ± 0.000072 | -0.033619 ± 0.008153 |
| fpr_at_most_0.01 | precision | 0.999900 ± 0.000091 | 0.960280 ± 0.031442 | 0.039620 ± 0.031493 |
| fpr_at_most_0.01 | f1 | 0.982825 ± 0.004230 | 0.979508 ± 0.016746 | 0.003316 ± 0.019744 |
| fpr_at_most_0.01 | macro_f1 | 0.990600 ± 0.002311 | 0.988731 ± 0.009239 | 0.001870 ± 0.010877 |
| fpr_at_most_0.01 | false_positive_rate | 0.000009 ± 0.000008 | 0.004079 ± 0.003436 | -0.004069 ± 0.003440 |
| fpr_at_most_0.01 | roc_auc | 0.999999 ± 0.000002 | 0.999963 ± 0.000013 | 0.000035 ± 0.000014 |
| fpr_at_most_0.01 | average_precision | 0.999984 ± 0.000017 | 0.999571 ± 0.000178 | 0.000413 ± 0.000189 |
| maximum_macro_f1 | recall | 0.966349 ± 0.008106 | 0.999594 ± 0.000700 | -0.033244 ± 0.008596 |
| maximum_macro_f1 | precision | 0.999900 ± 0.000091 | 0.978204 ± 0.004521 | 0.021696 ± 0.004467 |
| maximum_macro_f1 | f1 | 0.982825 ± 0.004230 | 0.988778 ± 0.002256 | -0.005954 ± 0.004434 |
| maximum_macro_f1 | macro_f1 | 0.990600 ± 0.002311 | 0.993841 ± 0.001239 | -0.003241 ± 0.002425 |
| maximum_macro_f1 | false_positive_rate | 0.000009 ± 0.000008 | 0.002150 ± 0.000457 | -0.002140 ± 0.000452 |
| maximum_macro_f1 | roc_auc | 0.999999 ± 0.000002 | 0.999963 ± 0.000013 | 0.000035 ± 0.000014 |
| maximum_macro_f1 | average_precision | 0.999984 ± 0.000017 | 0.999571 ± 0.000178 | 0.000413 ± 0.000189 |
## gatv2 versus gatv2_self_only

| Operating point | Metric | Model mean ± SD | Control mean ± SD | Paired difference mean ± SD |
| --- | --- | --- | --- | --- |
| fixed_0_5 | recall | 0.993058 ± 0.010155 | 0.980083 ± 0.023556 | 0.012975 ± 0.013683 |
| fixed_0_5 | precision | 0.999719 ± 0.000119 | 1.000000 ± 0.000000 | -0.000281 ± 0.000119 |
| fixed_0_5 | f1 | 0.996357 ± 0.005163 | 0.989826 ± 0.012142 | 0.006531 ± 0.007114 |
| fixed_0_5 | macro_f1 | 0.998005 ± 0.002828 | 0.994434 ± 0.006637 | 0.003571 ± 0.003883 |
| fixed_0_5 | false_positive_rate | 0.000027 ± 0.000011 | 0.000000 ± 0.000000 | 0.000027 ± 0.000011 |
| fixed_0_5 | roc_auc | 0.999999 ± 0.000002 | 0.999969 ± 0.000068 | 0.000029 ± 0.000067 |
| fixed_0_5 | average_precision | 0.999984 ± 0.000017 | 0.999746 ± 0.000564 | 0.000238 ± 0.000548 |
| fpr_at_most_0.01 | recall | 0.966349 ± 0.008106 | 0.989464 ± 0.001791 | -0.023115 ± 0.008399 |
| fpr_at_most_0.01 | precision | 0.999900 ± 0.000091 | 0.997632 ± 0.005296 | 0.002268 ± 0.005259 |
| fpr_at_most_0.01 | f1 | 0.982825 ± 0.004230 | 0.993529 ± 0.003523 | -0.010704 ± 0.005421 |
| fpr_at_most_0.01 | macro_f1 | 0.990600 ± 0.002311 | 0.996453 ± 0.001932 | -0.005853 ± 0.002966 |
| fpr_at_most_0.01 | false_positive_rate | 0.000009 ± 0.000008 | 0.000228 ± 0.000510 | -0.000219 ± 0.000506 |
| fpr_at_most_0.01 | roc_auc | 0.999999 ± 0.000002 | 0.999969 ± 0.000068 | 0.000029 ± 0.000067 |
| fpr_at_most_0.01 | average_precision | 0.999984 ± 0.000017 | 0.999746 ± 0.000564 | 0.000238 ± 0.000548 |
| maximum_macro_f1 | recall | 0.966349 ± 0.008106 | 0.989453 ± 0.001815 | -0.023104 ± 0.008403 |
| maximum_macro_f1 | precision | 0.999900 ± 0.000091 | 0.997706 ± 0.005130 | 0.002194 ± 0.005094 |
| maximum_macro_f1 | f1 | 0.982825 ± 0.004230 | 0.993560 ± 0.003453 | -0.010735 ± 0.005379 |
| maximum_macro_f1 | macro_f1 | 0.990600 ± 0.002311 | 0.996471 ± 0.001893 | -0.005871 ± 0.002942 |
| maximum_macro_f1 | false_positive_rate | 0.000009 ± 0.000008 | 0.000221 ± 0.000494 | -0.000211 ± 0.000490 |
| maximum_macro_f1 | roc_auc | 0.999999 ± 0.000002 | 0.999969 ± 0.000068 | 0.000029 ± 0.000067 |
| maximum_macro_f1 | average_precision | 0.999984 ± 0.000017 | 0.999746 ± 0.000564 | 0.000238 ± 0.000548 |
## gat_transformer_L8 versus gat_transformer_L1

| Operating point | Metric | Model mean ± SD | Control mean ± SD | Paired difference mean ± SD |
| --- | --- | --- | --- | --- |
| fixed_0_5 | recall | 0.997797 ± 0.002555 | 0.993475 ± 0.011465 | 0.004321 ± 0.012725 |
| fixed_0_5 | precision | 0.999560 ± 0.000180 | 0.999021 ± 0.000455 | 0.000539 ± 0.000431 |
| fixed_0_5 | f1 | 0.998677 ± 0.001340 | 0.996214 ± 0.005806 | 0.002463 ± 0.006428 |
| fixed_0_5 | macro_f1 | 0.999275 ± 0.000735 | 0.997926 ± 0.003179 | 0.001348 ± 0.003520 |
| fixed_0_5 | false_positive_rate | 0.000042 ± 0.000017 | 0.000094 ± 0.000044 | -0.000052 ± 0.000042 |
| fixed_0_5 | roc_auc | 0.999999 ± 8.318894e-07 | 0.999986 ± 0.000028 | 0.000013 ± 0.000028 |
| fixed_0_5 | average_precision | 0.999990 ± 0.000009 | 0.999871 ± 0.000267 | 0.000119 ± 0.000269 |
| fpr_at_most_0.01 | recall | 0.971355 ± 0.011803 | 0.971901 ± 0.003165 | -0.000546 ± 0.010508 |
| fpr_at_most_0.01 | precision | 0.999901 ± 0.000060 | 0.999835 ± 0.000202 | 0.000066 ± 0.000250 |
| fpr_at_most_0.01 | f1 | 0.985392 ± 0.006059 | 0.985668 ± 0.001604 | -0.000276 ± 0.005313 |
| fpr_at_most_0.01 | macro_f1 | 0.992004 ± 0.003312 | 0.992154 ± 0.000877 | -0.000149 ± 0.002904 |
| fpr_at_most_0.01 | false_positive_rate | 0.000009 ± 0.000006 | 0.000015 ± 0.000019 | -0.000006 ± 0.000023 |
| fpr_at_most_0.01 | roc_auc | 0.999999 ± 8.318894e-07 | 0.999986 ± 0.000028 | 0.000013 ± 0.000028 |
| fpr_at_most_0.01 | average_precision | 0.999990 ± 0.000009 | 0.999871 ± 0.000267 | 0.000119 ± 0.000269 |
| maximum_macro_f1 | recall | 0.971355 ± 0.011803 | 0.971901 ± 0.003165 | -0.000546 ± 0.010508 |
| maximum_macro_f1 | precision | 0.999901 ± 0.000060 | 0.999835 ± 0.000202 | 0.000066 ± 0.000250 |
| maximum_macro_f1 | f1 | 0.985392 ± 0.006059 | 0.985668 ± 0.001604 | -0.000276 ± 0.005313 |
| maximum_macro_f1 | macro_f1 | 0.992004 ± 0.003312 | 0.992154 ± 0.000877 | -0.000149 ± 0.002904 |
| maximum_macro_f1 | false_positive_rate | 0.000009 ± 0.000006 | 0.000015 ± 0.000019 | -0.000006 ± 0.000023 |
| maximum_macro_f1 | roc_auc | 0.999999 ± 8.318894e-07 | 0.999986 ± 0.000028 | 0.000013 ± 0.000028 |
| maximum_macro_f1 | average_precision | 0.999990 ± 0.000009 | 0.999871 ± 0.000267 | 0.000119 ± 0.000269 |

Individual seed results and all metrics are in per_seed_metrics.csv. No contribution is established solely by one favorable seed or operating point.

Seed variation measures training stochasticity on the fixed, previously observed Feb20 split. No significance tests or independent dataset replications are claimed.

Runtime: graph input construction is measured separately; fit residuals still include minibatch overhead. Head inference includes lookup. Shared encoder extraction is counted once per seed; history replay includes diagnostic counts and is shared across seeds. Raw cleaning/preprocessing/cache creation was not rerun; timings are not raw-data end-to-end serving latency. Pipeline memory is the maximum of separate measured stages, not their sum.

The initial restricted-process failure and successful existing-overlay recovery remain preserved. No packages were installed or changed during recovery. Environment checks ran inside every fit process.

STOP: no XAI, tuning, model changes, fusion changes, or paper rewriting was started.
