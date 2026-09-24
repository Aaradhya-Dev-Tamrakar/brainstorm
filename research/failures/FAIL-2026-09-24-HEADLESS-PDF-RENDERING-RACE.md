# Incident / Failure Report: Headless PDF Rendering Race Condition & 404 Capture

```text
Incident ID:       FAIL-2026-09-24-HEADLESS-PDF-RACE
Date / Timestamp:  2026-09-24T16:00:00+05:45
Component:         Document Export Pipeline / Typora MCP / Headless Edge PDF Rendering
Severity:          Medium (Document Integrity Corruption — Rendered 404 Error Page into PDF)
Resolution Status: RESOLVED
Verification Tier: E4 (Experimentally Verified)
```

---

## 1. Description of the Incident
When exporting research documents (`RESEARCH_PROFILE.md`, `SPARK_1PAGE.md`, etc.) to PDF using a headless Chromium/Edge subprocess, all generated PDF files were approximately 59 KB in size. Opening the PDFs revealed that rather than the formatted markdown content, the PDF contained an embedded browser error page:
> **"File not found. It may have been moved, edited, or deleted. ERR_FILE_NOT_FOUND"**

---

## 2. Root Cause Analysis

Two interacting bugs caused this failure:

1. **Premature Intermediate File Deletion (Async Race Condition):**
   The script generated a temporary `.html` file from markdown, spawned `msedge.exe --headless --print-to-pdf`, and immediately deleted the `.html` file without awaiting process termination. When Edge started rendering the DOM, the underlying `.html` file was already unlinked from disk.
2. **Malformed Local File Path vs. URI Scheme:**
   Headless Chromium on Windows requires a fully qualified `file:///` URI scheme (e.g., `file:///C:/Users/.../temp.html`) rather than raw filesystem paths when passed as command-line arguments to `--print-to-pdf`. Passing raw paths caused Edge to fail navigation, rendering the built-in 404 page into the resulting PDF.

---

## 3. Corrective Actions & Resolution

1. **Ecosystem-Wide Invariant (`INV-PDF-001`):**
   - Headless PDF generation must always convert filesystem paths to valid URI schemes using standard libraries (`[System.Uri]::new($path).AbsoluteUri` or `pathToFileURL(path).href`).
   - The headless browser process must be synchronously awaited (`Start-Process -Wait` or `execFileSync`) before any cleanup of intermediate files.
2. **`typora-mcp` Upgrade:**
   - Implemented first-class `typora_export_pdf` tool in `typora-mcp` with automatic browser discovery, RFC-compliant `file:///` URI resolution via `url.pathToFileURL`, and synchronous subprocess lifecycle management.
   - Built and synced to `origin/main` (`0e2653e`).
3. **Skill & Protocol Update:**
   - Documented headless PDF rendering rules in `doc-archiver/SKILL.md`.
