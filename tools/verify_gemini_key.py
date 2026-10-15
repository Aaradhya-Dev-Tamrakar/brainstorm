"""
Gemini Key Verification Utility (INV-VERIFY-GEMINI)
==================================================
Deterministic verification tool to validate newly provisioned Google Gemini API keys.
Compatible with google-genai SDK or fallback direct REST call.
"""

import os
import sys
import json
import urllib.request
import urllib.error

def verify_gemini_key(api_key: str | None = None) -> bool:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[-] ERROR: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("    Run: $env:GEMINI_API_KEY = '<YOUR_API_KEY>' or pass as argument.", file=sys.stderr)
        return False

    print(f"[*] Detected API key prefix: {key[:8]}... (Total length: {len(key)})")
    print("[*] Dispatching verification probe to Google Generative Language API...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Respond with single word: OK"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 10
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidate = data.get("candidates", [{}])[0]
            text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            print(f"[+] API Handshake SUCCESS: Model responded with '{text}'")
            print("[+] Verification Status: PASSED (Valid key & active generative quota)")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        try:
            parsed = json.loads(err_msg)
            print(f"    Details: {parsed.get('error', {}).get('message', err_msg)}", file=sys.stderr)
        except Exception:
            print(f"    Raw error: {err_msg}", file=sys.stderr)
        return False
    except Exception as ex:
        print(f"[-] Unexpected connection failure: {ex}", file=sys.stderr)
        return False

if __name__ == "__main__":
    cli_key = sys.argv[1] if len(sys.argv) > 1 else None
    success = verify_gemini_key(cli_key)
    sys.exit(0 if success else 1)
