<#
.SYNOPSIS
    High-efficiency, resilient YouTube Live Stream Recorder with auto-cut and lossless MP4 remuxing.
.PARAMETER Url
    YouTube live stream URL (video or /live channel link).
#>
[CmdletBinding()]
param(
    [Parameter(Position=0, ValueFromPipeline=$true)]
    [string]$Url
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = (Get-Location).Path }
Set-Location -LiteralPath $ScriptDir

$YtDlp = Join-Path $ScriptDir "yt-dlp.exe"
if (-not (Test-Path -LiteralPath $YtDlp)) {
    $YtDlp = "yt-dlp"
}

# 1. Automatic update check to stay ahead of YouTube player JS/signature changes
Write-Host "[INFO] Checking for yt-dlp updates..." -ForegroundColor Cyan
try {
    & $YtDlp -U --no-color
} catch {
    Write-Warning "Update check skipped or failed: $_"
}

# 2. Prompt for URL if not provided
if ([string]::IsNullOrWhiteSpace($Url)) {
    $Url = Read-Host "`nEnter YouTube Live Stream URL"
}

if ([string]::IsNullOrWhiteSpace($Url)) {
    Write-Error "No URL provided. Exiting."
    return
}

Write-Host "`n==============================================================================" -ForegroundColor Green
Write-Host " [RECORDING] Starting stream capture: $Url" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host " - Engine config: Loaded from yt-dlp.conf" -ForegroundColor DarkGray
Write-Host " - Directory:     ./downloads/<Channel>/<Date> - <Title> [<Id>].mp4" -ForegroundColor DarkGray
Write-Host " - Safety:        Continuous MPEG-TS container (prevents corruption on drops)" -ForegroundColor DarkGray
Write-Host " - Auto-Cut:      Terminates cleanly when stream finishes without hanging" -ForegroundColor DarkGray
Write-Host " - Post-Process:  Lossless FFmpeg stream copy to MP4 (zero CPU re-encoding)" -ForegroundColor DarkGray
Write-Host "`nPress Ctrl+C at any time to cut and finalize early.`n" -ForegroundColor Yellow

# 3. Execute recording (yt-dlp.conf handles arguments & cookies)
& $YtDlp --no-playlist $Url

Write-Host "`n==============================================================================" -ForegroundColor Green
Write-Host " [COMPLETED] Stream finalized in 'downloads/' folder." -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
