# Baseline preparation results

Binary target: Benign = 0, observed attacks = 1. All original attack labels are retained as metadata. No classifier training, model evaluation, graph construction, GATv2 or AIGT-CTD implementation was performed.

## Cleaning

| Measure | Records |
| --- | --- |
| cleaned_rows | 15,822,236 |
| exact_nonheader_duplicates | 410,707 |
| raw_rows | 16,233,002 |
| repeated_headers | 59 |
| temporal_exclusions | 14 |
| temporal_rows | 15,822,222 |
| year_1970_temporal_exclusions | 14 |

The Phase 2 duplicate count includes 56 repeated-header duplicates. Removing all 59 headers first leaves 410,707 non-header duplicates. The 14 year-1970 records remain in non-temporal quarantine files and are excluded from temporal partitions.

All raw SHA-256 hashes were recomputed after preparation and remain unchanged. Every raw data row is accounted for exactly once as temporally eligible, removed, or quarantined.

## Frozen chronological split

The complete class/file/date report was written before split selection. Whole-date candidates were ranked by training attack-class coverage and closeness to the configured 80/10/10 row proportions, subject to binary representation minimums. No shuffled or within-day stratified split was used.

| Partition | Dates | Records | Benign | Malicious | Attacks unseen in training |
| --- | --- | --- | --- | --- | --- |
| train | 2018-02-14 through 2018-02-22 | 12,795,136 | 10,885,643 | 1,909,493 | None |
| validation | 2018-02-23 through 2018-02-28 | 1,652,943 | 1,583,520 | 69,423 | Infilteration |
| test | 2018-03-01 through 2018-03-02 | 1,374,143 | 998,793 | 375,350 | Bot, Infilteration |

Class distribution for each partition, including zero-count classes, is saved in [partition_class_distribution.csv](partition_class_distribution.csv). Unseen attacks remain positive binary targets. These date-separated attack types prevent a claim of complete closed-set multiclass coverage.

Order is by the recorded day-first timestamp, then original source row. The source supplies no timezone or AM/PM marker. No missing clock information was reconstructed.

## Fitted preprocessing

| Property | Value |
| --- | --- |
| Fit partition | train |
| Training rows | 12,795,136 |
| Numeric features | 77 |
| Categorical features | 1 |
| Output features | 80 |
| Protocol categories | {"Protocol": ["0", "17", "6"]} |
| Numeric imputation | Mean from finite training values only |
| Categorical imputation | Training mode only |
| Scaling | StandardScaler fitted on imputed training rows only |
| Unknown categories | All-zero one-hot block; counted in application audit |
| All-missing training features | None |
| Additional direct target encodings excluded | None detected |

Label, target-named fields, timestamps and identifiers are excluded from model inputs. Training-only one-to-one target-encoding checks supplement the schema exclusions. All exclusion reasons are in [feature_exclusion_audit.csv](feature_exclusion_audit.csv). Correlation alone is not treated as proof of target leakage.

The saved preprocessor was reloaded and applied unchanged to every training, validation and test row. All transformed values were finite. Feature batches are generated on demand, so no second full scaled copy consumes disk space.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [cleaning_audit.csv](cleaning_audit.csv) | Each removed/excluded source row and retained duplicate reference |
| [cleaning_summary.csv](cleaning_summary.csv) | Per-file row conservation |
| [cleaning_cell_audit.csv](cleaning_cell_audit.csv) | Infinity-to-missing conversion and remaining missing counts |
| [pre_split_class_distribution.csv](pre_split_class_distribution.csv) | Class/file/date counts before choosing a split |
| [split_candidates.csv](split_candidates.csv) | Candidate boundaries, counts and deterministic ranking |
| [split_plan.json](split_plan.json) | Exact dates, files, row rules, hashes and membership paths |
| [preprocessing.json](preprocessing.json) | Persisted training-only imputation, categories, scaling and feature order |
| [preprocessing_application_audit.csv](preprocessing_application_audit.csv) | All-partition transform counts and checksums |
| [source_manifest.json](source_manifest.json) | Raw/derived paths, hashes and population counts |
| [verification.json](verification.json) | PASS: source preservation, conservation, chronology and split/preprocessor integrity |

Cleaned features and exact per-row partition membership are stored under `data/baseline_v1/`, with paths and hashes in the manifests. Reproduction commands and the streaming model-input interface are documented in [BASELINE_PIPELINE.md](../../../docs/methodology/BASELINE_PIPELINE.md).
