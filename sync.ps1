<#
.SYNOPSIS
    Automated Git synchronization and multi-branch ecosystem engine for brainstorm.

.DESCRIPTION
    sync.ps1 — The central synchronization hub for the brainstorm repository and its
    interconnected tool ecosystem: https://github.com/Aaradhya-Dev-Tamrakar/brainstorm

    Capabilities:
    1. Multi-Branch Operations: Safely switch, sync, or push specific tool branches
       (e.g., SPARK, super-nlm, system-optimizer, Nexus, Claude-Desktop, etc.).
    2. Ecosystem Synchronization (-AllBranches): Synchronizes and pushes all local
       tool branches to remote origin in a single command.
    3. Cross-Repo Health Check (-SyncToolRepos): Scans all local tool repos across
       F:\Aaradhya-Dev-Tamrakar and F:\AaradhyaDT to verify brainstorm branch states.
    4. New Tool Provisioning (-NewTool <name>): Automatically sets up a new tool branch
       in brainstorm, pushes it to origin, and configures the local tool repo branch.
    5. Pre-Commit Secret Scanner Guard: Prevents accidental credential/key commits.
    6. Intelligent Branch-Aware Conventional Commits: Automatically scopes commit messages
       to the active tool branch (e.g., docs(spark), feat(super-nlm), etc.).
    7. Clean Pull & Push Recovery: Pulls with --rebase --autostash and retries rejected pushes.

.PARAMETER Message
    Custom commit message (e.g. -m "docs(spark): add BLE kinematic specs").
    Alias: -m. If omitted, an intelligent conventional commit message is generated.

.PARAMETER Branch
    Target or switch to a specific tool branch to synchronize (e.g. -Branch SPARK).
    Alias: -b.

.PARAMETER AllBranches
    Synchronizes and pushes all local tool branches to remote origin.

.PARAMETER SyncToolRepos
    Audits and displays brainstorm branch states across all known tool repositories on disk.

.PARAMETER NewTool
    Provisions a new tool branch in brainstorm and sets up the matching local repo branch.

.PARAMETER CrossSync
    Audits and displays brainstorm branch states across all dynamically discovered tool repositories.

.PARAMETER CrossPull
    Performs dynamic ecosystem cross-sync and safely rebases/pulls updates for clean tool repos.

.PARAMETER Reconcile
    Executes dynamic documentation and invariant auto-reconciliation (sim\reconciliation_engine.py --fix).

.PARAMETER NoReconcile
    Bypasses the automatic reconciliation step during routine commit and push synchronization.

.PARAMETER PullOnly
    Safely pull remote updates with --rebase --autostash without committing or pushing.

.PARAMETER PushOnly
    Pushes existing local commits without creating new commits.

.PARAMETER NoPush
    Stages and commits changes locally without pushing to remote origin.

.PARAMETER WhatIf
    Dry-run mode: previews changes, secret scan, and auto-generated commit message
    without modifying git repository state.

.PARAMETER Status
    Displays repository telemetry: branch health, unpushed commits across all branches,
    and tool repository brainstorm status.

.EXAMPLE
    .\sync.ps1                               # Routine sync of active branch
    .\sync.ps1 -b SPARK                      # Switch to SPARK branch and sync
    .\sync.ps1 -AllBranches                  # Synchronize all tool branches with origin
    .\sync.ps1 -SyncToolRepos                # Audit brainstorm branch across all tool repos
    .\sync.ps1 -CrossSync                    # Audit cross-repo synchronization across tools
    .\sync.ps1 -CrossPull                    # Rebase and pull clean tool repos behind origin
    .\sync.ps1 -Reconcile                    # Reconcile docs, schemas, counts without commit
    .\sync.ps1 -NewTool "NovaVision"         # Provision a new tool branch across ecosystem
    .\sync.ps1 -m "docs: architecture notes" # Sync with custom commit message
    .\sync.ps1 -WhatIf                       # Dry-run preview
    .\sync.ps1 -Status                       # Show full ecosystem telemetry
#>

[CmdletBinding()]
param (
    [Alias("m")]
    [string]$Message,

    [Alias("b")]
    [string]$Branch,

    [switch]$AllBranches,

    [switch]$SyncToolRepos,

    [string]$NewTool,

    [switch]$PullOnly,

    [switch]$PushOnly,

    [switch]$NoPush,

    [switch]$CrossSync,

    [switch]$CrossPull,

    [switch]$Reconcile,

    [switch]$NoReconcile,

    [switch]$WhatIf,

    [switch]$Status
)

$ErrorActionPreference = "Stop"

$TargetRemoteName = "origin"
$TargetRemoteUrl  = "https://github.com/Aaradhya-Dev-Tamrakar/brainstorm.git"

