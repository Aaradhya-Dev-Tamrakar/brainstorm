> **Artifact ID:** `ARCH-SPEC-007`  
> **Title:** Deterministic Environment Reproducibility, Toolchain Bootstrapping & Antigravity Mirror Standard  
> **Version:** `1.0.0`  
> **Status:** `IMPLEMENTED`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Developer Operations, Systems Engineering & Deterministic Toolchain Automation  
> **Domain:** Environment Automation, Antigravity Agent Configuration & CLI Bootstrapping  
> **Created Date:** 2026-09-24  
> **Evidence Tier:** `E4`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\brainstorm`  
> **Execution Context:** Antigravity / Windows PowerShell Runtime  
> **Upstream Trace:** [`ARCH-SPEC-003: Headless Orchestration Substrate`](ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md), [`tools/skills/README.md`](../../tools/skills/README.md)  
> **Downstream Trace:** [`scripts/bootstrap-environment.ps1`](../../scripts/bootstrap-environment.ps1), [`audit.bat`](../../audit.bat)  

---

## 1. Executive Summary & Problem Statement

To prevent configuration drift, lost development velocity, and manual token-intensive re-setup when moving across workstations, clean OS reinstalls, or secondary development machines, this specification codifies a **Single-Command Deterministic Environment Bootstrap Protocol**.

Setting up an engineering environment across 23 capability modules, multi-agent frameworks, custom CLI scrapers, and MCP toolchains manually requires configuring dozens of disparate paths, registry keys, and API configs. ARCH-SPEC-007 provides a reproducible, automated substrate that restores the full ecosystem in under 60 seconds.

---

## 2. Environment Architecture & Customization Layers

```
+-------------------------------------------------------------------------+
|                  AARADHYA ECOSYSTEM RUNTIME TOPOLOGY                   |
+-------------------------------------------------------------------------+
|                                                                         |
|  [Layer 4: Agent & Cognitive Layer]                                     |
|    - 19 Antigravity Custom Skills (`tools/skills/` <-> `~/.gemini/`)     |
|    - Global System Rules (`RULE[user_global]`, `AGENTS.md`)             |
|    - Multi-Model Cognitive Council Protocol (`ARCH-RFC-002`)            |
|                                                                         |
|  [Layer 3: Protocol & Tool Bridges (MCP Mesh)]                          |
|    - `super-nlm` (NotebookLM Token-Ring Multi-Account Fleet)            |
|    - `localsend` (P2P Subnet Mutual-TLS Mobile Handoff)                 |
|    - `md2pdf` (LaTeX / Typst Publication-Grade PDF Engine)              |
|    - `gdrive` / `shadcn` / `typora` / `local-files`                     |
|                                                                         |
|  [Layer 2: Global CLI Execution Substrate]                              |
|    - `save-doc` (Universal Google Doc / HTML DOM AST Exporter)          |
|    - `save-chat` (ChatGPT Conversation Stream Payload Scraper)          |
|    - `sync.ps1` (Multi-Branch Git Sync, Rebase & Secret Scan Engine)     |
|                                                                         |
|  [Layer 1: Deterministic Verification & Ground Truth]                   |
|    - `audit.bat` & `reconciliation_engine.py` (0-Discrepancy AST Check)  |
|    - Discrete-Event Simulation Regression Suite (9/9 Test Harness)      |
|    - User Shell Folders Configuration (Selective OneDrive Bypass)       |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

## 3. The 1-Click Bootstrap Protocol (`bootstrap-environment.ps1`)

On any new or freshly installed Windows workstation:

### Step 1: Clone Repository
```powershell
git clone https://github.com/Aaradhya-Dev-Tamrakar/brainstorm.git F:\Aaradhya-Dev-Tamrakar\brainstorm
cd F:\Aaradhya-Dev-Tamrakar\brainstorm
```

### Step 2: Run Bootstrap Engine
```powershell
.\scripts\bootstrap-environment.ps1
```

### What the Bootstrap Engine Executes:
1. **Python Runtime Validation:** Verifies Python 3.10+ and pip package manager.
2. **Dependency Ingestion:** Installs core AST parsing, discrete-event simulation, and verification dependencies (`beautifulsoup4`, `pyyaml`, `simpy`, `z3-solver`).
3. **Global CLI Deployment:** Copies `save_chat.py` and `save_doc.py` to Python's global Scripts directory, generates `.bat` executable wrappers, and ensures User `PATH` integration.
4. **Antigravity Skills Synchronization:** Copies all 19 custom skills from `tools/skills/` into `$HOME/.gemini/config/skills/` with zero manual copying.
5. **Deterministic Audit Gate:** Executes `audit.bat` to certify 100% link resolution, schema validity, and numerical simulation consistency.

---

## 4. Skills Taxonomy & Registry Reference

The 19 customized skills mirrored under `tools/skills/` are cataloged in [`tools/skills/README.md`](../../tools/skills/README.md):

1. **Ingestion & Archival:** `doc-archiver`, `chat-archiver`, `google-classroom`.
2. **Autonomous Swarms:** `agent-teams-orchestration` (Scout-Reviewer-Writer-Lead cognitive division).
3. **Codebase Graph & Systems:** `graphify`, `graphify-code-search`, `mcp-integration`, `skill-development`.
4. **Frontend & Motion:** `frontend-design`, `design-taste-frontend`, `antigravity-ui-motion-design-expert`, `google-ux-fluidity`, `google-stitch-integration`, `shadcn-context`.
5. **Ecosystem & Workflow:** `portfolio-project-manager`, `feature-dev`, `commit-commands`, `pr-review-toolkit`, `security-guidance`.

---

## 5. Verification & Acceptance Criteria

An environment is certified **Reproducibility Tier E4 (VERIFIED_EMPIRICAL)** when:
- `save-chat` and `save-doc` execute headlessly from any working directory.
- Antigravity detects all 19 custom skills natively upon launch.
- `.\audit.bat` executes cleanly with `0 discrepancies` and `9/9 tests passed`.
- `.\sync.ps1 -WhatIf` validates multi-branch ecosystem status without errors.
