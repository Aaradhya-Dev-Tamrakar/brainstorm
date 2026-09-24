import sys
import os
import re
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString, Tag

def extract_gdoc_id(url: str) -> str:
    """Extract Google Doc / Drive file ID from various URL patterns."""
    patterns = [
        r'/document/d/([a-zA-Z0-9_-]+)',
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',
        r'/spreadsheets/d/([a-zA-Z0-9_-]+)',
        r'/presentation/d/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None

def fetch_gdoc_html(doc_id: str) -> str:
    """Fetch exported HTML for a Google Doc."""
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(export_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8')

def fetch_generic_html(url: str) -> str:
    """Fetch HTML content from generic URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8')

def parse_html_to_markdown(html_content: str) -> tuple[str, str]:
    """Parse HTML into clean GitHub Flavored Markdown and extract document title."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to determine title
    title = ""
    first_h1 = soup.find('h1')
    if first_h1 and first_h1.get_text(strip=True):
        title = first_h1.get_text(strip=True)
    elif soup.title and soup.title.string and soup.title.string.strip():
        title = soup.title.string.strip()
    else:
        first_p = soup.find('p')
        if first_p and first_p.get_text(strip=True):
            title = first_p.get_text(strip=True)[:60]
        else:
            title = "Exported Document"

    body = soup.body or soup

    def process_node(node):
        if isinstance(node, NavigableString):
            return str(node)
        
        tag = node.name
        inner = ''.join(process_node(c) for c in node.children)
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            return f"\n\n{'#' * level} {inner.strip()}\n\n"
        elif tag == 'p':
            text = inner.strip()
            if not text:
                return ''
            return f"\n\n{text}\n\n"
        elif tag in ['b', 'strong']:
            return f"**{inner.strip()}**" if inner.strip() else ''
        elif tag in ['i', 'em']:
            return f"*{inner.strip()}*" if inner.strip() else ''
        elif tag == 'code':
            return f"`{inner.strip()}`"
        elif tag == 'a':
            href = node.get('href', '')
            m = re.search(r'q=(https?[^&]+)', href)
            if m:
                href = urllib.parse.unquote(m.group(1))
            return f"[{inner.strip()}]({href})" if inner.strip() else ''
        elif tag == 'ul':
            return f"\n\n{inner}\n\n"
        elif tag == 'ol':
            return f"\n\n{inner}\n\n"
        elif tag == 'li':
            return f"- {inner.strip()}\n"
        elif tag == 'table':
            rows = node.find_all('tr')
            if not rows:
                return ''
            out = ['\n']
            header_done = False
            for r in rows:
                cells = r.find_all(['td', 'th'])
                cell_texts = [re.sub(r'\s+', ' ', ''.join(process_node(c) for c in cell.children)).strip() for cell in cells]
                out.append('| ' + ' | '.join(cell_texts) + ' |')
                if not header_done:
                    out.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
                    header_done = True
            out.append('\n')
            return '\n'.join(out)
        elif tag in ['tr', 'td', 'th']:
            return inner
        else:
            return inner

    md_content = process_node(body)
    md_content = re.sub(r'\n{3,}', '\n\n', md_content).strip()
    return title, md_content

def slugify(value: str) -> str:
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def format_document(title: str, url: str, md_body: str) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    header = [
        f"# {title}\n",
        f"- **Source URL:** [{url}]({url})",
        f"- **Archived Date:** {date_str}",
        f"- **Format:** Document Archive\n",
        "---\n\n"
    ]
    
    # Avoid duplicating top title if md_body already begins with the same h1
    if md_body.startswith('# '):
        lines = md_body.split('\n', 2)
        first_line = lines[0].replace('#', '').strip()
        if first_line.lower() == title.lower() or len(first_line) > 20:
            rest = lines[2] if len(lines) > 2 else ''
            return "".join(header) + rest.strip() + "\n"

    return "".join(header) + md_body + "\n"

def resolve_target_directory(specified_dir: str) -> str:
    """Determine target directory based on environment."""
    if specified_dir and specified_dir != ".":
        return specified_dir

    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "research", "transcripts")):
        return os.path.join(cwd, "research", "transcripts")
    if os.path.exists(os.path.join(cwd, "docs", "transcripts")):
        return os.path.join(cwd, "docs", "transcripts")
    if os.path.exists(os.path.join(cwd, "docs")):
        return os.path.join(cwd, "docs")
    return cwd

def find_last_doc(target_dir: str) -> str:
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

def main():
    parser = argparse.ArgumentParser(description="Universal Document Archiver for Google Docs and Web Documents")
    parser.add_argument("url", help="Google Doc URL or document link")
    parser.add_argument("-o", "--output", help="Output filepath. If omitted, generates from title in dedicated directory.")
    parser.add_argument("--dir", help="Target directory for output file", default="")
    parser.add_argument(
        "-a", "--append",
        nargs="?",
        const="__LATEST__",
        default=None,
        help="Append document content to an existing file. If no path is given, appends to the last/most recent file."
    )

    args = parser.parse_args()
    print(f"Fetching and parsing document: {args.url}")

    try:
        doc_id = extract_gdoc_id(args.url)
        if doc_id:
            html = fetch_gdoc_html(doc_id)
        else:
            html = fetch_generic_html(args.url)

        title, md_body = parse_html_to_markdown(html)
        print(f"Parsed document: '{title}' ({len(md_body)} chars)")

        target_dir = resolve_target_directory(args.dir)

        if args.append is not None:
            if args.append == "__LATEST__":
                target_file = find_last_doc(target_dir)
                if not target_file:
                    raise FileNotFoundError(f"No existing markdown document found in {target_dir} to append to.")
            else:
                target_file = args.append

            date_str = datetime.now().strftime("%Y-%m-%d")
            appendix = f"\n\n---\n\n# 📎 Document Appendix: {title}\n\n- **Source URL:** [{args.url}]({args.url})\n- **Appended:** {date_str}\n\n---\n\n{md_body}\n"
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write(appendix)

            print(f"Successfully appended document as Appendix to: {os.path.abspath(target_file)}")
            return

        final_content = format_document(title, args.url, md_body)

        if args.output:
            out_path = args.output
        else:
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)[:60]
            filename = f"{date_prefix}_{slug.upper()}.md" if slug else f"{date_prefix}_ARCHIVED_DOC.md"
            out_path = os.path.join(target_dir, filename)

        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"Successfully archived document to: {os.path.abspath(out_path)}")

    except Exception as e:
        print(f"Error archiving document: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
