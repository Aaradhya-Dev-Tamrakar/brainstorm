---
name: win-vault
description: Expert Windows folder locking, privacy vault management, and kernel-level NTFS Access Control (ACL) administration using Win-Vault (F:\Aaradhya-Dev-Tamrakar\Win-Vault). Use whenever asked to lock/unlock folders, protect sensitive directories, manage vault master passwords, or enforce low-level filesystem access denial without third-party tools.
category: security
---

# Win-Vault — Windows Privacy Vault & Access Control Engine

This skill guides agents in utilizing and managing **Win-Vault** (`F:\Aaradhya-Dev-Tamrakar\Win-Vault`), Aaradhya's zero-dependency Windows privacy vault and kernel-level filesystem locking engine.

---

## 1. Core Architecture & Location

* **Project Root:** `F:\Aaradhya-Dev-Tamrakar\Win-Vault`
* **Repository:** `https://github.com/Aaradhya-Dev-Tamrakar/Win-Vault`
* **Entrypoints:**
  * `Vault.bat`: Zero-friction batch launcher that invokes `Vault.ps1` silently.
  * `Vault.ps1`: Pure PowerShell + Windows Forms GUI controller and security engine.
  * `pass.bat`: Backwards-compatible legacy wrapper.

---

## 2. Security & Locking Primitives

Win-Vault operates across three distinct defensive layers:

1. **Kernel-Level NTFS Access Control List (ACL)**:
   * Uses .NET `System.Security.AccessControl.FileSystemAccessRule` to apply an explicit `Deny` rule for `WorldSid` (`*S-1-1-0`, Everyone).
   * Blocks all file open, read, list, write, and directory traversal attempts directly in the Windows filesystem driver (producing native "Access Denied" errors even from elevated terminals).
2. **Hidden + System Attributes**:
   * Applies `[System.IO.FileAttributes]::Hidden -bor [System.IO.FileAttributes]::System`.
   * Completely conceals the directory from standard File Explorer listings (even with "Show hidden files" enabled).
3. **Cryptographic SHA-256 Master Key Hashing**:
   * Plaintext passwords are never stored. The master password hash is recorded in `.vault_key.dat` with `Hidden + System` flags.

---

## 3. Usage & Operations

### Interactive GUI Mode
Double-click [`Vault.bat`](file:///F:/Aaradhya-Dev-Tamrakar/Win-Vault/Vault.bat) or run from PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File "F:\Aaradhya-Dev-Tamrakar\Win-Vault\Vault.ps1"
```
* **First Run:** Automatically launches the first-time setup wizard to create and confirm a master password.
* **When Unlocked:** Displays action dialog: **🔒 Lock Vault**, **📂 Open Folder**, or **🔑 Change Master Password**.
* **When Locked:** Displays a masked password prompt (`●●●●`) with a 3-attempt brute force rate limiter. Auto-opens File Explorer upon unlock.

### Programmatic CLI Locking & Unlocking

#### Locking a Folder via .NET ACL:
```powershell
$target = "F:\Aaradhya-Dev-Tamrakar\Win-Vault\PrivateVault"
$lockedName = "$target.{21EC2020-3AEA-1069-A2DD-08002B30309D}"

Rename-Item -LiteralPath $target -NewName $lockedName -Force
$item = Get-Item -LiteralPath $lockedName -Force
$item.Attributes = [IO.FileAttributes]::Hidden -bor [IO.FileAttributes]::System

$acl = $item.GetAccessControl()
$sid = New-Object Security.Principal.SecurityIdentifier([Security.Principal.WellKnownSidType]::WorldSid, $null)
$rule = New-Object Security.AccessControl.FileSystemAccessRule($sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Deny')
$acl.AddAccessRule($rule)
$item.SetAccessControl($acl)
```

#### Unlocking:
```powershell
$item = Get-Item -LiteralPath $lockedName -Force
$acl = $item.GetAccessControl()
$sid = New-Object Security.Principal.SecurityIdentifier([Security.Principal.WellKnownSidType]::WorldSid, $null)
$rule = New-Object Security.AccessControl.FileSystemAccessRule($sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Deny')
$acl.RemoveAccessRule($rule) | Out-Null
$item.SetAccessControl($acl)

$item.Attributes = [IO.FileAttributes]::Directory -bor [IO.FileAttributes]::Normal
Rename-Item -LiteralPath $lockedName -NewName "PrivateVault" -Force
```

---

## 4. Repository Synchronization

Always synchronize updates to Win-Vault using its dedicated wrapper:
```powershell
cd F:\Aaradhya-Dev-Tamrakar\Win-Vault
.\sync.bat -m "feat(scope): commit description"
```
