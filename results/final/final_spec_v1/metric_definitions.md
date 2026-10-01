# Frozen metric definitions

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
