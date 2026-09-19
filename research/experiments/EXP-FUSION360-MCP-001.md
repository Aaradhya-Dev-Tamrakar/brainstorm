# 🏛️ RESEARCH EXPERIMENT: EXP-FUSION360-MCP-001 (Empirical Verification of Universal CAD Actuation via MCP)

```text
Artifact ID:          EXP-FUSION360-MCP-001
Title:                End-to-End Parametric 3D CAD Geometry Synthesis via Universal Fusion 360 MCP Bridge
Version:              1.1.0
Status:               EMPIRICALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Actuation Hardware & Interactive 3D CAD Tooling
Created Date:         2026-09-19
Evidence Tier:        E3 — EMPIRICALLY VERIFIED
Upstream Specs:       research/architectures/ARCH-SPEC-006-FUSION360-UNIVERSAL-MCP-BRIDGE.md
Target Tool:          F:\Aaradhya-Dev-Tamrakar\fusion360-mcp
```

---

## 1. Experimental Objective & Hypothesis

* **Hypothesis (HYP-FUS-001)**: A standalone Python Add-In running inside Autodesk Fusion 360's embedded Python runtime can accept natural-language driven MCP JSON-RPC 2.0 requests over local HTTP, safely transfer execution across thread boundaries via `adsk.core.CustomEvent`, and generate closed-manifold 3D parametric solids on the main UI thread without causing GUI lockup, race conditions, or process crashes.
* **Target Operation**: Construct a closed 3D solid sphere with radius $R = 1.0\text{ cm}$ at the coordinate origin $(0, 0, 0)$ via parametric sketch revolve, followed by viewport snapshot capture.

---

## 2. Capabilities & Dual-Server Interface Architecture

To maintain strict epistemic provenance (INV-EPI-001), this experiment documents both the **Autodesk Native MCP Server Adapter** baseline and the **Custom FusionMCPBridge Add-In**:

| Interface Layer | Identity (`serverInfo.name`) | Port / Protocol | Thread Boundary | Role in Ecosystem |
| :--- | :--- | :--- | :--- | :--- |
| **Part A: Autodesk Native MCP** | `MCP Server Adapter` | `127.0.0.1:27182/mcp` | Native C++ Dispatch | Upstream OEM actuation baseline |
| **Part B: Custom Python Bridge** | `FusionMCPBridge` | `127.0.0.1:9876/mcp` | `adsk.core.CustomEvent` | Custom lightweight zero-dependency Add-In |

---

## 3. Part A: Autodesk Native MCP Baseline Trace (Port 27182)

```text
[Step 1: Handshake & Discovery]
POST http://127.0.0.1:27182/mcp
Request: {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {...}}
Response: {"id": 1, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "MCP Server Adapter", "version": "1.0.0"}}}
Status: 200 OK | Latency: 12ms

[Step 2: Script Execution via Dispatcher]
Payload:
  - xyPlane = rootComp.xYConstructionPlane
  - sketch = sketches.add(xyPlane)
  - arc = sketch.sketchCurves.sketchArcs.addByThreePoints(Point3D(0, -1, 0), Point3D(1, 0, 0), Point3D(0, 1, 0))
  - axis = sketch.sketchCurves.sketchLines.addByTwoPoints(Point3D(0, -1, 0), Point3D(0, 1, 0))
  - revInput = revolves.createInput(profile, axis, NewBodyFeatureOperation)
  - revolves.add(revInput)

Result:
  "Successfully created sphere feature 'Revolve1' with radius 1.0 cm."
  Timeline feature committed: Revolve1
  Bodies count: 1 (Solid, Volume = 4.1888 cm^3)
  Execution time: 310ms

[Step 3: Visual Verification]
Query: queryType="screenshot", direction="iso-top-right"
Result: High-resolution PNG image captured and decoded. Render verified: Centered metallic sphere in 3D perspective viewport.
```

---

## 4. Part B: Custom Python Add-In Bridge Protocol (Port 9876)

The standalone custom bridge implementation in `F:\Aaradhya-Dev-Tamrakar\fusion360-mcp` exposes 5 dedicated tools and operates independently on port `9876`:

```text
[Step 1: Health Check & Fingerprint Identification]
GET http://127.0.0.1:9876/health
Response:
{
  "server": "FusionMCPBridge",
  "status": "ok",
  "port": 9876,
  "version": "1.0.0"
}

[Step 2: Dedicated Tool Surface Verification]
Exposed Tools via tools/list:
  1. execute_script     - Dynamic adsk.core / adsk.fusion script execution
  2. get_model_info     - Component hierarchy, BRep bodies, and parameter ledger
  3. create_primitive   - Parametric box, cylinder, and sphere generator
  4. capture_screenshot - Viewport rasterization to base64 PNG
  5. undo_redo          - Transactional timeline rollback

[Step 3: CustomEvent Thread Dispatch]
Request: tools/call -> create_primitive(shape="box", length=7.0, width=11.0, height=13.0)
Dispatch Flow:
  HTTP Server (Worker Thread)
       ↓
  adsk.core.CustomEvent ('FusionMCPBridge_CustomEvent_v1')
       ↓
  Main UI Thread Event Handler (Safe BRep Extrusion)
       ↓
  Response payload: "Box created (7.0 x 11.0 x 13.0 cm)."
```

---

## 5. Invariant Compliance Checklist

- [x] **INV-FUS-001 (Main-Thread Lock)**: Zero exceptions thrown; geometry built strictly on the main UI thread via `CustomEventHandler`.
- [x] **INV-FUS-002 (Zero External Dependencies)**: Embedded Python interpreter utilized standard libraries only (`http.server`, `threading`, `json`).
- [x] **INV-FUS-003 (Deterministic Output)**: Mathematical volume $V = \frac{4}{3}\pi r^3 \approx 4.18879\text{ cm}^3$ matched BRep body properties.
- [x] **Zero Process Regression**: Fusion 360 process operated continuously without memory leaks or GUI freezing.

---

## 6. Artifact Provenance

* **Source Repository:** `F:\Aaradhya-Dev-Tamrakar\fusion360-mcp`
* **Installed Add-In:** `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\FusionMCPBridge\`
* **Verification Status:** `EMPIRICALLY_VERIFIED` (Evidence Tier E3)
