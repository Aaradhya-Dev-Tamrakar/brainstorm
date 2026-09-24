---
name: security-guidance
description: Security guidance for code generation, auditing, and commits. Covers dangerous patterns including secrets, deserialization, command injection, path traversal, XSS, SSRF, IDOR.
---

# security-guidance

Security review for Claude-generated code. Three layers:

1. **Pattern warnings** — instant regex-based reminders on `Edit`/`Write` for ~25 known-dangerous patterns (`yaml.load`, `torch.load(weights_only=False)`, `pickle.load` on untrusted data, raw `innerHTML`, hardcoded secrets, etc.).
2. **LLM diff review** — when Claude finishes a turn, the plugin sends the diff to a fast LLM call (Opus 4.7 by default) and feeds high-severity findings back to Claude so it can fix them before you see the response.
3. **Agentic commit review** — on `git commit`, an SDK-driven reviewer reads related files (`Read`/`Grep`/`Glob`) to trace data flow across the codebase, catching multi-file vulnerabilities pattern matching misses (IDOR, auth bypass, cross-file SSRF).

Findings cover common web-vulnerability classes — injection, XSS, SSRF, hardcoded secrets, IDOR, auth bypass, unsafe deserialization, and path traversal among others.

## Install

```
/plugin install security-guidance@claude-plugins-official
```

Marketplace ships enabled by default in Claude Code — no setup beyond having the CLI itself.

## Prerequisites

- Claude Code CLI ≥ v2.1.144
- Python 3.8+ on `PATH` (`python3`, `python`, or `py -3` — the plugin picks the first that works)
- A working API path (subscription, API key, or 3P provider config)

## Configuration

All configuration is via environment variables. None are required for default behavior.

### Selecting a model

```bash
# 1P / gateway: a canonical model id
SECURITY_REVIEW_MODEL=claude-opus-4-7   # default

# Bedrock: use the inference-profile id
SECURITY_REVIEW_MODEL=us.anthropic.claude-opus-4-7

# Vertex: use the Vertex date-tag form
SECURITY_REVIEW_MODEL=claude-opus-4-7@20260218
```

`SECURITY_REVIEW_MODEL` controls the LLM diff review. `SG_AGENTIC_MODEL` (same syntax) controls the agentic commit reviewer; defaults to the same model.

### Enabling/disabling layers

| Variable | Default | What it does |
|---|---|---|
| `SECURITY_GUIDANCE_DISABLE=1` | unset | Kill switch — disables the entire plugin |
| `ENABLE_PATTERN_RULES=0` | on | Disable layer 1 (regex pattern warnings) |
| `ENABLE_CODE_SECURITY_REVIEW=0` | on | Disable all LLM reviews (Stop hook + commit/push) |
| `ENABLE_STOP_REVIEW=0` | on | Disable only the Stop-hook diff review, keeping commit/push reviews. Useful for multi-agent / shared-worktree setups where another agent can move HEAD between a worker's turns |
| `ENABLE_COMMIT_REVIEW=0` | on | Disable layer 3 (agentic commit review) |

### Higher-recall mode

```bash
SG_DUAL_OR=on   # default off
```

Runs two parallel review calls and unions the findings. Catches a few percentage points more vulnerabilities in our testing, at roughly 2× the API cost per review. Most users don't need it.

## Org-specific policies

Drop a `claude-security-guidance.md` in any of:

- `~/.claude/claude-security-guidance.md` — user-wide rules
- `<project>/.claude/claude-security-guidance.md` — project rules, intended to be committed
- `<project>/.claude/claude-security-guidance.local.md` — local overrides, intended to be `.gitignore`'d

All three are loaded and concatenated into the LLM diff review's prompt in the order user → project → project-local. If the combined size exceeds the 8 KB prompt budget, the tail is truncated, so user-wide rules are kept and project-local rules are dropped first. The agentic commit reviewer (layer 3) does not currently read this file. Example:

