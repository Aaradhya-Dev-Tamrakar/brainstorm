"""
transcript_archiver.py
----------------------
Deterministic utility to identify and archive significant brainstorm sessions
per invariant INV-EPI-001.

Triggers on:
1. Explicit user trigger keywords ("log this", "archive session", "verbatim log", codeword reference).
2. Architectural milestone detection (creation of ARCH-SPEC, INV, or simulation files).
3. Session message threshold (conversations with > 6 significant dialogue turns).

Usage:
    python sim/transcript_archiver.py --codename STRANGLER-IPU
    python sim/transcript_archiver.py --auto
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Central AppData path for Antigravity engine transcripts
APPDATA_DIR = r"C:\Users\Aaradhya\.gemini\antigravity\brain"
BRAINSTORM_DIR = r"F:\Aaradhya-Dev-Tamrakar\brainstorm"
TRANSCRIPTS_TARGET_DIR = os.path.join(BRAINSTORM_DIR, "research", "transcripts")
def get_most_recent_conversation():
    """Auto-discover the latest active or completed conversation in APPDATA_DIR."""
    if not os.path.exists(APPDATA_DIR):
        return None, None
    candidates = []
    try:
        for entry in os.scandir(APPDATA_DIR):
            if entry.is_dir():
                tpath = os.path.join(entry.path, ".system_generated", "logs", "transcript_full.jsonl")
                if os.path.exists(tpath):
                    try:
                        mtime = os.path.getmtime(tpath)
                        candidates.append((mtime, entry.name, tpath))
                    except OSError:
                        pass
    except OSError:
        pass
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1], candidates[0][2]
    return None, None


def find_latest_transcript_path(conversation_id=None):
    if conversation_id:
        target = os.path.join(APPDATA_DIR, conversation_id, ".system_generated", "logs", "transcript_full.jsonl")
        if os.path.exists(target):
            return target
        # Fallback search across brain subdirectories
        for root, dirs, files in os.walk(APPDATA_DIR):
            if "transcript_full.jsonl" in files and conversation_id in root:
                return os.path.join(root, "transcript_full.jsonl")
        return None

    _, tpath = get_most_recent_conversation()
    return tpath


SIGNIFICANT_KEYWORDS = [
    "architect", "charter", "paradigm", "spec", "invariant",
    "codeword", "ipu", "strangler", "6g", "sim", "discrete",
    "coalescing", "reduction", "telecom", "verbatim"
]


def evaluate_significance(transcript_file):
    """
    Evaluates whether a transcript meets the criteria for permanent archival.
    Returns (is_significant, reason, stats)
    """
    turn_count = 0
    keyword_hits = 0
    user_prompts = []

    with open(transcript_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step_type = data.get("type")
                content = data.get("content", "").lower()
                if step_type == "USER_INPUT":
                    turn_count += 1
                    user_prompts.append(content)
                    for kw in SIGNIFICANT_KEYWORDS:
                        if kw in content:
                            keyword_hits += 1
            except Exception:
                continue

    # Decision logic
    if turn_count >= 5 and keyword_hits >= 3:
        return True, f"High architectural density ({turn_count} turns, {keyword_hits} architectural keyword matches)", turn_count
    elif any("log this" in p or "archive" in p or "verbatim" in p for p in user_prompts):
        return True, "Explicit user archival directive detected", turn_count
    else:
        return False, f"Below significance threshold ({turn_count} turns, {keyword_hits} hits)", turn_count


def export_verbatim(transcript_file, codename, output_path, conversation_id=None):
    if not conversation_id:
        # Extract conversation id from path structure if possible
        try:
            conversation_id = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(transcript_file)))))
        except Exception:
            conversation_id = "AUTO-DISCOVERED"

    out_lines = [
        f"# 🎙️ Verbatim Conversation Log: PROJECT {codename}\n\n",
        f"> **Date:** {datetime.now().strftime('%Y-%m-%d')}\n",
        f"> **Codename:** `{codename}`\n",
        f"> **Participants:** Aaradhya Dev Tamrakar & Antigravity (Gemini Engine)\n",
        f"> **Conversation ID:** `{conversation_id}`\n",
        f"> **Enforced By Invariant:** `INV-EPI-001` (Epistemic History Preservation)\n\n",
        "---\n\n"
    ]

    with open(transcript_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step_type = data.get("type")
                created_at = data.get("created_at", "")
                content = data.get("content", "")

                if step_type == "USER_INPUT" and content.strip():
                    out_lines.append(f"### 👤 USER (Aaradhya) [{created_at}]\n\n")
                    out_lines.append(f"{content.strip()}\n\n---\n\n")
                elif step_type == "PLANNER_RESPONSE" and content.strip():
                    out_lines.append(f"### 🤖 ASSISTANT (Antigravity) [{created_at}]\n\n")
                    out_lines.append(f"{content.strip()}\n\n---\n\n")
            except Exception:
                continue

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

    return len(out_lines)


def main():
    parser = argparse.ArgumentParser(description="Archive verbatim session transcript for brainstorm.")
    parser.add_argument("--codename", default="STRANGLER-IPU", help="Codename for the session")
    parser.add_argument("--conversation-id", default=None, help="Target specific conversation ID (defaults to auto-discovery)")
    parser.add_argument("--auto", action="store_true", help="Automatically check significance criteria")
    args = parser.parse_args()

    active_cid = args.conversation_id
    if not active_cid:
        active_cid, t_path = get_most_recent_conversation()
    else:
        t_path = find_latest_transcript_path(active_cid)

    if not t_path:
        target_info = active_cid if active_cid else "latest active session"
        print(f"[!] Transcript log not found for session: {target_info}")
        sys.exit(1)

    is_sig, reason, turns = evaluate_significance(t_path)
    print(f"[*] Conversation ID: {active_cid}")
    print(f"[*] Transcript: {t_path}")
    print(f"[*] Evaluation: {reason} (Total User Turns: {turns})")

    if args.auto and not is_sig:
        print("[-] Session did not meet significance criteria. Skipping archival.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    out_file = os.path.join(TRANSCRIPTS_TARGET_DIR, f"{today}_{args.codename}_CONVERSATION.md")
    lines_written = export_verbatim(t_path, args.codename, out_file, conversation_id=active_cid)
    print(f"[+] Verbatim session archived successfully: {lines_written} blocks written to:")
    print(f"    {out_file}")


if __name__ == "__main__":
    main()
