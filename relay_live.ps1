<#
.SYNOPSIS
    Real-time Live Stream Relay & Simultaneous Recorder.
    Streams a source YouTube Live broadcast directly to your private YouTube channel via RTMP
    while simultaneously saving a lossless local .mp4 copy.
.PARAMETER SourceUrl
    The source YouTube live stream URL.
.PARAMETER StreamKey
    Your private YouTube RTMP stream key (optional, will read from stream_key.txt or prompt).
#>
[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$SourceUrl,

    [Parameter(Position=1)]
    [string]$StreamKey
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = (Get-Location).Path }
Set-Location -LiteralPath $ScriptDir

# Ensure downloads folder exists
$DownloadsDir = Join-Path $ScriptDir "downloads"
if (-not (Test-Path -LiteralPath $DownloadsDir)) {
    New-Item -ItemType Directory -Path $DownloadsDir -Force | Out-Null
}

# 1. Manage Stream Key
$KeyFile = Join-Path $ScriptDir "stream_key.txt"
if ([string]::IsNullOrWhiteSpace($StreamKey) -and (Test-Path -LiteralPath $KeyFile)) {
    $StreamKey = (Get-Content -LiteralPath $KeyFile -Raw).Trim()
    Write-Host "[INFO] Loaded private stream key from stream_key.txt" -ForegroundColor Cyan
}

if ([string]::IsNullOrWhiteSpace($StreamKey)) {
    Write-Host "`n==============================================================================" -ForegroundColor Yellow
    Write-Host " YouTube Stream Key Setup (from YouTube Studio > Go Live > Stream Settings)" -ForegroundColor Yellow
    Write-Host "==============================================================================" -ForegroundColor Yellow
    $StreamKey = Read-Host "Enter your YouTube Stream Key"
    if ([string]::IsNullOrWhiteSpace($StreamKey)) {
        Write-Error "Stream key cannot be empty. Exiting."
        return
    }

    $Save = Read-Host "Save stream key to private stream_key.txt for future use? (Y/N)"
    if ($Save -eq 'Y' -or $Save -eq 'y') {
        Set-Content -LiteralPath $KeyFile -Value $StreamKey -Encoding UTF8
        Write-Host "[INFO] Stream key saved to stream_key.txt" -ForegroundColor Green
    }
}

# 2. Manage Source URL
if ([string]::IsNullOrWhiteSpace($SourceUrl)) {
    $SourceUrl = Read-Host "`nEnter Source YouTube Live Stream URL"
}

if ([string]::IsNullOrWhiteSpace($SourceUrl)) {
    Write-Error "Source URL cannot be empty. Exiting."
    return
}

# 3. Retrieve metadata for clean naming
Write-Host "`n[INFO] Fetching stream metadata..." -ForegroundColor Cyan
$BaseName = & .\yt-dlp.exe --no-playlist --windows-filenames --get-filename -o "%(channel)s - %(title)s [%(id)s]" $SourceUrl 2>$null
if ([string]::IsNullOrWhiteSpace($BaseName)) {
    $BaseName = "relay_" + (Get-Date -Format "yyyyMMdd_HHmmss")
}
# Sanitize spaces for tee muxer compatibility
$SafeBaseName = $BaseName -replace '[^\w\-\.]', '_'
$TempTs = Join-Path $DownloadsDir "$SafeBaseName.ts"
$FinalMp4 = Join-Path $DownloadsDir "$SafeBaseName.mp4"
$RtmpUrl = "rtmp://a.rtmp.youtube.com/live2/$StreamKey"

Write-Host "`n==============================================================================" -ForegroundColor Green
Write-Host " [LIVE RELAY ACTIVE]" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host " - Source Stream:   $SourceUrl"
Write-Host " - Live Target:     Your YouTube Channel (rtmp://a.rtmp.youtube.com/live2/****)"
Write-Host " - Local Output:    $FinalMp4"
Write-Host " - Video:           Direct Stream Copy (0% CPU re-encoding)"
Write-Host " - Audio:           AAC 44.1kHz 160kbps (YouTube RTMP standard)"
Write-Host "`nPress Ctrl+C in this window to stop relaying at any time.`n" -ForegroundColor Yellow

# 4. Stream and tee to RTMP and local file
$Cmd = "uvx streamlink ""$SourceUrl"" 480p,360p,best --stdout | ffmpeg -re -i - -c:v copy -tag:v 7 -c:a aac -b:a 128k -ar 44100 -f tee -map 0:v:0 -map 0:a:0 ""[f=flv]$RtmpUrl|[f=mpegts]$TempTs"""

cmd.exe /c $Cmd

# 5. Convert local TS to clean MP4
if (Test-Path -LiteralPath $TempTs) {
    Write-Host "`n[INFO] Finalizing local recording into MP4..." -ForegroundColor Cyan
    & ffmpeg -y -i $TempTs -c copy $FinalMp4 2>$null
    if (Test-Path -LiteralPath $FinalMp4) {
        Remove-Item -LiteralPath $TempTs -Force -ErrorAction SilentlyContinue
        Write-Host "[COMPLETED] Local recording saved: $FinalMp4" -ForegroundColor Green
    }
}

Write-Host "`n[DONE] Relay session closed." -ForegroundColor Green
