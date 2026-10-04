"""
Preeti ↔ Unicode Nepali Font Converter Engine
=============================================
Bidirectional conversion between legacy Nepali font encodings (Preeti, Kantipur,
PCS Nepali, Sagarmatha) and standard Unicode Devanagari (Nirmala UI, Mangal, Kalimati).

Handles:
  • Character-level mapping & complex ligature composition
  • Matra reordering (short-i / hraswa matra placed before consonants in Preeti)
  • Reph ({ / र्) placement before/after consonant clusters
  • Compound vowels (आ, ओ, औ, ऐ) and special conjuncts (क्ष, त्र, ज्ञ, श्र, द्ध, द्व, etc.)
  • Direct .docx Word document processing preserving tables, styles, English text, and formatting

Author: Aaradhya Dev Tamrakar
"""

import os
import re
import sys
import json
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from io import StringIO
from typing import Optional, Union, Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
#  AUTHORITATIVE PREETI CHARACTER MAP & REORDERING RULES
# ═══════════════════════════════════════════════════════════════════════════════

PREETI_CHAR_MAP: Dict[str, str] = {
    "÷": "/", "v": "ख", "r": "च", "\"": "ू", "~": "ञ्", "z": "श", "ç": "ॐ",
    "f": "ा", "b": "द", "n": "ल", "j": "व", "×": "×", "V": "ख्", "R": "च्",
    "ß": "द्म", "^": "६", "Û": "!", "Z": "श्", "F": "ँ", "B": "द्य", "N": "ल्",
    "Ë": "ङ्ग", "J": "व्", "6": "ट", "2": "द्द", "¿": "रू", ">": "श्र", ":": "स्",
    "§": "ट्ट", "&": "७", "£": "घ्", "•": "ड्ड", ".": "।", "«": "्र", "*": "८",
    "„": "ध्र", "w": "ध", "s": "क", "g": "न", "æ": "“", "c": "अ", "o": "य",
    "k": "प", "W": "ध्", "Ö": "=", "S": "क्", "Ò": "¨", "_": ")", "[": "ृ",
    "Ú": "’", "G": "न्", "ˆ": "फ्", "C": "ऋ", "O": "इ", "Î": "ङ्ख", "K": "प्",
    "7": "ठ", "¶": "ठ्ठ", "3": "घ", "9": "ढ", "?": "रु", ";": "स", "'": "ु",
    "#": "३", "¢": "द्घ", "/": "र", "+": "ं", "ª": "ङ", "t": "त", "p": "उ",
    "|": "्र", "x": "ह", "å": "द्व", "d": "म", "`": "ञ", "l": "ि", "h": "ज",
    "T": "त्", "P": "ए", "Ý": "ट्ठ", "\\": "्", "Ù": ";", "X": "ह्", "Å": "हृ",
    "D": "म्", "@": "२", "Í": "ङ्क", "L": "ी", "H": "ज्", "4": "द्ध", "±": "+",
    "0": "ण्", "<": "?", "8": "ड", "¥": "र्‍", "$": "४", "¡": "ज्ञ्", ",": ",",
    "©": "र", "(": "९", "‘": "ॅ", "u": "ग", "q": "त्र", "}": "ै", "y": "थ",
    "e": "भ", "a": "ब", "i": "ष्", "‰": "झ्", "U": "ग्", "Q": "त्त", "]": "े",
    "˜": "ऽ", "Y": "थ्", "Ø": "्य", "E": "भ्", "A": "ब्", "M": "ः", "Ì": "न्न",
    "I": "क्ष्", "5": "छ", "´": "झ", "1": "ज्ञ", "°": "ङ्ढ", "=": ".", "Æ": "”",
    "‹": "ङ्घ", "%": "५", "¤": "झ्", "!": "१", "-": "(", "›": "द्र", ")": "०",
    "…": "‘", "Ü": "%"
}