function Get-EcosystemToolRepos {
    $repos = [System.Collections.Generic.List[string]]::new()

    # 1. Primary Source of Truth: schemas/ecosystem.registry.json
    $registryPath = Join-Path $PSScriptRoot "schemas\ecosystem.registry.json"
    if (Test-Path $registryPath) {
        try {
            $regData = Get-Content $registryPath -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($regData -and $regData.modules) {
                foreach ($mod in $regData.modules) {
                    if ($mod.local_path -and -not $repos.Contains($mod.local_path)) {
                        $repos.Add($mod.local_path)
                    }
                }
            }
        }
        catch {
            Write-Notice "Notice: Could not parse ecosystem.registry.json for tool paths: $_"
        }
    }

    # 2. Dynamic Filesystem Discovery across active development roots (including Suites/Utilities)
    $scanRoots = @("F:\Aaradhya-Dev-Tamrakar", "F:\AaradhyaDT", "F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite", "F:\Aaradhya-Dev-Tamrakar\Utility", "F:\Aaradhya-Dev-Tamrakar\Utility-MCPs")
    foreach ($root in $scanRoots) {
        if (Test-Path $root) {
            $dirs = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue
            foreach ($d in $dirs) {
                $gitDir = Join-Path $d.FullName ".git"
                if (Test-Path $gitDir) {
                    if (-not $repos.Contains($d.FullName)) {
                        $repos.Add($d.FullName)
                    }
                }
            }
        }
    }

    # Fallback to known default paths if empty
    if ($repos.Count -eq 0) {
        $defaults = @(
            "F:\Aaradhya-Dev-Tamrakar\super-nlm",
            "F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\Autodesk-Fusion-360-MCP-Server",
            "F:\Aaradhya-Dev-Tamrakar\system-optimizer",
            "F:\Aaradhya-Dev-Tamrakar\SPARK",
            "F:\AaradhyaDT\Nexus",
            "F:\Aaradhya-Dev-Tamrakar\Claude-Desktop",
            "F:\Aaradhya-Dev-Tamrakar\BiasAperture",
            "F:\Aaradhya-Dev-Tamrakar\Alpha-SuperApp",
            "F:\Aaradhya-Dev-Tamrakar\Utility\md2pdf-desktop",
            "F:\AaradhyaDT\AI",
            "F:\AaradhyaDT\rsvp-reading",
            "F:\Aaradhya-Dev-Tamrakar\Aaradhya-Dev-Tamrakar.github.io",
            "F:\Aaradhya-Dev-Tamrakar\AaradhyaDT.github.io",
            "F:\Aaradhya-Dev-Tamrakar\makerspace",
            "F:\AaradhyaDT\react-workshop-ieeekecktm",
            "F:\Aaradhya-Dev-Tamrakar\Utility\github-pilot",
            "F:\Aaradhya-Dev-Tamrakar\Utility\nepali-ocr-ai",
            "F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\google-classroom-mcp",
            "F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\fusion360-mcp"
        )
        foreach ($def in $defaults) { $repos.Add($def) }
    }

    return @($repos)
}


function Write-Status {
    param(
        [string]$Message,
        [System.ConsoleColor]$Color = [System.ConsoleColor]::Cyan
    )
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor $Color
}

function Write-Notice {
    param([string]$Message)
    Write-Status -Message $Message -Color ([System.ConsoleColor]::Yellow)
}

function Write-Success {
    param([string]$Message)
    Write-Status -Message $Message -Color ([System.ConsoleColor]::Green)
}

function Write-Fail {
    param([string]$Message)
    Write-Status -Message $Message -Color ([System.ConsoleColor]::Red)
}

function Ensure-RemoteConfigured {
    $existingRemotes = @(git remote)
    if ($existingRemotes -notcontains $TargetRemoteName) {
        Write-Status "Adding remote '$TargetRemoteName' ($TargetRemoteUrl)..."
        git remote add $TargetRemoteName $TargetRemoteUrl
    }
    else {
        $currentUrl = (git remote get-url $TargetRemoteName 2>$null)
        if ($currentUrl) { $currentUrl = $currentUrl.Trim() }
        $cleanCurrent = $currentUrl -replace '\.git$', ''
        $cleanTarget  = $TargetRemoteUrl -replace '\.git$', ''
        if ($cleanCurrent -ne $cleanTarget) {
            Write-Notice "Updating remote '$TargetRemoteName' URL to $TargetRemoteUrl..."
            git remote set-url $TargetRemoteName $TargetRemoteUrl
        }
    }
}

function Resolve-PythonInterpreter {
    if ($env:VIRTUAL_ENV) {
        $venvPy = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
        if (Test-Path $venvPy) { return $venvPy }
        $venvPyUnix = Join-Path $env:VIRTUAL_ENV "bin\python"
        if (Test-Path $venvPyUnix) { return $venvPyUnix }
    }
    $localVenv = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (Test-Path $localVenv) { return $localVenv }

    # Query Python launcher for concrete sys.executable path
    $pyLauncher = Get-Command "py" -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $pyPath = (& py -3 -c "import sys; print(sys.executable)" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $pyPath) {
            $cleanPath = $pyPath.Trim()
            if (Test-Path $cleanPath) {
                return $cleanPath
            }
        }
    }
    $sysPy = Get-Command "python" -ErrorAction SilentlyContinue
    if ($sysPy) {
        if ($sysPy.Source -and (Test-Path $sysPy.Source)) {
            return $sysPy.Source
        }
        return "python"
    }

    return "python3"
}

