---
description: ">-"
---

# Portfolio Project Manager Skill

CRITICAL RULE: Whenever the user asks to add, update, or register a new project or tool to their portfolio website (`F:\AaradhyaDT\AaradhyaDT.github.io`):
- **NEVER** manually open and slice `projects.html` with regex or replace large string blocks.
- **NEVER** manually create unencrypted raw GitHub `href` tags in `projects.html`.
- **NEVER** hardcode or guess project numbers (`p-00x`) or filter pill counts.

You **MUST** invoke the deterministic project onboarding engine:
`F:\AaradhyaDT\AaradhyaDT.github.io\scripts\add_project.py`

---

## 1. Quick Ingestion Workflow (Zero-Token Manifest Mode)

1. Formulate a clean, compact project JSON manifest (either in memory or as a scratch file):
```json
{
  "title": "Windows Pilot — Semantic UIA & MCP Desktop Automation Engine",
  "repo_url": "https://github.com/AaradhyaDT/windows-pilot",
  "category": ["apps", "hardware"],
  "status": "Sep 2026",
  "bullets": [
    "Mission-critical Windows desktop automation engine for autonomous AI coding agents.",
    "Resolution-independent Microsoft UI Automation (UIA) COM & Win32 control.",
    "Native MCP server (winpilot-mcp) with virtual desktop awareness."
  ],
  "tags": ["Python 3.10+", "Win32 API", "MCP Server", "Windows 11"],
  "section": "personal",
  "tier": "vip"
}
```

2. Save to a temporary file (e.g., `new_project.json`) and execute with preview or live addition:

### Preview with Dry Run (Recommended first):
```powershell
python scripts/add_project.py --from-json new_project.json --dry-run
```

### Apply Live:
```powershell
python scripts/add_project.py --from-json new_project.json
```

---

## 2. CLI Single-Command Mode

For quick additions directly via terminal flags:
```powershell
python scripts/add_project.py `
  --title "Tool Name — Subtitle Description" `
  --repo "https://github.com/AaradhyaDT/my-tool" `
  --category apps aiml `
  --status "In Progress" `
  --bullets "Key technical architecture item 1." "Key benchmark or metric item 2." `
  --tags "Python" "FastMCP" "Async"
```

---

## 3. What the Engine Executes Automatically

In less than 1 second, `add_project.py`:
1. **Contiguous ID Assignment**: Scans DOM, finds the current max integer (e.g. `34`), and assigns `p-035` and `P — 035`.
2. **Zero-Leak Encryption**: Encrypts the repository URL with AES-256-GCM (PBKDF2) using `vip2026` or `master2026` and registers `proj-<slug>` into `access.js`.
3. **Card Generation**: Generates compliant, accessible `<details class="project-card reveal ...">` markup with the locked link `data-payload-link-id="proj-<slug>"`.
4. **DOM Section Injection**: Injects the card into `#section-personal` (default) or `#section-projects`.
5. **Exact Filter Recounting**: Parses all cards in the DOM and automatically writes the exact counts to `<span class="proj-filter-count">` for `All`, `aiml`, `embedded`, `hardware`, and `apps`.
6. **Post-Addition Integrity**: Automatically runs `scripts/extract_index.py` (updates static search index) and `scripts/verify.py` (guarantees 26/26 check categories pass, including `release-shas` and `version` integrity).

---

## 4. Release SHA & What's New Integrity Invariant

Whenever versioning, bumping, or adding releases to `assets/js/data/releases.js`:
- **NEVER** use synthetic or placeholder `sha` strings (e.g., `rel50`, `rel55`, `upg47`, `xtool20`).
- **ALWAYS** ensure every `sha` is a valid, existing Git commit short hash (matching `^[0-9a-f]{7,40}$`) that resolves directly to `https://github.com/AaradhyaDT/AaradhyaDT.github.io/commit/<sha>`.
- `scripts/site_automation.py` automatically resolves `git rev-parse --short HEAD` for major releases, and `scripts/verify.py` (Category 26: `release-shas`) enforces this during pre-commit and CI.

---

## 5. Finalizing Deployment

Once all additions pass local verification:
```powershell
.\sync.bat -m "feat(projects): register <project-name> in portfolio showcase"
```
*(Runs single-pass search extraction, AST graph update, 26-category verification gate, commit, push, and bot stamp sync).*
