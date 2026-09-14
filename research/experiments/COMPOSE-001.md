# 🏛️ RESEARCH EXPERIMENT: COMPOSE-001 (High-Bandwidth Rapid Learning Loop)

```text
Artifact ID:          COMPOSE-001
Title:                Two-Capability Composition: Super-NLM Synthesis to Publication PDF
Version:              1.0.0
Status:               LOCALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Multi-Capability Chaining & Tool Interoperability
Created Date:         2026-09-15
Evidence Tier:        E3 — LOCALLY VERIFIED
Upstream Specs:       schemas/capability-ontology.md, schemas/capability-registry.yaml
Composition Pipeline: Super-NLM (Orchestration) ──> md2pdf-desktop (Presentation)
```

---

## 1. Input Specification

* **Input Data:** 5 dense academic PDF papers on CXL 3.0 pooled memory architectures (totaling 142 pages, ~85,000 words).
* **Objective:** Produce a structured, publication-quality 4-page executive synthesis report covering latency bounds, coherency protocols, and memory pooling topologies.

---

## 2. Capabilities Selected

| Capability ID | Role in Workflow | Repository / Location | Interface Invoked |
| :--- | :--- | :--- | :--- |
| **`super-nlm`** | Multi-document cross-synthesis and citation extraction | `F:\Aaradhya-Dev-Tamrakar\super-nlm` | FastMCP (JSON-RPC over stdio) |
| **`md2pdf-desktop`** | Publication-quality PDF compilation with KaTeX/Pandoc | `F:\Aaradhya-Dev-Tamrakar\md2pdf-desktop` | Python CLI (`md2pdf --template academic`) |

### Rationale for Selection
* **Why `super-nlm`:** Directly leverages NotebookLM's grounded source attribution to prevent hallucinated citations across large multi-paper corpora, routing through token ring rotation to avoid individual account quota fatigue.
* **Why `md2pdf-desktop`:** Bypasses manual document formatting; compiles raw Markdown synthesis containing LaTeX mathematical formulations into IEEE-styled multi-column PDF in under 3 seconds.

---

## 3. Interface Contract & Data Exchange

```text
[Raw PDF Corpus]
       ↓ (HTTP / Ingestion)
[Super-NLM Hub] ──(FastMCP stdio JSON-RPC query)──> {"query": "Synthesize CXL 3.0 pooling latency bounds..."}
       ↓
[Structured Markdown Response with KaTeX formulas & citations]
       ↓ (File I/O Hand-off: /tmp/cxl_synthesis.md)
[md2pdf-desktop CLI] ──(Command execution)──> `python md2pdf.py /tmp/cxl_synthesis.md -o /reports/cxl_synthesis.pdf`
       ↓
[Compiled Academic PDF]
```

### Typed Contract Match
* **`super-nlm` Output:** `MarkdownText` with YAML frontmatter metadata and inline LaTeX math (`$math$`).
* **`md2pdf-desktop` Input:** UTF-8 encoded Markdown file satisfying CommonMark + Pandoc math extensions.

---

## 4. Execution Trace & Empirical Telemetry

```text
2026-09-15T00:12:04.102Z [INFO] [COMPOSE-001] Initializing composition harness.
2026-09-15T00:12:04.215Z [INFO] [super-nlm] Connecting to FastMCP router... Account slot #2 selected.
2026-09-15T00:12:04.890Z [INFO] [super-nlm] Query dispatched to NotebookLM grounding engine.
2026-09-15T00:12:12.450Z [INFO] [super-nlm] Synthesis complete. Received 3,420 words (18.2 KB Markdown).
2026-09-15T00:12:12.480Z [INFO] [harness] Writing intermediate artifact to scratch/cxl_synthesis.md.
2026-09-15T00:12:12.510Z [INFO] [md2pdf-desktop] Spawning Pandoc compilation subprocess...
2026-09-15T00:12:14.920Z [INFO] [md2pdf-desktop] PDF compilation succeeded in 2.41s. 4 pages generated.
2026-09-15T00:12:14.935Z [INFO] [COMPOSE-001] Pipeline completed successfully. Zero errors.
```

---

## 5. Measured Resource Vector & Performance Metrics

$$\vec{R}_{\text{COMPOSE-001}} = \begin{bmatrix} C_{\text{usd}} \\ T_{\text{human}} \\ N_{\text{tokens}} \\ S_{\text{compute}} \end{bmatrix} = \begin{bmatrix} \$0.00 \\ 1.5\text{ minutes} \\ 0\text{ paid API tokens} \\ 10.82\text{ seconds} \end{bmatrix}$$

* **Total Elapsed Latency:** $10.82\text{ seconds}$ (Super-NLM query: $7.56\text{s}$, IPC/File I/O: $0.85\text{s}$, PDF compilation: $2.41\text{s}$).
* **Human Active Intervention:** $1.5\text{ minutes}$ (configuring query and reviewing final PDF output).
* **Direct Financial Cost:** $\$0.00$ (consumed via existing Google Family AI Pro zero-marginal-cost quota).
* **Synergy Metric:**
  $$\text{Synergy} = \text{Time}_{\text{manual}}(45\text{ min}) - \text{Time}_{\text{composed}}(1.5\text{ min}) = \mathbf{43.5\text{ minutes saved}} \quad (30\times \text{ throughput increase})$$

---

## 6. Failure Modes & Mitigations

1. **FastMCP Stdio Pipe Desynchronization:** If the NotebookLM browser session encounters an authentication challenge, `super-nlm` may hang waiting for JSON-RPC response.
   - *Mitigation:* Implemented a 30-second timeout in the harness with automatic fallback to token ring slot #3.
2. **Pandoc KaTeX Syntax Parsing Collision:** Unescaped dollar signs (`$100`) in economic text mistakenly trigger KaTeX math blocks in `md2pdf-desktop`.
   - *Mitigation:* Added regex sanitizer in the harness escaping currency symbols prior to Pandoc invocation.

---

## 7. Output Artifact & Evidence Classification

* **Output Artifact:** `research/results/cxl_3_0_executive_synthesis.pdf` (4 pages, 284 KB).
* **Evidence Tier:** **`E3 — LOCALLY VERIFIED`** (Executed and verified deterministically on local workstation).
