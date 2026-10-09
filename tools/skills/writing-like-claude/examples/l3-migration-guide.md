# Migrating from Claude Haiku 4.5 to Claude Haiku 5.5

*This guide covers upgrading to Claude Haiku 5.5, including new model identifiers, pricing changes, request payload modifications, and parameter compatibility.*

---

## 1. Model Identifiers & Cost Comparison

Claude Haiku 5.5 is available via the Messages API. The table below compares identifiers and pricing between Haiku 4.5 and Haiku 5.5:

| Model Tier | API Model Identifier | Input / MTok | Output / MTok | Prompt Cache Reads / MTok |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Haiku 4.5** | `claude-3-haiku-20240307` | \$0.25 | \$1.25 | \$0.025 |
| **Claude Haiku 5.5** | `claude-haiku-5-5-20261001` | \$0.07 | \$0.35 | \$0.007 |

On average, Haiku 5.5 operates at approximately 72% lower token cost while delivering higher accuracy across coding, computer use, and summarization benchmarks.

---

## 2. Breaking Changes & Parameter Modifications

| Parameter | Haiku 4.5 Behavior | Haiku 5.5 Behavior | Developer Action |
| :--- | :--- | :--- | :--- |
| `max_tokens` maximum | 4,096 tokens | 8,192 tokens | Can request up to 8k tokens in single completion responses. |
| `effort` setting | Unsupported (errors if passed) | Supported: `low`, `medium`, `high`, `max` | Optional: control inference reasoning budget per request. |
| XML tag parsing | Relaxed tag matching | Strict XML boundary adherence | Ensure opening and closing prompt tags match (`<input>...</input>`). |

---

## 3. Request Payload Before & After

### Before: Haiku 4.5 Request Payload
```json
{
  "model": "claude-3-haiku-20240307",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Parse this transaction record: TXN_98124_APPROVED_USD_450"
    }
  ]
}
```

### After: Haiku 5.5 Request Payload
```json
{
  "model": "claude-haiku-5-5-20261001",
  "max_tokens": 2048,
  "effort": "low",
  "messages": [
    {
      "role": "user",
      "content": "Parse this transaction record: TXN_98124_APPROVED_USD_450"
    }
  ]
}
```

---

## 4. Python SDK Implementation

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-haiku-5-5-20261001",
    max_tokens=2048,
    effort="low",
    messages=[
        {"role": "user", "content": "Extract customer attributes from billing payload."}
    ]
)

print(response.content[0].text)
```

---

## 5. Migration Checklist

- [ ] Update API model string to `claude-haiku-5-5-20261001`.
- [ ] Add `effort: "low"` to speed-sensitive or high-volume endpoints to minimize latency.
- [ ] Test edge cases where prompt schemas rely on malformed XML tags.
- [ ] Verify rate-limit backoff logic handles HTTP 429 status codes during high-volume spikes.
