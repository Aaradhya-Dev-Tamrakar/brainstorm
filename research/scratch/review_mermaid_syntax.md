# Mermaid Syntax Review & Conversions

**Reviewer Agent Audit Report**
- Validated node syntax, ensuring labels containing special characters (parentheses, slashes, brackets) are safely enclosed in double quotes (e.g., `id["Label"]`).
- Replaced ASCII multi-line blocks with `<br>` inside Mermaid strings for semantic preservation.
- Ensured arrows and relationships correctly model the original ASCII data flow without broken syntaxes.

---

### Target 1: ARCH-SPEC-005 (Lipikaar-AI Pipeline)
```mermaid
flowchart TD
    in["[ Scanned Document / PDF / Image / Text ]"]
    ocr["Vision OCR Engine<br>- Flash Vision Multimodal<br>- Layout & Bounding Boxes"]
    
    in --> ocr
    ocr -- "Devanagari Unicode Text" --> lint["Hybrid Grammar & Linter<br>1. Deterministic Lexicon<br>   • Varnavinyas (ह्रस्व/दीर्घ)<br>   • Padayoga/Padaviyoga<br>2. LLM Contextual Sugg.<br>   • Adar/Honorific Agree<br>   • Legal/Admin Register"]
    
    lint -- "Linted & Corrected Unicode" --> mode1["Mode 1: Modern Unicode DOCX<br>- Target: Mangal / Kalimati<br>- Proper OpenXML font tags<br>- Universal Searchability"]
    lint --> mode2["Mode 2: Legacy Preeti DOCX<br>- Syllabic AST Transcoder<br>- Prefix matra / reph shift<br>- Injects Preeti font glyphs"]
    
    mode1 --> gen["OpenXML DOCX Generator<br>- Inline Proofing / Marks<br>- Paragraph & Table Styles<br>- Native Word Output"]
    mode2 --> gen
```

### Target 2: ARCH-SPEC-004 (YouTube Transformer Cluster)
```mermaid
flowchart TD
    in["[ Audio / Lyric Ingestion ]<br>(Public Domain / Free / Stems)"]
    
    in --> dsp["[ Normal -> Nightcore DSP Engine ]<br>• Rubberband Pitch/Tempo Stretch<br>• Sub-Bass Saturation (60 Hz punch)<br>• ITU-R BS.1770 (-14 LUFS leveling)"]
    in --> align["[ Alignment & Timing Engine ]<br>• WhisperX Word/Phoneme Timestamps<br>• Syllable Split & Karaoke Generator<br>• SSA/ASS Script Compilation (.ass)"]
    
    dsp --> join1{{" "}}
    align --> join1
    
    join1 -- "Transformed Audio + ASS Subtitles" --> comp["[ Hardware-Accelerated Compositor ]<br>• Intel Core Ultra 7 155H QuickSync (QSV)<br>• Encoders: h264_qsv / av1_qsv (Zero CPU Stall)<br>• Audio-Reactive Visualizer (FFmpeg showwaves/vectorscope)<br>• High-Contrast Vector Background (Kids/Nightcore Aesthetic)"]
    
    comp --> out["[ Validated Video Output ]<br>(1080p60 / 4K MP4 Containers)"]
    
    out --> dispatch["[ Autonomous Dispatch & Relay ]<br>• Scheduled Upload via YouTube Data API v3<br>• RTMP Stream Broadcast via yt-dlp-live Relay Engine<br>• SEO Metadata, Chapters & Thumbnail Injection"]
```

### Target 3: ARCH-SPEC-006 (Fusion 360 MCP Bridge)
```mermaid
sequenceDiagram
    participant Client as "AI Agent Client (Antigravity, Claude Desktop, Cursor)"
    box "Autodesk Fusion 360 Process (Embedded Python Runtime)"
        participant Daemon as "Threaded HTTPServer (Background Daemon Thread)"
        participant MainUI as "Main UI Thread (Single-Threaded CAD Lock Free)"
    end
    
    Client->>Daemon: HTTP POST (JSON-RPC 2.0)
    Note over Daemon: Bound to 127.0.0.1:9876<br>Handles /health (GET) & /mcp (POST)<br>Registers req with threading.Event()<br>app.fireCustomEvent(CUSTOM_EVENT_ID)
    Daemon->>MainUI: CustomEvent Trigger
    Note over Daemon: Blocks on event.wait(timeout=60.0)
    Note over MainUI: MCPCustomEventHandler.notify()<br>Executes CAD commands<br>Captures stdout/error/viewport<br>Sets req['result'] and signals event.set()
    MainUI->>Daemon: event.set() (Signals Worker Thread)
    Note over Daemon: Worker thread unblocks, formats JSON-RPC result
    Daemon->>Client: returns HTTP 200 (JSON-RPC Result)
```