function Invoke-PythonScript {
    param(
        [string]$ScriptPath,
        [string[]]$ScriptArgs = @()
    )
    $py = Resolve-PythonInterpreter
    & $py $ScriptPath @ScriptArgs
}

function Find-StagedSecrets {
    $stagedDiff = git diff --cached -U0 2>$null
    if (-not $stagedDiff) { return @() }

    $addedLines = @($stagedDiff | Where-Object { $_ -match '^\+[^+]' } | ForEach-Object { $_.Substring(1) })
    if ($addedLines.Count -eq 0) { return @() }

    $ignoreList = @()
    $ignoreFile = Join-Path $PSScriptRoot ".syncignore-secrets"
    if (Test-Path $ignoreFile) {
        $rawLines = Get-Content $ignoreFile -Encoding UTF8 -ErrorAction SilentlyContinue
        foreach ($il in $rawLines) {
            $trimmed = $il.Trim()
            if ($trimmed -and -not $trimmed.StartsWith("#")) {
                $ignoreList += $trimmed
            }
        }
    }

    $secretPatterns = @(
        'AKIA[0-9A-Z]{16}',                                              # AWS Access Key
        'sk-[a-zA-Z0-9]{20,}',                                           # OpenAI API Key
        'sk-ant-[a-zA-Z0-9\-]{20,}',                                     # Anthropic API Key
        'ghp_[a-zA-Z0-9]{36}',                                           # GitHub Personal Token
        'github_pat_[a-zA-Z0-9_]{20,}',                                  # GitHub Fine-grained PAT
        'AIza[0-9A-Za-z\-_]{35}',                                        # Google / Gemini API Key
        'xox[baprs]-[0-9a-zA-Z\-]{10,}',                                 # Slack Token
        '-----BEGIN (RSA|EC|OPENSSH|PGP|DSA)? ?PRIVATE KEY-----',        # Private Keys
        '(?i)(api[_-]?key|secret|password|token|passwd)\s*[:=]\s*[''"][^''"\s]{8,}[''"]' # Generic Secrets
    )

    $hits = @()
    foreach ($line in $addedLines) {
        $trimmedLine = $line.Trim()
        $isIgnored = $false
        foreach ($ig in $ignoreList) {
            try {
                if ($trimmedLine -match [regex]::Escape($ig) -or ($ig -match '^\^|[\*\+\?]' -and $trimmedLine -match $ig)) {
                    $isIgnored = $true
                    break
                }
            }
            catch {
                if ($trimmedLine.Contains($ig)) {
                    $isIgnored = $true
                    break
                }
            }
        }
        if ($isIgnored) { continue }

        foreach ($pattern in $secretPatterns) {
            if ($line -match $pattern) {
                $snippet = $line.Trim()
                $hits += [PSCustomObject]@{
                    Pattern = $pattern
                    Snippet = $snippet.Substring(0, [Math]::Min(60, $snippet.Length))
                }
                break
            }
        }
    }

    return @($hits)
}

