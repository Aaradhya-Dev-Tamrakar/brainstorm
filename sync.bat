@echo off
setlocal
REM ============================================================================
REM sync.bat - Zero-Friction Execution Wrapper for sync.ps1
REM Automatically bypasses PowerShell ExecutionPolicy across fresh clones/devices.
REM
REM All arguments are forwarded transparently to sync.ps1 via %%*.
REM
REM Common Usage:
REM   sync.bat                                (routine sync of active branch)
REM   sync.bat -SkipCI                        (suppress remote CI/CD with [skip ci])
REM   sync.bat -SkipCI -m "docs: notes"       (commit with [skip ci])
REM   sync.bat -WhatIf -SkipCI                (preview dry-run with CI suppression)
REM   sync.bat -PR -m "feat(p2p): campus swarm marketplace" -Issue 42
REM   sync.bat -PR -m "fix(aria2): path detection" -Reviewer teammate
REM ============================================================================

if "%~1"=="/?" goto :help
if "%~1"=="-help" goto :help
if "%~1"=="--help" goto :help
goto :run

:help
echo ============================================================================
echo sync.bat - Zero-Friction Execution Wrapper for sync.ps1
echo ============================================================================
echo Usage:
echo   sync.bat                                Routine sync of active branch
echo   sync.bat -m "commit message"            Sync with custom commit message
echo   sync.bat -SkipCI                        Suppress remote CI/CD with [skip ci]
echo   sync.bat -SkipCI -m "docs: notes"       Commit with [skip ci]
echo   sync.bat -WhatIf -SkipCI                Preview dry-run with CI suppression
echo   sync.bat -PullOnly                      Pull remote updates safely without commit
echo   sync.bat -PushOnly                      Push existing local commits
echo   sync.bat -PR -m "..." -Issue 42         BRL PR workflow with linked issue
echo   sync.bat -Status                        Display ecosystem telemetry
echo.
exit /b 0

:run
where pwsh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
)
exit /b %ERRORLEVEL%
