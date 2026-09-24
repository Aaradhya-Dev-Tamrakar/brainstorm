# Document 3: Repository Technical Inventory & Present State

## 1. Ecosystem Scope & Inventory Overview
The ecosystem comprises **22 distinct tool modules** across computational engines, actuation bridges, ingestion gateways, and presentation hubs. Below is the authoritative technical breakdown derived from `schemas/ecosystem.registry.json` and active repository trees in `F:\Aaradhya-Dev-Tamrakar\` and `F:\AaradhyaDT\`.

---

## 2. Granular Module Specifications

### 1. `super-nlm` (Super-NLM Hub)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\super-nlm` | **Branch**: `super-nlm`
- **Tech Stack**: Python (FastAPI), React, Model Context Protocol (MCP), `nlm` CLI
- **Evidence Tier**: **E3** (Deterministic Simulation & Validated CLI Automation)
- **Superpower**: Multi-account Google NotebookLM aggregator, token-ring round-robin query rotation across 6 authenticated Google accounts, folder-to-notebook continuous synchronization, and autonomous background studio creation queue (`schedule_batch_creation`).

### 2. `fusion360-mcp` (Autodesk Fusion 360 MCP Bridge)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\fusion360-mcp` | **Branch**: `Autodesk-Fusion-360-MCP-Server`
- **Tech Stack**: Embedded Python 3.10, Autodesk Fusion API, CustomEvent, FastMCP
- **Evidence Tier**: **E4** (Empirical Hardware Execution)
- **Superpower**: Conversational 3D CAD modeling, automated zero-dependency sketch/extrude execution, and live viewport rendering directly within native Fusion 360 desktop sessions.

### 3. `system-optimizer` (NovaOptimizer)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\system-optimizer` | **Branch**: `system-optimizer`
- **Tech Stack**: C# .NET 10, WPF, Win32 / NT Kernel Native APIs
- **Evidence Tier**: **E4** (Empirical Hardware Telemetry)
- **Superpower**: Micro-footprint Windows OS tuning, deep memory purge via `EmptyWorkingSet`, thread priority boosting, and zero-latency gaming/ML compute profile switching.

### 4. `SPARK` (SPARK Wearable Gateway)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\SPARK` | **Branch**: `SPARK`
- **Tech Stack**: C/C++ (ESP32-S3), Python, SHAP, Bluetooth Low Energy (BLE)
- **Evidence Tier**: **E4** (Empirical Physical Sensor Validation)
- **Superpower**: Two-layer edge fall detection on wearable IMU kinematics, millisecond-level alerting, SHAP clinical explainability, and automated medical PDF dossier generation.

### 5. `Nexus` (Nexus AI Workspace)
- **Path**: `F:\AaradhyaDT\Nexus` | **Branch**: `Nexus`
- **Tech Stack**: FastAPI, React (Vite), SQLite FTS5 Full-Text Search
- **Evidence Tier**: **E3**
- **Superpower**: Project-centric AI workspace, prompt multiplexing across parallel LLM providers, and contextual semantic note memory.

### 6. `Claude-Desktop` (Claude Worker Fleet v2)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\Claude-Desktop` | **Branch**: `Claude-Desktop`
- **Tech Stack**: FastAPI coordinator, SQLite WAL Checkpointing, PowerShell
- **Evidence Tier**: **E3**
- **Superpower**: Multi-profile session persistence, distributed DAG task worker fleet, and SKU pipeline decomposition.

### 7. `BiasAperture` (BiasAperture Vision Fairness Auditor)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\BiasAperture` | **Branch**: `BiasAperture`
- **Tech Stack**: PyTorch, Python CLI, LaTeX
- **Evidence Tier**: **E4**
- **Superpower**: Demographic bias auditing framework for computer vision models, statistical disparity metrics across demographic slices, and automated LaTeX/PDF generation.

### 8. `Alpha-SuperApp` (Alpha-SuperApp)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\Alpha-SuperApp` | **Branch**: `Alpha-SuperApp`
- **Tech Stack**: Kotlin 2.2, Jetpack Compose, Android 16 SDK
- **Evidence Tier**: **E2**
- **Superpower**: All-in-one mobile super-application uniting Computer Vision, BLE wearable hardware control, Personal Finance tracking, and embedded AI assistants.

### 9. `screen-qa-extension` (Screen Q&A Extension)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\screen-qa-extension` | **Branch**: `screen-qa-extension`
- **Tech Stack**: Chrome Manifest V3 (JavaScript), Gemini Flash API
- **Evidence Tier**: **E3**
- **Superpower**: Ambient browser intelligence, instant on-screen question extraction from DOM/selection, and zero-click overlay answer streaming.

### 10. `md2pdf-desktop` (md2pdf-desktop & FastMCP Server)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\md2pdf-desktop` | **Branch**: `md2pdf-desktop`
- **Tech Stack**: Python 3.10+, Tkinter, Pandoc, LaTeX (`pdflatex`), FastMCP
- **Evidence Tier**: **E3**
- **Superpower**: Publication-grade Markdown-to-PDF compilation pipeline featuring mathematical LaTeX equations, callout alerts, and headless FastMCP server integration.