function Get-AutoCommitMessage {
    param([string]$ActiveBranch = "main")

    $statusLines = @(git status --porcelain 2>$null)
    if (-not $statusLines -or $statusLines.Count -eq 0) { return $null }

    $modifiedFiles = @()
    $addedFiles = @()
    $deletedFiles = @()
    $allChanged = @()

    foreach ($line in $statusLines) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.Length -lt 3) { continue }
        $statusCode = $line.Substring(0, 2)
        $rawPath = $line.Substring(3).Trim()

        if ($rawPath -match '->') {
            $rawPath = ($rawPath -split '->')[-1].Trim()
        }

        $cleanPath = $rawPath.Trim('"')
        $fileName = Split-Path $cleanPath -Leaf
        if ([string]::IsNullOrWhiteSpace($fileName)) { continue }

        $allChanged += $cleanPath

        if ($statusCode -match 'A|\?\?') {
            $addedFiles += $cleanPath
        }
        elseif ($statusCode -match 'D') {
            $deletedFiles += $cleanPath
        }
        else {
            $modifiedFiles += $cleanPath
        }
    }

    if ($allChanged.Count -eq 0) { return $null }

    # Scope inference: if on a dedicated tool branch, adopt that branch as scope!
    $type = "docs"
    $scope = if ($ActiveBranch -and $ActiveBranch -ne "main") { $ActiveBranch.ToLower() } else { "brainstorm" }

    $hasDocs = $false
    $hasScripts = $false
    $hasWorkflows = $false
    $hasTests = $false
    $hasCode = $false
    $hasBuild = $false

    foreach ($f in $allChanged) {
        if ($f -match '\.md$') { $hasDocs = $true }
        elseif ($f -match 'test_[^/]+\.py$' -or $f -match '\.test\.') { $hasTests = $true }
        elseif ($f -match '\.(py|ts|tsx|js|jsx|cs|kt|cpp|c|rs|go)$') { $hasCode = $true }
        elseif ($f -match '\.(bat|cmd|dockerfile|requirements\.txt|package\.json)$' -or $f -match 'build_') { $hasBuild = $true }
        elseif ($f -match '\.(ps1|sh)$') { $hasScripts = $true }
        elseif ($f -match '(\.github|\.gitignore|\.yaml|\.yml|\.json)') { $hasWorkflows = $true }
    }

    if ($hasTests -and -not $hasCode) {
        $type = "test"
    }
    elseif ($hasCode) {
        # Check if all changed code files are brand new
        $codeFiles = @($allChanged | Where-Object { $_ -match '\.(py|ts|tsx|js|jsx|cs|kt|cpp|c|rs|go)$' })
        $allNewCode = $true
        foreach ($cf in $codeFiles) {
            if ($addedFiles -notcontains $cf) { $allNewCode = $false; break }
        }
        if ($allNewCode -and $codeFiles.Count -gt 0) {
            $type = "feat"
        }
        else {
            # Check diff for fix indicators
            $diffSummary = git diff --cached 2>$null
            if ($diffSummary -match '(?i)(fix|bug|patch|error|issue)') {
                $type = "fix"
            }
            else {
                $type = "refactor"
            }
        }
    }
    elseif ($hasBuild) {
        $type = "build"
    }
    elseif ($hasScripts) {
        $type = "chore"
    }
    elseif ($hasWorkflows) {
        $type = "ci"
    }
    elseif ($hasDocs) {
        $type = "docs"
    }

    # Main branch scope refinement
    if ($ActiveBranch -eq "main") {
        if ($allChanged | Where-Object { $_ -match '^sim/' }) {
            $scope = "sim"
        }
        elseif ($allChanged | Where-Object { $_ -match '^tools/' }) {
            $scope = "tools"
        }
        elseif ($allChanged | Where-Object { $_ -match '^scripts/' }) {
            $scope = "scripts"
        }
        elseif ($allChanged | Where-Object { $_ -match '^schemas/' }) {
            $scope = "schemas"
        }
        elseif ($allChanged | Where-Object { $_ -match '^research/' }) {
            $scope = "research"
        }
        elseif ($allChanged | Where-Object { $_ -match '^\.github/' }) {
            $scope = "ci"
        }
        elseif ($hasScripts) {
            $scope = "automation"
        }
        elseif ($hasWorkflows) {
            $scope = "repo"
        }
        elseif ($hasDocs) {
            if ($allChanged | Where-Object { $_ -match 'ECOSYSTEM' }) {
                $scope = "ecosystem"
            } else {
                $scope = "notes"
            }
        }
    }

    $fileNames = @($allChanged | ForEach-Object { Split-Path $_ -Leaf })
    $summary = ""
    if ($fileNames.Count -le 2) {
        $summary = $fileNames -join ", "
    }
    else {
        $firstTwo = ($fileNames[0..1]) -join ", "
        $extraCount = $fileNames.Count - 2
        $summary = "$firstTwo +$extraCount more"
    }

    $diffStat = git diff --cached --shortstat 2>$null
    $churn = ""
    if ($diffStat -match '(\d+)\s+insertion') { $ins = $Matches[1] } else { $ins = 0 }
    if ($diffStat -match '(\d+)\s+deletion') { $del = $Matches[1] } else { $del = 0 }
    if (($ins -as [int]) -gt 0 -or ($del -as [int]) -gt 0) {
        $churn = " (+$ins/-$del)"
    }

    return "${type}(${scope}): update ${summary}${churn}"
}

function Switch-ToBranch {
    param([string]$TargetBranch)

    $current = (git branch --show-current 2>$null)
    if ($current) { $current = $current.Trim() }
    if ($current -eq $TargetBranch) { return $TargetBranch }

    Write-Status "Switching from [$current] to target branch: [$TargetBranch]..."
    $localBranches = @(git branch --format="%(refname:short)")

    if ($localBranches -contains $TargetBranch) {
        $null = & git switch $TargetBranch 2>$null
        if ($LASTEXITCODE -ne 0) {
            # Stash uncommitted changes and retry
            Write-Notice "Stashing local changes to switch branch safely..."
            $null = & git stash push -u -m "sync-branch-switch" 2>$null
            $null = & git switch $TargetBranch 2>$null
            $null = & git stash pop 2>$null
        }
    }
    else {
        # Check if it exists on origin
        $null = & git fetch origin --prune 2>$null
        $remoteBranches = @(git branch -r --format="%(refname:short)")
        if ($remoteBranches -contains "origin/$TargetBranch") {
            $null = & git switch --track "origin/$TargetBranch" 2>$null
        }
        else {
            Write-Status "Creating new local branch [$TargetBranch] from origin/main base..."
            $null = & git checkout -b $TargetBranch origin/main 2>$null
            if ($LASTEXITCODE -ne 0) {
                $null = & git checkout -b $TargetBranch 2>$null
            }
        }
    }

    return $TargetBranch
}

