#!/usr/bin/env bash
# ============================================================================
# sim.sh - Warehouse logistics GPU-DRAM channel simulator shortcut
# Compatible with Linux, macOS, and WSL environments.
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[-] Error: Python is not installed or not in PATH." >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/sim/warehouse_mem_sim.py" "$@"
