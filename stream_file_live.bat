@echo off
setlocal enabledelayedexpansion
title YouTube Live File Streamer

cd /d "%~dp0"

:: 1. Read Stream Key
set "KEY_FILE=%~dp0stream_key.txt"
set "STREAM_KEY="

if exist "%KEY_FILE%" (
    set /p STREAM_KEY=<"%KEY_FILE%"
)

if "%STREAM_KEY%"=="" (
    echo [ERROR] stream_key.txt not found or empty.
    set /p "STREAM_KEY=Enter your YouTube Stream Key: "
    if "!STREAM_KEY!"=="" exit /b 1
    echo !STREAM_KEY!>"%KEY_FILE%"
)

:: 2. Get Video File to Stream
set "VIDEO_FILE=%~1"

if "%VIDEO_FILE%"=="" (
    echo.
    echo ==============================================================================
    echo  YouTube Live Video Broadcaster
    echo ==============================================================================
    echo  Stream Key:  Loaded from stream_key.txt
    echo  RTMP Ingest: rtmp://a.rtmp.youtube.com/live2/****
    echo.
    echo Searching downloads/ folder for video files...
    echo.
    set /a count=0
    for /r "downloads" %%f in (*.mp4 *.mkv *.ts) do (
        set /a count+=1
        set "file_!count!=%%f"
        echo  [!count!] %%~nxf
    )
    echo.
    if !count! GTR 0 (
        set /p "choice=Enter number to stream [1-!count!] (or type full path): "
        for %%i in (!choice!) do (
            if defined file_%%i set "VIDEO_FILE=!file_%%i!"
        )
    )
    if "!VIDEO_FILE!"=="" (
        set /p "VIDEO_FILE=Drag and drop or enter video file path: "
    )
)

:: Remove quotes around path
set "VIDEO_FILE=%VIDEO_FILE:"=%"

if not exist "%VIDEO_FILE%" (
    echo [ERROR] File not found: "%VIDEO_FILE%"
    pause
    exit /b 1
)

echo.
echo ==============================================================================
echo [BROADCASTING LIVE]
echo  - File:        "%VIDEO_FILE%"
echo  - Target:      Your YouTube Channel
echo  - Status:      Sending video stream to YouTube Studio...
echo.
echo Check your YouTube Studio tab - it will turn GREEN with "Excellent Connection"!
echo Press Ctrl+C at any time to stop the broadcast.
echo ==============================================================================
echo.

ffmpeg -re -i "%VIDEO_FILE%" -c:v copy -c:a aac -b:a 160k -ar 44100 -f flv "rtmp://a.rtmp.youtube.com/live2/%STREAM_KEY%"

echo.
echo [DONE] Broadcast ended.
pause
