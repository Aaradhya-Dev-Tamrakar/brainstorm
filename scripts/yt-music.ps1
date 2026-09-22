# Ensure paths resolve properly from repository root or current folder
$RepoRoot = Split-Path -Parent $PSScriptRoot

# Locate yt-dlp.exe (check scripts directory, then repo root, fallback to system PATH)
$YtDlp = "yt-dlp"
if (Test-Path (Join-Path $PSScriptRoot "yt-dlp.exe")) {
    $YtDlp = Join-Path $PSScriptRoot "yt-dlp.exe"
} elseif (Test-Path (Join-Path $RepoRoot "yt-dlp.exe")) {
    $YtDlp = Join-Path $RepoRoot "yt-dlp.exe"
}

# Locate cookies & archive
$CookiesPath = Join-Path $RepoRoot "cookies.txt"
if (-not (Test-Path $CookiesPath)) { $CookiesPath = Join-Path $PSScriptRoot "cookies.txt" }

$DownloadsPath = Join-Path $RepoRoot "downloads.txt"
if (-not (Test-Path $DownloadsPath)) { $DownloadsPath = Join-Path $PSScriptRoot "downloads.txt" }

Write-Host "Updating yt-dlp to nightly..." -ForegroundColor Cyan
& $YtDlp --update-to nightly
Write-Host ""

$URL = Read-Host "Enter YouTube or YouTube Music URL"

$MusicRoot = "C:\Users\Aaradhya\Music"
if (-not (Test-Path $MusicRoot)) {
    New-Item -ItemType Directory -Path $MusicRoot -Force | Out-Null
}

$Arguments = @(
    "--cookies", $CookiesPath,
    "--yes-playlist",
    "--download-archive", $DownloadsPath,
    "-f", "ba[ext=m4a]/ba",
    "-x",
    "--audio-format", "mp3",
    "--audio-quality", "0",
    "--embed-metadata",
    "--embed-thumbnail",
    "-o", "$MusicRoot\%(playlist_title|Single)s\%(title)s.%(ext)s",
    $URL
)

& $YtDlp @Arguments

Write-Host ""
Read-Host "Done. Press Enter to exit..."