```markdown
# Acme security rules

- All SELECTs against the `customers` or `orders` tables MUST go through `db.replica`,
  never `db.primary`. Primary is for writes only.
- Background jobs must not use the user-context auth token; they get
  service-account creds from `jobs.get_service_account()`.
- Calls to `requests.get(url)` with a user-controlled `url` need
  the SSRF-allowlist wrapper at `acme.net.safe_request`.
```

Built-in rules cover common web-vulnerability classes without it — `claude-security-guidance.md` is for things specific to your codebase that the model can't infer.

## Privacy and data handling

The plugin sends data to a model endpoint to perform its reviews. Specifically, each Stop-hook diff review transmits the changed file paths, the diff hunks, and the relevant file contents in the diff; each agentic commit review additionally transmits any files the reviewer pulls in via `Read`/`Grep`/`Glob` while tracing data flow. Your `claude-security-guidance.md` contents (user, project, and local) are appended to the prompt on every review, so don't put secrets in it.

Where that data goes depends on your Claude Code configuration:
- **Default (Anthropic API / subscription):** sent to `api.anthropic.com` and handled under Anthropic's [Commercial Terms](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
- **LLM gateway** (`ANTHROPIC_BASE_URL` set): sent to your gateway URL instead. The gateway operator's terms apply.
- **3rd-party providers** (Bedrock / Vertex / Foundry / Mantle): sent to your configured provider endpoint. The provider's data-handling terms apply (e.g., AWS / GCP / Azure).

The plugin writes its own debug log to `~/.claude/security/log.txt` (override with `SECURITY_GUIDANCE_DEBUG_LOG`). The log contains diffstate metadata and finding categories — no full file contents or model prompts — and rotates at 1 MB. Nothing is uploaded.

## Limitations

This is a best-effort assistive tool, not a guarantee. Treat findings as suggestions, not as a substitute for human code review, SAST/DAST, dependency scanning, or pen-testing. The reviewer can miss vulnerabilities, produce false positives, and may behave differently across codebases, languages, and model versions. **No warranty is provided** — use is subject to Anthropic's [Commercial Terms](https://www.anthropic.com/legal/commercial-terms).

## Troubleshooting

**Plugin doesn't seem to fire** — check that `~/.claude/claude-security-guidance.md` (or hook activity) shows in debug logs. Run Claude Code with `--debug-file /tmp/claude/debug.txt` and grep for `security_reminder_hook`. The plugin also writes its own log to `~/.claude/security/log.txt`.

**Review never finds anything** — verify your API path works. On 3P providers, check `SECURITY_REVIEW_MODEL` is set to a provider-specific id (not a bare `claude-opus-4-7`). On LLM gateways, check the gateway's logs for `POST /v1/messages` traffic from the plugin.

**Too many false positives** — drop `SECURITY_REVIEW_MODEL` to a cheaper model (`claude-sonnet-4-6`) and re-evaluate; if precision is the priority, stay on Opus 4.7.

**Want to silence a specific finding** — add a comment to the line explaining why it's safe; the LLM reviewer treats inline justifications as exclusions. For systemic exclusions, document them in your `claude-security-guidance.md`.

## Reporting issues

