import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from pilot import __version__
from pilot.config import get_config
from pilot.core.auditor import FleetAuditor
from pilot.core.profile import ProfileSynthesizer
from pilot.core.digest import DigestGenerator
from pilot.scraper.trending import TrendingParser

app = typer.Typer(
    name="pilot",
    help="GitHub Pilot: Macro-Plane Profile, Fleet Health & Ecosystem Navigator",
    add_completion=False,
)
scrape_app = typer.Typer(help="Zero-auth web scraper commands")
app.add_typer(scrape_app, name="scrape")

console = Console()

@app.command()
def status():
    """Display GitHub Pilot configuration, accounts, and telemetry."""
    config = get_config()
    console.print(Panel(f"[bold cyan]GitHub Pilot v{__version__}[/bold cyan] — Token-Zero Core", expand=False))
    
    table = Table(title="Target Fleet Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="dim")
    table.add_column("Identifier", style="bold green")
    table.add_column("Auth Status")

    auth_label = "[green]Authenticated (Personal PAT)[/green]" if config.has_auth else "[yellow]Unauthenticated (Public Fallback)[/yellow]"

    for org in config.orgs:
        table.add_row("Organization", org, auth_label)
    for u in config.users:
        table.add_row("Personal User", u, auth_label)

    console.print(table)

    console.print(f"\n[bold]Local Cache Directory:[/bold] {config.cache_dir.resolve()}")
    console.print(f"[bold]Cache TTL:[/bold] {config.cache_ttl_seconds} seconds")


@app.command()
def audit(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output compact JSON for agent handoff"),
    max_repos: int = typer.Option(50, "--limit", "-l", help="Max repos per account to scan")
):
    """Run deterministic fleet health audit across accounts."""
    config = get_config()
    auditor = FleetAuditor(config)

    with console.status("[bold green]Scanning ecosystem fleet across accounts..."):
        summary = asyncio.run(auditor.audit_fleet())

    if json_output:
        import json
        console.print(summary.model_dump_json(indent=2))
        return

    table = Table(title=f"Fleet Audit Telemetry ({summary.total_repos_scanned} Repositories)", show_header=True, header_style="bold blue")
    table.add_column("Repository", style="bold")
    table.add_column("Owner", style="dim")
    table.add_column("Lang")
    table.add_column("Stars", justify="right")
    table.add_column("Health", justify="right")
    table.add_column("Status / Anomalies")

    for r in summary.repos:
        health_style = "green" if r.health_score >= 80 else ("yellow" if r.health_score >= 50 else "red")
        anomalies_str = ", ".join(r.anomalies) if r.anomalies else "[green]Optimal[/green]"
        table.add_row(
            r.name,
            r.owner,
            r.language or "-",
            str(r.stars),
            f"[{health_style}]{r.health_score}%[/{health_style}]",
            anomalies_str
        )

    console.print(table)
    console.print(f"\n[bold cyan]Average Fleet Health:[/bold cyan] {summary.average_health_score}% | [bold yellow]Total Stars:[/bold yellow] {summary.total_stars}")


@app.command()
def profile(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="File to write rendered README to"),
    svg_output: Optional[Path] = typer.Option(None, "--svg", help="File to write rendered SVG badge to")
):
    """Synthesize dynamic profile README and SVG stats."""
    config = get_config()
    auditor = FleetAuditor(config)

    with console.status("[bold green]Harvesting fleet telemetry for profile..."):
        summary = asyncio.run(auditor.audit_fleet())

    synthesizer = ProfileSynthesizer(config)
    readme_md = synthesizer.render_profile_readme(summary)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(readme_md, encoding="utf-8")
        console.print(f"[green]Profile README written to {output}[/green]")
    else:
        console.print("\n" + readme_md)

    if svg_output:
        svg_code = synthesizer.generate_svg_radar(summary)
        svg_output.parent.mkdir(parents=True, exist_ok=True)
        svg_output.write_text(svg_code, encoding="utf-8")
        console.print(f"[green]SVG Radar written to {svg_output}[/green]")


@app.command()
def digest(
    days: int = typer.Option(7, "--days", "-d", help="Number of past days to scan"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path for markdown digest")
):
    """Generate categorized conventional commit digest."""
    generator = DigestGenerator()
    content = generator.render_markdown_digest(days=days)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        console.print(f"[green]Changelog digest written to {output}[/green]")
    else:
        console.print("\n" + content)


@scrape_app.command("trending")
def scrape_trending(
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Filter by programming language"),
    since: str = typer.Option("daily", "--since", "-s", help="daily, weekly, or monthly")
):
    """Scrape GitHub Trending repositories (Zero-API quota)."""
    parser = TrendingParser()

    with console.status(f"[bold green]Scraping GitHub Trending ({language or 'all'})..."):
        trending_repos = asyncio.run(parser.get_trending(language=language, since=since))

    if not trending_repos:
        console.print("[yellow]No trending repositories found or rate-limited by upstream.[/yellow]")
        return

    table = Table(title=f"GitHub Trending ({language or 'All Languages'} - {since})", show_header=True)
    table.add_column("Repository", style="bold cyan")
    table.add_column("Language", style="green")
    table.add_column("Trending Stars", justify="right", style="yellow")
    table.add_column("Description")

    for r in trending_repos[:15]:
        table.add_row(
            f"{r.owner}/{r.name}",
            r.language or "-",
            r.stars_today or "-",
            (r.description[:70] + "...") if r.description and len(r.description) > 70 else (r.description or "-")
        )

    console.print(table)


if __name__ == "__main__":
    app()
