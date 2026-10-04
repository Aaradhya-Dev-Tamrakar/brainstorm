# Preeti ↔ Unicode (Nirmala UI) Nepali Font Converter
> नेपाली फन्ट रूपान्तरक — प्रीति ↔ युनिकोड (निर्मला यूआई / मङ्गल)

A complete, production-grade toolkit for converting between legacy Nepali office fonts (**Preeti**, **Kantipur**, **PCS Nepali**) and modern standard **Unicode Devanagari** (**Nirmala UI**, **Mangal**, **Kalimati**).

---

## 🎯 The Core Problem Solved

In Nepal's offices, banks, and government institutions:
1. **Office Standard (Preeti)**: Senior staff and trained typists use **Preeti** font. Preeti is a legacy *ASCII font illusion* — it stores standard English keyboard letters (`g`, `]`, `k`, `f`, `n`) and renders them to look like Nepali glyphs (`नेपाल`).
2. **Modern Input (Nirmala UI / Windows Nepali Transliteration)**: Modern computers and Google Input Tools type in **Unicode Devanagari** (`U+0900..U+097F`), displayed using **Nirmala UI** or **Mangal**.
3. **The Incompatibility**:
   - Simply selecting text in Word and changing the font from Preeti to Nirmala UI (or vice-versa) **fails completely**, creating gibberish or diamond replacement characters (`◆`).
   - Copy-pasting Preeti text into web forms, emails, or chat shows English gibberish (`g]kfn`).
   - Preeti typing requires a trained typist because the keys do not correspond to phonetic sounds.

---

## 🚀 3 Ways to Use This Converter

### Option 1: One-Click Desktop Application (Recommended for PC)
Double-click `run.bat` in this folder:
```cmd
run.bat
```
This opens the desktop window featuring:
- **📝 Text Converter Tab**: Paste Preeti or Unicode text, click convert, copy to clipboard.
- **📄 Word Document (.docx) Tab**: Select any `.docx` file (like District Reports or Meeting Minutes), convert all Preeti paragraphs & tables into clean Nirmala UI with one click, and click **Open Converted File**.
- **⌨️ Preeti Keyboard Map Tab**: Quick reference cheat sheet for standard Preeti keys.

---

### Option 2: Zero-Install Standalone Web App (Best for Office / Government PCs)
If your father's office PC has administrative restrictions (cannot install Python or run `.bat` files):
- Simply double-click **`index.html`**!
- Opens instantly in Google Chrome, Microsoft Edge, or Firefox.
- **100% Offline**: Requires no internet connection and sends zero data to external servers.
- Features real-time instant typing conversion, swap, and clipboard integration.

---

### Option 3: Command Line (CLI) & Python Automation
```bash
# Convert Preeti string to Unicode Devanagari
python converter_engine.py "g]kfn"
# Output: नेपाल

# Convert Unicode Devanagari string to Preeti
python converter_engine.py --u2p "नेपाल"
# Output: g]kfn

# Convert an entire Word (.docx) document
python converter_engine.py --docx "Report.docx" "Report_Unicode.docx"
```

---

## 📂 Handling Word (.docx) Files Without Breaking Formatting

When converting Word documents:
- English headings (e.g. `Lions International District 325 C, Nepal`, `Subject area/Cause:`, `Highlights of Programs by Clubs`) remain **100% untouched** in their original font (`Calibri`, `Times New Roman`, etc.).
- Tables, table borders, cell alignments, bullet points, font sizes, and styles are **fully preserved**.
- Only the specific runs containing Preeti (or other legacy Nepali fonts) are translated into Unicode Devanagari with font set to **Nirmala UI**.

---

## ⌨️ Preeti Office Typing Cheat Sheet

| Nepali (Unicode) | Preeti Keystrokes | English Meaning |
| :--- | :--- | :--- |
| **नेपाल** | `g]kfn` | Nepal |
| **सेवा** | `;]jf` | Service |
| **नमस्ते** | `gd:t]` | Namaste |
| **बैठक** | `a}7s` | Meeting |
| **सदस्यता** | `;b:otf` | Membership |
| **नेतृत्व** | `g]t[Tj` | Leadership |
| **कार्यक्रम** | `sfo{s|d` | Program / Event |
| **प्रोग्राम** | `k|f]u|fd` | Program |
| **कोअर्डिनेटर** | `sf]cl8{g]6/` | Coordinator |
| **सम्बन्धित** | `;DalGwt` | Related / Concerned |
| **अध्यक्ष** | `cWoIf` | Chairperson / President |
| **प्रमुख** | `k|d'v` | Chief |
| **अन्य** | `cGo` | Other |
| **गतिविधि** | `ultljlw` | Activities |
| **चुनौतीहरू** | `r'gff}tLx?` | Challenges |

---

## 🏗️ Technical Architecture

```
tools/preeti-converter/
├── converter_engine.py     # Pure Python bidirectional engine + OpenXML .docx processor
├── converter_gui.py        # Desktop Tkinter GUI with High-DPI scaling & MD3 theme
├── index.html              # Standalone, zero-install, 100% offline Web app
├── run.bat                 # One-click Windows runner
└── README.md               # User & technical documentation
```

### Dependencies
- Python 3.9+ (bundled on Windows)
- `python-docx` (automatically installed on first run of `run.bat`)
- `tkinter` (included in standard Windows Python distribution)
- No internet connection required.
