<#
.SYNOPSIS
    Automated Graphify knowledge graph engine and stale cleaner for brainstorm.

.DESCRIPTION
    graphify.ps1 — Manages, thoroughly updates, and maintains the Graphify knowledge graph
    for the repository while automatically pruning stale snapshots and temporary build artifacts.

    Capabilities:
    1. Stale Artifact Elimination: Automatically detects and removes dated snapshot folders
       (e.g. 2026-09-*), abandoned chunks (.graphify_chunk_*.json), and orphaned intermediate files.
    2. Zero-Friction Python Resolution: Discovers graphifyy in uv tool environments,
       pipx, active virtual environments, or system paths.
    3. Thorough Extraction & Graph Updates: Executes multi-worker structural and AST
       extraction across code, markdown RFCs, JSON schemas, capability contracts, and specs.
    4. Community Clustering & Analysis: Performs Louvain/graspologic community detection,
       god node identification, and structural cohesion scoring.
    5. Visualization & Artifact Refresh: Regenerates graph.json, GRAPH_REPORT.md, and
       interactive graph.html.
    6. Clean State Guarantee: Ensures graphify-out remains minimal, fast, and free of
       accumulated stale snapshot clutter across regular updates.

.PARAMETER TargetDirectory
    Directory or repository root to graphify (default: current directory '.').

.PARAMETER Update
    Performs incremental update, re-extracting only modified/new files since last run.

.PARAMETER Full
    Forces a complete fresh scan and full extraction across the codebase.

.PARAMETER CleanStale
    Cleans stale dated snapshot folders and temporary artifacts without re-running extraction.

.PARAMETER NoViz
    Skips interactive HTML visualization generation.

.PARAMETER Obsidian
    Generates Obsidian markdown vault notes and canvas in graphify-out/obsidian.

.PARAMETER ClusterOnly
    Reruns clustering and community detection on existing graph without re-extracting.

.PARAMETER Directed
    Builds a directed graph preserving edge direction (source -> target).

.PARAMETER CodeOnly
    Runs structural AST extraction for code files only (skips markdown/docs).

.PARAMETER WhatIf
    Dry-run mode: inspects files to clean and update without modifying disk state.

.EXAMPLE
    .\graphify.bat                           # Thorough graph update and stale cleanup
    .\graphify.bat -Update                   # Incremental update + stale cleanup
    .\graphify.bat -Full                     # Force full rebuild
    .\graphify.bat -CleanStale               # Prune stale folders and temp files only
    .\graphify.bat -Obsidian                 # Update graph and generate Obsidian vault
    .\graphify.bat -ClusterOnly              # Re-cluster existing graph
#>

