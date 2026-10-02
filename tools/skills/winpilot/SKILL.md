---
name: winpilot
description: Expert Windows UI automation, screen perception, window management, and silent screenshot capture using the local WinPilot framework (F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot). Use whenever interacting with active desktop windows, reading UI Automation (UIA) trees, capturing/saving window screenshots, or extracting content from native apps and browsers.
category: automation
---

# WinPilot — Windows UI Automation & Perception Engine

This skill equips agents with precise knowledge of **WinPilot** (`F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot`), Aaradhya's custom Windows OS automation, screen perception, and UIA inspection framework.

---

## 1. Environment & Python Runtime
WinPilot dependencies (`pywinauto`, `Pillow`, `typer`, `rich`, `mcp`, `pywin32`) are pre-installed in its dedicated virtual environment:
* **Python Executable:** `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe`
* **Root Path:** `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot`

When executing WinPilot scripts via command line, always prepend the project directory to `sys.path` and use the `.venv` interpreter:
```python
import sys
sys.path.insert(0, r"F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot")
```

---

## 2. Core Modules & Capabilities

### A. Window Management (`winpilot.core.window`)
```python
from winpilot.core.window import Window, find_window, list_windows

# List matching windows
windows = list_windows(title_regex=r".*Chrome.*", visible_only=True)

# Find and control specific window
w = find_window(title_regex=r".*CS Academy.*")
if w:
    w.focus()     # Bypasses focus lock and uncloaks virtual desktop
    w.restore()   # Restores if minimized
    w.maximize()  # Maximizes window
    rect = w.rect # (left, top, right, bottom)
```

### B. Screen Perception & Image Capture (`winpilot.core.screen`)
WinPilot uses a silent Win32 GDI BitBlt capture engine (zero dialogs/popups):
```python
from winpilot.core.screen import Screen

# 1. Capture specific window and save to custom path
img, meta = Screen.capture_window(w)
if img:
    saved_path = Screen.save(img, r"path\to\output.png")

# 2. Capture direct to file (defaults to Windows Screenshots if dest_path=None)
saved, meta = Screen.capture_to_file(window_or_hwnd=w, dest_path=r"path\to\output.png")

# 3. Capture full multi-monitor virtual desktop
img, meta = Screen.capture_desktop()
```

### C. UI Automation & Text Extraction (`winpilot.core.uia`)
Extracts text and DOM structures directly from browsers, Electron apps, or native Win32/WPF/WinUI controls without browser extensions or HTTP scraping:
```python
from winpilot.core.uia import UIATree

tree = UIATree(w)

# Extract all text nodes
text_elements = [
    e.name for e in tree.root_element.descendants(depth=12)
    if e.control_type == "Text" and e.name.strip()
]

# Dump structured tree dictionary
dump = tree.dump_tree(max_depth=4, visible_only=True)
```

### D. Input Simulation (`winpilot.core.input`)
```python
from winpilot.core.input import Input

# Paste text via clipboard
Input.paste_text("Hello World", submit_enter=True)

# Send key combinations
Input.send_combo("ctrl", "a")
Input.send_combo("enter")
```

---

## 3. CLI Commands
The WinPilot CLI (`winpilot.cli`) supports quick operations:
```powershell
# List top-level windows
& "F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe" -m winpilot.cli list --visible-only

# Capture screenshot of window to specific destination
& "F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe" -m winpilot.cli screenshot --window "CS Academy" --output "output.png"

# Inspect UIA tree
& "F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe" -m winpilot.cli inspect "CS Academy" --depth 4
```

---

## 4. MCP Tools (`winpilot.mcp_server`)
When loaded into an MCP host, WinPilot exposes:
* `list_desktop_windows(title_regex, process_name, visible_only)`
* `focus_window(hwnd_or_title)`
* `get_ui_tree(hwnd_or_title, max_depth, visible_only)`
* `click_element(hwnd_or_title, query, method)`
* `paste_text(hwnd_or_title, text, submit_enter)`
* `send_keys(keys_combo)`
* `capture_screenshot(hwnd_or_title, output_path)` — captures window or desktop; saves directly to disk if `output_path` is specified, and returns resolution metadata + base64 PNG.
* `record_screen(hwnd_or_title, duration_seconds, fps)`
