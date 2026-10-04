# Preeti ↔ Unicode (Nirmala UI) Nepali Font Converter & Quick Bridge
> नेपाली फन्ट रूपान्तरक — प्रीति ↔ युनिकोड (निर्मला यूआई / मङ्गल) र तत्काल सुधार सहायक

A complete, production-grade toolkit for converting between legacy Nepali office fonts (**Preeti**, **Kantipur**, **PCS Nepali**) and modern standard **Unicode Devanagari** (**Nirmala UI**, **Mangal**, **Kalimati**).

Includes an **Authentic Ligature Synthesizer**, a **Desktop GUI**, an **Offline Single-Page Web App**, and a **Quick-Correction Companion** (`quick_bridge.py`) with a global hotkey bridge for instant word/sentence corrections while editing Word documents.

---

## 🎯 The Core Problem & Office Workflow

In government offices, schools, and organizations across Nepal:
1. **The Office Mandate (Preeti)**: Senior officers, clerks, and typists require documents in **Preeti** font. Preeti is a legacy *ASCII font illusion* — it stores standard English keyboard letters (`g`, `]`, `k`, `f`, `n`) and renders them to look like Nepali glyphs (`नेपाल`).
2. **Modern Phonetic Input (Google Input Tools / Nirmala UI)**: Fast typists use Google Input Tools Nepali (`D:\Misc Aaradhya\google input nepali`) or Windows Phonetic Devanagari (`Win + Space`), which outputs standard **Unicode Devanagari** rendered in **Nirmala UI**.
3. **The Incompatibility**:
   - Simply changing the font dropdown in Word from Nirmala UI to Preeti fails completely, causing corrupt diamonds (`◆`), missing letters, or unreadable boxes.
   - Pasting Preeti text into web browsers, email, or chat results in garbled English (`g]kfn`).
4. **The Quick-Correction Bridge**: This toolkit bridges the gap by allowing you to type phonetically with Google Input Tools (`Win+Space`) and instantly convert text into authentic Preeti keystrokes for your father's or colleagues' office documents.

---

## 🚀 4 Ways to Use This Toolkit

### Option 1: Quick-Correction Companion (Best for Fast Editing in Word)
Double-click **`quick_bridge.bat`** (or launch from GUI):
```cmd
quick_bridge.bat
```
Features:
- **Global Hotkey (`Ctrl+Alt+P`)**: Highlight any Unicode Nepali word in Word, press `Ctrl+C`, then press `Ctrl+Alt+P`. The text in your clipboard is instantly translated into authentic Preeti keystrokes, ready to paste (`Ctrl+V`) into your Preeti document. A subtle toast notification confirms the conversion.
- **Floating Mini-Widget (`Ctrl+Alt+M`)**: A tiny, always-on-top draggable pill. Type or paste with Google Input Tools; see the authentic Preeti keystrokes live, and press **Enter** or click **Copy** to grab the result.
- **System Tray Resident**: Sits quietly in the Windows system tray with right-click options to toggle the widget or quit. Dual-backend architecture uses `keyboard` library or native zero-dependency Windows `ctypes` hotkeys.

---

### Option 2: Full Desktop Application (Best for Long Text & Documents)
Double-click **`run.bat`**:
```cmd
run.bat
```
Features 3 powerful tabs:
- **📝 Text Converter Tab**: Side-by-side dual-pane converter with live counters, auto-detection, copy, paste, swap, and reverse conversion.
- **📄 Word Document (.docx) Tab**: Select any `.docx` file, convert all Devanagari runs into authentic Preeti (or vice-versa), update font attributes, and preserve 100% of English text, tables, styles, and spacing.
- **⌨️ Keyboard Map Tab**: Quick visual cheat sheet for all consonants, vowels, matras, and complex conjuncts.
- **⚡ Quick Bridge Launcher**: One-click header button to spawn or focus the background hotkey companion.

---

### Option 3: Zero-Install Standalone Web App (Best for Restricted Office PCs)
If an office PC has strict administrative restrictions (cannot install Python or run `.bat` files):
- Simply double-click **`index.html`**!
- Opens instantly in Google Chrome, Microsoft Edge, or Mozilla Firefox.
- **100% Offline**: Requires zero internet connection and sends zero data to external servers.
- Features real-time typing conversion, clipboard copy/paste, and the exact same authentic ligature synthesizer as the Python engine.

