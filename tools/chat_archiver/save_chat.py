import sys
import os
import re
import json
import argparse
import urllib.request
from datetime import datetime

def clean_text(text: str) -> str:
    """Normalize text and remove citation markers / artifacts."""
    if not text:
        return ""
    # Strip ChatGPT internal web citation markers and unicode artifacts
    text = re.sub(r'cite.*?', '', text)
    text = re.sub(r'[\ue200\ue201\ue202\ufffd]|turn[0-9]+view[0-9]+', '', text)
    return text.strip()

def parse_chatgpt_share(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        page_html = resp.read().decode('utf-8')

    scripts = re.findall(r'<script[^>]*>(.*?)</script>', page_html, re.DOTALL)
    stream_data = []

    for s in scripts:
        if 'streamController.enqueue' in s:
            idx = 0
            while True:
                pos = s.find('.enqueue(', idx)
                if pos == -1:
                    break
                start_arg = pos + len('.enqueue(')
                if s[start_arg:start_arg+1] == '"':
                    try:
                        decoder = json.JSONDecoder()
                        raw_str, _ = decoder.raw_decode(s[start_arg:])
                        parsed = json.loads(raw_str)
                        if isinstance(parsed, list) and len(parsed) > len(stream_data):
                            stream_data = parsed
                    except Exception:
                        pass
                idx = pos + 1

    if not stream_data:
        raise ValueError("Could not extract conversation stream data from the URL.")

    def decode_node(idx, visited=None):
        if visited is None:
            visited = set()
        if isinstance(idx, int):
            if idx < 0:
                return None
            if idx in visited:
                return None
            visited = visited | {idx}
            val = stream_data[idx]
        else:
            val = idx

        if isinstance(val, (int, float, str, bool)) or val is None:
            return val
        if isinstance(val, list):
            return [decode_node(item, visited) for item in val]
        if isinstance(val, dict):
            res = {}
            for k, v in val.items():
                key_name = stream_data[int(k[1:])] if k.startswith('_') and k[1:].isdigit() else k
                res[key_name] = decode_node(v, visited)
            return res
        return val

    conv_data = None
    for i, item in enumerate(stream_data):
        if isinstance(item, dict):
            keys = [stream_data[int(k[1:])] for k in item.keys() if k.startswith('_') and k[1:].isdigit()]
            if 'linear_conversation' in keys:
                conv_data = decode_node(i)
                break

    if not conv_data:
        raise ValueError("Could not locate conversation structure in payload.")

    title = conv_data.get('title') or "ChatGPT Conversation"
    linear = conv_data.get('linear_conversation', [])

    turns = []
    for node in linear:
        if not isinstance(node, dict):
            continue
        msg = node.get('message') or {}
        role = msg.get('author', {}).get('role')
        content = msg.get('content', {})
        content_type = content.get('content_type')
        parts = content.get('parts', [])

        if role in ('user', 'assistant') and content_type == 'text' and parts:
            text_parts = [clean_text(str(p)) for p in parts if str(p).strip()]
            full_text = "\n\n".join(text_parts)
            if full_text:
                turns.append({
                    'role': 'User' if role == 'user' else 'Assistant',
                    'text': full_text
                })

    return title, turns

def slugify(value: str) -> str:
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def format_markdown(title: str, url: str, turns: list) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = [f"# {title}\n"]
    md.append(f"- **Source URL:** [{url}]({url})")
    md.append(f"- **Archived Date:** {date_str}")
    md.append(f"- **Total Turns:** {len(turns)}\n")
    md.append("---\n")

    turn_num = 1
    i = 0
    while i < len(turns):
        t = turns[i]
        if t['role'] == 'User':
            md.append(f"## Turn {turn_num}\n")
            md.append("### User\n")
            md.append(t['text'] + "\n")
            if i + 1 < len(turns) and turns[i+1]['role'] == 'Assistant':
                md.append("### Assistant\n")
                md.append(turns[i+1]['text'] + "\n")
                i += 1
            md.append("---\n")
            turn_num += 1
        else:
            md.append(f"### {t['role']}\n")
            md.append(t['text'] + "\n")
            md.append("---\n")
        i += 1

    return "\n".join(md)

def find_last_transcript_doc(target_dir: str) -> str:
    """Finds the most recently modified or committed markdown transcript in target_dir."""
    if not os.path.exists(target_dir):
        return None
    md_files = [
        os.path.join(target_dir, f)
        for f in os.listdir(target_dir)
        if f.endswith(".md") and f != "README.md"
    ]
    if not md_files:
        return None
    # Sort by modification time descending
    md_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return md_files[0]

def format_appendix(title: str, url: str, turns: list) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    appendix = [
        "\n\n---\n",
        f"# 📎 Appendix: {title} (ChatGPT Session Continuation)\n",
        f"> **Source URL:** [{url}]({url})",
        f"> **Appended:** {date_str}",
        f"> **Total Turns:** {len(turns)}\n",
        "---\n"
    ]
    turn_num = 1
    i = 0
    while i < len(turns):
        t = turns[i]
        if t['role'] == 'User':
            appendix.append(f"## Turn {turn_num}\n")
            appendix.append("### User\n")
            appendix.append(t['text'] + "\n")
            if i + 1 < len(turns) and turns[i+1]['role'] == 'Assistant':
                appendix.append("### Assistant\n")
                appendix.append(turns[i+1]['text'] + "\n")
                i += 1
            appendix.append("---\n")
            turn_num += 1
        else:
            appendix.append(f"### {t['role']}\n")
            appendix.append(t['text'] + "\n")
            appendix.append("---\n")
        i += 1

    return "\n".join(appendix)

def resolve_target_directory(specified_dir: str) -> str:
    """
    Determines the dedicated subfolder for chat histories.
    - If user explicitly specified a custom subfolder/path, use it.
    - If in brainstorm repo, auto-route to research/transcripts if not specified.
    - Otherwise in any repo/CWD, auto-route to 'chat_history' subfolder.
    """
    if specified_dir and specified_dir != ".":
        return specified_dir

    cwd = os.getcwd()
    # Check if inside brainstorm repo
    if os.path.exists(os.path.join(cwd, "research", "transcripts")):
        return os.path.join(cwd, "research", "transcripts")
    
    # Check if inside docs folder exists
    if os.path.exists(os.path.join(cwd, "docs")):
        return os.path.join(cwd, "docs", "chat_history")

    # Default dedicated subfolder in any repo
    return os.path.join(cwd, "chat_history")

def main():
    parser = argparse.ArgumentParser(description="Universal Chat Archiver for AI share links (ChatGPT, etc.)")
    parser.add_argument("url", help="Share URL (e.g. https://chatgpt.com/share/...)")
    parser.add_argument("-o", "--output", help="Output filepath. If omitted, generates from title in dedicated subfolder.")
    parser.add_argument("--dir", help="Target directory for output file", default="")
    parser.add_argument(
        "-a", "--append",
        nargs="?",
        const="__LATEST__",
        default=None,
        help="Append conversation to an existing document. If no path is given, appends to the last/most recent transcript."
    )

    args = parser.parse_args()

    print(f"Fetching and parsing: {args.url}")
    try:
        title, turns = parse_chatgpt_share(args.url)
        print(f"Parsed '{title}' ({len(turns)} message turns)")
        
        target_dir = resolve_target_directory(args.dir)

        # Handle append mode
        if args.append is not None:
            if args.append == "__LATEST__":
                target_file = find_last_transcript_doc(target_dir)
                if not target_file:
                    raise FileNotFoundError(f"No existing transcript found in {target_dir} to append to.")
            else:
                target_file = args.append

            appendix_content = format_appendix(title, args.url, turns)
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write(appendix_content)

            print(f"Successfully appended chat as Appendix to: {os.path.abspath(target_file)}")
            return

        md_content = format_markdown(title, args.url, turns)
        
        if args.output:
            out_path = args.output
        else:
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            filename = f"{date_prefix}_{slug.upper()}_CONVERSATION.md" if slug else f"{date_prefix}_CHAT_CONVERSATION.md"
            out_path = os.path.join(target_dir, filename)

        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Successfully archived chat to: {os.path.abspath(out_path)}")

    except Exception as e:
        print(f"Error archiving chat: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
