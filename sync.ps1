<#
.SYNOPSIS
    Automated Git synchronization engine for the brainstorm repository.

.DESCRIPTION
    sync.ps1 — Safely synchronizes the local brainstorm repository with remote origin:
    https://github.com/Aaradhya-Dev-Tamrakar/brainstorm

    Workflow:
    1. Validates git repository environment and remote configuration.
    2. Pulls remote updates cleanly with --rebase --autostash.
    3. Scans staged changes for accidental credential or API key leaks.
    4. Auto-generates intelligent conventional commit messages if -Message is omitted.
    5. Stages local modifications, commits, and pushes to origin.
    6. Automatically retries with rebase if remote is ahead during push.

.PARAMETER Message
    Custom commit message (e.g. -m "docs: add sensory agent design").
    Alias: -m. If omitted, an intelligent conventional commit message is generated.

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
    Displays repository status, branch health, unpushed commits, and remote configuration.

.EXAMPLE
    .\sync.ps1                               # Routine sync: pull, stage, auto-commit & push
    .\sync.ps1 -m "docs: architecture notes" # Sync with custom commit message
    .\sync.ps1 -PullOnly                     # Pull latest changes only
    .\sync.ps1 -PushOnly                     # Push pending commits
    .\sync.ps1 -NoPush                       # Commit locally without pushing
    .\sync.ps1 -WhatIf                       # Dry-run preview of sync actions
    .\sync.ps1 -Status                       # Show repository telemetry
#>

[CmdletBinding()]
param (
    [Alias("m")]
    [string]$Message,

    [switch]$PullOnly,

    [switch]$PushOnly,

    [switch]$NoPush,

    [switch]$WhatIf,

    [switch]$Status
)

$ErrorActionPreference = "Stop"

$TargetRemoteName = "origin"
$TargetRemoteUrl  = "https://github.com/Aaradhya-Dev-Tamrakar/brainstorm.git"

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
        # If url doesn't match target base (ignoring trailing .git), update it
        $cleanCurrent = $currentUrl -replace '\.git$', ''
        $cleanTarget  = $TargetRemoteUrl -replace '\.git$', ''
        if ($cleanCurrent -ne $cleanTarget) {
            Write-Notice "Updating remote '$TargetRemoteName' URL to $TargetRemoteUrl..."
            git remote set-url $TargetRemoteName $TargetRemoteUrl
        }
    }
}

function Find-StagedSecrets {
    $stagedDiff = git diff --cached -U0 2>$null
    if (-not $stagedDiff) { return @() }

    $addedLines = $stagedDiff | Where-Object { $_ -match '^\+[^+]' } | ForEach-Object { $_.Substring(1) }
    if (-not $addedLines) { return @() }

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

        # Handle renamed files: "R  old -> new"
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

    # Determine conventional commit type & scope
    $type = "docs"
    $scope = "brainstorm"

    $hasDocs = $false
    $hasScripts = $false
    $hasWorkflows = $false

    foreach ($f in $allChanged) {
        if ($f -match '\.md$') { $hasDocs = $true }
        elseif ($f -match '\.(ps1|sh|bat|cmd)$') { $hasScripts = $true }
        elseif ($f -match '(\.github|\.gitignore|\.yaml|\.yml|\.json)') { $hasWorkflows = $true }
    }

    if ($hasScripts) {
        $type = "chore"
        $scope = "automation"
    }
    elseif ($hasWorkflows) {
        $type = "ci"
        $scope = "repo"
    }
    elseif ($hasDocs) {
        $type = "docs"
        if ($allChanged | Where-Object { $_ -match 'ECOSYSTEM' }) {
            $scope = "ecosystem"
        } else {
            $scope = "notes"
        }
    }

    # Generate summary list
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

    # Extract diff churn stats
    $diffStat = git diff --cached --shortstat 2>$null
    $churn = ""
    if ($diffStat -match '(\d+)\s+insertion') { $ins = $Matches[1] } else { $ins = 0 }
    if ($diffStat -match '(\d+)\s+deletion') { $del = $Matches[1] } else { $del = 0 }
    if (($ins -as [int]) -gt 0 -or ($del -as [int]) -gt 0) {
        $churn = " (+$ins/-$del)"
    }

    return "${type}(${scope}): update ${summary}${churn}"
}

function Show-RepoStatus {
    param([string]$RepoPath, [string]$Branch)

    Write-Host "`n========================================================" -ForegroundColor DarkCyan
    Write-Host " BRAINSTORM REPOSITORY STATUS" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor DarkCyan
    Write-Host "Path      : $RepoPath"
    Write-Host "Branch    : $Branch"
    Write-Host "Remote    : $(git remote get-url origin 2>$null)"

    $aheadBehind = git rev-list --left-right --count "origin/$Branch...$Branch" 2>$null
    if ($aheadBehind) {
        $parts = $aheadBehind.Trim() -split '\s+'
        $behind = $parts[0]
        $ahead = $parts[1]
        Write-Host "Ahead     : $ahead commit(s)" -ForegroundColor $(if ($ahead -gt 0) { [System.ConsoleColor]::Yellow } else { [System.ConsoleColor]::Green })
        Write-Host "Behind    : $behind commit(s)" -ForegroundColor $(if ($behind -gt 0) { [System.ConsoleColor]::Red } else { [System.ConsoleColor]::Green })
    }

    Write-Host "`nLocal Working Tree:" -ForegroundColor DarkCyan
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
    # Detect current branch
    $currentBranch = (git branch --show-current 2>$null)
    if ($currentBranch) { $currentBranch = $currentBranch.Trim() }
    if (-not $currentBranch) { $currentBranch = "main" }

    Ensure-RemoteConfigured

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
        Write-Notice "[WhatIf] Changes detected. Previewing synchronization:"
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
        $candidateMsg = if ($Message) { $Message } else { Get-AutoCommitMessage }
        Write-Notice "[WhatIf] Commit message: '$candidateMsg'"
        Write-Notice "[WhatIf] Push destination: origin/$currentBranch"
        git reset --quiet
        Write-Success "[WhatIf] Dry run completed. No changes committed or pushed."
        exit 0
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
        $Message = Get-AutoCommitMessage
        if (-not $Message) {
            $Message = "docs(brainstorm): update workspace files"
        }
        Write-Notice "Auto-generated commit message: '$Message'"
    }

    # 6. Commit changes
    Write-Status "Committing changes..."
    git commit -m "$Message"
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "git commit failed."
        exit $LASTEXITCODE
    }

    # 7. Push to remote
    if ($NoPush) {
        Write-Success "Changes committed locally. Push skipped (-NoPush flag active)."
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
}
catch {
    Write-Fail "Sync error: $_"
    exit 1
}
finally {
    Pop-Location
}
