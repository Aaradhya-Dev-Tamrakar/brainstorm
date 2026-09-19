# ARCH-RFC-006: Public/Private Information Boundary & Security Architecture

- **Artifact ID:** ARCH-RFC-006
- **Status:** IMPLEMENTED
- **Principal Architect:** Aaradhya Dev Tamrakar (ADT) & Multi-Model Cognitive Council
- **Evidence Tier:** E4 (Locally Verified)
- **Supersedes / Extends:** ARCH-RFC-001, POL-001 (Governance)

---

## 1. Executive Summary & Problem Statement

The 2026-09-19 external audit ([`2026-09-19_RATE-WORKFLOW_CONVERSATION.md`](file:///F:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts/2026-09-19_RATE-WORKFLOW_CONVERSATION.md)) evaluated information boundary design at **6.4/10**, identifying a critical architectural conflation:

*The repository simultaneously serves as a public R&D lab, an open portfolio substrate, a deterministic verification mesh, and a private cognitive memory space.*

Storing large personal profile documents (e.g., `AARADHYA_MASTER_v165.md`, ~118 KB) in the root of a public repository violates the principle of **least exposure** and risks accidental credential/personal data leakage during public git synchronization.

---

## 2. The Two-Plane Security Partition

To reconcile transparent engineering provenance with private cognitive memory, the repository enforces a strict two-plane security architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PUBLIC CONTROL PLANE                            │
│  (Public GitHub, Verified Reproducibility, Open-Source Verification)   │
│                                                                        │
│  - Architecture Specifications (`research/architectures/ARCH-*.md`)    │
│  - Capability Contracts (`schemas/capability.contract.v1.json`)        │
│  - Capability Registry (`schemas/ecosystem.registry.json`)             │
│  - Deterministic Simulation & Audit Engines (`sim/*.py`)               │
│  - LaTeX Research Dossier (`report/`)                                  │
│  - Verified Physical Output Artifacts (`research/results/*.pdf`)       │
│  - Sync & Orchestration Scripts (`sync.ps1`, `audit.bat`, `sim.bat`)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         FIREWALL / SCANNER GUARD
                          (`sync.ps1` Secret Scan)
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                        PRIVATE COGNITIVE PLANE                         │
│  (Local Filesystem Only / Encrypted / Restricted Access)               │
│                                                                        │
│  - Personal Profiles & Life Context (`*MASTER*.md`, `PROFILE.md`)      │
│  - Sensitive Transcripts & Unredacted Conversations                    │
│  - Unreleased Project Ideas & Proprietary API Tokens                   │
│  - Raw Memory Checkpoints & Session Scratchpads                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implementation Rules

1. **Pre-Commit Secret Scanner Guard**:
   `sync.ps1` runs `Find-StagedSecrets` on all staged changes prior to any commit. Any match for API tokens, private keys, or passwords immediately unstages changes and halts synchronization.

2. **Master Profile Hygiene**:
   - `AARADHYA_MASTER_*.md` files must undergo automated redaction of sensitive credentials, addresses, and private contact info before committing.
   - Private personal logs must be stored in `.gitignore`-guarded local paths or private submodules.

3. **Public Capability Contracts**:
   All capability modules in `schemas/ecosystem.registry.json` and `schemas/capability-registry.yaml` must only expose public function signatures, schema interfaces, and verified empirical metrics.

---

## 4. Verification & Conformance

- `sim/reconciliation_engine.py` verifies that all schema and RFC cross-references adhere to public boundary rules.
- Pre-commit scanning in `sync.ps1` guarantees zero secrets staged across all ecosystem branches.