[CmdletBinding()]
param (
    [Parameter(Position = 0)]
    [string]$TargetDirectory = ".",

    [Parameter(Position = 1)]
    [string]$OutDir = "",

    [switch]$Update,

    [switch]$Full,

    [switch]$CleanStale,

    [switch]$NoViz,

    [switch]$Obsidian,

    [switch]$ClusterOnly,

    [switch]$Directed,

    [switch]$CodeOnly,

    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

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

# 1. Resolve Target Root and graphify-out directory with smart multi-repo discovery
$ResolvedTarget = (Resolve-Path $TargetDirectory).Path

if ($OutDir) {
    if ([System.IO.Path]::IsPathRooted($OutDir)) {
        $GraphifyOutDir = $OutDir
    } else {
        $GraphifyOutDir = Join-Path $ResolvedTarget $OutDir
    }
    Write-Status "Using explicitly specified output directory: $GraphifyOutDir"
} elseif ($env:GRAPHIFY_OUT) {
    if ([System.IO.Path]::IsPathRooted($env:GRAPHIFY_OUT)) {
        $GraphifyOutDir = $env:GRAPHIFY_OUT
    } else {
        $GraphifyOutDir = Join-Path $ResolvedTarget $env:GRAPHIFY_OUT
    }
    Write-Status "Using environment GRAPHIFY_OUT directory: $GraphifyOutDir"
} else {
    # Auto-discover existing output directory if placed in standard alternative repo locations
    $candidates = @(
        (Join-Path $ResolvedTarget "graphify-out"),
        (Join-Path $ResolvedTarget "docs\graphify-out"),
        (Join-Path $ResolvedTarget "docs\knowledge-graph"),
        (Join-Path $ResolvedTarget ".graphify-out")
    )
    $found = $null
    foreach ($cand in $candidates) {
        if ((Test-Path (Join-Path $cand "graph.json")) -or (Test-Path (Join-Path $cand "GRAPH_REPORT.md"))) {
            $found = $cand
            break
        }
    }
    if ($found) {
        $GraphifyOutDir = $found
        Write-Status "Auto-discovered existing Graphify directory: $GraphifyOutDir"
    } else {
        $GraphifyOutDir = Join-Path $ResolvedTarget "graphify-out"
    }
}

if (-not (Test-Path $GraphifyOutDir)) {
    if (-not $WhatIf) {
        New-Item -ItemType Directory -Force -Path $GraphifyOutDir | Out-Null
    }
}

# 2. Stale Cleanup Function (Approved Verb: Remove)
function Remove-StaleGraphifyArtifacts {
    param(
        [string]$OutDir,
        [switch]$DryRun
    )

    if (-not (Test-Path $OutDir)) { return }

    Write-Status "Scanning for stale Graphify snapshots and intermediate artifacts in: $OutDir"

    # 2.1 Find and remove dated snapshot folders (e.g. 2026-09-15, 2026-09-16, etc.)
    $datedDirs = Get-ChildItem -Path $OutDir -Directory -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -match '^\d{4}-\d{2}-\d{2}'
    }

    $removedCount = 0
    foreach ($dir in $datedDirs) {
        if ($DryRun) {
            Write-Notice " [WhatIf] Would remove stale dated snapshot folder: $($dir.FullName)"
        }
        else {
            Write-Notice " Removing stale dated snapshot folder: $($dir.Name)"
            Remove-Item -Path $dir.FullName -Recurse -Force -ErrorAction SilentlyContinue
            $removedCount++
        }
    }

    # 2.2 Remove lingering temporary intermediate build files
    $tempPatterns = @(
        ".graphify_chunk_*.json",
        ".graphify_old.json",
        ".needs_update",
        ".graphify_ast.json",
        ".graphify_semantic_new.json",
        ".graphify_uncached.txt",
        ".graphify_incremental.json",
        ".graphify_cached.json",
        ".graphify_extract.json"
    )

    foreach ($pattern in $tempPatterns) {
        $tempFiles = Get-ChildItem -Path $OutDir -Filter $pattern -File -ErrorAction SilentlyContinue
        foreach ($file in $tempFiles) {
            if ($DryRun) {
                Write-Notice " [WhatIf] Would remove temp file: $($file.Name)"
            }
            else {
                Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
                $removedCount++
            }
        }
    }

    if ($removedCount -gt 0) {
        Write-Success "Pruned $removedCount stale snapshot(s) and temporary build artifact(s)."
    }
    else {
        Write-Success "Directory graphify-out is clean (no stale dated snapshots found)."
    }
}

# Execute stale cleanup before running updates
Remove-StaleGraphifyArtifacts -OutDir $GraphifyOutDir -DryRun:$WhatIf

if ($CleanStale) {
    Write-Success "CleanStale mode completed."
    exit 0
}

