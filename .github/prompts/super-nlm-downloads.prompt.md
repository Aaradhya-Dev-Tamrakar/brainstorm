---
description: "This skill should be used when the user pastes a Google NotebookLM link or notebook ID to download all studio artifacts (videos, quizzes, mind maps, slides, reports), requires files saved directly to the subject's downloads folder outside the repository, or asks to share downloaded folders/files via LocalSend (sharing the whole folder, or bundling files into a date-appended subfolder)."
---

# Super-NLM Studio Artifact Downloads & LocalSend Sharing Skill

This skill governs the automated downloading of Google NotebookLM Studio artifacts into dedicated external subject folders and seamless P2P sharing via LocalSend.

---

## ⚡ Core Operational Principles

1. **Zero Repository Pollution**:
   - Studio artifact media (videos `.mp4`, slide decks `.pdf`/`.pptx`, quizzes `.md`, mind maps `.json`) must **NEVER be saved or committed inside the active git repository** (e.g. `super-nlm` or workspace root).
   - All files must be saved directly to the subject's downloads folder under:
     `C:\Users\Aaradhya\Downloads\<SubjectFolder>` (e.g. `C:\Users\Aaradhya\Downloads\EX725 Exam`).

2. **Automated URL & Subject Resolution**:
   - Extract the notebook UUID from any Google NotebookLM link:
     `https://notebook.google.com/notebook/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})`
   - Retrieve the notebook title and identify the course or subject code (e.g. `EX725`, `ME708`, `CT653`, `CT704`, `EX751`, `EX752`).
   - Map to the canonical subject directory:
     | Course Code | Canonical Subject Directory |
     | :--- | :--- |
     | **EX725** | `C:\Users\Aaradhya\Downloads\EX725 Exam` |
     | **ME708** | `C:\Users\Aaradhya\Downloads\ME708 Exam` |
     | **CT653** | `C:\Users\Aaradhya\Downloads\CT653 Exam` |
     | **CT704** | `C:\Users\Aaradhya\Downloads\CT704 Exam` |
     | **EX751** | `C:\Users\Aaradhya\Downloads\EX751 Exam` |
     | **EX752** | `C:\Users\Aaradhya\Downloads\EX752 Exam` |
     | *Other* | `C:\Users\Aaradhya\Downloads\<SanitizedTitle>` |

3. **Deterministic LocalSend Sharing Modes**:
   - **Mode A: Share Whole Folder**:
     - When instructed to "share folder", "share everything", or "send to [Device]", send the entire subject directory (`C:\Users\Aaradhya\Downloads\<SubjectFolder>`).
     - LocalSend automatically preserves the relative directory hierarchy (e.g. `EX725 Exam/Chapter 1_ ...`).
   - **Mode B: Share Files Only**:
     - When asked to "share files only", "share the files", or send a filtered subset of artifacts:
       1. Compute today's date formatted as `YYYY-MM-DD` (e.g. `2026-10-02`).
       2. Create a dedicated date-appended subfolder inside the subject directory:
          `C:\Users\Aaradhya\Downloads\<SubjectFolder>\<SubfolderName>_<YYYY-MM-DD>`
          *(e.g. `C:\Users\Aaradhya\Downloads\EX725 Exam\EX725_2026-10-02`)*
       3. Copy the selected/requested files into that subfolder.
       4. Dispatch that newly created dated folder via LocalSend.

---

## 🛠️ Automated Execution Workflow

### Option 1: Direct Deterministic Script (Recommended)

The skill bundles an automated script at `scripts/download_and_share.mjs` that executes the full pipeline end-to-end:

```powershell
# 1. Download all artifacts from URL directly to subject downloads folder:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "https://notebook.google.com/notebook/56cdad30-13d3-4621-a0b7-8f841858476b"

# 2. Download and share the entire subject folder to V2029:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "https://notebook.google.com/notebook/56cdad30-13d3-4621-a0b7-8f841858476b" --share --to "V2029"

# 3. Share the existing folder only (without re-downloading):
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --share-only --to "V2029"

# 4. Share files only (automatically creates <Folder>_YYYY-MM-DD subfolder and shares):
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --files-only --to "V2029"

# 5. Share files only with keyword filter:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --files-only --filter "Chapter" --to "V2029"
```

---

### Option 2: Step-by-Step CLI Execution

If executing step-by-step manually:

#### Step 1: Identify Notebook & Resolve Path
```powershell
nlm notebook get <notebook_id> --json
# Read title -> Map to C:\Users\Aaradhya\Downloads\<Subject> Exam
```

#### Step 2: Download Outside Repository
```powershell
# Stage outside repo in a temporary staging folder
$staging = "C:\Users\Aaradhya\Downloads\_nlm_staging_$([guid]::NewGuid().ToString().Substring(0,8))"
nlm download all <notebook_id> --output-dir "$staging" --skip-existing --interactive-format markdown

# Move all files into the subject folder
$dest = "C:\Users\Aaradhya\Downloads\<Subject> Exam"
Get-ChildItem -Path "$staging" -Recurse -File | Move-Item -Destination "$dest" -Force
Remove-Item -Path "$staging" -Recurse -Force
```

#### Step 3: LocalSend Sharing via `localsend-mcp`

Use `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\localsend-mcp` client:

- **For Whole Folder**:
  ```javascript
  const payloads = collectPayloads(['C:\\Users\\Aaradhya\\Downloads\\<Subject> Exam']);
  await sendFiles(config, { peer, payloads });
  ```

- **For Files Only (Dated Subfolder)**:
  ```javascript
  const dateStr = new Date().toISOString().slice(0, 10);
  const subfolder = path.join('C:\\Users\\Aaradhya\\Downloads\\<Subject> Exam', `<Subject>_${dateStr}`);
  fs.mkdirSync(subfolder, { recursive: true });
  // Copy files to subfolder
  for (const f of selectedFiles) {
    fs.copyFileSync(path.join(sourceDir, f), path.join(subfolder, f));
  }
  const payloads = collectPayloads([subfolder]);
  await sendFiles(config, { peer, payloads });
  ```

---

## 🔒 Verification & Safety Gates

1. **Repo Cleanliness Check**:
   Immediately run `git status --short` after downloads to verify no files were placed in the repo working tree.
2. **LocalSend Peer Reachability**:
   Confirm the target device (e.g. `V2029`) is discovered on LAN before dispatching file transfers.