function Sync-AllBranches {
    Write-Status "Fetching all updates from origin..."
    git fetch origin --prune

    $branches = @(git branch --format="%(refname:short)")
    Write-Status "Synchronizing $($branches.Count) local branches with origin..." -Color ([System.ConsoleColor]::Cyan)

    $results = @()
    $active = (git branch --show-current 2>$null)
    if ($active) { $active = $active.Trim() }

    foreach ($b in $branches) {
        try {
            $aheadBehind = git rev-list --left-right --count "origin/$b...$b" 2>$null
            $ahead = 0; $behind = 0
            if ($aheadBehind) {
                $parts = $aheadBehind.Trim() -split '\s+'
                $behind = [int]$parts[0]
                $ahead  = [int]$parts[1]
            }

            $actionTaken = "In Sync"
            if ($ahead -gt 0) {
                git push origin $b 2>&1 | Out-Null
                $actionTaken = if ($LASTEXITCODE -eq 0) { "Pushed ($ahead commit(s))" } else { "Push Failed" }
            }
            elseif ($behind -gt 0) {
                if ($b -eq $active) {
                    git pull --rebase --autostash origin $b 2>&1 | Out-Null
                    $actionTaken = if ($LASTEXITCODE -eq 0) { "Rebased ($behind remote commit(s))" } else { "Pull Failed" }
                }
                else {
                    # Fast-forward non-active local branch safely without switching
                    $refSpec = "origin/$($b):$($b)"
                    $ffOut = git fetch . $refSpec 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        $actionTaken = "Fast-Forwarded ($behind commit(s))"
                    }
                    else {
                        $actionTaken = "Behind remote ($behind commit(s)) [Rebase on Switch]"
                    }
                }
            }

            $results += [PSCustomObject]@{
                Branch = $b
                Ahead  = $ahead
                Behind = $behind
                Result = $actionTaken
            }
        }
        catch {
            $results += [PSCustomObject]@{
                Branch = $b
                Ahead  = "?"
                Behind = "?"
                Result = "Error: $_"
            }
        }
    }

    Write-Host "`n========================================================" -ForegroundColor DarkCyan
    Write-Host " ALL BRANCHES SYNCHRONIZATION RESULTS" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor DarkCyan
    $results | Format-Table -AutoSize
    Write-Success "All local branches evaluated and synchronized."
}

function Audit-ToolRepositories {
    Write-Status "Auditing brainstorm branch status across dynamic ecosystem tool repos..." -Color ([System.ConsoleColor]::Cyan)
    $toolRepos = Get-EcosystemToolRepos
    $report = foreach ($dir in $toolRepos) {
        if (-not (Test-Path $dir)) {
            [PSCustomObject]@{
                Repository    = Split-Path $dir -Leaf
                ExistsOnDisk  = $false
                ActiveBranch  = "-"
                BrainstormBr  = "-"
                CleanTree     = "-"
            }
            continue
        }

        if (-not (Test-Path (Join-Path $dir ".git"))) {
            [PSCustomObject]@{
                Repository    = Split-Path $dir -Leaf
                ExistsOnDisk  = $true
                ActiveBranch  = "Non-git directory"
                BrainstormBr  = "-"
                CleanTree     = "-"
            }
            continue
        }

        $active = (git -C $dir branch --show-current 2>$null)
        $branches = @(git -C $dir branch --format="%(refname:short)" 2>$null)
        $hasBrainstorm = $branches -contains "brainstorm"
        $status = git -C $dir status --porcelain 2>$null
        $isClean = [bool](-not $status -or $status.Trim().Length -eq 0)

        [PSCustomObject]@{
            Repository    = Split-Path $dir -Leaf
            ExistsOnDisk  = $true
            ActiveBranch  = $active
            BrainstormBr  = if ($hasBrainstorm) { "Present" } else { "Missing" }
            CleanTree     = if ($isClean) { "Clean" } else { "Uncommitted Changes" }
        }
    }

    Write-Host "`n========================================================" -ForegroundColor DarkCyan
    Write-Host " ECOSYSTEM TOOL REPOSITORIES AUDIT" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor DarkCyan
    $report | Format-Table -AutoSize
}

