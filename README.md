# Google Classroom MCP Server — Brainstorm Ecosystem Branch

> **Ecosystem Branch**: `google-classroom-mcp`  
> **Canonical Repo**: [Aaradhya-Dev-Tamrakar/google-classroom-mcp](https://github.com/Aaradhya-Dev-Tamrakar/google-classroom-mcp)  
> **Archetype**: Sensory / Academic Hub Bridge Engine  
> **Role in Jarvis**: Direct Model Context Protocol (MCP) integration with Google Classroom for automated course monitoring, coursework grading, announcements, and submission turn-in workflows  

---

## Tool Summary

High-performance Model Context Protocol (MCP) bridge implemented in Node.js ESM via `@modelcontextprotocol/sdk`. Connects personal and fleet AI agents directly to Google Classroom API v1 endpoints with OAuth2 token auto-refresh, submission file turn-ins, and classroom skills.

| Field | Value |
|---|---|
| **Registry Index** | 20 |
| **Branch ID** | `google-classroom-mcp` |
| **Tech Stack** | Node.js ESM, `@modelcontextprotocol/sdk`, Google Classroom API |
| **Execution Context** | Local / Fleet MCP |
| **Core Superpower** | Direct Google Classroom integration for courses, coursework, assignments, announcements, and submissions |
| **Local Path** | `F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp` |
| **Contract Ref** | `schemas/examples/google-classroom-mcp.contract.json` |

---

## Files in This Branch

```text
google-classroom-mcp/
├── index.mjs             # MCP Server entry point and tool handler registrations
├── auth.mjs              # OAuth2 authentication lifecycle and token management
├── sync-schemas.mjs      # Auto-sync tool schemas with MCP definitions
├── skills/               # Reusable Antigravity/Claude skill configurations
├── package.json          # Node.js ESM project manifest
├── package-lock.json     # Deterministic npm dependency lock
├── sync.ps1              # Ecosystem Git sync engine with token pre-commit guards
├── LICENSE               # MIT License
├── README.md             # Ecosystem branch documentation
└── .gitignore            # Ignores credentials, tokens, and node_modules
```

---

## 📌 Ecosystem Architecture

See [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md) for the full Jarvis capability mesh.
