# Phase 5 integrity verification

| check | status |
| --- | --- |
| chronological_order_verified | PASS |
| common_target_records_across_lengths | PASS |
| labels_metadata_only | PASS |
| no_1970 | PASS |
| no_day_crossing | PASS |
| no_future_flow | PASS |
| no_partition_crossing | PASS |
| full_frozen_hash_verification | PASS |
| phase4_and_phase4a_unchanged | PASS |
| preprocessing_train_fitted_only | PASS |
| targets_and_families_excluded_from_features | PASS |
| timestamps_ordering_only | PASS |
| test_excluded_from_selection | PASS |
| thresholds_and_selected_models_verified | PASS |
| matched_baseline_targets | PASS |

Full verification rehashes original raw data, cleaned/quarantine artifacts and frozen membership through the Phase 4 guard. The pretraining integrity record and baseline snapshot preserve the earlier pretraining checks. The snapshot also protects Phase 4/4A results and source files. Evaluation records bind saved predictions to the model and operating-threshold lock. Partition chronology and day spans establish training/evaluation separation. The unchanged frozen preprocessing and feature list exclude labels, families and ordering metadata.

Thresholds were selected on matched validation predictions and frozen before held-out evaluation. Baseline models were not retrained; their existing saved prediction arrays were indexed by the exact same frozen partition row indices. Their 1% FPR thresholds are reselected on matched validation targets, not copied from a different cohort. A validation FPR cap is not a guarantee of the same test FPR.