# Regex post-rules for Preeti -> Unicode reordering
# Note: $1, $2 in JS regex replaced with Python \g<1>, \g<2>
PREETI_POST_RULES: List[Tuple[str, str]] = [
    (r"्ा", ""),
    (r"(त्र|त्त)([^उभप]+?)m", r"\g<1>m\g<2>"),
    (r"त्रm", "क्र"),
    (r"त्तm", "क्त"),
    (r"([^उभप]+?)m", r"m\g<1>"),
    (r"उm", "ऊ"),
    (r"भm", "झ"),
    (r"पm", "फ"),
    (r"इ{", "ई"),
    (r"ि((.्)*[^्])", r"\g<1>ि"),
    (r"(.[ािीुूृेैोौंःँ]*?){", r"{\g<1>"),
    (r"((.्)*){", r"{\g<1>"),
    (r"{", "र्"),
    (r"([ाीुूृेैोौंःँ]+?)(्(.्)*[^्])", r"\g<2>\g<1>"),
    (r"्([ाीुूृेैोौंःँ]+?)((.्)*[^्])", r"्\g<2>\g<1>"),
    (r"([ंँ])([ािीुूृेैोौः]*)", r"\g<2>\g<1>"),
    (r"ँँ", "ँ"),
    (r"ंं", "ं"),
    (r"ेे", "े"),
    (r"ैै", "ै"),
    (r"ुु", "ु"),
    (r"ूू", "ू"),
    (r"^ः", ":"),
    (r"टृ", "ट्ट"),
    (r"ेा", "ाे"),
    (r"ैा", "ाै"),
    (r"अाे", "ओ"),
    (r"अाै", "औ"),
    (r"अा", "आ"),
    (r"एे", "ऐ"),
    (r"ाे", "ो"),
    (r"ाै", "ौ"),
]

# Additional common office font mappings (Kantipur, PCS Nepali)
KANTIPUR_CHAR_MAP: Dict[str, str] = {
    "÷": "/", "v": "ख", "r": "च", "\"": "ू", "~": "ञ्", "z": "श", "ç": "ॐ",
    "f": "ा", "b": "द", "n": "ल", "j": "व", "V": "ख्", "R": "च्", "ß": "द्म",
    "^": "६", "Z": "श्", "F": "ा", "B": "द्य", "Ï": "फ्", "N": "ल्", "Ë": "ङ्ग",
    "J": "व्", "6": "ट", "2": "द्द", "¿": "रू", ">": "श्र", ":": "स्", "§": "ट्ट",
    "&": "७", "£": "घ्", "•": "ड्ड", "¯": "¯", ".": "।", "«": "्र", "*": "८",
    "„": "ध्र", "w": "ध", "s": "क", "g": "न", "æ": "“", "c": "अ", "o": "य",
    "k": "प", "W": "ध्", "S": "क्", "Ò": "¨", "_": ")", "[": "ृ", "Ú": "’",
    "G": "न्", "Æ": "”", "C": "ऋ", "Â": "र", "O": "इ", "Î": "फ्", "K": "प्",
    "7": "ठ", "¶": "ठ्ठ", "3": "घ", "9": "ढ", "?": "रु", ";": "स", "º": "फ्",
    "'": "ु", "#": "३", "¢": "द्घ", "/": "र", "®": "र", "+": "ं", "ª": "ङ",
    "t": "त", "p": "उ", "|": "्र", "x": "ह", "å": "द्व", "d": "म", "`": "ञ",
    "l": "ि", "h": "ज", "T": "त्", "P": "ए", "Œ": "त्त्", "\\": "्", "X": "हृ",
    "D": "म्", "@": "२", "Í": "ङ्क", "L": "ी", "H": "ज्", "µ": "र", "4": "द्ध",
    "±": "+", "0": "ण्", "<": "?", "8": "ड", "¥": "र्‍", "$": "४", "¡": "ज्ञ्",
    "†": "!", "™": "र", "­": "(", ",": ",", "©": "र", "(": "९", "“": "ँ",
    "‘": "ॅ", "u": "ग", "q": "त्र", "}": "ै", "y": "थ", "ø": "य्", "e": "भ",
    "a": "ब", "i": "ष्", "‰": "झ्", "U": "ग्", "Ô": "क्ष", "Q": "त्त", "œ": "त्र्",
    "]": "े", "˜": "ऽ", "Y": "थ्", "Ø": "्य", "E": "भ्", "A": "ब्", "M": "ः",
    "Ì": "न्न", "I": "क्ष्", "È": "ष", "5": "छ", "´": "झ", "1": "ज्ञ", "°": "ङ्ढ",
    "=": ".", "‹": "ङ्ग", "%": "५", "¤": "झ्", "!": "१", "-": "(", "¬": "…",
    "›": "ऽ", ")": "०", "¨": "ङ्ग", "…": "‘"
}

