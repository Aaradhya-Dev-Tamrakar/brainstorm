@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Zero-friction wrapper for FFmpeg Media Converter GUI / CLI
set "SCRIPT_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%convert-media.ps1" %*
