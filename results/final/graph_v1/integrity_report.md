# Graph experiment integrity

| check | status |
| --- | --- |
| split_explicitly_approved | PASS |
| original_artifacts_unchanged | PASS |
| preprocessing_train_only | PASS |
| identical_target_cohort | PASS |
| thresholds_frozen_before_test | PASS |
| primary_window_fixed | PASS |
| label_free_node_and_edge_features | PASS |
| history_completed_before_cutoff | PASS |
| partition_and_calendar_boundaries | PASS |
| saved_metrics_recomputed | PASS |
| seed_42_only | PASS |

Full evidence is in configs/split_approval.json, metrics/data_manifest.json, configs/threshold_lock.json, per-model histories/evaluations and metrics/integrity_verification.json. Protected earlier-phase artifact hashes were rechecked after report generation.
