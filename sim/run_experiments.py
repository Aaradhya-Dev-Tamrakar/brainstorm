"""Deterministic, zero-dependency STRANGLER-IPU pipeline experiments.

This is a queueing model, not a hardware benchmark.  Rates are decimal GB/s
and each stage is a single FIFO server.  A stage's completion time is
``max(arrival, previous_completion) + work/capacity``; overload therefore
creates an explicit backlog instead of being hidden by ``min(rate, bus)``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


SCHEMA_VERSION = "strangler-ipu-experiments.v1"
DEFAULT_OUTPUT_DIR = Path("sim") / "results" / "experiments"
VARIANTS = ("conventional", "naive_partitioned", "prefetch_only", "strangler_adaptive")


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 42
    payload_size_mb: float = 4.0
    ingress_gb_s: float = 100.0
    rho: float = 0.01
    interconnect_gb_s: float = 64.0
    dram_gb_s: float = 100.0
    compute_gb_s: float = 250.0
    ipu_compute_gb_s: float = 400.0
    ipu_boundary_latency_us: float = 0.8
    chunks: int = 32
    prefetch_factor: float = 1.20


def _stage(arrivals: Sequence[float], work_bytes: Sequence[float], capacity_gb_s: float) -> List[float]:
    """FIFO single-server completion times, in seconds."""
    if capacity_gb_s <= 0:
        raise ValueError("stage capacity must be positive")
    previous = 0.0
    result = []
    for arrival, work in zip(arrivals, work_bytes):
        completion = max(arrival, previous) + work / (capacity_gb_s * 1e9)
        result.append(completion)
        previous = completion
    return result


def _run_variant(cfg: ExperimentConfig, variant: str) -> Dict[str, float]:
    if variant not in VARIANTS:
        raise ValueError("unknown variant: " + variant)
    rng = random.Random(cfg.seed)
    payload = cfg.payload_size_mb * 1e6
    # Small deterministic jitter prevents a sweep from accidentally describing
    # only perfectly synchronized arrivals, while remaining reproducible.
    arrivals = [(i * payload / (cfg.ingress_gb_s * 1e9)) +
                (rng.random() - 0.5) * payload / (cfg.ingress_gb_s * 1e9) * 0.02
                for i in range(cfg.chunks)]
    arrivals = [max(0.0, x) for x in arrivals]

    if variant == "conventional":
        boundary = [payload] * cfg.chunks
        host_work = [payload * 2.0] * cfg.chunks
        transport_arrivals = _stage(arrivals, boundary, cfg.interconnect_gb_s)
        host_done = _stage(transport_arrivals, host_work, cfg.dram_gb_s)
    elif variant == "naive_partitioned":
        boundary = [payload] * cfg.chunks
        # Partitioning adds a second boundary traversal and a synchronization
        # penalty; it does not reduce bytes.
        first = _stage(arrivals, boundary, cfg.interconnect_gb_s)
        second = _stage(first, boundary, cfg.interconnect_gb_s)
        host_done = _stage(second, [payload * 1.6] * cfg.chunks, cfg.dram_gb_s)
        transport_arrivals = second
    elif variant == "prefetch_only":
        boundary = [payload] * cfg.chunks
        # Prefetch overlaps 20% of host work but leaves boundary capacity intact.
        transport_arrivals = _stage(arrivals, boundary, cfg.interconnect_gb_s)
        host_done = _stage(transport_arrivals, [payload * 1.6] * cfg.chunks,
                           cfg.dram_gb_s * cfg.prefetch_factor)
    else:
        reduced = payload * cfg.rho
        boundary = [reduced] * cfg.chunks
        ipu_done = _stage(arrivals, [payload] * cfg.chunks, cfg.ipu_compute_gb_s)
        # Boundary reduction is adaptive but cannot exceed the configured IPU
        # compute stage.  Latency is a fixed pipeline insertion, not a claim
        # about silicon.
        transport_arrivals = [x + cfg.ipu_boundary_latency_us * 1e-6 for x in
                              _stage(ipu_done, boundary, cfg.interconnect_gb_s)]
        # Reduction changes payload size, not the modeled number of host-memory
        # passes. Keeping the same two-pass cost makes rho=1 a valid control.
        host_done = _stage(transport_arrivals, [reduced * 2.0] * cfg.chunks, cfg.dram_gb_s)

    compute_work = [payload if variant != "strangler_adaptive" else payload * cfg.rho] * cfg.chunks
    compute_done = _stage(host_done, compute_work, cfg.compute_gb_s)
    end = compute_done[-1]
    span = max(payload / (cfg.ingress_gb_s * 1e9) * max(1, cfg.chunks - 1), 1e-12)
    offered_bytes = payload * cfg.chunks
    boundary_bytes = sum(boundary)
    queue_delay = max(0.0, end - (arrivals[-1] + (boundary_bytes / cfg.interconnect_gb_s / 1e9)))
    throughput = offered_bytes / max(end, 1e-12) / 1e9
    return {
        "variant": variant,
        "end_to_end_latency_us": end * 1e6,
        "boundary_bytes": boundary_bytes,
        "traffic_reduction_percent": (1.0 - boundary_bytes / offered_bytes) * 100.0,
        "throughput_gb_s": throughput,
        "queue_delay_us": queue_delay * 1e6,
        "queue_depth_indicator": max(0.0, (end - arrivals[-1]) / span),
        "transport_stall": max(0.0, end - arrivals[-1]) > span,
        "overload_ratio": cfg.ingress_gb_s / cfg.interconnect_gb_s,
    }


def run_case(cfg: ExperimentConfig) -> Dict[str, object]:
    records = [_run_variant(cfg, variant) for variant in VARIANTS]
    baseline = records[0]["end_to_end_latency_us"]
    for record in records:
        record["speedup_vs_conventional"] = baseline / record["end_to_end_latency_us"]
    return {"config": asdict(cfg), "records": records}


def _summary(records: Iterable[Dict[str, object]]) -> Dict[str, object]:
    rows = list(records)
    by_variant = {}
    for variant in VARIANTS:
        selected = [r for r in rows if r["variant"] == variant]
        by_variant[variant] = {
            "cases": len(selected),
            "median_speedup_vs_conventional": sorted(
                r["speedup_vs_conventional"] for r in selected)[len(selected) // 2],
            "max_traffic_reduction_percent": max(r["traffic_reduction_percent"] for r in selected),
            "overload_cases": sum(bool(r["transport_stall"]) for r in selected),
        }
    return {"by_variant": by_variant, "figures_are_model_outputs": True}


def _percentile(values: Sequence[float], percentile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot summarize an empty sample")
    index = (len(ordered) - 1) * percentile
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def _distribution(values: Sequence[float]) -> Dict[str, float]:
    return {
        "count": len(values),
        "mean": sum(values) / len(values),
        "min": min(values),
        "p50": _percentile(values, 0.50),
        "p95": _percentile(values, 0.95),
        "p99": _percentile(values, 0.99),
        "max": max(values),
    }


def _report_data(seed: int) -> Dict[str, object]:
    representative = ExperimentConfig(seed=seed, ingress_gb_s=200.0, rho=0.01, interconnect_gb_s=64.0)
    distribution = {}
    for variant in VARIANTS:
        values = [run_case(ExperimentConfig(seed=trial, ingress_gb_s=200.0,
                                             rho=0.01, interconnect_gb_s=64.0))["records"]
                  for trial in (42, 7, 13, 21, 99)]
        speedups = [next(row["speedup_vs_conventional"] for row in rows
                         if row["variant"] == variant) for rows in values]
        distribution[variant] = _distribution(speedups)

    falsification_configs = {
        "high_interconnect": ExperimentConfig(seed=seed, ingress_gb_s=25.0, rho=0.01,
                                              interconnect_gb_s=10000.0),
        "low_ingress_pressure": ExperimentConfig(seed=seed, ingress_gb_s=1.0, rho=0.01,
                                                 interconnect_gb_s=64.0),
        "tiny_working_set": ExperimentConfig(seed=seed, payload_size_mb=0.01, ingress_gb_s=25.0,
                                             rho=0.01, interconnect_gb_s=64.0),
        "no_reduction": ExperimentConfig(seed=seed, ingress_gb_s=200.0, rho=1.0,
                                         interconnect_gb_s=64.0),
    }
    falsification = {}
    for name, cfg in falsification_configs.items():
        rows = run_case(cfg)["records"]
        conv = next(row for row in rows if row["variant"] == "conventional")
        strangler = next(row for row in rows if row["variant"] == "strangler_adaptive")
        falsification[name] = {
            "config": asdict(cfg),
            "speedup": strangler["speedup_vs_conventional"],
            "traffic_reduction_percent": strangler["traffic_reduction_percent"],
            "benefit_collapses": strangler["speedup_vs_conventional"] <= 1.05,
            "interpretation": "falsification probe; not a claim that the mechanism must lose in all hardware",
        }
    return {
        "representative_config": asdict(representative),
        "seed_set": [42, 7, 13, 21, 99],
        "speedup_distributions": distribution,
        "falsification_probes": falsification,
        "mechanism_mapping": {
            "conventional": "baseline host movement and compute",
            "naive_partitioned": "partitioning/staging without reduction",
            "prefetch_only": "staging overlap without boundary traffic reduction",
            "strangler_adaptive": "boundary reduction plus IPU staging",
        },
    }


def _render_report(result: Dict[str, object]) -> str:
    inspect = result["inspectability"]
    lines = [
        "# STRANGLER-IPU Experiment Report",
        "",
        "> Evidence tier: `HEURISTIC_HYPOTHESIS`. This is a deterministic queueing",
        "> model and not a hardware benchmark or silicon validation.",
        "",
        "## What was tested",
        "",
        f"- Schema: `{result['schema_version']}`; raw records: **{len(result['raw_records'])}**.",
        "- Sweep dimensions: ingress rate, semantic density (`rho`), and interconnect bandwidth.",
        "- Variants: conventional, naive partitioned, prefetch-only, and STRANGLER adaptive.",
        "- Reproduction: `python sim\\run_experiments.py --reproduce-all`.",
        f"- Canonical result SHA-256: `{result['canonical_result_sha256']}`.",
        "",
        "## Formal model and assumptions",
        "",
        "For each FIFO stage, completion is `C_i = max(A_i, C_(i-1)) + W_i / mu`,",
        "where `A` is arrival time, `W` is bytes serviced, and `mu` is capacity in",
        "decimal GB/s. Utilization is `lambda / mu`; queue delay is the observed",
        "completion time beyond the offered arrival and service interval. STRANGLER",
        "changes `W` at the host boundary from `payload` to `rho * payload`, while",
        "adding an IPU service stage and fixed insertion latency.",
        "",
        "The model omits coherence traffic, finite buffers, packetization, multiple",
        "servers, dynamic policies, energy, silicon timing, and real workloads.",
        "",
        "## Why the mechanism should help",
        "",
        "When the boundary is the bottleneck, reducing host-bound bytes lowers the",
        "boundary service demand and can reduce queue buildup. Prefetch-only is the",
        "control for overlap without traffic reduction; naive partitioning is the",
        "control for extra staging without semantic reduction.",
        "",
        "## Distributional robustness",
        "",
        "| Variant | n | Mean speedup | P50 | P95 | P99 | Min | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for variant, stats in inspect["speedup_distributions"].items():
        lines.append("| {} | {} | {:.3f}x | {:.3f}x | {:.3f}x | {:.3f}x | {:.3f}x |".format(
            variant, stats["count"], stats["mean"], stats["p50"], stats["p95"],
            stats["p99"], stats["min"], stats["max"]))
    lines += [
        "",
        "The five-seed sample measures model-output variation from arrival jitter; it",
        "is not a confidence interval for hardware or a population-level estimate.",
        "",
        "## Falsification probes",
        "",
        "| Probe | Speedup | Boundary reduction | Benefit collapses? |",
        "|---|---:|---:|:---:|",
    ]
    for name, probe in inspect["falsification_probes"].items():
        lines.append("| {} | {:.3f}x | {:.3f}% | {} |".format(
            name, probe["speedup"], probe["traffic_reduction_percent"],
            "yes" if probe["benefit_collapses"] else "no"))
    lines += [
        "",
        "These probes test whether the modeled advantage weakens when the boundary is",
        "not pressured, reduction is absent, or the working set is tiny. A failed",
        "probe is a model diagnostic, not evidence that hardware behaves identically.",
        "",
        "## Causal interpretation and limits",
        "",
        "The current package supports a mechanistic hypothesis: boundary traffic",
        "reduction is the primary modeled cause of the speedup under boundary pressure.",
        "It does not isolate eviction, staging, and adaptive-policy effects beyond the",
        "four variant controls above. A future ablation should expose those mechanisms",
        "as independent switches before any stronger causal claim is made.",
        "",
        "All figures are generated from the JSON artifact; no headline number in this",
        "report is manually transcribed. Re-run the command above to reproduce it.",
        "",
    ]
    return "\n".join(lines)


def build_result(seed: int = 42, quick: bool = False) -> Dict[str, object]:
    rates = [25.0, 100.0, 500.0] if quick else [10.0, 25.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
    rhos = [0.001, 0.01, 0.1, 0.5, 1.0] if quick else [0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0]
    buses = [64.0, 128.0, 256.0]
    cases = []
    for rate in rates:
        for rho in rhos:
            for bus in buses:
                cases.append(run_case(ExperimentConfig(seed=seed, ingress_gb_s=rate,
                                                        rho=rho, interconnect_gb_s=bus)))
    raw = [record for case in cases for record in case["records"]]
    # Controlled ablation: vary rho at one fixed operating point.
    ablation = []
    for rho in (0.001, 0.01, 0.1, 0.5, 1.0):
        cfg = ExperimentConfig(seed=seed, ingress_gb_s=200.0, rho=rho, interconnect_gb_s=64.0)
        row = _run_variant(cfg, "strangler_adaptive")
        row["rho"] = rho
        ablation.append(row)
    canonical = {"cases": cases, "ablation": ablation, "seed": seed}
    canonical_json = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    result = {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        # Keep the recorded command stable across output directories. The
        # selected seed and quick/full mode are already captured in config.
        "command": "python sim/run_experiments.py --reproduce-all",
        "config": {"seed": seed, "quick": quick, "rates_gb_s": rates, "rho_values": rhos, "buses_gb_s": buses},
        "architecture_assumptions": {
            "units": "decimal GB/s, MB=1e6 bytes, latency in microseconds",
            "topology": "single FIFO server per ingress, boundary, DRAM, and compute stage",
            "arrival_process": "deterministic periodic chunks with seeded +/-1% jitter",
            "boundary_semantics": "rho is useful output bytes divided by raw input bytes",
            "prefetch_semantics": "prefetch-only raises modeled DRAM service capacity by 20%; boundary bytes unchanged",
            "strangler_semantics": "IPU consumes raw chunks, then emits rho-sized chunks across the host boundary",
        },
        "provenance": {"git_commit": _git_commit(), "model": "deterministic FIFO fluid queue; no hardware measurements"},
        "raw_records": raw,
        "summary": _summary(raw),
        "ablation": ablation,
        "limitations": [
            "Synthetic rates and capacities are assumptions, not hardware measurements.",
            "Each stage is modeled as one FIFO server; contention, coherence, and silicon effects are omitted.",
            "Traffic reduction is boundary bytes only and must not be generalized to whole-model speedup.",
        ],
        "canonical_result_sha256": hashlib.sha256(canonical_json.encode("utf-8")).hexdigest(),
        "canonical_result": canonical,
    }
    result["inspectability"] = _report_data(seed)
    return result


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL,
                                       text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reproduce-all", action="store_true", help="run the full controlled sweep")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--quick", action="store_true", help="smaller sweep for tests and smoke runs")
    args = parser.parse_args(argv)
    if not args.reproduce_all:
        parser.error("--reproduce-all is required")
    result = build_result(args.seed, args.quick)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / ("results-quick.json" if args.quick else "results.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.output_dir / ("REPORT-quick.md" if args.quick else "REPORT.md")).write_text(
        _render_report(result), encoding="utf-8"
    )
    print(f"Wrote {output} ({len(result['raw_records'])} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
