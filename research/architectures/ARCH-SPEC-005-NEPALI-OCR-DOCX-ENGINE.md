# ARCH-SPEC-005: Nepali OCR & Font-Agnostic Word Automation Substrate (Lipikaar-AI)

> **Artifact ID:** `ARCH-SPEC-005`  
> **Title:** Nepali OCR & Font-Agnostic Word Automation Substrate (Lipikaar-AI)  
> **Version:** `1.0.0`  
> **Status:** `PROPOSED`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Multimodal OCR, Computational Linguistics & Document Automation  
> **Domain:** Devanagari Unicode Normalization, Legacy Glyph Transcoding & OpenXML Engineering  
> **Created Date:** 2026-09-15  
> **Evidence Tier:** `E1`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\brainstorm`  
> **Execution Context:** Antigravity / Python CLI / OpenXML  
> **Upstream Trace:** [`schemas/capability.contract.v1.json`](../../schemas/capability.contract.v1.json), [`schemas/capability-registry.yaml`](../../schemas/capability-registry.yaml)  
> **Downstream Trace:** `lipikaar-ai` CLI, Word Automation, Document Repair Service  

---

## 1. Executive Summary & Problem Space

In administrative, legal, public sector, and educational institutions across Nepal, Devanagari document processing is crippled by a thirty-year historical fracture between **Legacy ASCII Font Hacks** (Preeti, Kantipur, Himali, Sagarmatha) and **Standard Unicode Devanagari** (Kalimati, Mangal, Kokila, Noto Sans).

```
+--------------------------------------+        +--------------------------------------+
| Legacy ASCII Font Hacks (Preeti)     |        | Modern Unicode Devanagari (Kalimati) |
| - Character: 8-bit Latin codepoints  |   VS   | - Character: UTF-8 Devanagari block  |
| - "g]kfnL" renders visually as नेपाली|        | - "नेपाली" stored as \u0928\u0947... |
| - Search, NLP, and AI break 100%     |        | - Searchable, native AI NLP ready    |
| - Required by many Govt/Law offices  |        | - Rejected by legacy Word templates  |
+--------------------------------------+        +--------------------------------------+
```

### Core Impediments
1. **Visual Glyph Ordering vs. Phonetic Ordering**:
   - In Preeti, prefix vowel signs (ि / l), rephs (र् / {), and post-subscripts are typed in visual display order (typing l *before* the consonant).
   - In Unicode, matras and conjuncts follow logical phonetic ordering (Consonant + Halanta + Consonant + Matra).
2. **Scanned Documents & OCR Degradation**:
   - Legacy government documents and legal notices are often faint photocopies or noisy scans.
   - Traditional OCR (e.g. uncalibrated Tesseract) chokes on fused Devanagari ligatures (e.g., क्ष, त्र, ज्ञ, द्ध, द्य, श्र, दृ).
3. **Word Document (.docx) Corruption**:
   - Existing web converters break tables, headers, footers, and inline mixed-language runs (e.g., English names or numbers mixed with Devanagari).

---

## 2. System Architecture: Lipikaar-AI Pipeline

```
                                  [ Scanned Document / PDF / Image ]
                                                  |
                                                  v
                                    +---------------------------+
                                    | Vision OCR Engine         |
                                    | - Flash Vision Multimodal |
                                    | - Layout & Bounding Boxes |
                                    +-------------+-------------+
                                                  | Clean Devanagari Unicode Text
                                                  v
                                    +---------------------------+
                                    | Phonetic & Grammar Check  |
                                    | - Legal & Admin Lexicon   |
                                    | - Halanta / Matra Linting |
                                    +-------------+-------------+
                                                  | Normalized Unicode
                   +------------------------------+------------------------------+
                   v                                                             v
    +-----------------------------+                               +-----------------------------+
    | Mode 1: Modern Unicode DOCX |                               | Mode 2: Legacy Preeti DOCX  |
    | - Target: Mangal / Kalimati |                               | - Bidirectional Mapping     |
    | - Proper OpenXML font tags  |                               | - Prefix matra / reph shift |
    | - Universal Searchability   |                               | - Injects Preeti font glyphs|
    +--------------+--------------+                               +--------------+--------------+
                   |                                                             |
                   +------------------------------+------------------------------+
                                                  v
                                    +---------------------------+
                                    | OpenXML DOCX Generator    |
                                    | - Paragraph Styles        |
                                    | - Preserved Table Layouts |
                                    | - Native Word Output      |
                                    +---------------------------+
```

---

## 3. Core Functional Invariants

1. **`INV-NEP-001` (Round-Trip Determinism):**  
   Converting Unicode Devanagari -> Preeti -> Unicode must guarantee >= 99.8% character fidelity on standard Nepali lexical dictionaries without ligature loss.
2. **`INV-NEP-002` (Style & Layout Preservation):**  
   Repairing an existing mixed-font `.docx` document must mutate solely the character runs and font definitions (`w:rFonts`), preserving all table column widths, line spacings, margins, and headings.
3. **`INV-NEP-003` (Headless First):**  
   All OCR, conversion, and Word compilation features must be completely executable through a headless CLI/Python API before any GUI wrapper is attached.

---

## 4. Verification & Milestone Roadmap

- **Phase 1 (Rules & Bi-directional Transcoder Core):** Zero-token Python module mapping Unicode <-> Preeti with ligature inversion unit tests.
- **Phase 2 (OpenXML DOCX Repair Engine):** Inspect `.docx` XML trees, isolate text runs, detect source encoding, and apply in-place font transcoding.
- **Phase 3 (Vision OCR Ingestion Pipeline):** Multimodal document ingestion with layout reconstruction and automated Word export.
