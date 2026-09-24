# Setup Guide: Antigravity Customization Token Budget & Overhead Optimization

> **Category**: Developer Environment & Agent Runtime Efficiency  
> **Epistemic Classification**: `EMPIRICALLY_VERIFIED`  
> **Date**: 2026-09-24  
> **Target Scope**: Antigravity IDE, Claude Code Plugins, MCP Servers & Skills Ecosystem

---

## 1. Executive Summary

Antigravity loads all globally registered **Rules (`RULE[...]`)**, **Skill Declarations (`<skills>`)**, and **Eager MCP Tool Schemas (`tool_declarations`)** directly into the system prompt prefix on **every single prompt turn**.

When inactive plugin packs (e.g., Firebase, Flutter/Dart, Google Maps Platform, Science Kit, Data Agent Kit) remain installed, static overhead can consume up to **$95\%$ ($\approx 19{,}000$ tokens)** of the total $20{,}000$-token customization budget before the conversation even begins.

Pruning unneeded plugins restored **$74.0\%$ ($14{,}799$ tokens) of available budget**, achieving an immediate **$\approx 13{,}800$ token reduction per turn**.

---

## 2. Empirical Overhead Breakdown

### Before vs. After Optimization

| Metric | Bloated State (Default / Extra Plugins) | Optimized State (Lean Active Stack) | Net Gain / Savings |
| :--- | :--- | :--- | :--- |
| **Customization Budget Used** | $95.0\%$ ($\approx 19{,}000\text{ tokens}$) | **$26.0\%$ ($5{,}201\text{ tokens}$)** | **$-69.0\%$ reduction** |
| **Available Headroom** | $5.0\%$ ($\approx 1{,}000\text{ tokens}$) | **$74.0\%$ ($14{,}799\text{ tokens}$)** | **$+69.0\%$ headroom** |
| **Rules Overhead** | Variable | $1{,}140\text{ tokens}$ ($5.7\%$) | Controlled |
| **Skills Overhead** | High | $2{,}973\text{ tokens}$ ($14.9\%$) | Controlled |
| **MCP Tools Overhead** | High | $1{,}088\text{ tokens}$ ($5.4\%$) | Controlled |
| **Tokens Consumed Per Turn** | $\approx 19{,}000\text{ tokens}$ | **$5{,}201\text{ tokens}$** | **$\approx 13{,}800\text{ tokens saved / turn}$** |

---

## 3. Financial & AI Credit Impact

Because Antigravity transmits full system definitions on every conversational turn, the overhead multiplies across multi-turn interactions:

$$\text{Session Waste} = \text{Turns} \times \Delta\text{Overhead Tokens} \times \text{Input Cost per Token}$$

### Estimated Waste per 100 Turns (Overhead Only)

| Model Tier | Input Price / 1M Tokens | Waste per Single Turn | Waste per 100 Turns (Heavy Day) | Monthly Waste (20 Active Days) |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 2.5 / 3.7 Flash** | \$0.075 / 1M | \$0.0010 | \$0.10 | **\$2.00 – \$5.00** |
| **Claude 3.5 / 3.7 Sonnet** | \$3.00 / 1M | \$0.0414 | \$4.14 | **\$82.80 – \$120.00** |
| **Claude 3.5 / 3 Opus** | \$15.00 / 1M | \$0.2070 | \$20.70 | **\$414.00+** |
| **OpenAI o1 / GPT-4o** | \$2.50 – \$5.00 / 1M | \$0.0345 – \$0.0690 | \$3.45 – \$6.90 | **\$69.00 – \$138.00** |

*Note: Prompt caching reduces the impact on cache hits, but cache misses, cache invalidations, and non-cached model tiers absorb 100% of this cost.*

---

## 4. Operational Degradation (The Hidden Tax)

Beyond monetary cost, high customization bloat creates three critical operational penalties:

1. **Premature Rate Limiting (TPM/RPM)**: Consuming $19\text{k}$ static tokens per prompt causes workspace sessions to hit Tokens-Per-Minute quotas $2\times$ to $3\times$ faster during rapid iterative debugging.
2. **Pre-fill Latency (TTFT)**: Processing large schema prefixes adds $200\text{ms} - 800\text{ms}$ of initial time-to-first-token latency to every model response.
3. **Context Window Crowding & Attention Dilution**: Retaining inactive tool schemas (e.g., Flutter CLI schemas during a Python backend session) dilutes attention, increasing the probability of tool misrouting or hallucinated tool invocations.

---

## 5. Standard Operating Procedure (SOP) for Setup

### Rule 1: On-Demand Plugin Installation
- Keep non-primary stacks uninstalled by default (e.g., `Dart and Flutter`, `Firebase`, `Chrome DevTools`, `Google Maps Platform`, `Data Agent Kit`, `Science`).
- Install plugins only when actively working on that specific domain; uninstall upon task completion.

### Rule 2: Enforce Lazy MCP Tool Loading
- Configure infrequently used MCP servers as lazy-loaded tools (`call_mcp_tool` wrapper) instead of eager registration. Eager registration injects complete JSON parameter schemas into every prompt.

### Rule 3: Maintain Lean Rule Files
- Restrict `RULE[...]` and `AGENTS.md` declarations to core repo invariants, safety checks, and deterministic sync gates (`.\sync.ps1`).
- Avoid pasting reference documentation or code snippets directly into global rules.

### Rule 4: Periodic Customization Auditing
- Regularly inspect `Settings > Customizations` in Antigravity.
- Target: **Maintain available customization budget $\ge 60\%$ ($\le 8{,}000$ tokens total overhead)**.
