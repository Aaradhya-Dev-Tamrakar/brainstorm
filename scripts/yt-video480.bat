@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Resolve repository root and scripts directory
set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%~dp0..\"

REM Locate yt-dlp.exe
if exist "%SCRIPT_DIR%yt-dlp.exe" (
  set "YTDLP=%SCRIPT_DIR%yt-dlp.exe"
) else if exist "%REPO_ROOT%yt-dlp.exe" (
  set "YTDLP=%REPO_ROOT%yt-dlp.exe"
) else (
  set "YTDLP=yt-dlp.exe"
)

REM Locate cookies and download archive
if exist "%REPO_ROOT%cookies.txt" (
  set "COOKIES=%REPO_ROOT%cookies.txt"
) else (
  set "COOKIES=%SCRIPT_DIR%cookies.txt"
)

if exist "%REPO_ROOT%downloads.txt" (
  set "ARCHIVE=%REPO_ROOT%downloads.txt"
) else (
  set "ARCHIVE=%SCRIPT_DIR%downloads.txt"
)

REM Ask for URL
set /p URL=Enter YouTube or YouTube Music URL: 

REM Target root folder (Videos)
set "OUTPUT_DIR=C:\Users\Aaradhya\Videos\yt-dlp"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM yt-dlp command (480p MP4)
"%YTDLP%" ^
  --cookies "%COOKIES%" ^
  --yes-playlist ^
  --download-archive "%ARCHIVE%" ^
  -f "bv*[ext=mp4][height<=480]+ba[ext=m4a]/b[ext=mp4][height<=480]" ^
  --merge-output-format mp4 ^
  --embed-metadata ^
  --embed-thumbnail ^
  -o "%OUTPUT_DIR%\%%(playlist_title|Single)s\%%(title)s.%%(ext)s" ^
  "%URL%"

echo.
echo Done.
pause
