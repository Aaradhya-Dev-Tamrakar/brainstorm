@echo off
REM ============================================================================
REM scorecard.bat - Workflow Telemetry & Performance Scorecard Dashboard
REM Displays Human Intervention Ratio (HIR), Token Volume, Dispatches & Rework
REM ============================================================================
python "%~dp0sim\task_telemetry.py" scorecard
