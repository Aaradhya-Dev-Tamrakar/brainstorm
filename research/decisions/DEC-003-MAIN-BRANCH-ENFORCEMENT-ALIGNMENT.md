# 🏛️ DECISION RECORD: DEC-003 (`main` Ruleset Enforcement Alignment — Verified Direct-Push Workflow)

```text
Decision ID:          DEC-003
Title:                Relaxation of the `Evidence-Backed-Ecosystem-main` Ruleset to Match the Verified Direct-Push Solo-Maintainer Workflow
Status:               IMPLEMENTED (Empirically Verified)
Decision Date:        2026-09-21
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Governing RFC:        research/architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md, research/architectures/ARCH-RFC-004-WORKFLOW-EXTERNALIZATION-FREEZE.md
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED (live GitHub ruleset API read-back + observed push acceptance)
Epistemic Class:      EMPIRICALLY_VERIFIED
Source Transcripts:   research/transcripts/2026-09-21_EVALUATE-FOUR-PROJECTS_CONVERSATION.md
Falsification Probe:  `gh api repos/Aaradhya-Dev-Tamrakar/brainstorm/rules/branches/main` — if `pull_request` or `required_status_checks` reappear, or if any push again reports `Bypassed rule violations`, the premise of this decision is false.
```

---

## 1. Context & Problem

On **2026-09-21** a routine [`sync.ps1`](../../sync.ps1) synchronization of this repository
pushed successfully to `main`, but the remote emitted an enforcement-bypass notice:

```text
remote: Bypassed rule violations for refs/heads/main:
remote: - Changes must be made through a pull request.
remote: - Required status check "verify" is expected.
```

The repository ruleset `Evidence-Backed-Ecosystem-main` (id `23533023`, created
2026-09-16 as part of the v1.0 governance freeze) enforced four rules on `refs/heads/main`:

| Rule | Parameters at the time | Effect on the actual workflow |
| :--- | :--- | :--- |
| `deletion` | — | Protects the branch from deletion. |
| `non_fast_forward` | — | Protects history from force pushes. |
| `pull_request` | `required_approving_review_count: 0`, strict base-branch policy, thread resolution | **Structurally unsatisfiable** by a direct push. |
| `required_status_checks` | `strict_required_status_checks_policy: true`, context `verify` | **Structurally unsatisfiable** before pushing: the check runs *on* the pushed commit. |

The ecosystem's actual, documented maintenance workflow for this repository is a
**local deterministic gate followed by a direct push** — `audit.bat` →
`sim/reconciliation_engine.py` (Layer 1 structural + Layer 2 behavioral) → `sync.ps1`
push — governed by [`ARCH-RFC-004`](../architectures/ARCH-RFC-004-WORKFLOW-EXTERNALIZATION-FREEZE.md)
and [`AGENTS.md`](../../AGENTS.md) §1 (which forbids ad-hoc per-repository Git commands in
favour of `sync.ps1`). Under that workflow the pre-push gate could never be satisfied, so
it was bypassed on **every** push via the ruleset's single bypass actor
(`actor_type: RepositoryRole`, `actor_id: 5`, `bypass_mode: always`).

Two problems follow, and both are governance defects rather than security defects:

1. **Ceremonial enforcement (epistemic inflation).** The repository's own
   [`README.md`](../../README.md) and freeze records advertised PR-gated merges with a
   required `verify` check, while the live system permitted every push through an
   administrative bypass. Under [`POL-001`](../../schemas/evidence-policy.md) this is an
   unearned claim about the enforcement tier, which is precisely the failure mode the
   Calibrated Evidence Policy exists to prevent.
2. **Document/reality drift.** `README.md` stated a *recommended policy* (require pull
   requests, checks up to date, one approving review, no force pushes) that no longer
   described the enforced state once the bypass became the normal path.

---

## 2. Decisions

**D1 — Reduce the enforced surface to integrity rules only.**
The ruleset remains `active` on `refs/heads/main` with exactly two rules: `deletion` and
`non_fast_forward`. The `pull_request` and `required_status_checks` rules are removed.
Branch-deletion and force-push protection are retained because they protect the provenance
chain itself, which is the asset [`INV-EPI-001`](../invariants/INV-EPI-001.md) depends on.

**D2 — Verification authority is stated explicitly rather than implied.**
Verification is not weakened; it is relocated to where it can actually execute:

- **Blocking gate (local, pre-commit):** [`sync.ps1`](../../sync.ps1) runs the dynamic
  reconciliation engine — Layer 1 structural consistency and Layer 2 behavioral
  reproducibility (`sim/test_*.py`) — *before* staging a commit.
- **Post-hoc evidence (remote, post-push):**
  [`.github/workflows/verification.yml`](../../.github/workflows/verification.yml)
  (job `verify`) runs `tools/validate_ecosystem.py` and `sim/reconciliation_engine.py` on
  every push to any branch.

Only the *blocking* semantics changed; the deterministic evidence chain is unchanged and
remains independently inspectable.