function Invoke-CrossSync {
    [CmdletBinding()]
    param([switch]$Pull)

    Write-Status "Initiating Dynamic Ecosystem Cross-Synchronization..." -Color ([System.ConsoleColor]::Cyan)
    $toolRepos = Get-EcosystemToolRepos
    Write-Status "Discovered $($toolRepos.Count) ecosystem repositories dynamically." -Color ([System.ConsoleColor]::DarkCyan)

    $results = @()
    foreach ($dir in $toolRepos) {
        $repoName = Split-Path $dir -Leaf
        if (-not (Test-Path $dir)) {
            $results += [PSCustomObject]@{
                Repository = $repoName
                Branch     = "-"
                CleanTree  = "-"
                Ahead      = "-"
                Behind     = "-"
                SyncAction = "Missing on disk"
            }
            continue
        }

        if (-not (Test-Path (Join-Path $dir ".git"))) {
            $results += [PSCustomObject]@{
                Repository = $repoName
                Branch     = "Non-git"
                CleanTree  = "-"
                Ahead      = "-"
                Behind     = "-"
                SyncAction = "Skipped"
            }
            continue
        }

        try {
            $active = (git -C $dir branch --show-current 2>$null)
            if ($active) { $active = $active.Trim() } else { $active = "detached" }

            $status = git -C $dir status --porcelain 2>$null
            $isClean = [bool](-not $status -or $status.Trim().Length -eq 0)

            $remotes = @(git -C $dir remote 2>$null)
            $hasOrigin = $remotes -contains "origin"

            $ahead = 0; $behind = 0
            $action = "In Sync"

            if ($hasOrigin -and $active -ne "detached") {
                $null = & git -C $dir fetch origin --prune 2>$null
                $aheadBehind = git -C $dir rev-list --left-right --count "origin/$active...$active" 2>$null
                if ($aheadBehind) {
                    $parts = $aheadBehind.Trim() -split '\s+'
                    $behind = [int]$parts[0]
                    $ahead  = [int]$parts[1]
                }

                if ($ahead -gt 0) {
                    $action = "Ahead ($ahead commit(s) unpushed)"
                }
                elseif ($behind -gt 0) {
                    if ($Pull -and $isClean) {
                        $null = & git -C $dir pull --rebase --autostash origin $active 2>$null
                        $action = if ($LASTEXITCODE -eq 0) { "Rebased ($behind remote commit(s))" } else { "Pull Failed" }
                    }
                    else {
                        $action = "Behind ($behind commit(s))"
                    }
                }
                elseif (-not $isClean) {
                    $action = "Uncommitted Changes"
                }
            }
            else {
                $action = if (-not $hasOrigin) { "No Remote Origin" } else { "Detached HEAD" }
            }

            $results += [PSCustomObject]@{
                Repository = $repoName
                Branch     = $active
                CleanTree  = if ($isClean) { "Clean" } else { "Dirty" }
                Ahead      = $ahead
                Behind     = $behind
                SyncAction = $action
            }
        }
        catch {
            $results += [PSCustomObject]@{
                Repository = $repoName
                Branch     = "?"
                CleanTree  = "?"
                Ahead      = "?"
                Behind     = "?"
                SyncAction = "Error: $_"
            }
        }
    }

    Write-Host "`n================================================================================" -ForegroundColor DarkCyan
    Write-Host " DYNAMIC CROSS-ECOSYSTEM SYNCHRONIZATION STATUS" -ForegroundColor Cyan
    Write-Host "================================================================================" -ForegroundColor DarkCyan
    $results | Format-Table -AutoSize
    Write-Success "Dynamic cross-sync evaluation complete across $($toolRepos.Count) ecosystem repositories."
}

function Provision-NewTool {
    param([string]$ToolName)

    Write-Status "Provisioning new ecosystem tool branch: [$ToolName]..."
    $localBranches = @(git branch --format="%(refname:short)")

    if ($localBranches -notcontains $ToolName) {
        git fetch origin main 2>$null
        git branch $ToolName origin/main 2>$null
        if ($LASTEXITCODE -ne 0) {
            git branch $ToolName main
        }
        Write-Success "Created branch [$ToolName] in brainstorm repo from origin/main base."
    }
    else {
        Write-Notice "Branch [$ToolName] already exists in brainstorm repo."
    }

    Write-Status "Pushing branch [$ToolName] to origin..."
    git push origin $ToolName
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Branch [$ToolName] pushed to origin successfully."
    }

    # Check if a matching directory exists on disk
    $candidates = @(
        "F:\Aaradhya-Dev-Tamrakar\$ToolName",
        "F:\AaradhyaDT\$ToolName",
        "F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\$ToolName",
        "F:\Aaradhya-Dev-Tamrakar\Utility\$ToolName",
        "F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\$ToolName"
    )
    foreach ($c in $candidates) {
        if (Test-Path (Join-Path $c ".git")) {
            $toolBranches = @(git -C $c branch --format="%(refname:short)" 2>$null)
            if ($toolBranches -notcontains "brainstorm") {
                git -C $c branch brainstorm
                Write-Success "Created 'brainstorm' branch in matching tool repo: $c"
            }
        }
    }
}

