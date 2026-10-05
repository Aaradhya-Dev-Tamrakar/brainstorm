<#
.SYNOPSIS
  Automated, lightweight BitTorrent dataset seeder using aria2c.
.DESCRIPTION
  Launches a background or interactive seeding process for datasets packaged
  via make_dataset_torrent.py. Configures DHT, Local Peer Discovery (LPD),
  and Peer Exchange (PEX) for maximum swarm throughput.
.PARAMETER Torrent
  Path to the .torrent file or Magnet URI.
.PARAMETER DataDir
  Directory containing the completed dataset files to seed.
  Defaults to the parent directory of the .torrent file.
.PARAMETER Port
  Incoming TCP/UDP peer port (default: 6881).
.PARAMETER MaxUploadSpeed
  Optional upload rate limit, e.g. "5M", "15M" (default: "0" = unlimited).
.PARAMETER InstallAria2
  Automatically installs aria2 via winget if missing from PATH.
.EXAMPLE
  .\scripts\seed_dataset.ps1 -Torrent "F:\Datasets\sensor_benchmark.torrent"
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Torrent,

    [Parameter(Position = 1)]
    [string]$DataDir = "",

    [int]$Port = 6881,

    [string]$MaxUploadSpeed = "0",

    [switch]$InstallAria2
)

# 1. Resolve aria2c executable
$aria2Cmd = Get-Command "aria2c" -ErrorAction SilentlyContinue

if (-not $aria2Cmd) {
    # Refresh PATH from registry in case winget just modified it
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machinePath;$userPath"
    $aria2Cmd = Get-Command "aria2c" -ErrorAction SilentlyContinue
}

if (-not $aria2Cmd) {
    # Check common winget install locations as secondary fallback
    $wingetMatches = Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "aria2c.exe" -Recurse -ErrorAction SilentlyContinue
    if ($wingetMatches) {
        $aria2Path = $wingetMatches[0].FullName
    } else {
        Write-Host "[!] aria2c was not found in PATH." -ForegroundColor Yellow
        if ($InstallAria2) {
            Write-Host "[+] Installing aria2 via winget..." -ForegroundColor Cyan
            winget install --id aria2.aria2 -e --accept-source-agreements --accept-package-agreements --silent
            $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
            $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
            $env:Path = "$machinePath;$userPath"
            $aria2Cmd = Get-Command "aria2c" -ErrorAction SilentlyContinue
            if ($aria2Cmd) {
                $aria2Path = $aria2Cmd.Source
            } else {
                Write-Error "aria2 installation finished, but executable not yet in PATH. Please restart terminal."
                exit 1
            }
        } else {
            Write-Host "    To install aria2 automatically, run this script with -InstallAria2 or run:" -ForegroundColor Gray
            Write-Host "    winget install aria2.aria2" -ForegroundColor Green
            exit 1
        }
    }
} else {
    $aria2Path = $aria2Cmd.Source
}

# 2. Validate torrent path and data directory
if ($Torrent.StartsWith("magnet:?", [System.StringComparison]::OrdinalIgnoreCase)) {
    if ([string]::IsNullOrWhiteSpace($DataDir)) {
        Write-Error "When seeding a Magnet URI, -DataDir must be specified."
        exit 1
    }
    $resolvedTorrent = $Torrent
} else {
    if (-not (Test-Path $Torrent)) {
        Write-Error "Torrent file does not exist: $Torrent"
        exit 1
    }
    $resolvedTorrent = (Resolve-Path $Torrent).Path
    if ([string]::IsNullOrWhiteSpace($DataDir)) {
        $DataDir = Split-Path -Parent $resolvedTorrent
    }
}

if (-not (Test-Path $DataDir)) {
    Write-Error "Data directory does not exist: $DataDir"
    exit 1
}
$resolvedDataDir = (Resolve-Path $DataDir).Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    AARADHYA DATASET SEEDER (aria2c engine)                 " -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Target Torrent : $resolvedTorrent" -ForegroundColor Gray
Write-Host " Storage Root   : $resolvedDataDir" -ForegroundColor Gray
Write-Host " P2P Port       : $Port (TCP/UDP)" -ForegroundColor Gray
Write-Host " Upload Cap     : $(if ($MaxUploadSpeed -eq '0') { 'Unlimited' } else { $MaxUploadSpeed })" -ForegroundColor Gray
Write-Host " Features       : DHT, PEX, LPD (Local Discovery) Active" -ForegroundColor Gray
Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " Press [Ctrl + C] at any time to gracefully halt seeding." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$ariaArgs = @(
    "--dir=$resolvedDataDir",
    "--enable-dht=true",
    "--dht-listen-port=$Port",
    "--listen-port=$Port",
    "--enable-peer-exchange=true",
    "--bt-enable-lpd=true",
    "--bt-seed-unverified=true",
    "--seed-ratio=0.0",
    "--summary-interval=5",
    "--bt-max-peers=100",
    "--max-upload-limit=$MaxUploadSpeed",
    "--file-allocation=none"
)

if ($resolvedTorrent.StartsWith("magnet:?", [System.StringComparison]::OrdinalIgnoreCase)) {
    $ariaArgs += "--bt-metadata-only=false"
    $ariaArgs += "$resolvedTorrent"
} else {
    $ariaArgs += "$resolvedTorrent"
}

& "$aria2Path" @ariaArgs
