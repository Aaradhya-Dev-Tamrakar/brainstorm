# 🧠 Antigravity Custom Skills Registry & Local Mirror

> **Path:** `tools/skills/`  
> **Global System Path:** `C:\Users\Aaradhya\.gemini\config\skills\`  
> **Purpose:** Version-controlled master repository and source-of-truth mirror for all 33 custom Antigravity agent skills.

---

## 📊 Skills Matrix & Functional Taxonomy (33 Skills)

| Category | Skill Name | Path | Description & Core Triggers |
| :--- | :--- | :--- | :--- |
| **Writing & Publishing** | [`blog-writing-like-claude`](blog-writing-like-claude/SKILL.md) | `tools/skills/blog-writing-like-claude/` | Enforces calm-authority voice, zero-hype vocabulary, functional precision, scope boundaries, and dog-fooding transparency modeled after the Claude blog. (Origin: BiasAperture) |
| **Compliance & Auditing** | [`compliance-report-harmonizer`](compliance-report-harmonizer/SKILL.md) | `tools/skills/compliance-report-harmonizer/` | Enforces report harmonization, structural invariants, dual HTML/PDF interoperability, and headless Blink print rendering. (Origin: BiasAperture) |
| **NotebookLM Fleet & Downloads** | [`super-nlm`](super-nlm/SKILL.md) | `tools/skills/super-nlm/` | Google NotebookLM multi-account rotator, MCP query engine, and batch generation. |
| | [`super-nlm-downloads`](super-nlm-downloads/SKILL.md) | `tools/skills/super-nlm-downloads/` | Automates URL extraction, subject folder downloads (outside repo), and LocalSend transfers. |
| **Ingestion & Archival** | [`doc-archiver`](doc-archiver/SKILL.md) | `tools/skills/doc-archiver/` | Invokes `save-doc` CLI to extract Google Docs and web docs into structured Markdown. |
| | [`chat-archiver`](chat-archiver/SKILL.md) | `tools/skills/chat-archiver/` | Invokes `save-chat` CLI to parse ChatGPT and model share URLs into clean dialogue logs. |
| | [`cp-archive-harvester`](cp-archive-harvester/SKILL.md) | `tools/skills/cp-archive-harvester/` | Autonomous CDP scraper for competitive programming problem statements and 100-pt solutions. |
| | [`google-classroom`](google-classroom/SKILL.md) | `tools/skills/google-classroom/` | Google Classroom MCP assistant for coursework, assignments, and due date management. |
| **Multi-Agent Orchestration** | [`agent-teams-orchestration`](agent-teams-orchestration/SKILL.md) | `tools/skills/agent-teams-orchestration/` | Scout-Reviewer-Writer-Lead division of labor, concurrency isolation, and bounded iterations. |
| **Codebase Graph & Systems** | [`graphify`](graphify/SKILL.md) | `tools/skills/graphify/` | Persistent knowledge graph query, path traversal, and community structure analysis. |
| | [`graphify-code-search`](graphify-code-search/SKILL.md) | `tools/skills/graphify-code-search/` | Call-chain discovery, caller/callee tracing, and AST helper reuse via Graphify graph. |
| | [`mcp-integration`](mcp-integration/SKILL.md) | `tools/skills/mcp-integration/` | Configuration, testing, and registration of Model Context Protocol servers. |
| | [`skill-development`](skill-development/SKILL.md) | `tools/skills/skill-development/` | Best practices for progressive disclosure skill design, structure, and metadata. |
| **Frontend & Motion Design** | [`frontend-design`](frontend-design/SKILL.md) | `tools/skills/frontend-design/` | Intentional visual layout and aesthetic direction overriding generic AI defaults. |
| | [`design-taste-frontend`](design-taste-frontend/SKILL.md) | `tools/skills/design-taste-frontend/` | Typography, spacing, micro-contrast, and dark-mode calibration rules. |
| | [`antigravity-ui-motion-design-expert`](antigravity-ui-motion-design-expert/SKILL.md) | `tools/skills/antigravity-ui-motion-design-expert/` | Spatial 3D CSS transforms, glassmorphism layers, and GSAP animation timelines. |
| | [`google-ux-fluidity`](google-ux-fluidity/SKILL.md) | `tools/skills/google-ux-fluidity/` | Material Design 3 (M3) UX fluidity, expressive curves, and tactile ripple states. |
| | [`google-stitch-integration`](google-stitch-integration/SKILL.md) | `tools/skills/google-stitch-integration/` | Ingests production-ready UI layout files and color tokens from Google Stitch. |
| | [`shadcn-context`](shadcn-context/SKILL.md) | `tools/skills/shadcn-context/` | Component schemas, props, and composition rules for shadcn/ui and Radix primitives. |
| | [`ui-ux-pro-max`](ui-ux-pro-max/SKILL.md) | `tools/skills/ui-ux-pro-max/` | Advanced UI/UX intelligence, dark-mode-first tokens, elevation layers, and editorial typography. |
| **Ecosystem & Workflow** | [`github-workflow`](github-workflow/SKILL.md) | `tools/skills/github-workflow/` | Canonical default workflow for issue anchoring, task tracking, verification, sync, and PRs. |
| | [`github-issue-pr-workflow`](github-issue-pr-workflow/SKILL.md) | `tools/skills/github-issue-pr-workflow/` | End-to-end issue-driven development, checkbox tracking, and PR dispatch lifecycle. |
| | [`portfolio-project-manager`](portfolio-project-manager/SKILL.md) | `tools/skills/portfolio-project-manager/` | Token-zero project onboarding engine for `AaradhyaDT.github.io` (auto IDs & AES encryption). |
| | [`feature-dev`](feature-dev/SKILL.md) | `tools/skills/feature-dev/` | Guided feature scoping, architecture decomposition, and requirements clarification. |
| | [`commit-commands`](commit-commands/SKILL.md) | `tools/skills/commit-commands/` | Semantic Git commits, branch hygiene, release commit invariants, and GitHub PR workflows. |
| | [`pr-review-toolkit`](pr-review-toolkit/SKILL.md) | `tools/skills/pr-review-toolkit/` | Multi-perspective code reviews (simplification, silent failure hunting, test quality). |
| | [`review-bugbot`](review-bugbot/SKILL.md) | `tools/skills/review-bugbot/` | Automated deep code review for silent regressions, race conditions, and concurrency bugs. |
| | [`split-to-prs`](split-to-prs/SKILL.md) | `tools/skills/split-to-prs/` | Splits large changesets and feature diffs into atomic, reviewer-friendly PR sequences. |
| | [`security-guidance`](security-guidance/SKILL.md) | `tools/skills/security-guidance/` | Security audits preventing secrets leakage, command injection, and SSRF vulnerabilities. |
| **System Automation & Forensics** | [`cyber-forensics`](cyber-forensics/SKILL.md) | `tools/skills/cyber-forensics/` | Windows DFIR triage, stealth evasion hunting, NTFS ADS detection, and cryptographic ledgers. |
| | [`win-vault`](win-vault/SKILL.md) | `tools/skills/win-vault/` | Windows folder locking, privacy vault management, and NTFS ACL administration. |
| | [`winpilot`](winpilot/SKILL.md) | `tools/skills/winpilot/` | Windows UI automation, screen perception, window management, and silent screenshot capture. |

---

## 🔄 Synchronization Protocol

To propagate updates between the repository mirror and the global Antigravity runtime:

- **Export from Local Repo to Global System:**
  ```powershell
  Copy-Item -Path "tools/skills/*" -Destination "$HOME/.gemini/config/skills" -Recurse -Force
  ```

- **Import from Global System into Local Repo:**
  ```powershell
  Copy-Item -Path "$HOME/.gemini/config/skills/*" -Destination "tools/skills" -Recurse -Force
  ```