Open an issue on the [security-guidance plugin repo](https://github.com/anthropics/claude-code/issues) with:
- The Claude Code CLI version (`claude --version`)
- Provider setup (1P / Bedrock / Vertex / LLM gateway / etc.)
- A minimal repro diff
- The relevant section of `~/.claude/security/log.txt`


## Vulnerability Patterns Reference

`python
"""
Regex-based security pattern definitions for the security-guidance plugin.

Pure data + one pure helper. No env-var reads, no I/O, no debug_log — kept
side-effect-free so it can be imported in isolation.
"""
from enum import IntEnum


_JS_EXTS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte")
_PY_EXTS = (".py", ".pyi", ".ipynb")
_DOC_EXTS = (".md", ".mdx", ".txt", ".rst", ".json", ".yaml", ".yml")


_UNSAFE_DESERIALIZATION_REMINDER = """⚠️ Security Warning: Loading pickle data (or equivalents: cPickle, cloudpickle, dill, marshal, shelve, joblib, pandas.read_pickle, numpy with allow_pickle=True) from untrusted sources allows arbitrary code execution.

For simple data, prefer JSON or msgspec. For typed objects, prefer a schema-validated deserializer (msgspec.Struct, pydantic, marshmallow) that constructs only declared types.

If this is safe or is explicitly needed, briefly document that in a comment before continuing."""

_UNSAFE_YAML_LOAD_REMINDER = """⚠️ Security Warning: yaml.load() / yaml.unsafe_load() execute arbitrary Python via !!python/object tags.

Use yaml.safe_load() if the file only contains simple data structures (dicts, lists, strings, numbers). If you need typed objects, parse with safe_load and validate the result against a schema (pydantic, msgspec, marshmallow) — never use a custom Loader that constructs arbitrary types."""

_UNSAFE_TORCH_LOAD_REMINDER = """⚠️ Security Warning: torch.load() defaults to weights_only=False, which unpickles arbitrary Python objects and allows arbitrary code execution.

If the file only contains tensors and simple data structures, pass weights_only=True (or set TORCH_FORCE_WEIGHTS_ONLY_LOAD=1)."""

# Security patterns configuration
SECURITY_PATTERNS = [
    {
        "ruleName": "github_actions_workflow",
        "path_check": lambda path: ".github/workflows/" in path
        and (path.endswith(".yml") or path.endswith(".yaml")),
        "reminder": """⚠️ Security Warning: You are editing a GitHub Actions workflow file. Be aware of these security risks:

1. **Command Injection**: Never use untrusted input (like issue titles, PR descriptions, commit messages) directly in run: commands without proper escaping
2. **Use environment variables**: Instead of ${{ github.event.issue.title }}, use env: with proper quoting
3. **Review the guide**: https://github.blog/security/vulnerability-research/how-to-catch-github-actions-workflow-injections-before-attackers-do/

Example of UNSAFE pattern to avoid:
run: echo "${{ github.event.issue.title }}"

Example of SAFE pattern:
env:
  TITLE: ${{ github.event.issue.title }}
run: echo "$TITLE"

Other risky inputs to be careful with:
- github.event.issue.body
- github.event.pull_request.title
- github.event.pull_request.body
- github.event.comment.body
- github.event.review.body
- github.event.review_comment.body
- github.event.pages.*.page_name
- github.event.commits.*.message
- github.event.head_commit.message
- github.event.head_commit.author.email
- github.event.head_commit.author.name
- github.event.commits.*.author.email
- github.event.commits.*.author.name
- github.event.pull_request.head.ref
- github.event.pull_request.head.label
- github.event.pull_request.head.repo.default_branch
- github.event.client_payload.* (repository_dispatch events — attacker can set any field)

4. **Ref injection**: Never use untrusted input in `ref:` parameters of `actions/checkout`. For `client_payload.pr_number`, validate it matches `^[0-9]+$` before using in `ref: refs/pull/${{ ... }}/head`
- github.head_ref""",
    },
    {
        "ruleName": "child_process_exec",
        # Gate to JS/TS files — bare `exec(` otherwise fires on Python's
        # exec() and on prose/docstrings mentioning exec.
        "path_filter": lambda p: p.endswith(_JS_EXTS),
        "substrings": ["child_process.exec", "execSync("],
        "regex": r"(?<![a-zA-Z0-9_\.])exec\(",
        "reminder": """⚠️ Security Warning: Using child_process.exec() can lead to command injection vulnerabilities.

exec() runs the command string through a shell, so any user input interpolated into it can inject arbitrary commands. Prefer child_process.execFile() (or spawn()) with an argument array instead of building a shell string.

Instead of:
  exec(`command ${userInput}`)

Use:
  import { execFile } from 'node:child_process'
  execFile('command', [userInput], callback)

Why execFile/spawn with an argument array is safer:
- No shell is involved, so shell metacharacters in arguments are not interpreted
- Arguments are passed directly to the program rather than interpolated into a command string

Only use exec() if you absolutely need shell features and the input is guaranteed to be safe.""",
    },
    {
        "ruleName": "new_function_injection",
        "substrings": ["new Function"],
        "reminder": "\u26a0\ufe0f Security Warning: Using new Function() with string interpolation is a CODE INJECTION vulnerability. If any variable is concatenated or interpolated into the function body string, an attacker controlling that variable can execute arbitrary code. Use safe alternatives: for property access use obj[key] or array.reduce((o, k) => o[k], root); for computation use a safe expression parser. NEVER interpolate untrusted strings into new Function() bodies.",
    },
    {
        "ruleName": "eval_injection",
        # Lookbehind excludes `.` so method calls like PyTorch model.eval(),
        # redis.eval(), spec.eval() don't match. Skip doc/prose files.
        "path_filter": lambda p: not p.endswith(_DOC_EXTS),
        "regex": r"(?<![a-zA-Z0-9_\.])eval\(",
        "reminder": "⚠️ Security Warning: eval() executes arbitrary code and is a major security risk. Use JSON.parse() for data, ast.literal_eval() for Python literals, or a safe expression parser. If this is safe or is explicitly needed, briefly document that in a comment before continuing.",
    },
    {
        "ruleName": "react_dangerously_set_html",
        "substrings": ["dangerouslySetInnerHTML"],
        "reminder": "⚠️ Security Warning: dangerouslySetInnerHTML can lead to XSS vulnerabilities if used with untrusted content. Ensure all content is properly sanitized using an HTML sanitizer library like DOMPurify, or use safe alternatives.",
    },
    {
        "ruleName": "document_write_xss",
        "substrings": ["document.write"],
        "reminder": "⚠️ Security Warning: document.write() can be exploited for XSS attacks and has performance issues. Use DOM manipulation methods like createElement() and appendChild() instead.",
    },
    {
        "ruleName": "innerHTML_xss",
        "substrings": [".innerHTML =", ".innerHTML="],
        "reminder": "⚠️ Security Warning: Setting innerHTML with untrusted content can lead to XSS vulnerabilities. Use textContent for plain text or safe DOM methods for HTML content. If you need HTML support, consider using an HTML sanitizer library such as DOMPurify.",
    },
    {
        "ruleName": "pickle_deserialization",
        # Match deserialization only (load/loads/Unpickler). pickle.dump is
        # not the RCE surface. `pkl_load` needs a word boundary so similarly
        # named safe loaders don't match.
        "path_filter": lambda p: p.endswith(_PY_EXTS),
        "regex": r"(?<![a-zA-Z0-9_])pickle\.(loads?|Unpickler)\b|(?<![a-zA-Z0-9_])pkl_load\(",
        "reminder": _UNSAFE_DESERIALIZATION_REMINDER,
    },
    {
        "ruleName": "os_system_injection",
        "path_filter": lambda p: p.endswith(_PY_EXTS),
        "regex": r"\bos\.system\s*\(",
        "substrings": ["from os import system"],
        "reminder": "⚠️ Security Warning: os.system() runs a shell and is a command-injection sink. Use subprocess.run([...]) with a list of arguments instead. If this is safe or is explicitly needed, briefly document that in a comment before continuing.",
    },
    {
        "ruleName": "python_subprocess_shell",
        "regex": r"subprocess\.(?:run|call|Popen|check_output|check_call)\(.*shell\s*=\s*True",
        "reminder": """⚠️ Security Warning: Using subprocess with shell=True enables command injection.

UNSAFE:
  subprocess.run(f"ls {user_input}", shell=True)
  subprocess.call("grep " + pattern, shell=True)

SAFE - pass arguments as a list without shell:
  subprocess.run(["ls", user_input])
  subprocess.call(["grep", pattern])

When arguments are passed as a list without shell=True, special characters cannot be interpreted as shell metacharacters.""",
    },
    # =====================================================================
    # Go-specific security patterns
    # =====================================================================
    {
        "ruleName": "go_exec_shell_injection",
        # Detect exec.Command with shell invocation (sh, bash, /bin/sh, /bin/bash)
        "regex": r'exec\.Command\(\s*"(?:sh|bash|/bin/sh|/bin/bash)"',
        "reminder": """⚠️ Security Warning: Using exec.Command with a shell interpreter (sh/bash) enables command injection.

UNSAFE:
  exec.Command("sh", "-c", "ping -c 1 " + host)
  exec.Command("bash", "-c", fmt.Sprintf("df -h %s", path))

SAFE - pass arguments directly without a shell:
  exec.Command("ping", "-c", "1", host)
  exec.Command("df", "-h", path)

When arguments are passed directly (not through a shell), special characters in user input cannot be interpreted as shell metacharacters. This prevents command injection entirely.

Additionally, validate user inputs:
- For hostnames/IPs: use net.ParseIP() or a hostname regex
- For file paths: use filepath.Clean() and verify the result is within an allowed directory
- For numeric values: parse to int/float first""",
    },
    {
        "ruleName": "unsafe_yaml_load",
        "regex": r"\byaml\.load\s*\((?![^)\n]{0,80}\bSafe)",
        "reminder": _UNSAFE_YAML_LOAD_REMINDER,
    },
    {
        "ruleName": "node_createcipher_no_iv",
        "regex": r"\bcrypto\.(createCipher|createDecipher)\b",
        "reminder": "⚠️ Security Warning: Use crypto.createCipheriv() / createDecipheriv(). createCipher was removed in Node 22 and derives the key insecurely (no IV, MD5-based KDF).",
    },
    {
        "ruleName": "aes_ecb_mode",
        "regex": r"\bAES\.MODE_ECB\b|\bmodes\.ECB\s*\(|[\x22\x27]aes-\d+-ecb[\x22\x27]",
        "reminder": "⚠️ Security Warning: Use AES-GCM or AES-CBC with HMAC. ECB mode leaks plaintext structure (identical blocks encrypt to identical ciphertext).",
    },
    {
        "ruleName": "tls_verification_disabled",
        "regex": r"\bverify\s*=\s*False\b|rejectUnauthorized\s*:\s*false|InsecureSkipVerify\s*:\s*true|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*[\x22\x27]?0|ssl\._create_unverified_context|check_hostname\s*=\s*False",
        "reminder": "⚠️ Security Warning: Don't disable TLS verification. This allows MITM attacks. For self-signed dev certs, add the CA to your trust store or use a properly-issued cert.",
    },
    {
        "ruleName": "marshal_loads",
        "regex": r"\bmarshal\.loads?\s*\(",
        "reminder": _UNSAFE_DESERIALIZATION_REMINDER,
    },
    {
        "ruleName": "shelve_open",
        "regex": r"\bshelve\.open\s*\(",
        "reminder": _UNSAFE_DESERIALIZATION_REMINDER,
    },
    {
        "ruleName": "xml_unsafe_parse",
        "regex": r"\b(xml\.etree\.ElementTree|ElementTree|ET)\.(parse|fromstring|XML)\s*\(|\bminidom\.(parse|parseString)\s*\(|\bxml\.sax\.(parse|make_parser)\b",
        "reminder": "⚠️ Security Warning: Use defusedxml.ElementTree. Python's stdlib XML parsers are vulnerable to XXE (external entity) and billion-laughs attacks by default.",
    },
    {
        "ruleName": "pickle_variants_load",
        "regex": r"\b(cPickle|cloudpickle|dill)\.(load|loads)\s*\(",
        "reminder": _UNSAFE_DESERIALIZATION_REMINDER,
    },
    {
        "ruleName": "outerHTML_xss",
        "substrings": [".outerHTML =", ".outerHTML="],
        "reminder": "⚠️ Security Warning: Use textContent or sanitize with DOMPurify. outerHTML assignment is an XSS sink equivalent to innerHTML.",
    },
    {
        "ruleName": "insertAdjacentHTML_xss",
        "substrings": [".insertAdjacentHTML("],
        "reminder": "⚠️ Security Warning: Use insertAdjacentText() or sanitize with DOMPurify. insertAdjacentHTML is an XSS sink.",
    },
    {
        "ruleName": "script_src_without_sri",
        # Detect remote code execution via dynamic import/eval of fetched content.
        # Negative lookahead after src checks for integrity= anywhere in the remaining tag.
        "regex": (
            r"<script\s+(?![^>]{0,400}integrity\s*=)"
            r"[^>]{0,200}src\s*=\s*[\x22\x27](?:https?:)?//"
            r"[^\x22\x27]{1,300}[\x22\x27]"
            r"[^>]{0,100}>"
        ),
        "reminder": '⚠️ Security Warning: Add integrity="sha384-..." crossorigin="anonymous" to external script tags. Loading scripts without Subresource Integrity exposes you to CDN compromise.',
    },
    {
        "ruleName": "torch_unsafe_load",
        # Suppressed by weights_only=True on the same line (within 200 chars). weights_only=False
        # still triggers. Multi-line calls false-positive — same known limitation as unsafe_yaml_load.
        "regex": r"(?:\btorch\.load|\.torch_load)\s*\((?![^)\n]{0,200}weights_only\s*=\s*True)",
        "reminder": _UNSAFE_TORCH_LOAD_REMINDER,
    },
    {
        "ruleName": "yaml_unsafe_load_variants",
        # yaml.unsafe_load (stdlib alias) plus unsafe wrapper method names seen in the wild.
        # Bare yaml.load() is unsafe_yaml_load's job (RuleId 12).
        "regex": r"(?:\byaml\.unsafe_load|\.yaml_unsafe_load)\s*\(",
        "reminder": _UNSAFE_YAML_LOAD_REMINDER,
    },
    {
        "ruleName": "pickle_wrapper_load",
        # Library APIs that unpickle without saying "pickle". numpy.load only triggers
        # when allow_pickle=True is explicit (defaults to False since numpy 1.16.3).
        "regex": r"\bjoblib\.load\s*\(|\b(?:pd|pandas)\.read_pickle\s*\(|\.cloudpickle_load\s*\(|\b(?:np|numpy)\.load\s*\([^)\n]{0,200}allow_pickle\s*=\s*True",
        "reminder": _UNSAFE_DESERIALIZATION_REMINDER,
    },
]


class RuleId(IntEnum):
    """
    Stable numeric IDs for SECURITY_PATTERNS rules, emitted via the PostToolUse
    metrics field so telemetry can attribute pattern-warning events to
    specific checks. The metrics schema only allows bool|number values (no
    strings), so rule names can't be sent directly.

    Values are frozen: do not renumber existing entries. Append new ones.
    """
    GITHUB_ACTIONS_WORKFLOW = 1
    CHILD_PROCESS_EXEC = 2
    NEW_FUNCTION_INJECTION = 3
    EVAL_INJECTION = 4
    REACT_DANGEROUSLY_SET_HTML = 5
    DOCUMENT_WRITE_XSS = 6
    INNERHTML_XSS = 7
    PICKLE_DESERIALIZATION = 8
    OS_SYSTEM_INJECTION = 9
    PYTHON_SUBPROCESS_SHELL = 10
    GO_EXEC_SHELL_INJECTION = 11
    UNSAFE_YAML_LOAD = 12
    NODE_CREATECIPHER_NO_IV = 13
    AES_ECB_MODE = 14
    TLS_VERIFICATION_DISABLED = 15
    MARSHAL_LOADS = 16
    SHELVE_OPEN = 17
    XML_UNSAFE_PARSE = 18
    PICKLE_VARIANTS_LOAD = 19
    OUTERHTML_XSS = 20
    INSERTADJACENTHTML_XSS = 21
    SCRIPT_SRC_WITHOUT_SRI = 22
    TORCH_UNSAFE_LOAD = 23
    YAML_UNSAFE_LOAD_VARIANTS = 24
    PICKLE_WRAPPER_LOAD = 25


_RULE_NAME_TO_ID = {
    "github_actions_workflow": RuleId.GITHUB_ACTIONS_WORKFLOW,
    "child_process_exec": RuleId.CHILD_PROCESS_EXEC,
    "new_function_injection": RuleId.NEW_FUNCTION_INJECTION,
    "eval_injection": RuleId.EVAL_INJECTION,
    "react_dangerously_set_html": RuleId.REACT_DANGEROUSLY_SET_HTML,
    "document_write_xss": RuleId.DOCUMENT_WRITE_XSS,
    "innerHTML_xss": RuleId.INNERHTML_XSS,
    "pickle_deserialization": RuleId.PICKLE_DESERIALIZATION,
    "os_system_injection": RuleId.OS_SYSTEM_INJECTION,
    "python_subprocess_shell": RuleId.PYTHON_SUBPROCESS_SHELL,
    "go_exec_shell_injection": RuleId.GO_EXEC_SHELL_INJECTION,
    "unsafe_yaml_load": RuleId.UNSAFE_YAML_LOAD,
    "node_createcipher_no_iv": RuleId.NODE_CREATECIPHER_NO_IV,
    "aes_ecb_mode": RuleId.AES_ECB_MODE,
    "tls_verification_disabled": RuleId.TLS_VERIFICATION_DISABLED,
    "marshal_loads": RuleId.MARSHAL_LOADS,
    "shelve_open": RuleId.SHELVE_OPEN,
    "xml_unsafe_parse": RuleId.XML_UNSAFE_PARSE,
    "pickle_variants_load": RuleId.PICKLE_VARIANTS_LOAD,
    "outerHTML_xss": RuleId.OUTERHTML_XSS,
    "insertAdjacentHTML_xss": RuleId.INSERTADJACENTHTML_XSS,
    "script_src_without_sri": RuleId.SCRIPT_SRC_WITHOUT_SRI,
    "torch_unsafe_load": RuleId.TORCH_UNSAFE_LOAD,
    "yaml_unsafe_load_variants": RuleId.YAML_UNSAFE_LOAD_VARIANTS,
    "pickle_wrapper_load": RuleId.PICKLE_WRAPPER_LOAD,
}

# Fail loudly at import time if a pattern is added without a RuleId.
# This fires in pytest on every PR, so desync is caught before merge.
assert set(_RULE_NAME_TO_ID) == {p["ruleName"] for p in SECURITY_PATTERNS}, (
    f"RuleId enum out of sync with SECURITY_PATTERNS: "
    f"missing={set(p['ruleName'] for p in SECURITY_PATTERNS) - set(_RULE_NAME_TO_ID)}, "
    f"extra={set(_RULE_NAME_TO_ID) - set(p['ruleName'] for p in SECURITY_PATTERNS)}"
)


def rule_names_to_mask(rule_names):
    """Pack a set of rule names into a bitmask. Bit N set means RuleId(N) matched.
    User-defined patterns (rule_name starting with "user:") have no static
    RuleId and are excluded from the mask."""
    mask = 0
    for name in rule_names:
        if name in _RULE_NAME_TO_ID:
            mask |= 1 << _RULE_NAME_TO_ID[name]
    return mask

`
