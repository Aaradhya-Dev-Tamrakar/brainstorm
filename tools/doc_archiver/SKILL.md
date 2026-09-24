---
name: doc-archiver
description: >-
  Universal Document Archiver for downloading and archiving Google Docs, Google Drive documents,
  and web pages as clean, structured Markdown files directly into the active repository,
  workspace, or research archives (e.g. brainstorm/research/transcripts).
---

# Document Archiver Skill

CRITICAL RULE: Whenever the user shares a Google Doc link (e.g., `https://docs.google.com/document/d/...`) or asks to archive/save a document/web doc to the repository, **DO NOT** fetch web pages manually, write custom parser scripts, or stream tokens analyzing the HTML.

You **MUST** immediately run the globally installed `save-doc` CLI tool via `run_command`.

## Execution Protocol

### 1. Save to Current Working Directory / Repo
```bash
save-doc "<URL>"
```

### 2. Save to a Specific Folder (e.g. `docs` or `research/transcripts`)
```bash
save-doc "<URL>" --dir "research/transcripts"
```

### 3. Save to Brainstorm Knowledge Base
If the user asks to save a document to `brainstorm` or research transcripts:
```bash
save-doc "<URL>" --dir "f:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts"
```

### 4. Custom Filename / Output Path
```bash
save-doc "<URL>" -o "path/to/custom_name.md"
```

### 5. Append Mode (Continuation of Last / Specified Document)
To append a shared document directly to the most recent markdown doc in the directory:
```bash
save-doc "<URL>" --append
# or short form:
save-doc "<URL>" -a
```

To append to a specific file:
```bash
save-doc "<URL>" --append "path/to/existing_document.md"
```

The `save-doc` command parses Google Docs and web documents into clean, structured Markdown with tables, headings, links, and formatting preserved without manual token overhead.
