# 🏛️ RESEARCH EXPERIMENT: EXP-REA-001 (Multi-Target Ecosystem Reverse Engineering via REA Swarm)

```text
Artifact ID:          EXP-REA-001
Title:                Multi-Target Ecosystem Reverse Engineering & Binary Verification via REA Swarm
Version:              1.0.0
Status:               EMPIRICALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Binary Diagnostics, Agent Runtimes & Customization Governance
Created Date:         2026-10-17
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED
Hub Conversation ID:  cf230d88-340f-48ec-bc32-f0bf96c8069d
Target Repository:    F:\AaradhyaDT\rea (v6.5.0, npm@11.16.0, Node.js v26.3.1)
```

---

## 1. Executive Summary & Verification Matrix

Four concurrent dedicated agent conversations were executed in parallel using the Reverse Engineer Anything (`rea-agents` v6.5.0) engine across distinct ecosystem targets:
1. **GitHub Copilot CLI Subsystem & Worker Runtime** (`copilot.EXE` + `@github/copilot` v1.0.65)
2. **Antigravity IDE Control Plane & Language Server Bridge** (`Antigravity.exe` + `app.asar`)
3. **Desktop MCP Targets** (`Typora.exe` + Claude Desktop MSIX package)
4. **Compiled Ecosystem Artifacts** (`NovaOptimizer.dll` .NET 8 vs .NET 10 + `Alpha-SuperApp` APK)

