#!/usr/bin/env python3
"""
Continuous Google Drive Synchronization Engine for Repository Documentation.
Updates living Markdown files in Google Drive folder preserving permanent fileIds.
Zero third-party dependencies — uses Python standard library urllib.
"""

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
DRIVE_UPLOAD_ENDPOINT = "https://www.googleapis.com/upload/drive/v3/files"
DRIVE_FILES_ENDPOINT = "https://www.googleapis.com/drive/v3/files"


def request_with_retry(
    req: urllib.request.Request,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Tuple[int, bytes]:
    """Executes urllib request with exponential backoff and jitter for transient HTTP errors."""
    last_err: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            body = e.read()
            last_err = e
            # Retry on 429 (rate limit) or 5xx (transient Google server errors)
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                sleep_time = initial_delay * (backoff_factor ** attempt) + random.uniform(0.1, 0.5)
                print(f"[RETRY] HTTP {e.code}. Retrying in {sleep_time:.2f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(sleep_time)
                continue
            raise urllib.error.HTTPError(e.url, e.code, body.decode("utf-8", errors="replace"), e.hdrs, None)
        except urllib.error.URLError as e:
            last_err = e
            if attempt < max_retries - 1:
                sleep_time = initial_delay * (backoff_factor ** attempt) + random.uniform(0.1, 0.5)
                print(f"[RETRY] Network error: {e.reason}. Retrying in {sleep_time:.2f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(sleep_time)
                continue
            raise

    if last_err:
        raise last_err
    raise RuntimeError("Unexpected request failure without error.")


def get_oauth_credentials() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Resolves OAuth credentials from environment variables or local credential files."""
    client_id = os.environ.get("GDRIVE_CLIENT_ID")
    client_secret = os.environ.get("GDRIVE_CLIENT_SECRET")
    refresh_token = os.environ.get("GDRIVE_REFRESH_TOKEN")

    if not (client_id and client_secret) and os.environ.get("GDRIVE_CLIENT_SECRET_JSON"):
        try:
            raw = json.loads(os.environ["GDRIVE_CLIENT_SECRET_JSON"])
            inst = raw.get("installed") or raw.get("web") or raw
            client_id = inst.get("client_id")
            client_secret = inst.get("client_secret")
        except Exception as e:
            print(f"[WARN] Failed to parse GDRIVE_CLIENT_SECRET_JSON: {e}")

    # Fallback to local credential files if environment variables are not set
    if not (client_id and client_secret):
        oauth_path = os.environ.get("GDRIVE_OAUTH_PATH") or os.path.expanduser("~/.gdrive-credentials.json")
        if os.path.exists(oauth_path):
            try:
                with open(oauth_path, "r", encoding="utf-8") as f:
                    oauth = json.load(f)
                    keys = oauth.get("installed") or oauth.get("web") or oauth
                    client_id = keys.get("client_id")
                    client_secret = keys.get("client_secret")
            except Exception as e:
                print(f"[WARN] Failed to read local OAuth credentials from {oauth_path}: {e}")

    if not refresh_token:
        creds_path = os.environ.get("GDRIVE_CREDENTIALS_PATH") or os.path.expanduser("~/.gdrive-server-credentials.json")
        if os.path.exists(creds_path):
            try:
                with open(creds_path, "r", encoding="utf-8") as f:
                    creds = json.load(f)
                    refresh_token = creds.get("refresh_token")
            except Exception as e:
                print(f"[WARN] Failed to read local server credentials from {creds_path}: {e}")

    return client_id, client_secret, refresh_token


def obtain_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    """Exchanges refresh token for a fresh Google OAuth2 access token with retry."""
    payload = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")

    req = urllib.request.Request(TOKEN_ENDPOINT, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        status, body_bytes = request_with_retry(req)
        data = json.loads(body_bytes.decode("utf-8"))
        return data["access_token"]
    except Exception as e:
        print(f"[ERROR] Failed to obtain access token: {e}")
        raise


def find_drive_file_by_name(access_token: str, folder_id: str, file_name: str) -> Optional[str]:
    """Checks if a file with the given name already exists in the target folder."""
    safe_name = file_name.replace("'", "\\'")
    query = f"'{folder_id}' in parents and name = '{safe_name}' and trashed = false"
    url = f"{DRIVE_FILES_ENDPOINT}?q={urllib.parse.quote(query)}&fields=files(id,name,mimeType)"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        status, body_bytes = request_with_retry(req)
        data = json.loads(body_bytes.decode("utf-8"))
        files = data.get("files", [])
        if files:
            return files[0]["id"]
    except Exception as e:
        print(f"[WARN] Could not query Drive files: {e}")
    return None


def update_drive_file(access_token: str, file_id: str, content_bytes: bytes, mime_type: str = "text/plain") -> bool:
    """Updates an existing Google Drive file in-place preserving its permanent fileId."""
    url = f"{DRIVE_UPLOAD_ENDPOINT}/{file_id}?uploadType=media"
    req = urllib.request.Request(url, data=content_bytes, method="PATCH")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", f"{mime_type}; charset=utf-8")

    try:
        status, _ = request_with_retry(req)
        return status in (200, 201)
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Drive PATCH failed ({e.code}): {e.msg}")
        return False
    except Exception as e:
        print(f"[ERROR] Drive PATCH failed: {e}")
        return False


def create_drive_file(
    access_token: str,
    folder_id: str,
    file_name: str,
    content_bytes: bytes,
    mime_type: str = "text/plain",
    convert_to_doc: bool = True
) -> str:
    """Creates a new file inside the specified Drive folder and returns its permanent fileId.
    Converts to Google Doc by default for native NotebookLM Drive integration.
    """
    boundary = "-------314159265358979323846"
    metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    if convert_to_doc:
        metadata["mimeType"] = "application/vnd.google-apps.document"

    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mime_type}; charset=utf-8\r\n\r\n"
    ).encode("utf-8") + content_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"{DRIVE_UPLOAD_ENDPOINT}?uploadType=multipart"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")

    try:
        status, body_bytes = request_with_retry(req)
        res_data = json.loads(body_bytes.decode("utf-8"))
        return res_data["id"]
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Drive POST multipart failed ({e.code}): {e.msg}")
        raise
    except Exception as e:
        print(f"[ERROR] Drive POST multipart failed: {e}")
        raise


def sync_notebooklm_sources(notebook_id: str) -> bool:
    """Triggers Super-NLM / nlm CLI sync on stale Drive sources if available."""
    nlm_bin = shutil.which("nlm")
    if not nlm_bin:
        home_dir = Path.home()
        fallback = home_dir / ".local" / "bin" / ("nlm.exe" if sys.platform == "win32" else "nlm")
        if fallback.exists():
            nlm_bin = str(fallback)

    if not nlm_bin:
        print("[NOTEBOOKLM] nlm CLI executable not found, skipping NotebookLM delta sync.")
        return False

    print(f"[NOTEBOOKLM] Triggering source sync for notebook {notebook_id}...")
    try:
        res = subprocess.run(
            [str(nlm_bin), "source", "sync", notebook_id, "--confirm"],
            capture_output=True,
            text=True,
            timeout=120
        )
        out = (res.stdout or res.stderr or "").strip()
        print(f"[NOTEBOOKLM] Sync output: {out}")
        return res.returncode == 0
    except Exception as e:
        print(f"[NOTEBOOKLM] Sync invocation failed: {e}")
        return False


def sync_manifest(
    manifest_path: Path,
    dry_run: bool = False,
    target_file_filter: Optional[str] = None,
    sync_nlm: bool = False,
    force: bool = False
) -> int:
    """Processes the manifest, updating or creating Drive documents."""
    if not manifest_path.exists():
        print(f"[ERROR] Manifest not found: {manifest_path}")
        return 1

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    folder_id = manifest.get("folder_id")
    notebook_id = manifest.get("notebook_id")
    files_map = manifest.get("files", {})
    repo_root = manifest_path.parent

    # Normalize target filter for cross-platform matching (e.g. windows backslashes)
    target_norm = Path(target_file_filter).as_posix().lstrip("./") if target_file_filter else None

    print("=== Google Drive Real-Time Sync ===")
    print(f"Target Folder: {folder_id}")
    print(f"Notebook ID:   {notebook_id}")
    print(f"Tracked Files: {len(files_map)}")
    print(f"Mode:          {'DRY-RUN (Preview Only)' if dry_run else 'LIVE SYNC'}")
    if target_norm:
        print(f"File Filter:   {target_norm}")
    print("-----------------------------------")

    matched_filter = False
    if dry_run:
        for rel_path, meta in files_map.items():
            rel_norm = Path(rel_path).as_posix().lstrip("./")
            if target_norm and rel_norm != target_norm:
                continue
            matched_filter = True
            local_path = repo_root / rel_path
            status = "EXISTS" if local_path.exists() else "MISSING"
            drive_id = meta.get("drive_file_id") or "[NEW FILE NEEDED]"
            print(f"[{status}] {rel_path} -> {meta.get('drive_file_name')} (ID: {drive_id})")

        if target_norm and not matched_filter:
            print(f"[ERROR] Target file filter '{target_file_filter}' matched no tracked files in manifest.")
            return 1
        return 0

    client_id, client_secret, refresh_token = get_oauth_credentials()
    missing_creds = []
    if not client_id:
        missing_creds.append("GDRIVE_CLIENT_ID")
    if not client_secret:
        missing_creds.append("GDRIVE_CLIENT_SECRET")
    if not refresh_token:
        missing_creds.append("GDRIVE_REFRESH_TOKEN")

    if missing_creds:
        print(f"[ERROR] Missing OAuth credentials: {', '.join(missing_creds)}")
        print("Please configure environment variables or local credential files.")
        return 1

    access_token = obtain_access_token(client_id, client_secret, refresh_token)
    print("[AUTH] Google OAuth2 access token verified.")

    manifest_modified = False
    success_count = 0
    failure_count = 0

    for rel_path, meta in files_map.items():
        rel_norm = Path(rel_path).as_posix().lstrip("./")
        if target_norm and rel_norm != target_norm:
            continue

        matched_filter = True
        local_path = repo_root / rel_path
        if not local_path.exists():
            print(f"[ERROR] Local tracked file missing: {rel_path}")
            failure_count += 1
            continue

        with open(local_path, "rb") as f:
            raw_bytes = f.read()

        # Deterministic cross-platform normalization: CRLF -> LF
        content_bytes = raw_bytes.replace(b"\r\n", b"\n")
        content_hash = hashlib.sha256(content_bytes).hexdigest()[:16]
        last_hash = meta.get("sha256")
        file_id = meta.get("drive_file_id")
        doc_name = meta.get("drive_file_name") or local_path.name

        # If file_id is missing from manifest, check if it already exists in Drive folder
        if not file_id:
            existing_id = find_drive_file_by_name(access_token, folder_id, doc_name)
            if existing_id:
                print(f"[ADOPT] Found existing Drive file for {doc_name} -> {existing_id}")
                file_id = existing_id
                meta["drive_file_id"] = file_id
                manifest_modified = True

        if file_id:
            if not force and last_hash == content_hash:
                print(f"[UNCHANGED] {rel_path} (ID: {file_id})")
                success_count += 1
                continue

            print(f"[UPDATE] {rel_path} -> Drive ID: {file_id}...", end=" ", flush=True)
            ok = update_drive_file(access_token, file_id, content_bytes)
            if ok:
                print("DONE (200 OK)")
                meta["sha256"] = content_hash
                manifest_modified = True
                success_count += 1
            else:
                print("FAILED")
                failure_count += 1
        else:
            print(f"[CREATE] {rel_path} -> {doc_name} in folder {folder_id}...", end=" ", flush=True)
            try:
                new_id = create_drive_file(access_token, folder_id, doc_name, content_bytes, convert_to_doc=True)
                print(f"CREATED (ID: {new_id})")
                meta["drive_file_id"] = new_id
                meta["sha256"] = content_hash
                manifest_modified = True
                success_count += 1
            except Exception as e:
                print(f"FAILED: {e}")
                failure_count += 1

    if target_norm and not matched_filter:
        print(f"[ERROR] Target file filter '{target_file_filter}' matched no tracked files in manifest.")
        return 1

    if manifest_modified:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"[MANIFEST] Updated {manifest_path.name} with permanent Drive File IDs and hashes.")

    print("-----------------------------------")
    print(f"Sync completed: {success_count} file(s) successful, {failure_count} failure(s).")

    if sync_nlm and notebook_id:
        sync_notebooklm_sources(notebook_id)

    if failure_count > 0:
        print(f"[ERROR] Synchronization encountered {failure_count} failure(s).")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="Continuous Google Drive Synchronization Engine")
    parser.add_argument("--manifest", default="drive-manifest.json", help="Path to manifest JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying Drive")
    parser.add_argument("--file", help="Filter sync to a single relative file path")
    parser.add_argument("--sync-notebook", action="store_true", help="Trigger NotebookLM source sync after Drive sync")
    parser.add_argument("--force", action="store_true", help="Force re-upload of all files regardless of hash")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    sys.exit(sync_manifest(
        manifest_path,
        dry_run=args.dry_run,
        target_file_filter=args.file,
        sync_nlm=args.sync_notebook,
        force=args.force
    ))


if __name__ == "__main__":
    main()

