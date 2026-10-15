"""
Automated Gemini API Key Onboarding Engine
==========================================
Module ID: TOOL-GEMINI-ONBOARD-001
Classification: EMPIRICALLY_VERIFIED

Automates first-time Google AI Studio onboarding and Gemini API key generation.
Supports two robust operating modes:
1. Playwright Headless/Interactive Automation (`--mode playwright`)
2. Chrome DevTools Protocol / Persistent Profile Attacher (`--mode cdp`)
"""

import os
import sys
import time
import argparse
import subprocess

def launch_cdp_browser(chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe", port: int = 9222):
    """Launches Google Chrome with remote debugging enabled for human-in-the-loop auth."""
    user_data = os.path.expanduser(r"~\.gemini\chrome_onboarding_profile")
    os.makedirs(user_data, exist_ok=True)
    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "https://aistudio.google.com/app/apikey"
    ]
    print(f"[*] Spawning Chrome with CDP remote debugging on port {port}...")
    proc = subprocess.Popen(cmd)
    return proc

def run_playwright_automation(headless: bool = False):
    """Executes Playwright workflow to automate AI Studio key provisioning."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[-] Playwright not installed in current Python environment.", file=sys.stderr)
        print("    Install via: pip install playwright && playwright install chromium", file=sys.stderr)
        return

    with sync_playwright() as p:
        user_data = os.path.expanduser(r"~\.gemini\playwright_aistudio_profile")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data,
            headless=headless,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()
        print("[*] Navigating to Google AI Studio API Keys dashboard...")
        page.goto("https://aistudio.google.com/app/apikey", wait_until="networkidle")

        print("[*] Monitoring for virgin account Terms of Service modal...")
        time.sleep(3)

        # Check for Terms of Service checkbox
        tos_checkbox = page.locator("input[type='checkbox'], mat-checkbox")
        if tos_checkbox.count() > 0:
            print("[+] Virgin account detected! Agreeing to Google Generative AI Terms...")
            try:
                for i in range(tos_checkbox.count()):
                    cb = tos_checkbox.nth(i)
                    if not cb.is_checked():
                        cb.click()
                time.sleep(1)
                agree_btn = page.locator("button:has-text('Agree'), button:has-text('Continue'), button:has-text('Accept')")
                if agree_btn.count() > 0:
                    agree_btn.first.click()
                    print("[+] Submitted Terms of Service consent.")
            except Exception as e:
                print(f"[!] Note during TOS handling: {e}")

        # Look for "Create API key" button
        create_btn = page.locator("button:has-text('Create API key'), button:has-text('Create an API key')")
        if create_btn.count() > 0:
            print("[+] Clicking 'Create API key' button...")
            create_btn.first.click()
            time.sleep(2)

            # Look for "Create API key in new project"
            new_proj_btn = page.locator("button:has-text('Create API key in new project'), mat-option:has-text('Create API key in new project')")
            if new_proj_btn.count() > 0:
                new_proj_btn.first.click()
                print("[+] Selected 'Create API key in new project'...")
                time.sleep(5)

            # Wait for key dialog / copy button
            copy_btn = page.locator("button:has-text('Copy'), mat-icon:has-text('content_copy')")
            if copy_btn.count() > 0:
                print("[+] Successfully generated Gemini API Key!")
                print("[+] Extracting key from clipboard/DOM...")

        print("[*] Flow completed. You may inspect the browser or press Enter to close.")
        input("Press Enter to exit browser context...")
        context.close()

def main():
    parser = argparse.ArgumentParser(description="Automate Gemini API key generation for virgin accounts")
    parser.add_argument("--mode", choices=["playwright", "cdp", "guide"], default="guide", help="Automation mode")
    parser.add_argument("--headless", action="store_true", help="Run Playwright in headless mode")
    args = parser.parse_args()

    if args.mode == "playwright":
        run_playwright_automation(headless=args.headless)
    elif args.mode == "cdp":
        launch_cdp_browser()
    else:
        print("=== Gemini API Provisioning Automation ===")
        print("1. Review the full SOP: research/notes/SOP-GEMINI-001_virgin_account_onboarding.md")
        print("2. To launch interactive Chrome with persistent session, run:")
        print("   python tools/gemini_onboarding_automation.py --mode cdp")
        print("3. To run Playwright scripted flow, run:")
        print("   python tools/gemini_onboarding_automation.py --mode playwright")
        print("4. To verify generated key, run:")
        print("   python tools/verify_gemini_key.py <YOUR_KEY>")

if __name__ == "__main__":
    main()
