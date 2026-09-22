from typing import Dict, Any, List, Optional
from pathlib import Path
from pilot.core.auditor import FleetAuditSummary, RepoAuditResult

class ProfileSynthesizer:
    def __init__(self, config=None):
        self.config = config

    def generate_svg_radar(self, summary: FleetAuditSummary) -> str:
        """Generates a high-aesthetic, dark-glass SVG radar telemetry card."""
        health = int(summary.average_health_score)
        repos_count = summary.total_repos_scanned
        stars_count = summary.total_stars
        forks_count = summary.total_forks
        anomalies = summary.critical_anomalies_count

        # Compute language distribution
        lang_counts: Dict[str, int] = {}
        for r in summary.repos:
            if r.language:
                lang_counts[r.language] = lang_counts.get(r.language, 0) + 1
        
        top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:4]
        langs_str = " • ".join([f"{l[0]} ({l[1]})" for l in top_langs]) if top_langs else "Python • C++ • C# • Kotlin"

        # Health ring calculation (circumference = 2 * pi * r = 2 * 3.14159 * 36 ~= 226)
        circumference = 226
        stroke_dashoffset = int(circumference - (health / 100.0) * circumference)
        health_color = "#10b981" if health >= 80 else ("#f59e0b" if health >= 50 else "#ef4444")

        return f"""<svg width="680" height="200" viewBox="0 0 680 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.98"/>
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366f1" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#06b6d4" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="{health_color}"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="2" y="2" width="676" height="196" rx="16" fill="url(#cardGrad)" stroke="url(#borderGrad)" stroke-width="1.5"/>

  <!-- Header Section -->
  <g transform="translate(28, 32)">
    <circle cx="6" cy="6" r="4" fill="#10b981" filter="url(#glow)"/>
    <text x="18" y="10" fill="#f8fafc" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" letter-spacing="0.05em">AARADHYA ECOSYSTEM RADAR</text>
    <text x="320" y="10" fill="#64748b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11">ORCHESTRATED VIA GITHUB PILOT</text>
  </g>

  <!-- Metrics Grid -->
  <g transform="translate(28, 68)">
    <!-- Metric 1: Repos -->
    <text x="0" y="18" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="24" font-weight="800">{repos_count}</text>
    <text x="0" y="34" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="500">FLEET REPOSITORIES</text>

    <!-- Metric 2: Stars -->
    <text x="150" y="18" fill="#facc15" font-family="system-ui, sans-serif" font-size="24" font-weight="800">⭐ {stars_count}</text>
    <text x="150" y="34" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="500">COMMUNITY STARS</text>

    <!-- Metric 3: Forks -->
    <text x="290" y="18" fill="#a855f7" font-family="system-ui, sans-serif" font-size="24" font-weight="800">🍴 {forks_count}</text>
    <text x="290" y="34" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="500">ECOSYSTEM FORKS</text>
  </g>

  <!-- Languages Ribbon -->
  <g transform="translate(28, 142)">
    <rect width="440" height="28" rx="6" fill="#1e293b" fill-opacity="0.6"/>
    <text x="12" y="18" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" font-weight="500">⚡ Core Stacks: <tspan fill="#38bdf8">{langs_str}</tspan></text>
  </g>

  <!-- Health Ring Meter -->
  <g transform="translate(560, 95)">
    <circle cx="0" cy="0" r="36" stroke="#1e293b" stroke-width="8" fill="none"/>
    <circle cx="0" cy="0" r="36" stroke="url(#ringGrad)" stroke-width="8" stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}" stroke-linecap="round" fill="none" transform="rotate(-90)" filter="url(#glow)"/>
    <text x="0" y="6" text-anchor="middle" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="800">{health}%</text>
    <text x="0" y="48" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" font-weight="600">HEALTH SCORE</text>
  </g>
</svg>"""

    def render_profile_readme(self, summary: FleetAuditSummary, svg_relative_path: str = "./radar.svg") -> str:
        top_repos = sorted(summary.repos, key=lambda r: (r.stars, r.health_score), reverse=True)[:8]
        
        repo_rows = []
        for r in top_repos:
            lang_badge = f"`{r.language}`" if r.language else "`General`"
            desc = r.description or "High-agency autonomous module"
            health_color = "🟢" if r.health_score >= 80 else ("🟡" if r.health_score >= 50 else "🔴")
            repo_rows.append(f"| **[{r.name}](https://github.com/{r.owner}/{r.name})** | {lang_badge} | ⭐ {r.stars} | {health_color} {r.health_score}% | {desc} |")
        
        table_content = "\n".join(repo_rows) if repo_rows else "| No repositories indexed | - | - | - | - |"

        return f"""# Aaradhya Dev Tamrakar 🪐
### Computational R&D • Autonomous AI Systems • Systems Engineering

[![Orchestrated by GitHub Pilot](https://img.shields.io/badge/Orchestrated%20by-GitHub%20Pilot-6366f1.svg)](https://github.com/Aaradhya-Dev-Tamrakar/github-pilot)
[![Ecosystem Health](https://img.shields.io/badge/Fleet%20Health-{summary.average_health_score}%25-10b981.svg)](#)
[![Total Ecosystem Repos](https://img.shields.io/badge/Fleet%20Repos-{summary.total_repos_scanned}-38bdf8.svg)](#)
[![Token-Zero Core](https://img.shields.io/badge/Core-Token--Zero-emerald.svg)](https://github.com/Aaradhya-Dev-Tamrakar/github-pilot)

---

<div align="center">
  <img src="{svg_relative_path}" alt="Aaradhya Ecosystem Radar" width="680" />
</div>

---

### 🛠️ Active Ecosystem & Production Repositories

| Repository | Tech Stack | Stars | Health | Focus & Architecture |
| :--- | :--- | :--- | :--- | :--- |
{table_content}

---

### 🌐 Multi-Account Fleet Topology
- **Organization Hub**: [github.com/Aaradhya-Dev-Tamrakar](https://github.com/Aaradhya-Dev-Tamrakar) *(Core Tool R&D, Microservices, CAD & Wearables)*
- **Personal Workspace**: [github.com/AaradhyaDT](https://github.com/AaradhyaDT) *(Web Mirrors, Sandboxes, Constraint Solvers)*

---
<sub>*Continuously monitored and auto-synthesized by [GitHub Pilot](https://github.com/Aaradhya-Dev-Tamrakar/github-pilot) via Token-Zero local scripts.*</sub>
"""
