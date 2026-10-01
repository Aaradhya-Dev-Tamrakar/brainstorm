#!/usr/bin/env python3
"""
toggle_issue_task.py — Deterministic Task Checklist Toggler for GitHub Issues

Retrieves an issue's markdown body via GitHub CLI (`gh`), parses checklist items,
toggles one or more task states (`[ ]` <-> `[x]`), and updates the issue via `gh issue edit`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys


CHECKBOX_RE = re.compile(r"^(\s*[-*]\s*\[)([\sxX])(\]\s+)(.*)$")


def run_gh_command(cmd: list[str]) -> str:
    """Execute a gh CLI command and return stdout as string."""
    result = subprocess.run(
        ["gh", *cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        err = result.stderr.strip() or f"gh exited with code {result.returncode}"
        raise RuntimeError(f"GitHub CLI error: {err}")
    return result.stdout


def get_issue_body(issue_num: int, repo: str | None = None) -> tuple[str, str]:
    """Fetch issue title and body markdown via gh issue view."""
    cmd = ["issue", "view", str(issue_num), "--json", "title,body"]
    if repo:
        cmd.extend(["-R", repo])
    output = run_gh_command(cmd)
    data = json.loads(output)
    return data.get("title", ""), data.get("body", "")


def parse_tasks(body: str) -> list[dict]:
    """Extract all checkbox tasks with line numbers and completion status."""
    lines = body.splitlines()
    tasks = []
    for idx, line in enumerate(lines):
        match = CHECKBOX_RE.match(line)
        if match:
            is_checked = match.group(2).lower() == "x"
            task_text = match.group(4).strip()
            tasks.append({
                "line_idx": idx,
                "checked": is_checked,
                "text": task_text,
                "raw_line": line,
            })
    return tasks


def update_issue_body(
    body: str,
    target_indices: set[int],
    target_state: bool,
) -> tuple[str, list[dict]]:
    """Update checkboxes at specified line indices to the target state."""
    lines = body.splitlines()
    updated_tasks = []
    char = "x" if target_state else " "

    for idx in sorted(target_indices):
        if idx < len(lines):
            match = CHECKBOX_RE.match(lines[idx])
            if match:
                prefix = match.group(1)
                suffix = match.group(3)
                content = match.group(4)
                old_checked = match.group(2).lower() == "x"
                lines[idx] = f"{prefix}{char}{suffix}{content}"
                updated_tasks.append({
                    "line_idx": idx,
                    "old_state": old_checked,
                    "new_state": target_state,
                    "text": content.strip(),
                })

    return "\n".join(lines), updated_tasks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Toggle task checklist items in GitHub issue bodies via gh CLI."
    )
    parser.add_argument("--issue", "-i", type=int, required=True, help="GitHub issue number.")
    parser.add_argument("--repo", "-R", type=str, default=None, help="Target GitHub repository (owner/repo).")
    parser.add_argument("--task", "-t", type=str, default=None, help="Case-insensitive substring match for task.")
    parser.add_argument("--index", type=int, default=None, help="1-based index of task to toggle.")
    parser.add_argument("--all", action="store_true", help="Toggle all tasks in the issue.")
    parser.add_argument(
        "--state",
        choices=["done", "undone"],
        default="done",
        help="Target checkbox state: 'done' ([x]) or 'undone' ([ ]). Default is 'done'.",
    )
    parser.add_argument("--list", action="store_true", help="List all tasks and exit without modifying.")
    parser.add_argument("--dry-run", action="store_true", help="Print resulting markdown body without saving.")

    args = parser.parse_args()

    try:
        title, body = get_issue_body(args.issue, args.repo)
    except Exception as e:
        sys.stderr.write(f"Error fetching issue #{args.issue}: {e}\n")
        return 1

    tasks = parse_tasks(body)
    if not tasks:
        sys.stdout.write(f"Issue #{args.issue} ('{title}') contains no markdown checklist tasks.\n")
        return 0

    if args.list:
        sys.stdout.write(f"Tasks in Issue #{args.issue} ('{title}'):\n")
        for i, t in enumerate(tasks, 1):
            status = "[x]" if t["checked"] else "[ ]"
            sys.stdout.write(f"  {i}. {status} {t['text']}\n")
        return 0

    target_state = args.state == "done"
    matched_line_indices: set[int] = set()

    if args.all:
        for t in tasks:
            matched_line_indices.add(t["line_idx"])
    elif args.index is not None:
        idx_zero = args.index - 1
        if 0 <= idx_zero < len(tasks):
            matched_line_indices.add(tasks[idx_zero]["line_idx"])
        else:
            sys.stderr.write(f"Error: task index {args.index} out of range (1..{len(tasks)}).\n")
            return 1
    elif args.task:
        query = args.task.lower().strip()
        for t in tasks:
            if query in t["text"].lower():
                matched_line_indices.add(t["line_idx"])
        if not matched_line_indices:
            sys.stderr.write(f"No task matched query: '{args.task}'. Use --list to see available tasks.\n")
            return 1
    else:
        sys.stderr.write("Error: Must specify --task, --index, --all, or --list.\n")
        return 1

    new_body, updated = update_issue_body(body, matched_line_indices, target_state)

    if args.dry_run:
        sys.stdout.write(f"--- Dry Run: Updated Issue #{args.issue} Body ---\n")
        sys.stdout.write(new_body + "\n")
        return 0

    # Save via gh issue edit
    edit_cmd = ["issue", "edit", str(args.issue), "--body", new_body]
    if args.repo:
        edit_cmd.extend(["-R", args.repo])

    try:
        run_gh_command(edit_cmd)
    except Exception as e:
        sys.stderr.write(f"Failed to update issue #{args.issue}: {e}\n")
        return 1

    sys.stdout.write(f"Successfully updated Issue #{args.issue} ('{title}'):\n")
    for u in updated:
        prev = "[x]" if u["old_state"] else "[ ]"
        curr = "[x]" if u["new_state"] else "[ ]"
        sys.stdout.write(f"  {prev} -> {curr} {u['text']}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
