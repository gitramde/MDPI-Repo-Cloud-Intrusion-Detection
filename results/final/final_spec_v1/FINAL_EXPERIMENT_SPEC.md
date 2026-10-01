# FINAL EXPERIMENT SPECIFICATION — final_spec_v1

**FROZEN; EXECUTION NOT AUTHORIZED. Phase10 performs no training.** Await explicit approval before the final seed42 rerun or seeds123/456/789/1024. All development artifacts are protected.

## Frozen roster and dependencies

| model | cohort | final status | dependency |
| --- | --- | --- | --- |
| logistic_regression | full_dataset | five_seed_required |  |
| random_forest | full_dataset | five_seed_required |  |
| xgboost | full_dataset | five_seed_required |  |
| mlp | full_dataset | five_seed_required |  |
| transformer_L1 | phase5_matched | five_seed_required |  |
| transformer_L64 | phase5_matched | five_seed_required |  |
| edge_mlp | feb20_matched | five_seed_required |  |
| gatv2 | feb20_matched | five_seed_required |  |
| gatv2_self_only | feb20_matched | five_seed_planned_resource_conditional |  |
| gat_transformer_L1 | feb20_matched | five_seed_required | gatv2[s] |
| gat_transformer_L8 | feb20_matched | five_seed_required | gatv2[s] |
| autoencoder_B | full_dataset | five_seed_required |  |
| isolation_forest | full_dataset | development_seed42_secondary_only | existing Phase7 |
| rf_or_ae | full_dataset | derived_no_training | random_forest[s];autoencoder_B[s] |

Every stochastic configuration is freshly fitted under42,123,456,789,1024 with the same bounded training/validation rules. Seed42 development is not reused as a final fit. Architecture search is disabled; checkpoint selection within the frozen budget remains validation-only per seed. Each graph-temporal head uses its own seed GAT encoder, frozen after that encoder’s validation selection. RF–AE fusion uses matching seed-specific predictions and recalibrated component thresholds. Numeric development thresholds are not copied across seeds.

Self-only is planned for all five seeds, subject only to documented resource feasibility. L4, alternative graph windows, IF retraining and weighted/MAX fusion are excluded from final fitting. This roster is recorded before additional seeds. Original Phase9 coverage-gate revision remains a development limitation; exact cohort/history identities and masking are now fixed, with no further gate relaxation.

## Dataset/cohort separation

Full-data TRAIN/validation/test contain12,795,136 /1,652,943 /1,374,143 rows. Phase5 matched targets contain99,962 /206,603 /171,753. Feb20 graph and graph-temporal targets contain172,984 /88,782 /212,591. All IDs and order remain fixed. Do not compare metrics from different cohorts as component ablations. Full-data baseline predictions are sliced and thresholds recalibrated on the Phase5 matched validation cohort for temporal comparisons. Graph controls are independently fitted under the Feb20 TRAIN-only preprocessing, never reused from full-data Phase4 fits.

Baseline cleaning and preprocessing are immutable; full-data preprocessing used all TRAIN classes. AE fitting alone is benign-only. Full-data split dates and every feature, category, imputation and scaling value are embedded below. The graph start-time split is before10:30/[10:30,11:00)/from11:00 on Feb20, with completion-causal graph and temporal history and the original split-boundary limitations. Phase5 uses start-ordered global flow sequences; do not relabel it as completion-causal deployment replay.

## Thresholds, metrics and statistical interpretation

Positive class is malicious; negative class is Benign. Detection is score >= threshold. On each identical cohort and seed, save TN, FP, FN, TP and N as integer counts.

| Metric | Definition |
| --- | --- |
| Accuracy | (TP + TN) / N |
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1 | 2 TP / (2 TP + FP + FN) |
| Macro-F1 | mean of malicious F1 and 2 TN / (2 TN + FP + FN) |
| FPR | FP / (FP + TN) |
| FNR (supplementary) | FN / (FN + TP) |
| ROC-AUC | sklearn roc_auc_score on the continuous malicious-oriented score, ties handled by its ranking implementation |
| PR-AUC | sklearn auc(recall, precision) from precision_recall_curve; trapezoidal area |
| Average Precision | sklearn average_precision_score; not interchangeable with trapezoidal PR-AUC |
| Family recall | detected malicious rows of the family / all evaluated rows of that family |

For zero denominators, binary classification ratios are 0, matching the frozen metric implementation. Absent family recall is null with N=0, not 0. ROC/PR/AP require both classes; record null and reason otherwise. Raw AE error is a score, not a probability. No clipping or percentile transform is introduced for final AE/OR reporting.

Report each metric for each seed, model, cohort, partition and operating criterion. Report arithmetic mean and sample standard deviation (ddof=1) over the five completed seeds; retain full-precision values, use six decimals for display and scientific notation for small differences. Report number of completed seeds. Do not silently drop failures or substitute development results. A planned five-seed result is incomplete until all five exist. IF remains a single development-seed row without a fabricated standard deviation.

The fixed split and target records are shared across seeds. Seed variation measures training stochasticity only, not dataset or split uncertainty. Five seeds are not five independent dataset replications. Do not pool repeated targets or average confusion counts as independent datasets; retain per-seed confusion matrices. Compute metrics per seed before mean/std aggregation. No significance tests, confidence intervals, or confirmatory claims are predeclared.

For component contribution, save within-seed signed differences and their mean/sample SD: graph minus edge MLP, graph minus self-only if available, temporal-L64 minus temporal-L1, and graph-temporal-L8 minus graph-temporal-L1. Include recall, precision, F1, macro-F1, FPR, ROC-AUC and AP at every shared operating point. Positive FPR differences mean more false alarms. Do not claim incremental benefit from one favorable operating point alone.

Bot and Infilteration diagnostics apply to full-data and Phase5 matched cohorts. Both families are absent from full TRAIN; Infilteration is present in validation. Supervised validation selection is therefore label-aware for this family. Feb20 tests only Benign versus DDoS attacks-LOIC-HTTP, not unseen-family detection. Preserve the literal dataset spelling Infilteration.

OR is a binary decision, not a new fitted ranking score. Its ROC-AUC, trapezoidal PR-AUC and AP, if displayed to complete the metric schema, use the 0/1 decision and are explicitly marked binary-decision ranking. Do not compare that AP as equivalent to continuous RF/AE ranking AP. Report actual test FPR, Bot/Infilteration recall, and RF-only/AE-only/both/neither detections and Jaccard by family at the component 1% points. Jaccard is intersection/union, null for empty union. Component caps do not guarantee a 1% OR union FPR.

## Frozen research questions

**RQ1:** How effectively do conventional and neural flow-based models detect malicious traffic under chronological distribution shift?

**RQ2:** How effectively do models detect attack families absent from the training period, particularly Bot and Infilteration?

**RQ3:** Does graph-based relational modeling improve DDoS detection over matched non-graph controls on the Feb-20 network-flow graph subset?

**RQ4:** Does explicit temporal context provide incremental benefit over capacity-matched non-temporal controls?

**RQ5:** Does a benign-trained reconstruction anomaly branch provide complementary detection behavior for attack families absent from training?

**RQ6:** What computational overhead is introduced by graph, temporal and anomaly components?

Use “attack families absent from training” for empirical full-dataset claims. No zero-day-detection claim. RQ3 concerns only the Feb20 within-day binary graph subset.

## Frozen interpretation

1. Conventional supervised models can fit known training distributions extremely well but generalization varies substantially across later attack families.

2. Graph modeling achieves highly accurate LOIC-HTTP detection on the Feb-20 benchmark, but incremental graph benefit over strong controls is operating-point dependent.

3. Temporal context did not show a consistent incremental benefit in either the full-dataset temporal experiment or graph-temporal experiment.

4. Benign-trained reconstruction anomaly detection provides complementary family-specific detections but weak aggregate performance at strict false-positive control.

5. Simple risk fusion does not establish overall superiority under comparable false-alarm control.

These are development interpretations, not outcomes that final data must reproduce. Update numerical estimates and report any contrary evidence honestly; do not tune architectures post hoc to change their direction or suppress inconsistent results. The model roster, selection/calibration algorithms and exclusions remain frozen. All test cohorts were previously observed; final multi-seed evaluation measures stochastic stability on these fixed splits, not a new confirmatory holdout.

## Execution order, runtime and approval gate

Status: specification frozen; execution awaits explicit user approval. No final model was trained in Phase10, including seed42. Seeds123/456/789/1024 were not executed.

1. After explicit approval, build a separate final runner/output tree (proposed `results/final_runs_v1/seed_<s>/`), retaining this spec and every development artifact unchanged. Existing development entry points hard-code seed42, write old paths and may reopen searches; do not launch them as final runners. Copy/adapt only the frozen algorithms into new code, parameterize RNG/epoch shuffle/output paths and remove all architecture searches. Verify behavior with semantic tests before fitting. The freeze itself is not authorization to implement or execute final training now.
2. Verify artifact_hash_manifest.csv, the specification hash, exact library versions, CPU/RAM/device/thread settings, frozen feature dimensions, membership order and all cohort/history IDs. Check invariants and masks. No data or preprocessing refit. Refuse silent version drift: preparation sklearn1.6.1 state is reused transform-only; modeling requires recorded sklearn1.7.2. Snapshot final runner source and effective configs before the first fit. Record and stop on a mismatch.
3. For seeds in order42,123,456,789,1024, train only the frozen four full-data supervised models with their original bounded validation-checkpoint procedures. Fresh seed42 replaces nothing in development. Save configs, stage histories, checkpoints, scores, hashes, TRAIN-derived weights, exact target IDs and environment.
4. For each seed, train only Phase5-style Transformer-L64 and L1 on the frozen matched targets. Filter same-seed full-data conventional predictions to those target IDs and recalibrate their matched-validation FPR threshold. Never refit conventional models to the sampled temporal cohort.
5. For each seed, train the Feb20 Edge MLP and selected GAT architecture from scratch; retain self-only GAT across all five seeds if feasible under the fixed resource rule. Use only the one-minute primary graph. The 5/10-minute seed42 studies remain sensitivity results.
6. Freeze that seed's selected GAT checkpoint, extract that seed's graph representations and fit graph-temporal L1 and L8 heads. Both heads share the same frozen encoder and fixed history indices. Rebuild representations per seed; never reuse Phase9 seed42 embeddings for other seeds. No end-to-end fine-tuning; no L4 run. Shared prepared IDs/history may be reused only after checksum verification.
7. For each seed, train only AE-B on every benign TRAIN record under the frozen block/minibatch ordering and benign-validation reconstruction selection. Lock Protocol-A caps without malicious labels. Do not train AE-A or IF. Retain original IF only as single-seed development evidence.
8. Freeze seed-specific model and threshold locks before test evaluation. Threshold rules and cohorts are fixed; numerical thresholds and validation-selected checkpoints may differ across seeds. Derive RF, AE and OR component comparison from matching-seed full-cohort predictions at their approximately1% validation operating points. No alpha/normalization/union-threshold optimization.
9. Store individual seed metric/family/confusion/runtime rows and paired component deltas. Produce mean and sample SD only after all five required runs exist. Validate outputs by recomputing metrics from saved scores, checking cohort equality and all provenance hashes. Do not pool repeated test rows as independent data. No new model decisions from seed outcomes.
10. Stop after the approved frozen final evaluation. Any subsequent design change requires a separately versioned experiment and explicit approval, with old evidence retained. A resource failure is logged, not resolved by performance-driven seed/model substitution.

Expected workload after approval:55 mandatory fits (11 configurations ×5 seeds), plus5 planned resource-conditional self-only fits. OR adds no fitting. Encoder fits are reused by both graph-temporal heads, not duplicated. IF and other excluded development ablations add no final fits.

Save per seed: effective configuration, source/environment hashes, checkpoint and score hashes, selected epoch/step, full training/validation histories, threshold lock, target IDs, validation/test metrics, per-family N/detected/recall, confusion counts, component deltas, RF–AE overlap/Jaccard, runtime stage measurements, peak memory and serialized sizes. Keep audit logs separate from metric data. No overwriting or automatic resume from a development artifact; final-stage resume requires matching seed/config/input hashes.

Runtime is CPU-only on the recorded i7-8565U/16.94GB machine, two math/PyTorch threads and RF n_jobs1, one fitting process at a time. The machine/software and stage definitions are fully embedded below. Distinguish fitting from checkpoint selection and preparation, model compute from complete inference, and head size from shared-encoder pipeline size. Explicitly include separately measured history-index preparation; no unqualified comparisons across full-flow, sampled temporal and graph cohorts.

## Complete machine-readable configuration embedded for reproduction

The following is the complete JSON specification, not a selection based on test performance. “s” denotes the current seed. Source paths and SHA-256 values identify the immutable data/code required by these algorithms. Historical fields in provenance snapshots (including a pre-split proposal marked approved=false and old development method lists) describe earlier artifacts only: the explicit approved split record and final model registry/normalized protocols govern final execution. No new search is authorized by a historical field.

