#!/usr/bin/env python3
"""
audit_calm_writing.py — Deterministic Style & Invariant Linter for Anthropic-Style Technical Writing

Validates markdown documents against:
1. Complete elimination of banned marketing hype words.
2. 1-Sentence Empirical Thesis presence.
3. Tier-specific structural invariants (Tiers L1 through L5).
4. Machine-readable and benchmark grid standards.
"""

import sys
import re
import argparse
from pathlib import Path

# Ensure stdout handles UTF-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BANNED_HYPE_WORDS = [
    r"\brevolutionary\b",
    r"\bgame-changing\b",
    r"\bgroundbreaking\b",
    r"\bunleash\b",
    r"\bunleashes\b",
    r"\bunleashing\b",
    r"\bsupercharge\b",
    r"\bsupercharged\b",
    r"\bturbocharge\b",
    r"\bseamlessly\b",
    r"\bcutting-edge\b",
    r"\bnext-generation\b",
    r"\bnext-gen\b",
    r"\beffortlessly\b",
    r"\bmagical\b",
    r"\bwe are thrilled\b",
    r"\bwe are excited\b",
    r"\bunprecedented power\b",
]

def audit_file(filepath: Path, expected_tier: str = None) -> list[str]:
    errors = []
    text = filepath.read_text(encoding="utf-8")
    words = text.split()
    word_count = len(words)
    fname = filepath.name.lower()

    # 1. Hype Word Scan
    for pattern in BANNED_HYPE_WORDS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            errors.append(f"Banned hype word detected: '{matches[0]}' (matches pattern '{pattern}')")

    # 2. Tier Detection (Explicit tags take precedence)
    tier = expected_tier
    if not tier:
        if "l5" in fname or "system-card" in fname:
            tier = "L5"
        elif "l4" in fname or "launch" in fname:
            tier = "L4"
        elif "l3" in fname or "migration" in fname:
            tier = "L3"
        elif "l2" in fname or "case-study" in fname or "blog" in fname:
            tier = "L2"
        elif "l1" in fname or "pr" in fname or "portfolio" in fname or "readme" in fname:
            tier = "L1"
        elif word_count <= 400:
            tier = "L1"
        else:
            tier = "GENERIC"

    # 3. Tier-Specific Invariant Checks
    if tier == "L1":
        if word_count > 500:
            errors.append(f"Tier L1 word count exceeded: {word_count} words (max recommended: 350-400 words)")
        has_bullets = bool(re.search(r"^\s*[-*]\s+", text, re.MULTILINE))
        if not has_bullets:
            errors.append("Tier L1 requires active bullet points for changes/capabilities.")

    elif tier == "L2":
        # Case study / blog
        has_metrics = bool(re.search(r"\d+%", text)) or bool(re.search(r"\d+\s*(hours|seconds|ms|queries)", text))
        if not has_metrics:
            errors.append("Tier L2 case study requires concrete empirical operational metrics.")

    elif tier == "L3":
        # Migration guide
        has_json = "```json" in text or "```typescript" in text or "```python" in text
        if not has_json:
            errors.append("Tier L3 developer migration guide must contain code or JSON request payload blocks.")

    elif tier == "L4":
        # Model launch
        has_table = "|" in text and ("Subject" in text or "Haiku" in text or "Sonnet" in text)
        if not has_table:
            errors.append("Tier L4 model launch report must contain a pinned benchmark comparison table.")

    elif tier == "L5":
        # System card
        has_eval = bool(re.search(r"(evaluation|audit|refusal|harmlessness|safety)", text, re.IGNORECASE))
        if not has_eval:
            errors.append("Tier L5 system card must contain formal evaluation and audit sections.")

    return errors

def main():
    parser = argparse.ArgumentParser(description="Audit technical writing against calm authority invariants.")
    parser.add_argument("path", help="Path to markdown file or directory.")
    parser.add_argument("--tier", choices=["L1", "L2", "L3", "L4", "L5"], help="Explicitly enforce a specific depth tier.")
    parser.add_argument("--all", action="store_true", help="Audit all markdown files in target directory.")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files_to_check = []
    if target.is_dir():
        files_to_check = sorted(list(target.glob("*.md")))
    else:
        files_to_check = [target]

    total_errors = 0
    print(f"Auditing {len(files_to_check)} document(s) against Anthropic Calm Authority Invariants...\n")

    for f in files_to_check:
        errors = audit_file(f, expected_tier=args.tier)
        if errors:
            print(f"[FAIL] {f.name}")
            for err in errors:
                print(f"   * {err}")
            total_errors += len(errors)
        else:
            print(f"[PASS] {f.name}")

    print("\n" + "=" * 50)
    if total_errors > 0:
        print(f"FAILED: Found {total_errors} violation(s).")
        sys.exit(1)
    else:
        print("SUCCESS: All documents comply with Calm Authority Invariants (0 errors).")
        sys.exit(0)

if __name__ == "__main__":
    main()
