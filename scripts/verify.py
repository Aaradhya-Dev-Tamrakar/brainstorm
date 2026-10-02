#!/usr/bin/env python3
"""
scripts/verify.py - Deterministic Verification Gate for brainstorm
Executes reconciliation engine, dual-layer audits, and test suites.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main():
    print(f"Running deterministic verification in {ROOT}\n")
    
    # 1. Ecosystem manifest validation
    print("[1/3] Validating ecosystem manifest...")
    res = subprocess.run([sys.executable, "tools/validate_ecosystem.py"], cwd=str(ROOT))
    if res.returncode != 0:
        print("[FAIL] tools/validate_ecosystem.py failed.")
        return res.returncode

    # 2. Dual-layer reconciliation engine
    print("\n[2/3] Running dual-layer reconciliation engine...")
    res = subprocess.run([sys.executable, "sim/reconciliation_engine.py"], cwd=str(ROOT))
    if res.returncode != 0:
        print("[FAIL] sim/reconciliation_engine.py failed.")
        return res.returncode

    # 3. Unit test discovery
    print("\n[3/3] Running simulation regressions test suite...")
    res = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "sim", "-p", "test_*.py"], cwd=str(ROOT))
    if res.returncode != 0:
        print("[FAIL] Test suite failed.")
        return res.returncode

    print("\n" + "=" * 50)
    print("ALL BRAINSTORM CHECKS PASSED DETERMINISTICALLY.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
