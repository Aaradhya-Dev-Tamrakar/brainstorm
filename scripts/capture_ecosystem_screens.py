#!/usr/bin/env python3
"""
capture_ecosystem_screens.py — Autonomous Ecosystem Working Screenshot & Visual Proof Engine
Part of PLAN-MEDIA-001 (Brainstorm & Portfolio Sync)

Integrates WinPilot (OS-level UI Automation & BitBlt) to capture, crop,
optimize, and package working screenshots for:
1. Canonical Portfolio (F:\\AaradhyaDT\\AaradhyaDT.github.io\\assets\\images\\projects\\)
2. Ecosystem Repositories (docs/assets/preview.png)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Prepend WinPilot to sys.path if running in winpilot virtualenv or default environment
WINPILOT_ROOT = Path(r"F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot")
if WINPILOT_ROOT.exists() and str(WINPILOT_ROOT) not in sys.path:
    sys.path.insert(0, str(WINPILOT_ROOT))

PORTFOLIO_ASSETS = Path(r"F:\AaradhyaDT\AaradhyaDT.github.io\assets\images\projects")
REGISTRY_PATH = Path(r"F:\Aaradhya-Dev-Tamrakar\brainstorm\schemas\ecosystem.registry.json")

PROJECT_SLUGS = [
    ("p-001", "gcsbr", "Gesture-Controlled Self-Balancing Robot"),
    ("p-002", "alpha-superapp", "Alpha Android Super-App"),
    ("p-003", "fuse-wk1-cardiac", "Fusemachines Wk 1 — Cardiac Event Data Wrangling"),
    ("p-004", "fuse-wk2-cust-api", "Fusemachines Wk 2 — Customer API App"),
    ("p-005", "fuse-wk3-text2sql", "Fusemachines Wk 3 — Text-to-SQL Agentic Pipeline"),
    ("p-006", "fuse-wk4-churn-ml", "Fusemachines Wk 4 — Telco Churn & CLV ML Pipeline"),
    ("p-007", "edge-ai-stability", "Edge AI Stability Detection System"),
    ("p-008", "fuse-wk5-ensemble", "Fusemachines Wk 5 — Telco Churn Tree-Based Ensemble Pipeline"),
    ("p-009", "fuse-wk6-prob", "Fusemachines Wk 6 — Probabilistic Models"),
    ("p-010", "nexus", "Nexus — Personal AI Operating System"),
    ("p-011", "fuse-wk7-segment", "Fusemachines Wk 7 — Customer Segmentation"),
    ("p-012", "prakopnet", "PrakopNet — Multi-Hazard Early Warning System"),
    ("p-013", "antenna-lab", "Antenna Lab Data Analysis"),
    ("p-014", "custom-processor-fsm", "Custom Processor FSM Design"),
    ("p-015", "react-workshop", "IEEE KEC React Workshop"),
    ("p-016", "fuse-wk8-forecast", "Fusemachines Wk 8 — Forecasting"),
    ("p-017", "fuse-wk9-neu-steel", "Fusemachines Wk 9 — NEU Steel Defect CNN"),
    ("p-018", "spark", "SPARK — Two-Layer Fall Detection Wearable"),
    ("p-019", "fuse-wk10-img-proc", "Fusemachines Wk 10 — Image Processing"),
    ("p-020", "ai-constraint-solver", "Cryptarithmetic Solver & API"),
    ("p-021", "pulse-live", "Pulse Live — Real-Time Interactive Polling Platform"),
    ("p-022", "fuse-wk11-vit", "Fusemachines Wk 11 — Vision Transformers"),
    ("p-023", "claude-desktop-dsp", "Claude Desktop Multi-Profile & Distributed Service Provisioning"),
    ("p-024", "fuse-wk12-ner", "Fusemachines Wk 12 — NER for Customer Support"),
    ("p-025", "biasaperture", "BiasAperture — Vision Fairness & Bias Audit"),
    ("p-026", "onm-case-study", "ONM Case Study — Fusemachines Inc."),
    ("p-027", "fuse-wk13-lstm", "Fusemachines Wk 13 — LSTM Text Classification"),
    ("p-028", "fuse-wk14-intent", "Fusemachines Wk 14 — Agentic Intent Routing"),
    ("p-029", "md2pdf", "md2pdf — Desktop Markdown to PDF Converter"),
    ("p-030", "nova-optimizer", "NovaOptimizer — Windows System Optimizer"),
    ("p-031", "super-nlm", "Super-NLM — Multi-Account NotebookLM Hub"),
    ("p-032", "strangler-ipu", "STRANGLER-IPU — Ingress Processing Unit Architecture"),
    ("p-033", "windows-pilot", "Windows Pilot — Semantic UIA & MCP Desktop Automation Engine"),
    ("p-034", "github-pilot", "GitHub Pilot — Multi-Account Fleet Auditor"),
    ("p-035", "localsend-mcp", "LocalSend MCP — Zero-Cloud LAN P2P File & Clipboard Transfer Bridge"),
    ("p-036", "google-classroom-mcp", "Google Classroom MCP — Academic Coursework Bridge"),
    ("p-037", "typora-mcp", "Typora MCP Server — Native Markdown Desktop Orchestration"),
    ("p-038", "nepali-ocr-ai", "Nepali OCR AI — Vision OCR, Varnavinyas & Transcoder"),
    ("p-039", "ieee-xtreme-archive", "IEEE-Xtreme Algorithmic Intelligence Archive & Xtreme-Bench"),
]


def cmd_scaffold(args):
    """Scaffold directory tree for all 39 projects in portfolio assets."""
    created = 0
    PORTFOLIO_ASSETS.mkdir(parents=True, exist_ok=True)
    for pid, slug, title in PROJECT_SLUGS:
        proj_dir = PORTFOLIO_ASSETS / slug
        if not proj_dir.exists():
            proj_dir.mkdir(parents=True, exist_ok=True)
            created += 1
            meta_path = proj_dir / "meta.json"
            meta = {
                "id": pid,
                "slug": slug,
                "title": title,
                "status": "pending_capture",
                "updated_at": datetime.now().isoformat(),
                "assets": []
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
    print(f"[+] Scaffolded {created} project media folders in: {PORTFOLIO_ASSETS}")


def cmd_status(args):
    """Print capture completion status across all 39 projects."""
    print("=" * 80)
    print(" ECOSYSTEM PROJECT WORKING SCREENSHOT STATUS (PLAN-MEDIA-001)")
    print("=" * 80)
    total = len(PROJECT_SLUGS)
    captured = 0
    for pid, slug, title in PROJECT_SLUGS:
        proj_dir = PORTFOLIO_ASSETS / slug
        hero_webp = proj_dir / "hero.webp"
        hero_png = proj_dir / "hero.png"
        has_hero = hero_webp.exists() or hero_png.exists()
        if has_hero:
            captured += 1
            status_str = "[VETTED] hero.webp" if hero_webp.exists() else "[PARTIAL] hero.png"
        else:
            status_str = "[PENDING]"
        print(f" {pid.ljust(6)} | {slug.ljust(24)} | {status_str.ljust(18)} | {title[:32]}")
    pct = (captured / total) * 100
    print("-" * 80)
    print(f" Total Projects: {total} | Captured: {captured} ({pct:.1f}%) | Pending: {total - captured}")
    print("=" * 80)


def cmd_capture_window(args):
    """Capture a live window using WinPilot BitBlt and save to project folder."""
    try:
        from PIL import Image
        from winpilot.core.window import find_window
        from winpilot.core.screen import Screen
    except ImportError as e:
        print(f"[-] Error: WinPilot dependencies not available ({e}).")
        print(r"    Please run using: F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe")
        sys.exit(1)

    proj_dir = PORTFOLIO_ASSETS / args.slug
    proj_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Searching for active window matching: '{args.title}'...")
    w = find_window(title_regex=args.title)
    if not w:
        print(f"[-] No window found matching title regex: '{args.title}'")
        sys.exit(1)

    print(f"[+] Found window: '{w.title}' (HWND: {w.hwnd})")
    w.focus()
    w.restore()

    raw_png = proj_dir / "hero.png"
    webp_hero = proj_dir / "hero.webp"

    saved, meta = Screen.capture_to_file(window_or_hwnd=w, dest_path=str(raw_png))
    if not saved or not raw_png.exists():
        print(f"[-] Capture failed for window: {w.title}")
        sys.exit(1)

    print(f"[+] Captured raw PNG: {raw_png} ({meta.get('width')}x{meta.get('height')})")

    # Convert to optimized WebP (<250KB)
    with Image.open(raw_png) as img:
        img_rgb = img.convert("RGB")
        img_rgb.save(webp_hero, format="WEBP", quality=args.quality, method=6)

    size_kb = webp_hero.stat().st_size / 1024
    print(f"[+] Converted to WebP: {webp_hero} ({size_kb:.1f} KB)")

    # Update metadata
    meta_path = proj_dir / "meta.json"
    meta_data = {
        "slug": args.slug,
        "title": w.title,
        "captured_at": datetime.now().isoformat(),
        "resolution": f"{meta.get('width')}x{meta.get('height')}",
        "webp_size_kb": round(size_kb, 2),
        "source": "WinPilot BitBlt GDI"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2)

    print(f"[+] Completed capture for project: {args.slug}")


def main():
    parser = argparse.ArgumentParser(description="Ecosystem Screenshot Capture Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scaffold
    subparsers.add_parser("scaffold", help="Scaffold directory structure for all projects")

    # status
    subparsers.add_parser("status", help="Print capture status table")

    # capture-window
    cap_parser = subparsers.add_parser("capture-window", help="Capture a live window for a project")
    cap_parser.add_argument("--slug", required=True, help="Project slug (e.g. nova-optimizer)")
    cap_parser.add_argument("--title", required=True, help="Window title regex pattern")
    cap_parser.add_argument("--quality", type=int, default=85, help="WebP compression quality (default: 85)")

    args = parser.parse_args()
    if args.command == "scaffold":
        cmd_scaffold(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "capture-window":
        cmd_capture_window(args)


if __name__ == "__main__":
    main()
