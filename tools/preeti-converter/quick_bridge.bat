@echo off
REM ═══════════════════════════════════════════════════════════════════
REM  Preeti Quick Bridge — Background Companion Launcher
REM  Global Hotkey (Ctrl+Alt+P) & Floating Mini-Widget (Ctrl+Alt+M)
REM ═══════════════════════════════════════════════════════════════════

title Preeti Quick Bridge
cd /d "%~dp0"

REM Check recommended dependencies (keyboard, pystray, pillow)
python -c "import keyboard, pystray, PIL" 2>nul
if errorlevel 1 (
    echo [INFO] Installing recommended dependencies (keyboard, pystray, pillow)...
    pip install keyboard pystray pillow --quiet
)

echo Starting Preeti Quick Bridge Companion...
echo   * Ctrl+Alt+P : Convert clipboard text (Unicode Devanagari to Preeti)
echo   * Ctrl+Alt+M : Toggle floating mini-widget
echo.

REM Launch in background without console window using pythonw
start "" pythonw quick_bridge.py

if errorlevel 1 (
    echo [Fallback] Starting in console mode...
    python quick_bridge.py
)
