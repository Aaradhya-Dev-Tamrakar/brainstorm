# Authoritative Ecosystem Repository & Capability Directory

This directory catalogs all repositories, computational engines, and presentation hubs across Aaradhya's personal tool ecosystem. 

Ground truth is anchored in [`schemas/ecosystem.registry.json`](../../../../schemas/ecosystem.registry.json). All physical paths and test commands are classified under `ARCH-RFC-001` epistemic evidence tiers.

---

## 1. Dynamic Path Resolution Invariant

To ensure multi-device portability across laptops, external storage, and secondary clones:
- **Canonical Default**: `F:\Aaradhya-Dev-Tamrakar` and `F:\AaradhyaDT`.
- **Dynamic Fallback**: If drive `F:\` is unmounted, tools must resolve roots via:
  1. `$env:ECOSYSTEM_ROOT` (if defined in machine environment).
  2. Relative sibling discovery: `(Get-Item $PSScriptRoot).Parent.FullName`.

---

## 2. Central Architectural Root

| ID | Name | Local Path | Role | Verification Command |
| :--- | :--- | :--- | :--- | :--- |
| **`brainstorm`** | Central Architecture Registry | `F:\Aaradhya-Dev-Tamrakar\brainstorm` | Mesh Root, SMT Verification, Simulation Engine, RFCs | `.\audit.bat` `[EMPIRICALLY_VERIFIED]` |

---

## 3. Computational Engines (24 Authoritative Modules)

| Index | ID | Name | Canonical Path | Tech Stack | Execution Context | Core Superpower | Test / Execution Command |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `super-nlm` | Super-NLM Hub | `F:\Aaradhya-Dev-Tamrakar\super-nlm` | FastAPI, React, MCP | Cloud / Hybrid | Multi-account NotebookLM aggregator & rotation | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **2** | `fusion360-mcp` | Fusion 360 MCP Bridge | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\fusion360-mcp` | Python 3.10, Fusion API, MCP | Local Desktop | Conversational 3D CAD parametric modeling automation | Direct MCP `[EMPIRICALLY_VERIFIED]` |
| **3** | `system-optimizer` | NovaOptimizer | `F:\Aaradhya-Dev-Tamrakar\system-optimizer` | C# .NET 10, WPF, Win32 | Local Bare Metal | RAM cache purge (`EmptyWorkingSet`) & priority boost | `dotnet build` `[EMPIRICALLY_VERIFIED]` |
| **4** | `SPARK` | SPARK Gateway | `F:\Aaradhya-Dev-Tamrakar\SPARK` | C/C++ (ESP32-S3), Python, SHAP | Edge Hardware | Edge fall detection, kinematics, clinical explainability | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **5** | `Nexus` | Nexus AI Workspace | `F:\AaradhyaDT\Nexus` | FastAPI, React, SQLite FTS5 | Local / Hybrid | Project-centric AI workspace & prompt multiplexer | `start-nexus.bat` `[EMPIRICALLY_VERIFIED]` |
| **6** | `Claude-Desktop` | Claude Worker Fleet | `F:\Aaradhya-Dev-Tamrakar\Claude-Desktop` | FastAPI, SQLite WAL, PowerShell | Local / Distributed | Multi-profile session persistence & DAG task fleet | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **7** | `BiasAperture` | BiasAperture | `F:\Aaradhya-Dev-Tamrakar\BiasAperture` | PyTorch, Python CLI, LaTeX | Local / Compute | Demographic bias auditing framework for vision models | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **8** | `Alpha-SuperApp` | Alpha-SuperApp | `F:\Aaradhya-Dev-Tamrakar\Alpha-SuperApp` | Kotlin 2.2, Jetpack Compose | Mobile Device | Android super-app: CV, BLE hardware, Finance, AI | `gradlew assembleDebug` `[EMPIRICALLY_VERIFIED]` |
| **9** | `screen-qa-extension` | Screen Q&A | `F:\Aaradhya-Dev-Tamrakar\Utility\screen-qa-extension` | Chrome MV3 (JS), Gemini Flash | Ambient Browser | Ambient browser zero-click question overlay | Chrome DevTools `[EMPIRICALLY_VERIFIED]` |
| **10** | `md2pdf-desktop` | md2pdf & MCP | `F:\Aaradhya-Dev-Tamrakar\Utility\md2pdf-desktop` | Python, Pandoc, LaTeX, FastMCP | Desktop / Fleet MCP | Publication-grade Markdown-to-PDF rendering engine | `python test_md2pdf.py` `[EMPIRICALLY_VERIFIED]` |
| **11** | `yt-dlp-live` | yt-dlp-live | `F:\Aaradhya-Dev-Tamrakar\Utility\yt-dlp-live` | PowerShell, yt-dlp, FFmpeg, QSV | Local Daemon | 24/7 stream capture daemon & media transformer | `.\record_live.bat` `[EMPIRICALLY_VERIFIED]` |
| **12** | `AI` | AI Constraint Solver | `F:\AaradhyaDT\AI` | Python, FastAPI, CLI | Local Microservice | Cryptarithmetic and combinatorial CSP solver | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **13** | `rsvp-reading` | RSVP Reader | `F:\AaradhyaDT\rsvp-reading` | Svelte, Vite, Vitest | Local Web | High-speed RSVP reader with ORP centering | `npm test` `[EMPIRICALLY_VERIFIED]` |
| **14** | `github-pilot` | GitHub Pilot | `F:\Aaradhya-Dev-Tamrakar\Utility\github-pilot` | Python, HTTP/2, selectolax | Local / Fleet CLI | Autonomous GitHub profile & ecosystem navigator | `python -m github_pilot` `[EMPIRICALLY_VERIFIED]` |
| **15** | `nepali-ocr-ai` | Nepali OCR AI | `F:\Aaradhya-Dev-Tamrakar\Utility\nepali-ocr-ai` | Python, python-docx, FastMCP | Local Microservice | Nepali vision OCR, grammar check, Unicode transcoder | FastMCP Call `[EMPIRICALLY_VERIFIED]` |
| **16** | `google-classroom-mcp` | Classroom MCP | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\google-classroom-mcp` | Node.js ESM, MCP SDK | Local / Fleet MCP | Google Classroom courses, assignments & submissions | MCP Query `[EMPIRICALLY_VERIFIED]` |
| **17** | `localsend-mcp` | LocalSend MCP | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\localsend-mcp` | Node.js ESM, MCP SDK | Local / Fleet MCP | Zero-cloud LAN file, text & clipboard transfer | MCP Query `[EMPIRICALLY_VERIFIED]` |
| **18** | `downloader-scripts` | Downloader Scripts | `F:\Aaradhya-Dev-Tamrakar\Utility\downloader-scripts` | PowerShell 7, WPF, yt-dlp | Local Desktop | Zero-click clipboard auto-downloader & audio selector | PowerShell Test `[EMPIRICALLY_VERIFIED]` |
| **19** | `typora-mcp` | Typora MCP | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\typora-mcp` | Node.js ESM, TypeScript | Local / Fleet MCP | Programmatic Typora editor automation & crash parsing | MCP Query `[EMPIRICALLY_VERIFIED]` |
| **20** | `Win-Vault` | Win-Vault | `F:\Aaradhya-Dev-Tamrakar\Win-Vault` | PowerShell 7, WinForms, NTFS | Bare Metal Desktop | Native GUI privacy vault with kernel-level NTFS ACL denial | `.\Vault.bat` `[EMPIRICALLY_VERIFIED]` |
| **21** | `Cyber-Forensics` | Cyber-Forensics | `F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics` | PowerShell 7, Win32 NT APIs | Bare Metal Desktop | DFIR artifact triage & stealth evasion hunting | `pwsh tests\*.ps1` `[EMPIRICALLY_VERIFIED]` |
| **22** | `omnivault` | OmniVault | `F:\Aaradhya-Dev-Tamrakar\omnivault` | Python 3.14, SQLite FTS5, BLAKE3 | Desktop / Hybrid | Tri-tier archival engine (Mobile, NVMe, Cold HDD) | `pytest` `[EMPIRICALLY_VERIFIED]` |
| **23** | `Fleet-Orchestrator` | Fleet-Orchestrator | `F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator` | Python 3.12+, FastAPI, SQLite | Local Fleet Cluster | Swarm task coordinator, 27x Copilot quota pooling | `copilot_fleet.py` `[EMPIRICALLY_VERIFIED]` |
| **24** | `agent-customization-sync` | Agent-Customization-Sync | `F:\Aaradhya-Dev-Tamrakar\Agent-Customization-Sync` | Python 3.14, Win32 NTFS | Local Desktop / Cross-IDE | Cross-IDE agent customization sync, cryptographic state snapshots, and lossless transpilation | `pytest` `[EMPIRICALLY_VERIFIED]` |

---

## 4. Presentation & Educational Hubs (4 Authoritative Hubs)

| Index | ID | Name | Canonical Path | Tech Stack | Role & Canonical Superpower |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **25** | `AaradhyaDT.github.io` | Primary Authoritative Portfolio | `F:\AaradhyaDT\AaradhyaDT.github.io` | Static Web, Vanilla JS, CSS | Canonical portfolio website, interactive radar, 26-category verification gate |
| **26** | `Aaradhya-Dev-Tamrakar.github.io` | Portfolio Profile Mirror | `F:\Aaradhya-Dev-Tamrakar\Aaradhya-Dev-Tamrakar.github.io` | Static Web | Secondary public organization mirror |
| **27** | `makerspace` | Makerspace Hub | `F:\Aaradhya-Dev-Tamrakar\makerspace` | CAD / Hardware Assets | Physical maker laboratory, fabrication assets, 3D printing staging |
| **28** | `react-workshop-ieeekecktm` | React Workshop Hub | `F:\AaradhyaDT\react-workshop-ieeekecktm` | React, TypeScript, Vite | Hands-on curriculum and modern frontend architecture reference |

---

## 5. Specialized AEC-MCP Suite (`F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite`)

14 specialized Architecture, Engineering & Construction Model Context Protocol servers:
- `fusion360-mcp` / `Autodesk-Fusion-360-MCP-Server`: Parametric 3D CAD modeling.
- `revit-mcp`: BIM parameter modification and model inspection.
- `autocad-mcp`: DWG/DXF programmatic geometry automation.
- `rhino-mcp`: NURBS and computational geometry manipulation.
- `etabs-mcp`, `sap2000-mcp`, `staad-mcp`: Structural analysis and FEM frame solvers.
- `epanet-mcp`: Hydraulic pipe network flow simulation.
- `qgis-mcp`: GIS vector/raster geospatial processing.
- `sketchup-mcp`, `3dsmax-mcp`, `maya-mcp`: Architectural visualization and rendering.
- `autodesk-mcp`: Master unified gateway dispatching across Autodesk desktop products.

---

## 6. Local Utility Extras & Experimental Archives (Non-Registry)

These utilities are tracked locally on disk but remain outside the formal 28-module ecosystem registry:
- **`windows-pilot`** (`F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot`): Native UI Automation (UIA) tree inspector, screenshot perception, desktop driver.
- **`IEEE-Xtreme-Archive`** (`F:\Aaradhya-Dev-Tamrakar\IEEE-Xtreme-Archive`): Competitive programming task and solution repository.
