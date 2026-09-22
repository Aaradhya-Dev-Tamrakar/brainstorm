param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("mp3", "720p")]
    [string]$Mode,

    [Parameter(Mandatory=$true)]
    [string]$Url
)

# Output directory configuration
$MusicRoot = "C:\Users\Aaradhya\Music"
$VideoRoot = "C:\Users\Aaradhya\Videos\yt-dlp"

if ($Mode -eq "mp3") {
    $OutputDir = $MusicRoot
} else {
    $OutputDir = $VideoRoot
}

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$RepoRoot = Split-Path -Parent $PSScriptRoot

# Locate yt-dlp.exe (check scripts directory, then repo root, fallback to system PATH)
$YtDlp = "yt-dlp"
if (Test-Path (Join-Path $PSScriptRoot "yt-dlp.exe")) {
    $YtDlp = Join-Path $PSScriptRoot "yt-dlp.exe"
} elseif (Test-Path (Join-Path $RepoRoot "yt-dlp.exe")) {
    $YtDlp = Join-Path $RepoRoot "yt-dlp.exe"
}

# Locate cookies
$Cookies = Join-Path $RepoRoot "cookies.txt"
if (-not (Test-Path $Cookies)) { $Cookies = Join-Path $PSScriptRoot "cookies.txt" }

$Output = "$OutputDir\%(title)s.%(ext)s"

if ($Mode -eq "mp3") {
    & $YtDlp `
        --cookies $Cookies `
        -x `
        --audio-format mp3 `
        --audio-quality 0 `
        -o $Output `
        $Url
}
elseif ($Mode -eq "720p") {
    & $YtDlp `
        --cookies $Cookies `
        -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" `
        --merge-output-format mp4 `
        -o $Output `
        $Url
}
