# ARCH-PLAN-001: Commercial Business Plan & Technical Roadmap
## Universal Engineering Protocol: AEC-MCP & Multi-Disciplinary Engineering Fleet

**Document ID:** `ARCH-PLAN-001`  
**Classification:** Strategic Business Plan & Commercial Architecture  
**Author / Founder:** Aaradhya Dev Tamrakar  
**Date:** September 20, 2026  
**Status:** APPROVED / INITIATED  
**Target Markets:** Nepal (TU-IOE & KU Ecosystems, B2B Consultancies) & Global International Engineers  

---

## 1. Executive Summary

The **Universal Engineering Protocol (Eng-MCP)** is a modular, domain-specific suite of Model Context Protocol (MCP) bridges connecting frontier AI models (Claude, Cursor, Antigravity, GPT) directly to industry-standard desktop engineering CAD, FEA, BIM, and simulation environments.

Starting with the fully built and verified **`aec-mcp`** suite (13 local bridges spanning Civil, Architecture, Structural, Water, and GIS), this venture operates on a **Local-First, Zero-Cloud-Cost Bootstrap Model**. By executing tools locally via Windows COM, OAPI, and .NET interop, the operational burn rate is **$0.00/month**, allowing 100% of early subscription revenue to be captured as profit to amass cloud budget for future heavy-compute features.

Monetization utilizes an **Annuity-Based Subscription Model** with dual-rail payment processing:
1. **Domestic Rail (Nepal - NPR):** Fonepay QR, eSewa, and Khalti for student passes and engineering consultancy annual licenses.
2. **Global Rail (International - USD):** Merchant of Record (Polar.sh / Lemon Squeezy) paying out via Payoneer/SWIFT to Nepal bank accounts.

---

## 2. Market Opportunity & Problem Statement

### 2.1 The Engineering Bottleneck
* **Repetitive Manual Tasks:** Practicing engineers spend 60%+ of their billable hours manually transferring structural analysis outputs (e.g. ETABS/SAP2000 member forces) into drafting software (AutoCAD rebar schedules), running code compliance checks, and writing municipal approval reports.
* **Siloed Tool Chains:** Structural software, BIM models, hydraulic calculators, and GIS mapping do not communicate natively.
* **High Learning Curve:** Students and junior engineers struggle with complex software setup and steep domain learning curves across university coursework.

### 2.2 Why AEC is the Perfect Beachhead
* **Legislation-Driven Demand:** In Nepal, every commercial and residential building requires municipal structural dossiers strictly complying with **NBC 105:2020** and **IS 456:2000**.
* **Concentrated Tech Stack:** Over 90% of firms in Nepal and South Asia rely on the exact same stack: **ETABS + SAP2000 + AutoCAD + Excel**.
* **Zero Infrastructure Cost:** Because all these enterprise programs run on Windows desktop workstations, MCP bridges run locally via IPC/COM. The founder incurs zero server or GPU costs.

---

## 3. Product Architecture & Fleet Inventory

The ecosystem is anchored by the **`aec-mcp` Master STDIO Gateway**, routing requests dynamically to 13 specialized engineering bridges:

```
                                  [ AI Client ]
                     (Claude Desktop / Cursor / Antigravity)
                                        │
                                        │ (STDIO Stream + Bearer License Key)
                                        ▼
                           ┌───────────────────────────┐
                           │    aec-mcp Master Gateway  │
                           │  - License Gate (Ed25519) │
                           │  - Dynamic Port Registry  │
                           │  - Process Lifecycle & PID│
                           └─────────────┬─────────────┘
                                         │
     ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
     ▼                   ▼                               ▼                   ▼
┌──────────────┐  ┌──────────────┐                ┌──────────────┐    ┌──────────────┐
│  Structural  │  │  BIM & Archi │                │ Civil/Water  │    │  Parametric  │
│  - sap2000   │  │  - revit-mcp │                │ - epanet-mcp │    │  - rhino-mcp │
│  - staad-mcp │  │  - autocad   │                │ - qgis-mcp   │    │  - sketchup  │
│  - etabs-mcp │  │  - 3dsmax    │                │ - civil3d    │    │  - maya/fus  │
└──────────────┘  └──────────────┘                └──────────────┘    └──────────────┘
```

### 3.1 Live Repository Fleet (100% Passing Tests)

