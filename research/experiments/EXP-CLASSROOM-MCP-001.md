# 🏛️ RESEARCH EXPERIMENT: EXP-CLASSROOM-MCP-001 (Live Read-Only Verification of the Google Classroom MCP Server)

```text
Artifact ID:          EXP-CLASSROOM-MCP-001
Title:                Live Read-Only Verification of google-classroom-mcp against a Real Course
Version:              1.0.0
Status:               EMPIRICALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Ingestion & Actuation (Academic Workflow)
Created Date:         2026-09-19
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED
Target Tool:          F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp
Contract:             schemas/examples/google-classroom-mcp.contract.json
```

---

## 1. Objective & Hypothesis

* **Hypothesis (HYP-CLS-001):** The `google-classroom-mcp` stdio server, using the previously completed OAuth authorization, can complete an MCP handshake, advertise its tool surface, and return live data from the Google Classroom REST API v1 for a real course.
* **Scope:** Read-only. Only `list_courses`, `list_coursework`, and `list_announcements` were invoked. The write-capable tools `turn_in_assignment` and `reclaim_assignment` were NOT called.

## 2. Method

A throwaway Node.js client (deleted after the run; not committed) spawned `node index.mjs` as a child process over stdio and sent newline-delimited JSON-RPC 2.0. Wall-clock latency was measured client-side around each request. Identifiers in this record are redacted or omitted.

| Setting | Value |
| :--- | :--- |
| Host | Windows 11 workstation, Node.js via nvm4w |
| Transport | MCP stdio JSON-RPC, protocol `2024-11-05` |
| Auth | Pre-existing OAuth credentials file (contents not inspected or recorded) |
| Date of run | 2026-09-19 |
| Trials | 1 (single run) |

## 3. Results

| # | Call | isError | Latency | Observation |
| :-: | :--- | :-: | :-: | :--- |
| 1 | `initialize` | false | 236-403 ms (two runs) | `serverInfo = {"name": "classroom-mcp", "version": "1.0.0"}` |
| 2 | `tools/list` | false | 3-5 ms | 12 tools: `list_courses`, `get_course`, `list_coursework`, `get_coursework`, `list_submissions`, `get_submission`, `list_announcements`, `list_coursework_materials`, `list_teachers`, `list_students`, `turn_in_assignment`, `reclaim_assignment` |
| 3 | `list_courses` | false | 1034-1410 ms (two runs) | `Found 1 course(s)`: "AI Fellowship 2026", state `ACTIVE` |
| 4 | `list_coursework` | false | 907 ms | `Found 34 coursework item(s)` |
| 5 | `list_announcements` | false | 816 ms | `Found 30 announcement(s)` |

Latencies for `initialize`, `tools/list` and `list_courses` come from two separate runs; the range is reported. `list_coursework` and `list_announcements` were measured once.

## 4. Claim Reconciliation

| Claim in `capability-registry.yaml` (before this record) | Measured | Verdict |
| :--- | :--- | :--- |
| 34 coursework items | 34 | Confirmed |
| 29 announcements | 30 | **Discrepancy (+1).** Consistent with an announcement posted between the earlier check and this run, but that explanation is unverified. Registry updated to the measured value. |
| Live HTTP 200 API verification | All 5 calls returned `isError = false` with data | Confirmed at the MCP layer (raw HTTP status codes are not surfaced by the server) |
| Token auto-refresh lifecycle test | Not exercised in this run | **Not verified here.** Removed from the verified set. |

## 5. Limitations

* Single run, single machine, single course; no variance, no load testing.
* Read-only: submission, grade, roster, and write paths (`list_submissions`, `list_students`, `list_teachers`, `turn_in_assignment`, `reclaim_assignment`) were not exercised.
* Only the MCP layer was observed; raw HTTP status codes and the OAuth refresh path were not captured.
* Course, coursework and announcement contents are deliberately not stored in this repository.
* Tier basis: the policy defines E4 as executed against a live network target. Reproducibility by an independent party (E5) is not claimed.

## 6. Provenance

* **Source repository:** `F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp` (HEAD `4d2e181` at time of run)
* **Reproduction:** run `node index.mjs`, send `initialize`, `tools/list`, then `tools/call` for `list_courses`, `list_coursework` and `list_announcements` with the returned course id.