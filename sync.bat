@echo off
setlocal
REM ============================================================================
REM sync.bat - Zero-Friction Execution Wrapper for sync.ps1
REM Automatically bypasses PowerShell ExecutionPolicy across fresh clones/devices.
REM
REM All arguments are forwarded transparently to sync.ps1 via %%*.
REM BRL Pull Request Workflow examples:
REM   sync.bat -PR -m "feat(p2p): campus swarm marketplace" -Issue 42
REM   sync.bat -PR -m "fix(aria2): path detection" -Reviewer teammate
REM ============================================================================

where pwsh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
)
exit /b %ERRORLEVEL%
