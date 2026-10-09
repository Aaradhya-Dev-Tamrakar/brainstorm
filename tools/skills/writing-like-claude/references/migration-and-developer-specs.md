# Developer Technical Specifications & Migration Guides (Register 3)

This reference defines the documentation standards for developer tutorials, platform SDK guides, and model migration manuals modeled after `platform.claude.com/docs`.

---

## 1. Core Principles: Zero Ambiguity & Mechanical Precision

Developer-facing technical writing must prioritize copy-paste reliability, parameter clarity, and explicit breaking change demarcation:
- **Exact Identifiers**: Always publish full, un-aliased model strings (e.g. `claude-haiku-5-5-20261001`) alongside standard alias pointers (`claude-haiku-5-5`).
- **Before vs. After Payloads**: Never describe API payload alterations purely in prose. Always provide side-by-side or consecutive JSON snippets showing the exact field diff.
- **Immediate Copy-Pasteability**: Every code example must include necessary client initializations, environment variable definitions, and expected return structures.

---

## 2. Model Migration Guide Blueprint

When documenting a model version transition (*e.g. migrating from Haiku 4.5 to Haiku 5.5*), follow this standardized 5-part structure:

### 1. Model Identifier Table & Cost Deltas
Declare the exact model ID strings and token price comparisons upfront:

| Model Version | API Model Identifier | Input / MTok | Output / MTok | Cache Read / MTok |
| :--- | :--- | :--- | :--- | :--- |
| **Haiku 4.5 (Legacy)** | `claude-3-haiku-20240307` | \$0.25 | \$1.25 | \$0.025 |
| **Haiku 5.5 (Current)** | `claude-haiku-5-5-20261001` | \$0.07 | \$0.35 | \$0.007 |

### 2. Breaking Changes Matrix
Document parameter alterations, deprecations, and type modifications in a structured table:

| Parameter / Feature | Previous Model (Haiku 4.5) | Current Model (Haiku 5.5) | Required Action |
| :--- | :--- | :--- | :--- |
| `max_tokens` max limit | 4,096 | 8,192 | Can increase output buffer up to 8k tokens. |
| Tool choice syntax | `{"type": "auto"}` | `{"type": "auto", "disable_parallel_tool_use": false}` | Optional: control tool parallelism explicitly. |
| `effort` setting | Unsupported | `low` \| `medium` \| `high` \| `max` | Add `effort` parameter to adjust compute budget. |

### 3. Request Payload Before / After Diffs
Provide concrete request blocks illustrating exact parameter transitions:

#### Previous Request (Legacy Model):
```json
{
  "model": "claude-3-haiku-20240307",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "Extract invoice items from this receipt text."}
  ]
}
```

#### New Request (Current Model):
```json
{
  "model": "claude-haiku-5-5-20261001",
  "max_tokens": 2048,
  "effort": "low",
  "messages": [
    {"role": "user", "content": "Extract invoice items from this receipt text."}
  ]
}
```

### 4. SDK Integration Example
Provide functional code in Python and TypeScript demonstrating client invocation:

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-haiku-5-5-20261001",
    max_tokens=2048,
    effort="low",
    messages=[
        {"role": "user", "content": "Summarize server logs into structured JSON."}
    ]
)
print(response.content[0].text)
```

### 5. Migration Checklist by Starting Model
Provide actionable checkboxes enabling engineering teams to verify their rollout:

- [ ] Update `model` parameter string to `claude-haiku-5-5-20261001`.
- [ ] Review `max_tokens` limits across production prompts.
- [ ] Evaluate `effort` parameter configuration: set to `low` for high-throughput classification; set to `high` for subagent coding workflows.
- [ ] Verify error handling for rate limit status codes (`429`) and context overflow (`400`).
- [ ] Test system prompt adherence: Haiku 5.5 adheres more strictly to XML formatting tags (`<instructions>`, `<context>`).
