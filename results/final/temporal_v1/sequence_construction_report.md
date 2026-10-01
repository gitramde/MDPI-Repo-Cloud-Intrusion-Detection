# Phase 5 sequence construction

Frozen membership is already chronological; its original timestamps were scanned for monotonic order and valid calendar days before training. Ties retain frozen membership order. Each sequence contains contiguous historical flow vectors and its final flow; only that final flow supplies the binary target (0 benign, 1 malicious) and diagnostic family. No sequence includes future records or crosses a partition/day boundary. Quarantined 1970 records remain excluded.

Lengths 16, 32 and 64 share target records: exclude the first 63 records of every day for all lengths, then take training stride 128 and validation/test stride 8. This common cohort makes length selection and L1 ablation comparable. Striding reduces CPU work and retains deterministic chronological coverage, but metrics describe sampled targets, not every frozen record. Training batches shuffle already-constructed windows, never their internal temporal order. The L1 control uses identical target records and parameter count, with only the final vector and the same final positional index.

| partition | rows | targets | stride | benign | malicious | coverage_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| test | 1374143 | 171753 | 8 | 124795 | 46958 | 0.124989 |
| train | 12795136 | 99962 | 128 | 85086 | 14876 | 0.007812 |
| validation | 1652943 | 206603 | 8 | 197989 | 8614 | 0.124991 |