# ═══════════════════════════════════════════════════════════════════════════════
#  UNICODE → PREETI CONVERSION DICTIONARY & NORMALIZER
# ═══════════════════════════════════════════════════════════════════════════════

UNICODE_TO_PREETI_MAP: Dict[str, str] = {
    'क': 's', 'ख': 'v', 'ग': 'u', 'घ': '3', 'ङ': 'ª',
    'च': 'r', 'छ': '5', 'ज': 'h', 'झ': '´', 'ञ': '`',
    'ट': '6', 'ठ': '7', 'ड': '8', 'ढ': '9', 'ण': '0f',
    'त': 't', 'थ': 'y', 'द': 'b', 'ध': 'w', 'न': 'g',
    'प': 'k', 'फ': 'km', 'ब': 'a', 'भ': 'e', 'म': 'd',
    'य': 'o', 'र': '/', 'ल': 'n', 'व': 'j',
    'श': 'z', 'ष': 'if', 'स': ';', 'ह': 'x',
    'ा': 'f', 'ि': 'l', 'ी': 'L', 'ु': "'", 'ू': '"', 'ृ': '[',
    'े': ']', 'ै': '}',
    '्': '\\', '्र': '|',
    'ं': '+', 'ँ': 'F', 'ः': 'M', '।': '.', '॥': '..',
    '०': ')', '१': '!', '२': '@', '३': '#', '४': '$', '५': '%',
    '६': '^', '७': '&', '८': '*', '९': '(',
    'अ': 'c', 'आ': 'cf', 'इ': 'O', 'ई': 'O{', 'उ': 'p', 'ऊ': 'pm',
    'ऋ': 'C', 'ए': 'P', 'ऐ': 'P]', 'ओ': 'cf]', 'औ': 'cf}',
    'क्': 'S', 'ख्': 'V', 'ग्': 'U', 'घ्': '£',
    'च्': 'R', 'छ्': '5\\', 'ज्': 'H', 'झ्': '‰', 'ञ्': '~',
    'ट्': '6\\', 'ठ्': '7\\', 'ड्': '8\\', 'ढ्': '9\\', 'ण्': '0',
    'त्': 'T', 'थ्': 'Y', 'द्': 'b\\', 'ध्': 'W', 'न्': 'G',
    'प्': 'K', 'फ्': 'ˆ', 'ब्': 'A', 'भ्': 'E', 'म्': 'D',
    'य्': 'Y', 'ल्': 'N', 'व्': 'J',
    'श्': 'Z', 'ष्': 'i', 'स्': ':', 'ह्': 'X',
    'क्ष': 'If', 'क्ष्': 'I',
    'त्र': 'q', 'त्त': 'Q', 'ज्ञ': '1', 'श्र': '>',
    'द्द': '2', 'द्ध': '4', 'द्व': 'å', 'द्य': 'B', 'द्म': 'ß',
    'ट्ट': '§', 'ठ्ठ': '¶', 'ड्ड': '•', 'ङ्क': 'Í', 'ङ्ख': 'Î', 'ङ्ग': 'Ë',
    'ॐ': 'ç', 'रू': '¿', 'रु': '?', 'द्र': '›', 'ध्र': '„',
    '(': '-', ')': '_', '?': '<', '=': 'Ö', '!': 'Û',
    ':': 'Ù', '/': '÷',
}


def normalize_unicode(text: str) -> str:
    """Normalize Devanagari Unicode sequences before mapping."""
    if not text:
        return ""
    # Normalize decomposed conjuncts into standard forms
    text = text.replace('क' + '्' + 'ष', 'क्ष')
    text = text.replace('त' + '्' + 'र', 'त्र')
    text = text.replace('ज' + '्' + 'ञ', 'ज्ञ')
    text = text.replace('श' + '्' + 'र', 'श्र')
    # Normalize double vowel matras
    text = text.replace('ो', 'ाे')
    text = text.replace('ौ', 'ाै')
    return text