### 11. `yt-dlp-live` (yt-dlp-live Capture & DSP Cluster)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\yt-dlp-live` | **Branch**: `yt-dlp-live`
- **Tech Stack**: PowerShell 7, `yt-dlp`, FFmpeg, Intel QSV
- **Evidence Tier**: **E3**
- **Superpower**: Resilient livestream capture daemon, RTMP relay, and automated media transformer (Nightcore audio DSP scaling + Intel Arc hardware accelerated rendering).

### 12. `AI` (AI Constraint Solver)
- **Path**: `F:\AaradhyaDT\AI` | **Branch**: `AI`
- **Tech Stack**: Python, FastAPI, CLI
- **Evidence Tier**: **E3**
- **Superpower**: Cryptarithmetic and combinatorial constraint satisfaction problem (CSP) solver with structured JSON execution metrics.

### 13. `rsvp-reading` (RSVP Reader)
- **Path**: `F:\AaradhyaDT\rsvp-reading` | **Branch**: `rsvp-reading`
- **Tech Stack**: Svelte, Vite
- **Evidence Tier**: **E3**
- **Superpower**: High-speed RSVP reading HUD featuring Optimal Recognition Point (ORP) focal highlighting for EPUB and PDF documents.

### 14. `Aaradhya-Dev-Tamrakar.github.io` & 15. `AaradhyaDT.github.io`
- **Path**: `F:\Aaradhya-Dev-Tamrakar\Aaradhya-Dev-Tamrakar.github.io` | **Branch**: `Aaradhya-Dev-Tamrakar.github.io`
- **Tech Stack**: Static Web, Vanilla JS, Modern CSS, AES-256-GCM Link Encryption
- **Evidence Tier**: **E4**
- **Superpower**: Public portfolio presentation hub, interactive project radar, AES-256 protected access portal, and technical documentation mirror.

### 16. `makerspace` (Makerspace Fabrication Hub)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\makerspace` | **Branch**: `makerspace`
- **Tech Stack**: 3D CAD Assets, STEP/STL models, Bambu Studio configs
- **Evidence Tier**: **E2**
- **Superpower**: Physical maker laboratory, electronic component inventory, and rapid 3D printing staging.

### 17. `react-workshop-ieeekecktm` (React Workshop Reference)
- **Path**: `F:\AaradhyaDT\react-workshop-ieeekecktm` | **Branch**: `react-workshop-ieeekecktm`
- **Tech Stack**: React, TypeScript, Vite, Tailwind CSS
- **Evidence Tier**: **E3**
- **Superpower**: Educational curriculum and modern frontend architectural blueprint for IEEE workshops.

### 18. `github-pilot` (GitHub Pilot Fleet Auditor)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\github-pilot` | **Branch**: `github-pilot`
- **Tech Stack**: Python (Typer), HTTP/2, selectolax, Rich
- **Evidence Tier**: **E3**
- **Superpower**: Autonomous macro-plane GitHub profile auditor, repository health telemetry analyzer, and ecosystem navigator.

### 19. `nepali-ocr-ai` (Nepali OCR & Linguistic Repair AI)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\nepali-ocr-ai` | **Branch**: `nepali-ocr-ai`
- **Tech Stack**: Python 3.11, python-docx, FastMCP, OpenCV
- **Evidence Tier**: **E3**
- **Superpower**: Devanagari vision OCR, Varnavinyas grammar checking/correction, bi-directional Preeti-to-Unicode font transcoding, and Microsoft Word (`.docx`) layout repair.

### 20. `google-classroom-mcp` (Google Classroom MCP Server)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp` | **Branch**: `google-classroom-mcp`
- **Tech Stack**: Node.js ESM, `@modelcontextprotocol/sdk`, Google Classroom API
- **Evidence Tier**: **E4**
- **Superpower**: Headless Google Classroom integration for inspecting active courses, due dates, coursework attachments, teacher announcements, and managing student turn-ins.

### 21. `localsend-mcp` (LocalSend LAN P2P MCP Server)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\localsend-mcp` | **Branch**: `localsend-mcp`
- **Tech Stack**: Node.js ESM, `@modelcontextprotocol/sdk`, LocalSend Protocol v2.1
- **Evidence Tier**: **E4**
- **Superpower**: Air-gapped, zero-cloud P2P file, text, and clipboard transfer across local LAN/Wi-Fi devices with mutual TLS and persistent device listening.

### 22. `downloader-scripts` (Downloader Scripts Hub)
- **Path**: `F:\Aaradhya-Dev-Tamrakar\downloader-scripts` | **Branch**: `downloader-scripts`
- **Tech Stack**: PowerShell 7, WPF XAML, Windows Shell APIs, `yt-dlp`
- **Evidence Tier**: **E4**
- **Superpower**: Zero-click clipboard auto-paste downloader, 1-click WPF Audio vs Video selector dialog, dedicated routing to system Music/Video libraries, and Windows Toast notifications.

### 23. Domain Engineering CAD MCP Servers
- **Paths**: `F:\Aaradhya-Dev-Tamrakar\` (`3dsmax-mcp`, `autocad-mcp`, `autodesk-mcp`, `epanet-mcp`, `etabs-mcp`, `maya-mcp`, `qgis-mcp`, `revit-mcp`, `rhino-mcp`, `sap2000-mcp`, `sketchup-mcp`, `staad-mcp`, `windows-pilot`).
- **Superpower**: Comprehensive headless MCP bridging suite extending conversational agentic control into civil, structural, geospatial, hydraulic, and 3D architectural CAD software.
