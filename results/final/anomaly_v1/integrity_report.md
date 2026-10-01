# Phase 7 integrity

| check | status |
| --- | --- |
| frozen_data_hashes_verified | PASS |
| prior_phases_unchanged | PASS |
| full_benign_train_used_by_every_AE_epoch | PASS |
| representation_fit_train_only | PASS |
| preprocessing_unchanged | PASS |
| labels_excluded_from_inputs | PASS |
| architecture_and_early_stopping_benign_validation_only | PASS |
| protocol_A_benign_calibration_only | PASS |
| protocol_A_locked_before_malicious_scoring | PASS |
| protocol_B_explicitly_label_aware | PASS |
| test_excluded_from_selection | PASS |
| full_matched_test_cohort | PASS |
| seed_42_only | PASS |

Evidence: anomaly_training_manifest.json, configs/protocol.json, both calibration locks, complete epoch histories, per-model training/scoring manifests and metrics/integrity_verification.json. Original preprocessing was fitted on all TRAIN classes; it was not refitted or represented as benign-only.
