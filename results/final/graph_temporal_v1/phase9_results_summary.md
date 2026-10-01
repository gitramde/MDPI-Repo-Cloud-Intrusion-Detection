# Phase 9 seed-42 graph + temporal contribution results

Frozen Phase-6 primary GATv2 encoder (1-minute window, hidden 128, two layers, four heads, dropout 0.2), followed by separately fitted identical Transformer heads (d_model 64, two layers, four heads, FFN 128, dropout 0.1). Only Transformer heads are trained; this evaluates temporal readout of frozen graph-derived representations, not end-to-end joint training. No graph architecture search was reopened.

All original target edges are retained; current-token availability permits masking absent history. Existing Edge MLP/GAT predictions are reused without refitting and metrics recomputed on exactly this cohort. L1/L4/L8 have equal trainable parameter counts and the same eight-slot position table; unused historical positions remain inactive at L1.

Each historical observation is one Phase-6 sampled target flow represented by its own-minute frozen GAT source/destination embeddings and complete flow vector. For each current target, each previous calendar minute supplies at most one token: latest completed same directed pair first, otherwise latest same-source observation, otherwise latest same-destination observation. Completion must be strictly before the current second-30 graph cutoff. Completion ties use source row. The fallback follows a role-consistent endpoint but may change the interaction partner; it is not pure pair history. Only sampled target observations are in this temporal history; unsampled flows still enter the unchanged Phase-6 node aggregates and messages.

L includes the current target, so L=4 uses the current step plus three preceding calendar minutes and L=8 plus seven. Missing minutes are masked, not compressed into adjacent unrelated flows. History counts count distinct earlier occupied minute steps anywhere within the same partition; recent-slot coverage separately measures the actual contiguous L=4/8 input. Coverage percentages below use all target rows as denominator.

The initial diagnostic gate required at least 50% of TRAIN targets to have every L4/L8 historical slot filled. L8 reached 42.87% (74,150 complete examples), while L4 reached 50.26% (86,935). Before any fitting, the gate was revised to require at least 10,000 complete TRAIN contexts for each length, retaining masking for the rest. This avoids treating substantial support as unusable simply because a majority is not fully populated. The revision used TRAIN coverage, not test performance; it is a documented diagnostic-stage development decision, not preregistered evidence. The original failed gate and revision are retained in configs/coverage_gate_amendment.json.

| partition | label | targets | pair_ge1_percent | pair_ge4_percent | pair_ge8_percent | source_ge8_percent | destination_ge8_percent | previous_3_slots_complete_percent | previous_7_slots_complete_percent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | all | 172984 | 57.76372381260695 | 43.835846089811774 | 38.285043703463906 | 81.52892753086991 | 86.5114692688341 | 50.25609304906812 | 42.865236091199186 |
| train | Benign | 168357 | 56.67718004003398 | 42.64925129338251 | 37.54699834280725 | 81.97936527735705 | 86.15857968483638 | 49.25069940661808 | 42.33503804415617 |
| train | DDoS attacks-LOIC-HTTP | 4627 | 97.29846552842014 | 87.01102226064404 | 65.13939917873353 | 65.13939917873353 | 99.35163172682083 | 86.83812405446294 | 62.156905122109364 |
| validation | all | 88782 | 64.59867991259489 | 47.9950890946363 | 36.07600639769323 | 54.93455880696537 | 63.17609425333964 | 71.9312473249082 | 56.29181590863013 |
| validation | Benign | 54220 | 44.15160457395795 | 23.334562891921802 | 12.305422353375137 | 43.185171523423094 | 56.6801918111398 | 60.39653264478052 | 43.312430837329394 |
| validation | DDoS attacks-LOIC-HTTP | 34562 | 96.67553960997628 | 86.68190498235056 | 73.36670331578034 | 73.36670331578034 | 73.36670331578034 | 90.02661882992882 | 76.6535501417742 |
| test | all | 212591 | 60.38026068836404 | 42.087388459530274 | 32.49337930580316 | 73.54262409979727 | 78.73428320107625 | 68.88203169466252 | 54.063436363721884 |
| test | Benign | 193893 | 57.14388863961051 | 38.878144131041346 | 30.721067805439084 | 75.72888139334582 | 81.42119622678487 | 67.66051378853285 | 53.78997694604756 |
| test | DDoS attacks-LOIC-HTTP | 18698 | 93.94052839875923 | 75.36634934217562 | 50.871750989410636 | 50.871750989410636 | 50.871750989410636 | 81.54882875173816 | 56.89913359717617 |

