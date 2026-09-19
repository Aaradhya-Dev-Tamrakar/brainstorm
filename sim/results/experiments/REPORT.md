# STRANGLER-IPU Experiment Report

> Evidence tier: `HEURISTIC_HYPOTHESIS`. This is a deterministic queueing
> model and not a hardware benchmark or silicon validation.

## What was tested

- Schema: `strangler-ipu-experiments.v1`; raw records: **672**.
- Sweep dimensions: ingress rate, semantic density (`rho`), and interconnect bandwidth.
- Variants: conventional, naive partitioned, prefetch-only, and STRANGLER adaptive.
- Reproduction: `python sim\run_experiments.py --reproduce-all`.
- Canonical result SHA-256: `5d931914c7bdd6de6471033be15166b2f22be13c13373440fbb372bcd4370b0e`.

## Formal model and assumptions

For each FIFO stage, completion is `C_i = max(A_i, C_(i-1)) + W_i / mu`,
where `A` is arrival time, `W` is bytes serviced, and `mu` is capacity in
decimal GB/s. Utilization is `lambda / mu`; queue delay is the observed
completion time beyond the offered arrival and service interval. STRANGLER
changes `W` at the host boundary from `payload` to `rho * payload`, while
adding an IPU service stage and fixed insertion latency.

The model omits coherence traffic, finite buffers, packetization, multiple
servers, dynamic policies, energy, silicon timing, and real workloads.

## Why the mechanism should help

When the boundary is the bottleneck, reducing host-bound bytes lowers the
boundary service demand and can reduce queue buildup. Prefetch-only is the
control for overlap without traffic reduction; naive partitioning is the
control for extra staging without semantic reduction.

## Distributional robustness

| Variant | n | Mean speedup | P50 | P95 | P99 | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| conventional | 5 | 1.000x | 1.000x | 1.000x | 1.000x | 1.000x |
| naive_partitioned | 5 | 1.205x | 1.205x | 1.205x | 1.205x | 1.205x |
| prefetch_only | 5 | 1.275x | 1.275x | 1.275x | 1.275x | 1.275x |
| strangler_adaptive | 5 | 4.172x | 4.172x | 4.173x | 4.173x | 4.171x |

The five-seed sample measures model-output variation from arrival jitter; it
is not a confidence interval for hardware or a population-level estimate.

## Falsification probes

| Probe | Speedup | Boundary reduction | Benefit collapses? |
|---|---:|---:|:---:|
| high_interconnect | 1.017x | 99.000% | yes |
| low_ingress_pressure | 1.001x | 99.000% | yes |
| tiny_working_set | 0.967x | 99.000% | yes |
| no_reduction | 0.996x | 0.000% | yes |

These probes test whether the modeled advantage weakens when the boundary is
not pressured, reduction is absent, or the working set is tiny. A failed
probe is a model diagnostic, not evidence that hardware behaves identically.

## Causal interpretation and limits

The current package supports a mechanistic hypothesis: boundary traffic
reduction is the primary modeled cause of the speedup under boundary pressure.
It does not isolate eviction, staging, and adaptive-policy effects beyond the
four variant controls above. A future ablation should expose those mechanisms
as independent switches before any stronger causal claim is made.

All figures are generated from the JSON artifact; no headline number in this
report is manually transcribed. Re-run the command above to reproduce it.
