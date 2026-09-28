@echo off
setlocal
REM ============================================================================
REM graphify.bat - Zero-Friction Execution Wrapper for graphify.ps1
REM Automatically bypasses PowerShell ExecutionPolicy across fresh clones/devices.
REM ============================================================================

where pwsh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0graphify.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0graphify.ps1" %*
)
exit /b %ERRORLEVEL%
