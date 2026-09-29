#!/usr/bin/env bash
# ============================================================================
# audit.sh - Dual-Layer Deterministic Audit & Behavioral Verification Engine
# Enforces Layer 1 (Structural Consistency) & Layer 2 (Simulation Tests)
# Pass --fix or -f for dynamic cross-document count auto-reconciliation
# Compatible with Linux, macOS, and WSL environments.
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve Python interpreter (python3 preferred on Unix)
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[-] Error: Python is not installed or not in PATH. Please install Python 3.10+." >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/sim/reconciliation_engine.py" "$@"