# 3. Resolve Python Environment with Graphify
function Resolve-GraphifyPython {
    # 1. uv tool install (authoritative)
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $uvDir = (uv tool dir 2>$null)
        if ($uvDir) {
            $cleanUv = $uvDir.Trim()
            $py = Join-Path $cleanUv "graphifyy\Scripts\python.exe"
            if (Test-Path $py) {
                & $py -c "import graphify" 2>$null
                if ($LASTEXITCODE -eq 0) { return $py }
            }
        }
    }

    # 2. pipx environment
    if (Get-Command pipx -ErrorAction SilentlyContinue) {
        $venvs = (pipx environment --value PIPX_LOCAL_VENVS 2>$null)
        if ($venvs) {
            $cleanVenvs = $venvs.Trim()
            $py = Join-Path $cleanVenvs "graphifyy\Scripts\python.exe"
            if (Test-Path $py) {
                & $py -c "import graphify" 2>$null
                if ($LASTEXITCODE -eq 0) { return $py }
            }
        }
    }

    # 3. Active virtual environment
    if ($env:VIRTUAL_ENV) {
        $venvPy = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
        if (Test-Path $venvPy) {
            & $venvPy -c "import graphify" 2>$null
            if ($LASTEXITCODE -eq 0) { return $venvPy }
        }
    }

    # 4. Local repo .venv
    $localVenv = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (Test-Path $localVenv) {
        & $localVenv -c "import graphify" 2>$null
        if ($LASTEXITCODE -eq 0) { return $localVenv }
    }

    # 5. graphify.exe launcher directory python
    $graphifyCmd = Get-Command graphify -ErrorAction SilentlyContinue
    if ($graphifyCmd) {
        $cmdDir = Split-Path $graphifyCmd.Source
        $pyCandidate = Join-Path $cmdDir "python.exe"
        if (Test-Path $pyCandidate) {
            & $pyCandidate -c "import graphify" 2>$null
            if ($LASTEXITCODE -eq 0) { return $pyCandidate }
        }
    }

    # 6. Fallback system python
    $sysPy = Get-Command python -ErrorAction SilentlyContinue
    if ($sysPy) {
        & $sysPy.Source -c "import graphify" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pyOut = (& $sysPy.Source -c "import sys; print(sys.executable)").Trim()
            return $pyOut
        }
    }

    return $null
}

$GraphifyPython = Resolve-GraphifyPython

if (-not $GraphifyPython) {
    Write-Notice "graphify module not found. Installing via uv tool / pip..."
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv tool install --upgrade graphifyy
    }
    else {
        pip install --upgrade graphifyy
    }
    $GraphifyPython = Resolve-GraphifyPython
}

if (-not $GraphifyPython) {
    Write-Fail "Error: Could not locate or install a Python environment containing 'graphifyy'."
    exit 1
}

Write-Status "Resolved Graphify Python: $GraphifyPython"

# Save environment markers
if (-not $WhatIf) {
    $Utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText((Join-Path $GraphifyOutDir ".graphify_python"), [string]$GraphifyPython, $Utf8NoBom)
    [System.IO.File]::WriteAllText((Join-Path $GraphifyOutDir ".graphify_root"), [string]$ResolvedTarget, $Utf8NoBom)
}

# 4. Execute Graphify Operations
if ($ClusterOnly) {
    Write-Status "Executing cluster-only refresh on existing graph..."
    if (-not $WhatIf) {
        graphify cluster-only "$ResolvedTarget"
    }
    Write-Success "Cluster-only refresh complete."
    exit 0
}

Write-Status "Executing thorough Graphify extraction & graph update on: $ResolvedTarget"

$CurrentGitCommit = (git rev-parse HEAD 2>$null)
if ($CurrentGitCommit) { $CurrentGitCommit = $CurrentGitCommit.Trim() }
if (-not $CurrentGitCommit) { $CurrentGitCommit = "UNKNOWN" }

# Build Python execution script for deterministic graph updates
$isDirectedStr = if ($Directed) { "True" } else { "False" }
$isUpdateStr = if ($Update -and -not $Full) { "True" } else { "False" }
$isCodeOnlyStr = if ($CodeOnly) { "True" } else { "False" }

$PyScript = @'
import os, sys, json, datetime
from pathlib import Path

