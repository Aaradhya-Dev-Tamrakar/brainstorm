#!/usr/bin/env python3
"""
scaffold_semester.py
Generic academic semester scaffolder and syllabus extractor.
Parses master curriculum markdown/PDFs, creates per-subject folders with extracted syllabi,
centralizes past examination papers, and scaffolds modular elective candidate directories.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

def extract_markdown_section(content: str, header_regex: str, next_header_regex: str = None) -> str:
    match = re.search(header_regex, content, re.MULTILINE)
    if not match:
        return ""
    start = match.start()
    if next_header_regex:
        next_m = re.search(next_header_regex, content[match.end():], re.MULTILINE)
        if next_m:
            end = match.end() + next_m.start()
            return content[start:end].strip()
    return content[start:].strip()

def main():
    parser = argparse.ArgumentParser(description="Scaffold academic semester note repository")
    parser.add_argument("--syllabus", required=True, help="Path to master curriculum markdown file")
    parser.add_argument("--target-dir", required=True, help="Path to target semester directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview scaffolding without creating files")
    args = parser.parse_args()

    syl_path = Path(args.syllabus).resolve()
    target_dir = Path(args.target_dir).resolve()

    if not syl_path.exists():
        print(f"ERROR: Syllabus file not found: {syl_path}")
        sys.exit(1)

    print(f"=== Academic Semester Scaffolder ===")
    print(f"Syllabus: {syl_path}")
    print(f"Target Directory: {target_dir}")
    print(f"Dry Run: {args.dry_run}")

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "Past Qns").mkdir(parents=True, exist_ok=True)

    with open(syl_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Loaded syllabus ({len(content)} characters). Ready for extraction.")

if __name__ == "__main__":
    main()
