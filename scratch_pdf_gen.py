import os
import subprocess
import markdown

docs_dir = os.path.expanduser(r'~\Downloads\Research-Profile-Docs')
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

css = """
@page {
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 13px;
    line-height: 1.5;
    color: #24292e;
    max-width: 100%;
    margin: 0 auto;
}
h1 {
    font-size: 19px;
    border-bottom: 1.5px solid #eaecef;
    padding-bottom: 5px;
    margin-top: 0;
    margin-bottom: 10px;
    color: #111827;
}
h2 {
    font-size: 15px;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 4px;
    margin-top: 14px;
    margin-bottom: 8px;
    color: #1f2937;
}
h3 {
    font-size: 14px;
    margin-top: 12px;
    margin-bottom: 6px;
    color: #111827;
}
h4 {
    font-size: 13px;
    margin-top: 8px;
    margin-bottom: 4px;
    color: #374151;
}
p, ul, ol {
    margin-top: 0;
    margin-bottom: 6px;
}
li {
    margin-bottom: 3px;
}
hr {
    height: 1px;
    background-color: #e1e4e8;
    border: none;
    margin: 10px 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 10px;
    font-size: 12px;
}
table th, table td {
    border: 1px solid #dfe2e5;
    padding: 5px 8px;
}
table th {
    background-color: #f6f8fa;
    font-weight: 600;
}
table tr:nth-child(2n) {
    background-color: #fcfcfc;
}
code {
    background-color: rgba(27,31,35,0.05);
    padding: 0.15em 0.3em;
    border-radius: 3px;
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 88%;
}
pre {
    background-color: #f6f8fa;
    padding: 8px;
    border-radius: 4px;
    overflow: auto;
    font-size: 11.5px;
    line-height: 1.4;
    border: 1px solid #e1e4e8;
    margin-bottom: 8px;
}
pre code {
    background-color: transparent;
    padding: 0;
}
a {
    color: #0366d6;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""

md_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
for mf in md_files:
    in_path = os.path.join(docs_dir, mf)
    base_name = os.path.splitext(mf)[0]
    out_html = os.path.join(docs_dir, base_name + '.html')
    out_pdf = os.path.join(docs_dir, base_name + '.pdf')
    
    with open(in_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    html_body = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    full_html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{html_body}</body></html>'
    
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    cmd = [
        edge_path,
        '--headless',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={out_pdf}',
        out_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(out_html):
        os.remove(out_html)
    print(f'Generated: {out_pdf}')
