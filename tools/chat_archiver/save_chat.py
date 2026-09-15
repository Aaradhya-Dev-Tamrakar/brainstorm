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
            # Next turn if assistant
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

def main():
    parser = argparse.ArgumentParser(description="Universal Chat Archiver for AI share links (ChatGPT, etc.)")
    parser.add_argument("url", help="Share URL (e.g. https://chatgpt.com/share/...)")
    parser.add_argument("-o", "--output", help="Output filepath. If omitted, generates from title in CWD.")
    parser.add_argument("--dir", help="Target directory for output file", default=".")
    parser.add_argument("--repo-name", help="Optional repo name to append or prefix", default="")

    args = parser.parse_args()

    print(f"Fetching and parsing: {args.url}")
    try:
        title, turns = parse_chatgpt_share(args.url)
        print(f"Parsed '{title}' ({len(turns)} message turns)")
        
        md_content = format_markdown(title, args.url, turns)
        
        if args.output:
            out_path = args.output
        else:
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            filename = f"{date_prefix}_{slug.upper()}_CONVERSATION.md" if slug else f"{date_prefix}_CHAT_CONVERSATION.md"
            out_path = os.path.join(args.dir, filename)

        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Successfully archived chat to: {os.path.abspath(out_path)}")

    except Exception as e:
        print(f"Error archiving chat: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
