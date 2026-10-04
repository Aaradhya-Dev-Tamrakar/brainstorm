"""
Preeti ↔ Unicode Converter — Desktop GUI Application
=====================================================
A clean, user-friendly desktop GUI for converting between legacy Nepali fonts
(Preeti, Kantipur, PCS Nepali) and standard Unicode Devanagari (Nirmala UI / Mangal).

Designed specifically for office workers, government staff, and students:
  • Bidirectional live text conversion (Preeti ↔ Unicode Nirmala UI)
  • .docx Word document conversion preserving tables, English text, and formatting
  • One-click Open Converted File / Open Folder
  • Built-in Preeti keyboard layout cheat sheet and common office ligatures

Author: Aaradhya Dev Tamrakar
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

# Ensure the converter engine is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from converter_engine import (
    preeti_to_unicode,
    unicode_to_preeti,
    convert_docx,
    detect_encoding,
    SUPPORTED_LEGACY_FONTS,
    KNOWN_UNICODE_FONTS,
)


class PreetiConverterApp:
    """Main application window."""

    # ── Color Palette (Dark theme inspired by Material Design 3) ──
    BG = "#1C1B1F"
    SURFACE = "#2B2930"
    SURFACE_HIGH = "#36343B"
    PRIMARY = "#D0BCFF"       # Purple accent
    ON_PRIMARY = "#381E72"
    SECONDARY = "#CCC2DC"
    ON_SURFACE = "#E6E1E5"
    ON_SURFACE_VARIANT = "#CAC4D0"
    OUTLINE = "#49454F"
    ERROR = "#F2B8B5"
    SUCCESS = "#A8DAB5"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("प्रीति ↔ यूनिकोड | Preeti ↔ Unicode (Nirmala UI) Converter")
        self.root.geometry("980x740")
        self.root.minsize(780, 580)
        self.root.configure(bg=self.BG)

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self._create_styles()
        self._create_widgets()
        self._bind_shortcuts()

    def _create_styles(self):
        """Configure ttk styles for the dark theme."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(".", background=self.BG, foreground=self.ON_SURFACE)
        self.style.configure("TFrame", background=self.BG)
        self.style.configure("Surface.TFrame", background=self.SURFACE)
        self.style.configure("TLabel", background=self.BG, foreground=self.ON_SURFACE, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI Semibold", 16), foreground=self.PRIMARY)
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 9), foreground=self.ON_SURFACE_VARIANT)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground=self.SUCCESS, background=self.SURFACE)

        self.style.configure(
            "Accent.TButton",
            background=self.PRIMARY,
            foreground=self.ON_PRIMARY,
            font=("Segoe UI Semibold", 10),
            padding=(16, 8),
            borderwidth=0,
        )
        self.style.map("Accent.TButton",
            background=[("active", self.SECONDARY), ("disabled", self.OUTLINE)],
            foreground=[("disabled", self.ON_SURFACE_VARIANT)],
        )

        self.style.configure(
            "Secondary.TButton",
            background=self.SURFACE_HIGH,
            foreground=self.ON_SURFACE,
            font=("Segoe UI", 9),
            padding=(12, 6),
            borderwidth=0,
        )
        self.style.map("Secondary.TButton",
            background=[("active", self.OUTLINE)],
        )

        self.style.configure("TNotebook", background=self.BG, borderwidth=0)
        self.style.configure("TNotebook.Tab",
            background=self.SURFACE,
            foreground=self.ON_SURFACE_VARIANT,
            font=("Segoe UI", 10),
            padding=(20, 8),
        )
        self.style.map("TNotebook.Tab",
            background=[("selected", self.SURFACE_HIGH)],
            foreground=[("selected", self.PRIMARY)],
        )

    def _create_widgets(self):
        """Build the complete UI with 3 functional tabs."""
        # ── Header ──
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=(16, 6))

        ttk.Label(header, text="नेपाली फन्ट रूपान्तरक", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="Preeti ↔ Unicode (Nirmala UI / Mangal)", style="Subtitle.TLabel").pack(side="left", padx=(14, 0), pady=(4, 0))

        # ── Notebook (Tabs) ──
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(6, 16))

        # Tab 1: Text Converter
        self._create_text_tab()

        # Tab 2: Word Document (.docx) Converter
        self._create_file_tab()

        # Tab 3: Preeti Keyboard Cheat Sheet
        self._create_cheatsheet_tab()

    # ═══════════════════════════════════════════════════════════════════════
    #  TAB 1: TEXT CONVERTER
    # ═══════════════════════════════════════════════════════════════════════

    def _create_text_tab(self):
        tab = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(tab, text="  📝 Text Converter (अक्षर रूपान्तरण)  ")

        # Top control bar
        top_bar = ttk.Frame(tab, style="Surface.TFrame")
        top_bar.pack(fill="x", padx=16, pady=(14, 6))

        self.direction_var = tk.StringVar(value="p2u")

        ttk.Label(top_bar, text="Mode:", background=self.SURFACE, font=("Segoe UI Semibold", 9)).pack(side="left", padx=(0, 8))

        modes = [
            ("Preeti → Unicode (Nirmala UI)", "p2u"),
            ("Unicode (Nirmala UI) → Preeti", "u2p"),
            ("Auto-detect (स्वतः पहिचान)", "auto"),
        ]
        for label, val in modes:
            rb = tk.Radiobutton(
                top_bar, text=label, variable=self.direction_var, value=val,
                bg=self.SURFACE, fg=self.ON_SURFACE, selectcolor=self.SURFACE_HIGH,
                activebackground=self.SURFACE, activeforeground=self.PRIMARY,
                font=("Segoe UI", 9),
            )
            rb.pack(side="left", padx=(0, 14))

        # Panels (Input & Output)
        panels = ttk.Frame(tab, style="Surface.TFrame")
        panels.pack(fill="both", expand=True, padx=16, pady=4)
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(2, weight=1)
        panels.rowconfigure(1, weight=1)

        # Input label & count
        in_header = ttk.Frame(panels, style="Surface.TFrame")
        in_header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(in_header, text="Input (यता पेस्ट वा टाइप गर्नुहोस्):",
                  background=self.SURFACE, foreground=self.ON_SURFACE_VARIANT).pack(side="left")
        self.in_count_label = ttk.Label(in_header, text="0 chars", background=self.SURFACE, foreground=self.SECONDARY, font=("Segoe UI", 8))
        self.in_count_label.pack(side="right")

        self.input_text = scrolledtext.ScrolledText(
            panels, wrap="word", height=12, font=("Consolas", 11),
            bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
            selectbackground=self.PRIMARY, selectforeground=self.ON_PRIMARY,
            borderwidth=0, padx=10, pady=10,
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        self.input_text.bind("<KeyRelease>", self._on_input_change)

        # Center control buttons
        btn_frame = ttk.Frame(panels, style="Surface.TFrame")
        btn_frame.grid(row=1, column=1, padx=10)

        ttk.Button(btn_frame, text="Convert →", style="Accent.TButton",
                   command=self._convert_text).pack(pady=4)
        ttk.Button(btn_frame, text="Swap ⇄", style="Secondary.TButton",
                   command=self._swap_panels).pack(pady=4)
        ttk.Button(btn_frame, text="← Reverse", style="Secondary.TButton",
                   command=self._reverse_convert).pack(pady=4)
        ttk.Button(btn_frame, text="Clear All", style="Secondary.TButton",
                   command=self._clear_all).pack(pady=4)

        # Output label & count
        out_header = ttk.Frame(panels, style="Surface.TFrame")
        out_header.grid(row=0, column=2, sticky="ew", pady=(0, 4))
        ttk.Label(out_header, text="Output (रूपान्तरित नतिजा):",
                  background=self.SURFACE, foreground=self.ON_SURFACE_VARIANT).pack(side="left")
        self.out_count_label = ttk.Label(out_header, text="0 chars", background=self.SURFACE, foreground=self.SECONDARY, font=("Segoe UI", 8))
        self.out_count_label.pack(side="right")

        self.output_text = scrolledtext.ScrolledText(
            panels, wrap="word", height=12, font=("Nirmala UI", 12),
            bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
            selectbackground=self.PRIMARY, selectforeground=self.ON_PRIMARY,
            borderwidth=0, padx=10, pady=10,
        )
        self.output_text.grid(row=1, column=2, sticky="nsew", pady=(0, 8))

        # Bottom action bar
        action_bar = ttk.Frame(tab, style="Surface.TFrame")
        action_bar.pack(fill="x", padx=16, pady=(0, 14))

        ttk.Button(action_bar, text="📋 Paste from Clipboard", style="Secondary.TButton",
                   command=self._paste_from_clipboard).pack(side="left", padx=(0, 8))
        ttk.Button(action_bar, text="📋 Copy Converted Output", style="Secondary.TButton",
                   command=self._copy_output).pack(side="left", padx=(0, 8))

        self.text_status = ttk.Label(action_bar, text="", style="Status.TLabel")
        self.text_status.pack(side="right")

    def _on_input_change(self, event=None):
        text = self.input_text.get("1.0", "end-1c")
        chars = len(text)
        words = len(text.split())
        self.in_count_label.configure(text=f"{chars} chars, {words} words")

    # ═══════════════════════════════════════════════════════════════════════
    #  TAB 2: WORD DOCUMENT (.DOCX) CONVERTER
    # ═══════════════════════════════════════════════════════════════════════

    def _create_file_tab(self):
        tab = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(tab, text="  📄 Word Document (.docx)  ")

        # Instruction card
        info_frame = ttk.Frame(tab, style="Surface.TFrame")
        info_frame.pack(fill="x", padx=20, pady=(16, 8))

        info_text = (
            "Select any Microsoft Word (.docx) file to convert.\n"
            "• Preserves English headers, numbers, tables, colors, bullet points, and layout perfectly.\n"
            "• Automatically scans every paragraph, table cell, header, footer, and shape.\n"
            "• Converts Preeti font text to true Unicode Devanagari (Nirmala UI), or vice versa."
        )
        ttk.Label(info_frame, text=info_text, background=self.SURFACE,
                  foreground=self.ON_SURFACE_VARIANT, font=("Segoe UI", 9),
                  wraplength=850, justify="left").pack(anchor="w")

        # File selection box
        file_frame = ttk.Frame(tab, style="Surface.TFrame")
        file_frame.pack(fill="x", padx=20, pady=8)
        file_frame.columnconfigure(1, weight=1)

        # Input file
        ttk.Label(file_frame, text="Input .docx:", background=self.SURFACE).grid(row=0, column=0, sticky="w", pady=6)
        self.input_file_var = tk.StringVar()
        input_entry = tk.Entry(file_frame, textvariable=self.input_file_var,
                               bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
                               font=("Segoe UI", 9), borderwidth=0)
        input_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=6)
        ttk.Button(file_frame, text="Browse...", style="Secondary.TButton",
                   command=self._browse_input).grid(row=0, column=2, pady=6)

        # Output file
        ttk.Label(file_frame, text="Output .docx:", background=self.SURFACE).grid(row=1, column=0, sticky="w", pady=6)
        self.output_file_var = tk.StringVar()
        output_entry = tk.Entry(file_frame, textvariable=self.output_file_var,
                                bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
                                font=("Segoe UI", 9), borderwidth=0)
        output_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        ttk.Button(file_frame, text="Browse...", style="Secondary.TButton",
                   command=self._browse_output).grid(row=1, column=2, pady=6)

        # Options frame
        opts_frame = ttk.Frame(tab, style="Surface.TFrame")
        opts_frame.pack(fill="x", padx=20, pady=8)

        self.file_direction_var = tk.StringVar(value="auto")

        ttk.Label(opts_frame, text="Direction:", background=self.SURFACE, font=("Segoe UI Semibold", 9)).pack(side="left")
        dir_options = [
            ("Auto-detect (सिफारिस गरिएको)", "auto"),
            ("Preeti → Unicode (Nirmala UI)", "p2u"),
            ("Unicode (Nirmala UI) → Preeti", "u2p"),
        ]
        for text, val in dir_options:
            rb = tk.Radiobutton(
                opts_frame, text=text, variable=self.file_direction_var, value=val,
                bg=self.SURFACE, fg=self.ON_SURFACE, selectcolor=self.SURFACE_HIGH,
                activebackground=self.SURFACE, activeforeground=self.PRIMARY,
                font=("Segoe UI", 9),
            )
            rb.pack(side="left", padx=(14, 0))

        # Target Unicode Font
        target_frame = ttk.Frame(tab, style="Surface.TFrame")
        target_frame.pack(fill="x", padx=20, pady=6)

        ttk.Label(target_frame, text="Target Unicode Font:", background=self.SURFACE).pack(side="left")
        self.target_unicode_font_var = tk.StringVar(value="Nirmala UI")
        font_dropdown = ttk.Combobox(
            target_frame, textvariable=self.target_unicode_font_var,
            values=["Nirmala UI", "Mangal", "Kalimati", "Noto Sans Devanagari"],
            width=20, state="readonly"
        )
        font_dropdown.pack(side="left", padx=(10, 0))

        # Action Buttons
        convert_frame = ttk.Frame(tab, style="Surface.TFrame")
        convert_frame.pack(fill="x", padx=20, pady=12)

        ttk.Button(convert_frame, text="🔄 Convert Word Document", style="Accent.TButton",
                   command=self._convert_file).pack(side="left")

        self.open_file_btn = ttk.Button(convert_frame, text="📂 Open Converted File", style="Secondary.TButton",
                                        command=self._open_converted_file, state="disabled")
        self.open_file_btn.pack(side="left", padx=(10, 0))

        self.open_folder_btn = ttk.Button(convert_frame, text="📁 Open Folder", style="Secondary.TButton",
                                          command=self._open_folder, state="disabled")
        self.open_folder_btn.pack(side="left", padx=(8, 0))

        self.file_status = ttk.Label(convert_frame, text="", style="Status.TLabel")
        self.file_status.pack(side="left", padx=(16, 0))

        # Conversion Log
        log_frame = ttk.Frame(tab, style="Surface.TFrame")
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        ttk.Label(log_frame, text="Conversion Activity Log:", background=self.SURFACE,
                  foreground=self.ON_SURFACE_VARIANT).pack(anchor="w", pady=(0, 4))

        self.log_text = scrolledtext.ScrolledText(
            log_frame, wrap="word", height=6, font=("Consolas", 9),
            bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
            borderwidth=0, padx=8, pady=8, state="disabled",
        )
        self.log_text.pack(fill="both", expand=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  TAB 3: PREETI KEYBOARD CHEAT SHEET
    # ═══════════════════════════════════════════════════════════════════════

    def _create_cheatsheet_tab(self):
        tab = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(tab, text="  ⌨️ Preeti Keyboard Map & Office Tips  ")

        # Scrollable container
        container = scrolledtext.ScrolledText(
            tab, wrap="word", font=("Consolas", 10),
            bg=self.SURFACE_HIGH, fg=self.ON_SURFACE, insertbackground=self.PRIMARY,
            borderwidth=0, padx=16, pady=16
        )
        container.pack(fill="both", expand=True, padx=16, pady=16)

        cheat_text = r"""
═══════════════════════════════════════════════════════════════════════════════
        PREETI FONT QUICK TYPING & REFERENCE CHEAT SHEET
═══════════════════════════════════════════════════════════════════════════════

1. BASIC CONSONANTS (क देखि ज्ञ सम्म):
   Key   Normal   Shift     |   Key   Normal   Shift
   ───   ──────   ─────     |   ───   ──────   ─────
   s     क        क्        |   v     ख        ख्
   u     ग        ग्        |   3     घ        घ् (£)
   r     च        च्        |   5     छ        छ् (5\\)
   h     ज        ज्        |   `     ञ        ञ् (~)
   6     ट        ट्ट (§)   |   7     ठ        ठ्ठ (¶)
   8     ड        ड्ड (•)   |   9     ढ        ढ्
   0     ण        ण्        |   t     त        त्
   y     थ        थ्        |   b     द        द्य (B)
   w     ध        ध्        |   g     न        न्
   k     प        प्        |   e     भ        भ् (E)
   a     ब        ब्        |   d     म        म्
   o     य        य्        |   /     र        (Reph: {)
   n     ल        ल्        |   j     व        व्
   z     श        श्        |   i     ष्       क्ष् (I)
   ;     स        स्        |   x     ह        ह्
   q     त्र      त्त (Q)   |   1     ज्ञ      ज्ञ् (¡)

2. VOWELS & MATRAS (स्वर र मात्रा):
   Key   Normal   Shift     |   Key   Normal   Shift
   ───   ──────   ─────     |   ───   ──────   ─────
   c     अ        ऋ         |   P     ए        (ऐ: P])
   p     उ        ऊ (pm)    |   O     इ        (ई: O{)
   f     ा (आकार)           |   l     ि (ह्रस्व इकार - अगाडि टाइप गर्ने)
   L     ी (दीर्घ ईकार)    |   '     ु (ह्रस्व उकार)
   "     ू (दीर्घ ऊकार)    |   [     ृ (ऋकार)
   ]     े (एकार)          |   }     ै (ऐकार)
   +     ं (शिरबिन्दु)      |   F     ँ (चन्द्रबिन्दु)
   m     ः (विसर्ग)        |   .     । (पूर्णविराम)

3. IMPORTANT OFFICE WORDS IN PREETI:
   Nepali Unicode          Preeti Keystrokes
   ──────────────          ─────────────────
   नेपाल                   g]kfn
   सेवा                    ;]jf
   नमस्ते                  gd:t]
   बैठक                    a}7s
   सदस्यता                 ;b:otf
   नेतृत्व                  g]t[Tj
   कार्यक्रम               sfo{s|d  वा  sfo{qmd
   प्रोग्राम               k|f]u|fd
   कोअर्डिनेटर             sf]cl8{g]6/
   सम्बन्धित               ;DalGwt  वा  ;d\ag\lwt
   अध्यक्ष                 cWoIf
   प्रमुख                  k|d'v
   अन्य                    cGo
   गतिविधि                 ultljlw
   चुनौतीहरू               r'gff}tLx?

4. WHY PREETI & NIRMALA UI CONFLICT:
   • Preeti is a "Font-Illusion" (ASCII-based): It stores standard English letters
     (like 'g', ']', 'k') and merely paints them to look like Nepali glyphs.
   • Nirmala UI / Mangal is standard Unicode Devanagari: Each Nepali letter has its
     own official world-standard codepoint (U+0900..U+097F).
   • Changing the font name in Word without converting the underlying codes causes
     unreadable gibberish and diamond replacement characters (◆).
   • This tool converts the actual underlying data so both systems understand it!
═══════════════════════════════════════════════════════════════════════════════
"""
        container.insert("1.0", cheat_text)
        container.configure(state="disabled")

    # ═══════════════════════════════════════════════════════════════════════
    #  HANDLERS
    # ═══════════════════════════════════════════════════════════════════════

    def _convert_text(self):
        text = self.input_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_text_status("⚠ No input text", error=True)
            return

        direction = self.direction_var.get()
        if direction == "auto":
            enc = detect_encoding(text)
            if enc == "unicode":
                res = unicode_to_preeti(text)
                self._set_text_status("✓ Auto-detected Unicode → converted to Preeti")
            else:
                res = preeti_to_unicode(text)
                self._set_text_status("✓ Auto-detected Preeti → converted to Unicode")
        elif direction == "p2u":
            res = preeti_to_unicode(text)
            self._set_text_status("✓ Converted Preeti → Unicode (Nirmala UI)")
        else:
            res = unicode_to_preeti(text)
            self._set_text_status("✓ Converted Unicode → Preeti")

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)

        out_chars = len(res)
        out_words = len(res.split())
        self.out_count_label.configure(text=f"{out_chars} chars, {out_words} words")

    def _reverse_convert(self):
        text = self.output_text.get("1.0", "end-1c")
        if not text.strip():
            self._set_text_status("⚠ No output text to reverse", error=True)
            return

        direction = self.direction_var.get()
        if direction == "p2u":
            res = unicode_to_preeti(text)
        elif direction == "u2p":
            res = preeti_to_unicode(text)
        else:
            res = preeti_to_unicode(text)

        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", res)
        self._on_input_change()
        self._set_text_status("✓ Reverse conversion applied to input panel")

    def _swap_panels(self):
        in_t = self.input_text.get("1.0", "end-1c")
        out_t = self.output_text.get("1.0", "end-1c")

        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", out_t)

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", in_t)

        self._on_input_change()
        self.out_count_label.configure(text=f"{len(in_t)} chars, {len(in_t.split())} words")
        self._set_text_status("⇄ Swapped input and output panels")

    def _clear_all(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.in_count_label.configure(text="0 chars")
        self.out_count_label.configure(text="0 chars")
        self._set_text_status("Cleared")

    def _paste_from_clipboard(self):
        try:
            text = self.root.clipboard_get()
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)
            self._on_input_change()
            self._set_text_status(f"📋 Pasted {len(text)} characters from clipboard")
        except tk.TclError:
            self._set_text_status("⚠ Clipboard is empty", error=True)

    def _copy_output(self):
        text = self.output_text.get("1.0", "end-1c")
        if text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._set_text_status("📋 Copied output to clipboard!")
        else:
            self._set_text_status("⚠ Nothing to copy", error=True)

    def _set_text_status(self, msg: str, error: bool = False):
        self.text_status.configure(
            text=msg,
            foreground=self.ERROR if error else self.SUCCESS
        )

    # ── File conversion handlers ──

    def _browse_input(self):
        path = filedialog.askopenfilename(
            title="Select Word (.docx) Document",
            filetypes=[("Word Documents (*.docx)", "*.docx"), ("All Files", "*.*")],
        )
        if path:
            self.input_file_var.set(path)
            stem = Path(path).stem
            parent = Path(path).parent
            self.output_file_var.set(str(parent / f"{stem}_converted.docx"))
            self._log(f"Selected file: {path}")

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Converted Document As",
            defaultextension=".docx",
            filetypes=[("Word Documents (*.docx)", "*.docx"), ("All Files", "*.*")],
        )
        if path:
            self.output_file_var.set(path)

    def _log(self, msg: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _convert_file(self):
        inp = self.input_file_var.get().strip()
        outp = self.output_file_var.get().strip()

        if not inp:
            messagebox.showerror("Missing File", "Please select an input .docx file first.")
            return
        if not outp:
            messagebox.showerror("Missing Destination", "Please specify an output .docx destination.")
            return
        if not os.path.exists(inp):
            messagebox.showerror("Not Found", f"Cannot find file:\n{inp}")
            return

        direction_choice = self.file_direction_var.get()
        dir_arg = "auto"
        if direction_choice == "p2u":
            dir_arg = "preeti_to_unicode"
        elif direction_choice == "u2p":
            dir_arg = "unicode_to_preeti"

        target_u_font = self.target_unicode_font_var.get().strip() or "Nirmala UI"

        self._log(f"{'═' * 60}")
        self._log(f"Starting conversion: {inp}")
        self._log(f"Mode: {dir_arg} | Target Unicode Font: {target_u_font}")

        try:
            stats = convert_docx(
                input_path=inp,
                output_path=outp,
                direction=dir_arg,
                target_unicode_font=target_u_font
            )
            self._log(f"✓ Converted: {stats['runs_converted']} of {stats['runs_total']} text runs")
            self._log(f"✓ Detected Fonts in Document: {stats['fonts_detected']}")
            self._log(f"✓ Successfully saved to: {outp}")

            self.file_status.configure(
                text=f"✓ Done! {stats['runs_converted']} runs converted",
                foreground=self.SUCCESS
            )
            self.open_file_btn.configure(state="normal")
            self.open_folder_btn.configure(state="normal")

            messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted document!\n\n"
                f"Runs converted: {stats['runs_converted']}\n"
                f"Target font: {target_u_font}\n"
                f"Saved to: {outp}"
            )

        except Exception as e:
            self._log(f"✗ Conversion error: {e}")
            self.file_status.configure(text=f"✗ Error: {e}", foreground=self.ERROR)
            messagebox.showerror("Error", f"Failed to convert document:\n{e}")

    def _open_converted_file(self):
        outp = self.output_file_var.get().strip()
        if outp and os.path.exists(outp):
            try:
                os.startfile(outp)
            except Exception as e:
                messagebox.showerror("Cannot Open", str(e))

    def _open_folder(self):
        outp = self.output_file_var.get().strip()
        if outp:
            folder = os.path.dirname(os.path.abspath(outp))
            if os.path.exists(folder):
                try:
                    os.startfile(folder)
                except Exception as e:
                    messagebox.showerror("Cannot Open", str(e))

    def _bind_shortcuts(self):
        self.root.bind("<Control-Return>", lambda e: self._convert_text())
        self.root.bind("<Control-Shift-Return>", lambda e: self._reverse_convert())
        self.root.bind("<Control-Shift-C>", lambda e: self._copy_output())
        self.root.bind("<Control-Shift-V>", lambda e: self._paste_from_clipboard())


def main():
    root = tk.Tk()

    # Windows High-DPI crisp rendering
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = PreetiConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