| Discipline | Repository | Integration Mechanism | Key Functionality |
| :--- | :--- | :--- | :--- |
| **Fleet Routing** | `aec-mcp` | STDIO Gateway / Registry | Dynamic port router, license verification, PID health monitoring. |
| **Structural / FEA** | `sap2000-mcp` | CSI SAP2000 OAPI COM | 2D/3D truss generation, FEA frame solving, joint reaction extraction. |
| **Structural Steel** | `staad-mcp` | OpenSTAAD COM | Bentley STAAD.Pro model generation, ISMB/W-shape tables, linear solver. |
| **High-Rise / Seismic** | `etabs-mcp` | CSI ETABS OAPI COM | Story drift verification, diaphragm checks, NBC 105:2020 seismic analysis. |
| **Hydraulics / Water** | `epanet-mcp` | EPA NET C-DLL / CLI | Water distribution network simulation, Hazen-Williams head loss, pressure heads. |
| **Geospatial / Topo** | `qgis-mcp` | QGIS Python API / CLI | DEM elevation profile sampling, parametric contour extraction, DXF export. |
| **Drafting / Civil 3D** | `autocad-mcp` | AutoCAD ActiveX COM | ModelSpace entity drawing, layer control, AutoLISP execution, PDF plotting. |
| **BIM Architecture** | `revit-mcp` | C# .NET AddIn + ExternalEvent | Wall/column authoring, parameter edits, IFC schema export. |
| **Massing & Daylight** | `sketchup-mcp` | Ruby IPC Socket Bridge | 3D pushpull massing, solar daylight and shadow studies. |
| **Computational Archi**| `rhino-mcp` | RhinoCommon & Grasshopper | Parametric geometry baking, viewport frame capture. |
| **Visual Rendering** | `3dsmax-mcp` | Autodesk 3ds Max `pymxs` | Modifier stack automation, Arnold render passes. |
| **Animation / VFX** | `maya-mcp` | Autodesk Maya `cmds` | Polygon primitives, playblast animation capture. |
| **CAD & Fabrication** | `fusion360-mcp` | Fusion 360 C++ / Python | Solid body generation, parametric constraint solver. |

---

## 4. The 4 Universal Engineering Driver Patterns

Every future engineering discipline follows one of these 4 pre-built communication patterns:

```
1. Windows COM / .NET Interop  ──► AutoCAD, Revit, SAP2000, STAAD, ETABS, SolidWorks, ETAP
2. Native Python / C APIs      ──► KiCad (pcbnew), QGIS, 3ds Max, Maya, PyAnsys, Abaqus
3. Headless CLI / File Stream  ──► EPANET (.inp), LTspice (.raw), Wireshark (tshark), Vivado
4. IPC / Socket / REPL Engines ──► MATLAB Engine for Python, Cisco Packet Tracer, QEMU
```

---

## 5. Monetization, Pricing & Payment Rails

### 5.1 Pricing Strategy & Packages

