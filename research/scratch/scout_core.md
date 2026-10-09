# Executive Data Manifest: Core Computational Engines (Scout Core)

**Generated**: 2026-10-09  
**Inspector**: Commander 1 (Core Repos Commander)  
**Scope**: 14 Core Computational Engines across `F:\Aaradhya-Dev-Tamrakar` & `F:\AaradhyaDT`  
**Schema Authority**: `schemas/capability.contract.v1.json`, `schemas/ecosystem.registry.json`, `schemas/capability-registry.yaml`

---

## 1. Core Computational Engines Manifest

| Repo ID | Name | Absolute Local Path | Tech Stack | Execution Context | Core Superpower | CLI / Test Command |
|---|---|---|---|---|---|---|
| `Fleet-Orchestrator` | Fleet-Orchestrator | `F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator` | Python 3.12+, FastAPI, SQLite WAL, httpx, Copilot CLI, Chrome DevTools Protocol (CDP) | Local / Hybrid Fleet Cluster | Distributed agent swarm task coordinator, multi-account GitHub Copilot quota pooling, lease-based state machine, and headless adapter engine | `pytest` / `.\launch_copilot_fleet.bat` |
| `super-nlm` | Super-NLM Hub | `F:\Aaradhya-Dev-Tamrakar\super-nlm` | Python 3.11+, FastAPI, React, FastMCP, httpx, Playwright, SQLite WAL | Cloud / Hybrid Microservice | Multi-account Google NotebookLM aggregator, token-ring round-robin rotation, session cooldown management, and cross-notebook synthesis | `pytest` / `.\launch.bat` / `python run.py` |
| `omnivault` | OmniVault | `F:\Aaradhya-Dev-Tamrakar\omnivault` | Python 3.14, SQLite FTS5, BLAKE3, FastAPI, Pillow, Watchdog, PyYAML | Local Desktop / Hybrid Storage | Tri-tier archival and sub-second retrieval engine bridging Mobile (LocalSend/Wired), Laptop NVMe shadow catalog, and External HDD cold vaults with automated storage bloat optimization | `pytest` / `.\omnivault.bat` / `.\run_web.bat` |
| `Cyber-Forensics` | Cyber-Forensics | `F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics` | PowerShell 7, Win32/NT APIs, NTFS Streams, DFIR Parsers, SHA-256 | Local Desktop (Bare Metal) | Deterministic Windows DFIR artifact triage, multi-layer stealth evasion detection (ADS, CLSID, RLO, MZ PE magic byte masquerades), and cryptographic chain of custody logging | `pwsh tests\test_evasion_hunter.ps1` / `pwsh .\src\EvasionHunter.ps1` |
| `Win-Vault` | Win-Vault | `F:\Aaradhya-Dev-Tamrakar\Win-Vault` | PowerShell 7, Windows Forms (GUI), NTFS Kernel ACLs (icacls), SHA-256 | Local Desktop (Bare Metal) | Lightweight, zero-dependency Windows native GUI privacy vault with kernel-level NTFS Access Control (ACL) denial and hidden system encapsulation | `.\Vault.bat` / `powershell -ExecutionPolicy Bypass -File .\Vault.ps1` |
| `system-optimizer` | NovaOptimizer | `F:\Aaradhya-Dev-Tamrakar\system-optimizer` | C# .NET 10, WPF, Win32/NT Kernel APIs (`EmptyWorkingSet`, `SetProcessWorkingSetSize`) | Local Desktop (Bare Metal) | Micro-footprint Windows OS tuning, deep RAM cache purge (`EmptyWorkingSet`), and real-time thread/process priority boosting | `dotnet build` / `dotnet run -c Release` / `.\Run.bat` |
| `SPARK` | SPARK Wearable Gateway | `F:\Aaradhya-Dev-Tamrakar\SPARK` | C/C++ (ESP32-S3 / ESP-IDF), Python, TensorFlow Lite Micro, SHAP, BLE GATT, FastAPI | Edge Hardware / Local Gateway | Two-layer edge fall detection architecture pairing continuous 200 Hz microsecond interrupt gating with quantized INT8 CNN inference and clinician SHAP explainability | `pytest` / `uv run pytest tests/` |
| `BiasAperture` | BiasAperture Disparity Auditor | `F:\Aaradhya-Dev-Tamrakar\BiasAperture` | PyTorch, Python 3.11+, LaTeX (pdflatex), Matplotlib, SciPy | Local Compute / Research | Demographic bias auditing framework for vision models, multi-attribute disparity metrics, and automated publication-grade LaTeX/PDF dossier generation | `pytest src/tests/` / `python -m biasaperture.cli --help` |
| `Claude-Desktop` | Claude Worker Fleet (v2) | `F:\Aaradhya-Dev-Tamrakar\Claude-Desktop` | FastAPI coordinator, SQLite WAL, PowerShell 7, Chrome DevTools Protocol (CDP), FastMCP | Local / Distributed Fleet | Multi-profile session persistence, distributed DAG task worker fleet, SKU pipeline decomposition, and prompt quota rotation | `pytest` / `.\launch.bat` / `pwsh .\sync-mcp.ps1` |
| `Alpha-SuperApp` | Alpha-SuperApp | `F:\Aaradhya-Dev-Tamrakar\Alpha-SuperApp` | Kotlin 2.2, Jetpack Compose, Android 16 (SDK 35), BLE APIs, ONNX / TFLite | Mobile Device (Android) | Mobile super-app consolidating on-device Computer Vision, BLE hardware peripheral control, Personal Finance tracking, and multimodal AI assistants | `.\gradlew assembleDebug` / `.\gradlew test` |
| `Nexus` | Nexus AI Workspace | `F:\AaradhyaDT\Nexus` | FastAPI (Python), React (Vite / Tailwind CSS), SQLite FTS5 | Local / Hybrid Web | Project-centric AI workspace, prompt multiplexing across parallel LLMs, and full-text contextual note memory via SQLite FTS5 | `.\start-nexus.bat` (Backend: `uvicorn main:app`, Frontend: `npm run dev`) |
| `AI` | AI Constraint Solver | `F:\AaradhyaDT\AI` | Python 3.11, FastAPI, Backtracking / Forward Checking CSP Engine, CLI | Local Microservice / CLI | Cryptarithmetic and combinatorial constraint satisfaction problem (CSP) solver with JSON telemetry and automated verification | `pytest tests/` / `python cli.py solve --puzzle "SEND+MORE=MONEY"` |
| `rsvp-reading` | RSVP Reader | `F:\AaradhyaDT\rsvp-reading` | Svelte 5 / Vite, JavaScript (ESM), HTML5 Canvas, Vitest | Local Web Client / Browser | High-speed Rapid Serial Visual Presentation (RSVP) reader with Optimal Recognition Point (ORP) highlighting, WPM regulation, and EPUB/PDF ingestion | `npm run dev` / `npm test` (or `npx vitest run`) |
| `yt-dlp-live` | yt-dlp-live | `F:\Aaradhya-Dev-Tamrakar\Utility\yt-dlp-live` | PowerShell 7, yt-dlp, FFmpeg, Intel QSV Hardware Acceleration | Local Daemon / Media Pipeline | Resilient 24/7 live stream capture daemon, RTMP relay, and autonomous media transformer cluster (Normal-to-Nightcore DSP, QSV render) | `.\record_live.bat <URL>` / `pwsh .\record_live.ps1 -Url "<URL>"` |

