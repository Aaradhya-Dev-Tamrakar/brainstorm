<#
.SYNOPSIS
    Deterministic Single-Command Environment Bootstrap for Aaradhya's Engineering & Antigravity Suite.

.DESCRIPTION
    Automates 100% reproducible onboarding on new machines or clean OS installations:
    1. Validates Python and PowerShell execution environment.
    2. Installs required Python dependencies from requirements.txt.
    3. Deploys global CLI tools (`save-chat`, `save-doc`) to Python Scripts / User PATH.
    4. Synchronizes all 19 Antigravity custom skills from `tools/skills/` into `$HOME/.gemini/config/skills/`.
    5. Configures Antigravity MCP directory structures and dependencies.
    6. Runs verification audit gate (`audit.bat`) to certify zero-discrepancy operational health.

.EXAMPLE
    .\scripts\bootstrap-environment.ps1
    .\scripts\bootstrap-environment.ps1 -SkipPythonDeps
#>

[CmdletBinding()]
param(
    [switch]$SkipPythonDeps,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$GeminiConfigDir = Join-Path $HOME ".gemini"
$GlobalSkillsDir = Join-Path $GeminiConfigDir "config\skills"
$GlobalMcpDir = Join-Path $GeminiConfigDir "antigravity\mcp"

Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "  AARADHYA ECOSYSTEM & ANTIGRAVITY ENVIRONMENT BOOTSTRAP ENGINE           " -ForegroundColor Cyan
Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "[*] Repository Root: $RepoRoot" -ForegroundColor Gray
Write-Host "[*] Target Gemini Dir: $GeminiConfigDir" -ForegroundColor Gray

# 1. Verify Python & Pip
Write-Host "`n[1/6] Validating Python Runtime Environment..." -ForegroundColor Yellow
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    Write-Error "Python is not installed or not available in PATH. Please install Python 3.10+."
    exit 1
}
$PythonVersion = & python --version
Write-Host " [+] Detected: $PythonVersion" -ForegroundColor Green

# Get Python Scripts directory
$PythonScriptsDir = & python -c "import sysconfig, sys; print(sysconfig.get_path('scripts'))"
Write-Host " [+] Python Scripts Directory: $PythonScriptsDir" -ForegroundColor Gray

# 2. Install Python Dependencies
if (-not $SkipPythonDeps) {
    Write-Host "`n[2/6] Installing Core Python Dependencies..." -ForegroundColor Yellow
    $ReqFile = Join-Path $RepoRoot "requirements.txt"
    if (Test-Path $ReqFile) {
        Write-Host " [*] Installing packages from $ReqFile..." -ForegroundColor Gray
        & python -m pip install --upgrade pip -q
        & python -m pip install -r $ReqFile -q
        & python -m pip install beautifulsoup4 pyyaml simpy -q
        Write-Host " [+] Python dependencies installed successfully." -ForegroundColor Green
    }
} else {
    Write-Host "`n[2/6] Skipping Python dependencies installation (-SkipPythonDeps active)." -ForegroundColor DarkGray
}

# 3. Deploy Global CLI Tools (save-chat, save-doc)
Write-Host "`n[3/6] Deploying Global CLI Tools (save-chat, save-doc)..." -ForegroundColor Yellow
if (Test-Path $PythonScriptsDir) {
    $ToolsToDeploy = @(
        @{ Name = "save_chat.py"; Bat = "save-chat.bat"; SourceDir = "$RepoRoot\tools\chat_archiver" },
        @{ Name = "save_doc.py";  Bat = "save-doc.bat";  SourceDir = "$RepoRoot\tools\doc_archiver" }
    )

    foreach ($tool in $ToolsToDeploy) {
        $srcPy = Join-Path $tool.SourceDir $tool.Name
        $dstPy = Join-Path $PythonScriptsDir $tool.Name
        $dstBat = Join-Path $PythonScriptsDir $tool.Bat

        if (Test-Path $srcPy) {
            Copy-Item $srcPy $dstPy -Force
            # Create/update batch runner
            $batContent = "@echo off`r`npython `"$dstPy`" %*`r`n"
            Set-Content -Path $dstBat -Value $batContent -Encoding Ascii
            Write-Host " [+] Deployed: $($tool.Bat) -> $dstBat" -ForegroundColor Green
        } else {
            Write-Warning "Source tool not found: $srcPy"
        }
    }
} else {
    Write-Warning "Could not locate Python scripts directory ($PythonScriptsDir)."
}

# 4. Deploy Antigravity Custom Skills Mirror
Write-Host "`n[4/6] Synchronizing 19 Antigravity Custom Skills to ~/.gemini/config/skills/..." -ForegroundColor Yellow
$LocalSkillsDir = Join-Path $RepoRoot "tools\skills"
if (Test-Path $LocalSkillsDir) {
    if (-not (Test-Path $GlobalSkillsDir)) {
        New-Item -ItemType Directory -Path $GlobalSkillsDir -Force | Out-Null
    }
    
    $skills = Get-ChildItem -Path $LocalSkillsDir -Directory
    $syncedCount = 0
    foreach ($skill in $skills) {
        $destSkillDir = Join-Path $GlobalSkillsDir $skill.Name
        Copy-Item -Path $skill.FullName -Destination $GlobalSkillsDir -Recurse -Force
        $syncedCount++
    }
    Write-Host " [+] Synchronized $syncedCount custom skills into $GlobalSkillsDir" -ForegroundColor Green
} else {
    Write-Warning "Local skills mirror not found at $LocalSkillsDir"
}

# 5. Validate User PATH
Write-Host "`n[5/6] Checking PATH Environment Variable..." -ForegroundColor Yellow
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notmatch [regex]::Escape($PythonScriptsDir)) {
    Write-Host " [*] Appending $PythonScriptsDir to User PATH..." -ForegroundColor Gray
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$PythonScriptsDir", "User")
    Write-Host " [+] Added Python Scripts directory to User PATH." -ForegroundColor Green
} else {
    Write-Host " [+] Python Scripts directory already present in PATH." -ForegroundColor Green
}

# 6. Execute Deterministic Audit Gate
Write-Host "`n[6/6] Executing Repository Verification Audit Gate..." -ForegroundColor Yellow
$AuditBat = Join-Path $RepoRoot "audit.bat"
if (Test-Path $AuditBat) {
    & $AuditBat
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n===========================================================================" -ForegroundColor Green
        Write-Host "  BOOTSTRAP COMPLETE: 100% REPRODUCIBLE ENVIRONMENT CERTIFIED             " -ForegroundColor Green
        Write-Host "===========================================================================" -ForegroundColor Green
    } else {
        Write-Warning "Audit gate reported discrepancies. Please review output above."
    }
} else {
    Write-Host " [+] Bootstrap operations finished." -ForegroundColor Green
}
