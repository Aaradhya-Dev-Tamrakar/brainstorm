# ARCH-SPEC-005: Nepali OCR, Grammar Checker & Font-Agnostic Word Substrate (Lipikaar-AI)

> **Artifact ID:** `ARCH-SPEC-005`  
> **Title:** Nepali OCR, Grammar Checker & Font-Agnostic Word Substrate (Lipikaar-AI)  
> **Version:** `1.1.0`  
> **Status:** `PROPOSED`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Multimodal OCR, Computational Linguistics & Document Automation  
> **Domain:** Devanagari Unicode Normalization, Rule/LLM Grammar Verification & OpenXML Engineering  
> **Created Date:** 2026-09-15  
> **Evidence Tier:** `E1`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\brainstorm`  
> **Execution Context:** Antigravity / Python CLI / OpenXML  
> **Upstream Trace:** [`schemas/capability.contract.v1.json`](../../schemas/capability.contract.v1.json), [`schemas/capability-registry.yaml`](../../schemas/capability-registry.yaml)  
> **Downstream Trace:** `lipikaar-ai` CLI, Word Automation, Grammar Linter & Document Repair Service  

---

## 1. Executive Summary & Problem Space

In administrative, legal, public sector, and educational institutions across Nepal, Devanagari document processing is crippled by two compounding fractures:
1. **Legacy Font Incompatibility**: The thirty-year historical split between **Legacy ASCII Font Hacks** (Preeti, Kantipur, Himali) and **Standard Unicode Devanagari** (Kalimati, Mangal).
2. **Grammar & Orthographic Chaos (वर्णविन्यास र व्याकरण समस्या)**:
   - Frequent confusion between **ह्रस्व** (short vowel, e.g. `ि`, `ु`) vs **दीर्घ** (long vowel, e.g. `ी`, `ू`).
   - Sibilant consonant confusion: `श` (तालव्य), `ष` (मूर्धन्य), and `स` (दन्त्य).
   - Word boundary / joint-word conventions (**पदयोग र पदवियोग**): e.g., `गरिसकेपछि` vs `गरि सके पछि`, postpositions (*विभक्ति* like `ले`, `लाई`, `मा`, `को`).
   - Subject-Verb Agreement (**लिङ्ग, वचन, पुरुष र आदर अनुसार क्रियापदको सङ्गति**): e.g., *उनी जान्छन्* vs *उनी जान्छिन्* vs *उहाँ जानुहुन्छ*.

Existing spelling tools either only support Hindi or lack context-aware modern Nepali orthographic standards (नेपाल प्रज्ञा-प्रतिष्ठान नियम).

---

## 2. System Architecture: Lipikaar-AI Pipeline

```
                                  [ Scanned Document / PDF / Image / Text ]
                                                     |
                                                     v
                                       +---------------------------+
                                       | Vision OCR Engine         |
                                       | - Flash Vision Multimodal |
                                       | - Layout & Bounding Boxes |
                                       +-------------+-------------+
                                                     | Devanagari Unicode Text
                                                     v
                                       +---------------------------+
                                       | Hybrid Grammar & Linter   |
                                       | 1. Deterministic Lexicon  |
                                       |    • Varnavinyas (ह्रस्व/दीर्घ) |
                                       |    • Padayoga/Padaviyoga  |
                                       | 2. LLM Contextual Sugg.   |
                                       |    • Adar/Honorific Agree |
                                       |    • Legal/Admin Register |
                                       +-------------+-------------+
                                                     | Linted & Corrected Unicode
                      +------------------------------+------------------------------+
                      v                                                             v
       +-----------------------------+                               +-----------------------------+
       | Mode 1: Modern Unicode DOCX |                               | Mode 2: Legacy Preeti DOCX  |
       | - Target: Mangal / Kalimati |                               | - Syllabic AST Transcoder   |
       | - Proper OpenXML font tags  |                               | - Prefix matra / reph shift |
       | - Universal Searchability   |                               | - Injects Preeti font glyphs|
       +--------------+--------------+                               +--------------+--------------+
                      |                                                             |
                      +------------------------------+------------------------------+
                                                     v
                                       +---------------------------+
                                       | OpenXML DOCX Generator    |
                                       | - Inline Proofing / Marks |
                                       | - Paragraph & Table Styles|
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
   All OCR, grammar linting, font conversion, and Word compilation features must be completely executable through a headless CLI/Python API before any GUI wrapper is attached.
4. **`INV-NEP-004` (Grammar Suggestion Transparency):**  
   Grammar checking must categorize suggestions explicitly into deterministic rule violations (ह्रस्व/दीर्घ, पदयोग) versus stylistic/honorific improvements, preserving original text if auto-apply is false.

---

## 4. Verification & Milestone Roadmap

- **Phase 1 (Rules & Bi-directional Transcoder Core):** Zero-token Python module mapping Unicode <-> Preeti with ligature inversion unit tests.
- **Phase 2 (Varnavinyas & Grammar Linting Engine):** Hybrid rule-based Nepali spell/grammar checker with Pragya-Pratishthan orthographic rules + local/cloud LLM contextual suggestions.
- **Phase 3 (OpenXML DOCX Repair & Proofing Engine):** Inspect `.docx` XML trees, transcode fonts, and optionally inject Word comment/highlight suggestions.
- **Phase 4 (Vision OCR Ingestion Pipeline):** Multimodal document ingestion with layout reconstruction and automated Word export.
