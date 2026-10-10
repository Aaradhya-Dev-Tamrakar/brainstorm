---
description: "Windows Digital Forensics & Incident Response (DFIR) triage and stealth evasion hunting engine (F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics). Use whenever asked to scan directories for hidden/masqueraded files, detect NTFS Alternate Data Streams (ADS), unmask CLSID/Unicode RLO exploits, verify executable PE headers, harvest Windows Prefetch execution artifacts, or maintain cryptographic chain-of-custody evidence ledgers."
---

# Cyber-Forensics — Windows DFIR & Stealth Evasion Hunting Engine

This skill guides agents in utilizing **Cyber-Forensics** (`F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics`), Aaradhya's lightweight, deterministic Windows forensic triage and evasion detection engine.

---

## 1. Core Architecture & Location

* **Project Root:** `F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics`
* **Repository:** `https://github.com/Aaradhya-Dev-Tamrakar/Cyber-Forensics`
* **Core Modules:**
  * `src/EvasionHunter.ps1`: Multi-layer stealth evasion detection (ADS, CLSID, RLO, MZ PE magic-byte masquerading).
  * `src/ArtifactHarvester.ps1`: Windows Prefetch (`.pf`) timeline extraction, execution frequency, and cryptographic metadata stamping.
  * `tests/test_evasion_hunter.ps1`: Synthetic evasion specimen regression suite.

---

## 2. Evasion Detection Primitives

The Evasion Hunter uncovers 6 distinct stealth mechanisms:

| Evasion Class | Technique | Detection Method | Threat Level |
| :--- | :--- | :--- | :--- |
| **`SUPER_HIDDEN`** | `Hidden` + `System` flags (`attrib +h +s`) | Bitmask check on `[IO.FileAttributes]::Hidden` & `System` | `MEDIUM` |
| **`NTFS_ADS`** | Data attached to secondary streams (`file.txt:evil.exe`) | `Get-Item -Stream *` filtering out `:$DATA` & `Zone.Identifier` | `HIGH` |
| **`CLSID_SPOOF`** | Appending Windows shell GUIDs (`folder.{GUID}`) | Regex matching `\{[0-9a-fA-F-]{36}\}` | `HIGH` |
| **`UNICODE_OBFUSCATION`**| Right-To-Left Override (`\u202E`) or zero-width chars | Unicode code point scanning (`[\u202A-\u202E\u200B-\u200D\uFEFF]`) | `HIGH` |
| **`WIN32_NAMESPACE_BYPASS`** | Trailing dots/spaces or reserved names (`CON`, `NUL`) | POSIX path normalization & NT namespace checks (`\\?\`) | `HIGH` |
| **`PE_MASQUERADE`** | Windows PE executables disguised as `.png`, `.pdf`, `.txt` | Binary magic-byte inspection (checking bytes 0-1 for `0x4D 0x5A` / `MZ`) | `CRITICAL` |

---

## 3. Operational CLI Commands

### A. Run Comprehensive Evasion Scan
```powershell
# Interactive colored CLI report
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\src\EvasionHunter.ps1" -TargetPath "C:\TargetDirectory"

# Machine-readable JSON for automated SIEM / EDR pipelines
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\src\EvasionHunter.ps1" -TargetPath "C:\TargetDirectory" -JsonOutput
```

### B. Harvest Windows Execution Artifacts (Prefetch)
```powershell
# Harvest recent 50 executions
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\src\ArtifactHarvester.ps1" -Limit 50

# Filter execution history for a specific binary
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\src\ArtifactHarvester.ps1" -ProcessNameFilter "powershell"
```

### C. Run Regression Test Suite
```powershell
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\tests\test_evasion_hunter.ps1"
```

---

## 4. Repository Synchronization

Always run version control and regression passes through `sync.bat`:
```powershell
cd F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics
.\sync.bat -m "feat(scope): commit description"
```
