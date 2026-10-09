"""
tools/adaptive_engine.py
------------------------
Unified CLI Interface for the Deterministic Zero-AI Adaptive Workflow Engine.

Exposes deterministic commands:
  - flight-check: Antigravity memory guard & NovaOptimizer steady-state verification.
  - triage <task> [--files ...]: Decouples volume (V) & criticality (R) into matrix cells.
  - fast-path <task>: Detects zero-AI deterministic CLI commands.
  - cpm --dag-json <file>: Mathematical DAG schedule and slack solver.
  - fleet-task --title ... --repo ... --prompt ...: Declarative task JSON generator for Fleet.
  - snapshot [--tag ...]: Captures Git recovery snapshot in refs/backup/.
  - rollback [--tag ...]: Restores Git recovery snapshot.
"""

from __future__ import annotations

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Ensure brainstorm root is in sys.path
BRAINSTORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BRAINSTORM_ROOT not in sys.path:
    sys.path.insert(0, BRAINSTORM_ROOT)

from sim.adaptive_orchestrator import (
    AntigravityMemoryGovernor,
    DeterministicTriageEngine,
    DeterministicCPMScheduler,
    DAGCycleError,
    FleetFirstBridge,
    DeterministicTransactionalRecovery,
)


def cmd_flight_check(args: argparse.Namespace) -> int:
    """Checks RAM headroom against Antigravity reserve, NovaOptimizer thresholds, and router health."""
    status = AntigravityMemoryGovernor.get_memory_status()
    safe, msg = AntigravityMemoryGovernor.assert_headroom()
    router_telemetry = FleetFirstBridge.get_router_telemetry()
    output = {
        "memory_status": status,
        "headroom_assertion": {
            "passed": safe,
            "message": msg,
        },
        "nova_optimizer_state": status["nova_state"],
        "router_status": {
            "online": router_telemetry["port_1234_online"],
            "state": router_telemetry["current_state"],
            "telemetry": router_telemetry,
        },
    }
    print(json.dumps(output, indent=2))
    return 0 if safe else 1


def cmd_triage(args: argparse.Namespace) -> int:
    """Performs deterministic volume & criticality matrix triage."""
    files = args.files or []
    result = DeterministicTriageEngine.triage(
        task_description=args.task,
        file_paths=files if files else None,
        repo_root=BRAINSTORM_ROOT,
    )
    print(json.dumps(result, indent=2))
    return 0


def cmd_fast_path(args: argparse.Namespace) -> int:
    """Checks if incoming task can be satisfied instantly via Tier 0 deterministic CLI."""
    result = DeterministicTriageEngine.detect_fast_path(args.task)
    if result:
        print(json.dumps(result, indent=2))
        return 0
    else:
        output = {
            "is_fast_path": False,
            "message": "Task requires non-deterministic execution or domain reasoning.",
        }
        print(json.dumps(output, indent=2))
        return 1


