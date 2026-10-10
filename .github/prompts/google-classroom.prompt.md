---
description: ">-"
---

# Google Classroom Agent Skill

This skill governs how AI assistants (Antigravity, Claude, and orchestration agents) interact with Google Classroom using the `classroom` MCP tools (`google-classroom-mcp`).

---

## 🎯 When to Activate This Skill

Activate this skill whenever the user:
- Asks about their classes, courses, or professors (e.g. *"What classes am I enrolled in?"*, *"Show my course roster"*).
- Inquires about homework, upcoming deadlines, assignments, or quizzes (e.g. *"What assignments are due this week?"*, *"Do I have any pending quizzes?"*).
- Asks for details, instructions, or materials for a specific assignment (e.g. *"What do I need to do for Assignment 3?"*, *"Show the rubric for the MLOps project"*).
- Asks to check their grades, feedback, or submission status (e.g. *"Did I turn in the NLP quiz?"*, *"What was my score on the CV assignment?"*).
- Asks for class stream announcements, teacher updates, or lecture materials.
- Wants to turn in or reclaim a submission.

---

## 🧰 Available MCP Tools Mapping

All tools are provided by the `classroom` MCP server:

| User Intent | Primary MCP Tool | Key Parameters |
| :--- | :--- | :--- |
| Discover active classes | `call_mcp_tool(ServerName="classroom", ToolName="list_courses", ...)` | `courseStates: ["ACTIVE"]` |
| View specific course details | `call_mcp_tool(ServerName="classroom", ToolName="get_course", ...)` | `courseId` |
| Check assignments / homework | `call_mcp_tool(ServerName="classroom", ToolName="list_coursework", ...)` | `courseId`, `courseWorkStates: ["PUBLISHED"]`, `orderBy: "dueDate asc"` |
| Inspect assignment instructions | `call_mcp_tool(ServerName="classroom", ToolName="get_coursework", ...)` | `courseId`, `courseWorkId` |
| Check turn-in status & grades | `call_mcp_tool(ServerName="classroom", ToolName="list_submissions", ...)` | `courseId`, `courseWorkId: "-"`, `userId: "me"` |
| Inspect submission attachments | `call_mcp_tool(ServerName="classroom", ToolName="get_submission", ...)` | `courseId`, `courseWorkId`, `submissionId` |
| Read stream announcements | `call_mcp_tool(ServerName="classroom", ToolName="list_announcements", ...)` | `courseId`, `orderBy: "updateTime desc"` |
| Fetch lecture slides & syllabi | `call_mcp_tool(ServerName="classroom", ToolName="list_coursework_materials", ...)` | `courseId` |
| List instructors or classmates | `call_mcp_tool(ServerName="classroom", ToolName="list_teachers" / "list_students", ...)` | `courseId` |
| Submit completed homework | `call_mcp_tool(ServerName="classroom", ToolName="turn_in_assignment", ...)` | `courseId`, `courseWorkId`, `submissionId` |
| Unsubmit homework to edit | `call_mcp_tool(ServerName="classroom", ToolName="reclaim_assignment", ...)` | `courseId`, `courseWorkId`, `submissionId` |

---

## 📋 Core Orchestration Workflows

### 1. The "What's Due / Pending Homework" Audit (Most Common)
When asked for pending work or deadlines:
1. Call `list_courses` to find enrolled active classes (or use the cached `courseId` if known).
2. For the target course(s), call `list_coursework` with `courseWorkStates: ["PUBLISHED"]`.
3. Call `list_submissions` with `userId: "me"` and `courseWorkId: "-"` to get student submission statuses across all items.
4. Cross-reference: Filter for assignments where `state` is `NEW`, `CREATED`, or `RECLAIMED_BY_STUDENT` (not yet `TURNED_IN` or `RETURNED`).
5. Present a clear, chronologically sorted markdown table:
   - **Assignment Name** (with link)
   - **Due Date & Time**
   - **Max Points**
   - **Status / Urgency** (e.g. 🔴 Due in 24h, 🟡 Due this week, 🟢 Due later)