def preeti_to_unicode(text: str, font: str = "Preeti") -> str:
    """
    Convert Preeti (or Kantipur) encoded text to Unicode Devanagari.

    Args:
        text: Preeti-encoded string.
        font: Source font name ("Preeti", "Kantipur", "PCS Nepali").

    Returns:
        Unicode Devanagari text compatible with Nirmala UI, Mangal, Kalimati.
    """
    if not text:
        return ""

    font_lower = font.lower().replace(" ", "").replace("_", "")
    char_map = PREETI_CHAR_MAP
    if "kantipur" in font_lower:
        char_map = KANTIPUR_CHAR_MAP

    # Step 1: Character mapping
    chars = [char_map.get(c, c) for c in text]
    mapped = "".join(chars)

    # Step 2: Post-processing reordering rules
    result = mapped
    for pattern, replacement in PREETI_POST_RULES:
        result = re.sub(pattern, replacement, result)

    return result


def unicode_to_preeti(text: str) -> str:
    """
    Convert Unicode Devanagari text (e.g. from Nirmala UI) to Preeti encoding.

    Accurately handles:
      - Short-i matra (ि) reordered to precede the consonant/cluster ('l' + consonant)
      - Complex conjunct clusters (स्ति, त्ति, ष्ट्रिय, etc.)
      - Reph (र्) placed after following consonant/vowel mark with '{'
      - Ligatures and half-characters (क्ष, त्र, ज्ञ, श्र, द्व, द्ध, etc.)

    Args:
        text: Unicode Devanagari string.

    Returns:
        Preeti-encoded ASCII string.
    """
    if not text:
        return ""

    normalized = normalize_unicode(text)
    converted: List[str] = []
    idx = -1
    n = len(normalized)

    half_char_keys = set('WERTYUXASDGHJK:ZVNIi')

    while idx + 1 < n:
        idx += 1
        ch = normalized[idx]
        if ch == '\ufeff':
            continue

        try:
            # Check 1: Normal hraswa ikar (क + ि -> l + s)
            if idx + 1 < n and normalized[idx + 1] == 'ि':
                if ch == 'q':  # त्र
                    converted.append('l' + ch)
                else:
                    mapped_ch = UNICODE_TO_PREETI_MAP.get(ch, ch)
                    converted.append('l' + mapped_ch)
                idx += 1
                continue

            # Check 2: Two-character cluster + ikar (e.g. स्ति, त्ति)
            if idx + 2 < n and normalized[idx + 2] == 'ि':
                mapped_ch = UNICODE_TO_PREETI_MAP.get(ch, ch)
                if mapped_ch in half_char_keys:
                    next_ch = normalized[idx + 1]
                    if next_ch != 'q':
                        converted.append('l' + mapped_ch + UNICODE_TO_PREETI_MAP.get(next_ch, next_ch))
                        idx += 2
                        continue
                    else:
                        converted.append('l' + mapped_ch + next_ch)
                        idx += 2
                        continue

            # Check 3: Reph (र + ् + consonant) e.g. कर्म, वार्ता
            if idx + 1 < n and ch == 'र' and normalized[idx + 1] == '्':
                if idx + 3 < n and normalized[idx + 3] in ('ा', 'ो', 'ौ', 'े', 'ै', 'ी', 'ाे', 'ाै'):
                    cons = UNICODE_TO_PREETI_MAP.get(normalized[idx + 2], normalized[idx + 2])
                    matra = UNICODE_TO_PREETI_MAP.get(normalized[idx + 3], normalized[idx + 3])
                    converted.append(cons + matra + '{')
                    idx += 3
                    continue
                elif idx + 3 < n and normalized[idx + 3] == 'ि':
                    matra = UNICODE_TO_PREETI_MAP.get(normalized[idx + 3], normalized[idx + 3])
                    cons = UNICODE_TO_PREETI_MAP.get(normalized[idx + 2], normalized[idx + 2])
                    converted.append(matra + cons + '{')
                    idx += 3
                    continue
                elif idx + 2 < n:
                    cons = UNICODE_TO_PREETI_MAP.get(normalized[idx + 2], normalized[idx + 2])
                    converted.append(cons + '{')
                    idx += 2
                    continue

            # Check 4: Three-character cluster + ikar (e.g. ष्ट्रिय)
            if idx + 3 < n and normalized[idx + 3] == 'ि':
                cluster_join = normalized[idx + 2]
                if cluster_join in ('|', '«'):
                    mapped_ch = UNICODE_TO_PREETI_MAP.get(ch, ch)
                    if mapped_ch in half_char_keys:
                        converted.append('l' + mapped_ch + UNICODE_TO_PREETI_MAP.get(normalized[idx + 1], normalized[idx + 1]) + cluster_join)
                        idx += 3
                        continue

        except IndexError:
            pass

        # Standard mapping
        converted.append(UNICODE_TO_PREETI_MAP.get(ch, ch))

    res = "".join(converted)

    # Post-mapping fixes for Preeti ligatures & composites
    res = res.replace('Si', 'I')       # half-ka + half-ssa -> half-ksha
    res = res.replace('H`', '1')       # half-ja + nya -> jnya (ज्ञ)
    res = res.replace('b\\w', '4')     # da + halant + dha -> ddha (द्ध)
    res = res.replace('z|', '>')       # sha + ra -> shra (श्र)
    res = res.replace("/'", '?')       # ra + u -> ru (रु)
    res = res.replace('/"', '¿')       # ra + uu -> ruu (रू)
    res = res.replace('Tt', 'Q')       # half-ta + ta -> tta (त्त)
    res = res.replace('b\\lj', 'lå')   # da + halant + i-matra + va -> dvi (द्वि)
    res = res.replace('b\\j', 'å')     # da + halant + va -> dva (द्व)
    res = res.replace('0f\\', '0')     # nna + aa-matra + halant -> half-nna
    res = res.replace('`\\', '~')      # nya + halant -> half-nya

    return res


