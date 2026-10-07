# 🏛️ Research Protocol & Experiment Dossier: EXP-012

> **Artifact ID:** `EXP-012`  
> **Title:** Empirical Scale-Out & Activation Protocol for 27-Worker GitHub Copilot Multi-Account Fleet  
> **Status:** `IMPLEMENTED`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Date:** 2026-10-07  
> **Evidence Tier:** `E4` (`EMPIRICALLY_VERIFIED`)  
> **Upstream Traces:** [`ARCH-SPEC-003`](../architectures/ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md), [`FLEET-001`](FLEET-001.md), [`FLEET-002`](FLEET-002.md)  
> **Capability Contract:** [`fleet-orchestrator.contract.json`](../../schemas/examples/fleet-orchestrator.contract.json)  
> **Target Subsystem:** Fleet Orchestrator (`F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator`)  

---

## 1. Executive Summary & Objective

The Headless Worker Fleet architecture specified in [`FLEET-002`](FLEET-002.md) established the mathematical and architectural rationale for zero-GUI, asynchronous GitHub Copilot agent runtimes operating at ~15 MB RAM per worker. 

This experiment executes the empirical production scale-out of the fleet from an initial 13-account baseline to **27 concurrent GitHub accounts**, achieving **27 verified active canary workers** pooling **5,400 AI credits / month** of parallel, non-interactive execution capacity following policy cooldown resolution.

This protocol documents the empirical discovery of the **9-Step Account Activation Playbook**, token permission boundaries, runtime adapter credit constraints, and end-to-end task lease lifecycle verification.
---

## 2. Empirical Ground Truth & Capacity Metrics

| Metric | Baseline (`FLEET-002`) | Empirical Result (`EXP-012`) | Variance / Scaling |
| :--- | :--- | :--- | :--- |
| **Registered GitHub Accounts** | 13 accounts | **27 accounts** | $+107.7\%$ |
| **Active Canary Verified Workers** | 13 accounts | **27 accounts** | $+107.7\%$ |
| **Pending Policy Cooldown** | 0 accounts | **0 accounts** (Resolved) | Fully Cleared |
| **Monthly Compute Capacity** | 2,600 AI credits | **5,400 AI credits** | $+107.7\%$ |
| **Local Memory Footprint** | ~15 MB / worker | **~14.2 MB / worker** | $-5.3\%$ |
| **Headless Concurrency Model** | Non-blocking `asyncio` | **`asyncio.gather` concurrent canary** | Zero-leakage verified |
| **Test Suite Certification** | 100/100 pytest | **111/111 pytest (100%)** | 0 regressions (52.45s) |

---

## 3. The 9-Step Account Activation Playbook

During empirical onboarding, raw token generation without explicit web-portal feature entitlement failed with `Access denied by policy settings`. The deterministic protocol to provision and activate each fleet account is established as follows:

1. **Session Isolation:** Open a clean browser session or private container. Sign out of all existing GitHub accounts.
2. **Account Sign-In:** Authenticate into the target auxiliary GitHub worker account.
3. **Gateway Entitlement Provisioning:** Navigate directly to `https://github.com/settings/copilot/features`.
4. **Feature Activation:** Click **"Start using Copilot Free"** (or enroll in available Copilot tier). *Crucial: this triggers internal provisioning on GitHub's gateway routing layer.*
5. **Token Configuration:** Navigate to `https://github.com/settings/personal-access-tokens/new`.
6. **Token Metadata:** Name the token `Fleet-Orchestrator`. Set expiration to preferred policy (custom or no expiration).
7. **Permission Domain Isolation:** Under **Permissions**, select the **Account** tab. Explicitly set **Repository permissions to *None***.
8. **Scope Grant:** Under **Account permissions**, check:
   - **`Copilot Requests`**: `Read and write` (strictly mandatory for CLI autopilot).
   - *(Optional)* `Copilot Chat`: `Read and write`.
   - *(Optional)* `Copilot Editor Context`: `Read and write`.
9. **Token Deployment:** Click **Generate token**, copy the token string, and append to `.env.fleet` under `COPILOT_ACCOUNT_N_TOKEN`.

---

## 4. Key Architectural Invariants & Discoveries

### Invariant 1: Security & Identity Separation (Repository None Scope)
Auxiliary fleet tokens execute code locally on the workstation filesystem via child processes spawned by the supervisor. They **never** require GitHub repository read or write permissions. By enforcing Repository: *None*:
- Push access remains exclusively bound to the maintainer identity (`@AaradhyaDT`).
- Auxiliary tokens cannot tamper with remote repositories or branches.
- Token leakage risk is strictly confined to Copilot inference requests.

### Invariant 2: Copilot CLI Minimum AI Credits Boundary
When configuring the headless execution runtime via `--max-ai-credits`, GitHub Copilot CLI rejected allocations $< 30$ with an input validation failure. The runtime adapter in `tools/copilot_fleet.py` and `client/fleet_supervisor.py` was patched to enforce $\text{max\_ai\_credits} \ge 30$, ensuring stable task execution without runtime CLI crashes.

### Invariant 3: Gateway Policy Cooldown on Fresh Accounts
Three auxiliary worker accounts (`beie7923`, `Majorprj79039-Sankalpa`, `Majorprj79043-Sonia`) initially exhibited `Access denied by policy settings` despite valid token permissions and completed UI enrollment. Historical telemetry confirmed that brand-new accounts encounter a ~12–24h asynchronous policy synchronization cooldown before GitHub API routing recognizes newly provisioned Free-tier Copilot entitlements. *(Resolution Milestone: On 2026-10-07, the asynchronous policy synchronization window concluded; all 3 accounts passed API status verification, bringing the fleet to 27 / 27 active ready workers).*

### Invariant 4: Dual-File Configuration Architecture
Worker configuration follows strict secret isolation:
- `.env.fleet`: Git-ignored file containing live API credentials and token pairs across all 27 workers.
- `.env.fleet.example`: Version-controlled sanitised schema documenting structure and indexing.

---

## 5. End-to-End Task Lease Lifecycle Verification

The autonomous dispatch lifecycle was empirically validated using `tools/e2e_dispatch_smoke.py`:
1. **REGISTER:** Worker registers its capabilities (`fastapi`, `cli`, `autopilot`) and credit balance with the central FastAPI DAG Orchestrator.
2. **CLAIM LEASE:** Worker claims a distributed task lease with bounded TTL and heartbeat monitoring.
3. **AUTOPILOT EXECUTE:** Worker spawns a non-interactive headless `CopilotCLIAdapter` sub-process to solve the task.
4. **CHECKPOINT:** Intermediate state and AST diffs are saved to the persistent store.
5. **DONE:** Task marked completed; lease released; credit meter decremented; worker returns to idle pool.

All 111 unit and integration tests passed cleanly in 38.71s with zero race conditions across concurrent lease acquisitions.

---

## 6. Epistemic Provenance & Audit Trail

- **Evidence Tier:** `E4` (`EMPIRICALLY_VERIFIED`).
- **Deterministic Verification Ledger:** Validated via `sim/reconciliation_engine.py` and `audit.bat`.
- **Ecosystem Registration:** Cataloged in `schemas/ecosystem.registry.json` (Module #27) and `schemas/capability-registry.yaml`.
- **Related Repositories:** `https://github.com/AaradhyaDT/Fleet-Orchestrator`.