function Show-RepoStatus {
    param([string]$RepoPath, [string]$Branch)

    Write-Host "`n========================================================" -ForegroundColor DarkCyan
    Write-Host " BRAINSTORM REPOSITORY STATUS" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor DarkCyan
    Write-Host "Path          : $RepoPath"
    Write-Host "Active Branch : $Branch"
    Write-Host "Remote URL    : $(git remote get-url origin 2>$null)"

    $aheadBehind = git rev-list --left-right --count "origin/$Branch...$Branch" 2>$null
    if ($aheadBehind) {
        $parts = $aheadBehind.Trim() -split '\s+'
        $behind = $parts[0]
        $ahead  = $parts[1]
        Write-Host "Active Ahead  : $ahead commit(s)" -ForegroundColor $(if ($ahead -gt 0) { [System.ConsoleColor]::Yellow } else { [System.ConsoleColor]::Green })
        Write-Host "Active Behind : $behind commit(s)" -ForegroundColor $(if ($behind -gt 0) { [System.ConsoleColor]::Red } else { [System.ConsoleColor]::Green })
    }

    $allBranches = @(git branch --format="%(refname:short)")
    Write-Host "`nTool / Ecosystem Branches ($($allBranches.Count) total):" -ForegroundColor DarkCyan
    $branchTelemetry = foreach ($b in $allBranches) {
        $ab = git rev-list --left-right --count "origin/$b...$b" 2>$null
        $a = 0; $beh = 0
        if ($ab) {
            $p = $ab.Trim() -split '\s+'
            $beh = $p[0]; $a = $p[1]
        }
        $mark = if ($b -eq $Branch) { "* active" } else { "" }
        [PSCustomObject]@{
            Branch = $b
            Ahead  = $a
            Behind = $beh
            Active = $mark
        }
    }
    $branchTelemetry | Format-Table -AutoSize

    Write-Host "Local Working Tree:" -ForegroundColor DarkCyan
    $statusOutput = git status --short
    if ($statusOutput) {
        Write-Host $statusOutput
    }
    else {
        Write-Host "  (clean, no unstaged or untracked changes)" -ForegroundColor Green
    }
    Write-Host "========================================================`n" -ForegroundColor DarkCyan
}

$RepoPath = $PSScriptRoot
if (-not (Test-Path (Join-Path $RepoPath '.git'))) {
    Write-Fail "Not inside a git repository: $RepoPath"
    exit 1
}

