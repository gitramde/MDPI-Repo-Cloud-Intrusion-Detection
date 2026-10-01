# Phase 6 seed-42 graph contribution results

Primary window: **1 minute**, declared before training. Selected GATv2: two layers, hidden dimension 128 total across four heads, dropout 0.2, epoch 3; validation macro-F1 0.999929. Two architectures were evaluated under a four-epoch ceiling and patience two. Model, epoch and threshold decisions used validation only. The selected architecture was held fixed for 5/10-minute sensitivity runs, which independently selected epochs and thresholds on validation.

The approved Feb-20 split uses 10:30 and 11:00 boundaries. This is within-day graph-contribution development on Benign versus DDoS attacks-LOIC-HTTP, not an unseen-attack or zero-day experiment. All comparisons below use identical target flows and newly fitted Feb-20 TRAIN preprocessing. Existing Phase 4 models/results were not used as comparison scores.

## Shared target cohort

| partition | approved_rows | target_edges | benign | malicious | target_coverage |
| --- | --- | --- | --- | --- | --- |
| train | 5507159 | 172984 | 168357 | 4627 | 0.031411 |
| validation | 727258 | 88782 | 54220 | 34562 | 0.122078 |
| test | 1714329 | 212591 | 193893 | 18698 | 0.124008 |

Targets come from each minute’s final 30 seconds, deterministically sampled at stride 16 in train and 4 in validation/test, resetting each minute. Metrics apply to this sampled cohort. Preprocessing uses every approved training row; model fitting uses only training target rows. Source-row cohort membership is saved and hashed.

## Matched test comparison

| model | criterion | recall | precision | f1 | macro_f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gatv2_w1_h128_p2 | fixed_0_5 | 1.000000 | 0.999786 | 0.999893 | 0.999941 | 0.000021 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | maximum_macro_f1 | 0.953578 | 0.999832 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | fpr_at_most_0.01 | 0.953578 | 0.999832 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| edge_mlp | fixed_0_5 | 0.979356 | 0.994893 | 0.987063 | 0.992913 | 0.000485 | 0.999959 | 0.999478 |
| edge_mlp | maximum_macro_f1 | 0.999947 | 0.975428 | 0.987535 | 0.993158 | 0.002429 | 0.999959 | 0.999478 |
| edge_mlp | fpr_at_most_0.01 | 1.000000 | 0.973043 | 0.986338 | 0.992500 | 0.002672 | 0.999959 | 0.999478 |
| logistic_regression | fixed_0_5 | 1.000000 | 0.560912 | 0.718698 | 0.839736 | 0.075490 | 0.997215 | 0.958451 |
| logistic_regression | maximum_macro_f1 | 1.000000 | 0.764057 | 0.866250 | 0.925568 | 0.029779 | 0.997215 | 0.958451 |
| logistic_regression | fpr_at_most_0.01 | 0.910525 | 0.900555 | 0.905513 | 0.948173 | 0.009696 | 0.997215 | 0.958451 |
| random_forest | fixed_0_5 | 0.998182 | 0.996796 | 0.997488 | 0.998623 | 0.000309 | 0.999999 | 0.999986 |
| random_forest | maximum_macro_f1 | 0.999840 | 0.994521 | 0.997173 | 0.998450 | 0.000531 | 0.999999 | 0.999986 |
| random_forest | fpr_at_most_0.01 | 1.000000 | 0.951407 | 0.975098 | 0.986315 | 0.004925 | 0.999999 | 0.999986 |
| xgboost | fixed_0_5 | 1.000000 | 0.999733 | 0.999866 | 0.999927 | 0.000026 | 1.000000 | 1.000000 |
| xgboost | maximum_macro_f1 | 1.000000 | 0.999038 | 0.999519 | 0.999736 | 0.000093 | 1.000000 | 1.000000 |
| xgboost | fpr_at_most_0.01 | 1.000000 | 0.999038 | 0.999519 | 0.999736 | 0.000093 | 1.000000 | 1.000000 |

