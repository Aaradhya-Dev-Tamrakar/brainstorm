/**
 * TLS material management for LocalSend mTLS.
 *
 * Caches a self-signed client & server X.509 certificate in ~/.localsend-mcp/
 * and exposes its SHA-256 fingerprint for protocol identity verification.
 */

import * as crypto from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { generateSelfSignedCertificate } from "./x509.js";

const VALIDITY_DAYS = 365;
const RENEW_BEFORE_MS = 14 * 24 * 60 * 60 * 1000;

export interface TlsMaterial {
  readonly cert: string;
  readonly key: string;
  readonly fingerprint: string;
}

export function getCertDirectory(): string {
  const home = process.env.USERPROFILE || process.env.HOME || os.homedir();
  return path.join(home, ".localsend-mcp");
}

export function certificateFingerprint(certPem: string): string {
  const der = new crypto.X509Certificate(certPem).raw;
  return crypto.createHash("sha256").update(der).digest("hex");
}

export function isUsableCertificate(certPem: string): boolean {
  try {
    const parsed = new crypto.X509Certificate(certPem);

    if (parsed.ca) return false;
    if (!parsed.subjectAltName) return false;

    const expiry = Date.parse(parsed.validTo);
    if (Number.isNaN(expiry) || expiry - Date.now() < RENEW_BEFORE_MS) return false;

    const usage = parsed.keyUsage ?? [];
    if (usage.length > 0 && !usage.includes("1.3.6.1.5.5.7.3.2")) return false;

    return true;
  } catch {
    return false;
  }
}

export function ensureTlsMaterial(): TlsMaterial | null {
  const dir = getCertDirectory();
  const certPath = path.join(dir, "cert.pem");
  const keyPath = path.join(dir, "key.pem");

  try {
    if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
      const cert = fs.readFileSync(certPath, "utf-8");
      const key = fs.readFileSync(keyPath, "utf-8");
      if (isUsableCertificate(cert)) {
        return { cert, key, fingerprint: certificateFingerprint(cert) };
      }
    }
  } catch {
    // Regenerate if unreadable or corrupted
  }

  try {
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });

    const generated = generateSelfSignedCertificate({ validityDays: VALIDITY_DAYS });
    fs.writeFileSync(keyPath, generated.key, { encoding: "utf-8", mode: 0o600 });
    fs.writeFileSync(certPath, generated.cert, { encoding: "utf-8", mode: 0o644 });

    return {
      cert: generated.cert,
      key: generated.key,
      fingerprint: certificateFingerprint(generated.cert),
    };
  } catch (err) {
    console.error("Failed to generate or save TLS material:", err);
    return null;
  }
}
