<#
.SYNOPSIS
    Installs the single unified Windows shortcut for zero-click downloading.
#>

$ScriptDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $ScriptDir
$DownloaderScript = Join-Path $ScriptDir "clipboard-downloader.ps1"

# Resolve user's actual Desktop path (handles OneDrive or local profile Desktop)
$DesktopPath = [System.Environment]::GetFolderPath("Desktop")
if (-not (Test-Path $DesktopPath)) {
    $DesktopPath = Join-Path $env:USERPROFILE "Desktop"
}

# Clean up older separate shortcuts so only ONE unified shortcut remains
$oldShortcuts = @(
    (Join-Path $DesktopPath "Download Music (Clipboard).lnk"),
    (Join-Path $DesktopPath "Download Video (Clipboard).lnk"),
    (Join-Path (Join-Path $env:USERPROFILE "Desktop") "Download Music (Clipboard).lnk"),
    (Join-Path (Join-Path $env:USERPROFILE "Desktop") "Download Video (Clipboard).lnk")
)
foreach ($old in $oldShortcuts) {
    if (Test-Path $old) {
        Remove-Item -Path $old -Force -ErrorAction SilentlyContinue
    }
}

# Create ONE single shortcut
$WshShell = New-Object -ComObject WScript.Shell
$SingleShortcutPath = Join-Path $DesktopPath "YouTube Downloader.lnk"
$Shortcut = $WshShell.CreateShortcut($SingleShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$DownloaderScript`" -Mode prompt"
$Shortcut.IconLocation = "shell32.dll,264" # Standard system download icon
$Shortcut.Hotkey = "CTRL+ALT+D"
$Shortcut.Description = "Auto-pastes YouTube link from clipboard and lets you select Audio or Video"
$Shortcut.WorkingDirectory = $RepoRoot
$Shortcut.Save()

# Configure PowerShell $PROFILE alias 'dl'
$ProfileDir = Split-Path -Parent $PROFILE
if (-not (Test-Path $ProfileDir)) {
    New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
}

$ProfileSnippet = @"

# --- Downloader Scripts Integration ---
function dl { & "$DownloaderScript" -Mode prompt @args }
# --------------------------------------
"@

if (Test-Path $PROFILE) {
    $existing = Get-Content $PROFILE -Raw
    if ($existing -match "# --- Downloader Scripts") {
        $updated = $existing -replace '(?s)# --- Downloader Scripts.*?# --------------------------------------', $ProfileSnippet.Trim()
        $updated = $updated -replace '(?s)# --- Downloader Scripts Zero-Click Integration ---.*?# -------------------------------------------------', $ProfileSnippet.Trim()
        Set-Content -Path $PROFILE -Value $updated
    } else {
        Add-Content -Path $PROFILE -Value $ProfileSnippet
    }
} else {
    Set-Content -Path $PROFILE -Value $ProfileSnippet
}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  SINGLE UNIFIED SHORTCUT CONFIGURED" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Desktop Shortcut: $SingleShortcutPath" -ForegroundColor Yellow
Write-Host "Global Hotkey   : [Ctrl + Alt + D]" -ForegroundColor Yellow
Write-Host ""
Write-Host "Workflow:" -ForegroundColor White
Write-Host "  1. Copy any YouTube URL (Ctrl + C)"
Write-Host "  2. Hit [Ctrl + Alt + D] (or double click 'YouTube Downloader')"
Write-Host "  3. Link is auto-pasted -> Click [🎵 Audio] or [🎬 Video]"
Write-Host "==========================================================" -ForegroundColor Green
