/**
 * Configuration manager for LocalSend MCP server.
 */

import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type { LocalSendConfig } from "./types.js";
import { DEFAULT_MCP_PORT } from "./types.js";
import { ensureTlsMaterial, getCertDirectory } from "./tls.js";
import { randomFingerprint } from "./net.js";

let currentConfig: LocalSendConfig | null = null;

export function getConfigFile(): string {
  return path.join(getCertDirectory(), "config.json");
}

export function getDefaultConfig(): LocalSendConfig {
  const hostname = os.hostname();
  const tls = ensureTlsMaterial();
  const home = process.env.USERPROFILE || process.env.HOME || os.homedir();
  const downloadDir = path.join(home, "Downloads");

  return {
    alias: `Antigravity on ${hostname}`,
    deviceModel: "Antigravity Agent",
    deviceType: "desktop",
    port: DEFAULT_MCP_PORT,
    protocol: "https",
    fingerprint: tls?.fingerprint || randomFingerprint(),
    downloadDir,
  };
}

export function loadConfig(): LocalSendConfig {
  if (currentConfig) return currentConfig;

  const defaults = getDefaultConfig();
  const file = getConfigFile();

  try {
    if (fs.existsSync(file)) {
      const parsed = JSON.parse(fs.readFileSync(file, "utf-8"));
      currentConfig = { ...defaults, ...parsed };
      return currentConfig!;
    }
  } catch (err) {
    console.error("Warning: could not read localsend config, using defaults:", err);
  }

  currentConfig = defaults;
  return currentConfig;
}

export function saveConfig(updates: Partial<LocalSendConfig>): LocalSendConfig {
  const config = { ...loadConfig(), ...updates };
  const file = getConfigFile();

  try {
    const dir = path.dirname(file);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    }
    fs.writeFileSync(file, JSON.stringify(config, null, 2), "utf-8");
  } catch (err) {
    console.error("Warning: could not write localsend config:", err);
  }

  currentConfig = config;
  return currentConfig;
}
