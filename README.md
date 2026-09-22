# LocalSend MCP Server — Brainstorm Ecosystem Branch

> **Ecosystem Branch**: `localsend-mcp`  
> **Canonical Repo**: [Aaradhya-Dev-Tamrakar/localsend-mcp](https://github.com/Aaradhya-Dev-Tamrakar/localsend-mcp)  
> **Archetype**: Executive Actuator / Zero-Cloud P2P Transport Engine  
> **Role in Jarvis**: Direct LAN/Wi-Fi file, text, and clipboard transport across phones, PCs, and laptops without cloud intermediaries  

---

## Tool Summary

TypeScript Model Context Protocol (MCP) server implementing the LocalSend Protocol v2.1. Enables AI agents to discover local network peers, initiate mutual TLS encrypted file transfers, broadcast text and clipboard snippets, and maintain a persistent listening daemon.

| Field | Value |
|---|---|
| **Registry Index** | 21 |
| **Branch ID** | `localsend-mcp` |
| **Tech Stack** | Node.js ESM, TypeScript, `@modelcontextprotocol/sdk`, LocalSend Protocol v2.1 |
| **Execution Context** | Local / Fleet MCP |
| **Core Superpower** | Zero-cloud local P2P file, text, and clipboard transfer across LAN/Wi-Fi devices with mutual TLS and persistent favoriting listener |
| **Local Path** | `F:\Aaradhya-Dev-Tamrakar\localsend-mcp` |
| **Contract Ref** | `schemas/examples/localsend-mcp.contract.json` |

---

## Files in This Branch

```text
localsend-mcp/
├── src/                  # TypeScript source code (index, protocol, crypto, transport)
├── package.json          # Node.js project manifest & build scripts
├── package-lock.json     # Deterministic npm dependency tree
├── tsconfig.json         # TypeScript compiler configuration
├── sync.ps1              # Ecosystem Git sync engine with secret scanning
├── LICENSE               # MIT License
├── README.md             # Ecosystem branch documentation
└── .gitignore            # Ignores build artifacts (dist/), keys, and node_modules
```

---

## 📌 Ecosystem Architecture

See [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md) for the full Jarvis capability mesh.
