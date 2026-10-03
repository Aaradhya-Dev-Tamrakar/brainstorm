# PLAN-GCP-001: Google Classroom Pilot Architectural Plan & Roadmap 🎓🧭

> **Plan ID**: `PLAN-GCP-001`  
> **Target Module**: `google-classroom-pilot` (`F:\Aaradhya-Dev-Tamrakar\Utility\google-classroom-pilot`)  
> **Status**: `PROPOSED`  
> **Created**: 2026-10-03  
> **Ecosystem Class**: Utility Fleet / Autonomous Intent Pilot  
> **Sibling Tools**: `github-pilot` (`F:\Aaradhya-Dev-Tamrakar\Utility\github-pilot`), `windows-pilot` (`F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot`)

---

## 1. Executive Summary & Core Philosophy

**`google-classroom-pilot`** is an autonomous, intent-driven academic orchestrator designed to operate at the macro-plane of a student's term. While conversational LLM chats handle micro-plane questions (e.g. *"explain question 3 of homework 2"*), the pilot handles macro-plane automation: multi-course material harvesting, deadline triage, YouTube/drive asset sync, assignment specification parsing, and safe two-phase submission commit.

### Key Architectural Pillars

1. **Token-Zero Local Core**:
   - API calls, binary asset downloads, checksumming, and folder layout generation execute locally in deterministic Python without burning LLM context tokens. Emits micro-payload status summaries (`< 1 KB`) for AI agents.
2. **Dual-Scope Authentication Guarantee (`INV-AUTH-001`)**:
   - Resolves Classroom API scopes (`https://www.googleapis.com/auth/classroom.*`) and Drive API scopes (`https://www.googleapis.com/auth/drive.readonly`) simultaneously to eliminate HTTP 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT` errors during binary file downloads.
3. **Two-Phase Human Confirmation Gate (`INV-SUB-001`)**:
   - Preparing and attaching files to `studentSubmissions` is non-destructive; executing `turn_in_assignment` is legally final. All automated submission flows require human terminal confirmation.
4. **Natural Language Intent Engine**:
   - Dual-path router combining a local zero-token heuristic matcher (regex/keyword) with a structured LLM intent planner (Gemini 3.8 Flash).

---

## 2. Directory Layout & Module Specifications

Target location: `F:\Aaradhya-Dev-Tamrakar\Utility\google-classroom-pilot`

```
google-classroom-pilot/
├── pilot/
│   ├── __init__.py
│   ├── cli.py                     # Typer CLI application (interactive & automated commands)
│   ├── config.py                  # OAuth credentials resolver & directory mappings
│   │
│   ├── intent/                    # Natural Language Understanding & Planning Engine
│   │   ├── __init__.py
│   │   ├── router.py              # Zero-token heuristic matcher + fast LLM planner
│   │   ├── schemas.py             # Pydantic action schemas (Harvest, Inspect, Submit, Radar)
│   │   └── prompts.py             # System prompts for intent classification
│   │
│   ├── core/                      # Deterministic Execution Engines
│   │   ├── __init__.py
│   │   ├── client.py              # Unified Classroom & Drive API client (OAuth token refresh)
│   │   ├── radar.py               # Deadline scanner, submission state diffing, grade tracking
│   │   ├── harvester.py           # Multi-threaded asset downloader (PDF, Doc, Slide, Zip, Links)
│   │   ├── submitter.py           # Two-phase assignment staging & submission harness
│   │   └── organizer.py           # Local folder taxonomist & file naming normalizer
│   │
│   ├── integrations/              # Ecosystem Connectors
│   │   ├── __init__.py
│   │   ├── obsidian.py            # Generates Obsidian-compatible syllabus & MOC ([[wikilinks]])
│   │   ├── super_nlm.py           # Staging harvested slides into Google NotebookLM fleet
│   │   ├── youtube.py             # Parses lecture video links and triggers yt-dlp
│   │   └── localsend.py           # Shares downloaded bundles via LocalSend MCP
│   │
│   └── mcp/                       # Native MCP Server Bridge
│       ├── __init__.py
│       └── server.py              # Exposes pilot tools to Antigravity & Claude Desktop
│
├── tests/                         # Pytest test suite
├── .env.example                   # Environment configuration template
├── AGENTS.md                      # Agent operational protocol & evidence rules
├── pyproject.toml                 # Packaging specification
├── sync.ps1                       # Ecosystem Git sync & secret guard
├── sync.bat                       # Zero-friction execution wrapper
└── README.md                      # Architecture documentation
```

---

## 3. Invariants & Safety Protocols

| Invariant | Title | Enforcement Rule |
| :--- | :--- | :--- |
| `INV-AUTH-001` | Dual-Scope Credentials Partitioning | Mandatory separation of Classroom REST API calls and Drive v3 binary stream downloads using respective token stores (`.classroom-server-credentials.json` & `.gdrive-server-credentials.json`). |
| `INV-SUB-001` | Two-Phase Submission Confirmation | Staging files on Drive/Classroom is non-final. `turn_in_assignment` MUST prompt for explicit human confirmation (`[Y/n]`) with staged file metadata displayed. |
| `INV-ENC-001` | Windows Console UTF-8 Safety | Enforce `sys.stdout.reconfigure(encoding='utf-8')` on terminal startup to handle Unicode symbols, bullet points, and special course names. |
| `INV-TOK-001` | Token-Zero Local Telemetry | Data fetching, filtering, sorting, and asset downloading must run locally with zero LLM API overhead. |

---

## 4. Phased Implementation Roadmap

1. **Phase 1 (Core Foundation)**: Unified Classroom & Drive API Client (`pilot/core/client.py`), OAuth loopback listener, and authentication sanity tests.
2. **Phase 2 (Radar & CLI Entrypoints)**: Deadline triage scanner (`pilot/core/radar.py`), course list inspector, and Typer CLI foundation (`pilot/cli.py`).
3. **Phase 3 (Asset Harvester)**: Multi-threaded Google Drive downloader, external link indexer, YouTube video link extractor, and local taxonomy organizer (`pilot/core/harvester.py`).
4. **Phase 4 (Intent Router & AI Integration)**: Heuristic regex matcher + Gemini 3.8 Flash structured intent router (`pilot/intent/router.py`).
5. **Phase 5 (Two-Phase Submission Harness)**: Pre-flight validation, Drive staging, student submission attachment, confirmation prompt, and `turn_in` execution (`pilot/core/submitter.py`).
6. **Phase 6 (Ecosystem Integration & Native MCP)**: `super-nlm` slide feeder, Obsidian MOC indexer, and MCP server bridge (`pilot/mcp/server.py`).
