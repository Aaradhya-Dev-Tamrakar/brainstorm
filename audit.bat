@echo off
REM ============================================================================
REM audit.bat - Dual-Layer Deterministic Audit & Behavioral Verification Engine
REM Enforces Layer 1 (Structural Consistency) & Layer 2 (Simulation Tests)
REM Pass --fix or -f for dynamic cross-document count auto-reconciliation
python "%~dp0sim\reconciliation_engine.py" %*
