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

    Authentic ligature synthesizer pipeline:
      1. Unicode NFC normalization & decomposed matra fix
      2. Longest-first multi-character ligature substitution (क्ष, त्र, ज्ञ, etc.)
      3. Halant-aware cluster tokenization: Consonant+् → half-character Preeti code
      4. Short-i (ि / 'l') extraction & reordering before consonant cluster
      5. Reph (र् / '{') extraction & placement after following consonant+matra

    Args:
        text: Unicode Devanagari string.

    Returns:
        Preeti-encoded ASCII string.
    """
    if not text:
        return ""

    HALANT = '्'

    # Devanagari consonant set
    CONSONANTS = set('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')

    # Half-character codes (consonant + halant → Preeti shift key)
    HALF_CHAR: Dict[str, str] = {
        'क': 'S', 'ख': 'V', 'ग': 'U', 'घ': '£',
        'च': 'R', 'छ': '5\\', 'ज': 'H', 'झ': '‰', 'ञ': '~',
        'ट': '6\\', 'ठ': '7\\', 'ड': '8\\', 'ढ': '9\\', 'ण': '0',
        'त': 'T', 'थ': 'Y', 'द': 'b\\', 'ध': 'W', 'न': 'G',
        'प': 'K', 'फ': 'ˆ', 'ब': 'A', 'भ': 'E', 'म': 'D',
        'य': 'o\\', 'र': '/\\', 'ल': 'N', 'व': 'J',
        'श': 'Z', 'ष': 'i', 'स': ':', 'ह': 'X',
    }

    # Multi-character ligatures (longest-first greedy matching)
    # (unicode_seq, preeti_output, is_full_form)
    LIGATURES: List[Tuple[str, str, bool]] = [
        ('क्ष्', 'I', False),       # half-ksha
        ('क्ष', 'If', True),        # ksha
        ('त्र', 'q', True),         # tra
        ('त्त', 'Q', True),         # tta
        ('ज्ञ', '1', True),         # gya
        ('श्र', '>', True),         # shra
        ('द्द', '2', True),         # dda
        ('द्ध', '4', True),         # ddha
        ('द्व', 'å', True),         # dva
        ('द्य', 'B', True),         # dya
        ('द्म', 'ß', True),         # dma
        ('द्र', '›', True),         # dra
        ('ध्र', '„', True),         # dhra
        ('ट्ट', '§', True),         # tta
        ('ट्ठ', 'Ý', True),         # ttha
        ('ठ्ठ', '¶', True),         # tthha
        ('ड्ड', '•', True),         # dda
        ('ङ्क', 'Í', True),         # ngka
        ('ङ्ख', 'Î', True),         # ngkha
        ('ङ्ग', 'Ë', True),         # ngga
        ('ङ्ढ', '°', True),         # ngdha
        ('ङ्घ', '‹', True),         # nggha
        ('न्न', 'Ì', True),         # nna
    ]

    # Full-consonant map (with inherent vowel)
    FULL_CONS: Dict[str, str] = {
        'क': 's', 'ख': 'v', 'ग': 'u', 'घ': '3', 'ङ': 'ª',
        'च': 'r', 'छ': '5', 'ज': 'h', 'झ': '´', 'ञ': '`',
        'ट': '6', 'ठ': '7', 'ड': '8', 'ढ': '9', 'ण': '0f',
        'त': 't', 'थ': 'y', 'द': 'b', 'ध': 'w', 'न': 'g',
        'प': 'k', 'फ': 'km', 'ब': 'a', 'भ': 'e', 'म': 'd',
        'य': 'o', 'र': '/', 'ल': 'n', 'व': 'j',
        'श': 'z', 'ष': 'if', 'स': ';', 'ह': 'x',
    }

    # Matra / vowel sign map
    MATRA: Dict[str, str] = {
        'ा': 'f', 'ि': 'l', 'ी': 'L', 'ु': "'", 'ू': '"', 'ृ': '[',
        'े': ']', 'ै': '}',
        'ो': 'f]', 'ौ': 'f}',
        'ं': '+', 'ँ': 'F', 'ः': 'M',
    }

    # Independent vowels
    VOWELS: Dict[str, str] = {
        'अ': 'c', 'आ': 'cf', 'इ': 'O', 'ई': 'O{', 'उ': 'p', 'ऊ': 'pm',
        'ऋ': 'C', 'ए': 'P', 'ऐ': 'P]', 'ओ': 'cf]', 'औ': 'cf}',
    }

    # Special symbols
    SPECIALS: Dict[str, str] = {
        '।': '.', '॥': '..', 'ॐ': 'ç', 'ऽ': '˜',
        '०': ')', '१': '!', '२': '@', '३': '#', '४': '$', '५': '%',
        '६': '^', '७': '&', '८': '*', '९': '(',
        '(': '-', ')': '_', '?': '<', '=': 'Ö', '!': 'Û',
        ':': 'Ù', '/': '÷',
    }

    # ── Helpers ──

    def _try_ligature(text: str, pos: int) -> Optional[Tuple[str, int, bool]]:
        """Try to match a ligature at pos. Returns (preeti, chars_consumed, is_full) or None."""
        for lig_uni, lig_preeti, is_full in LIGATURES:
            lig_len = len(lig_uni)
            if text[pos:pos + lig_len] == lig_uni:
                return (lig_preeti, lig_len, is_full)
        return None

    def _convert_cluster(text: str, start: int) -> Tuple[str, int, bool]:
        """
        Convert a consonant cluster starting at `start`.
        Returns (preeti_cluster_string, new_index, has_short_i).
        The cluster is: (half-consonants)* + final-consonant [+ optional short-i].
        """
        idx_c = start
        parts: List[str] = []
        n_t = len(text)

        while idx_c < n_t and text[idx_c] in CONSONANTS:
            cons_ch = text[idx_c]

            # Try ligature match first
            lig = _try_ligature(text, idx_c)
            if lig:
                lig_preeti, lig_len, lig_full = lig
                parts.append(lig_preeti)
                idx_c += lig_len
                if lig_full:
                    break
                continue

            # Check half-char: consonant + halant (not followed by र for ्र)
            if idx_c + 1 < n_t and text[idx_c + 1] == HALANT:
                if idx_c + 2 < n_t and text[idx_c + 2] == 'र':
                    # Subscript-ra (्र = |)
                    parts.append(FULL_CONS.get(cons_ch, cons_ch))
                    parts.append('|')
                    idx_c += 3
                    continue
                else:
                    parts.append(HALF_CHAR.get(cons_ch, FULL_CONS.get(cons_ch, cons_ch) + '\\'))
                    idx_c += 2
                    continue
            else:
                # Full consonant (cluster end)
                parts.append(FULL_CONS.get(cons_ch, cons_ch))
                idx_c += 1
                break

        # Check short-i after cluster
        has_i = (idx_c < n_t and text[idx_c] == 'ि')
        if has_i:
            idx_c += 1

        return (''.join(parts), idx_c, has_i)

    # ── Main conversion loop ──
    normalized = normalize_unicode(text)
    n = len(normalized)
    result: List[str] = []
    idx = 0

    while idx < n:
        ch = normalized[idx]

        # Skip BOM
        if ch == '\ufeff':
            idx += 1
            continue

        # ── Reph: र + ् at start of cluster (followed by another consonant) ──
        if ch == 'र' and idx + 1 < n and normalized[idx + 1] == HALANT:
            if idx + 2 < n and normalized[idx + 2] in CONSONANTS:
                # Reph: convert the following syllable, then append '{'
                cluster_str, new_idx, has_i = _convert_cluster(normalized, idx + 2)

                # Consume matras after cluster
                matra_parts: List[str] = []
                while new_idx < n and normalized[new_idx] in MATRA:
                    matra_parts.append(MATRA[normalized[new_idx]])
                    new_idx += 1
                matra_str = ''.join(matra_parts)

                if has_i:
                    result.append('l' + cluster_str + matra_str + '{')
                else:
                    result.append(cluster_str + matra_str + '{')
                idx = new_idx
                continue
            else:
                # Word-final र् or र् before non-consonant
                if idx + 2 < n and normalized[idx + 2] == 'ु':
                    result.append('?')  # रु
                    idx += 3
                    continue
                elif idx + 2 < n and normalized[idx + 2] == 'ू':
                    result.append('¿')  # रू
                    idx += 3
                    continue
                else:
                    result.append('/\\')
                    idx += 2
                    continue

        # ── Consonant cluster ──
        if ch in CONSONANTS:
            cluster_str, new_idx, has_i = _convert_cluster(normalized, idx)

            if has_i:
                result.append('l' + cluster_str)
            else:
                result.append(cluster_str)
            idx = new_idx
            continue

        # ── Matra ──
        if ch in MATRA:
            result.append(MATRA[ch])
            idx += 1
            continue

        # ── Independent vowel ──
        if ch in VOWELS:
            result.append(VOWELS[ch])
            idx += 1
            continue

        # ── Special symbols ──
        if ch in SPECIALS:
            result.append(SPECIALS[ch])
            idx += 1
            continue

        # ── Halant fallback ──
        if ch == HALANT:
            result.append('\\')
            idx += 1
            continue

        # ── Pass-through (English, spaces, etc.) ──
        result.append(ch)
        idx += 1

    res = ''.join(result)

    # Post-processing: special ra+vowel composites
    res = res.replace("/'", '?')   # र + u → रु
    res = res.replace('/"', '¿')   # र + uu → रू

    return res


# ═══════════════════════════════════════════════════════════════════════════════
#  ENCODING AUTO-DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

COMMON_ENGLISH_WORDS = {
    'lions', 'international', 'district', 'nepal', 'year', 'report', 'prepared',
    'by', 'lion', 'date', 'zone', 'chairperson', 'region', 'meeting', 'location',
    'city', 'time', 'called', 'to', 'order', 'adjourned', 'next', 'attendance',
    'number', 'of', 'clubs', 'in', 'focus', 'service', 'membership', 'leadership',
    'other', 'recap', 'challenges', 'what', 'were', 'the', 'main', 'shared',
    'specify', 'if', 'pertinent', 'opportunities', 'and', 'solutions', 'discussed',
    'plan', 'action', 'decided', 'upon', 'are', 'any', 'global', 'team',
    'members', 'support', 'teams', 'going', 'assist', 'yes', 'no', 'success',
    'stories', 'practices', 'best', 'can', 'do', 'further', 'officers',
    'key', 'decisions', 'summarize', 'major', 'made', 'during', 'follow', 'up',
    'outline', 'activities', 'planned', 'attachments', 'include', 'relevant',
    'documents', 'such', 'as', 'minutes', 'presentations', 'or', 'sn', 'name',
    'title', 'position', 'signature', 'remarks', 'total', 'page', 'status',
    'for', 'with', 'from', 'an', 'at', 'on', 'is', 'it', 'this', 'that', 'we', 'you',
    'our', 'their', 'club', 'president', 'secretary', 'treasurer'
}


def detect_encoding(text: str) -> str:
    """
    Detect whether a string is Unicode Devanagari or Preeti-encoded.

    Returns:
        "unicode" : contains Devanagari Unicode characters (U+0900..U+097F)
        "preeti"  : ASCII text with high density of Preeti typing symbols
        "unknown" : generic English or digits
    """
    if not text or not text.strip():
        return "unknown"

    # Check Devanagari Unicode codepoints U+0900..U+097F
    if re.search(r'[\u0900-\u097F]', text):
        return "unicode"

    words = re.findall(r'[a-zA-Z]+', text.lower())
    if not words:
        return "unknown"

    # Check if string is predominantly English
    eng_matches = sum(1 for w in words if w in COMMON_ENGLISH_WORDS)
    if eng_matches / len(words) >= 0.25:
        return "unknown"

    # Strong Preeti indicators (symbols that never exist in normal English prose)
    preeti_symbols = set("]}[{|\\~`^")
    if any(c in preeti_symbols for c in text):
        return "preeti"

    # Common Preeti typing n-grams / matras (e.g. short-i before consonant, trailing f/]/}/')
    preeti_patterns = [
        r'l[sfgndtbvwxhkljzc]',   # short-i before consonant
        r'[sfgndtbvwxhkljzc]f',   # aa matra
        r'[sfgndtbvwxhkljzc]\]',  # e matra
        r'[sfgndtbvwxhkljzc]\}',  # ai matra
        r'[sfgndtbvwxhkljzc]\'',  # u matra
        r';b:o',                  # सदस्य
        r'pkl:yt',                # उपस्थित
        r'gfd',                   # नाम
        r'ePsf]',                 # भएको
        r'sf]',                   # को
        r'gsf]',                  # को
    ]
    matches = sum(1 for p in preeti_patterns if re.search(p, text))
    if matches >= 1:
        return "preeti"

    # Weak fallback check: high proportion of typical Preeti characters AND low standard English structure
    preeti_markers = set("sfgndtbvwxhkljzircoepqSFTWDNGKLZICH")
    ascii_letters = [c for c in text if c.isalpha()]
    if len(ascii_letters) >= 4:
        char_matches = sum(1 for c in ascii_letters if c in preeti_markers)
        if char_matches / len(ascii_letters) > 0.8 and eng_matches == 0:
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
    w_ns = XML_NS["w"]

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Extract archive
        with zipfile.ZipFile(input_path, 'r') as zin:
            zin.extractall(tmp_dir)

        # 1. Parse styles.xml to resolve font inheritance
        style_fonts: Dict[str, Set[str]] = {}
        styles_xml_path = os.path.join(tmp_dir, "word", "styles.xml")
        styles_tree = None
        if os.path.exists(styles_xml_path):
            styles_tree = ET.parse(styles_xml_path)
            s_root = styles_tree.getroot()
            for s_elem in s_root.findall(f".//{{{w_ns}}}style"):
                sid = s_elem.attrib.get(f"{{{w_ns}}}styleId")
                rpr = s_elem.find(f"{{{w_ns}}}rPr")
                rfonts = rpr.find(f"{{{w_ns}}}rFonts") if rpr is not None else None
                if rfonts is not None:
                    fonts = {
                        rfonts.attrib.get(f"{{{w_ns}}}ascii", "").lower(),
                        rfonts.attrib.get(f"{{{w_ns}}}hAnsi", "").lower(),
                        rfonts.attrib.get(f"{{{w_ns}}}cs", "").lower()
                    }
                    fonts.discard("")
                    if sid:
                        style_fonts[sid] = fonts

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
                    for r_fonts in root.iter(f"{{{w_ns}}}rFonts"):
                        ascii_f = r_fonts.attrib.get(f"{{{w_ns}}}ascii", "")
                        hAnsi_f = r_fonts.attrib.get(f"{{{w_ns}}}hAnsi", "")
                        cs_f = r_fonts.attrib.get(f"{{{w_ns}}}cs", "")
                        all_f = {ascii_f.lower(), hAnsi_f.lower(), cs_f.lower()}
                        if any(f in legacy_fonts_lower for f in all_f):
                            has_preeti = True
                        if any(f in unicode_fonts_lower for f in all_f):
                            has_unicode = True
                    for t_elem in root.iter(f"{{{w_ns}}}t"):
                        if t_elem.text and re.search(r'[\u0900-\u097F]', t_elem.text):
                            has_unicode = True
                except Exception:
                    pass

            for sid, sfonts in style_fonts.items():
                if any(f in legacy_fonts_lower for f in sfonts):
                    has_preeti = True

            if has_preeti:
                active_direction = "preeti_to_unicode"
            elif has_unicode:
                active_direction = "unicode_to_preeti"
            else:
                active_direction = "preeti_to_unicode"
        else:
            active_direction = direction

        # Second pass: execute selective run-level font and text conversion with chunk merging
        for target_xml in xml_targets:
            tree = ET.parse(target_xml)
            root = tree.getroot()

            for p_elem in root.iter(f"{{{w_ns}}}p"):
                # Determine paragraph's style and inherited font
                p_pr = p_elem.find(f"{{{w_ns}}}pPr")
                p_style_elem = p_pr.find(f"{{{w_ns}}}pStyle") if p_pr is not None else None
                p_style = p_style_elem.attrib.get(f"{{{w_ns}}}val") if p_style_elem is not None else None
                p_fonts = style_fonts.get(p_style, set())

                runs = p_elem.findall(f"{{{w_ns}}}r")
                if not runs:
                    continue

                runs_total += len(runs)
                run_info = []

                for r in runs:
                    t_elem = r.find(f"{{{w_ns}}}t")
                    text = t_elem.text if (t_elem is not None and t_elem.text) else ""

                    r_pr = r.find(f"{{{w_ns}}}rPr")
                    r_fonts = r_pr.find(f"{{{w_ns}}}rFonts") if r_pr is not None else None
                    if r_fonts is not None:
                        ascii_f = r_fonts.attrib.get(f"{{{w_ns}}}ascii", "")
                        hAnsi_f = r_fonts.attrib.get(f"{{{w_ns}}}hAnsi", "")
                        cs_f = r_fonts.attrib.get(f"{{{w_ns}}}cs", "")
                        if ascii_f:
                            fonts_detected.add(ascii_f)
                        if cs_f:
                            fonts_detected.add(cs_f)
                        rf_set = {ascii_f.lower(), hAnsi_f.lower(), cs_f.lower()}
                        rf_set.discard("")
                    else:
                        rf_set = set()

                    eff_fonts = rf_set if rf_set else p_fonts

                    is_target_script = False
                    if active_direction == "preeti_to_unicode":
                        if any(f in legacy_fonts_lower for f in eff_fonts):
                            is_target_script = True
                        if re.search(r'[\u0900-\u097F]', text):
                            is_target_script = False

                    elif active_direction == "unicode_to_preeti":
                        if any(f in unicode_fonts_lower for f in eff_fonts) or re.search(r'[\u0900-\u097F]', text):
                            is_target_script = True

                    run_info.append({
                        'elem': r,
                        'text': text,
                        'is_target': is_target_script,
                        'eff_fonts': eff_fonts,
                        't_elem': t_elem,
                        'r_pr': r_pr,
                    })

                # In preeti_to_unicode: evaluate contiguous spans without explicit fonts
                if active_direction == "preeti_to_unicode":
                    span_idx = 0
                    while span_idx < len(run_info):
                        if run_info[span_idx]['is_target'] or not run_info[span_idx]['text']:
                            span_idx += 1
                            continue

                        # Skip runs with explicit non-legacy fonts (e.g. Cambria, Arial)
                        if run_info[span_idx]['eff_fonts']:
                            span_idx += 1
                            continue

                        span_start = span_idx
                        while (span_idx < len(run_info) and
                               not run_info[span_idx]['is_target'] and
                               not run_info[span_idx]['eff_fonts'] and
                               not re.search(r'[\u0900-\u097F]', run_info[span_idx]['text'])):
                            span_idx += 1
                        span_end = span_idx

                        span_text = "".join(run_info[k]['text'] for k in range(span_start, span_end))
                        if detect_encoding(span_text) == "preeti":
                            for k in range(span_start, span_end):
                                run_info[k]['is_target'] = True

                # Group contiguous target runs and convert as coherent chunks
                idx = 0
                while idx < len(run_info):
                    if not run_info[idx]['is_target']:
                        idx += 1
                        continue

                    start = idx
                    while idx < len(run_info) and run_info[idx]['is_target']:
                        idx += 1
                    end = idx

                    chunk = run_info[start:end]
                    combined_text = "".join(item['text'] for item in chunk)
                    if not combined_text.strip():
                        continue

                    if active_direction == "preeti_to_unicode":
                        converted = preeti_to_unicode(combined_text)
                        target_font = target_unicode_font
                    else:
                        converted = unicode_to_preeti(combined_text)
                        target_font = target_preeti_font

                    # Place converted text in the first run of the chunk
                    first_run = chunk[0]['elem']
                    first_t = chunk[0]['t_elem']
                    if first_t is None:
                        first_t = ET.SubElement(first_run, f"{{{w_ns}}}t")
                    first_t.text = converted
                    if converted.startswith(" ") or converted.endswith(" "):
                        first_t.attrib["{http://www.w3.org/XML/1998/namespace}space"] = "preserve"

                    # Update font properties of first run
                    r_pr = chunk[0]['r_pr']
                    if r_pr is None:
                        r_pr = ET.SubElement(first_run, f"{{{w_ns}}}rPr")
                    r_fonts = r_pr.find(f"{{{w_ns}}}rFonts")
                    if r_fonts is None:
                        r_fonts = ET.SubElement(r_pr, f"{{{w_ns}}}rFonts")
                    r_fonts.attrib[f"{{{w_ns}}}ascii"] = target_font
                    r_fonts.attrib[f"{{{w_ns}}}hAnsi"] = target_font
                    r_fonts.attrib[f"{{{w_ns}}}cs"] = target_font

                    # Cleanly remove subsequent runs in chunk from paragraph
                    for item in chunk[1:]:
                        if item['elem'] in p_elem:
                            p_elem.remove(item['elem'])

                    runs_converted += 1

            # Write modified XML back
            tree.write(target_xml, encoding="utf-8", xml_declaration=True)

        # 3. Update legacy styles in styles.xml if needed
        if styles_tree is not None and os.path.exists(styles_xml_path):
            s_root = styles_tree.getroot()
            styles_modified = False
            for s_elem in s_root.findall(f".//{{{w_ns}}}style"):
                rpr = s_elem.find(f"{{{w_ns}}}rPr")
                rfonts = rpr.find(f"{{{w_ns}}}rFonts") if rpr is not None else None
                if rfonts is not None:
                    ascii_f = rfonts.attrib.get(f"{{{w_ns}}}ascii", "").lower()
                    if active_direction == "preeti_to_unicode" and ascii_f in legacy_fonts_lower:
                        rfonts.attrib[f"{{{w_ns}}}ascii"] = target_unicode_font
                        rfonts.attrib[f"{{{w_ns}}}hAnsi"] = target_unicode_font
                        rfonts.attrib[f"{{{w_ns}}}cs"] = target_unicode_font
                        styles_modified = True
                    elif active_direction == "unicode_to_preeti" and ascii_f in unicode_fonts_lower:
                        rfonts.attrib[f"{{{w_ns}}}ascii"] = target_preeti_font
                        rfonts.attrib[f"{{{w_ns}}}hAnsi"] = target_preeti_font
                        rfonts.attrib[f"{{{w_ns}}}cs"] = target_preeti_font
                        styles_modified = True
            if styles_modified:
                styles_tree.write(styles_xml_path, encoding="utf-8", xml_declaration=True)

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