| Package Tier | Scope & Modules | Target Audience | Pricing (NPR) | Pricing (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **Beta / Inner Circle** | Full Access (All 13 Tools) | Close peers, university labs | **FREE / Token-0** | **FREE** |
| **Student Academic Pass** | Coursework Tools (SAP2000, EPANET, QGIS, AutoCAD) | IOE & KU Undergraduates | NPR 2,000 / year | $20 / year |
| **Structural Engineering Suite** | SAP2000, STAAD.Pro, ETABS | Structural Design Consultancies | NPR 18,000 / year | $180 / year |
| **Architectural BIM Suite** | Revit, AutoCAD, SketchUp, Rhino, 3ds Max | Architecture Studios | NPR 20,000 / year | $200 / year |
| **Master AEC Enterprise** | All 13 Tools + Priority Prompt Engine | Multi-disciplinary Firms | NPR 30,000 / year | $299 / year |

### 5.2 Payment Rails Architecture

* **Inbound Payment Problem Solved:**
  * *Nepali Bank Dollar Cards* are outbound-only ($500 limit).
  * **Domestic Solution:** Fonepay Dynamic QR / eSewa / Khalti API integration with automated license key issuance.
  * **Global Solution:** Merchant of Record (Polar.sh / Lemon Squeezy) handles international VAT, credit cards, and compliance, paying out via **Payoneer / SWIFT Wire** into Nepali commercial bank accounts.

---

## 6. Zero-Server Licensing Engine

No complex server infrastructure is required. The licensing system runs on **Offline Cryptographic Verification (Ed25519 Signed JWTs)**:

1. Customer completes payment $\rightarrow$ Secret key generates a signed license string containing:
   ```json
   {
     "licensee": "consultancy@firm.com.np",
     "tier": "AEC_MASTER_ANNUAL",
     "expires": "2027-09-20T00:00:00Z",
     "sig": "3a7f8c9b..."
   }
   ```
2. User places token in their MCP configuration:
   ```json
   {
     "mcpServers": {
       "aec-mcp": {
         "command": "python",
         "args": ["-m", "aec_mcp"],
         "env": {
           "AEC_LICENSE_KEY": "eyJsaWNlbnNlZSI6Li4ufQ=="
         }
       }
     }
   }
   ```
3. `aec-mcp` validates the digital signature locally on startup using the embedded public key. If expired, it halts with a renewal link. **Operating Cost = $0.00**.

---

## 7. Multi-Disciplinary Expansion Roadmap (Eng-MCP)

```
                       [ Eng-MCP Universal Protocol ]
                                     │
         ┌───────────────────┬───────┴───────────┬───────────────────┐
         ▼                   ▼                   ▼                   ▼
    [ aec-mcp ]         [ mech-mcp ]        [ eda-mcp ]        [ embedded-mcp ]
     (Live Now)          (Phase 2)           (Phase 3)            (Phase 4)
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     ┌──────────────┐
  │ Civil, Archi │    │ SolidWorks   │    │ KiCad        │     │ PlatformIO   │
  │ Structural   │    │ Inventor     │    │ Altium       │     │ STM32Cube    │
  │ Water, GIS   │    │ Ansys Mech   │    │ LTspice      │     │ Wireshark    │
  │ 13 Tools     │    │ OpenFOAM     │    │ ETAP / MATLAB│     │ QEMU / GDB   │
  └──────────────┘    └──────────────┘    └──────────────┘     └──────────────┘
```

### 7.1 Nepal Specialized Engineering Verticals
* **Geomatics (WRC Pokhara / KU):** DGN/DXF cadastral parceling, DEM slope classification via `qgis-mcp`.
* **Electrical & Electronics (IOE Pulchowk/Thapathali):** `matlab-mcp`, `proteus-mcp`, `ltspice-mcp`.
* **Mechanical & Automobile (IOE Thapathali):** `solidworks-mcp`, `ansys-mcp`.
* **Mining Engineering (KU Dhulikhel):** Geological rock mechanics and slope stability overlays.

---

## 8. Strategic Execution Milestones

* **Milestone 1 (Week 1–2):** Finalize `aec-mcp` umbrella rebranding, removing legal exposure from `autodesk-mcp`.
* **Milestone 2 (Week 3–4):** Onboard 5–10 senior civil/architecture beta testers from IOE Pulchowk / Thapathali and local consultancies.
* **Milestone 3 (Month 2):** Launch Fonepay/eSewa QR onboarding for Nepal and Lemon Squeezy for international users.
* **Milestone 4 (Month 3–6):** Accumulate initial annuity bootstrap fund; begin prototyping `mech-mcp` (SolidWorks) and `eda-mcp` (KiCad/LTspice).

---

## 9. Developing Market Software Licensing Realities & Air-Gapped Workarounds

In emerging markets like Nepal, a substantial portion of university students, independent draftspersons, and boutique engineering consultancies utilize legacy or patched/cracked installations of enterprise CAD and FEA suites (AutoCAD, Revit, ETABS, SAP2000).

### 9.1 The Problem
When workstations connect to the internet to run frontier AI models (Claude Desktop, Cursor, Antigravity):
* **Autodesk Genuine Service (`AdskLicensingService`)** and **CSI Sentinel RMS License Managers** attempt outbound telemetry pings.
* If unlicensed, the host software flags the installation, displays warnings, or terminates process execution.

### 9.2 The Technical Decoupling (Why MCP Still Works)
* **Local Kernel-Level IPC:** All 13 MCP bridges interact with desktop applications exclusively via **in-memory Windows COM (`win32com.client`)**, **C# .NET ExternalEvents**, or **Localhost (`127.0.0.1`) sockets**.
* **Zero Outbound Exposure:** The MCP bridges never transmit CAD project data, serial numbers, or license states to external servers.
* **The Only Internet Requirement:** Internet connectivity is strictly required by the **AI Client** (Claude/Cursor) to perform LLM inference over HTTPS.

### 9.3 The Strategic & Technical Resolution

1. **Firewall Outbound Isolation (`protect-cad.ps1`):**
   * Provide an optional, automated Windows Defender Firewall helper script that creates outbound block rules specifically for CAD executables (`acad.exe`, `revit.exe`, `Sap2000.exe`, `ETABS.exe`).
   * **Result:** The workstation remains 100% online for AI LLM streaming, while the CAD software remains entirely air-gapped from vendor telemetry servers. Local COM interop continues functioning uninterrupted.
2. **Official Student License Pipeline:**
   * Educational promotion for IOE and KU engineering students (`@ioe.edu.np`, `@ku.edu.np`) to obtain official, 100% free 1-year renewable Autodesk Educational licenses, eliminating fear of vendor lockouts.
3. **Open-Source Core Anchors:**
   * Tools like **EPANET** (US EPA Public Domain) and **QGIS** (OSGeo Open Source) are fully open-source with zero licensing friction or internet deactivation risk.
4. **B2B Consultancy Focus:**
   * Institutional consultancies operating with legitimate licenses experience zero disruption and represent the primary high-ticket annuity target.

