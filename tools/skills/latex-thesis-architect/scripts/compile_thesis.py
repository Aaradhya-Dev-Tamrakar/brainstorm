#!/usr/bin/env python3
"""
compile_thesis.py — Fast-Path LaTeX Thesis & Fellowship Report Compiler
Part of latex-thesis-architect skill.

Executes deterministic multi-pass LaTeX compilation:
1. Prefers `latexmk` if installed (using local .latexmkrc for glossaries & bibtex).
2. Falls back to deterministic multi-pass CLI:
   pdflatex -> makeglossaries -> bibtex -> pdflatex -> pdflatex
3. Analyzes output logs for warnings, overfull \hboxes, and missing references.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


def compile_with_latexmk(report_dir: Path, main_file: str) -> bool:
    print(f"[*] Compiling via latexmk in {report_dir}...")
    cmd = ["latexmk", "-pdf", "-synctex=1", "-interaction=nonstopmode", main_file]
    res = run_cmd(cmd, cwd=report_dir)
    if res.returncode != 0:
        print("[!] latexmk encountered errors during compilation.")
        return False
    return True


def compile_manual_multipass(report_dir: Path, base_name: str) -> bool:
    print(f"[*] Running multi-pass compilation for {base_name}.tex...")
    passes = [
        ["pdflatex", "-interaction=nonstopmode", f"{base_name}.tex"],
        ["makeglossaries", base_name],
        ["bibtex", base_name],
        ["pdflatex", "-interaction=nonstopmode", f"{base_name}.tex"],
        ["pdflatex", "-interaction=nonstopmode", f"{base_name}.tex"],
    ]

    for step in passes:
        prog = step[0]
        if not shutil.which(prog):
            if prog in ("makeglossaries", "bibtex"):
                print(f"[-] Optional tool '{prog}' not in PATH; skipping pass.")
                continue
            else:
                sys.stderr.write(f"Error: Required binary '{prog}' not found in PATH.\n")
                return False
        print(f"  -> Running {prog}...")
        res = run_cmd(step, cwd=report_dir)
        # Note: pdflatex may exit with 1 on warnings; check log instead

    pdf_file = report_dir / f"{base_name}.pdf"
    return pdf_file.exists()


def analyze_log(log_path: Path) -> None:
    if not log_path.exists():
        return
    content = log_path.read_text(encoding="utf-8", errors="ignore")

    undefined_refs = re.findall(r"LaTeX Warning: Reference `([^']+)' on page \d+ undefined", content)
    undefined_cites = re.findall(r"LaTeX Warning: Citation `([^']+)' on page \d+ undefined", content)
    overfull_boxes = len(re.findall(r"Overfull \\hbox", content))

    print("------------------------------------------------------------")
    print(f"Log Diagnostics: {log_path.name}")
    print(f"  Undefined References (??) : {len(undefined_refs)}")
    if undefined_refs:
        for r in undefined_refs[:5]:
            print(f"    - {r}")
        if len(undefined_refs) > 5:
            print(f"    ... and {len(undefined_refs)-5} more")

    print(f"  Undefined Citations [?]   : {len(undefined_cites)}")
    if undefined_cites:
        for c in undefined_cites[:5]:
            print(f"    - {c}")

    print(f"  Overfull \\hbox Warnings   : {overfull_boxes}")
    print("------------------------------------------------------------")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile LaTeX Thesis Report")
    parser.add_argument("report_dir", type=Path, nargs="?", default=Path("."), help="Path to report directory")
    parser.add_argument("--main", default="main.tex", help="Main tex file name (default: main.tex)")
    parser.add_argument("--force-manual", action="store_true", help="Force multi-pass pdflatex instead of latexmk")
    args = parser.parse_args()

    report_dir = args.report_dir.resolve()
    main_path = report_dir / args.main
    base_name = Path(args.main).stem

    if not main_path.exists():
        sys.stderr.write(f"Error: Master file '{args.main}' not found in {report_dir}\n")
        sys.exit(1)

    has_latexmk = shutil.which("latexmk") is not None and not args.force_manual

    success = False
    if has_latexmk:
        success = compile_with_latexmk(report_dir, args.main)
    else:
        success = compile_manual_multipass(report_dir, base_name)

    log_path = report_dir / f"{base_name}.log"
    analyze_log(log_path)

    pdf_path = report_dir / f"{base_name}.pdf"
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"[SUCCESS] PDF compiled successfully: {pdf_path} ({size_kb:.1f} KB)")
        sys.exit(0)
    else:
        print("[ERROR] PDF generation failed. Check the log above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