# ═══════════════════════════════════════════════════════════════════════════════
#  ENCODING AUTO-DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def detect_encoding(text: str) -> str:
    """
    Detect whether a string is Unicode Devanagari or Preeti-encoded.

    Returns:
        "unicode" : contains Devanagari Unicode characters (U+0900..U+097F)
        "preeti"  : ASCII text with high density of Preeti typing symbols
        "unknown" : generic English or digits
    """
    if not text:
        return "unknown"

    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    if has_devanagari:
        return "unicode"

    # Preeti signatures: sequence of letters commonly occurring in Nepali typing
    preeti_markers = set("sfgndtbvwxhkljzircoepqSFTWDNGKLZICH[]{}|;")
    ascii_letters = [c for c in text if c.isalpha() or c in "[]{}|;~`^&*()_+="]
    if len(ascii_letters) > 0:
        matches = sum(1 for c in ascii_letters if c in preeti_markers)
        if matches / len(ascii_letters) > 0.6:
            return "preeti"

    return "unknown"


# ═══════════════════════════════════════════════════════════════════════════════
#  WORD DOCUMENT (.DOCX) CONVERTER ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

SUPPORTED_LEGACY_FONTS = [
    "Preeti", "Kantipur", "PCS NEPALI", "PCS Nepali", "Sagarmatha",
    "FONTASY_HIMALI_TT", "Himashikhar", "Fontasy Himali"
]

KNOWN_UNICODE_FONTS = [
    "Nirmala UI", "Nirmala UI Semilight", "Mangal", "Kalimati",
    "Noto Sans Devanagari", "Aparajita", "Utsaah", "Kokila",
    "Shree Devanagari 714", "Sanskrit Text"
]