Push-Location $RepoPath
try {
    Ensure-RemoteConfigured

    if ($CrossSync -or $CrossPull) {
        Invoke-CrossSync -Pull:$CrossPull
        exit 0
    }

    if ($Reconcile) {
        Write-Status "Executing dynamic documentation & invariant auto-reconciliation..." -Color ([System.ConsoleColor]::Cyan)
        $reconPy = Join-Path $RepoPath "sim\reconciliation_engine.py"
        Invoke-PythonScript -ScriptPath $reconPy -ScriptArgs @("--fix")
        exit $LASTEXITCODE
    }

    if ($SyncToolRepos) {
        Audit-ToolRepositories
        exit 0
    }

    if ($NewTool) {
        Provision-NewTool -ToolName $NewTool
        exit 0
    }

    if ($AllBranches) {
        Sync-AllBranches
        exit 0
    }

    # Detect or switch target branch
    if ($Branch) {
        $currentBranch = Switch-ToBranch -TargetBranch $Branch
    }
    else {
        $currentBranch = (git branch --show-current 2>$null)
        if ($currentBranch) { $currentBranch = $currentBranch.Trim() }
        if (-not $currentBranch) { $currentBranch = "main" }
    }

    if ($Status) {
        Show-RepoStatus -RepoPath $RepoPath -Branch $currentBranch
        exit 0
    }

    Write-Status "Repository : $RepoPath"
    Write-Status "Branch     : $currentBranch"
    Write-Status "Remote URL : $TargetRemoteUrl"

    # 1. Pull latest changes
    Write-Status "Pulling latest updates from origin/$currentBranch..."
    git pull --rebase --autostash origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "git pull encountered conflicts or errors."
        exit $LASTEXITCODE
    }

    if ($PullOnly) {
        Write-Success "Pull completed successfully (-PullOnly flag active)."
        exit 0
    }

    # 2. Check uncommitted changes
    $statusPorcelain = git status --porcelain 2>$null
    $hasUncommitted = [bool]($statusPorcelain -and $statusPorcelain.Trim().Length -gt 0)

    # Check unpushed commits
    $unpushed = git rev-list "origin/$currentBranch..$currentBranch" 2>$null
    $hasUnpushed = [bool]($unpushed -and $unpushed.Trim().Length -gt 0)

    if ($PushOnly) {
        if ($hasUnpushed) {
            Write-Status "Pushing existing commits to origin/$currentBranch..."
            git push origin $currentBranch
            Write-Success "Push completed successfully."
        }
        else {
            Write-Success "No unpushed commits found. Remote is up to date."
        }
        exit 0
    }

    if (-not $hasUncommitted) {
        if ($hasUnpushed) {
            Write-Notice "No local changes to commit, but local branch is ahead of remote."
            if (-not $NoPush -and -not $WhatIf) {
                Write-Status "Pushing pending commit(s) to origin/$currentBranch..."
                git push origin $currentBranch
                Write-Success "All commits synchronized to remote origin."
            }
        }
        else {
            Write-Success "Working directory clean and synchronized with origin. Nothing to commit."
        }
        exit 0
    }

    # 3. Dry run / WhatIf inspection
    if ($WhatIf) {
        Write-Notice "[WhatIf] Changes detected on [$currentBranch]. Previewing synchronization:"
        git status --short
        git add -A
        $secretHits = Find-StagedSecrets
        if (@($secretHits).Count -gt 0) {
            Write-Fail "[WhatIf] Security Alert: Found possible secret(s) in staged changes:"
            foreach ($hit in @($secretHits)) {
                Write-Host "    Pattern: $($hit.Pattern)" -ForegroundColor Yellow
                Write-Host "    Line   : $($hit.Snippet)..." -ForegroundColor Gray
            }
        }
        $candidateMsg = if ($Message) { $Message } else { Get-AutoCommitMessage -ActiveBranch $currentBranch }
        Write-Notice "[WhatIf] Commit message: '$candidateMsg'"
        Write-Notice "[WhatIf] Push destination: origin/$currentBranch"
        git reset --quiet
        Write-Success "[WhatIf] Dry run completed. No changes committed or pushed."
        exit 0
    }

    # 3.5 Dynamic Documentation & Invariant Auto-Reconciliation Gate
    if (-not $NoReconcile -and (Test-Path (Join-Path $RepoPath "sim\reconciliation_engine.py"))) {
        Write-Status "Executing dynamic documentation & invariant auto-reconciliation..." -Color ([System.ConsoleColor]::Cyan)
        $reconPy = Join-Path $RepoPath "sim\reconciliation_engine.py"
        Invoke-PythonScript -ScriptPath $reconPy -ScriptArgs @("--fix")
        $rc = $LASTEXITCODE
        if ($rc -ne 0) {
            Write-Fail "Zero-Discrepancy Audit Gate Failed: Dynamic reconciliation reported discrepancies (exit code $rc)."
            Write-Notice "Halted sync to prevent unverified commits. Run '.\audit.bat --fix' or inspect discrepancies before committing."
            exit $rc
        }
        else {
            Write-Success "All documentation counts and invariant ledgers dynamically reconciled."
        }
    }

    # 4. Stage and verify secrets
    Write-Status "Staging changes..."
    git add -A

    $secretHits = Find-StagedSecrets
    if (@($secretHits).Count -gt 0) {
        Write-Fail "Security gate failed: Possible secret(s) detected in staged changes!"
        foreach ($hit in @($secretHits)) {
            Write-Host "    Pattern: $($hit.Pattern)" -ForegroundColor Yellow
            Write-Host "    Line   : $($hit.Snippet)..." -ForegroundColor Gray
        }
        Write-Notice "Staged files have been un-staged for safety. Please remove credentials before committing."
        git reset --quiet
        exit 1
    }

    # 5. Determine commit message
    if (-not $Message) {
        $Message = Get-AutoCommitMessage -ActiveBranch $currentBranch
        if (-not $Message) {
            $Message = "docs($currentBranch): update workspace files"
        }
        Write-Notice "Auto-generated commit message: '$Message'"
    }

    # 6. Commit changes
    Write-Status "Committing changes on [$currentBranch]..."
    git commit -m "$Message"
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "git commit failed."
        exit $LASTEXITCODE
    }

    # 7. Push to remote
    if ($NoPush) {
        Write-Success "Changes committed locally on [$currentBranch]. Push skipped (-NoPush flag active)."
        exit 0
    }

    Write-Status "Pushing to origin/$currentBranch..."
    git push origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Notice "Push was rejected (remote may have new changes). Pulling with rebase and retrying..."
        git pull --rebase --autostash origin $currentBranch
        git push origin $currentBranch
        if ($LASTEXITCODE -ne 0) {
            Write-Fail "Push failed after retry. Please inspect conflicts manually."
            exit $LASTEXITCODE
        }
    }

    Write-Success "Repository synchronized successfully with origin/$currentBranch."

    # Ecosystem Pulse
    try {
        $branches = @(git branch --format="%(refname:short)" 2>$null)
        $cleanStatus = git status --porcelain 2>$null
        $treeState = if (-not $cleanStatus -or $cleanStatus.Trim().Length -eq 0) { "Clean" } else { "Dirty" }
        Write-Host "`n[Pulse] Ecosystem Branches: $($branches.Count) | Active: [$currentBranch] | Working Tree: $treeState | Remote: origin" -ForegroundColor Green
    }
    catch {}
}
catch {
    Write-Fail "Sync error: $_"
    exit 1
}
finally {
    Pop-Location
}
