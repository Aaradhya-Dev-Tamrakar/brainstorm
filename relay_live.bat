@echo off
setlocal enabledelayedexpansion
title YouTube Live Relay & Stream Recorder

cd /d "%~dp0"

:: Ensure downloads directory exists
if not exist "downloads" mkdir downloads

:: 1. Read or prompt for YouTube Stream Key
set "KEY_FILE=%~dp0stream_key.txt"
set "STREAM_KEY="

if exist "%KEY_FILE%" (
    set /p STREAM_KEY=<"%KEY_FILE%"
    echo [INFO] Loaded private stream key from stream_key.txt
)

if "%STREAM_KEY%"=="" (
    echo.
    echo ==============================================================================
    echo  YouTube Stream Key Setup
    echo  (Find this in YouTube Studio ^> Go Live ^> Stream Settings)
    echo ==============================================================================
    set /p "STREAM_KEY=Enter your YouTube Stream Key: "
    if "!STREAM_KEY!"=="" (
        echo [ERROR] Stream key cannot be empty. Exiting.
        pause
        exit /b 1
    )
    set /p "SAVE_KEY=Save stream key to private stream_key.txt for future use? (Y/N): "
    if /i "!SAVE_KEY!"=="Y" (
        echo !STREAM_KEY!>"%KEY_FILE%"
        echo [INFO] Saved stream key to stream_key.txt.
    )
)

:: 2. Get Source Stream URL
echo.
set "SOURCE_URL=%~1"
if "%SOURCE_URL%"=="" (
    set /p "SOURCE_URL=Enter Source YouTube Live Stream URL: "
)

if "%SOURCE_URL%"=="" (
    echo [ERROR] No URL entered. Exiting.
    pause
    exit /b 1
)

:: 3. Fetch title for local recording filename
echo.
echo [INFO] Fetching stream metadata...
for /f "delims=" %%i in ('yt-dlp.exe --no-playlist --windows-filenames --get-filename -o "%%(channel)s - %%(title)s [%%(id)s]" "!SOURCE_URL!" 2^>nul') do (
    set "BASENAME=%%i"
)
if "%BASENAME%"=="" set "BASENAME=live_relay_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%"
set "BASENAME=%BASENAME: =_%"

set "TEMP_TS=downloads\%BASENAME%.ts"
set "FINAL_MP4=downloads\%BASENAME%.mp4"
set "RTMP_URL=rtmp://a.rtmp.youtube.com/live2/%STREAM_KEY%"

echo.
echo ==============================================================================
echo [LIVE RELAY ACTIVE]
echo  - Source Stream:   !SOURCE_URL!
echo  - Live Broadcast:  rtmp://a.rtmp.youtube.com/live2/**** (Your YouTube Channel)
echo  - Local Recording: %FINAL_MP4%
echo  - Video Mode:      Lossless Stream Copy (0%% CPU re-encoding)
echo  - Audio Mode:      Broadcast AAC (44.1kHz / 160kbps)
echo.
echo Press Ctrl+C in this window to stop relaying at any time.
echo ==============================================================================
echo.

:: 4. Stream and tee to both RTMP and local file
uvx streamlink "!SOURCE_URL!" 480p,360p,best --stdout | ffmpeg -re -i - -c:v copy -c:a aac -b:a 128k -ar 44100 -f tee -map 0:v:0 -map 0:a:0 "[f=flv]!RTMP_URL!|[f=mpegts]!TEMP_TS!"

:: 5. Post-process local file to clean MP4
if exist "!TEMP_TS!" (
    echo.
    echo [INFO] Remuxing local recording to MP4...
    ffmpeg -y -i "!TEMP_TS!" -c copy "!FINAL_MP4!" >nul 2>&1
    if exist "!FINAL_MP4!" del "!TEMP_TS!"
    echo [COMPLETED] Local recording saved as: !FINAL_MP4!
)

echo [DONE] Relay session closed.
pause
