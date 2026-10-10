#!/usr/bin/env python3
"""
audit_latex_thesis.py — Calm-Authority & Deterministic Integrity Linter for LaTeX Thesis Reports
Part of latex-thesis-architect skill.

Audits:
1. Calm-authority style (hype blacklist, marketing superlative detection)
2. Label & reference integrity (\\cref, \\Cref, \\ref without matching \\label)
3. BibTeX citation integrity (\\cite matches keys in references.bib)
4. Glossary & acronym coverage (\\gls, \\glspl match abbreviations.tex/symbols.tex)
5. Empirical rigor rules (n >= 30 sample size guards, 95% bootstrap CI, explicit cut-list)
6. Requirements formalization (FR-xxx and NFR-xxx IEEE 830 'shall' phrasing)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

BANNED_HYPE_WORDS = [
    "revolutionary",
    "revolutionize",
    "game-changing",
    "game changer",
    "groundbreaking",
    "unleash",
    "supercharge",
    "seamless",
    "seamlessly",
    "cutting-edge",
    "magic",
    "magical",
    "effortlessly",
    "next-gen",
    "next generation",
    "paradigm-shifting",
    "phenomenal",
    "ultimate",
    "miracle",
    "breakthrough system",
    "flawless",
    "incomparable",
]


def extract_regex_matches(pattern: str, text: str) -> List[str]:
    return re.findall(pattern, text)


def scan_tex_files(report_dir: Path) -> List[Path]:
    return list(report_dir.rglob("*.tex"))


def load_bib_keys(report_dir: Path) -> Set[str]:
    bib_files = list(report_dir.rglob("*.bib"))
    keys: Set[str] = set()
    for bib in bib_files:
        content = bib.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"@\w+\s*\{\s*([^,\s]+),", content):
            keys.add(match.group(1).strip())
    return keys


def load_acronym_keys(report_dir: Path) -> Set[str]:
    keys: Set[str] = set()
    frontmatter_dir = report_dir / "src" / "frontmatter"
    if frontmatter_dir.exists():
        for file_path in frontmatter_dir.glob("*.tex"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r"\\newacronym(?:\[[^\]]*\])?\{([^}]+)\}", content):
                keys.add(match.group(1).strip())
            for match in re.finditer(r"\\newglossaryentry\{([^}]+)\}", content):
                keys.add(match.group(1).strip())
    return keys


def audit_thesis(report_dir: Path) -> Dict[str, any]:
    tex_files = scan_tex_files(report_dir)
    bib_keys = load_bib_keys(report_dir)
    acronym_keys = load_acronym_keys(report_dir)

    all_labels: Set[str] = set()
    all_refs: List[Tuple[str, str, int]] = []  # (label, filepath, lineno)
    all_cites: List[Tuple[str, str, int]] = []  # (key, filepath, lineno)
    all_gls: List[Tuple[str, str, int]] = []  # (key, filepath, lineno)

    hype_violations: List[Dict[str, any]] = []
    file_contents: Dict[str, str] = {}

    for tex_path in tex_files:
        rel_path = str(tex_path.relative_to(report_dir))
        content = tex_path.read_text(encoding="utf-8", errors="ignore")
        file_contents[rel_path] = content

        lines = content.splitlines()
        in_verbatim = False
        for idx, line in enumerate(lines, start=1):
            if "\\begin{verbatim}" in line or "\\begin{lstlisting}" in line:
                in_verbatim = True
                continue
            if "\\end{verbatim}" in line or "\\end{lstlisting}" in line:
                in_verbatim = False
                continue
            if in_verbatim:
                continue

            # Strip comments
            comment_pos = line.find("%")
            code_line = line if comment_pos == -1 else line[:comment_pos]

            # 1. Hype words check
            lower_line = code_line.lower()
            for word in BANNED_HYPE_WORDS:
                if re.search(r"\b" + re.escape(word) + r"\b", lower_line):
                    hype_violations.append({
                        "file": rel_path,
                        "line": idx,
                        "word": word,
                        "snippet": line.strip()
                    })

            # 2. Extract labels
            for match in re.finditer(r"\\label\{([^}]+)\}", code_line):
                all_labels.add(match.group(1).strip())

            # 3. Extract refs (\cref, \Cref, \ref)
            for match in re.finditer(r"\\(?:cref|Cref|ref)\{([^}]+)\}", code_line):
                for single_ref in match.group(1).split(","):
                    all_refs.append((single_ref.strip(), rel_path, idx))

            # 4. Extract cites
            for match in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", code_line):
                for single_cite in match.group(1).split(","):
                    all_cites.append((single_cite.strip(), rel_path, idx))

            # 5. Extract glossaries
            for match in re.finditer(r"\\gls(?:pl)?\{([^}]+)\}", code_line):
                all_gls.append((match.group(1).strip(), rel_path, idx))

    # Cross-reference analysis
    broken_refs = [
        {"ref": ref, "file": f, "line": l}
        for ref, f, l in all_refs
        if ref and ref not in all_labels
    ]

    broken_cites = [
        {"cite": cite, "file": f, "line": l}
        for cite, f, l in all_cites
        if cite and cite not in bib_keys
    ]

    missing_acronyms = [
        {"key": key, "file": f, "line": l}
        for key, f, l in all_gls
        if acronym_keys and key not in acronym_keys and not key.startswith("symb:")
    ]

    # Empirical rigor analysis across all combined text
    combined_text = "\n".join(file_contents.values())

    # Sample size guard check
    has_sample_size_guard = bool(
        re.search(r"n\s*<\s*30|n\s*>=\s*30|n\s*\\ge\s*30|insufficient\s+sample|sparse\s+cohort", combined_text, re.IGNORECASE)
    )

    # Uncertainty quantification check (95% CI or bootstrap)
    has_ci_or_bootstrap = bool(
        re.search(r"confidence\s+interval|bootstrap|\bci\b|bca", combined_text, re.IGNORECASE)
    )

    # Scope boundaries and cut-list check
    has_cutlist_or_limitations = bool(
        re.search(r"cut-list|descop|limitations|non-goals|out of scope", combined_text, re.IGNORECASE)
    )

    # IEEE 830 'shall' phrasing check in requirements
    req_file_key = next((k for k in file_contents if "requirements" in k.lower()), None)
    req_shall_count = 0
    if req_file_key:
        req_shall_count = len(re.findall(r"\bshall\b", file_contents[req_file_key], re.IGNORECASE))

    audit_passed = (
        len(hype_violations) == 0
        and len(broken_refs) == 0
        and len(broken_cites) == 0
        and has_sample_size_guard
        and has_ci_or_bootstrap
        and has_cutlist_or_limitations
    )

    return {
        "audit_passed": audit_passed,
        "summary": {
            "tex_files_scanned": len(tex_files),
            "bib_keys_indexed": len(bib_keys),
            "acronym_keys_indexed": len(acronym_keys),
            "labels_defined": len(all_labels),
            "references_checked": len(all_refs),
            "citations_checked": len(all_cites),
            "hype_violations_count": len(hype_violations),
            "broken_refs_count": len(broken_refs),
            "broken_cites_count": len(broken_cites),
            "missing_acronyms_count": len(missing_acronyms),
            "has_sample_size_guard": has_sample_size_guard,
            "has_ci_or_bootstrap": has_ci_or_bootstrap,
            "has_cutlist_or_limitations": has_cutlist_or_limitations,
            "requirements_shall_count": req_shall_count,
        },
        "hype_violations": hype_violations,
        "broken_refs": broken_refs,
        "broken_cites": broken_cites,
        "missing_acronyms": missing_acronyms,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit LaTeX Thesis Report for Calm Authority & Structural Integrity")
    parser.add_argument("report_dir", type=Path, help="Directory containing the LaTeX thesis report")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    if not args.report_dir.exists():
        sys.stderr.write(f"Error: Directory not found at {args.report_dir}\n")
        sys.exit(1)

    results = audit_thesis(args.report_dir)

    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0 if results["audit_passed"] else 1)

    print("============================================================")
    print("      LaTeX Thesis Calm-Authority & Integrity Audit         ")
    print("============================================================")
    s = results["summary"]
    print(f"Scanned: {s['tex_files_scanned']} .tex files | {s['bib_keys_indexed']} BibTeX keys | {s['acronym_keys_indexed']} Acronym keys")
    print(f"Labels:  {s['labels_defined']} defined | {s['references_checked']} references checked")
    print("------------------------------------------------------------")
    print(f"Hype / Superlative Violations : {s['hype_violations_count']}")
    print(f"Broken References (??)        : {s['broken_refs_count']}")
    print(f"Missing BibTeX Citations      : {s['broken_cites_count']}")
    print(f"Missing Acronym Keys          : {s['missing_acronyms_count']}")
    print(f"Sample Size Guard (n >= 30)   : {'[PASS]' if s['has_sample_size_guard'] else '[FAIL]'}")
    print(f"Uncertainty (95% CI / Boot)   : {'[PASS]' if s['has_ci_or_bootstrap'] else '[FAIL]'}")
    print(f"Explicit Scope / Cut-Lists    : {'[PASS]' if s['has_cutlist_or_limitations'] else '[FAIL]'}")
    print(f"Requirements 'Shall' Phrasing : {s['requirements_shall_count']} occurrences")
    print("------------------------------------------------------------")

    if results["hype_violations"]:
        print("\n[!] Banned Hype Words Detected:")
        for h in results["hype_violations"]:
            print(f"  {h['file']}:{h['line']} -> \"{h['word']}\" in: {h['snippet']}")

    if results["broken_refs"]:
        print("\n[!] Broken References (Undefined Labels):")
        for r in results["broken_refs"]:
            print(f"  {r['file']}:{r['line']} -> \\ref{{{r['ref']}}}")

    if results["broken_cites"]:
        print("\n[!] Missing BibTeX Citations:")
        for c in results["broken_cites"]:
            print(f"  {c['file']}:{c['line']} -> \\cite{{{c['cite']}}}")

    print("============================================================")
    if results["audit_passed"]:
        print("RESULT: AUDIT PASSED. Document complies with Calm Authority & Structural Invariants.")
        sys.exit(0)
    else:
        print("RESULT: AUDIT FAILED. Please remediate the flagged violations above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
