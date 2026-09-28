# Research & Product Plan: Nepal Sovereign Knowledge Graph & IDBFS Ingestion Engine

**ID:** `PLAN-NEP-DATA-001`  
**Date:** 2026-09-28  
**Status:** In Progress / Active Execution  
**Principal Architect:** Aaradhya Dev Tamrakar, Antigravity Agent  
**Context:** Sovereign Intelligence, Legal AI Ingestion, OCR Training Flywheel & Economic Self-Sufficiency  
**Ecosystem Modules Referenced:** `nepali-ocr-ai` (Module #19), `super-nlm` (Module #1), `brainstorm` (Orchestration Root)

---

## 1. Executive Summary & Master Vision

Emerging and frontier markets like Nepal suffer from extreme **information opacity and structural fragmentation**: critical public and private data exists, but it sits isolated across 25 federal ministries, 753 municipalities, scanned paper archives, and disconnected corporate registries.

This plan details the end-to-end architecture for building the **Nepal Sovereign Knowledge Graph**:
1. **Phase 1 (Government & Statutory Substrate):** The Constitution, all ~500 federal Acts, regulations (*नियमावली*), Nepal Gazette (*राजपत्र*), and Supreme Court precedents (*नेकाप*).
2. **Phase 2 (Commercial & Economic Substrate):** Office of Company Registrar (OCR), Public Procurement Tenders (e-GP), NEPSE disclosures, and commercial court filings.
3. **Phase 3 (Physical & Societal Substrate):** Cadastral/GIS maps, infrastructure tenders, university research, and national demographic data.
4. **Phase 4 (Regional Portability & Export):** Exporting the unified ingestion, OCR, and ontology engine to adjacent South Asian and developing regulatory environments (e.g., Bhutan, Bangladesh).

---

## 2. Ingestion Engine Architecture (IDBFS)

To systematically gather all public legal data without getting trapped in deep pagination rabbit holes or exploding memory queues, the crawler implements **Iterative Deepening Breadth-First Search (IDBFS)**:

```
For max_depth = 0 to 3:
    Queue Q = [(seed_urls, depth=0)]
    Visited_d = set()
    
    While Q is not empty:
        pop (url, depth)
        if url in Visited_d: continue
        mark url in Visited_d
        
        # Triage Content
        if is_pdf(url):
            hash = sha256(content)
            if hash not in CorpusStore:
                if has_native_unicode(content):
                    extract_text_direct(content) -> data/corpus_clean/
                else:
                    queue_for_ocr(content)       -> data/ocr_queue/
        
        if depth < max_depth:
            enqueue child_urls with depth + 1 (rate-limited at 1 req/sec per .gov.np domain)
```

### Depth Cutoff Milestones:
- **Depth 0 ($d=0$):** Top-level ministry and commission publication hubs (~100–200 seed endpoints).
- **Depth 1 ($d=1$):** Complete primary statutory framework: Constitution + all ~500 active Federal Acts (~1.2 GB).
- **Depth 2 ($d=2$):** Enabling legislation: Rules, Regulations, and Ministerial Directives (~3,000 files, ~8 GB).
- **Depth 3 ($d=3$):** Interpretive substrate: Supreme Court precedents (*नेकाप*) and extraordinary Gazette supplements.

---

## 3. The `nepali-ocr-ai` Synthetic Training Flywheel

### Current State Audit of `nepali-ocr-ai`
An audit of `F:\Aaradhya-Dev-Tamrakar\Utility\nepali-ocr-ai` reveals:
- **Working Components:** Preeti $\leftrightarrow$ Unicode phonetic transcoder (`transcoder.py`), Varnavinyas grammar/orthography checker (`grammar.py`), OpenXML Word `.docx` font run repair engine (`docx_engine.py`), FastMCP server, and Typer CLI.
- **The Core Gap:** **No neural visual OCR pipeline exists yet.** The vision layer is currently unpopulated.

### The Google Colab Closed-Loop Training Loop
To complete `nepali-ocr-ai` without manual annotation or heavy local GPU heat:

1. **Scraper generates text corpus:** Clean digital text from $d=1$ Acts feeds `legal_sentences.txt` (~5 MB).
2. **Colab generates in-memory synthetics:** 
   - A Colab notebook runs `trdg` (TextRecognitionDataGenerator) using authentic government fonts (Kalimati, Preeti, Kantipur, Kokila).
   - Augments 50,000 patches with photocopy noise, paper bleed, and rotation directly in RAM.
3. **Fine-tuning TrOCR / GOT-OCR-2.0:** 
   - Fine-tunes a vision transformer on Colab T4/A100.
   - Exports compact ONNX/PyTorch weights (`model.safetensors`, ~300 MB) back to Google Drive and local `nepali-ocr-ai`.
4. **Scanned Archive Ingestion:** The trained model transcribes `data/ocr_queue/` (historical Gazettes and scanned cases) into clean, searchable markdown.

---

## 4. Entity Resolution: The Core Defensible Moat

Raw documents are commoditized; interconnected relational entities form the proprietary asset:

```
[Contractor Name / Director]
         │
         ├──> Registered Entity (Office of the Company Registrar)
         │           │
         │           └──> Shareholding & Corporate Officers
         ├──> Bidder in e-GP Tender (Public Procurement Monitoring Office)
         └──> Litigant in Supreme Court Precedent (NKP Judgment Index)
                     │
                     └──> Evaluated against Public Procurement Act, 2063
```

---

## 5. Economic Self-Sufficiency Invariant

To guarantee sustainable progress without speculative burn:
- **Phase 1 Monetization:** B2C study products for SEE/NEB students and Lok Sewa aspirants (NPR 199–499) + B2B legal search subscription for law firms.
- **Phase 2 Monetization:** Corporate compliance, credit risk intelligence, and public tender alert subscriptions for commercial banks, contractors, and investment firms.
- **Phase 3 Monetization:** Enterprise spatial, economic, and infrastructure data for development agencies, insurers, and urban planners.

---

## 6. Safety-First Harvester Invariants

To prevent server disruption on `.gov.np` infrastructure and ensure legal compliance under ETA 2063:

1. **Jittered Domain Politeness:** Enforces a minimum 1.5s – 2.5s randomized delay per domain.
2. **Transparent Identity:** Emits an explicit academic User-Agent header: `KEC-Academic-Research-Bot/1.0 (+http://kec.edu.np; contact: aaradhyadevtmr@gmail.com)`.
3. **Automated Circuit Breaker:** Implements zero-overhead socket liveness checks (`1.1.1.1:53`) and backs off 300s on 429/503 responses or router drops.
4. **Atomic Swapping:** Downloads to `.tmp`, verifies length > 128 bytes and SHA-256 integrity, then performs an atomic OS replace.
5. **Status Detection:** Automatically detects repeal keywords (*“खारेज गरिएको”, “द्वारा खारेज”*) to tag active vs. repealed statutes.
6. **Reference Implementation:** Executable prototype verified in [`sim/nepal_law_harvester.py`](../../sim/nepal_law_harvester.py) and [`sim/test_nepal_law_harvester.py`](../../sim/test_nepal_law_harvester.py) (7/7 tests passing).

---

## 7. 125-Year Bikram Sambat Temporal Engine

Extracted and ported directly from Aaradhya's portfolio engine (`AaradhyaDT.github.io` `assets/js/modules/core.js`):
- **Span:** BS 1975 to 2099 (~AD 1918 to 2043) — 125 continuous years.
- **Zero-Dependency Implementation:** [`sim/nepali_calendar.py`](../../sim/nepali_calendar.py) provides deterministic, $O(1)$ bi-directional conversion between A.D. and B.S. with English and Nepali month names.
- **Validation:** Verified across key milestones (Constitution promulgation `2015-09-20 AD` $\leftrightarrow$ `2072-06-03 BS` and live execution date `2026-09-28 AD` $\leftrightarrow$ `2083-06-12 BS`).

---

## 8. Multi-Node Cluster Topology & 1-Click Worker UX

### Hardware Fleet Roles:
- **Jetson Nano (ARM64 + 512GB SSD):** 5W–10W always-on central data lake, SQLite WAL queue, and Tailscale mesh node.
- **Makerspace Rig 1 (i7-12700K + RTX 3060 12GB):** Heavy CUDA vision OCR training (`nepali-ocr-ai`).
- **Makerspace Rig 2 (i5-12600K + RTX 3050 8GB):** Synthetic dataset rendering and OpenVINO PDF layout analysis.
- **Mac mini (10-Core Apple Silicon):** 15W–35W continuous NLP de-jargonizing via Apple MLX and vector search.
- **Client Fleet (Laptops):** Review, evaluation, and opportunistic domain-sharded scraping.

### 1-Click Autonomous Worker (`worker.bat`):
- Zero-configuration auto-discovery via LAN/UDP beacon.
- Hardware self-profiling (CPU thread count, CUDA availability) for intelligent batch assignment.
- Graceful shutdown with heartbeat expiration and automatic task reclamation.

---

## 9. Self-Healing & Hardware Preservation Protocol

1. **Hardware Longevity:** Enforces a 70% GPU power cap (`nvidia-smi -pl 115`), a 45m/15m compute-rest duty cycle, and max 75°C thermal safety throttling.
2. **Power Outage Resilience:** Desktops set to BIOS `Restore on AC Power Loss = Power On`; Jetson Nano backed by micro-UPS power bank.
3. **Database WAL Checkpointing:** SQLite operating with `journal_mode=WAL` and `synchronous=NORMAL` to guarantee zero database corruption across abrupt power cuts.