Full CSV includes source/destination >=1/4/8, counts, percentages, median/p90/max, and fallback token counts by class.

## Training and selection

AdamW lr 0.0005, weight decay 0.01, TRAIN-only positive class weight, batch size 2048, clipping 1.0, at most four epochs and patience two. Epoch selection uses validation macro-F1 at 0.5 only. All sequence lengths are reported; no test-selected winner. Learned positions encode the fixed minute slots; the current output attends only to current and completion-eligible past tokens. Frozen embedding extraction uses no labels.

| model | length | fitted_in_phase9 | selected_epoch | executed_epochs | selected_validation_macro_f1 |
| --- | --- | --- | --- | --- | --- |
| edge_mlp |  | False | 3 | 4 | 0.990354 |
| gatv2_w1_h128_p2 |  | False | 3 | 4 | 0.999929 |
| gat_transformer_L1 | 1 | True | 1 | 3 | 0.999917 |
| gat_transformer_L4 | 4 | True | 1 | 3 | 0.999905 |
| gat_transformer_L8 | 8 | True | 3 | 4 | 0.999929 |

## Matched test component progression

| model | criterion | recall | precision | f1 | macro_f1 | false_positive_rate | roc_auc | average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| edge_mlp | fixed_0_5 | 0.979356 | 0.994893 | 0.987063 | 0.992913 | 0.000485 | 0.999959 | 0.999478 |
| edge_mlp | maximum_macro_f1 | 0.999947 | 0.975428 | 0.987535 | 0.993158 | 0.002429 | 0.999959 | 0.999478 |
| edge_mlp | fpr_at_most_0.01 | 1.000000 | 0.973043 | 0.986338 | 0.992500 | 0.002672 | 0.999959 | 0.999478 |
| gatv2_w1_h128_p2 | fixed_0_5 | 1.000000 | 0.999786 | 0.999893 | 0.999941 | 0.000021 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | maximum_macro_f1 | 0.953578 | 0.999832 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| gatv2_w1_h128_p2 | fpr_at_most_0.01 | 0.953578 | 0.999832 | 0.976157 | 0.986958 | 0.000015 | 0.999999 | 0.999990 |
| gat_transformer_L1 | fixed_0_5 | 1.000000 | 0.999786 | 0.999893 | 0.999941 | 0.000021 | 1.000000 | 0.999999 |
| gat_transformer_L1 | maximum_macro_f1 | 0.973687 | 1.000000 | 0.986668 | 0.992700 | 0.000000 | 1.000000 | 0.999999 |
| gat_transformer_L1 | fpr_at_most_0.01 | 0.973687 | 1.000000 | 0.986668 | 0.992700 | 0.000000 | 1.000000 | 0.999999 |
| gat_transformer_L4 | fixed_0_5 | 1.000000 | 0.999733 | 0.999866 | 0.999927 | 0.000026 | 1.000000 | 0.999999 |
| gat_transformer_L4 | maximum_macro_f1 | 0.966307 | 1.000000 | 0.982865 | 0.990621 | 0.000000 | 1.000000 | 0.999999 |
| gat_transformer_L4 | fpr_at_most_0.01 | 0.966307 | 1.000000 | 0.982865 | 0.990621 | 0.000000 | 1.000000 | 0.999999 |
| gat_transformer_L8 | fixed_0_5 | 1.000000 | 0.999626 | 0.999813 | 0.999897 | 0.000036 | 1.000000 | 0.999995 |
| gat_transformer_L8 | maximum_macro_f1 | 0.983260 | 0.999891 | 0.991506 | 0.995347 | 0.000010 | 1.000000 | 0.999995 |
| gat_transformer_L8 | fpr_at_most_0.01 | 0.983260 | 0.999891 | 0.991506 | 0.995347 | 0.000010 | 1.000000 | 0.999995 |

## Temporal contribution: temporal minus L1 capacity control

Positive FPR differences mean more false alarms. Differences are absolute fractions.

