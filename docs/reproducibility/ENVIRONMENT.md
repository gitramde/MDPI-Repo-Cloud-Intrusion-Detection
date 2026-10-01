# Recorded execution environment

These versions come from preserved records, not packages installed during cleanup. No environment installation, model execution or dependency upgrade was performed.

Baseline preparation used Python 3.13.5, NumPy 2.1.3, pandas 2.2.3, PyArrow 19.0.0 and scikit-learn 1.6.1, as recorded in [requirements-baseline.txt](../../requirements-baseline.txt) and the [preparation guide](../methodology/BASELINE_PIPELINE.md). Final modeling uses scikit-learn 1.7.2; preparation states remain transform-only and must never be refitted to reconcile environments.

## Final modeling versions

The [frozen runtime specification](../../experiments/final_spec/final_experiment_spec.json) records the following versions. The separately archived Phase 11B recovery verification agreed with these values when inspected during the audit; that recovery file is outside the approved 26-file evidence set. No new verification of installed modeling packages was performed.

| Package | Recorded version |
| --- | --- |
| joblib | 1.4.2 |
| matplotlib | 3.10.0 |
| numpy | 2.1.3 |
| pandas | 2.2.3 |
| psutil | 5.9.0 |
| pyarrow | 19.0.0 |
| python | 3.13.5 |
| scikit_learn | 1.7.2 |
| scipy | 1.15.3 |
| threadpoolctl | 3.5.0 |
| torch | 2.6.0+cpu |
| xgboost | 3.0.5 |

CPU execution: Intel Core i7-8565U, four physical cores / eight logical CPUs, Windows 11, approximately 16 GB RAM. PyTorch is the CPU build. Frozen policy: two numerical/PyTorch threads, deterministic algorithms, RF n_jobs=1, one concurrent training job, separate workers for fits/evaluation. Peak memory is a process high-water measurement; separately executed stages use their maximum, not their sum. Runtime comparisons require the same cohort, cache policy, and measured stage.

## Phase differences and limitations

[requirements-phase4.txt](../../requirements-phase4.txt) records the Phase-4 overlay dependencies. [requirements.txt](../../requirements.txt) is an unpinned dataset-audit dependency list, not a complete final-model environment. Imports also require SciPy, PyTorch and the other final packages above. No PyTorch Geometric dependency is inferred merely from the GATv2 model name; the graph implementation is in project source.

The modeling runtime used a system/Anaconda interpreter plus project-local `data/phase4_runtime` and `data/temporal_runtime` overlays. The legacy `.venv` is documented as Python 3.11.7 and is not the recorded Python 3.13.5 modeling environment. A restricted process initially resolved preparation scikit-learn 1.6.1; recovery restored access to existing overlays rather than changing the frozen requirements. The historical recovery summary remains in the separate reference archive and is not bundled. The retained [Phase 11B completion report](../../results/final/phase11b/PHASE_11B_EXECUTION_SUMMARY.md) also documents that recovery reused existing overlays.

These records establish major package versions, but do not provide a complete transitive lockfile, wheel provenance or a portable environment image. Overlays, raw/derived data, scores and checkpoints are omitted from this public document copy. Embedded legacy absolute paths need a separately reviewed portability plan. No install command is represented as sufficient for exact reproduction. The fixed experimental settings, thresholds and seeds remain untouched.