## Graph contribution ablation

| model | criterion | recall | f1 | macro_f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gatv2_w1_h128_p2 | fixed_0_5 | 1.000000 | 0.999893 | 0.999941 | 0.000021 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | maximum_macro_f1 | 0.953578 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | fpr_at_most_0.01 | 0.953578 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| edge_mlp | fixed_0_5 | 0.979356 | 0.987063 | 0.992913 | 0.000485 | 0.999959 | 0.999478 |
| edge_mlp | maximum_macro_f1 | 0.999947 | 0.987535 | 0.993158 | 0.002429 | 0.999959 | 0.999478 |
| edge_mlp | fpr_at_most_0.01 | 1.000000 | 0.986338 | 0.992500 | 0.002672 | 0.999959 | 0.999478 |
| gatv2_self_only | fixed_0_5 | 0.991603 | 0.995784 | 0.997690 | 0.000000 | 1.000000 | 0.999996 |
| gatv2_self_only | maximum_macro_f1 | 0.990480 | 0.995217 | 0.997379 | 0.000000 | 1.000000 | 0.999996 |
| gatv2_self_only | fpr_at_most_0.01 | 0.990480 | 0.995217 | 0.997379 | 0.000000 | 1.000000 | 0.999996 |

Edge MLP uses only the current flow features, with a hidden width chosen to approximately match the selected GATv2 parameter count. GATv2 additionally has historical node aggregates and relational messages, so that pair alone cannot isolate message passing from extra historical information. The self-only control keeps the same architecture and historical node inputs but removes all inter-node message edges; this is the more direct test of relational message passing. Its unused edge-attention parameters remain in the checkpoint, so equal serialized parameter counts do not imply equal active degrees of freedom.

GATv2 minus control differences (positive FPR means more false alarms):

| control | criterion | recall | f1 | macro_f1 | false_positive_rate | average_precision |
| --- | --- | --- | --- | --- | --- | --- |
| edge_mlp | fixed_0_5 | 0.020644 | 0.012830 | 0.007028 | -0.000464 | 0.000512 |
| gatv2_self_only | fixed_0_5 | 0.008397 | 0.004109 | 0.002252 | 0.000021 | -0.000007 |
| edge_mlp | maximum_macro_f1 | -0.046369 | -0.011378 | -0.006200 | -0.002414 | 0.000512 |
| gatv2_self_only | maximum_macro_f1 | -0.036902 | -0.019060 | -0.010421 | 0.000015 | -0.000007 |
| edge_mlp | fpr_at_most_0.01 | -0.046422 | -0.010180 | -0.005542 | -0.002656 | 0.000512 |
| gatv2_self_only | fpr_at_most_0.01 | -0.036902 | -0.019060 | -0.010421 | 0.000015 | -0.000007 |

These are descriptive, single-seed comparisons. Improvements at one operating point do not establish an overall graph benefit, and no statistical significance is claimed.

## Window sensitivity

| window_minutes | criterion | recall | f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | fixed_0_5 | 1.000000 | 0.999893 | 0.000021 | 0.999999 | 0.999990 |
| 1 | maximum_macro_f1 | 0.953578 | 0.976157 | 0.000015 | 0.999999 | 0.999990 |
| 1 | fpr_at_most_0.01 | 0.953578 | 0.976157 | 0.000015 | 0.999999 | 0.999990 |
| 5 | fixed_0_5 | 1.000000 | 0.999679 | 0.000062 | 1.000000 | 0.999998 |
| 5 | maximum_macro_f1 | 0.990159 | 0.995029 | 0.000005 | 1.000000 | 0.999998 |
| 5 | fpr_at_most_0.01 | 0.990159 | 0.995029 | 0.000005 | 1.000000 | 0.999998 |
| 10 | fixed_0_5 | 0.990962 | 0.995407 | 0.000010 | 0.999998 | 0.999976 |
| 10 | maximum_macro_f1 | 0.989197 | 0.994516 | 0.000010 | 0.999998 | 0.999976 |
| 10 | fpr_at_most_0.01 | 0.989197 | 0.994516 | 0.000010 | 0.999998 | 0.999976 |