### 2. Assignment Deep-Dive & Requirements Extraction
When asked about a specific assignment:
1. Retrieve the full object via `get_coursework`.
2. Extract:
   - Full description / instructions.
   - Any attached Google Drive templates, rubrics, YouTube links, or code repositories.
   - Due date and maximum grade points.
3. If the user needs to inspect an attached Google Doc / Drive file, leverage the `gdrive` MCP (`read_file_content`) using the `driveFile.id` extracted from the coursework materials.

### 3. Submission Grade & Feedback Review
When asked about grades or performance:
1. Retrieve the student submissions via `list_submissions(courseId, courseWorkId, userId="me")`.
2. Display:
   - Assigned Grade / Max Points (e.g. `95 / 100`).
   - Late flag (`late: true/false`).
   - Feedback comments or attached graded work.

### 4. Turn-In & Reclaim Safety Protocol
- **Action Confirmation**: Before calling `turn_in_assignment`, always confirm the target assignment title and submission ID with the user.
- **Attachment Verification**: Ensure student work attachments are uploaded to Google Drive / Classroom before invoking `turn_in_assignment`.
- **Reclaim**: Use `reclaim_assignment` only when the user explicitly requests to retract or edit their turned-in work.

---

## 💡 Best Practices & Performance Rules

- **Zero Redundant Listing**: If the course ID (e.g. `849624491859` for *"AI Fellowship 2026"*) has already been established in conversation, jump straight to `list_coursework` or `list_submissions` without repeating `list_courses`.
- **Chronological Sorting**: Always format due dates cleanly in ISO format (`YYYY-MM-DD HH:mm`) and sort upcoming tasks by deadline earliest-first.
- **Drive Cross-Linking & Scope Partitioning (`INV-AUTH-001`)**:
  - Google Classroom assignments store problem sets, rubrics, and templates in Google Drive (`materials[].driveFile`).
  - **CRITICAL SCOPE BOUNDARY**: Classroom OAuth credentials (`.classroom-server-credentials.json`) only grant Classroom API scopes. Requesting binary downloads via `https://www.googleapis.com/drive/v3/files/{id}?alt=media` using the Classroom token will fail with HTTP 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT`.
  - When downloading binary coursework attachments (e.g. PDFs, zip archives), **always cross-wire to the `gdrive` MCP credentials** (`C:\Users\Aaradhya\.gdrive-server-credentials.json`) which carry full Drive API scopes.

---

## 🔧 Infrastructure & Troubleshooting Guide

### Canonical Path Reference
- **Active Repository**: `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\google-classroom-mcp`
- **Backwards Compatibility Junction**: `F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp`
- **Configuration Path**: `C:\Users\Aaradhya\.gemini\config\mcp_config.json`

### Handling MCP Daemon Caching & Connection Closed EOF
If the MCP server was moved or offline during host IDE startup, Antigravity's client manager may transition the server into a cached `connection closed: EOF` error state in daemon memory. If `call_mcp_tool` fails with this error:
1. Verify the NTFS directory junction exists:
   ```powershell
   New-Item -ItemType Junction -Path "F:\Aaradhya-Dev-Tamrakar\google-classroom-mcp" -Target "F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\google-classroom-mcp"
   ```
2. Execute requests via a direct zero-overhead Node runner importing stored tokens from `C:\Users\Aaradhya\.classroom-server-credentials.json` directly to Google Classroom API endpoints (`https://classroom.googleapis.com/v1/...`).

### Windows Console UTF-8 Encoding
When running diagnostics, text extraction, or reading Classroom metadata in Windows PowerShell, always enforce UTF-8 to prevent `UnicodeEncodeError` on bullet points (`\u25cf`) or symbols:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```
