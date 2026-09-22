@echo off
setlocal EnableExtensions

REM Run PowerShell in hidden window mode to pop the UI without leaving a black terminal window open
start "" powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0scripts\clipboard-downloader.ps1" -Mode prompt
