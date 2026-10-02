@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Ultra-fast 1-click TS to MP4 converter wrapper
REM Supports drag-and-drop of .ts files/folders or running directly in active directory
set "SCRIPT_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%convert-media.ps1" -Path "%~1" -Preset ts2mp4
if "%~1"=="" (
    pause
)
