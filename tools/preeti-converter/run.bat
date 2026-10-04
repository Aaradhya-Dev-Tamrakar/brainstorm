@echo off
REM ═══════════════════════════════════════════════════════════════════
REM  Preeti ↔ Unicode Converter — One-click Launcher
REM  Double-click this file to launch the converter GUI.
REM ═══════════════════════════════════════════════════════════════════

title Preeti Unicode Converter
cd /d "%~dp0"

REM Check for python-docx (optional, for .docx support)
python -c "import docx" 2>nul
if errorlevel 1 (
    echo [INFO] Installing python-docx for .docx file support...
    pip install python-docx --quiet
)

echo Starting Preeti Unicode Converter...
python converter_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start. Make sure Python is installed and in PATH.
    pause
)
