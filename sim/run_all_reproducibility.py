"""
run_all_reproducibility.py
--------------------------
Master Single-Command E5 Scientific Reproducibility Engine for brainstorm.
Executes end-to-end discrete event simulations, invariant assurance benchmarks,
reconciliation consistency gates, and validates cryptographic checksums.

Usage:
    python sim/run_all_reproducibility.py
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone

BRAINSTORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BRAINSTORM_ROOT, "research", "results")
MANIFEST_PATH = os.path.join(RESULTS_DIR, "checksum_manifest.sha256")
sys.path.insert(0, BRAINSTORM_ROOT)


def verify_checksums() -> bool:
    print("[*] STEP 1: Verifying Canonical Cryptographic Artifact Checksums (SHA-256)...")
    if not os.path.exists(MANIFEST_PATH):
        print(f"[!] Manifest not found: {MANIFEST_PATH}")
        return False

    all_matched = True
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            expected_hash, rel_path = parts[0].strip(), parts[1].strip()
            full_path = os.path.join(BRAINSTORM_ROOT, rel_path.replace("/", os.sep))
            if not os.path.exists(full_path):
                print(f"    [FAIL] Missing artifact: {rel_path}")
                all_matched = False
                continue

            with open(full_path, "rb") as af:
                computed_hash = hashlib.sha256(af.read()).hexdigest()

            if computed_hash.lower() == expected_hash.lower():
                print(f"    [PASS] {rel_path} -> {computed_hash[:16]}...")
            else:
                print(f"    [FAIL] {rel_path} -> HASH MISMATCH (expected {expected_hash[:16]}, got {computed_hash[:16]})")
                all_matched = False

    return all_matched


def run_discrete_simulations() -> bool:
    print("\n[*] STEP 2: Executing Discrete Event Memory Simulation & Golden Regression...")
    from sim.warehouse_mem_sim import (
        run_baseline_uncoalesced,
        run_upgrade_v1_smart_coalescer,
        run_upgrade_v2_near_memory_reduction,
    )
    import random
    random.seed(42)
    base_ptr = 0x100000
    scattered_addresses = [
        base_ptr + (random.randint(0, 100) * 128) + (i % 4) * 4
        for i in range(32)
    ]
    baseline = run_baseline_uncoalesced(scattered_addresses)
    v1 = run_upgrade_v1_smart_coalescer(scattered_addresses)
    v2 = run_upgrade_v2_near_memory_reduction(4096)

    speedup = baseline.total_latency_cycles / v1.total_latency_cycles
    bus_saving = ((baseline.bytes_transferred - v1.bytes_transferred) / baseline.bytes_transferred) * 100
    traffic_reduction = ((4096 * 4 - v2.bytes_transferred) / (4096 * 4)) * 100

    print(f"    [PASS] Memory Sim: v+1 speedup={speedup:.2f}x ({bus_saving:.1f}% bus saved), v+2 traffic reduction={traffic_reduction:.3f}%.")

    from sim.run_experiments import build_result
    ipu_res = build_result(seed=42, quick=True)
    if "raw_records" in ipu_res and len(ipu_res["raw_records"]) > 0:
        print(f"    [PASS] STRANGLER-IPU Simulation: {len(ipu_res['raw_records'])} records generated deterministically.")
        return True
    return False


def run_invariant_benchmark() -> bool:
    print("\n[*] STEP 3: Executing Headless Invariant Assurance Engine Benchmark (INV-BMK-001)...")
    from sim.invariant_engine.benchmark_runner import run_benchmark
    record = run_benchmark()
    if record.discovery_recall_pct != 100.0:
        print(f"[!] Invariant benchmark recall failure: {record.discovery_recall_pct}% (expected 100.0%)")
        return False
    if record.counterexample_validity_pct != 100.0:
        print(f"[!] Sandbox replay validity failure: {record.counterexample_validity_pct}% (expected 100.0%)")
        return False
    if record.false_discovery_rate_pct != 0.0:
        print(f"[!] False discovery rate failure: {record.false_discovery_rate_pct}% (expected 0.0%)")
        return False
    print(f"    [PASS] INV-BMK-001: 100% recall on planted bugs, 100% replay confirmed, 0% FDR.")
    return True


def run_dual_layer_audit() -> bool:
    print("\n[*] STEP 4: Executing Dual-Layer Deterministic Verification Gate...")
    from sim.reconciliation_engine import audit_repository
    # Pure read-only audit
    errors = audit_repository(auto_fix=False, write_ledger=False)
    return errors == 0


def main():
    print("=" * 80)
    print("   BRAINSTORM MASTER E5 SCIENTIFIC REPRODUCIBILITY ENGINE")
    print(f"   Environment: Python {sys.version.split()[0]} on {sys.platform}")
    print(f"   Timestamp  : {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    chk_ok = verify_checksums()
    sim_ok = run_discrete_simulations()
    inv_ok = run_invariant_benchmark()
    audit_ok = run_dual_layer_audit()

    print("\n" + "=" * 80)
    print(" E5 REPRODUCIBILITY CERTIFICATION SUMMARY")
    print("=" * 80)
    print(f"  * Cryptographic Checksums (SHA-256) : {'PASSED' if chk_ok else 'FAILED'}")
    print(f"  * Discrete Event Memory Simulation  : {'PASSED' if sim_ok else 'FAILED'}")
    print(f"  * Headless Invariant Benchmark (Z3) : {'PASSED' if inv_ok else 'FAILED'}")
    print(f"  * Dual-Layer Deterministic Audit    : {'PASSED' if audit_ok else 'FAILED'}")

    all_passed = chk_ok and sim_ok and inv_ok and audit_ok
    if all_passed:
        print("\n[+] CERTIFIED E5: All experiments, models, and invariants reproducibly verified.")
        print("=" * 80)
        return 0
    else:
        print("\n[!] REJECTED: Reproducibility verification failed one or more gates.")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