| model | criterion | delta_recall | delta_precision | delta_f1 | delta_macro_f1 | delta_false_positive_rate | delta_roc_auc | delta_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat_transformer_L4 | fixed_0_5 | 0.000000 | -0.000053 | -0.000027 | -0.000015 | 0.000005 | -2.813e-08 | -2.973e-07 |
| gat_transformer_L4 | maximum_macro_f1 | -0.007380 | 0.000000 | -0.003804 | -0.002079 | 0.000000 | -2.813e-08 | -2.973e-07 |
| gat_transformer_L4 | fpr_at_most_0.01 | -0.007380 | 0.000000 | -0.003804 | -0.002079 | 0.000000 | -2.813e-08 | -2.973e-07 |
| gat_transformer_L8 | fixed_0_5 | 0.000000 | -0.000160 | -0.000080 | -0.000044 | 0.000015 | -3.844e-07 | -0.000004 |
| gat_transformer_L8 | maximum_macro_f1 | 0.009573 | -0.000109 | 0.004838 | 0.002647 | 0.000010 | -3.844e-07 | -0.000004 |
| gat_transformer_L8 | fpr_at_most_0.01 | 0.009573 | -0.000109 | 0.004838 | 0.002647 | 0.000010 | -3.844e-07 | -0.000004 |

L4: no consistent temporal benefit across the requested operating points under the joint recall/F1/macro-F1/FPR check.

L8: no consistent temporal benefit across the requested operating points under the joint recall/F1/macro-F1/FPR check.

## Runtime and measurement scope

| model | training_seconds | inference_seconds | latency_ms_per_1000 | peak_memory_bytes | model_size_bytes | total_required_model_bytes |
| --- | --- | --- | --- | --- | --- | --- |
| edge_mlp | 31.241703 | 1.176663 | 5.534868 | 1233817600 | 456850 | 456850 |
| gatv2_w1_h128_p2 | 141.374413 | 5.049065 | 23.750134 | 1234116608 | 460146 | 460146 |
| gat_transformer_L1 | 12.366932 | 5.362501 | 25.224495 | 1787011072 | 366762 | 826908 |
| gat_transformer_L4 | 42.581553 | 10.913229 | 51.334389 | 1787011072 | 366762 | 826908 |
| gat_transformer_L8 | 103.107442 | 13.892282 | 65.347462 | 1787011072 | 366762 | 826908 |

Temporal inference time is an amortized sum of frozen graph-prefix preparation/encoding and measured cached temporal lookup/head inference. Historical tokens are reused rather than recomputed for every target. Metadata/model loading and one-time history-index construction are excluded; representation timings are saved separately. These are not strict online-replay timings. Prior controls retain their original full-cohort Phase-6 timing, while Phase-9 training time for those controls is zero. Training timings for temporal models exclude the shared frozen encoder preparation. Peak memory is process high-water RSS including dependencies, with the maximum of separate representation and head stages; repeated training values must not be summed. Full model size includes the shared frozen encoder once per deployable pipeline; head checkpoint size is also reported.

Membership remains the approved Feb-20 flow-start split: TRAIN before 10:30, validation 10:30 to before 11:00, test from 11:00 onward. Some TRAIN and validation flows complete after the next partition starts. No cross-partition graph or temporal inputs are permitted. This remains an offline start-time-split benchmark, not a strict deployment replay; no completion-time purge or embargo was silently introduced. Labels are used for training targets and coverage diagnostics, never history construction or graph inputs. This is Benign versus DDoS attacks-LOIC-HTTP within-day graph-temporal contribution development, not unseen-threat, zero-day or multiclass detection. Prior test results were already observed; no untouched confirmatory test or statistical significance is claimed. Seed 42 only. No anomaly branch, risk fusion, explainability or five-seed experiments were added.

## Independent verification and preparation costs

All saved metrics were independently recomputed. All temporal indices were replayed exactly after lookup optimization; partition, minute, completion and endpoint identities passed. Cached graph representations reproduced the frozen GAT classifier within a maximum probability difference of 2.9103830456733704e-11. All heads have 89089 trainable parameters. Three focused causality/masking tests passed. Prior artifact hashes remain unchanged.

Shared offline history-index preparation was separately replayed and measured below. This implementation also computes diagnostic history counts and all eight historical slots, so these costs are not pure online serving latency. L4/L8 share this prepared index; L1 needs none. runtime_metrics.csv includes both cached-index inference and an additional preparation-inclusive total. Do not add shared preparation repeatedly across methods.

| partition | targets | history_index_seconds |
| --- | --- | --- |
| train | 172984 | 136.244574 |
| validation | 88782 | 4.403920 |
| test | 212591 | 36.273474 |