**D3 — Documentation MUST match enforcement.**
The `README.md` section on `main`-branch checks was rewritten to describe the enforced
state (integrity rules only) and to name this record as the rationale. No repository
document may claim PR-gated merges for `brainstorm` while that gate is bypassable. The
2026-09-16 freeze record and its verbatim transcripts
([`2026-09-16_ANTIGRAVITY_GOVERNANCE_RULESETS_FREEZE.md`](../transcripts/2026-09-16_ANTIGRAVITY_GOVERNANCE_RULESETS_FREEZE.md))
remain **unmodified historical artifacts**; on this single governance point they are
superseded by this record, because [`INV-EPI-001`](../invariants/INV-EPI-001.md) forbids
rewriting verbatim epistemic history.

**D4 — The bypass actor is deliberately preserved.**
`bypass_actors` is left exactly as found (`actor_id: 5`, `bypass_mode: always`). With only
integrity rules enforced, the escape hatch is retained for exceptional recovery
operations rather than for routine pushes.

**D5 — Scope is repository-local.**
This decision applies to `brainstorm` only. `super-nlm`, `Claude-Desktop` and
`AaradhyaDT.github.io` may continue to enforce PR-based gating; rulesets are a
per-repository admin operation and are not managed by these workflows.

---

## 3. Empirical Verification (E4)

**3.1 Pre-state (live read-back, 2026-09-21 16:16 +05:45)**

```text
gh api repos/Aaradhya-Dev-Tamrakar/brainstorm/rulesets/23533023
  enforcement: active
  bypass_actors: [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
  rules:
    - {"type": "deletion"}
    - {"type": "non_fast_forward"}
    - {"type": "pull_request", "parameters": {"required_approving_review_count": 0, ...}}
    - {"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": true,
        "required_status_checks": [{"context": "verify"}]}}

gh api repos/Aaradhya-Dev-Tamrakar/brainstorm/branches/main/protection
  -> HTTP 404 "Branch not protected"   (no classic branch protection present)
```

Classic branch protection was confirmed absent, so the ruleset was the only enforcement
surface: removing its two unsatisfiable rules is both sufficient and necessary.

**3.2 Post-state (live read-back after the alignment `PUT`)**

```text
gh api repos/Aaradhya-Dev-Tamrakar/brainstorm/rulesets/23533023
  name: Evidence-Backed-Ecosystem-main
  enforcement: active
  bypass_actors: [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
  rules: [deletion, non_fast_forward]

gh api repos/Aaradhya-Dev-Tamrakar/brainstorm/rules/branches/main
  - deletion
  - non_fast_forward
  total: 2
```

The effective-rules endpoint confirms the change is live on the branch, not merely stored
on the ruleset object.

**3.3 Observed push behaviour — before alignment**

The `sync.ps1` push at 11:16:53 local time produced the `Bypassed rule violations` block
quoted in §1. That is the direct observable of the defect.

**3.4 Observed push behaviour — after alignment**

The commit that introduces this record doubles as the intentional probe: it is a real
content change to `main` pushed by `sync.ps1`, with no bypass notice expected. Its
verbatim push output is appended to this record in the immediately following commit, so
that post-state evidence is an observed log rather than a prediction.

---

## 4. Consequences & Non-Goals

**Consequences**

- Direct pushes to `main` are now permitted by policy _and_ by the platform, so the
  documented workflow and the enforced workflow agree.
- Branch deletion and force pushes remain blocked for all actors.
- Re-enabling PR gating is now an explicit, deliberate change (a ruleset update plus a
  PR-producing path for `sync.ps1`, which does not currently exist). If it is ever
  re-enabled, the `sync.ps1` direct push will fail loudly and visibly instead of silently
  bypassing — which is the desired failure mode.
- The conditional warning in
  [`.github/workflows/sync-drive.yml`](../../.github/workflows/sync-drive.yml) remains
  correct as a fallback for a re-tightened ruleset.

**Non-Goals**

- This record does **not** weaken structural or behavioral verification, does not change
  the reconciliation engine, and does not alter any evidence tier elsewhere in the repo.
- This record does **not** assert that PR-based gating is bad practice; it asserts that
  *advertising* a gate which is bypassed on every push is worse than an honestly scoped
  one.

---

## 5. Cross-References

- Enforcement statement: [`README.md`](../../README.md) → `main` branch checks & verified enforcement
- Related decisions: [`DEC-001`](DEC-001-MEMORY-STRATIFICATION.md), [`DEC-002`](DEC-002-PERSONAL-RD-CAPSTONE-BOUNDARY.md)
- Governing standards: [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md), [`ARCH-RFC-004`](../architectures/ARCH-RFC-004-WORKFLOW-EXTERNALIZATION-FREEZE.md), [`POL-001`](../../schemas/evidence-policy.md)
- Deterministic gates: [`sync.ps1`](../../sync.ps1), [`audit.bat`](../../audit.bat), [`sim/reconciliation_engine.py`](../../sim/reconciliation_engine.py)
