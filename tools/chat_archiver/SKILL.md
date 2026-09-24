---
name: chat-archiver
description: >-
  Universal AI chat archiver for downloading and archiving shared conversation links
  (such as ChatGPT share URLs, etc.) as clean, structured Markdown history files directly
  into the active repository, workspace, or research archives (e.g. brainstorm/research/transcripts).
---

# Chat Archiver Skill

CRITICAL RULE: Whenever the user shares a chat link (e.g., `https://chatgpt.com/share/...`) or asks to log/save/archive a shared conversation, **DO NOT** fetch web pages manually, write custom parser scripts, or stream tokens analyzing the HTML.

You **MUST** immediately run the globally installed `save-chat` CLI tool via `run_command`.

## Execution Protocol

### 1. Save to Current Working Directory / Repo
```bash
save-chat "<URL>"
```

### 2. Save to a Specific Folder (e.g. `docs/chat_history` or custom path)
```bash
save-chat "<URL>" --dir "docs/chat_history"
```

### 3. Save to Brainstorm Knowledge Base
If the user asks to save to `brainstorm` or research transcripts:
```bash
save-chat "<URL>" --dir "f:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts"
```

### 4. Custom Filename / Output Path
```bash
save-chat "<URL>" -o "path/to/custom_name.md"
```

### 5. Append Mode (Continuation of Last / Specified Transcript)
To append a shared continuation session directly to the most recent transcript doc:
```bash
save-chat "<URL>" --append
# or short form:
save-chat "<URL>" -a
```

To append to a specific file:
```bash
save-chat "<URL>" --append "path/to/existing_transcript.md"
```

The `save-chat` command runs in under 1 second, automatically parses the conversation data, strips citation noise, cleans formatting, and writes the structured markdown file directly to disk with zero manual token overhead.

