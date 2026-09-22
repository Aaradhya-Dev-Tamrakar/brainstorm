/**
 * Network and filesystem helpers for LocalSend MCP.
 */

import * as crypto from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

export function localAddresses(): string[] {
  const found: string[] = [];
  const interfaces = os.networkInterfaces();
  for (const entries of Object.values(interfaces)) {
    for (const entry of entries ?? []) {
      if (entry.family === "IPv4" && !entry.internal) {
        found.push(entry.address);
      }
    }
  }
  return found;
}

export function randomFingerprint(): string {
  return crypto.randomBytes(32).toString("hex");
}

export function generatePin(): string {
  return String(crypto.randomInt(0, 1000000)).padStart(6, "0");
}

export function randomId(): string {
  return crypto.randomUUID();
}

export function safeFileName(raw: string): string {
  const withoutDirs =
    String(raw ?? "")
      .replace(/\\/g, "/")
      .split("/")
      .pop() ?? "";

  const cleaned = withoutDirs
    .replace(/[\x00-\x1f\x7f]/g, "")
    .replace(/^\.+$/, "")
    .trim();

  if (!cleaned || cleaned === "." || cleaned === "..") {
    return `file-${Date.now()}`;
  }
  if (cleaned.length > 200) {
    const ext = path.extname(cleaned).slice(0, 20);
    return cleaned.slice(0, 200 - ext.length) + ext;
  }
  return cleaned;
}

export function uniquePath(dir: string, fileName: string): string {
  const safe = safeFileName(fileName);
  const targetDir = path.resolve(dir);
  const base = path.basename(safe, path.extname(safe));
  const ext = path.extname(safe);

  let candidate = path.resolve(targetDir, safe);
  let counter = 2;
  while (fs.existsSync(candidate)) {
    candidate = path.resolve(targetDir, `${base} (${counter})${ext}`);
    counter += 1;
    if (counter > 1000) {
      throw new Error(`Too many duplicate files in ${targetDir}`);
    }
  }
  return candidate;
}

const MIME_BY_EXTENSION: Record<string, string> = {
  ".txt": "text/plain",
  ".md": "text/markdown",
  ".json": "application/json",
  ".csv": "text/csv",
  ".html": "text/html",
  ".css": "text/css",
  ".js": "text/javascript",
  ".ts": "text/plain",
  ".pdf": "application/pdf",
  ".zip": "application/zip",
  ".gz": "application/gzip",
  ".tar": "application/x-tar",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".mp3": "audio/mpeg",
  ".wav": "audio/wav",
  ".m4a": "audio/mp4",
  ".mp4": "video/mp4",
  ".mov": "video/quicktime",
  ".webm": "video/webm",
  ".doc": "application/msword",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xls": "application/vnd.ms-excel",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".ppt": "application/vnd.ms-powerpoint",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
};

export function guessFileType(fileName: string): string {
  return MIME_BY_EXTENSION[path.extname(fileName).toLowerCase()] ?? "application/octet-stream";
}

export function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) return "0 B";
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(value >= 10 ? 0 : 1)} ${units[unit]}`;
}

export function expandPath(input: string): string {
  const raw = String(input ?? "").trim();
  if (raw === "~") return os.homedir();
  if (raw.startsWith("~/") || raw.startsWith("~\\")) {
    return path.join(os.homedir(), raw.slice(2));
  }
  return path.resolve(raw);
}
