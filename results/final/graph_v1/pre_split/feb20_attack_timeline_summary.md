# Feb-20 pre-split review — no model training

Status: **PROPOSED, awaiting review**. No preprocessing was fitted, graph model trained, or test model performance measured. Seed 42 is reserved for development.

Verified frozen raw and cleaned SHA-256 checksums. The cleaned cohort has 7,948,746 flows: 7,372,555 benign and 576,191 DDoS attacks-LOIC-HTTP. Exactly 2 raw rows are excluded by existing cleaning. All 720 minutes from 2018-02-20 01:00:00 through 2018-02-20 13:00:00 (exclusive) are included in the timeline, including any empty minutes.

The cleaned parquet excludes IP metadata. Unique endpoint counts therefore come from a read-only join to the original CSV using retained source_row IDs; labels and minute timestamps were cross-checked. Excluded raw rows never enter the timeline. Source IP, destination IP, source port, destination port and protocol are present with no missing values in retained rows. Raw identifier values are not encoded as numeric features.

## Attack timeline

| start | end_exclusive | active_minutes | benign | malicious |
| --- | --- | --- | --- | --- |
| 2018-02-20 01:14:00 | 2018-02-20 01:30:00 | 16 | 215184 | 797 |
| 2018-02-20 10:13:00 | 2018-02-20 11:17:00 | 64 | 939885 | 575394 |

Times above are the existing audited, parsed timestamp values. The early 01:14 attack cluster is retained as recorded; no timezone or AM/PM correction is inferred. The source provides second-resolution timestamps, so equal-time causal ordering must be explicitly specified before graph training.

## Simple elapsed-time split checks

Boundaries are rounded to the nearest ten-minute clock boundary so none of the planned window sizes straddles a split. Fractions refer to elapsed time, not equal flow counts.

| candidate | partition | rows | benign | malicious |
| --- | --- | --- | --- | --- |
| elapsed_80_10_10 | train | 5754139 | 5514050 | 240089 |
| elapsed_80_10_10 | validation | 1376718 | 1040616 | 336102 |
| elapsed_80_10_10 | test | 817889 | 817889 | 0 |
| elapsed_70_15_15 | train | 4343635 | 4342838 | 797 |
| elapsed_70_15_15 | validation | 2124531 | 1608882 | 515649 |
| elapsed_70_15_15 | test | 1480580 | 1420835 | 59745 |
| elapsed_60_20_20 | train | 3598024 | 3597227 | 797 |
| elapsed_60_20_20 | validation | 2156115 | 1916823 | 239292 |
| elapsed_60_20_20 | test | 2194607 | 1858505 | 336102 |

The 80/10/10 candidate leaves test without malicious flows. Earlier training cutoffs in the 70/15/15 and 60/20/20 candidates retain only the 797-example early attack cluster in training. None puts all malicious traffic in one partition, but class presence alone does not ensure a useful protocol. No random or stratified split has been substituted.

## Proposed chronological split for review

Train: before **10:30**; validation: **10:30–11:00**; test: **11:00 onward**, all on 2018-02-20. Boundaries are half-open and aligned with the predeclared primary 1-minute and sensitivity 5/10-minute windows. Every eligible flow belongs to exactly one partition.

| partition | timestamp_min | timestamp_max | rows | benign | malicious | malicious_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| train | 2018-02-20 01:00:00 | 2018-02-20 10:29:59 | 5507159 | 5359206 | 147953 | 0.02686557624357677 |
| validation | 2018-02-20 10:30:00 | 2018-02-20 10:59:59 | 727258 | 450793 | 276465 | 0.3801470729782278 |
| test | 2018-02-20 11:00:00 | 2018-02-20 12:59:59 | 1714329 | 1562556 | 151773 | 0.08853201456663219 |

This is an explicitly timeline-informed proposal, not a finalized split. It gives all three partitions observations from the main attack period, but evaluates continuation of the same within-day attack episode, with potentially recurring endpoints and correlated adjacent windows. It cannot establish generalization to unseen attacks, independent incidents or other days. Different partition durations and class prevalence must remain visible in later results.

## Review gate and next-stage constraints

The Phase 6 request says **“STOP BEFORE MODEL TRAINING”** and **“Do not train GATv2 until this split has been reviewed.”** Review the proposed 10:30/11:00 boundaries before proceeding. No split is approved automatically. Membership hashes in proposed_split.json identify the proposed source-row sets in chronological order; they are not approval or fitted preprocessing artifacts.

After approval, fit preprocessing exclusively on the approved Feb-20 train partition. The earlier baseline_v1 preprocessing includes future Feb-20 rows and must not be reused. Node aggregates alone being historical is insufficient: message passing must also exclude future flows within a target snapshot. Declare this causal graph construction, timestamp-tie policy and history-state handling before training. The matched edge MLP must share target edges, eligible flow features, preprocessing and partitions. Phase 4 test metrics are not comparable to this cohort.

Reproduce with `python -m src.graph.pre_split`. This command reads verified sources and writes only results/graph_v1/pre_split; it does not construct graphs, fit preprocessing or train models.
