# Document 4: Strategic Future Roadmap & Architectural Invariants

## 1. Flagship Research Wedge: Headless Invariant Assurance Engine

To avoid the common failure mode of unbounded feature expansion, near-term ecosystem R&D is anchored around a single high-leverage wedge: **Software, API & Protocol Invariant Assurance**.

```
Natural-Language Specification / API Documentation
                    ↓
Formalization into Typed Capability Contract (E1)
                    ↓
Candidate Invariant Formulation
                    ↓
SMT Symbolic Verification (Z3 Solver)
                    ↓
Executable Sandbox Verification (Docker / Anvil)
                    ↓
Reproducible Counterexample or Evidence Dossier (E4/E5)
```

- **Target Domain**: Software state machines, REST/FastAPI endpoints, and deterministic protocol rules.
- **Core Optimization Metric**: **Discovery Cost Efficiency**:
  $$\text{Efficiency} = \frac{\text{Financial Cost} + \text{Compute Cost}}{\text{Verified Discoveries}}$$
  with **100% recall strictly enforced on planted synthetic violations**.

---

## 2. The 9-Stage Engineering & R&D Sequence

Rather than expanding the ecosystem by inventing disconnected projects, engineering execution follows a deterministic, 9-stage sequence:

| Phase | Milestone | Scope & Deliverable | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Canonical Registry & Ontological Hardening** | Establish single source of truth across all 22 tools (`schemas/capability-registry.yaml` and `schemas/ecosystem.registry.json`). | **Completed** |
| **2** | **Comprehensive Epistemic Audit** | Granular audit classifying all major claims, numbers, and citations against traceable artifacts (`report/repository-audit.md`). | **Completed** |
| **3** | **Economic Model Correction** | Decouple personal living expenses from productive CAPEX/OPEX and vectorize resource tracking. | **Completed** |
| **4** | **Invariant Assurance Engine MVP** | Build synthetic state machine invariant generator and Z3 verification loop. | **Months 0–3** |
| **5** | **Reproducibility Benchmark Suite** | Containerize simulation models (`sim/`) with deterministic seeds, fixed parameters, and automated assertions. | **Months 1–3** |
| **6** | **2-Capability Composition Test** | Formally benchmark and measure composition synergy between `Super-NLM` and `md2pdf-desktop`. | **Months 2–4** |
| **7** | **3-Capability Composition Test** | End-to-end telemetry chain: `Screen Q&A` $\to$ `Super-NLM` $\to$ `RSVP Reader`. | **Months 4–6** |
| **8** | **Worker Session Runtime (WSR) Abstraction** | Standardize task checkpointing harness for zero-data-loss multi-agent session migration. | **Months 6–9** |
| **9** | **Jarvis Executive Interface** | Assemble the vendor-agnostic high-level natural language executive interface over the verified capability mesh. | **Months 9–12** |

---

## 3. Defensible Economic Model & Capital Accounting

The ecosystem models economic sustainability with strict accounting discipline:
1. **Separation of Concerns**: Personal living expenses are cleanly separated from productive CAPEX (hardware compute rigs, ESP32 boards, local disks) and OPEX (electricity, local inference compute, targeted API usage).
2. **Cognitive-Worker Baseline**: Minimizes high recurring subscription costs by leaning heavily on local execution, zero-token batch scripts (`audit.bat`, `sim.bat`), and rotating multi-account free/pro tiers via Super-NLM.
3. **Marginal Task Accounting**: Compute and API expenses are calculated per verified task or discovery rather than amortized globally.

---

## 4. Transparent Limitations & Known Failure Modes

Every mature engineering system acknowledges its architectural constraints (`report/limitations.md`):
- **Cross-Account Session Volatility**: Multi-account Google rotations depend on valid browser cookies; automated token refreshers and headless session maintainers mitigate cookie expiration.
- **Hardware-Specific Acceleration**: High-speed video transcoding in `yt-dlp-live` relies on Intel Arc QSV hardware; headless fallback to CPU FFmpeg requires higher CPU utilization.
- **Subprocess Concurrency on Windows**: Windows IOCP handles and conhost spawns can introduce latency; Super-NLM and Claude-Desktop mitigate this via `CREATE_NO_WINDOW` (0x08000000) flags and thread-pooled execution.
