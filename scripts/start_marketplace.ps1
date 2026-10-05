<#
.SYNOPSIS
  Launches the Brainstorm & Campus Swarm Marketplace local and LAN server.
.DESCRIPTION
  Hosts tools/swarm_marketplace on port 8080, automatically detects local Wi-Fi /
  Ethernet IP addresses for campus sharing, and prints the Cohort Pro access credentials.
.PARAMETER Port
  HTTP server port (default: 8080).
.PARAMETER NoBrowser
  Prevents automatic browser opening.
.EXAMPLE
  .\scripts\start_marketplace.ps1
#>

[CmdletBinding()]
param (
    [int]$Port = 8080,
    [switch]$NoBrowser
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$marketplaceDir = Join-Path $rootDir "tools\swarm_marketplace"

if (-not (Test-Path $marketplaceDir)) {
    Write-Error "Marketplace directory not found at: $marketplaceDir"
    exit 1
}

# Resolve Local IPv4 Address
$lanIps = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | 
    Where-Object { $_.InterfaceAlias -notmatch "Loopback|vEthernet|Virtual" -and $_.IPAddress -notlike "169.254*" } | 
    Select-Object -ExpandProperty IPAddress

$primaryLanIp = if ($lanIps) { $lanIps[0] } else { "127.0.0.1" }

$localUrl = "http://localhost:$Port"
$lanUrl = "http://${primaryLanIp}:$Port"
$proUrl = "http://${primaryLanIp}:${Port}/?role=cohort-pro-2026"

Clear-Host
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "     BRAINSTORM & CAMPUS SWARM MARKETPLACE (IOE Pulchowk)         " -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " Serving Directory : $marketplaceDir" -ForegroundColor Gray
Write-Host " Local Access      : $localUrl" -ForegroundColor Green
Write-Host " Campus / LAN URL  : $lanUrl" -ForegroundColor Yellow
Write-Host " Cohort Pro Access : $proUrl" -ForegroundColor Cyan
Write-Host " Cohort Passkey    : cohort-pro-2026" -ForegroundColor Magenta
Write-Host "------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " [!] Classmates on the same Wi-Fi can visit: $lanUrl" -ForegroundColor Gray
Write-Host " [*] Press [Ctrl + C] in this window to stop the server." -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $NoBrowser) {
    Start-Process $localUrl
}

# Launch Python HTTP Server
Set-Location -Path $marketplaceDir
python -m http.server $Port --bind 0.0.0.0
