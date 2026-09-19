# STRANGLER-IPU reproducibility package

The warehouse memory model is the canonical, zero-dependency regression for the
STRANGLER-IPU research slice. It uses a fixed random seed (`42`) and reports
the baseline, v+1 coalescer, and isolated v+2 near-memory reduction.

```powershell
python sim\warehouse_mem_sim.py --json-output sim\results\latest.json
python -m unittest sim.test_warehouse_mem_sim sim.test_reproducibility
```

`sim/results/latest.json` is generated output, not a manually transcribed
claim. The v+1 speedup is measured on the modeled workload. The v+2
`99.976%` figure is **boundary traffic reduction for the isolated reduction
channel**; it is not a whole-pipeline attention result or a hardware
measurement.

## STRANGLER-IPU pipeline runner

`run_experiments.py` is a separate, zero-dependency FIFO queueing model for
EXP-001. Reproduce the full controlled sweep from the repository root:

```powershell
python sim\run_experiments.py --reproduce-all
python -m unittest sim.test_run_experiments
```

Use `--quick` for a smoke run, `--seed N` to select the deterministic workload
seed, or `--output-dir PATH` to write elsewhere. The default artifact is
`sim/results/experiments/results.json`. It contains the conventional host,
naive partitioned, prefetch-only, and STRANGLER adaptive variants; raw records,
an overload-aware summary, and a rho sensitivity/ablation table.

The model explicitly queues each stage using
`completion=max(arrival, previous_completion)+work/capacity`. It therefore does
not treat `min(rate,bus)` as a completed transfer. Rates, payloads, DRAM,
compute, and interconnect capacities are assumptions. Results are
`HEURISTIC_HYPOTHESIS` evidence: useful for testing relationships and claims
such as ~2.26x or ~99.98%, but not hardware measurements or validation of those
figures. The canonical result hash covers only deterministic configuration and
measurements; runtime metadata (timestamp, command, and git provenance) is
retained separately for auditability.

The conventional and STRANGLER paths retain the same modeled two-pass host
memory cost; STRANGLER changes the bytes per pass to `rho * payload`. This
makes `rho=1` a valid no-reduction control rather than an unfair host-work
advantage.

The same command also generates `sim/results/experiments/REPORT.md`. The report
is derived from the JSON artifact and includes the formal FIFO model, mechanism
mapping, five-seed speedup distributions (mean, p50, p95, p99, min, max),
boundary-pressure falsification probes, and explicit model limitations. It is
an inspectability aid, not an additional evidence tier or a hardware result.