def cmd_cpm(args: argparse.Namespace) -> int:
    """Calculates mathematical CPM schedule from DAG JSON specification."""
    dag_path = Path(args.dag_json)
    if not dag_path.exists():
        print(json.dumps({"error": f"DAG file '{args.dag_json}' not found."}, indent=2), file=sys.stderr)
        return 1

    try:
        with open(dag_path, "r", encoding="utf-8") as f:
            dag_data = json.load(f)
        tasks = dag_data.get("tasks", dag_data) if isinstance(dag_data, dict) else dag_data
        schedule = DeterministicCPMScheduler.calculate_schedule(tasks)
        print(json.dumps(schedule, indent=2))
        return 0
    except DAGCycleError as e:
        output = {
            "cycle_detected": True,
            "cycle_path": e.cycle,
            "unresolved_tasks": e.unresolved_tasks,
            "remediation": e.remediation,
            "error": str(e),
        }
        print(json.dumps(output, indent=2), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        return 1


def cmd_fleet_task(args: argparse.Namespace) -> int:
    """Generates task JSON for Fleet-Orchestrator cloud copilot execution."""
    manifest = FleetFirstBridge.create_fleet_task_manifest(
        title=args.title,
        repo=args.repo,
        prompt=args.prompt,
        priority=args.priority,
        output_dir=args.out_dir,
        kind=getattr(args, "kind", "code"),
        parent_id=getattr(args, "parent_id", None),
    )
    print(json.dumps(manifest, indent=2))
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    """Captures atomic Git recovery snapshot in refs/backup/."""
    success, msg = DeterministicTransactionalRecovery.create_snapshot(
        tag=args.tag, repo_root=BRAINSTORM_ROOT
    )
    print(json.dumps({"success": success, "message": msg}, indent=2))
    return 0 if success else 1


def cmd_rollback(args: argparse.Namespace) -> int:
    """Rolls back to recovery snapshot in refs/backup/."""
    ref = f"refs/backup/{args.tag}" if args.tag else "refs/backup/snapshot-1"
    success, msg = DeterministicTransactionalRecovery.rollback(
        snapshot_ref=ref, repo_root=BRAINSTORM_ROOT
    )
    print(json.dumps({"success": success, "message": msg}, indent=2))
    return 0 if success else 1


def cmd_fleet_status(args: argparse.Namespace) -> int:
    """Displays live status and remaining credit capacity of the 27-worker Copilot fleet."""
    fleet_script = Path(r"F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\tools\copilot_fleet.py")
    if not fleet_script.exists():
        print(json.dumps({"error": "copilot_fleet.py not found"}, indent=2), file=sys.stderr)
        return 1
    res = subprocess.run([sys.executable, str(fleet_script), "status"], check=False)
    return res.returncode


def cmd_fleet_merge(args: argparse.Namespace) -> int:
    """Merges a completed task worktree branch (task/<task_id>) into the current repository branch."""
    branch = f"task/{args.task_id}" if not args.task_id.startswith("task/") else args.task_id
    repo_root = Path(args.repo or BRAINSTORM_ROOT)

    # Check if branch exists
    res = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        print(json.dumps({"error": f"Branch '{branch}' does not exist in {repo_root}."}, indent=2), file=sys.stderr)
        return 1

    merge_res = subprocess.run(
        ["git", "merge", branch, "-m", f"feat(fleet): integrate completed task {args.task_id}"],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    success = (merge_res.returncode == 0)
    output = {
        "success": success,
        "branch": branch,
        "stdout": merge_res.stdout.strip(),
        "stderr": merge_res.stderr.strip(),
    }
    print(json.dumps(output, indent=2))
    return 0 if success else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified CLI for Deterministic Zero-AI Adaptive Workflow Engine."
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # flight-check
    p_flight = subparsers.add_parser("flight-check", help="Antigravity memory headroom check")
    p_flight.set_defaults(func=cmd_flight_check)

    # triage
    p_triage = subparsers.add_parser("triage", help="2D matrix task triage")
    p_triage.add_argument("task", help="Task prompt or description")
    p_triage.add_argument("--files", nargs="*", default=[], help="Target file paths")
    p_triage.set_defaults(func=cmd_triage)

    # fast-path
    p_fast = subparsers.add_parser("fast-path", help="Zero-AI deterministic fast path check")
    p_fast.add_argument("task", help="Task prompt or description")
    p_fast.set_defaults(func=cmd_fast_path)

    # cpm
    p_cpm = subparsers.add_parser("cpm", help="CPM topological DAG solver")
    p_cpm.add_argument("--dag-json", required=True, help="Path to DAG JSON file")
    p_cpm.set_defaults(func=cmd_cpm)

    # fleet-task
    p_fleet = subparsers.add_parser("fleet-task", help="Generate task JSON for Fleet-Orchestrator")
    p_fleet.add_argument("--title", required=True, help="Task title")
    p_fleet.add_argument("--repo", required=True, help="Repository name")
    p_fleet.add_argument("--prompt", required=True, help="Task prompt")
    p_fleet.add_argument("--priority", default="normal", help="Task priority")
    p_fleet.add_argument("--kind", default="code", choices=["code", "text"], help="Task kind (code or text)")
    p_fleet.add_argument("--parent-id", default=None, help="Parent task ID if subtask")
    p_fleet.add_argument("--out-dir", default=None, help="Output directory for task JSON")
    p_fleet.set_defaults(func=cmd_fleet_task)

    # snapshot
    p_snap = subparsers.add_parser("snapshot", help="Capture Git recovery snapshot")
    p_snap.add_argument("--tag", default=None, help="Snapshot tag name")
    p_snap.set_defaults(func=cmd_snapshot)

    # rollback
    p_roll = subparsers.add_parser("rollback", help="Restore Git recovery snapshot")
    p_roll.add_argument("--tag", default=None, help="Snapshot tag name")
    p_roll.set_defaults(func=cmd_rollback)

    # fleet-status
    p_status = subparsers.add_parser("fleet-status", help="Display live Copilot fleet capacity")
    p_status.set_defaults(func=cmd_fleet_status)

    # fleet-merge
    p_merge = subparsers.add_parser("fleet-merge", help="Merge completed task worktree branch")
    p_merge.add_argument("--task-id", required=True, help="Task ID or branch name (task/<task_id>)")
    p_merge.add_argument("--repo", default=None, help="Repository path (defaults to brainstorm)")
    p_merge.set_defaults(func=cmd_fleet_merge)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
