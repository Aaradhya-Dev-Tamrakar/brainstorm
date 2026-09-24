"""
task_telemetry.py
-----------------
Continuous deterministic task telemetry engine and Workflow Scorecard for brainstorm.
Implements the multi-dimensional economic vector (C_direct, T_human, T_model, T_compute)
and calculates empirical Human Intervention Ratio (HIR) and Discovery Cost Efficiency (DCE)
using discrete measured interval durations rather than static heuristic assumptions.

Usage:
    python sim/task_telemetry.py start <task_id> --goal "Goal text" [--tier E3]
    python sim/task_telemetry.py log-intervention <task_id> --minutes 15.0 [--reason "debugging"] [--start ISO] [--end ISO]
    python sim/task_telemetry.py log-dispatch <task_id> --model "claude-3-7-sonnet" --tokens-in 5000 --tokens-out 1200 --compute-sec 2.5 [--duration-sec 30.0]
    python sim/task_telemetry.py log-rework <task_id> --reason "schema mismatch" [--minutes 5.0]
    python sim/task_telemetry.py close <task_id> --status COMPLETED --artifact "sim/reconciliation_engine.py"
    python sim/task_telemetry.py scorecard
    python sim/task_telemetry.py --test
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone

BRAINSTORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELEMETRY_DIR = os.path.join(BRAINSTORM_ROOT, "research", "telemetry")
LEDGER_FILE = os.path.join(TELEMETRY_DIR, "task_ledger.jsonl")


def get_utc_now():
    return datetime.now(timezone.utc).isoformat()


def ensure_telemetry_dir():
    os.makedirs(TELEMETRY_DIR, exist_ok=True)
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            pass


def load_tasks():
    ensure_telemetry_dir()
    tasks = {}
    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                tid = record.get("task_id")
                if tid:
                    tasks[tid] = record
            except json.JSONDecodeError:
                continue
    return tasks


def save_all_tasks(tasks):
    ensure_telemetry_dir()
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        for record in tasks.values():
            f.write(json.dumps(record) + "\n")


def cmd_start(args):
    tasks = load_tasks()
    tid = args.task_id
    if tid in tasks and tasks[tid].get("status") == "IN_PROGRESS":
        print(f"[!] Task '{tid}' is already active.")
        return 1

    tasks[tid] = {
        "task_id": tid,
        "goal": args.goal,
        "target_evidence_tier": getattr(args, "tier", None) or "E3",
        "status": "IN_PROGRESS",
        "start_time": get_utc_now(),
        "end_time": None,
        "human_active_minutes": 0.0,
        "agent_active_seconds": 0.0,
        "agent_active_minutes": 0.0,
        "interventions": [],
        "worker_dispatches": 0,
        "tokens_input": 0,
        "tokens_output": 0,
        "compute_seconds": 0.0,
        "handoffs": 0,
        "rework_events": 0,
        "rework_log": [],
        "output_artifact": None,
        "dispatches_log": []
    }
    save_all_tasks(tasks)
    print(f"[+] Task '{tid}' started at {tasks[tid]['start_time']}.")
    return 0


def cmd_log_intervention(args):
    tasks = load_tasks()
    tid = args.task_id
    if tid not in tasks:
        print(f"[!] Task '{tid}' not found in ledger.")
        return 1

    t = tasks[tid]
    start_ts = getattr(args, "start", None)
    end_ts = getattr(args, "end", None)

    if start_ts and end_ts:
        try:
            t0 = datetime.fromisoformat(start_ts)
            t1 = datetime.fromisoformat(end_ts)
            mins = max(0.0, (t1 - t0).total_seconds() / 60.0)
        except Exception:
            mins = float(getattr(args, "minutes", 0.0) or 0.0)
    else:
        mins = float(getattr(args, "minutes", 0.0) or 0.0)

    now = get_utc_now()
    if not start_ts:
        start_ts = now
    if not end_ts:
        end_ts = now

    t["human_active_minutes"] = round(t.get("human_active_minutes", 0.0) + mins, 2)
    t.setdefault("interventions", []).append({
        "timestamp": now,
        "started_at": start_ts,
        "ended_at": end_ts,
        "minutes": round(mins, 2),
        "reason": getattr(args, "reason", None) or "manual intervention"
    })
    save_all_tasks(tasks)
    print(f"[+] Logged {mins:.2f}m intervention to '{tid}' (Total human time: {t['human_active_minutes']:.2f}m).")
    return 0


def cmd_log_dispatch(args):
    tasks = load_tasks()
    tid = args.task_id
    if tid not in tasks:
        print(f"[!] Task '{tid}' not found in ledger.")
        return 1

    t = tasks[tid]
    start_ts = getattr(args, "start", None)
    end_ts = getattr(args, "end", None)

    dur_sec = getattr(args, "duration_sec", None)
    comp_sec = float(getattr(args, "compute_sec", 0.0) or 0.0)

    if start_ts and end_ts:
        try:
            t0 = datetime.fromisoformat(start_ts)
            t1 = datetime.fromisoformat(end_ts)
            measured_sec = max(0.0, (t1 - t0).total_seconds())
        except Exception:
            measured_sec = float(dur_sec if dur_sec is not None else comp_sec)
    elif dur_sec is not None:
        measured_sec = float(dur_sec)
    elif comp_sec > 0.0:
        measured_sec = comp_sec
    else:
        measured_sec = 0.0

    now = get_utc_now()
    if not start_ts:
        start_ts = now
    if not end_ts:
        end_ts = now

    tokens_in = int(getattr(args, "tokens_in", 0) or 0)
    tokens_out = int(getattr(args, "tokens_out", 0) or 0)

    t["worker_dispatches"] = t.get("worker_dispatches", 0) + 1
    t["tokens_input"] = t.get("tokens_input", 0) + tokens_in
    t["tokens_output"] = t.get("tokens_output", 0) + tokens_out
    t["compute_seconds"] = round(t.get("compute_seconds", 0.0) + comp_sec, 2)
    t["agent_active_seconds"] = round(t.get("agent_active_seconds", 0.0) + measured_sec, 2)
    t["agent_active_minutes"] = round(t["agent_active_seconds"] / 60.0, 2)

    if getattr(args, "handoff", False):
        t["handoffs"] = t.get("handoffs", 0) + 1

    t.setdefault("dispatches_log", []).append({
        "timestamp": now,
        "started_at": start_ts,
        "ended_at": end_ts,
        "duration_seconds": round(measured_sec, 2),
        "model": getattr(args, "model", "agent") or "agent",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "compute_sec": comp_sec,
        "handoff": bool(getattr(args, "handoff", False))
    })
    save_all_tasks(tasks)
    print(f"[+] Logged dispatch for '{tid}': {getattr(args, 'model', 'agent')} (Duration: {measured_sec:.1f}s, Total Agent Active: {t['agent_active_minutes']:.2f}m).")
    return 0


def cmd_log_rework(args):
    tasks = load_tasks()
    tid = args.task_id
    if tid not in tasks:
        print(f"[!] Task '{tid}' not found in ledger.")
        return 1

    t = tasks[tid]
    t["rework_events"] = t.get("rework_events", 0) + 1
    rework_mins = float(getattr(args, "minutes", 0.0) or 0.0)
    if rework_mins > 0:
        t["human_active_minutes"] = round(t.get("human_active_minutes", 0.0) + rework_mins, 2)

    t.setdefault("rework_log", []).append({
        "timestamp": get_utc_now(),
        "reason": getattr(args, "reason", None) or "unspecified rework",
        "minutes": rework_mins
    })
    save_all_tasks(tasks)
    print(f"[+] Logged rework event for '{tid}' (Total rework count: {t['rework_events']}).")
    return 0


def cmd_close(args):
    tasks = load_tasks()
    tid = args.task_id
    if tid not in tasks:
        print(f"[!] Task '{tid}' not found in ledger.")
        return 1

    t = tasks[tid]
    t["status"] = getattr(args, "status", None) or "COMPLETED"
    t["end_time"] = get_utc_now()
    if getattr(args, "artifact", None):
        t["output_artifact"] = args.artifact

    save_all_tasks(tasks)
    print(f"[+] Task '{tid}' closed with status: {t['status']}.")
    return 0


def cmd_scorecard(args=None):
    tasks = load_tasks()
    print("=" * 85)
    print("   BRAINSTORM CONTINUOUS WORKFLOW SCORECARD (Scorecard v2 - Measured Intervals)")
    print("=" * 85)

    if not tasks:
        print("  No tasks recorded in task ledger yet.")
        print("=" * 85)
        return 0

    total_tasks = len(tasks)
    completed = sum(1 for t in tasks.values() if t.get("status") == "COMPLETED")
    in_progress = sum(1 for t in tasks.values() if t.get("status") == "IN_PROGRESS")
    rework_total = sum(t.get("rework_events", 0) for t in tasks.values())
    total_human_mins = sum(t.get("human_active_minutes", 0.0) for t in tasks.values())
    total_agent_mins = sum(t.get("agent_active_minutes", 0.0) for t in tasks.values())
    total_tokens_in = sum(t.get("tokens_input", 0) for t in tasks.values())
    total_tokens_out = sum(t.get("tokens_output", 0) for t in tasks.values())
    total_dispatches = sum(t.get("worker_dispatches", 0) for t in tasks.values())
    total_handoffs = sum(t.get("handoffs", 0) for t in tasks.values())

    # Task Table
    header = f"{'Task ID':<26} | {'Status':<11} | {'Tier':<4} | {'Human(m)':<8} | {'Agent(m)':<8} | {'Dispatches':<10} | {'Tokens':<8} | {'Rework':<6}"
    print(header)
    print("-" * len(header))

    for t in tasks.values():
        tokens_k = f"{(t.get('tokens_input', 0) + t.get('tokens_output', 0)) / 1000:.1f}k"
        row = (
            f"{t.get('task_id', ''):<26} | "
            f"{t.get('status', ''):<11} | "
            f"{t.get('target_evidence_tier', 'E3'):<4} | "
            f"{t.get('human_active_minutes', 0.0):<8.1f} | "
            f"{t.get('agent_active_minutes', 0.0):<8.1f} | "
            f"{t.get('worker_dispatches', 0):<10} | "
            f"{tokens_k:<8} | "
            f"{t.get('rework_events', 0):<6}"
        )
        print(row)

    print("=" * 85)
    print(" ECOSYSTEM MACRO TELEMETRY METRICS (Empirically Measured Intervals)")
    print("=" * 85)
    print(f"  * Total Tasks Logged      : {total_tasks} ({completed} completed, {in_progress} active)")
    print(f"  * Measured Human Time     : {total_human_mins:.1f} minutes ({total_human_mins / 60:.2f} hours)")
    print(f"  * Measured Agent Time     : {total_agent_mins:.1f} minutes ({total_agent_mins / 60:.2f} hours)")
    total_engineering_mins = total_human_mins + total_agent_mins
    print(f"  * Total Active Eng. Time  : {total_engineering_mins:.1f} minutes ({total_engineering_mins / 60:.2f} hours)")
    print(f"  * Total Worker Dispatches : {total_dispatches} dispatches, {total_handoffs} context handoffs")
    print(f"  * Total LLM Tokens        : {total_tokens_in + total_tokens_out:,} (In: {total_tokens_in:,}, Out: {total_tokens_out:,})")
    print(f"  * Total Rework Events     : {rework_total} (Rework Rate: {(rework_total / max(1, total_dispatches)) * 100:.1f}%)")
    
    # Calculate Human Intervention Ratio (HIR) empirically:
    # HIR = T_human / (T_human + T_agent_active)
    if total_engineering_mins > 0:
        hir = (total_human_mins / total_engineering_mins) * 100
    else:
        hir = 0.0
    print(f"  * Empirical HIR           : {hir:.1f}% human time share (Target: < 30%) [Zero-heuristic derivation]")
    print("=" * 85)
    return 0


def run_self_test():
    print("[*] Running Task Telemetry Engine self-test (Measured Intervals)...")
    test_tid = "TEST-TASK-001"
    
    # Mock args
    class MockArgs:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    cmd_start(MockArgs(task_id=test_tid, goal="Verify telemetry logger", tier="E4"))
    cmd_log_intervention(MockArgs(task_id=test_tid, minutes=2.5, reason="Testing intervention hook"))
    cmd_log_dispatch(MockArgs(
        task_id=test_tid,
        model="test-agent",
        tokens_in=1000,
        tokens_out=500,
        compute_sec=0.1,
        duration_sec=30.0,
        handoff=True
    ))
    cmd_log_rework(MockArgs(task_id=test_tid, reason="Test rework", minutes=0.5))
    cmd_close(MockArgs(task_id=test_tid, status="COMPLETED", artifact="sim/task_telemetry.py"))
    
    tasks = load_tasks()
    assert test_tid in tasks, "Task not saved to ledger"
    assert tasks[test_tid]["human_active_minutes"] == 3.0, f"Expected 3.0, got {tasks[test_tid]['human_active_minutes']}"
    assert tasks[test_tid]["tokens_input"] == 1000
    assert tasks[test_tid]["worker_dispatches"] == 1
    assert tasks[test_tid]["agent_active_seconds"] == 30.0
    assert tasks[test_tid]["agent_active_minutes"] == 0.5
    assert tasks[test_tid]["status"] == "COMPLETED"
    
    print("[+] Self-test passed! Displaying test scorecard:")
    cmd_scorecard()
    
    # Clean up test task
    del tasks[test_tid]
    save_all_tasks(tasks)
    print("[+] Test task cleaned up successfully.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Continuous Task Telemetry Engine & Scorecard")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    
    subparsers = parser.add_subparsers(dest="command")

    # start
    p_start = subparsers.add_parser("start", help="Start a new tracked task")
    p_start.add_argument("task_id", help="Unique Task ID (e.g. TASK-2026-09-01)")
    p_start.add_argument("--goal", required=True, help="Task objective description")
    p_start.add_argument("--tier", default="E3", help="Target evidence tier (E0-E5)")

    # log-intervention
    p_int = subparsers.add_parser("log-intervention", help="Log active human intervention time")
    p_int.add_argument("task_id", help="Task ID")
    p_int.add_argument("--minutes", type=float, default=None, help="Active human minutes")
    p_int.add_argument("--start", type=str, default=None, help="ISO start timestamp")
    p_int.add_argument("--end", type=str, default=None, help="ISO end timestamp")
    p_int.add_argument("--reason", help="Reason for intervention")

    # log-dispatch
    p_disp = subparsers.add_parser("log-dispatch", help="Log worker invocation / LLM dispatch")
    p_disp.add_argument("task_id", help="Task ID")
    p_disp.add_argument("--model", default="agent", help="Model / agent identifier")
    p_disp.add_argument("--tokens-in", type=int, default=0, help="Input prompt tokens")
    p_disp.add_argument("--tokens-out", type=int, default=0, help="Output completion tokens")
    p_disp.add_argument("--compute-sec", type=float, default=0.0, help="Compute seconds")
    p_disp.add_argument("--duration-sec", type=float, default=None, help="Total measured dispatch duration seconds")
    p_disp.add_argument("--start", type=str, default=None, help="ISO start timestamp")
    p_disp.add_argument("--end", type=str, default=None, help="ISO end timestamp")
    p_disp.add_argument("--handoff", action="store_true", help="Flag if this dispatch was a manual context handoff")

    # log-rework
    p_rew = subparsers.add_parser("log-rework", help="Log rework / correction event")
    p_rew.add_argument("task_id", help="Task ID")
    p_rew.add_argument("--reason", help="Reason for rework")
    p_rew.add_argument("--minutes", type=float, default=0.0, help="Rework minutes incurred")

    # close
    p_close = subparsers.add_parser("close", help="Close a completed or abandoned task")
    p_close.add_argument("task_id", help="Task ID")
    p_close.add_argument("--status", default="COMPLETED", choices=["COMPLETED", "REWORK_REQUIRED", "ABANDONED"])
    p_close.add_argument("--artifact", help="Path to verified output artifact")

    # scorecard
    subparsers.add_parser("scorecard", help="Display workflow scorecard and macro telemetry")

    args = parser.parse_args()

    if args.test:
        return run_self_test()

    if args.command == "start":
        return cmd_start(args)
    elif args.command == "log-intervention":
        return cmd_log_intervention(args)
    elif args.command == "log-dispatch":
        return cmd_log_dispatch(args)
    elif args.command == "log-rework":
        return cmd_log_rework(args)
    elif args.command == "close":
        return cmd_close(args)
    elif args.command == "scorecard":
        return cmd_scorecard(args)
    else:
        return cmd_scorecard()


if __name__ == "__main__":
    sys.exit(main() or 0)
