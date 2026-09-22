@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM brainstorm.bat - Unified Ecosystem CLI & Automation Dispatcher
REM Central command center for the brainstorm repository and research engine.
REM ============================================================================

set "ACTION=%~1"

if "%ACTION%"=="" goto help
if /i "%ACTION%"=="help" goto help
if /i "%ACTION%"=="--help" goto help
if /i "%ACTION%"=="-h" goto help

set "REST_ARGS="
for /f "tokens=1,* delims= " %%a in ("%*") do set "REST_ARGS=%%b"

if /i "%ACTION%"=="audit" goto cmd_audit
if /i "%ACTION%"=="verify" goto cmd_audit
if /i "%ACTION%"=="sim" goto cmd_sim
if /i "%ACTION%"=="scorecard" goto cmd_scorecard
if /i "%ACTION%"=="telemetry" goto cmd_telemetry
if /i "%ACTION%"=="report" goto cmd_report
if /i "%ACTION%"=="archive" goto cmd_archive
if /i "%ACTION%"=="validate" goto cmd_validate
if /i "%ACTION%"=="sweep" goto cmd_sweep
if /i "%ACTION%"=="experiments" goto cmd_experiments
if /i "%ACTION%"=="sync" goto cmd_sync
if /i "%ACTION%"=="status" goto cmd_status

echo [!] Unknown command: "%ACTION%"
echo Type "brainstorm help" for a list of available commands.
exit /b 1

:cmd_audit
python "%~dp0sim\reconciliation_engine.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_sim
python "%~dp0sim\warehouse_mem_sim.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_scorecard
python "%~dp0sim\task_telemetry.py" scorecard %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_telemetry
python "%~dp0sim\task_telemetry.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_report
call "%~dp0build_report.bat"
exit /b %ERRORLEVEL%

:cmd_archive
if "%REST_ARGS%"=="" (
    python "%~dp0sim\transcript_archiver.py" --auto
) else (
    python "%~dp0sim\transcript_archiver.py" %REST_ARGS%
)
exit /b %ERRORLEVEL%

:cmd_validate
python "%~dp0tools\validate_ecosystem.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_sweep
python "%~dp0sim\sweep_ipu_breakeven.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_experiments
python "%~dp0sim\run_experiments.py" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_sync
powershell.exe -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %REST_ARGS%
exit /b %ERRORLEVEL%

:cmd_status
powershell.exe -ExecutionPolicy Bypass -File "%~dp0sync.ps1" -Status
exit /b %ERRORLEVEL%

:help
echo ============================================================================
echo   BRAINSTORM UNIFIED CLI DISPATCHER
echo ============================================================================
echo Usage: brainstorm ^<command^> [options]
echo.
echo Verification ^& Auditing:
echo   audit [--fix]          Dual-layer deterministic audit (reconciliation engine)
echo   validate               Validate ecosystem verification manifest schema
echo   scorecard              Display continuous task telemetry ^& workflow scorecard
echo   telemetry ^<action^>     Run or log task telemetry commands
echo.
echo Simulation ^& Research:
echo   sim                    Run warehouse memory GPU-DRAM queue simulation
echo   sweep                  Run IPU breakeven parameter sweep
echo   experiments            Run benchmark experiments suite
echo   report                 Compile LaTeX research dossier into report/main.pdf
echo   archive [codename]     Archive session transcripts per INV-EPI-001
echo.
echo Ecosystem Synchronization:
echo   status                 Display full multi-branch ecosystem status
echo   sync [options]         Synchronize repository via sync.ps1
echo   help                   Show this help message
echo ============================================================================
exit /b 0
