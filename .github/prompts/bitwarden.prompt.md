---
description: ">-"
---

# Bitwarden MCP Assistant Skill

This skill governs how AI assistants (Antigravity, Claude, and orchestration agents) interact securely with local Bitwarden vaults using the official `@bitwarden/mcp-server` integration.

---

## 🎯 When to Activate This Skill

Activate this skill whenever the user:
- Requests access to credentials, API keys, or accounts stored in Bitwarden (e.g. *"Get my login for GitHub"*, *"Fetch my API key from secure notes"*).
- Asks to save or generate credentials (e.g. *"Generate a 32-character password and store it for cloudflare.com"*).
- Asks to search or inspect vault items (e.g. *"List logins in my Work folder"*, *"Check details for item 'Database'*).
- Asks to lock, unlock, or sync the Bitwarden vault.
- Asks to share text or files securely using Bitwarden Send.
- Inquires about Bitwarden organization collections, members, or policies.

---

## 🔒 Security Invariants & Epistemic Boundaries

1. **Local Execution Only**: The MCP server and Bitwarden CLI (`bw`) operate strictly on localhost. Under no circumstances should this server be hosted publicly or bridged over remote networks.
2. **Zero-Knowledge Master Password Handling**:
   - The `unlock` tool takes **no arguments**. It triggers a native OS masked input dialog (PowerShell WinForms on Windows).
   - Never prompt the user for their master password in chat, and never echo or store master passwords in code or environment files.
3. **Redaction & Context Hygiene**:
   - Only retrieve specific items needed for the task; avoid dumping whole vault inventories into model contexts.
   - When presenting credentials, avoid logging raw passwords to long-term conversation logs or committed repository artifacts.
4. **Interactive Confirmation for Destructive Actions**:
   - Permanent deletion (`delete`, `delete_send`) or policy alterations must have explicit user confirmation.

---

## 🧰 Available MCP Tools Mapping

All tools are exposed by the `bitwarden` MCP server:

### Session & Vault Status
| Intent | MCP Tool | Details |
| :--- | :--- | :--- |
| Check vault lock/sync status | `status` | Returns lock state, user email, server URL |
| Unlock vault | `unlock` | Opens native Windows masked password prompt |
| Lock vault | `lock` | Purges local session decryption keys |
| Sync vault | `sync` | Fetches latest vault changes from Bitwarden cloud |

### Vault Items & Secrets
| Intent | MCP Tool | Key Parameters |
| :--- | :--- | :--- |
| Search vault items | `list` | `search`, `folderId`, `collectionId` |
| Get item details | `get` | `id` |
| Create new credential | `create_item` | `item` (login, note, card, identity) |
| Edit existing item | `edit_item` | `id`, `item` |
| Move item to trash | `delete` | `id` |
| Restore item from trash | `restore` | `id` |
| Generate secure password | `generate` | `length`, `uppercase`, `lowercase`, `numbers`, `special` |

### Bitwarden Send & Files
| Intent | MCP Tool | Key Parameters |
| :--- | :--- | :--- |
| Send secure text | `create_text_send` | `name`, `text`, `maxAccessCount`, `expirationDate` |
| Send secure file | `create_file_send` | `name`, `filePath` (must be in `BW_ALLOWED_DIRECTORIES`) |
| List active Sends | `list_send` | - |
| Remove Send password | `remove_send_password`| `id` |

---

## 📋 Standard Workflow Patterns

### 1. Retrieving a Secret / Login
1. Call `status` to ensure vault is unlocked.
2. If locked, call `unlock` (notifying the user that a native Windows password prompt will appear).
3. Call `list` with `search: "<keyword>"` to find the matching item ID.
4. Call `get` with the item `id` to obtain the specific field required.

### 2. Generating & Saving Credentials
1. Generate password via `generate(length=32, uppercase=true, lowercase=true, numbers=true, special=true)`.
2. Construct item schema (URI, username, password, notes).
3. Call `create_item(item=...)`.
4. Confirm creation to the user without printing plaintext passwords unless explicitly asked.
