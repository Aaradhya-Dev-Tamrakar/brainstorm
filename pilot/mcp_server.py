import json
import asyncio
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

from pilot.config import get_config
from pilot.core.auditor import FleetAuditor
from pilot.core.profile import ProfileSynthesizer
from pilot.core.digest import DigestGenerator
from pilot.scraper.trending import TrendingParser

mcp = FastMCP("github-pilot")

@mcp.tool()
async def get_fleet_health(limit: int = 50) -> str:
    """Audit repository hygiene, license compliance, and CI health across multi-account GitHub fleet. Emits compact JSON."""
    auditor = FleetAuditor()
    summary = await auditor.audit_fleet(max_repos=limit)
    return summary.model_dump_json(indent=2)

@mcp.tool()
async def scrape_trending(language: Optional[str] = None, since: str = "daily") -> str:
    """Zero-auth web scrape of GitHub trending repositories without consuming API quota."""
    parser = TrendingParser()
    repos = await parser.get_trending(language=language or None, since=since)
    return json.dumps([r.model_dump() for r in repos[:15]], indent=2)

@mcp.tool()
def get_changelog_digest(days: int = 7) -> str:
    """Generate categorized conventional commit changelog digest across git tracking branches."""
    gen = DigestGenerator()
    return gen.render_markdown_digest(days=days)

@mcp.tool()
async def generate_profile_assets(output_dir: str = "./assets") -> str:
    """Synthesizes dynamic SVG radar badge and profile README markdown."""
    auditor = FleetAuditor()
    summary = await auditor.audit_fleet()
    syn = ProfileSynthesizer()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    readme = syn.render_profile_readme(summary)
    (out / "README.md").write_text(readme, encoding="utf-8")
    
    svg = syn.generate_svg_radar(summary)
    (out / "radar.svg").write_text(svg, encoding="utf-8")
    return f"Profile assets generated in {output_dir}: README.md and radar.svg ({summary.total_repos_scanned} repos indexed)"

if __name__ == "__main__":
    mcp.run(transport="stdio")