---

### Option 4: Command Line (CLI) & Python Automation
```bash
# Convert Preeti string to Unicode Devanagari
python converter_engine.py "g]kfn"
# Output: नेपाल

# Convert Unicode Devanagari string to Preeti
python converter_engine.py --u2p "नेपाल"
# Output: g]kfn

# Convert an entire Word (.docx) document (Unicode -> Preeti)
python converter_engine.py --docx "Report_Nirmala.docx" "Report_Preeti.docx" --dir u2p

# Convert Word document (Preeti -> Unicode Nirmala UI)
python converter_engine.py --docx "Report_Preeti.docx" "Report_Unicode.docx" --dir p2u
```

---

## 🔤 Authentic Ligature Synthesizer & Rules

Unlike basic converters that produce decomposed halant sequences (e.g. `gd;\t]`), this engine synthesizes **authentic typist keystrokes** matching standard Nepali office conventions:

| Nepali (Unicode) | Authentic Preeti | Keystroke Notes |
| :--- | :--- | :--- |
| **नमस्ते** | `gd:t]` | Shift-key half-consonant `:` (स्) + `t]` (ते) |
| **प्रमुख** | `k\|d'v` | Subscript-ra `\|` (्र) + `d'v` (मुख) |
| **कार्यक्रम** | `sfo{s\|d` | Reph `{` placed after `o` + subscript-ra `\|` |
| **अध्यक्ष** | `cWoIf` | Half-dha `W` + full conjunct `If` (क्ष) |
| **सम्बन्धित** | `;DalGwt` | Half-ma `D`, half-na `G`, short-i `l` before cluster |
| **नेतृत्व** | `g]t[Tj` | Ri-matra `[` + half-ta `T` + `j` |
| **प्रोग्राम** | `k\|f]u\|fd` | Subscript-ra `\|` on `k` and `u` |
| **कोअर्डिनेटर** | `sf]cl8{g]6/` | Reph `{` after `8` + matra `]` |
| **राष्ट्रिय** | `/fli6\|o` | Short-i `l` placed before cluster `i6\|` (ष्ट्र) |
| **विद्यालय** | `ljBfno` | Special conjunct `B` (द्य) |
| **द्वन्द्व** | `åGå` | Special conjunct `å` (द्व) + half-na `G` |
| **बैठक** | `a}7s` | Ai-matra `}` |
| **लायन** | `nfog` | Standard vowels and consonants |

---

## 📂 Non-Destructive Word (.docx) Conversion

When converting `.docx` documents:
- **English Headings & Content**: (e.g. `Lions International District 325 C`, `$15,000 USD`, dates, email addresses) remain **100% untouched** in their original fonts (`Calibri`, `Times New Roman`, `Arial`).
- **Formatting Preservation**: Table borders, column widths, row heights, bullet lists, numbering, bold/italic styles, margins, and headers/footers are **fully preserved**.
- **Font Attributes**: When converting to Preeti, XML run fonts are set to `<w:rFonts w:ascii="Preeti" w:hAnsi="Preeti" w:cs="Preeti"/>`. When converting to Unicode, fonts are set to `Nirmala UI`.

---

## 🏗️ Repository Structure

```
tools/preeti-converter/
├── converter_engine.py    # Bidirectional engine + OpenXML .docx processor (28/28 tests passed)
├── quick_bridge.py       # Global hotkey (Ctrl+Alt+P) + floating mini-widget (Ctrl+Alt+M)
├── converter_gui.py      # Tkinter GUI with High-DPI scaling, MD3 theme & Quick-Bridge launcher
├── quick_bridge.bat      # One-click silent background launcher for Quick Bridge companion
├── run.bat               # One-click GUI launcher
├── index.html            # Standalone zero-install 100% offline Web app
└── README.md             # Complete user and technical guide
```

---

## ⚙️ Dependencies

- **Python 3.9+** (standard Windows installation)
- **`python-docx`** (automatically verified and installed via `run.bat` for `.docx` support)
- **`keyboard`** and **`pystray` + `Pillow`** (optional, automatically installed by `quick_bridge.bat`; falls back to zero-dependency Windows `ctypes` hotkeys if missing)
- **Zero Internet Requirement**: All engines run locally and offline.