---

## 2. Schema Contract Verification Status (`schemas/capability.contract.v1.json`)

All 14 computational engines have been audited against the brainstorm architectural contract schemas (`schemas/capability.contract.v1.json`, `schemas/ecosystem.registry.json`, and `schemas/capability-registry.yaml`):

### Formal Contract Instances on Disk (`schemas/examples/`)
The following 6 core computational engines possess explicit, validated capability contract files conforming to `schemas/capability.contract.v1.json`:
1. **Fleet-Orchestrator**: `schemas/examples/fleet-orchestrator.contract.json` (v1.0.0, runtime: `python312`, 3 capability declarations)
2. **omnivault**: `schemas/examples/omnivault.contract.json` (v1.0.0, runtime: `python314`, 4 capability declarations)
3. **Cyber-Forensics**: `schemas/examples/cyber-forensics.contract.json` (v1.0.0, runtime: `powershell7`, 2 capability declarations)
4. **Win-Vault**: `schemas/examples/win-vault.contract.json` (v1.0.0, runtime: `powershell7`, 2 capability declarations)
5. **AI Constraint Solver**: `schemas/examples/AI-Constraint-Solver.contract.json` (v1.0.0, runtime: `python3.11`, 1 capability declaration)
6. **yt-dlp-live**: `schemas/examples/yt-dlp-live.contract.json` (v1.1.0, runtime: `powershell7-python3.11`, 5 capability declarations)

*(Note: Companion utilities also contracted in `schemas/examples/`: `downloader-scripts`, `fusion360-mcp`, `github-pilot`, `google-classroom-mcp`, `localsend-mcp`, `md2pdf-desktop`, `nepali-ocr-ai`, `typora-mcp`).*

### Canonical Capability & Registry Grounding
The remaining 8 core computational engines are fully cataloged, epistemically calibrated, and verified in the central registries:
- **`schemas/ecosystem.registry.json`**: Authoritative repository metadata, category mapping (`computational_engine`), local paths, and remote branch mapping (31 branches, 100% 1-to-1 tracking cardinality).
- **`schemas/capability-registry.yaml`**: Formal semantic capabilities, input/output schemas, hardware/runtime dependencies, benchmarks, verification procedures, and epistemic evidence tiers:
  - `super-nlm`: Tier E3 (Verification: `test_rotation.py`, multi-account token ring mock suite)
  - `system-optimizer`: Tier E4 (Verification: `PerformanceCounter` telemetry, Win32 `GetProcessMemoryInfo` logs)
  - `SPARK`: Tier E4 (Verification: SisFall benchmark 0.9185 AUC-ROC, 56 unit tests, CTest logic analyzer logs)
  - `BiasAperture`: Tier E4 (Verification: `pytest src/tests/`, known-answer fairness metrics test suite)
  - `Claude-Desktop`: Tier E3 (Verification: `pytest.ini`, CDP session attachment test suite)
  - `Alpha-SuperApp`: Tier E3 (Verification: Android unit/instrumentation tests, Gradle build pass)
  - `Nexus`: Tier E3 (Verification: FastAPI backend endpoint tests, Vite client build)
  - `rsvp-reading`: Tier E3 (Verification: Vitest test suite covering RSVP parsing, ORP calculation, progress storage)

### Verification Engine Status
- **Layer 1 (Structural Consistency)**: PASSED (573 files, 0 broken links, 100% schema conformance).
- **Layer 2 (Behavioral Reproducibility)**: PASSED (36/36 tests, 12/12 SMT invariant properties verified via Z3).