| Target Artifact | Primary REA Tool(s) | Observed Format / Runtime | SHA-256 Digest | Primary Empirical Discovery |
| :--- | :--- | :--- | :--- | :--- |
| `copilot.EXE` | `inspect_pe_resources`, `inspect_rust_binary` | PE32+ x86_64, Node SEA + Rust shims | `23e44448b2589401081aa90ee04201fa4b17e4e36d2ac2a10f57e5e1a317cc54` | 67.3 MB `NODE_SEA_BLOB` (Resource 10), Rust shims (`rustc 48a229ce...`), 31 undocumented `COPILOT_*` env vars, `--headless --stdio`, SQLite `session-store.db` schema. |
| `Antigravity.exe` | `inspect_electron_fuses`, `analyze_javascript_application` | Electron PE x86_64 + ASAR bundle | `045a622bb57e7fcdceaafe37e561d53a48353c0e227cbb045e653df448c856b3` | Fuses: `RunAsNode: 1`, `EnableNodeCliInspectArguments: 1`, `EnableEmbeddedAsarIntegrityValidation: 0`. Undocumented `mcp_config.json` keys: `timeoutSeconds`, `mcpMaxOutputBytes`, `enabledTools`. |
| `Typora.exe` | `inspect_electron_fuses`, `analyze_javascript_application` | Electron PE x86_64 + ASAR bundle | `3a1807daf4f0f9e8d1257fac5f61429e9535debf230ffece8b7d931749108a57` | `EnableNodeCliInspectArguments: 0` (explaining CLI `--inspect` failures), but `EnableNodeOptionsEnvironmentVariable: 1` enables `NODE_OPTIONS` preload bypass. Extracted `JSBridge.invoke` IPC map. |
| `NovaOptimizer.dll` | `inspect_managed_artifact`, `compare_managed_members` | PE32 / CLI (.NET 8.0 vs .NET 10.0) | `6e1bca44...` (.NET 8) vs `76c223c8...` (.NET 10) | 503 unchanged, 380 changed, 14 added members (C# 13 `InlineArrayAsReadOnlySpan`, `TurboBoostService.SetPowerPlan`). Verified all 30 Win32 P/Invoke imports. |
| `app-debug.apk` | `inspect_artifact`, `project_android_application_graph` | Android ZIP/DEX (Multi-DEX, 14 DEX, 11 .so) | `715cddbb7880e3250ae6d40b6f3b46159d3d2af0d0ef48b05644234ed62d6d1a` | 684 central directory nodes, 154 JNI bridge candidates. Caught missing `libmediapipe_tasks_vision_jni.so` in `x86_64` slice. |

---

## 2. Granular Target Dissections

### 2.1 Fleet-Orchestrator Worker Runtime (`copilot.EXE` & `@github/copilot`)
- **Conversation Anchor:** [ae0cd08a-0145-475f-8dec-e4d24882d6fc](conversation://ae0cd08a-0145-475f-8dec-e4d24882d6fc)
- **Source Artifact:** `copilot_re_findings.md`
- **Architecture**:
  - The standalone binary `copilot.EXE` (~154 MB) embeds a 67,369,747-byte Node.js Single Executable Application blob (`RT_RCDATA` resource ID `10`).
  - Bundled auxiliary binaries: Ripgrep v14 (`rg.exe`, 5.4 MB) and semantic AST search engine (`tgrep.exe`, 4.65 MB).
  - Rust component confirmed at offset `161278647` matching commit `48a229ceaefd4985c50990b14116b6d856af0985`.
- **Fleet-Orchestrator Invariants Upgraded**:
  - Headless stdio execution: `--headless --stdio` provides direct structured JSON-RPC piping without pseudo-TTY terminal escape sequence parsing.
  - Process isolation switches: `COPILOT_ALLOW_ALL=true`, `COPILOT_FORCE_WINDOWS_HIDE=1`, `COPILOT_DEBUG_SKIP_LAUNCH_CHECKS=1`, and `--disallow-temp-dir`.
  - Quota telemetry: Real production row in `session-store.db` confirmed billing units recorded as `total_nano_aiu` with rate limits classified as `user_weekly_rate_limited`, `user_model_rate_limited`, or `user_global_rate_limited`.

### 2.2 Antigravity IDE Control Plane & Language Server Bridge
- **Conversation Anchor:** [f978e64b-fc04-4790-b978-a805c508e050](conversation://f978e64b-fc04-4790-b978-a805c508e050)
- **Source Artifact:** `antigravity_re_findings.md`
- **Fuses Matrix**:
  - `RunAsNode: ENABLED (0x31)`
  - `EnableNodeCliInspectArguments: ENABLED (0x31)`
  - `EnableEmbeddedAsarIntegrityValidation: DISABLED (0x30)`
  - `OnlyLoadAppFromAsar: DISABLED (0x30)`
- **Configuration Protobuf Extensions (`language_server.exe`)**:
  - `mcp_config.json` exposes native `timeoutSeconds: uint32` (default 60s), `mcpMaxOutputBytes: uint32` (default 1MB), `forceAllToolsEager: bool`, `enabledTools: string[]`, `disabledTools: string[]`, and `authProviderType: "AUTH_PROVIDER_TYPE_GOOGLE_CREDENTIALS"`.
  - Stdio lifecycle hooks (`~/.gemini/config/hooks.json`) validate protojson events for `PreToolUse`, `PostToolUse`, `PreTurn`, `PostTurn`, and `StopResult`.

### 2.3 Desktop MCP Targets (Typora & Claude Desktop)
- **Conversation Anchor:** [d6af067e-6db8-4984-af54-95f1bf027d2a](conversation://d6af067e-6db8-4984-af54-95f1bf027d2a)
- **Source Artifact:** `desktop_mcp_re_findings.md`
- **Typora Inspection**:
  - Explains why CLI `--inspect` flags were failing: fuse `EnableNodeCliInspectArguments` is disabled (`0x30`).
  - Identified reliable bypass: fuse `EnableNodeOptionsEnvironmentVariable` is enabled (`0x31`) and `EnableEmbeddedAsarIntegrityValidation` is disabled (`0x30`), allowing runtime inspection attachment via `NODE_OPTIONS="--inspect=9229"`.
  - Recovered IPC channels for PDF rendering (`export.printToPDF`, `export.genPrintView`) and live in-memory AST mutations (`doc.syncChange`, `document.syncFullContent`, `File.editor.nodeMap`).
- **Claude Desktop MSIX Inspection**:
  - Package `Claude_pzs8sxrjxfjjc` enforces integrity (`EnableEmbeddedAsarIntegrityValidation: 0x31`, `EnableNodeOptionsEnvironmentVariable: 0x30`).
  - Extracted full Zod `AppConfigSchema` (`isCoworkSdkDebuggingEnabled`, `isUsingBuiltInNodeForMcp`, `coworkUserFilesPath`, `extensionId`) and `directMcpHost.js` utility-process lifecycle.

### 2.4 Compiled Ecosystem Artifacts (NovaOptimizer & Alpha-SuperApp)
- **Conversation Anchor:** [5e150d14-042e-4a1d-b40e-b1c3d340608a](conversation://5e150d14-042e-4a1d-b40e-b1c3d340608a)
- **Source Artifact:** `compiled_artifacts_re_findings.md`
- **NovaOptimizer Evolution**:
  - Verified 973 managed member items between .NET 8.0 and .NET 10.0 builds. Confirmed legacy hung-process UI kill handlers removed in favor of headless watchdog tracking.
  - Verified all 30 Win32 P/Invoke boundaries (`psapi.dll!EmptyWorkingSet`, `kernel32.dll!SetProcessWorkingSetSize`, `ntdll.dll!NtSetSystemInformation`).
- **Alpha-SuperApp Defect Detection**:
  - Projected application graph (`adp_7447b94...`) revealed `libmediapipe_tasks_vision_jni.so` exists in `arm64-v8a`, `armeabi-v7a`, and `x86`, but is absent from `x86_64`, which would cause `UnsatisfiedLinkError` on standard 64-bit Android Studio emulators.

---

## 3. Epistemic Classification

- **Classification:** `TIER 2: EMPIRICALLY_VERIFIED`
- **Reproducibility:** 100% deterministic local tool execution via REA v6.5.0 on Node.js v26.3.1. All file paths, hashes, and symbol offsets authenticated against live host storage.
