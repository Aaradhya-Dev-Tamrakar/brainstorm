import sys
import os
import re
import json
import argparse
import urllib.request
import subprocess
import shutil
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from markdownify import markdownify as md
except ImportError:
    md = None

def clean_text(text: str) -> str:
    """Normalize text and remove citation markers / artifacts."""
    if not text:
        return ""
    # Strip ChatGPT internal web citation markers and unicode artifacts
    text = re.sub(r'cite.*?', '', text)
    text = re.sub(r'[\ue200\ue201\ue202\ufffd]|turn[0-9]+view[0-9]+', '', text)
    return text.strip()

def find_browser_executable() -> str:
    """Locate headless Chromium binary (Chrome or Edge) on Windows or Unix."""
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    for cmd in ["chrome", "google-chrome", "msedge", "edge", "chromium"]:
        found = shutil.which(cmd)
        if found:
            return found
    return None

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

def parse_gemini_share(url: str):
    """Parses Google Gemini public shared chat links (share.gemini.google or gemini.google.com/share)."""
    if not BeautifulSoup:
        raise RuntimeError("beautifulsoup4 is required to parse Gemini shared links. Please install it with 'pip install beautifulsoup4'.")
    if not md:
        raise RuntimeError("markdownify is required to parse Gemini shared links. Please install it with 'pip install markdownify'.")

    browser_exe = find_browser_executable()
    if not browser_exe:
        raise RuntimeError("No Chromium browser (Chrome or Edge) found to render Gemini dynamic share pages.")

    cmd = [
        browser_exe,
        '--headless=new',
        '--disable-gpu',
        '--virtual-time-budget=8000',
        '--dump-dom',
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if res.returncode != 0 and not res.stdout:
        raise RuntimeError(f"Headless browser failed to render Gemini share link: {res.stderr}")

    soup = BeautifulSoup(res.stdout, 'html.parser')

    # Extract conversation title
    title = "Gemini Conversation"
    h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True):
        title = h1.get_text(strip=True)
    else:
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            cleaned = og_title['content'].replace('\u200e', '').replace('Gemini - direct access to Google AI', '').strip()
            if cleaned:
                title = cleaned

    turns = []
    turn_viewers = soup.find_all('share-turn-viewer')
    for tv in turn_viewers:
        # Extract user query
        uq = tv.find('user-query')
        if uq:
            query_lines = [p.get_text(strip=True) for p in uq.find_all('p', class_='query-text-line')]
            if not query_lines:
                for hidden in uq.find_all(class_=re.compile(r'visually-hidden|screen-reader')):
                    hidden.decompose()
                u_text = uq.get_text('\n', strip=True)
                if u_text.startswith('You said'):
                    u_text = u_text[len('You said'):].strip()
            else:
                u_text = '\n\n'.join(query_lines)
            if u_text:
                turns.append({'role': 'User', 'text': clean_text(u_text)})

        # Extract assistant response
        mc = tv.find('message-content')
        if mc:
            md_div = mc.find('div', class_='markdown') or mc
            resp_md = md(str(md_div), heading_style='ATX').strip()
            resp_md = re.sub(r'\n{3,}', '\n\n', resp_md)
            if resp_md:
                turns.append({'role': 'Assistant', 'text': clean_text(resp_md)})

    if not turns:
        raise ValueError("Could not extract conversation turns from Gemini share link. The link may be invalid or expired.")

    return title, turns

def dispatch_share_parser(url: str):
    """Detects provider and delegates to the appropriate conversation extractor."""
    lower_url = url.lower()
    if 'gemini.google' in lower_url or 'share.gemini' in lower_url or 'bard.google' in lower_url:
        return parse_gemini_share(url)
    elif 'chatgpt.com' in lower_url or 'openai.com' in lower_url:
        return parse_chatgpt_share(url)
    else:
        # Default fallback: try ChatGPT format first, then Gemini format
        try:
            return parse_chatgpt_share(url)
        except Exception:
            return parse_gemini_share(url)

def slugify(value: str) -> str:
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def format_markdown(title: str, url: str, turns: list) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    md_lines = [f"# {title}\n"]
    md_lines.append(f"- **Source URL:** [{url}]({url})")
    md_lines.append(f"- **Archived Date:** {date_str}")
    md_lines.append(f"- **Total Turns:** {len(turns)}\n")
    md_lines.append("---\n")

    turn_num = 1
    i = 0
    while i < len(turns):
        t = turns[i]
        if t['role'] == 'User':
            md_lines.append(f"## Turn {turn_num}\n")
            md_lines.append("### User\n")
            md_lines.append(t['text'] + "\n")
            if i + 1 < len(turns) and turns[i+1]['role'] == 'Assistant':
                md_lines.append("### Assistant\n")
                md_lines.append(turns[i+1]['text'] + "\n")
                i += 1
            md_lines.append("---\n")
            turn_num += 1
        else:
            md_lines.append(f"### {t['role']}\n")
            md_lines.append(t['text'] + "\n")
            md_lines.append("---\n")
        i += 1

    return "\n".join(md_lines)

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
    md_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return md_files[0]

def format_appendix(title: str, url: str, turns: list) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    appendix = [
        "\n\n---\n",
        f"# 📎 Appendix: {title} (Session Continuation)\n",
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
    if os.path.exists(os.path.join(cwd, "research", "transcripts")):
        return os.path.join(cwd, "research", "transcripts")
    
    if os.path.exists(os.path.join(cwd, "docs")):
        return os.path.join(cwd, "docs", "chat_history")

    return os.path.join(cwd, "chat_history")

def main():
    parser = argparse.ArgumentParser(description="Universal Chat Archiver for AI share links (ChatGPT, Google Gemini, etc.)")
    parser.add_argument("url", help="Share URL (e.g. https://chatgpt.com/share/... or https://share.gemini.google/...)")
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
        title, turns = dispatch_share_parser(args.url)
        print(f"Parsed '{title}' ({len(turns)} message turns)")
        
        target_dir = resolve_target_directory(args.dir)

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
