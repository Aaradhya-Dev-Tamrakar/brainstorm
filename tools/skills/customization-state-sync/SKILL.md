---
name: customization-state-sync
description: Use this skill when the user asks to "snapshot customization state", "sync customizations across IDEs", "project Antigravity rules to Cursor or Claude", "audit customization drift", "restore agent settings snapshot", or mentions managing Agent-Customization-Sync.
version: 1.0.0
---

# Agent-Customization-Sync Reference Specification

Agent-Customization-Sync captures, snapshots, and losslessly projects Antigravity customization state across Cursor IDE, Claude Code CLI, GitHub Copilot, and OpenAI Codex environments while enforcing a strict 8,000-token static overhead ceiling.

---

## 1. Architectural Foundations

The engine designates `~/.gemini/config/` as the single authoritative state store. Edits made to rules, domain skills, and Model Context Protocol (MCP) server definitions synchronize outward to satellite environments via deterministic transpilation and zero-duplication NTFS directory junctions.

```
                          +-----------------------------------+
                          |  Antigravity SSOT (~/.gemini/)    |
                          |  - AGENTS.md, GEMINI.md           |
                          |  - mcp_config.json, config.json   |
                          |  - skills/ (45+ modular skills)   |
                          +-----------------+-----------------+
                                            |
                       +--------------------+--------------------+
                       |                                         |
                       v                                         v
        +-----------------------------+           +-----------------------------+
        |   Snapshot & Rollback       |           |   Cross-IDE Transpiler      |
        |   - SHA-256 Merkle Manifest |           |   - Rules: .mdc, CLAUDE.md  |
        |   - Rolling 5-slot Buffer   |           |   - MCP: Cursor/Claude/VSCode|
        |   - Pre-restore Safety Back |           |   - Skills: NTFS Junctions  |
        +--------------+--------------+           +--------------+--------------+
                       |                                         |
                       +--------------------+--------------------+
                                            |
                                            v
                         +-------------------------------------+
                         |      Drift & Token Auditor          |
                         |      - Cross-IDE divergence checks  |
                         |      - Ceiling: < 8,000 tokens      |
                         |      - Headroom: >= 60% budget      |
                         +-------------------------------------+
```

### Core Subsystems

1. **State Snapshot & Rollback Engine (`snapshot_engine.py`)**:
   - Generates a cryptographic SHA-256 manifest across all rules, skills, MCP servers, and settings.
   - Archives state bundles into `~/.gemini/snapshots/customizations/snapshot_<timestamp>.zip`.
   - Enforces a rolling 5-slot ring buffer eviction policy to bound local disk consumption.
   - Guarantees safe restoration with pre-flight safety backups and byte-level hash verification.

2. **Cross-IDE Transpiler (`transpilers/`)**:
   - `RulesTranspiler`: Ingests `AGENTS.md` and generates Claude Code `CLAUDE.md`, Cursor modular `.cursor/rules/*.mdc` (with YAML frontmatter `globs: ["*"]` and `alwaysApply: true`), legacy `.cursorrules`, and GitHub Copilot `.github/copilot-instructions.md`.
   - `MCPNormalizer`: Normalizes `mcp_config.json` into Cursor (`~/.cursor/mcp.json`), Claude Code (`~/.claude/settings.json`), and VS Code (`.vscode/mcp.json`) schemas with optional credential scrubbing.
   - `SkillsLinker`: Uses Windows NTFS Directory Junctions (`mklink /J`) to mirror `~/.gemini/config/skills/` into `~/.claude/skills/` and `~/.cursor/skills-cursor/` without disk duplication.

3. **Drift & Token Overhead Auditor (`auditor.py`)**:
   - Compares live configurations across target IDEs against the canonical manifest.
   - Measures token overhead per component and validates against the 8,000-token ceiling ($\ge 60\%$ context headroom).

4. **Zero-Friction CLI & Batch Wrapper (`custom_sync.bat`)**:
   - Exposes clean CLI subcommands (`snapshot`, `list`, `restore`, `push`, `audit`, `status`).

---

## 2. Operational Invariants & Scope Boundaries

1. **Single Source of Truth Invariant**: All rule, skill, and MCP modifications must occur in Antigravity or git. Edits in target IDE directories are treated as configuration drift and are overwritten during push operations.
2. **Safe Rollback Invariant**: Restoring a snapshot must create an automated pre-restore backup of target directories before applying changes.
3. **Token Ceiling Invariant**: Total static prompt prefix overhead across active configurations must not exceed 8,000 tokens ($< 40\%$ of standard prefix budgets).
4. **Non-Goal: Bidirectional Merging**: The engine does not perform three-way Git merges on rules modified independently across multiple IDEs.
5. **Non-Goal: Secret Vault Replacement**: MCP normalization masks credentials when exporting configuration bundles, but the tool does not replace dedicated credential vaults such as Bitwarden.

---

## 3. Command Line Interface

Execute the tool using the zero-friction batch wrapper `custom_sync.bat` from `F:\Aaradhya-Dev-Tamrakar\Agent-Customization-Sync`:

```bat
REM Create a timestamped state snapshot checkpoint
.\custom_sync.bat snapshot --tag "pre-upgrade"

REM List available snapshots in the rolling ring buffer
.\custom_sync.bat list

REM Restore configuration from a designated snapshot
.\custom_sync.bat restore --latest
.\custom_sync.bat restore --id "snapshot_20261009_073208_initial_baseline"

REM Project canonical state to all supported IDEs
.\custom_sync.bat push --all

REM Project state selectively to specific targets
.\custom_sync.bat push --cursor --mode junction
.\custom_sync.bat push --claude
.\custom_sync.bat push --vscode

REM Run drift detection and token budget audit
.\custom_sync.bat audit

REM View active configuration telemetry
.\custom_sync.bat status
```

### Programmatic Python Interface

The engine can be invoked directly from Python workflows or subagents:

```python
from pathlib import Path
from agent_customization_sync.snapshot_engine import SnapshotEngine
from agent_customization_sync.auditor import CustomizationAuditor

# Create a state snapshot
engine = SnapshotEngine()
metadata = engine.create_snapshot(tag="pre-release")
print(f"Snapshot created: {metadata.snapshot_id}")

# Run drift audit across IDEs
auditor = CustomizationAuditor()
report = auditor.audit_drift()
print(f"Drift status: {report.overall_status}")
```

### Manifest Schema Payload

The snapshot engine records state in `customization_manifest.json`:

```json
{
  "schema_version": "1.0.0",
  "created_at": "2026-10-09T07:32:08.368157+00:00",
  "source_path": "C:\\Users\\Aaradhya\\.gemini\\config",
  "total_token_overhead": 560189,
  "headroom_percent": 0.0,
  "sha256_root": "4bd2274796a3f73ccf3b859047a9a56f356023af366fa656f6faa327fb64256f"
}
```

---

## 4. Verification Protocol

The regression test suite verifies hashing stability, ring buffer eviction, schema transpilation, and rollback verification:

```powershell
pytest "F:\Aaradhya-Dev-Tamrakar\Agent-Customization-Sync\tests" -v
```