The 1-minute model remains primary regardless of sensitivity test performance. All windows use the same minute-level cutoffs and target cohort; sensitivity changes the available within-window history. Larger windows may hit the message-edge cap more often.

## Causality, scope and measurement limits

At each minute’s second-30 cutoff, history contains only flows starting inside the assigned calendar window and completing strictly before the cutoff. Equal-cutoff completions are excluded. Targets start at or after the cutoff and are classified at completion using their own complete flow vector. Calendar-window and partition membership use the frozen start timestamp; a target can complete after its start window ends, but its context remains frozen at the earlier cutoff. Node history and message passing cannot use target labels, target-flow data, future flows or other partitions. Validation/test histories may use earlier unlabeled completed flows within their own partition. No future-window node universe is supplied. This is flow-completion detection, not prediction at flow start.

Node statistics use all eligible history, while message edges retain the 8,192 most recently completed eligible flows (source-row tie break). Nodes irrelevant to retained messages and targets are pruned after aggregation. Thus this tests a bounded historical network-flow graph instantiation of the generalized AIGT-CTD architecture, not exhaustive graph processing or the full AIGT-CTD system. Directed edges follow Source IP to Destination IP; IP indices are topology keys, never numeric/learned identity features.

graph_snapshot_diagnostics.csv describes complete calendar-window topology using all cleaned flows for descriptive diagnostics only; those complete graphs are never training inputs. Density counts unique non-self directed pairs divided by n(n−1), not parallel edges. Components are reported both weakly and strongly. Isolated-node count is zero by the full-window endpoint-defined node universe. causal_prefix_diagnostics.csv separately describes actual historical model inputs, caps and cold endpoints. Summaries include mean, median, p90 and maximum.

All metric tables include Accuracy, Precision, Recall, F1, Macro-F1, ROC-AUC, trapezoidal PR-AUC, Average Precision, FPR, FNR and confusion counts. Thresholds are fixed 0.5, validation maximum macro-F1, and validation FPR ≤1%; the cap is not a test FPR guarantee. Conventional controls are newly fitted on the same sampled targets: logistic-loss SGD, Random Forest, XGBoost, and the edge MLP.

Runtime measurements include graph-prefix preparation and model compute during inference but exclude raw joining, preprocessing/cache creation and model loading. data_manifest.json records the completed resumed materialization pass, not total preparation cost including earlier cache creation and timestamp-unit repair. Latency is milliseconds per 1,000 evaluated target edges. Peak memory is process working-set/RSS including dependencies and cached metadata; training peaks repeat across partition rows and should not be summed. CPU timings are machine-specific. Training histories and all searched configurations are saved.

The same attack episode spans partitions, endpoints may recur, and prevalence differs sharply. The sparse target schedule, four-epoch budget and message cap limit generalization of findings. Frozen timestamps are preserved without AM/PM repair. Baseline_v1, Phase 4/4A and Phase 5 artifacts remain unchanged. No Transformer, anomaly/reconstruction branch, explainability, risk fusion or final five-seed run was introduced.

## Start-time split versus completion-time availability

| partition | next_partition_start | flows_completing_at_or_after_boundary | target_flows_completing_at_or_after_boundary | latest_completion |
| --- | --- | --- | --- | --- |
| train | 2018-02-20 10:30:00 | 6097 | 253 | 2018-02-20 10:31:58.325414 |
| validation | 2018-02-20 11:00:00 | 5397 | 832 | 2018-02-20 11:01:57.559507 |

The approved membership is based on flow start timestamps, so some earlier-partition flows finish after the next partition starts. No later-partition record is fitted, and every message/node context is completion-causal, but these results are an offline benchmark under the approved start-time split, not proof that a freshly trained model could be deployed exactly at the boundary. A strict deployment replay would need a separately approved completion-time purge/embargo and fresh preprocessing; that would change the approved membership and was not silently substituted here.
