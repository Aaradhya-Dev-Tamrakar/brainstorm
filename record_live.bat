@echo off
setlocal enabledelayedexpansion
title YouTube Live Stream Recorder

cd /d "%~dp0"

:: 1. Auto-update yt-dlp nightly/stable to avoid YouTube cipher & signature blocks
echo [INFO] Checking for yt-dlp updates...
yt-dlp.exe -U --no-color
echo.

:: 2. Check if a URL was passed as an argument
set "URL=%~1"
if "%URL%"=="" (
    set /p "URL=Enter YouTube Live Stream URL: "
)

if "%URL%"=="" (
    echo [ERROR] No URL entered. Exiting.
    timeout /t 3 >nul
    exit /b 1
)

echo.
echo ==============================================================================
echo [RECORDING] Starting stream capture:
echo !URL!
echo ==============================================================================
echo  - Portable config: loaded from yt-dlp.conf
echo  - Output folder:   downloads/
echo  - Container:       MPEG-TS (safe against connection loss)
echo  - Final format:    MP4 (automatic lossless remux upon finish)
echo  - Auto-cut:        Cleanly terminates when stream ends
echo.
echo Press Ctrl+C at any time to cut and finalize early.
echo ==============================================================================
echo.

yt-dlp.exe --no-playlist "!URL!"

echo.
echo ==============================================================================
echo [COMPLETED] Stream finalized in 'downloads/' directory.
echo ==============================================================================
pause