target_root = Path(r'__TARGET_ROOT__')
out_dir = Path(r'__OUT_DIR__')
out_dir.mkdir(parents=True, exist_ok=True)

is_directed = __IS_DIRECTED__
is_update = __IS_UPDATE__
is_code_only = __IS_CODE_ONLY__
built_at_commit = '__BUILT_AT_COMMIT__'
built_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

print(f"Target Root: {target_root}")
print(f"Mode: {'Incremental Update' if is_update else 'Full Extraction'}")
print(f"Commit Provenance: {built_at_commit}")

# Step A: Detection & Extraction
from graphify.detect import detect, detect_incremental, save_manifest
from graphify.extract import collect_files, extract
from graphify.build import build_from_json, build_merge
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json
from graphify.cli import _stamped_manifest_files

if is_update and (out_dir / "graph.json").exists() and (out_dir / "manifest.json").exists():
    print("Running incremental detection...")
    inc_res = detect_incremental(target_root)
    new_total = inc_res.get('new_total', 0)
    deleted = list(inc_res.get('deleted_files', []))
    print(f"Incremental scan: {new_total} changed/new, {len(deleted)} deleted files")
    
    categories = ['code'] if is_code_only else ['code', 'document', 'paper']
    extract_files = []
    for cat in categories:
        for f in inc_res.get('new_files', {}).get(cat, []):
            p = Path(f)
            extract_files.extend(collect_files(p) if p.is_dir() else [p])
            
    ast_result = extract(extract_files, cache_root=target_root, parallel=(sys.platform != 'win32')) if extract_files else {'nodes': [], 'edges': [], 'input_tokens': 0, 'output_tokens': 0}
    
    prune = list(deleted) or None
    G = build_merge(
        [ast_result],
        graph_path=str(out_dir / 'graph.json'),
        prune_sources=prune,
        root=str(target_root),
        directed=is_directed
    )
    
    extraction = {
        'nodes': [{'id': n, **d} for n, d in G.nodes(data=True)],
        'edges': [{'source': d.get('_src', u), 'target': d.get('_tgt', v), **{k: val for k, val in d.items() if k not in ('_src', '_tgt', 'source', 'target')}} for u, v, d in G.edges(data=True)],
        'hyperedges': list(G.graph.get('hyperedges', [])),
        'input_tokens': ast_result.get('input_tokens', 0),
        'output_tokens': ast_result.get('output_tokens', 0)
    }
    
    _manifest_files = _stamped_manifest_files(inc_res.get('files', {}), extraction, target_root)
    _scan = {f for fl in inc_res.get('files', {}).values() for f in fl}
    save_manifest(_manifest_files, root=str(target_root), scan_corpus=_scan)

else:
    print("Running full codebase detection & multi-worker extraction...")
    det_res = detect(target_root)
    print(f"Corpus detected: {det_res.get('total_files', 0)} files, ~{det_res.get('total_words', 0):,} words")
    
    categories = ['code'] if is_code_only else ['code', 'document', 'paper']
    extract_files = []
    for cat in categories:
        for f in det_res.get('files', {}).get(cat, []):
            p = Path(f)
            extract_files.extend(collect_files(p) if p.is_dir() else [p])
            
    print(f"Extracting AST & semantics across {len(extract_files)} files...")
    ast_result = extract(extract_files, cache_root=target_root, parallel=(sys.platform != 'win32')) if extract_files else {'nodes': [], 'edges': [], 'input_tokens': 0, 'output_tokens': 0}
    print(f"Extracted: {len(ast_result['nodes'])} nodes, {len(ast_result['edges'])} edges")
    
    G = build_from_json(ast_result, root=str(target_root), directed=is_directed)
    extraction = ast_result
    
    _manifest_files = _stamped_manifest_files(det_res.get('files', {}), extraction, target_root)
    _scan = {f for fl in det_res.get('files', {}).values() for f in fl}
    save_manifest(_manifest_files, root=str(target_root), scan_corpus=_scan)

