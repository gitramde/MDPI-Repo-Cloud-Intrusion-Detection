# Graph construction and model specification

GATv2 uses edge-aware dynamic attention: for each destination i and source j, form LeakyReLU(W_destination h_i + W_source h_j + W_edge e_ji), dot with one learned vector per head, normalize over incoming edges plus an explicit self loop, then aggregate W_source h_j. Four heads concatenate into the configured total hidden dimension (64 or 128). Two layers use ELU, dropout, residual addition and LayerNorm. Synthetic self loops have zero edge attributes. Original directed multiedges remain separate.

The implementation follows the [official GATv2 operator equations](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.GATv2Conv.html) using native PyTorch scatter operations. A dense-reference test checks numerical equivalence and gradients. No PyTorch Geometric installation is required.

The edge head concatenates [source endpoint embedding, destination endpoint embedding, current train-preprocessed flow feature vector], followed by Linear -> GELU -> Dropout -> Linear -> binary logit. Sigmoid yields malicious probability. BCEWithLogitsLoss uses training-target negative/positive weighting. AdamW uses learning rate 0.0005, weight decay 0.01 and gradient clipping at 1.0. Seed is 42 and deterministic CPU algorithms are enabled.

Node features, in order, are log1p of incoming count, outgoing count, incoming total flow bytes, outgoing total flow bytes, TCP incident count, UDP incident count, low (<1024) source-port outgoing count, and low destination-port incoming count. Flow bytes are forward plus backward bytes attributed to the directed flow's endpoints; they are not a claim about true one-way byte direction. These deterministic aggregates use no fitted vocabulary, labels, numerical IP encoding or future history. Protocol and ports come from the source-row identifier join and frozen cleaned records.

Historical edge attention features are the train-transformed subset named below; the current target retains the full eligible feature vector. Frozen feature eligibility is reused, but imputation, categories, train-value leakage checks and scaling are fitted afresh on all approved Feb-20 training rows only. Protocol unknown categories use all-zero encoding.

Historical edge features: Flow Duration, Tot Fwd Pkts, Tot Bwd Pkts, TotLen Fwd Pkts, TotLen Bwd Pkts, Dst Port, Protocol=0, Protocol=6, Protocol=17.

The precise causal cutoff, completion-time rule, cap, target sampling and history-state policies are frozen in configs/protocol.json. No snapshot crosses its calendar window or approved partition.

## Descriptive graph overview

| window_minutes | calendar_snapshots | causal_prefixes | mean_nodes | mean_edges | mean_weak_components | mean_density | mean_message_edges | capped_prefix_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 720 | 720 | 1279.434722 | 11039.925000 | 5.454167 | 0.011798 | 4445.068056 | 0.091667 |
| 5 | 144 | 720 | 2648.881944 | 55199.625000 | 2.298611 | 0.006803 | 5889.733333 | 0.615278 |
| 10 | 72 | 720 | 3668.361111 | 110399.250000 | 2.000000 | 0.005377 | 6171.743056 | 0.691667 |

Complete per-snapshot diagnostics are in graph_snapshot_diagnostics.csv; graph_diagnostics_summary.csv gives partition-specific mean, median, p90 and maximum for nodes, edges, weak/strong components, isolated nodes, repeated pairs, density and both classes. The complete-window topology is diagnostic only and is never supplied to a classifier. causal_prefix_diagnostics.csv records the actual pruned/capped model graph sizes.
