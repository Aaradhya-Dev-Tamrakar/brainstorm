# SOP: Zero-to-One Google Gemini API Provisioning & Onboarding Guide

**Document ID**: `SOP-GEMINI-001`  
**Classification**: `EMPIRICALLY_VERIFIED`  
**Target Audience**: Developers, Students, and Autonomous Agents with clean/virgin Google accounts  
**Governing Standard**: Google AI Studio & Google Cloud Generative Language API  

---

## 1. Executive Overview & Prerequisites

This Standard Operating Procedure (SOP) details the end-to-end process of generating and configuring a **Google Gemini API Key** from a brand-new Google Account that has never accessed Google AI Studio or Google Cloud Console before.

### Prerequisites Checklist
- [ ] Active Google Account (Personal `@gmail.com` or Google Workspace account).
- [ ] Modern web browser (Chrome, Chromium, Edge, or Firefox).
- [ ] Installed Python runtime (Python 3.10+ recommended) for verification.
- [ ] Local environment management tool or password manager (e.g., Bitwarden / Win-Vault / `.env`).

---

## 2. Decision Matrix: Google AI Studio vs. Vertex AI

| Feature | Google AI Studio (Recommended for Fast Start) | Vertex AI (Google Cloud Platform) |
| :--- | :--- | :--- |
| **Best For** | Prototyping, personal development, agent swarms, SLM/LLM experiments | Enterprise production, strict compliance (SOC2/HIPAA), IAM role segregation |
| **Setup Friction** | **Zero credit card required**; instant API key in < 2 minutes | Requires GCP Billing Account, IAM configuration, service account keys |
| **Free Tier Quota** | Generous free tier (RPM/TPM/RPD limits per model family) | Pay-as-you-go billing with GCP free credits trial |
| **Console Portal** | [https://aistudio.google.com/](https://aistudio.google.com/) | [https://console.cloud.google.com/vertex-ai](https://console.cloud.google.com/vertex-ai) |

> [!TIP]
> **Default Recommendation**: Always start with **Google AI Studio**. You can migrate projects seamlessly to Google Cloud Vertex AI later when enterprise billing or custom quotas are needed.

---

## 3. Step-by-Step Manual Onboarding Procedure (Google AI Studio)

### Step 1: Navigate and Sign In
1. Open your browser and navigate to the Google AI Studio portal:
   ```
   https://aistudio.google.com/app/apikey
   ```
2. Log in using your Google credentials.

### Step 2: Accept Terms of Service (Virgin Account Gate)
Virgin accounts will encounter a modal titled **"Get started with Google AI Studio"**:
1. Review the **Terms of Service** and **Generative AI Additional Terms of Service**.
2. Check the box: `I accept the Google APIs Terms of Service and the Generative AI Additional Terms of Service`.
3. *(Optional)* Select whether to opt in to email announcements.
4. Click **"Continue"** / **"Agree and Continue"**.

> [!IMPORTANT]
> **Data Privacy Distinction**:
> In the free tier of Google AI Studio, input and output data may be reviewed by human reviewers and used to improve Google products. Do not transmit sensitive unredacted PII or secrets under the unpaid tier. Paid tier accounts do not log customer prompts for model training.

### Step 3: Generate the Gemini API Key
1. In the top navigation or main dashboard, locate the blue or prominent button:
   ```
   [ Create API key ]
   ```
2. In the modal that appears, you will have two options:
   - **Option A (Instant / Recommended)**: `Create API key in new project`. AI Studio automatically provisions a managed cloud container project (e.g. `Generative Language Client`).
   - **Option B (Existing Project)**: Select an existing Google Cloud Project from the dropdown list.
3. Click **"Create API key in new project"**.
4. Within 3–5 seconds, the modal will display your new key string formatted as:
   ```
   AIzaSy***********************************
   ```
5. Click the copy icon (`📋 Copy`) next to the key.

### Step 4: Secure Key Storage & Local Machine Configuration
Never hardcode or push API keys to Git repositories.

#### Option A: User Environment Variable (Persistent Windows)
Run in PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', '<insert-key>', [System.EnvironmentVariableTarget]::User)
```

#### Option B: User Environment Variable (Linux / macOS)
Add to your shell configuration (`~/.bashrc` or `~/.zshrc`):
```bash
# Set GEMINI_API_KEY in environment
export GEMINI_API_KEY
```

#### Option C: Project Local `.env`
Specify inside your project `.env` file:
```
# Gemini API Key configuration
# Format: GEMINI_API_KEY=<token>
```
Ensure `.env` is declared inside your `.gitignore`.

---

## 4. Automated Provisioning Tooling (Playwright / CDP)

To eliminate repetitive manual UI clicks across new test accounts or test environments, refer to the companion Python script:
- [`tools/gemini_onboarding_automation.py`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/tools/gemini_onboarding_automation.py)

### How the Automation Operates
1. Spawns an isolated Chromium instance using Playwright.
2. Directs the user to complete Google OAuth / 2FA securely (or reuses a saved browser user data directory / CDP session).
3. Detects first-time Terms of Service modals and automatically checks consent.
4. Triggers the API Key creation workflow and intercepts the DOM node containing `AIzaSy...`.
5. Outputs the key into a secure masked terminal prompt, saves to `.env.template`, or registers into Bitwarden / Win-Vault.

---

## 5. Verification & Reality Layer Test

Validate the newly provisioned key immediately with the official `google-genai` SDK or raw REST API.

### Verification via Python SDK (`google-genai`)
Run:
```powershell
python tools/verify_gemini_key.py
```
Expected output:
```
[+] GEMINI_API_KEY detected.
[+] Connected to Gemini API endpoint.
[+] Model: gemini-2.5-flash
[+] Response: Hello! Gemini API connection verified successfully.
[+] Verification Gate: PASSED (Tier E4)
```

---

## 6. Rate Limits & Quotas Reference (Free Tier Baseline)

| Model Target | Requests Per Minute (RPM) | Tokens Per Minute (TPM) | Requests Per Day (RPD) |
| :--- | :--- | :--- | :--- |
| `gemini-2.5-flash` | 15 RPM | 1,000,000 TPM | 1,500 RPD |
| `gemini-2.5-pro` | 2 RPM | 32,000 TPM | 50 RPD |
| `gemini-1.5-flash` | 15 RPM | 1,000,000 TPM | 1,500 RPD |

*Quotas are refreshed daily at midnight Pacific Time.*