### Target 4: ARCH-SPEC-002 (IPU System Topology)
```mermaid
flowchart TD
    ingress["[ 6G Sub-THz Ingress / High-Speed Sensor Array ]<br>(1 Tbps Burst Stream)"]
    
    subgraph IPU ["THE INGESTION PROCESSING UNIT (IPU)<br>(The Architectural Shock Absorber)"]
        s1["1. Line-Rate Ingestion Buffer & Traffic Shaper<br>• Absorbs multi-gigabit bursts without host CPU/GPU interrupts<br>• Dynamic Bank-Conflict & Jitter Predictor"]
        s2["2. Inline Stream Transform & Reduction Engine (v+2 PIM Logic)<br>• Baseband Channel Estimation & Massive MIMO Matrix Inversion<br>• Semantic Tokenization & Attention Softmax Local Accumulation<br>• Zero-Copy Discard: 99%+ raw entropy reduced at boundary"]
        s3["3. Smart Coalescing & Interconnect Adapter (v+1 Logic)<br>• Translates scattered payloads into optimal 64B cacheline bursts<br>• Presents a standard, legacy-compliant CXL / PCIe / AXI-4 face"]
        
        s1 -- "Filtered Stream" --> s2
        s2 -- "Clustered Bursts" --> s3
    end
    
    subgraph Host ["LEGACY HOST SUBSYSTEM"]
        h1["[ Host GPU / Vortex RISC-V Cores ] ── [ Commodity DDR5 / HBM Memory ]<br>(Zero hardware changes required; operates unthrottled on digested data)"]
    end
    
    ingress --> s1
    s3 -- "Pristine, Low-Bandwidth Semantic Payloads<br>(PCIe 5.0/6.0, CXL 3.0, or AXI-4)" --> h1
```

### Target 5: SPARK README.md
```mermaid
flowchart TD
    subgraph Wearable ["WEARABLE NODE (ESP32-S3)"]
        imu["MPU6050 6-DOF<br>IMU @ 200 Hz"]
        l1["[Layer 1: Pre-Impact Gate]<br>|a| > 2.5g, Δt < 300 ms (Host-testable C/C++)"]
        l2["[Layer 2: Edge ML Classifier]<br>Quantized 1D CNN on TFLite Micro (spark_cnn_int8.h)"]
        
        imu --> l1
        l1 -- "(Triggered: Motion Window)" --> l2
    end
    
    subgraph Gateway ["LOCAL GATEWAY (Laptop / Local Server)"]
        recv["[BleReceiver / Replay / Serial]"]
        json["[JSON Store]"]
        shap["[SHAP Attribution Engine]"]
        pdf["[ReportLab Clinical PDF Report]"]
        api["[Gateway REST API & Embedded Web Dashboard Server]<br>(gateway/server.py)"]
        
        recv --> json
        json --> shap
        shap --> pdf
        pdf --> api
    end
    
    subgraph Client ["DISPLAY CLIENT (Smartphone / Web UI)"]
        dash["Layer 3 Read-Only Responsive Dashboard<br>(Live Alert Feed & Clinical PDF Viewer)"]
    end
    
    l2 -- "BLE Notification (WIRE_FORMAT_v1)" --> recv
    api -- "Local Network (HTTP / REST)" --> dash
```

### Target 6: BiasAperture (Conditional SHAP Pipeline)
```mermaid
flowchart TD
    row["Metric Result Row"]
    flag{"[ Is Disparity Flagged? ]<br>(p < 0.05 AND n >= 30)"}
    skip["Skip SHAP (Zero overhead)"]
    exp["[ Explainer Strategy ]"]
    
    p_exp["PartitionExplainer<br>(Black-Box Default)"]
    g_exp["GradientExplainer<br>(In-Process PyTorch Fast-Path)"]
    
    parse["[ Pretrained Face Parsing (BiSeNet) ]"]
    attr["[ Spatial Attribution Shift + ITA ]"]
    vis["[ Inlined Base64 PNG Visualization ]"]
    
    row --> flag
    flag -- "NO" --> skip
    flag -- "YES" --> exp
    
    exp --> p_exp
    exp --> g_exp
    
    p_exp --> parse
    g_exp --> parse
    
    parse --> attr
    attr --> vis
```

### Target 7: super-nlm telecom_guide.md (SS7 Protocol Stack)
```mermaid
flowchart TB
    app["Application Layer: TCAP, MAP, INAP, CAMEL"]
    cc["Call Control: ISUP (ISDN User Part) / TUP (Tel User)"]
    sccp["SCCP (Signaling Connection Control Part - Global Title)"]
    mtp3["MTP-3 (Message Transfer Part Level 3: Routing/Network)"]
    mtp2["MTP-2 (Message Transfer Part Level 2: Link HDLC/FCS)"]
    mtp1["MTP-1 (Message Transfer Part Level 1: Physical E1/V.35)"]
    
    app --- cc --- sccp --- mtp3 --- mtp2 --- mtp1
```

### Target 8: super-nlm is_guide.md (ERP, SCM, CRM Matrix)
```mermaid
flowchart TD
    sup["[ SUPPLIERS ]"]
    erp["ENTERPRISE RESOURCE PLANNING (ERP)<br>- Financials & Accounting<br>- Production Planning<br>- Human Capital Management<br>- Inventory / Warehouse"]
    cust["[ CUSTOMERS ]"]
    
    sup -- "( SCM Pipeline )" --> erp
    erp -- "( CRM Channels )" --> cust
```
