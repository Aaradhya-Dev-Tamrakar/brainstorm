"""
Cross-Platform Headless PDF Exporter for Compliance Reports.

Origin: BiasAperture (Fuse AI Fellowship Capstone Project)
License: MIT
Author: Aaradhya Dev Tamrakar (@AaradhyaDT)

This script discovers the native Blink engine (Chromium / Chrome / Edge)
across Windows, Linux, and macOS (with Windows discovery prioritized) to
deterministically compile standalone HTML audit dossiers into vector-crisp,
paginated PDFs without requiring heavy C-dependencies (Cairo/Pango/TeX).
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def find_blink_browser() -> Path:
    """
    Discovers an available Blink-based browser binary across platforms.
    Prioritizes Windows standard installations, followed by Linux and macOS.
    """
    # 1. Environment variable override
    if env_bin := os.environ.get("BIASAPERTURE_BROWSER_BIN"):
        p = Path(env_bin)
        if p.exists():
            return p

    # 2. Executable name discovery in PATH (Windows prioritized)
    search_names = [
        "chrome.exe",
        "msedge.exe",
        "chrome",
        "msedge",
        "google-chrome-stable",
        "google-chrome",
        "chromium-browser",
        "chromium",
        "microsoft-edge-stable",
        "microsoft-edge",
    ]
    for name in search_names:
        if found := shutil.which(name):
            return Path(found)

    # 3. Known OS filesystem locations (Windows prioritized)
    system = platform.system()
    candidates: list[Path] = []

    if system == "Windows":
        candidates = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
            Path(
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
                )
            ),
            Path(
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"
                )
            ),
        ]
    elif system == "Linux":
        candidates = [
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/google-chrome-stable"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
            Path("/usr/bin/microsoft-edge"),
            Path("/usr/bin/microsoft-edge-stable"),
            Path("/snap/bin/chromium"),
        ]
    elif system == "Darwin":
        candidates = [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ]

    for p in candidates:
        if p.exists():
            return p

    raise FileNotFoundError(
        f"No Blink-based browser (Chrome, Edge, Chromium) discovered on {system}. "
        "Please install Chromium/Chrome/Edge or set BIASAPERTURE_BROWSER_BIN."
    )


def convert_html_to_pdf(html_path: Path, pdf_path: Path | None = None) -> Path:
    """
    Converts a standalone HTML report into a publication-grade PDF file.

    Parameters
    ----------
    html_path : Path
        Absolute or relative path to source HTML report.
    pdf_path : Path | None
        Target path for generated PDF. Defaults to input path with .pdf extension.

    Returns
    -------
    Path
        Path to compiled PDF dossier.
    """
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        raise FileNotFoundError(f"Source HTML report not found: {html_file}")

    if pdf_path is None:
        target_pdf = html_file.with_suffix(".pdf")
    else:
        target_pdf = Path(pdf_path).resolve()

    target_pdf.parent.mkdir(parents=True, exist_ok=True)
    browser_bin = find_blink_browser()

    cmd = [
        str(browser_bin),
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        # Cross-platform / Docker container flags
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        f"--print-to-pdf={target_pdf}",
        str(html_file),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0 and not target_pdf.exists():
        raise RuntimeError(
            f"PDF compilation failed (exit code {result.returncode}):\n{result.stderr}"
        )

    return target_pdf


def compile_all_case_study_reports(report_dir: Path) -> list[Path]:
    """Compiles all HTML compliance reports found in report directory to PDF."""
    html_files = sorted(report_dir.glob("*.html"))
    compiled: list[Path] = []
    for h in html_files:
        out_pdf = h.with_suffix(".pdf")
        print(f"Compiling: {h.name} -> {out_pdf.name}...")
        res = convert_html_to_pdf(h, out_pdf)
        compiled.append(res)
    return compiled


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert standalone HTML compliance reports to PDF dossiers."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Path to input HTML file (or use --all to compile all reports in directory)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Optional path to output PDF file.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compile all HTML reports in directory to companion PDFs.",
    )

    args = parser.parse_args()

    if args.all or args.input is None:
        report_dir = Path.cwd()
        outputs = compile_all_case_study_reports(report_dir)
        print(f"\nSuccessfully compiled {len(outputs)} PDF reports in {report_dir}.")
    else:
        out = convert_html_to_pdf(args.input, args.output)
        print(f"Successfully exported PDF dossier: {out}")


if __name__ == "__main__":
    main()