XML_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def convert_docx(
    input_path: str,
    output_path: str,
    direction: str = "auto",
    target_unicode_font: str = "Nirmala UI",
    target_preeti_font: str = "Preeti",
) -> Dict[str, Union[int, List[str]]]:
    """
    Convert a .docx Word document between Preeti and Unicode Devanagari.

    Selectively processes only the runs matching the source font/script,
    leaving English headings, tables, numbering, bullet points, colors,
    and styles 100% intact!

    Args:
        input_path: Path to input .docx file.
        output_path: Path to save the converted .docx file.
        direction: "preeti_to_unicode", "unicode_to_preeti", or "auto".
        target_unicode_font: Font to set when converting to Unicode (default "Nirmala UI").
        target_preeti_font: Font to set when converting to Preeti (default "Preeti").

    Returns:
        Dict with conversion statistics.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Register all XML namespaces to prevent ns0 prefixes
    for prefix, uri in [
        ("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main"),
        ("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships"),
        ("m", "http://schemas.openxmlformats.org/officeDocument/2006/math"),
        ("v", "urn:schemas-microsoft-com:vml"),
        ("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"),
        ("w10", "urn:schemas-microsoft-com:office:word"),
        ("w14", "http://schemas.microsoft.com/office/word/2010/wordml"),
        ("w15", "http://schemas.microsoft.com/office/word/2012/wordml"),
    ]:
        ET.register_namespace(prefix, uri)

    legacy_fonts_lower = {f.lower() for f in SUPPORTED_LEGACY_FONTS}
    unicode_fonts_lower = {f.lower() for f in KNOWN_UNICODE_FONTS}

    runs_converted = 0
    runs_total = 0
    fonts_detected = set()

    # Read and modify word/document.xml inside docx zip package
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Extract archive
        with zipfile.ZipFile(input_path, 'r') as zin:
            zin.extractall(tmp_dir)

        # Candidate XML files containing user text: document.xml, headers, footers
        xml_targets = []
        word_dir = os.path.join(tmp_dir, "word")
        if os.path.exists(word_dir):
            for fname in os.listdir(word_dir):
                if fname == "document.xml" or fname.startswith("header") or fname.startswith("footer"):
                    if fname.endswith(".xml"):
                        xml_targets.append(os.path.join(word_dir, fname))

        # First pass: detect direction if auto
        if direction == "auto":
            has_preeti = False
            has_unicode = False
            for target_xml in xml_targets:
                try:
                    tree = ET.parse(target_xml)
                    root = tree.getroot()
                    for r_fonts in root.iter(f"{{{XML_NS['w']}}}rFonts"):
                        ascii_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}ascii", "")
                        hAnsi_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}hAnsi", "")
                        cs_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}cs", "")
                        all_f = {ascii_f.lower(), hAnsi_f.lower(), cs_f.lower()}
                        if any(f in legacy_fonts_lower for f in all_f):
                            has_preeti = True
                        if any(f in unicode_fonts_lower for f in all_f):
                            has_unicode = True
                    # Also check actual text content for Devanagari codepoints
                    for t_elem in root.iter(f"{{{XML_NS['w']}}}t"):
                        if t_elem.text and re.search(r'[\u0900-\u097F]', t_elem.text):
                            has_unicode = True
                except Exception:
                    pass

            if has_preeti:
                active_direction = "preeti_to_unicode"
            elif has_unicode:
                active_direction = "unicode_to_preeti"
            else:
                active_direction = "preeti_to_unicode"
        else:
            active_direction = direction

        # Second pass: execute selective run-level font and text conversion
        for target_xml in xml_targets:
            tree = ET.parse(target_xml)
            root = tree.getroot()

            for r_elem in root.iter(f"{{{XML_NS['w']}}}r"):
                runs_total += 1
                r_pr = r_elem.find(f"{{{XML_NS['w']}}}rPr")
                t_elem = r_elem.find(f"{{{XML_NS['w']}}}t")

                if t_elem is None or not t_elem.text:
                    continue

                original_text = t_elem.text

                # Inspect fonts in run properties
                r_fonts = r_pr.find(f"{{{XML_NS['w']}}}rFonts") if r_pr is not None else None
                ascii_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}ascii", "") if r_fonts is not None else ""
                hAnsi_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}hAnsi", "") if r_fonts is not None else ""
                cs_f = r_fonts.attrib.get(f"{{{XML_NS['w']}}}cs", "") if r_fonts is not None else ""

                if ascii_f:
                    fonts_detected.add(ascii_f)
                if cs_f:
                    fonts_detected.add(cs_f)

                run_fonts = {ascii_f.lower(), hAnsi_f.lower(), cs_f.lower()}

                if active_direction == "preeti_to_unicode":
                    is_legacy_run = any(f in legacy_fonts_lower for f in run_fonts)
                    if is_legacy_run:
                        # Determine source font name
                        src_font = ascii_f or hAnsi_f or "Preeti"
                        converted = preeti_to_unicode(original_text, font=src_font)
                        t_elem.text = converted

                        # Update run fonts to Target Unicode font (Nirmala UI)
                        if r_pr is None:
                            r_pr = ET.SubElement(r_elem, f"{{{XML_NS['w']}}}rPr")
                        if r_fonts is None:
                            r_fonts = ET.SubElement(r_pr, f"{{{XML_NS['w']}}}rFonts")

                        r_fonts.attrib[f"{{{XML_NS['w']}}}ascii"] = target_unicode_font
                        r_fonts.attrib[f"{{{XML_NS['w']}}}hAnsi"] = target_unicode_font
                        r_fonts.attrib[f"{{{XML_NS['w']}}}cs"] = target_unicode_font
                        runs_converted += 1

                elif active_direction == "unicode_to_preeti":
                    # Check if run uses known Unicode font OR contains Devanagari characters
                    is_unicode_run = (
                        any(f in unicode_fonts_lower for f in run_fonts) or
                        bool(re.search(r'[\u0900-\u097F]', original_text))
                    )
                    if is_unicode_run:
                        converted = unicode_to_preeti(original_text)
                        t_elem.text = converted

                        # Update run fonts to Target Preeti font
                        if r_pr is None:
                            r_pr = ET.SubElement(r_elem, f"{{{XML_NS['w']}}}rPr")
                        if r_fonts is None:
                            r_fonts = ET.SubElement(r_pr, f"{{{XML_NS['w']}}}rFonts")

                        r_fonts.attrib[f"{{{XML_NS['w']}}}ascii"] = target_preeti_font
                        r_fonts.attrib[f"{{{XML_NS['w']}}}hAnsi"] = target_preeti_font
                        r_fonts.attrib[f"{{{XML_NS['w']}}}cs"] = target_preeti_font
                        runs_converted += 1

            # Write modified XML back to tmp directory
            tree.write(target_xml, encoding="utf-8", xml_declaration=True)

        # Repackage docx zip
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for foldername, subfolders, filenames in os.walk(tmp_dir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, tmp_dir)
                    zout.write(filepath, arcname)

    return {
        "runs_converted": runs_converted,
        "runs_total": runs_total,
        "direction": active_direction,
        "fonts_detected": sorted(list(fonts_detected)),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Preeti ↔ Unicode Converter CLI")
        print("Usage:")
        print("  python converter_engine.py <text>                     # Auto-detect & convert")
        print("  python converter_engine.py --p2u <text>               # Preeti → Unicode")
        print("  python converter_engine.py --u2p <text>               # Unicode → Preeti")
        print("  python converter_engine.py --docx in.docx out.docx    # Convert Word document")
        sys.exit(0)

    arg1 = sys.argv[1]

    if arg1 == "--p2u":
        text = " ".join(sys.argv[2:])
        print(preeti_to_unicode(text))
    elif arg1 == "--u2p":
        text = " ".join(sys.argv[2:])
        print(unicode_to_preeti(text))
    elif arg1 == "--docx":
        if len(sys.argv) < 4:
            print("Usage: python converter_engine.py --docx <in.docx> <out.docx> [--dir p2u|u2p|auto]")
            sys.exit(1)
        in_file = sys.argv[2]
        out_file = sys.argv[3]
        direction = "auto"
        if "--dir" in sys.argv:
            d_idx = sys.argv.index("--dir")
            direction = sys.argv[d_idx + 1]
            if direction == "p2u":
                direction = "preeti_to_unicode"
            elif direction == "u2p":
                direction = "unicode_to_preeti"
        stats = convert_docx(in_file, out_file, direction=direction)
        print(f"Converted {stats['runs_converted']}/{stats['runs_total']} runs ({stats['direction']})")
        print(f"Detected fonts: {stats['fonts_detected']}")
    else:
        text = " ".join(sys.argv[1:])
        enc = detect_encoding(text)
        if enc == "unicode":
            print(f"[Auto: Unicode → Preeti]")
            print(unicode_to_preeti(text))
        else:
            print(f"[Auto: Preeti → Unicode]")
            print(preeti_to_unicode(text))