if G.number_of_nodes() == 0:
    print("Warning: Graph has 0 nodes.")
else:
    print("Clustering graph & detecting communities...")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    
    labels_file = out_dir / ".graphify_labels.json"
    if labels_file.exists():
        try:
            existing_labels = json.loads(labels_file.read_text(encoding="utf-8"))
            labels = {int(k): v for k, v in existing_labels.items()}
        except Exception:
            labels = {cid: f"Community {cid}" for cid in communities}
    else:
        labels = {cid: f"Community {cid}" for cid in communities}
        
    for cid in communities:
        if cid not in labels:
            labels[cid] = f"Community {cid}"
            
    questions = suggest_questions(G, communities, labels)
    
    # Save graph.json with force=True for deterministic authoritative updates
    to_json(G, communities, str(out_dir / "graph.json"), community_labels=labels, force=True)
    
    # Save report
    det_summary = detect(target_root)
    tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
    report = generate(G, communities, cohesion, labels, gods, surprises, det_summary, tokens, str(target_root), suggested_questions=questions)
    report += f"\n\n## Graph Freshness\n- **Built at commit:** `{built_at_commit}`\n- **Built timestamp:** `{built_timestamp}`\n- **Lineage type:** `ancestor_snapshot`\n"
    (out_dir / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    
    # Save analysis sidecar
    analysis = {
        'built_at_commit': built_at_commit,
        'built_timestamp': built_timestamp,
        'lineage_type': 'ancestor_snapshot',
        'communities': {str(k): v for k, v in communities.items()},
        'cohesion': {str(k): v for k, v in cohesion.items()},
        'gods': gods,
        'surprises': surprises,
        'questions': questions
    }
    (out_dir / ".graphify_analysis.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / ".graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()}, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"Graph finalized: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities (commit {built_at_commit[:8]})")
'@ -replace '__TARGET_ROOT__', $ResolvedTarget -replace '__OUT_DIR__', $GraphifyOutDir -replace '__IS_DIRECTED__', $isDirectedStr -replace '__IS_UPDATE__', $isUpdateStr -replace '__IS_CODE_ONLY__', $isCodeOnlyStr -replace '__BUILT_AT_COMMIT__', $CurrentGitCommit

if ($WhatIf) {
    Write-Notice "[WhatIf] Would execute graphify update pipeline with interpreter: $GraphifyPython"
}
else {
    $RunnerPy = Join-Path $GraphifyOutDir ".graphify_update_runner.py"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($RunnerPy, $PyScript, $Utf8NoBom)
    try {
        & $GraphifyPython $RunnerPy
        $resCode = $LASTEXITCODE
    }
    finally {
        if (Test-Path $RunnerPy) { Remove-Item $RunnerPy -Force -ErrorAction SilentlyContinue }
    }
    if ($resCode -ne 0) {
        Write-Fail "Graphify Python update exited with code $resCode"
        exit $resCode
    }

    # Generate HTML visualization if not skipped
    if (-not $NoViz) {
        Write-Status "Generating interactive HTML visualization..."
        graphify export html --graph (Join-Path $GraphifyOutDir "graph.json") --labels (Join-Path $GraphifyOutDir ".graphify_labels.json")
    }

    # Generate Obsidian vault if requested
    if ($Obsidian) {
        Write-Status "Generating Obsidian notes & canvas..."
        graphify export obsidian --graph (Join-Path $GraphifyOutDir "graph.json") --labels (Join-Path $GraphifyOutDir ".graphify_labels.json")
    }

    # Post-run cleanup: guarantee no stale temporary files remain
    Remove-StaleGraphifyArtifacts -OutDir $GraphifyOutDir
}

Write-Success "Graphify update completed successfully."
Write-Host "Outputs available in: $GraphifyOutDir"
Write-Host " - graph.json (Knowledge Graph Structure)"
Write-Host " - GRAPH_REPORT.md (Architectural & Community Report)"
Write-Host " - graph.html (Interactive Visualization)"