```json
{
  "artifact_hash_manifest": {
    "bytes": 199838,
    "path": "results/final_spec_v1/artifact_hash_manifest.csv",
    "sha256": "384904d39ad96fe65626ebfb531507e2637fc9a62dc25c3307fb0b2b67dd391b"
  },
  "claim_freeze": [
    "Conventional supervised models can fit known training distributions extremely well but generalization varies substantially across later attack families.",
    "Graph modeling achieves highly accurate LOIC-HTTP detection on the Feb-20 benchmark, but incremental graph benefit over strong controls is operating-point dependent.",
    "Temporal context did not show a consistent incremental benefit in either the full-dataset temporal experiment or graph-temporal experiment.",
    "Benign-trained reconstruction anomaly detection provides complementary family-specific detections but weak aggregate performance at strict false-positive control.",
    "Simple risk fusion does not establish overall superiority under comparable false-alarm control."
  ],
  "created_at_utc": "2026-09-21T22:51:52Z",
  "data": {
    "anomaly_training_manifest": {
      "artifacts": [
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\anomaly_v1\\benign_train_ids.npy",
          "sha256": "57c051e352942b48a6edeb0ad0c8ea36cfa60e6d11a5ca9d2fd48001ace478a4"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\anomaly_v1\\isolation_train_ids.npy",
          "sha256": "6d7613befc31bdf01566515e16ee594cfa6e69833feae83020746b991856d906"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\anomaly_v1\\benign_validation_features.npy",
          "sha256": "e14932d20d653d82ef57186c41351c2f3a4761e101078df4536e05a30b266cf3"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\anomaly_v1\\configs\\protocol.json",
          "sha256": "923a58291ca8ad9ebfedfacec03caf08b0fec98d811730c03a6073bfe3295b83"
        }
      ],
      "autoencoder_subsampled": false,
      "autoencoder_training_rows": 10885643,
      "benign_ids_sha256": "57c051e352942b48a6edeb0ad0c8ea36cfa60e6d11a5ca9d2fd48001ace478a4",
      "benign_train_rows": 10885643,
      "benign_validation_rows": 1583520,
      "isolation_forest_fit_rows": 250000,
      "isolation_forest_tree_subsample": 256,
      "isolation_sample_sha256": "6d7613befc31bdf01566515e16ee594cfa6e69833feae83020746b991856d906",
      "label_use": "binary labels only identify benign fitting/calibration cohorts; no labels in reconstruction objective or Isolation Forest fit",
      "partitions": {
        "test": {
          "dates": [
            "2018-03-01",
            "2018-03-02"
          ],
          "membership_sha256": "c51988409cf084b0656f7985a2a51c44aac5944f357c01356e5c21b5999eb95b",
          "rows": 1374143
        },
        "train": {
          "dates": [
            "2018-02-14",
            "2018-02-15",
            "2018-02-16",
            "2018-02-20",
            "2018-02-21",
            "2018-02-22"
          ],
          "membership_sha256": "3478533e80f58c092372361051d9f7b83199f284a5d57af2549f6d74051e9ecd",
          "rows": 12795136
        },
        "validation": {
          "dates": [
            "2018-02-23",
            "2018-02-28"
          ],
          "membership_sha256": "2bdd932fb3155c492619faf9a01af18e6862b13e8b72225f61cc6ead36084f28",
          "rows": 1652943
        }
      },
      "preprocessing_sha256": "7a7e15a52108b0ef165481baaf9833c88c42e8c246a612f6846db2b0f2ae565a",
      "seed": 42,
      "status": "PASS",
      "train_rows": 12795136,
      "training_cache_sha256": "37a9e9899647b0e61c2f4db4846f1b03a80fe67d8931af078ffcc5a556599d38"
    },
    "baseline_training_cache_manifest": {
      "creation_seconds": 154.89708509999946,
      "dtype": "float32",
      "features": 80,
      "frozen_float64_transform_sha256": "8c459aade75ef45925b2b8c04ec79c7e6b907522e3a45d42ae9baec3d6e40523",
      "note": "Model-input dtype conversion only; frozen float64 transform checksum exactly matches Phase 3.",
      "preprocessing_sha256": "7a7e15a52108b0ef165481baaf9833c88c42e8c246a612f6846db2b0f2ae565a",
      "rows": 12795136,
      "x_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\phase4_cache\\train_float32.dat",
      "x_sha256": "37a9e9899647b0e61c2f4db4846f1b03a80fe67d8931af078ffcc5a556599d38",
      "y_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\phase4_cache\\train_y_uint8.dat",
      "y_sha256": "bc36529299436f0c31eaf979f5419a401b8d7e7593f5ff95aed46290150e5ced"
    },
    "cleaning_configuration": {
      "all_missing_numeric_fill": 0.0,
      "batch_size": 50000,
      "benign_label": "Benign",
      "categorical_columns": [
        "Protocol"
      ],
      "data_dir": "data/baseline_v1",
      "expected_raw_files": 10,
      "expected_totals": {
        "exact_nonheader_duplicates": 410707,
        "raw_rows": 16233002,
        "repeated_headers": 59,
        "temporal_rows": 15822222,
        "year_1970_temporal_exclusions": 14
      },
      "imputation": "training_mean",
      "infinity_to_nan": [
        "Flow Byts/s",
        "Flow Pkts/s"
      ],
      "metadata_only_columns": [
        "Label",
        "Timestamp",
        "Flow ID",
        "Src IP",
        "Dst IP",
        "Src Port"
      ],
      "raw_dir": "data/raw/Processed Traffic Data for ML Algorithms",
      "report_dir": "results/baseline_v1",
      "scaling": "training_standard_scaler",
      "schema_version": 1,
      "seed": 20260920,
      "split": {
        "minimum_benign_per_partition": 100,
        "minimum_malicious_per_partition": 100,
        "minimum_test_dates": 2,
        "minimum_train_dates": 3,
        "minimum_validation_dates": 1,
        "target_fractions": [
          0.8,
          0.1,
          0.1
        ]
      },
      "target": "binary",
      "unknown_category": "all_zero_one_hot"
    },
    "cleaning_semantics": "Exact full-row duplicates removed per file (hash collision resolved by tuple equality), repeated headers removed, source row IDs retained. Parse %d/%m/%Y %H:%M:%S without AM/PM repair. Invalid/date-mismatched/1970 timestamps quarantined rather than repaired. Missing tokens normalized; infinities only in configured rate columns become missing. Numeric values float64; categorical Protocol string; chronological sort timestamp/source_row within file. Reuse exact cleaned files and partition membership; no cleaning/split rerun.",
    "full_dataset_counts": {
      "test": 1374143,
      "train": 12795136,
      "validation": 1652943
    },
    "full_preprocessing": {
      "all_missing_numeric_columns": [],
      "all_missing_numeric_fill": 0.0,
      "categorical_columns": [
        "Protocol"
      ],
      "categorical_imputation_values": {
        "Protocol": "6"
      },
      "categories": {
        "Protocol": [
          "0",
          "17",
          "6"
        ]
      },
      "constant_training_numeric_columns": [
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "CWE Flag Count",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg"
      ],
      "environment": {
        "numpy": "2.1.3",
        "pandas": "2.2.3",
        "pyarrow": "19.0.0",
        "python": "3.13.5",
        "scikit_learn": "1.6.1"
      },
      "excluded_target_encodings": [],
      "fit_partition": "train",
      "fitting_order": "Chronological files and recorded timestamps; original source_row breaks timestamp ties.",
      "materialization": "Transform batches on demand; no second full scaled feature copy.",
      "numeric_columns": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min"
      ],
      "numeric_imputation_strategy": "training_mean",
      "numeric_imputation_values": [
        9560.48577647006,
        12022910.892056404,
        28.358745385746584,
        6.177367243302455,
        1119.4709750642744,
        4523.449719877929,
        210.32272732388307,
        11.168756080435566,
        52.175493687300985,
        75.14887894537749,
        361.06164201771674,
        27.09353069791521,
        116.55903613364532,
        137.40298361226934,
        266851.3776954958,
        30921.820386941115,
        3112317.6040494344,
        1030213.4918212147,
        5962194.9819422,
        2660787.9752793564,
        11739942.595281754,
        3454253.8062445354,
        1170181.523087483,
        5775706.810387088,
        2751964.789711731,
        7703099.466347603,
        872962.8039375037,
        876288.1545217041,
        2700299.946935304,
        325674.9500223366,
        0.04516825768792141,
        0.0,
        0.0,
        0.0,
        296.34253641383725,
        131.24397489796124,
        26394.509569459722,
        4341.470114722967,
        11.041200187321182,
        406.14656655466575,
        80.06311862812811,
        127.40198584212952,
        43093.18031326028,
        0.004881698795542306,
        0.04516825768792141,
        0.19049910841119624,
        0.3778021585702567,
        0.340538701581601,
        0.03762593848162302,
        0.0,
        0.19049988995818412,
        0.47734584454592743,
        92.4647739649114,
        52.175493687300985,
        116.55903613364532,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        28.358745385746584,
        1119.4709750642744,
        6.177367243302455,
        4523.449719877929,
        8885.106879676778,
        8726.71368909248,
        24.72554250302615,
        17.721451026390028,
        180059.56435820018,
        90912.67634544165,
        272580.43065779057,
        119535.79719754444,
        4578977.525318113,
        153369.5203686486,
        4709596.422727355,
        4435482.15045014
      ],
      "numeric_observed_counts": [
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12718237,
        12718237,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136,
        12795136
      ],
      "output_feature_names": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min",
        "Protocol=0",
        "Protocol=17",
        "Protocol=6"
      ],
      "scaler_mean": [
        9560.485776470055,
        12022910.892056404,
        28.358745385746584,
        6.177367243302452,
        1119.4709750642746,
        4523.449719877925,
        210.3227273238831,
        11.16875608043557,
        52.17549368730097,
        75.14887894537745,
        361.06164201771657,
        27.09353069791521,
        116.55903613364532,
        137.40298361226942,
        266851.3776954949,
        30921.82038694092,
        3112317.604049435,
        1030213.491821215,
        5962194.9819422,
        2660787.9752793573,
        11739942.595281744,
        3454253.806244534,
        1170181.5230874843,
        5775706.810387082,
        2751964.7897117306,
        7703099.466347603,
        872962.8039375037,
        876288.1545217041,
        2700299.9469353044,
        325674.9500223367,
        0.04516825768792141,
        0.0,
        0.0,
        0.0,
        296.34253641383725,
        131.24397489796112,
        26394.509569459722,
        4341.470114722967,
        11.041200187321182,
        406.1465665546659,
        80.06311862812811,
        127.40198584212955,
        43093.18031326024,
        0.0048816987955423085,
        0.04516825768792141,
        0.19049910841119624,
        0.3778021585702567,
        0.340538701581601,
        0.03762593848162298,
        0.0,
        0.19049988995818412,
        0.4773458445459274,
        92.4647739649114,
        52.17549368730097,
        116.55903613364532,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        28.358745385746584,
        1119.4709750642746,
        6.177367243302452,
        4523.449719877925,
        8885.106879676776,
        8726.713689092487,
        24.72554250302615,
        17.72145102639004,
        180059.5643582001,
        90912.67634544164,
        272580.4306577905,
        119535.79719754448,
        4578977.525318111,
        153369.5203686487,
        4709596.422727356,
        4435482.150450142
      ],
      "scaler_scale": [
        19519.608985585724,
        30604279.071359694,
        1712.3252122449733,
        143.54662786596,
        55612.07996083851,
        207357.3217719949,
        312.8357746746614,
        23.13774970863601,
        61.238056237135666,
        122.16005061649031,
        496.2540874806744,
        51.34215855121842,
        162.13458059845448,
        205.58568829129362,
        3729872.2120176465,
        211967.75075973518,
        12629826.808193991,
        3674843.547731472,
        16438780.356816066,
        12592299.645218609,
        30524172.24128136,
        12863095.543946367,
        4271253.6443306925,
        16360279.69065646,
        12785530.628534831,
        26012695.973732263,
        4615960.213359841,
        3453160.431678197,
        10464630.245937042,
        4105331.024212643,
        0.2076730271011649,
        1.0,
        1.0,
        1.0,
        13740.715568192743,
        2872.2820348977357,
        201245.63980272852,
        42317.16465261706,
        21.467742514880324,
        516.7121740233837,
        102.13923086580208,
        163.8960472869143,
        186623.74139614115,
        0.06969840609664002,
        0.2076730271011649,
        0.39269479001603785,
        0.48483779509224895,
        0.47389038216312823,
        0.19028985058326087,
        1.0,
        0.3926954059880359,
        1.0366627115169238,
        106.48511780130812,
        61.238056237135666,
        162.13458059845448,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1712.3252122449733,
        55612.07996083851,
        143.54662786596,
        207357.3217719949,
        16665.005392152158,
        20515.218839049416,
        1711.5473192806976,
        7.35147139852804,
        2585647.8743276885,
        1567446.7260700897,
        3422912.5425198055,
        2178434.132996447,
        15087132.5753479,
        1695090.295908838,
        15360809.663481215,
        14951845.619617442
      ],
      "scaler_variance": [
        381015134.95015895,
        936621897477665.0,
        2932057.632489793,
        20605.634371688408,
        3092703437.570697,
        42997058892.454636,
        97866.22191629554,
        535.3554615794858,
        3750.099531702591,
        14923.077966623476,
        246268.11934127682,
        2636.01724469845,
        26287.622225836734,
        42265.47523020494,
        13911946717981.41,
        44930327362.14121,
        159512525204975.6,
        13504475100303.633,
        270233499619641.75,
        158566010354972.7,
        931725091015411.5,
        165459226972692.88,
        18243607694208.22,
        267658751556506.28,
        163469793453202.25,
        676660351821826.6,
        21307088691321.027,
        11924316966907.951,
        109508486184180.34,
        16853742818362.828,
        0.04312808618536117,
        0.0,
        0.0,
        0.0,
        188807264.3259744,
        8250004.087996278,
        40499807539.60954,
        1790742424.2367027,
        460.8639686852002,
        266991.4707839716,
        10432.422481857615,
        26861.914316274448,
        34828420852.69377,
        0.004857867812412147,
        0.04312808618536117,
        0.15420919810574005,
        0.23506768754991358,
        0.2245720943067157,
        0.036210227234999746,
        0.0,
        0.1542096818841083,
        1.0746695774496207,
        11339.080313158467,
        3750.099531702591,
        26287.622225836734,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2932057.632489793,
        3092703437.570697,
        20605.634371688408,
        42997058892.454636,
        277722404.7204605,
        420874204.01408803,
        2929394.2261369424,
        54.04413172337581,
        6685574930015.294,
        2456889239067.843,
        11716330273739.4,
        4745575271803.981,
        227621569346123.78,
        2873331111284.3125,
        235954473517697.88,
        223557687432873.28
      ],
      "schema_version": 1,
      "source_manifest_sha256": "cbdad0dadd1964f461cde88a6c16a400a7a07bb35bb6e9a3dfbec715ef0253a4",
      "split_plan_sha256": "9890a711c0838190a13816736f7c099685d2c2690caa6c74afb2b217e1f7362e",
      "training_rows": 12795136,
      "unknown_category_policy": "all_zero_one_hot"
    },
    "full_split": {
      "exact_row_rule": "Each listed source file: discard complete repeated headers; retain the earliest original source_row for each exact full parsed record; exclude nonmatching dates/invalid timestamps from temporal partitions. Every retained source_row is enumerated in the hashed membership Parquet.",
      "limitations": [
        "Attack types occur on different dates; a globally chronological split cannot cover every attack type in every partition.",
        "Unseen attack types remain positive binary targets and are explicitly reported; this is a temporal generalization evaluation, not a closed-set multiclass claim.",
        "Feature statistics and preprocessing are not used to select date boundaries. Labels are used only for this predeclared cohort-design report."
      ],
      "ordering": [
        "recorded_timestamp_ascending",
        "source_filename_ascending",
        "original_source_row_ascending"
      ],
      "partitions": {
        "test": {
          "class_counts": {
            "Benign": 998793,
            "Bot": 282310,
            "Infilteration": 93040
          },
          "dates": [
            "2018-03-01",
            "2018-03-02"
          ],
          "files": [
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Thursday-01-03-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "802cedc1871324f3003cd85f63d8c3b1b4003869fe97ef76ef9abfe253d4ea48",
              "filename": "Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "b0534c5d7d8b41e03df71c6966c995d116a8ed28e61f377c8b14cdf5d28f4edf",
              "rows": 331027
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Friday-02-03-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "bf8b4e4f5264fa362d3f59737717977cf7e960e03c1f34125c52034b631b4cd6",
              "filename": "Friday-02-03-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "d96f38e7496aba83475031e6fb8c6fdf1abf6aa1b71325a917798f3c7de93de1",
              "rows": 1043116
            }
          ],
          "interval_end_exclusive": "2018-03-03T00:00:00",
          "interval_start_inclusive": "2018-03-01T00:00:00",
          "membership_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\membership\\test.parquet",
          "membership_sha256": "c51988409cf084b0656f7985a2a51c44aac5944f357c01356e5c21b5999eb95b",
          "rows": 1374143,
          "timestamp_max": "2018-03-02T12:59:59",
          "timestamp_min": "2018-03-01T01:00:00",
          "unseen_attack_classes": [
            "Bot",
            "Infilteration"
          ]
        },
        "train": {
          "class_counts": {
            "Benign": 10885643,
            "Brute Force -Web": 249,
            "Brute Force -XSS": 79,
            "DDOS attack-HOIC": 668461,
            "DDOS attack-LOIC-UDP": 1730,
            "DDoS attacks-LOIC-HTTP": 576191,
            "DoS attacks-GoldenEye": 41455,
            "DoS attacks-Hulk": 434873,
            "DoS attacks-SlowHTTPTest": 19462,
            "DoS attacks-Slowloris": 10285,
            "FTP-BruteForce": 39352,
            "SQL Injection": 34,
            "SSH-Bruteforce": 117322
          },
          "dates": [
            "2018-02-14",
            "2018-02-15",
            "2018-02-16",
            "2018-02-20",
            "2018-02-21",
            "2018-02-22"
          ],
          "files": [
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Wednesday-14-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "d6fc7e25cdcc99c11835395317ce7195bc453905a69d4a5e3ae2369c41b0670d",
              "filename": "Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "acff8bc61376ee031d80878ee6099e0b1a87a1bd711d8068298421418c9f8147",
              "rows": 822942
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Thursday-15-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "f412998558ac29e6e063e831158b8c75a65f5116cd3d7047450929200fd55acc",
              "filename": "Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "fa2947a8256d81ee9103ae16139d62d0e17aa23e696ee80d9e76fb51c01c9c4b",
              "rows": 1046154
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Friday-16-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "118d1d5604994e5a9c643f3fd041135245a82a090096c8b597cfa1964db581e1",
              "filename": "Friday-16-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "1a4919faa0c49c7af97230b0c2d076eba23ee6dd81103a3801d51ac316355d8b",
              "rows": 900988
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Thuesday-20-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "13f86441342466c1e4bf0a01cf5d7b04b22f6138b392bda114eb7b52fe24cd93",
              "filename": "Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "7287a4d7740a1dddbf330ceb2beb6a4889d33ba63674558a68b5eb50d16711df",
              "rows": 7948746
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Wednesday-21-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "d289537700c0b6b8d78a7b06acd89dcdf3e34732316d2d1ffbf33ccf816a9204",
              "filename": "Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "a5f4a1c2689e0aa6566c03a58466de9c407c0be0cbd3cc69306544026611be04",
              "rows": 1031018
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Thursday-22-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "a51c836af9ba68783318a4097851d1d9080ffe1b4c5cb0c39c96c98b6951b52e",
              "filename": "Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "da33c927018274f9d49b145baa00e4ce0526c25b3b890b34c489e247b5e24544",
              "rows": 1045288
            }
          ],
          "interval_end_exclusive": "2018-02-23T00:00:00",
          "interval_start_inclusive": "2018-02-14T00:00:00",
          "membership_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\membership\\train.parquet",
          "membership_sha256": "3478533e80f58c092372361051d9f7b83199f284a5d57af2549f6d74051e9ecd",
          "rows": 12795136,
          "timestamp_max": "2018-02-22T12:59:59",
          "timestamp_min": "2018-02-14T01:00:00",
          "unseen_attack_classes": []
        },
        "validation": {
          "class_counts": {
            "Benign": 1583520,
            "Brute Force -Web": 362,
            "Brute Force -XSS": 151,
            "Infilteration": 68857,
            "SQL Injection": 53
          },
          "dates": [
            "2018-02-23",
            "2018-02-28"
          ],
          "files": [
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Friday-23-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "50098b4f1562d49685c4e8b1d56da9626f70cddc0cfbf5b5b3710d4c6d6ad2f8",
              "filename": "Friday-23-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "d0a7f5059d9823b6e9b392b759e306481a3502d190dea7a1b5502ae079ea069b",
              "rows": 1045961
            },
            {
              "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Wednesday-28-02-2018_TrafficForML_CICFlowMeter.parquet",
              "cleaned_sha256": "f1634b9f95e837d851ea18e9810122b116d8eddc9b5caeb9c13c6c0c54f2781b",
              "filename": "Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv",
              "raw_sha256": "f15e2a12304446058a0186c8ad67de2bd15735a9ba5c70c9a1f4c4242ab06771",
              "rows": 606982
            }
          ],
          "interval_end_exclusive": "2018-03-01T00:00:00",
          "interval_start_inclusive": "2018-02-23T00:00:00",
          "membership_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\membership\\validation.parquet",
          "membership_sha256": "2bdd932fb3155c492619faf9a01af18e6862b13e8b72225f61cc6ead36084f28",
          "rows": 1652943,
          "timestamp_max": "2018-02-28T12:59:59",
          "timestamp_min": "2018-02-23T01:00:00",
          "unseen_attack_classes": [
            "Infilteration"
          ]
        }
      },
      "pre_split_class_report": "pre_split_class_distribution.csv",
      "pre_split_report_sha256": "ca607efa06bc3c08e6a6481a32cbf53ffdbdb7f45085d4a092b44cda89f7d854",
      "schema_version": 1,
      "selection": "Whole dates only. Require configured benign/malicious minimums. Maximize training attack-class coverage, then minimize L1 deviation from configured row fractions; chronological cutoffs break ties.",
      "selection_spec": {
        "minimum_benign_per_partition": 100,
        "minimum_malicious_per_partition": 100,
        "minimum_test_dates": 2,
        "minimum_train_dates": 3,
        "minimum_validation_dates": 1,
        "target_fractions": [
          0.8,
          0.1,
          0.1
        ]
      },
      "source_manifest_sha256": "cbdad0dadd1964f461cde88a6c16a400a7a07bb35bb6e9a3dfbec715ef0253a4",
      "status": "split_frozen",
      "target": "binary",
      "target_mapping": {
        "Benign": 0,
        "all_observed_attack_labels": 1
      },
      "timestamp_interpretation": "Day-first, timezone unspecified. No AM/PM reconstruction; ordering is by recorded timestamps, not claimed physical capture chronology."
    },
    "full_temporal_cohort": {
      "checks": {
        "chronological_order_verified": true,
        "common_target_records_across_lengths": true,
        "labels_metadata_only": true,
        "no_1970": true,
        "no_day_crossing": true,
        "no_future_flow": true,
        "no_partition_crossing": true
      },
      "codebook": [
        "Benign",
        "Bot",
        "Brute Force -Web",
        "Brute Force -XSS",
        "DDOS attack-HOIC",
        "DDOS attack-LOIC-UDP",
        "DDoS attacks-LOIC-HTTP",
        "DoS attacks-GoldenEye",
        "DoS attacks-Hulk",
        "DoS attacks-SlowHTTPTest",
        "DoS attacks-Slowloris",
        "FTP-BruteForce",
        "Infilteration",
        "SQL Injection",
        "SSH-Bruteforce"
      ],
      "features": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min",
        "Protocol=0",
        "Protocol=17",
        "Protocol=6"
      ],
      "partitions": {
        "test": {
          "benign": 124795,
          "class_counts": {
            "Benign": 124795,
            "Bot": 35326,
            "Brute Force -Web": 0,
            "Brute Force -XSS": 0,
            "DDOS attack-HOIC": 0,
            "DDOS attack-LOIC-UDP": 0,
            "DDoS attacks-LOIC-HTTP": 0,
            "DoS attacks-GoldenEye": 0,
            "DoS attacks-Hulk": 0,
            "DoS attacks-SlowHTTPTest": 0,
            "DoS attacks-Slowloris": 0,
            "FTP-BruteForce": 0,
            "Infilteration": 11632,
            "SQL Injection": 0,
            "SSH-Bruteforce": 0
          },
          "cohort_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\temporal_v1\\metrics\\test_cohort.parquet",
          "cohort_sha256": "e48271110891a56408bc0bef3c281e1724a95f48e182593efd1e0600b99cd560",
          "coverage_fraction": 0.12498917507129899,
          "dates": [
            "2018-03-01",
            "2018-03-02"
          ],
          "malicious": 46958,
          "rows": 1374143,
          "spans": [
            [
              0,
              331027
            ],
            [
              331027,
              1374143
            ]
          ],
          "stride": 8,
          "targets": 171753
        },
        "train": {
          "benign": 85086,
          "class_counts": {
            "Benign": 85086,
            "Bot": 0,
            "Brute Force -Web": 4,
            "Brute Force -XSS": 1,
            "DDOS attack-HOIC": 5196,
            "DDOS attack-LOIC-UDP": 12,
            "DDoS attacks-LOIC-HTTP": 4498,
            "DoS attacks-GoldenEye": 328,
            "DoS attacks-Hulk": 3387,
            "DoS attacks-SlowHTTPTest": 152,
            "DoS attacks-Slowloris": 78,
            "FTP-BruteForce": 285,
            "Infilteration": 0,
            "SQL Injection": 1,
            "SSH-Bruteforce": 934
          },
          "cohort_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\temporal_v1\\metrics\\train_cohort.parquet",
          "cohort_sha256": "957f6659a08ed76d768deee9b89b994f9aaa092eb3f3a94fa7929f49b7db63a8",
          "coverage_fraction": 0.0078125,
          "dates": [
            "2018-02-14",
            "2018-02-15",
            "2018-02-16",
            "2018-02-20",
            "2018-02-21",
            "2018-02-22"
          ],
          "malicious": 14876,
          "rows": 12795136,
          "spans": [
            [
              0,
              822942
            ],
            [
              822942,
              1869096
            ],
            [
              1869096,
              2770084
            ],
            [
              2770084,
              10718830
            ],
            [
              10718830,
              11749848
            ],
            [
              11749848,
              12795136
            ]
          ],
          "stride": 128,
          "targets": 99962
        },
        "validation": {
          "benign": 197989,
          "class_counts": {
            "Benign": 197989,
            "Bot": 0,
            "Brute Force -Web": 48,
            "Brute Force -XSS": 11,
            "DDOS attack-HOIC": 0,
            "DDOS attack-LOIC-UDP": 0,
            "DDoS attacks-LOIC-HTTP": 0,
            "DoS attacks-GoldenEye": 0,
            "DoS attacks-Hulk": 0,
            "DoS attacks-SlowHTTPTest": 0,
            "DoS attacks-Slowloris": 0,
            "FTP-BruteForce": 0,
            "Infilteration": 8551,
            "SQL Injection": 4,
            "SSH-Bruteforce": 0
          },
          "cohort_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\temporal_v1\\metrics\\validation_cohort.parquet",
          "cohort_sha256": "9e498c35c3430a1055553d3adde7b6df399677467fb01583ffd4d5cf417edeab",
          "coverage_fraction": 0.12499100089960755,
          "dates": [
            "2018-02-23",
            "2018-02-28"
          ],
          "malicious": 8614,
          "rows": 1652943,
          "spans": [
            [
              0,
              1045961
            ],
            [
              1045961,
              1652943
            ]
          ],
          "stride": 8,
          "targets": 206603
        }
      }
    },
    "graph_data_manifest": {
      "artifacts": [
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\graph_v1\\metadata.parquet",
          "sha256": "c077ccf78e4e5d2310e4d47920b0585690a6f0099be66c77868ba8d063cc39f6"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\graph_v1\\target_ids.npy",
          "sha256": "06000e0c4b80de292acb824703ca446b1b71e8ac5a789c0d836a9038160c9664"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\graph_v1\\target_groups.json",
          "sha256": "7c6314fbae4fc768add0b9a52aa5e02b4eabe6f0b98541a62aa98cedfa8c4df5"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\graph_v1\\target_features.npy",
          "sha256": "0ac3c12a3ced48033569d3e5929202b45d080478965be08704bca4ddc2be7021"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\graph_v1\\history_features.npy",
          "sha256": "065ffffe3816094046465b15da7864291b63cebd01ea83e2c4aab79cabc07e17"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_v1\\metrics\\evaluation_cohort.parquet",
          "sha256": "9bc27a5c2700c6b17a08fccdae270cb9d6c547b2ded4b530274fe4cb37936312"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_v1\\configs\\preprocessing.json",
          "sha256": "ba9b94d60b81cfd664ee1a70f938fbfe17f5d137b347b8cda0a59bfbbf7082ae"
        }
      ],
      "edge_feature_names": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min",
        "Protocol=0",
        "Protocol=17",
        "Protocol=6"
      ],
      "history_feature_names": [
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Dst Port",
        "Protocol=0",
        "Protocol=6",
        "Protocol=17"
      ],
      "preparation_seconds": 81.26263929999914,
      "preprocessing_sha256": "ba9b94d60b81cfd664ee1a70f938fbfe17f5d137b347b8cda0a59bfbbf7082ae",
      "rows": 7948746,
      "split_approval_sha256": "f2cc699ccc08522ec52cf7feb9a430b95c25f3e0df369d941346c872e2dbbfa7",
      "status": "PASS",
      "target_rows": 474357
    },
    "graph_membership_definition": {
      "approved": false,
      "attack_episodes": [
        {
          "active_minutes": 16,
          "benign": 215184,
          "end_exclusive": "2018-02-20 01:30:00",
          "malicious": 797,
          "start": "2018-02-20 01:14:00"
        },
        {
          "active_minutes": 64,
          "benign": 939885,
          "end_exclusive": "2018-02-20 11:17:00",
          "malicious": 575394,
          "start": "2018-02-20 10:13:00"
        }
      ],
      "boundaries": [
        "2018-02-20 10:30:00",
        "2018-02-20 11:00:00"
      ],
      "cleaning": "Reuse exact frozen temporal-eligible source_row membership; no recleaning or sampling",
      "endpoint_missing_counts": {
        "Dst IP": 0,
        "Dst Port": 0,
        "Protocol": 0,
        "Src IP": 0,
        "Src Port": 0
      },
      "endpoint_recovery": "Read raw identifiers only for source_row IDs retained in the verified cleaned parquet",
      "inputs": {
        "cleaned_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\baseline_v1\\cleaned\\Thuesday-20-02-2018_TrafficForML_CICFlowMeter.parquet",
        "cleaned_sha256": "13f86441342466c1e4bf0a01cf5d7b04b22f6138b392bda114eb7b52fe24cd93",
        "raw_path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\data\\raw\\Processed Traffic Data for ML Algorithms\\Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv",
        "raw_sha256": "7287a4d7740a1dddbf330ceb2beb6a4889d33ba63674558a68b5eb50d16711df"
      },
      "membership_hash_encoding": "SHA256 of source_row int64 little-endian sequence in frozen chronological order, scoped to source_file",
      "next_stage_requirements": [
        "Explicit split review/approval before preprocessing or training",
        "Fit imputation/scaling only on approved Feb-20 TRAIN; do not reuse baseline_v1 fitted preprocessing",
        "Keep identifiers separate; raw IPs, labels and timestamps are not numeric model features",
        "Causal node history and message-passing neighborhoods must exclude later flows, including later flows in the same snapshot",
        "Declare tie handling and historical state policy before fitting",
        "Matched edge MLP and GATv2 use identical targets, features, splits and preprocessing"
      ],
      "partition_rules": {
        "test": "timestamp >= 2018-02-20 11:00:00",
        "train": "timestamp < 2018-02-20 10:30:00",
        "validation": "2018-02-20 10:30:00 <= timestamp < 2018-02-20 11:00:00"
      },
      "partitions": [
        {
          "benign": 5359206,
          "malicious": 147953,
          "malicious_fraction": 0.02686557624357677,
          "partition": "train",
          "rows": 5507159,
          "source_row_sequence_sha256": "19472fd02d7d4b8263b89a4c20ecf30b7938611881c42cabb169bfbf7fad3866",
          "timestamp_max": "2018-02-20 10:29:59",
          "timestamp_min": "2018-02-20 01:00:00"
        },
        {
          "benign": 450793,
          "malicious": 276465,
          "malicious_fraction": 0.3801470729782278,
          "partition": "validation",
          "rows": 727258,
          "source_row_sequence_sha256": "b97eb04f25514b1ee0737d7b85d1cf450169bf0bdaccb5e7ade5abd5d018c93f",
          "timestamp_max": "2018-02-20 10:59:59",
          "timestamp_min": "2018-02-20 10:30:00"
        },
        {
          "benign": 1562556,
          "malicious": 151773,
          "malicious_fraction": 0.08853201456663219,
          "partition": "test",
          "rows": 1714329,
          "source_row_sequence_sha256": "094fbef8f988d587a10d7e0f91ac2716688a1df01e294e78caaac99b4937aaaf",
          "timestamp_max": "2018-02-20 12:59:59",
          "timestamp_min": "2018-02-20 11:00:00"
        }
      ],
      "primary_window_minutes": 1,
      "purpose": "within-day graph contribution; not unseen-attack or zero-day evaluation",
      "rationale": "Timeline-informed proposal: all partitions include both classes and a portion of the main attack period; boundaries align with 1/5/10-minute windows. Not selected from model performance.",
      "seed": 42,
      "sensitivity_window_minutes": [
        5,
        10
      ],
      "simple_chronological_candidates": [
        {
          "all_malicious_in_one_partition": false,
          "both_classes_in_all_partitions": false,
          "boundaries": [
            "2018-02-20 10:40:00",
            "2018-02-20 11:50:00"
          ],
          "name": "elapsed_80_10_10",
          "partitions": [
            {
              "benign": 5514050,
              "malicious": 240089,
              "malicious_fraction": 0.04172457425863366,
              "partition": "train",
              "rows": 5754139,
              "source_row_sequence_sha256": "24c3a414290f36dec64959e6c6b21fdd948f9e4ba91024fa2b0dbae911e264ec",
              "timestamp_max": "2018-02-20 10:39:59",
              "timestamp_min": "2018-02-20 01:00:00"
            },
            {
              "benign": 1040616,
              "malicious": 336102,
              "malicious_fraction": 0.24413278536345134,
              "partition": "validation",
              "rows": 1376718,
              "source_row_sequence_sha256": "eb3a4dbfe471f59ba30e85616f6f13bf0bc609e29e0a6ffa52f5077caad2293e",
              "timestamp_max": "2018-02-20 11:49:59",
              "timestamp_min": "2018-02-20 10:40:00"
            },
            {
              "benign": 817889,
              "malicious": 0,
              "malicious_fraction": 0.0,
              "partition": "test",
              "rows": 817889,
              "source_row_sequence_sha256": "d21d0b3f50cfcc037f1c217754444bfae26dd8a1d1aa86a4cc0c8c189a12dc64",
              "timestamp_max": "2018-02-20 12:59:59",
              "timestamp_min": "2018-02-20 11:50:00"
            }
          ]
        },
        {
          "all_malicious_in_one_partition": false,
          "both_classes_in_all_partitions": true,
          "boundaries": [
            "2018-02-20 09:20:00",
            "2018-02-20 11:10:00"
          ],
          "name": "elapsed_70_15_15",
          "partitions": [
            {
              "benign": 4342838,
              "malicious": 797,
              "malicious_fraction": 0.0001834868721704287,
              "partition": "train",
              "rows": 4343635,
              "source_row_sequence_sha256": "b1918cef5ea5eecdd07f1f089eaa30b41dea24aecf053f3ad381d63771b16261",
              "timestamp_max": "2018-02-20 09:19:59",
              "timestamp_min": "2018-02-20 01:00:00"
            },
            {
              "benign": 1608882,
              "malicious": 515649,
              "malicious_fraction": 0.24271192088983404,
              "partition": "validation",
              "rows": 2124531,
              "source_row_sequence_sha256": "0cbf25f54ad26404a6e498bd5f8296cd4af32e27caa0d2656d2e99ebf252f5ee",
              "timestamp_max": "2018-02-20 11:09:59",
              "timestamp_min": "2018-02-20 09:20:00"
            },
            {
              "benign": 1420835,
              "malicious": 59745,
              "malicious_fraction": 0.04035242945332235,
              "partition": "test",
              "rows": 1480580,
              "source_row_sequence_sha256": "749fe5261902505662aac9661fd81b6795f71a4caacff9ce48d1e33e18c1f96f",
              "timestamp_max": "2018-02-20 12:59:59",
              "timestamp_min": "2018-02-20 11:10:00"
            }
          ]
        },
        {
          "all_malicious_in_one_partition": false,
          "both_classes_in_all_partitions": true,
          "boundaries": [
            "2018-02-20 08:10:00",
            "2018-02-20 10:40:00"
          ],
          "name": "elapsed_60_20_20",
          "partitions": [
            {
              "benign": 3597227,
              "malicious": 797,
              "malicious_fraction": 0.00022151047352658016,
              "partition": "train",
              "rows": 3598024,
              "source_row_sequence_sha256": "4049758452c25caef20e78be41c285ab8ab1e0270f85d6a81927c012fef54227",
              "timestamp_max": "2018-02-20 08:09:57",
              "timestamp_min": "2018-02-20 01:00:00"
            },
            {
              "benign": 1916823,
              "malicious": 239292,
              "malicious_fraction": 0.11098294849764508,
              "partition": "validation",
              "rows": 2156115,
              "source_row_sequence_sha256": "beb000be500169ae3af972b2ba3b74e4319ba98c506ad39647a460812eb25344",
              "timestamp_max": "2018-02-20 10:39:59",
              "timestamp_min": "2018-02-20 08:10:00"
            },
            {
              "benign": 1858505,
              "malicious": 336102,
              "malicious_fraction": 0.15314906040124723,
              "partition": "test",
              "rows": 2194607,
              "source_row_sequence_sha256": "8e48a4e27be8908eb328f221a4b055112592f38df3cf41ed1f997b46cf022837",
              "timestamp_max": "2018-02-20 12:59:59",
              "timestamp_min": "2018-02-20 10:40:00"
            }
          ]
        }
      ],
      "software_versions": {
        "numpy": "2.1.3",
        "pandas": "2.2.3",
        "pyarrow": "19.0.0"
      },
      "source_file": "Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv",
      "source_manifest_sha256": "cbdad0dadd1964f461cde88a6c16a400a7a07bb35bb6e9a3dfbec715ef0253a4",
      "source_row_definition": "1-based CSV data record excluding header; (source_file, source_row) is unique",
      "status": "PROPOSED_AWAITING_USER_REVIEW",
      "timeline_sha256": "af13c28aeebcfb6aee98ef3e7d035cb36b36195bb17814dfd8455aaedc13f1ef",
      "timestamp_policy": "Frozen parsed timestamps; dataset-local naive times, no inferred timezone or AM/PM repair",
      "training_permitted": false,
      "window_alignment": "calendar clock, half-open [start,end)"
    },
    "graph_preprocessing": {
      "all_missing_numeric_columns": [],
      "all_missing_numeric_fill": 0.0,
      "categorical_columns": [
        "Protocol"
      ],
      "categorical_imputation_values": {
        "Protocol": "6"
      },
      "categories": {
        "Protocol": [
          "0",
          "17",
          "6"
        ]
      },
      "constant_training_numeric_columns": [
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "CWE Flag Count",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg"
      ],
      "excluded_target_encodings": [],
      "fit_partition": "train",
      "fit_scope": "approved Feb-20 TRAIN only",
      "numeric_columns": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min"
      ],
      "numeric_imputation_strategy": "training_mean",
      "numeric_imputation_values": [
        7753.597221180648,
        13732745.475026596,
        22.126276179787073,
        7.054358336122127,
        889.6221955821504,
        5329.121837230412,
        179.0916873836401,
        13.960450388303661,
        47.815463436165004,
        56.57526314214296,
        387.0582269369742,
        34.10745504170117,
        125.0533774712606,
        137.49862091687177,
        298425.6035595136,
        34838.000880835796,
        2834964.159458231,
        1193632.0144249136,
        6210642.544931243,
        2313767.600481482,
        13444832.854302553,
        3238493.4010944613,
        1389568.4053262742,
        6033718.071474058,
        2400530.6534765023,
        9542216.143964611,
        1086235.8994496537,
        1053607.8614768623,
        3364564.5331095397,
        436250.86893623375,
        0.06020236568437556,
        0.0,
        0.0,
        0.0,
        241.8223450603115,
        144.92540927182236,
        31106.246776146327,
        3454.0766218591825,
        13.798955323425382,
        395.79317048953914,
        81.86315505199366,
        120.54581804963473,
        41272.905780552835,
        0.006011629589775781,
        0.06020236568437556,
        0.20570424787081687,
        0.3853340715239927,
        0.2599490953502523,
        0.040449894401087746,
        0.0,
        0.20570588210727164,
        0.5441754995633865,
        95.17116275395385,
        47.815463436165004,
        125.0533774712606,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        22.126276179787073,
        889.6221955821504,
        7.054358336122127,
        5329.121837230412,
        5165.5231094653345,
        10139.257633563875,
        18.27554116378336,
        15.768110562996274,
        270203.43306494557,
        137817.23956989215,
        402841.4087470509,
        177150.72992172552,
        5016024.392010586,
        192532.2500381921,
        5173202.648993791,
        4838395.829128776
      ],
      "numeric_observed_counts": [
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5463264,
        5463264,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159,
        5507159
      ],
      "output_feature_names": [
        "Dst Port",
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Fwd Pkt Len Max",
        "Fwd Pkt Len Min",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Std",
        "Bwd Pkt Len Max",
        "Bwd Pkt Len Min",
        "Bwd Pkt Len Mean",
        "Bwd Pkt Len Std",
        "Flow Byts/s",
        "Flow Pkts/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Fwd IAT Tot",
        "Fwd IAT Mean",
        "Fwd IAT Std",
        "Fwd IAT Max",
        "Fwd IAT Min",
        "Bwd IAT Tot",
        "Bwd IAT Mean",
        "Bwd IAT Std",
        "Bwd IAT Max",
        "Bwd IAT Min",
        "Fwd PSH Flags",
        "Bwd PSH Flags",
        "Fwd URG Flags",
        "Bwd URG Flags",
        "Fwd Header Len",
        "Bwd Header Len",
        "Fwd Pkts/s",
        "Bwd Pkts/s",
        "Pkt Len Min",
        "Pkt Len Max",
        "Pkt Len Mean",
        "Pkt Len Std",
        "Pkt Len Var",
        "FIN Flag Cnt",
        "SYN Flag Cnt",
        "RST Flag Cnt",
        "PSH Flag Cnt",
        "ACK Flag Cnt",
        "URG Flag Cnt",
        "CWE Flag Count",
        "ECE Flag Cnt",
        "Down/Up Ratio",
        "Pkt Size Avg",
        "Fwd Seg Size Avg",
        "Bwd Seg Size Avg",
        "Fwd Byts/b Avg",
        "Fwd Pkts/b Avg",
        "Fwd Blk Rate Avg",
        "Bwd Byts/b Avg",
        "Bwd Pkts/b Avg",
        "Bwd Blk Rate Avg",
        "Subflow Fwd Pkts",
        "Subflow Fwd Byts",
        "Subflow Bwd Pkts",
        "Subflow Bwd Byts",
        "Init Fwd Win Byts",
        "Init Bwd Win Byts",
        "Fwd Act Data Pkts",
        "Fwd Seg Size Min",
        "Active Mean",
        "Active Std",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Std",
        "Idle Max",
        "Idle Min",
        "Protocol=0",
        "Protocol=17",
        "Protocol=6"
      ],
      "scaler_mean": [
        7753.597221180648,
        13732745.475026596,
        22.126276179787098,
        7.054358336122127,
        889.6221955821507,
        5329.121837230412,
        179.0916873836402,
        13.960450388303661,
        47.81546343616502,
        56.57526314214296,
        387.0582269369741,
        34.10745504170117,
        125.0533774712606,
        137.4986209168719,
        298425.60355951363,
        34838.000880835396,
        2834964.159458231,
        1193632.014424913,
        6210642.544931241,
        2313767.600481482,
        13444832.854302553,
        3238493.4010944623,
        1389568.4053262754,
        6033718.071474058,
        2400530.653476503,
        9542216.143964605,
        1086235.8994496537,
        1053607.8614768626,
        3364564.533109539,
        436250.86893623375,
        0.060202365684375564,
        0.0,
        0.0,
        0.0,
        241.82234506031145,
        144.92540927182236,
        31106.246776146338,
        3454.0766218591825,
        13.798955323425382,
        395.79317048953914,
        81.86315505199369,
        120.54581804963473,
        41272.905780552835,
        0.006011629589775782,
        0.060202365684375564,
        0.20570424787081695,
        0.3853340715239927,
        0.25994909535025224,
        0.04044989440108777,
        0.0,
        0.20570588210727164,
        0.5441754995633865,
        95.17116275395388,
        47.81546343616502,
        125.0533774712606,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        22.126276179787098,
        889.6221955821507,
        7.054358336122127,
        5329.121837230412,
        5165.523109465334,
        10139.257633563875,
        18.27554116378334,
        15.768110562996274,
        270203.43306494557,
        137817.23956989218,
        402841.4087470509,
        177150.72992172558,
        5016024.392010586,
        192532.2500381921,
        5173202.648993791,
        4838395.829128774
      ],
      "scaler_scale": [
        17672.86963122655,
        33135531.725643244,
        1494.7273452167303,
        177.8858843873899,
        47837.337364425715,
        256779.53057219685,
        264.5656382336129,
        24.627030955538164,
        50.76865001935018,
        89.11624215226698,
        528.2910335730809,
        55.04767016136943,
        170.33871491123958,
        215.55303301064544,
        4034992.9113723426,
        227728.2074715371,
        11978992.351805478,
        3942347.232376419,
        16729742.91742085,
        11929181.92556074,
        33051691.448143236,
        12210200.367546242,
        4784257.519339984,
        16641647.361136885,
        12071526.553362263,
        28767115.409582652,
        5170234.320134769,
        3751748.183935712,
        11655918.897878427,
        4718577.1965338215,
        0.23786138999506082,
        1.0,
        1.0,
        1.0,
        12030.300678731888,
        3558.266052362494,
        222717.48423485112,
        32820.58479932596,
        22.417280749193665,
        528.0935475865256,
        104.05351272866095,
        163.52862602882422,
        259927.51760322167,
        0.07730129299986449,
        0.23786138999506082,
        0.4042153018859134,
        0.4866741464745735,
        0.4386063875239793,
        0.19701192969977405,
        1.0,
        0.40421649171421176,
        1.422899871356526,
        107.40874791053514,
        50.76865001935018,
        170.33871491123958,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1494.7273452167303,
        47837.337364425715,
        177.8858843873899,
        256779.53057219685,
        10733.77126428223,
        22481.812479014334,
        1493.3305384744422,
        6.2733527502487,
        3300631.97078842,
        2007949.9396811211,
        4367652.574232147,
        2778828.473351084,
        15533176.383720271,
        1880893.887338034,
        15844665.584523663,
        15370446.274594245
      ],
      "scaler_variance": [
        312330321.0023296,
        1097963462741109.9,
        2234209.8365386548,
        31643.387864283846,
        2288410846.117881,
        65935727320.87778,
        69994.97693395894,
        606.490653685035,
        2577.455824787265,
        7941.704615341487,
        279091.41615371406,
        3030.245990194923,
        29015.27779761255,
        46463.1100400884,
        16281167794825.053,
        51860136478.199455,
        143496257764614.12,
        15542101700626.01,
        279884298082993.06,
        142305381413125.06,
        1092414307583264.8,
        149088993015626.38,
        22889120011361.184,
        276944426892434.25,
        145721753328530.22,
        827546928988247.6,
        26731322925099.44,
        14075614435664.912,
        135860445353919.45,
        22264970759648.98,
        0.05657804085038241,
        0.0,
        0.0,
        0.0,
        144728134.42069694,
        12661257.299395368,
        49603077783.90116,
        1077190786.5697463,
        502.5344761881689,
        278882.795002522,
        10827.133511173606,
        26741.61153087505,
        67562314407.37311,
        0.005975489899450899,
        0.05657804085038241,
        0.16339001027872013,
        0.23685172484675462,
        0.1923755631768351,
        0.03881370044402871,
        0.0,
        0.1633909721737454,
        2.0246440439064184,
        11536.639127708888,
        2577.455824787265,
        29015.27779761255,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2234209.8365386548,
        2288410846.117881,
        31643.387864283846,
        65935727320.87778,
        115213845.55393094,
        505431892.34156466,
        2230036.097140367,
        39.35495472905292,
        10894171406590.65,
        4031862960265.4185,
        19076389009196.7,
        7721887684306.718,
        241279568567765.2,
        3537761815425.5815,
        251053427485388.6,
        236250618680188.1
      ],
      "schema_version": 1,
      "split_approval_sha256": "f2cc699ccc08522ec52cf7feb9a430b95c25f3e0df369d941346c872e2dbbfa7",
      "training_rows": 5507159,
      "unknown_category_policy": "all_zero_one_hot"
    },
    "graph_split_approval": {
      "approval_source": "User replied yes to explicit 10:30/11:00 split approval question",
      "approved": true,
      "boundaries": [
        "2018-02-20 10:30:00",
        "2018-02-20 11:00:00"
      ],
      "proposal_sha256": "593589f8f9c387ae65bde0ec4c837d297615f25223434db13b5614004cdd3259"
    },
    "graph_temporal_cohort": {
      "all_phase6_targets_retained": true,
      "artifacts": [
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_temporal_v1\\metrics\\eligible_source_rows.npy",
          "sha256": "7efec58fc4eb4331a8c38b84f6b33ed78d0a89f58991cfa2c170afd63555769d"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_temporal_v1\\metrics\\eligible_target_ids.npy",
          "sha256": "06000e0c4b80de292acb824703ca446b1b71e8ac5a789c0d836a9038160c9664"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_temporal_v1\\metrics\\history_identity_types.npy",
          "sha256": "f16fdedeb1aa60d05eb87a5fe3d29656b86bc98de9b949c895051095e8756b64"
        },
        {
          "path": "C:\\Users\\ramku\\Documents\\codebase\\aigt-ctd\\results\\graph_temporal_v1\\metrics\\history_indices.npy",
          "sha256": "e07c965ad8e8b0a421a0167460033acaa4f8f9bcb4bb739bfa79ec739290f1b7"
        }
      ],
      "partitions": {
        "test": 212591,
        "train": 172984,
        "validation": 88782
      },
      "phase6_cohort_sha256": "9bc27a5c2700c6b17a08fccdae270cb9d6c547b2ded4b530274fe4cb37936312",
      "rows": 474357,
      "status": "coverage_pass_after_documented_pretraining_amendment"
    },
    "preprocessing_rule": "No per-seed refit. Numeric TRAIN means impute; frozen standard scaling, Protocol TRAIN-mode imputation and frozen ordered one-hot levels; unseen category all-zero; ordered frozen feature lists in state. Neither labels nor identifiers enter features.",
    "target": "0 Benign;1 any other attack label; attack labels/source IDs/timestamps metadata only"
  },
  "exclusions": [
    "Phase5 L16/L32/alternate architecture search",
    "Phase6 5/10-minute primary windows",
    "Phase9 L4 final fitting",
    "AE architecture A search",
    "five-seed Isolation Forest",
    "MAX/weighted fusion final fitting or selection",
    "anomaly ProtocolB tuning",
    "joint GAT/Transformer training",
    "anomaly integration into graph-temporal",
    "SHAP/GNNExplainer",
    "new features",
    "new split",
    "zero-day empirical claims"
  ],
  "execution_authorized": false,
  "model_registry": [
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/logistic_regression",
      "dependency": "",
      "family": "supervised",
      "final_status": "five_seed_required",
      "model_id": "logistic_regression",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/random_forest",
      "dependency": "",
      "family": "supervised",
      "final_status": "five_seed_required",
      "model_id": "random_forest",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/xgboost",
      "dependency": "",
      "family": "supervised",
      "final_status": "five_seed_required",
      "model_id": "xgboost",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/mlp",
      "dependency": "",
      "family": "supervised",
      "final_status": "five_seed_required",
      "model_id": "mlp",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "phase5_matched",
      "configuration_json_pointer": "/models/transformer_L1",
      "dependency": "",
      "family": "temporal",
      "final_status": "five_seed_required",
      "model_id": "transformer_L1",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "phase5_matched",
      "configuration_json_pointer": "/models/transformer_L64",
      "dependency": "",
      "family": "temporal",
      "final_status": "five_seed_required",
      "model_id": "transformer_L64",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "feb20_matched",
      "configuration_json_pointer": "/models/edge_mlp",
      "dependency": "",
      "family": "graph_control",
      "final_status": "five_seed_required",
      "model_id": "edge_mlp",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "feb20_matched",
      "configuration_json_pointer": "/models/gatv2",
      "dependency": "",
      "family": "graph",
      "final_status": "five_seed_required",
      "model_id": "gatv2",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "feb20_matched",
      "configuration_json_pointer": "/models/gatv2_self_only",
      "dependency": "",
      "family": "graph_ablation",
      "final_status": "five_seed_planned_resource_conditional",
      "model_id": "gatv2_self_only",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "feb20_matched",
      "configuration_json_pointer": "/models/gat_transformer_L1",
      "dependency": "gatv2[s]",
      "family": "graph_temporal",
      "final_status": "five_seed_required",
      "model_id": "gat_transformer_L1",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "feb20_matched",
      "configuration_json_pointer": "/models/gat_transformer_L8",
      "dependency": "gatv2[s]",
      "family": "graph_temporal",
      "final_status": "five_seed_required",
      "model_id": "gat_transformer_L8",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/autoencoder_B",
      "dependency": "",
      "family": "anomaly",
      "final_status": "five_seed_required",
      "model_id": "autoencoder_B",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/isolation_forest",
      "dependency": "existing Phase7",
      "family": "anomaly_secondary",
      "final_status": "development_seed42_secondary_only",
      "model_id": "isolation_forest",
      "seeds": "42",
      "training_in_phase10": false
    },
    {
      "cohort": "full_dataset",
      "configuration_json_pointer": "/models/rf_or_ae",
      "dependency": "random_forest[s];autoencoder_B[s]",
      "family": "derived_fusion",
      "final_status": "derived_no_training",
      "model_id": "rf_or_ae",
      "seeds": "42,123,456,789,1024",
      "training_in_phase10": false
    }
  ],
  "model_training_performed": false,
  "models": {
    "autoencoder_B": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "full_dataset",
      "configuration": {
        "batch_size": 8192,
        "benign_validation": "all 1583520 benign validation records; no malicious validation used for checkpoint/calibration",
        "deterministic_algorithms": true,
        "gradient_clip_norm": 10.0,
        "hidden_layers": [
          128,
          32,
          128
        ],
        "initialization": "PyTorch default Linear initialization",
        "input_features": 80,
        "loss": "float32 mean squared reconstruction error",
        "network": "Linear80->128->ReLU->Linear128->32->ReLU->Linear32->128->ReLU->Linear128->80; linear output; no dropout",
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.001,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 1e-05
        },
        "order": "starts arange(0,full_TRAIN_rows,65536); rng=default_rng(s+epoch-1); permute blocks; within each selected block permute benign row IDs with same RNG; slice 8192 minibatches",
        "output_features": 80,
        "population": "every one of 10885643 benign TRAIN rows per executed epoch; no AE subsampling",
        "preprocessing": "frozen baseline all-class TRAIN preprocessing, not benign-only fitted preprocessing",
        "read_block_size": 65536,
        "replay": "replay checkpoint on exact benign cache batch layout and preserve exact benign calibration scores in full validation array; mixed-layout relative drift must remain <1e-6 with denominator1+abs(score)",
        "score": "convert reconstructed and input vectors individually to float64, subtract, square, mean across features; greater error more anomalous"
      },
      "dependency": "",
      "family": "anomaly",
      "selection": {
        "metric": "minimum benign-validation mean reconstruction MSE",
        "minimum_relative_improvement": 0.0001,
        "patience": 2,
        "rule": "mean < best*(1-.0001); save improving checkpoint; ties retain earlier; architecture already fixed; no malicious validation/test selection"
      },
      "status": "five_seed_required"
    },
    "edge_mlp": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "feb20_matched",
      "configuration": {
        "batch": "one entire target-minute graph per update",
        "deterministic_algorithms": true,
        "dtype": "float32",
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(TRAIN graph groups)",
        "gradient_clip_norm": 1.0,
        "initialization": "PyTorch default Linear initialization",
        "input_features": 80,
        "loss": "BCEWithLogitsLoss(pos_weight=168357/4627)",
        "network": "Linear(input,298)->GELU->Dropout.2->Linear(298,298)->GELU->Dropout.2->Linear(298,1)",
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0005,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        }
      },
      "dependency": "",
      "family": "graph_control",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "gat_transformer_L1": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "feb20_matched",
      "configuration": {
        "activation": "gelu",
        "attention": "key padding mask; padded raw representations zero; current unmasked; bidirectional within already eligible context; only final output classified; no persistent transformed hidden state",
        "batch_first": true,
        "batch_size": 2048,
        "bias": true,
        "d_model": 64,
        "deterministic_algorithms": true,
        "dropout": 0.1,
        "dtype": "float32",
        "enable_nested_tensor": false,
        "encoder": "same-seed final gatv2 best validation checkpoint; requires_grad=False and eval mode",
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(all fixed TRAIN target positions)",
        "feedforward_dim": 128,
        "final_encoder_norm": null,
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "initialization": "PyTorch default Linear/Transformer layers; TransformerEncoder clones initial layer unchanged, exactly Phase9; learned positions Normal(0,.02)",
        "layer_norm_eps": 1e-05,
        "layers": 2,
        "length": 1,
        "loss": "BCEWithLogitsLoss(pos_weight=168357/4627)",
        "norm_first": false,
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0005,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        },
        "output": "Linear64->1 on last token",
        "positions": "learned (1,8,64) Normal(mean0,std.02); use last L slots; current always slot7; do not shrink table at L1",
        "projection": "Linear(336,64)",
        "representation": "concat(src128,dst128,current80); dimension 336",
        "trainable_parameters": 89089
      },
      "dependency": "gatv2[s]",
      "family": "graph_temporal",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "gat_transformer_L8": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "feb20_matched",
      "configuration": {
        "activation": "gelu",
        "attention": "key padding mask; padded raw representations zero; current unmasked; bidirectional within already eligible context; only final output classified; no persistent transformed hidden state",
        "batch_first": true,
        "batch_size": 2048,
        "bias": true,
        "d_model": 64,
        "deterministic_algorithms": true,
        "dropout": 0.1,
        "dtype": "float32",
        "enable_nested_tensor": false,
        "encoder": "same-seed final gatv2 best validation checkpoint; requires_grad=False and eval mode",
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(all fixed TRAIN target positions)",
        "feedforward_dim": 128,
        "final_encoder_norm": null,
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "initialization": "PyTorch default Linear/Transformer layers; TransformerEncoder clones initial layer unchanged, exactly Phase9; learned positions Normal(0,.02)",
        "layer_norm_eps": 1e-05,
        "layers": 2,
        "length": 8,
        "loss": "BCEWithLogitsLoss(pos_weight=168357/4627)",
        "norm_first": false,
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0005,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        },
        "output": "Linear64->1 on last token",
        "positions": "learned (1,8,64) Normal(mean0,std.02); use last L slots; current always slot7; do not shrink table at L1",
        "projection": "Linear(336,64)",
        "representation": "concat(src128,dst128,current80); dimension 336",
        "trainable_parameters": 89089
      },
      "dependency": "gatv2[s]",
      "family": "graph_temporal",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "gatv2": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "feb20_matched",
      "configuration": {
        "attention": "edge-aware dynamic GATv2; source/destination/edge linear projections without bias; per-head learnable attention Xavier uniform; LeakyReLU slope .2; stable softmax over incoming edges; attention dropout .2",
        "batch": "one entire target-minute graph per update",
        "channels_per_head": 32,
        "classifier": "concat(src128,dst128,current80)->Linear128->GELU->Dropout.2->Linear1",
        "deterministic_algorithms": true,
        "dropout": 0.2,
        "dtype": "float32",
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(TRAIN graph groups)",
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "hidden": 128,
        "history_edge_dim": 9,
        "initialization": "PyTorch2.6.0 defaults except Xavier uniform edge-attention vectors and zero GAT output bias",
        "layer_update": "LayerNorm(x + Dropout(ELU(GATv2(x,edges,history_features)))); LayerNorm eps1e-5, affine; two layers",
        "layers": 2,
        "loops": "explicit self loops with zero edge attributes for all retained nodes",
        "loss": "BCEWithLogitsLoss(pos_weight=168357/4627)",
        "node_features": [
          "log1p_in_count",
          "log1p_out_count",
          "log1p_in_bytes",
          "log1p_out_bytes",
          "log1p_tcp_incident",
          "log1p_udp_incident",
          "log1p_low_source_port",
          "log1p_low_destination_port"
        ],
        "node_input_dim": 8,
        "node_projection": "Linear8->128 with bias",
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0005,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        }
      },
      "dependency": "",
      "family": "graph",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "gatv2_self_only": {
      "budget": {
        "max_epochs": 4
      },
      "cohort": "feb20_matched",
      "configuration": {
        "attention": "edge-aware dynamic GATv2; source/destination/edge linear projections without bias; per-head learnable attention Xavier uniform; LeakyReLU slope .2; stable softmax over incoming edges; attention dropout .2",
        "batch": "one entire target-minute graph per update",
        "capacity_caveat": "unused edge-attention parameters remain serialized; equal stored count is not equal active degrees of freedom",
        "channels_per_head": 32,
        "classifier": "concat(src128,dst128,current80)->Linear128->GELU->Dropout.2->Linear1",
        "deterministic_algorithms": true,
        "dropout": 0.2,
        "dtype": "float32",
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(TRAIN graph groups)",
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "hidden": 128,
        "history_edge_dim": 9,
        "initialization": "PyTorch2.6.0 defaults except Xavier uniform edge-attention vectors and zero GAT output bias",
        "inter_node_messages": "empty edges/features; explicit self loops remain; original historical node inputs retained",
        "layer_update": "LayerNorm(x + Dropout(ELU(GATv2(x,edges,history_features)))); LayerNorm eps1e-5, affine; two layers",
        "layers": 2,
        "loops": "explicit self loops with zero edge attributes for all retained nodes",
        "loss": "BCEWithLogitsLoss(pos_weight=168357/4627)",
        "node_features": [
          "log1p_in_count",
          "log1p_out_count",
          "log1p_in_bytes",
          "log1p_out_bytes",
          "log1p_tcp_incident",
          "log1p_udp_incident",
          "log1p_low_source_port",
          "log1p_low_destination_port"
        ],
        "node_input_dim": 8,
        "node_projection": "Linear8->128 with bias",
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0005,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        }
      },
      "dependency": "",
      "family": "graph_ablation",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_planned_resource_conditional"
    },
    "isolation_forest": {
      "cohort": "full_dataset",
      "configuration": {
        "bootstrap": false,
        "contamination": "auto",
        "max_features": 1.0,
        "max_samples": 256,
        "n_estimators": 100,
        "n_jobs": 2,
        "random_state": 42,
        "sample_size": 250000,
        "sampling": "uniform without replacement from benign TRAIN IDs using NumPy seed 42"
      },
      "policy": "Use only protected Phase7 seed42 predictions/metrics, explicitly development evidence; no five-seed mean/std or silent promotion",
      "status": "development_seed42_secondary_only",
      "training_authorized": false
    },
    "logistic_regression": {
      "budget": {
        "max_epochs": 5
      },
      "cohort": "full_dataset",
      "configuration": {
        "class_weights": {
          "0": 0.5877069457449596,
          "1": 3.3504013892692983
        },
        "dtype": "float32 model inputs; frozen float64 transformation before conversion",
        "epoch_shuffle": "NumPy default_rng(s+epoch-1).permutation(all TRAIN indices)",
        "estimator": {
          "alpha": 0.0001,
          "average": true,
          "class_weight": {
            "0": 0.5877069457449596,
            "1": 3.3504013892692983
          },
          "early_stopping": false,
          "epsilon": 0.1,
          "eta0": 0.001,
          "execution": "partial_fit each outer batch with classes=[0,1]; max_iter/tol do not replace the five-pass externally controlled schedule",
          "fit_intercept": true,
          "l1_ratio": 0.15,
          "learning_rate": "constant",
          "loss": "log_loss",
          "max_iter": 1000,
          "n_iter_no_change": 5,
          "n_jobs": null,
          "penalty": "l2",
          "power_t": 0.5,
          "random_state": "s",
          "shuffle": true,
          "tol": 0.001,
          "validation_fraction": 0.1,
          "verbose": 0,
          "warm_start": false
        },
        "implementation": "sklearn.SGDClassifier incremental logistic regression",
        "outer_batch_size": 50000,
        "seed": "s",
        "test_access_for_selection": false,
        "train_rows": 12795136
      },
      "dependency": "",
      "family": "supervised",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "mlp": {
      "budget": {
        "max_epochs": 5
      },
      "cohort": "full_dataset",
      "configuration": {
        "class_weights": {
          "0": 0.5877069457449596,
          "1": 3.3504013892692983
        },
        "dtype": "float32 model inputs; frozen float64 transformation before conversion",
        "epoch_shuffle": "NumPy default_rng(s+epoch-1).permutation(all TRAIN indices)",
        "estimator": {
          "activation": "relu",
          "alpha": 0.0001,
          "batch_size": 2048,
          "beta_1": 0.9,
          "beta_2": 0.999,
          "early_stopping": false,
          "epsilon": 1e-08,
          "execution": "partial_fit(classes=[0,1]) on each 50000-row outer batch; internal batch2048; external five-pass schedule and validation checkpointing",
          "hidden_layer_sizes": [
            64,
            32
          ],
          "learning_rate": "constant",
          "learning_rate_init": 0.001,
          "max_fun": 15000,
          "max_iter": 200,
          "momentum": 0.9,
          "n_iter_no_change": 10,
          "nesterovs_momentum": true,
          "power_t": 0.5,
          "random_state": "s",
          "sample_weight": "TRAIN inverse-frequency weight per row in every partial_fit call",
          "shuffle": true,
          "solver": "adam",
          "tol": 0.0001,
          "validation_fraction": 0.1,
          "verbose": false,
          "warm_start": false
        },
        "implementation": "sklearn.MLPClassifier",
        "outer_batch_size": 50000,
        "seed": "s",
        "test_access_for_selection": false,
        "train_rows": 12795136
      },
      "dependency": "",
      "family": "supervised",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "random_forest": {
      "budget": {
        "tree_checkpoints": [
          16,
          32,
          64
        ]
      },
      "cohort": "full_dataset",
      "configuration": {
        "class_weights": {
          "0": 0.5877069457449596,
          "1": 3.3504013892692983
        },
        "dtype": "float32 model inputs; frozen float64 transformation before conversion",
        "epoch_shuffle": "NumPy default_rng(s+epoch-1).permutation(all TRAIN indices)",
        "estimator": {
          "bootstrap": true,
          "ccp_alpha": 0.0,
          "class_weight": {
            "0": 0.5877069457449596,
            "1": 3.3504013892692983
          },
          "criterion": "gini",
          "execution": "fit same full TRAIN cache at each warm-start checkpoint; all rows eligible, each tree bootstrap draws 500000; validation chooses checkpoint",
          "max_depth": 16,
          "max_features": "sqrt",
          "max_leaf_nodes": null,
          "max_samples": 500000,
          "min_impurity_decrease": 0.0,
          "min_samples_leaf": 20,
          "min_samples_split": 2,
          "min_weight_fraction_leaf": 0.0,
          "monotonic_cst": null,
          "n_estimators_initial": 16,
          "n_jobs": 1,
          "oob_score": false,
          "random_state": "s",
          "tree_checkpoints": [
            16,
            32,
            64
          ],
          "verbose": 0,
          "warm_start": true
        },
        "implementation": "sklearn.RandomForestClassifier",
        "outer_batch_size": 50000,
        "seed": "s",
        "test_access_for_selection": false,
        "train_rows": 12795136
      },
      "dependency": "",
      "family": "supervised",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "rf_or_ae": {
      "OR_cap": "two approximately1% component caps do not imply1% union cap; explicitly compare actual FPR and family tradeoffs",
      "cohort": "full_dataset",
      "decision": "(RF_score >= seed-specific full-validation label-aware FPR<=.01 threshold) OR (AE_error >= seed-specific benign-validation ProtocolA .01 threshold)",
      "dependencies": [
        "random_forest[s]",
        "autoencoder_B[s]"
      ],
      "reporting": "RF alone, AE alone and OR on same full test IDs; no score normalization, alpha, calibration model or fitted fusion",
      "status": "derived_no_training",
      "thresholds": "freeze each component before test evaluation; do not recalibrate OR union; do not reuse seed42 numeric thresholds across seeds"
    },
    "transformer_L1": {
      "budget": {
        "max_epochs": 3
      },
      "cohort": "phase5_matched",
      "configuration": {
        "activation": "gelu",
        "attention": "bidirectional within supplied start-ordered historical/current window; no future-index flow",
        "batch_first": true,
        "batch_size": 256,
        "bias": true,
        "context_length": 64,
        "control": true,
        "d_model": 64,
        "deterministic_algorithms": true,
        "dropout": 0.1,
        "dtype": "float32",
        "enable_nested_tensor": false,
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(number of fixed TRAIN targets)",
        "feedforward_dim": 128,
        "final_norm": "LayerNorm64 eps1e-5",
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "initialization": "PyTorch defaults for scalar/vector parameters; Xavier uniform for every parameter with dimension>1; positional encoding is a buffer",
        "input_features": 80,
        "layer_norm_eps": 1e-05,
        "layers": 2,
        "length": 1,
        "loss": "BCEWithLogitsLoss(pos_weight=85086/14876)",
        "name": "transformer_L1_control",
        "norm_first": true,
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0003,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        },
        "output": "linear64->1 on last token; sigmoid scores",
        "position": "fixed sinusoid,64 slots; even sin odd cos; exp(arange(0,64,2)*(-log10000/64)); current position63 for both lengths",
        "position_offset": 63,
        "seed": "s"
      },
      "dependency": "",
      "family": "temporal",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "transformer_L64": {
      "budget": {
        "max_epochs": 3
      },
      "cohort": "phase5_matched",
      "configuration": {
        "activation": "gelu",
        "attention": "bidirectional within supplied start-ordered historical/current window; no future-index flow",
        "batch_first": true,
        "batch_size": 256,
        "bias": true,
        "context_length": 64,
        "control": false,
        "d_model": 64,
        "deterministic_algorithms": true,
        "dropout": 0.1,
        "dtype": "float32",
        "enable_nested_tensor": false,
        "epoch_shuffle": "default_rng(s+epoch-1).permutation(number of fixed TRAIN targets)",
        "feedforward_dim": 128,
        "final_norm": "LayerNorm64 eps1e-5",
        "gradient_clip_norm": 1.0,
        "heads": 4,
        "initialization": "PyTorch defaults for scalar/vector parameters; Xavier uniform for every parameter with dimension>1; positional encoding is a buffer",
        "input_features": 80,
        "layer_norm_eps": 1e-05,
        "layers": 2,
        "length": 64,
        "loss": "BCEWithLogitsLoss(pos_weight=85086/14876)",
        "name": "transformer_L64_d64_n2_p01",
        "norm_first": true,
        "optimizer": {
          "amsgrad": false,
          "betas": [
            0.9,
            0.999
          ],
          "capturable": false,
          "differentiable": false,
          "eps": 1e-08,
          "foreach": null,
          "fused": null,
          "lr": 0.0003,
          "maximize": false,
          "name": "AdamW",
          "weight_decay": 0.01
        },
        "output": "linear64->1 on last token; sigmoid scores",
        "position": "fixed sinusoid,64 slots; even sin odd cos; exp(arange(0,64,2)*(-log10000/64)); current position63 for both lengths",
        "position_offset": 0,
        "seed": "s"
      },
      "dependency": "",
      "family": "temporal",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    },
    "xgboost": {
      "budget": {
        "round_checkpoints": [
          20,
          40,
          60,
          80,
          100
        ]
      },
      "cohort": "full_dataset",
      "configuration": {
        "class_weights": {
          "0": 0.5877069457449596,
          "1": 3.3504013892692983
        },
        "dtype": "float32 model inputs; frozen float64 transformation before conversion",
        "epoch_shuffle": "NumPy default_rng(s+epoch-1).permutation(all TRAIN indices)",
        "estimator": {
          "base_score": "XGBoost3.0.5 default automatic intercept estimation; no manual tuning",
          "booster": "gbtree",
          "colsample_bytree": 0.8,
          "device": "cpu",
          "eta": 0.1,
          "execution": "QuantileDMatrix from 50000-row CacheIterator; max_bin128,nthread2; callback checks only at 20/40/60/80/100 rounds",
          "gamma": 0.0,
          "grow_policy": "depthwise",
          "max_bin": 128,
          "max_delta_step": 0.0,
          "max_depth": 6,
          "min_child_weight": 1.0,
          "nthread": 2,
          "objective": "binary:logistic",
          "reg_alpha": 0.0,
          "reg_lambda": 1.0,
          "sampling_method": "uniform",
          "scale_pos_weight": 5.700802778538597,
          "seed": "s",
          "seed_per_iteration": true,
          "subsample": 0.8,
          "tree_method": "hist"
        },
        "implementation": "xgboost.train",
        "outer_batch_size": 50000,
        "seed": "s",
        "test_access_for_selection": false,
        "train_rows": 12795136
      },
      "dependency": "",
      "family": "supervised",
      "selection": {
        "metric": "validation macro-F1 at fixed .5",
        "minimum_improvement": 1e-05,
        "patience": 2,
        "rule": "score > best + minimum_improvement; save improving checkpoint; ties retain earlier checkpoint; restore best; stop after 2 nonimproving scheduled checks"
      },
      "status": "five_seed_required"
    }
  },
  "phase": 10,
  "planned_fit_count": {
    "derived_fusion_rows": 5,
    "required": 55,
    "resource_conditional_self_only": 5,
    "total_if_all_feasible": 60
  },
  "protocols": {
    "anomaly": {
      "activation": "ReLU",
      "architecture": [
        128,
        32,
        128
      ],
      "architecture_search": "disabled",
      "batch_size": 8192,
      "dropout": 0.0,
      "learning_rate": 0.001,
      "loss": "mean squared reconstruction error",
      "max_epochs": 4,
      "min_relative_improvement": 0.0001,
      "optimizer": "AdamW",
      "patience": 2,
      "preprocessing": "reuse baseline_v1 train-fitted preprocessing unchanged; it was fitted on all TRAIN classes, not benign-only",
      "protocol_A_caps": [
        0.05,
        0.01,
        0.005,
        0.001
      ],
      "protocol_A_rule": "conservative upper order statistic with >= detection; nextafter boundary handles ties",
      "protocol_B": "excluded from final calibration",
      "read_block_size": 65536,
      "score": "per-record feature-mean squared reconstruction error; higher is more anomalous",
      "selection": "lowest benign-validation mean reconstruction error; malicious validation scores unavailable to selection",
      "temporal_autoencoder": "not run; optional secondary scope deferred",
      "threads": 2,
      "training_population": "all benign TRAIN rows; no AE subsampling",
      "weight_decay": 1e-05
    },
    "coverage_gate_amendment": {
      "original_passed": false,
      "original_rule": "TRAIN only, label-free: >=50% targets have >=3 and >=7 populated slots among previous 3 and 7 minutes respectively; otherwise stop",
      "reason": "A majority-full-context rule needlessly rejects substantial temporal support despite the explicitly required missing-history masking. Retain all targets and report masking coverage. This gate revision is diagnostic-stage development, not preregistration.",
      "revised_rule": "Diagnostic-stage revised TRAIN-only gate: >=10000 fully populated L4 and L8 contexts; missing contexts masked for all remaining targets; no test metrics used",
      "selection_uses_test_metrics": false,
      "stage": "before any model fitting",
      "training_full_context_counts": {
        "L4": 86935,
        "L8": 74150
      },
      "training_started": false
    },
    "graph": {
      "architecture_search": "disabled",
      "batch_graphs": 1,
      "cutoff_second": 30,
      "detection_time": "flow completion; target features may summarize the full current flow. No claim of start-time detection.",
      "endpoint_id_policy": "indices only, never learned identity embeddings or numerical IP features",
      "evaluation_stride": 4,
      "final_windows": [
        1
      ],
      "gradient_clip_norm": 1.0,
      "historical_edge_feature_names": [
        "Flow Duration",
        "Tot Fwd Pkts",
        "Tot Bwd Pkts",
        "TotLen Fwd Pkts",
        "TotLen Bwd Pkts",
        "Dst Port",
        "Protocol=0",
        "Protocol=6",
        "Protocol=17"
      ],
      "history_cap_policy": "most recently completed eligible flows; source_row breaks completion ties",
      "history_edge_cap": 8192,
      "history_state": "reset at partition/window boundaries; validation/test history may use earlier unlabeled completed flows from that same partition",
      "learning_rate": 0.0005,
      "max_epochs": 4,
      "message_passing": "directed historical Source IP -> Destination IP, two layers, explicit self loops with zero edge attributes",
      "min_improvement": 1e-05,
      "node_features": [
        "log1p_in_count",
        "log1p_out_count",
        "log1p_in_bytes",
        "log1p_out_bytes",
        "log1p_tcp_incident",
        "log1p_udp_incident",
        "log1p_low_source_port",
        "log1p_low_destination_port"
      ],
      "node_history": "all completed flows within the assigned calendar window before cutoff; no labels",
      "patience": 2,
      "primary_window_minutes": 1,
      "selection_metric": "validation_macro_f1_at_0.5",
      "snapshot_rule": "one causal prefix per occupied target minute at second 30; reset calendar window and partition",
      "target_rule": "current completed flow binary label; current features available at classification time",
      "target_seconds": [
        30,
        60
      ],
      "threads": 2,
      "train_stride": 16,
      "weight_decay": 0.01
    },
    "graph_semantics": "Use exact approved start-time membership before10:30 / [10:30,11:00) / >=11:00. Every minute second30 cutoff; targets start in final30sec, stride16 TRAIN/4 validation-test resetting minute. Current flow features available at completion; within-current-minute history starts before cutoff and completes strictly before cutoff. No partition crossing. Aggregate all history; cap messages8192 most recently completed, ties source_row; prune irrelevant nodes after aggregation; directed source->destination; IP IDs topology only.",
    "graph_split_limit": "Start-time membership allows6097 TRAIN flows (253 targets) and5397 validation flows (832 targets) to finish at/after next partition start. Retain membership; no cross-partition history; offline benchmark, not boundary-time deployment replay; no silent purge/embargo.",
    "graph_temporal": {
      "batch_size": 2048,
      "coverage_gate": "Diagnostic-stage revised TRAIN-only gate: >=10000 fully populated L4 and L8 contexts; missing contexts masked for all remaining targets; no test metrics used",
      "d_model": 64,
      "dropout": 0.1,
      "eligibility": "same partition; prior minute; completion strictly before current minute second30 cutoff; source_row breaks completion ties",
      "encoder": "gatv2_w1_h128_p2",
      "encoder_frozen": true,
      "epochs": 4,
      "gat_dropout": 0.2,
      "gat_heads": 4,
      "gat_layers": 2,
      "heads": 4,
      "hidden": 128,
      "historical_observation": "one completed Phase6 sampled target flow representation from an earlier minute; frozen own-minute GAT context and own complete flow vector",
      "identity": "directed pair first, same source endpoint second, same destination endpoint third; latest eligible completion within that minute",
      "layers": 2,
      "learning_rate": 0.0005,
      "lengths": [
        1,
        8
      ],
      "padding": "missing historical slots zero padded and key-padding masked; current always present; learned absolute slot positions shared across L1/4/8",
      "patience": 2,
      "representation": "concat frozen GAT source node embedding, destination node embedding, current full flow features; historical tokens belong to earlier completed observed flows",
      "scope": "sampled-target history; no labels, raw endpoint ID features, cross-partition tokens or future snapshots",
      "selection": "validation macro-F1 at .5; min improvement .00001",
      "temporal_step": "one previous calendar minute; L includes current step and L-1 preceding minutes; no compression of missing minutes",
      "threads": 2,
      "weight_decay": 0.01,
      "window_minutes": 1
    },
    "graph_temporal_gate": "Reuse exact Phase9 cohort/history indices and hashes. The documented diagnostic-stage gate amendment is fixed now; do not rerun or relax it based on final-seed outcomes.",
    "graph_temporal_semantics": "History lookup uses only fixed Phase6 sampled targets in previous calendar-minute slots. Latest eligible directed pair first, same source second, same destination third; eligible completion strictly before current second30 cutoff; ascending source_row breaks completion ties by retaining greatest. L8=current+7 previous minutes, L1=current; missing slots zero/key-masked without time compression; per-partition reset. Same-seed graph embeddings frozen in eval mode; own flow features only after its completion. Retain all original targets.",
    "temporal": {
      "ablation": "same architecture and target records; only final flow with same final positional index",
      "attention": "bidirectional within historical window including current flow; no later flow is present",
      "batch_size": 256,
      "evaluation_stride": 8,
      "feature_dtype": "float32",
      "feedforward_multiplier": 2,
      "gradient_clip_norm": 1.0,
      "learning_rate": 0.0003,
      "lengths": [
        1,
        64
      ],
      "max_epochs": 3,
      "min_improvement": 1e-05,
      "model_search": "disabled",
      "optimizer": "AdamW",
      "patience": 2,
      "position_encoding": "fixed sinusoidal",
      "selection_metric": "validation_macro_f1_at_0.5",
      "small_architecture": {
        "d_model": 64,
        "dropout": 0.1,
        "heads": 4,
        "layers": 2
      },
      "threads": 2,
      "train_stride": 128,
      "warmup": 63,
      "weight_decay": 0.01
    },
    "temporal_matched_controls": "Slice each seed full-data conventional predictions to exact Phase5 validation/test partition_index IDs; independently recalibrate FPR<=1% on that matched validation slice; no control refit; do not borrow full-validation numeric threshold for the slice.",
    "temporal_semantics": "Same-day start-timestamp ordered global adjacent-flow sequences; exclude first63 each day; TRAIN targets every128 from day_start+63, validation/test every8; L1 takes only current at position63; L64 takes target-63 through target; no cross-day/partition sequences. Phase5 is not endpoint-consistent graph history and does not establish completion-causal online availability."
  },
  "research_questions": {
    "RQ1": "How effectively do conventional and neural flow-based models detect malicious traffic under chronological distribution shift?",
    "RQ2": "How effectively do models detect attack families absent from the training period, particularly Bot and Infilteration?",
    "RQ3": "Does graph-based relational modeling improve DDoS detection over matched non-graph controls on the Feb-20 network-flow graph subset?",
    "RQ4": "Does explicit temporal context provide incremental benefit over capacity-matched non-temporal controls?",
    "RQ5": "Does a benign-trained reconstruction anomaly branch provide complementary detection behavior for attack families absent from training?",
    "RQ6": "What computational overhead is introduced by graph, temporal and anomaly components?"
  },
  "runtime": {
    "comparison": "Keep hardware and measurement definitions fixed across final seeds. Never compare full-cohort flow timing, sampled temporal timing, Feb20 graph timing and cached-pipeline timing without explicit scope qualification. Record any hardware change and do not pool incompatible timing runs.",
    "concurrent_training_jobs": 1,
    "device": "cpu",
    "environment_policy": "Verify exact modeling versions before fitting; baseline preparation originally used sklearn1.6.1 but is transform-only and never refitted. The Phase10 sandbox inspection resolved sklearn1.6.1; this does not authorize use for final fitting. Read the isolated recorded runtime and fail if version checks disagree.",
    "graph_temporal": "Same-seed frozen encoder reused by L1/L8. Report shared embedding preparation and shared history-index preparation once, head-only inference and preparation-inclusive total; include diagnostic-count work in its own explicitly labeled replay cost. Do not add repeated shared costs across models.",
    "hardware": {
      "cpu": "Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz",
      "logical_cpus": 8,
      "physical_cores": 4,
      "platform": "Windows-11-10.0.22631-SP0",
      "ram_bytes": 16944599040
    },
    "inference": "Report model-only compute, feature transformation/loading, graph-prefix construction/encoding, sequence/history construction and lookup, and complete available-pipeline total separately. Raw cleaning/join/cache materialization/model loading are separately recorded preparation stages, never silently omitted from a claimed end-to-end value.",
    "latency": "1000 * 1000 * inference_seconds / number_of_evaluated_target_flows_or_edges, in milliseconds per 1000; name the corresponding stage and cohort.",
    "memory": "Process high-water RSS/Windows peak working set bytes, including dependencies and resident caches; poll every .05 seconds; use a separate worker per fit/evaluation. For separately executed stages report max(stage peaks), not their sum; disclose that as an amortized pipeline maximum.",
    "model_size": "Checkpoint bytes; report head-only and required pipeline size, counting shared encoder once. Preserve unused serialized parameters caveat for self-only and unused positional slots.",
    "repeat_policy": "One measured training/evaluation run per seed under the same cache policy; no picking fastest repeats. Repeated values across partition rows are not independent costs.",
    "rf_n_jobs": 1,
    "software": {
      "joblib": "1.4.2",
      "matplotlib": "3.10.0",
      "numpy": "2.1.3",
      "pandas": "2.2.3",
      "psutil": "5.9.0",
      "pyarrow": "19.0.0",
      "python": "3.13.5",
      "scikit_learn": "1.7.2",
      "scipy": "1.15.3",
      "threadpoolctl": "3.5.0",
      "torch": "2.6.0+cpu",
      "xgboost": "3.0.5"
    },
    "threads": 2,
    "training": "Report optimizer/fit wall seconds separately from validation-selection seconds, input/preparation seconds and total stage wall seconds; include necessary XGBoost quantile matrix construction in fitting cost; no subtracting undocumented costs."
  },
  "schema_version": 1,
  "seed_mapping": {
    "data_membership": "unchanged across all seeds",
    "deterministic_algorithms": true,
    "epoch_order": "s+epoch-1",
    "fixed_data_preparation_seed": 20260920,
    "numpy_global": "s",
    "python_random": "s",
    "sklearn_random_state": "s",
    "torch_manual_seed": "s",
    "xgboost_seed": "s"
  },
  "seeds": [
    42,
    123,
    456,
    789,
    1024
  ],
  "seeds_policy": "Fresh fits for all five seeds including42; development42 remains immutable and is not substituted into final aggregation. Replace only stochastic seed inputs; same seed across paired components. No architecture/hyperparameter/threshold-rule changes after other seeds.",
  "self_only_resource_rule": "Plan all five self-only seeds. If infeasible, document measured resource reason before omission; do not inspect performance to decide. No changed width/budget, no replacement seed; any partial run remains explicitly incomplete secondary evidence.",
  "specification": "final_spec_v1",
  "specification_generator": [
    {
      "bytes": 49323,
      "path": "src/final_spec/freeze.py",
      "sha256": "d5f12f8ad8dbf92ba405bc01c7bf3fecda3080414372c9ccbe41e7cc8bd37d6b"
    },
    {
      "bytes": 91,
      "path": "src/final_spec/__init__.py",
      "sha256": "36e7502492959df49a2fffe45fe28f1dfee8ce2eb65a9826c61af454f5be627f"
    }
  ],
  "statistics": {
    "mean": "arithmetic per-seed metric mean",
    "metrics": [
      "accuracy",
      "precision",
      "recall",
      "f1",
      "macro_f1",
      "false_positive_rate",
      "roc_auc",
      "pr_auc",
      "average_precision"
    ],
    "no_confusion_count_pooling": true,
    "no_significance_claim": true,
    "paired_differences": true,
    "seeds": [
      42,
      123,
      456,
      789,
      1024
    ],
    "std": "sample standard deviation ddof1",
    "supplementary": [
      "false_negative_rate",
      "TN",
      "FP",
      "FN",
      "TP",
      "family_N",
      "family_detected",
      "family_recall"
    ],
    "test_already_observed": true,
    "uncertainty": "training stochasticity on fixed data, not independent dataset/split replications"
  },
  "status": "frozen_awaiting_explicit_execution_approval",
  "stopping_rule": "Phase10 ends with specification files only. Explicit user approval is required before ANY final training, including the fresh seed42 rerun. Existing development runners have hard-coded42 and old output paths; do not invoke them for final runs. A separate seed-parameterized final runner must enforce this spec without modifying frozen development sources.",
  "thresholds": {
    "anomaly_algorithm": "Sort all benign validation errors ascending b (N>0). k=floor(cap*N), threshold=nextafter(b[N-k-1],+inf). Compare >=; verify false positives<=k. Ties conservatively excluded; raw errors are not probabilities.",
    "anomaly_primary": {
      "cap": 0.01,
      "protocol": "A_benign_only"
    },
    "anomaly_protocol_B": "not authorized for final selection",
    "anomaly_secondary_caps": [
      0.05,
      0.005,
      0.001
    ],
    "cap_limitation": "Empirical validation cap is not a population/test guarantee; OR union not capped.",
    "comparator": ">=",
    "graph_and_graph_temporal": [
      "fixed_0_5",
      "maximum_macro_f1",
      "validation_fpr_at_most_0.01"
    ],
    "label_aware_algorithm": "Candidates unique validation scores descending plus nextafter(max_score,+inf), evaluate >= threshold. Macro-F1: maximize then highest threshold. FPR cap: feasible FP/N_benign<=cap; maximize TP/recall then minimize FP then highest threshold. Use only the evaluated cohort validation labels; never test.",
    "per_seed": "Recalibrate numeric thresholds from that seed validation scores under fixed rules. Freeze model hash, score hash, cohort hash and thresholds before test scoring/evaluation. Test labels never select anything.",
    "supervised_primary": [
      "fixed_0_5",
      "validation_fpr_at_most_0.01"
    ],
    "temporal_primary": [
      "fixed_0_5",
      "validation_fpr_at_most_0.01"
    ],
    "temporal_secondary": [
      "maximum_macro_f1",
      "validation_fpr_at_most_0.005",
      "validation_fpr_at_most_0.001"
    ]
  }
}
```
