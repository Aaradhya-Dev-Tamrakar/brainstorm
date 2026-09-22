/**
 * Tool definitions and execution handlers for LocalSend MCP Server.
 */

import * as fs from "node:fs";
import * as path from "node:path";
import type { LocalSendConfig, Payload, Peer } from "./types.js";
import { DEFAULT_PORT, PeerNotFoundError } from "./types.js";
import { discoverPeers, findPeer } from "./discovery.js";
import { sendFiles } from "./client.js";
import { expandPath, formatBytes, localAddresses } from "./net.js";
import { saveConfig } from "./config.js";
import type { LocalSendServer } from "./server.js";

const MAX_FILES = 100;

function isHostAddress(val: string): boolean {
  return /^\d{1,3}(\.\d{1,3}){3}$/.test(val) || /^[a-z0-9-]+\.local$/i.test(val);
}

function collectPayloads(paths: ReadonlyArray<string>): Payload[] {
  const payloads: Payload[] = [];

  for (const raw of paths) {
    const resolved = expandPath(raw);
    let stat: fs.Stats;
    try {
      stat = fs.statSync(resolved);
    } catch {
      throw new Error(`File not found: ${resolved}`);
    }

    if (stat.isDirectory()) {
      const entries = fs.readdirSync(resolved, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isFile()) continue;
        const childPath = path.join(resolved, entry.name);
        const childStat = fs.statSync(childPath);
        payloads.push({
          fileName: entry.name,
          path: childPath,
          size: childStat.size,
          modified: childStat.mtime.toISOString(),
        });
      }
      continue;
    }

    payloads.push({
      fileName: path.basename(resolved),
      path: resolved,
      size: stat.size,
      modified: stat.mtime.toISOString(),
    });
  }

  return payloads;
}

export const TOOLS = [
  {
    name: "localsend_devices",
    description: "Scan the local Wi-Fi/LAN for active LocalSend devices and list their aliases, IPs, and models.",
    inputSchema: {
      type: "object",
      properties: {
        timeoutSeconds: {
          type: "number",
          description: "How many seconds to scan for LAN devices. Default 3, max 30.",
          default: 3,
        },
      },
    },
  },
  {
    name: "localsend_send",
    description: "Send files, folders, or direct text/clipboard snippets to a LocalSend device on LAN by alias or IP.",
    inputSchema: {
      type: "object",
      required: ["to"],
      properties: {
        to: {
          type: "string",
          description: "Target device alias (e.g. 'SFG16' or 'iPhone') or IP address (e.g. '192.168.1.11').",
        },
        files: {
          type: "array",
          items: { type: "string" },
          description: "List of absolute or relative file or folder paths to send.",
        },
        text: {
          type: "string",
          description: "Text snippet, note, or code to send directly as a text transfer.",
        },
        textFileName: {
          type: "string",
          description: "Optional filename for text snippet (default: 'note.txt').",
        },
        pin: {
          type: "string",
          description: "PIN if requested by receiving device.",
        },
        port: {
          type: "number",
          description: "Custom port if sending directly to IP (default 53317).",
        },
        protocol: {
          type: "string",
          enum: ["https", "http"],
          description: "Transport protocol (default: 'https').",
        },
        timeoutSeconds: {
          type: "number",
          description: "Timeout waiting for recipient to accept in seconds (default 60).",
        },
      },
    },
  },
  {
    name: "localsend_status",
    description: "Inspect local network addresses, active MCP listening port, certificate fingerprint, and inbox status.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "localsend_history",
    description: "List incoming files received by the LocalSend MCP server inbox.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "localsend_setup",
    description: "Update LocalSend MCP server configuration (alias, download directory, or transport).",
    inputSchema: {
      type: "object",
      properties: {
        alias: {
          type: "string",
          description: "New broadcast alias for the AI agent (e.g. 'Antigravity Agent').",
        },
        downloadDir: {
          type: "string",
          description: "Directory path where incoming files are automatically saved.",
        },
      },
    },
  },
];

export async function handleToolCall(
  name: string,
  args: any,
  config: LocalSendConfig,
  server: LocalSendServer,
): Promise<{ content: Array<{ type: string; text: string }>; isError?: boolean }> {
  try {
    switch (name) {
      case "localsend_devices": {
        const timeoutSeconds = Math.min(Math.max(args?.timeoutSeconds ?? 3, 1), 30);
        const result = await discoverPeers(config, {
          timeoutMs: timeoutSeconds * 1000,
          listenPort: server.port,
        });

        if (result.peers.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: `No LocalSend devices responded within ${timeoutSeconds}s.\nMake sure LocalSend is open on target devices on the same Wi-Fi network.`,
              },
            ],
          };
        }

        const lines = [
          `Found ${result.peers.length} LocalSend device(s) on LAN:`,
          "",
          ...result.peers.map((p) => {
            const dev = p.deviceModel ? ` (${p.deviceModel})` : "";
            return `* **${p.alias}**${dev}\n  - Address: \`${p.host}:${p.port}\` [${p.protocol}]\n  - Fingerprint: \`${p.fingerprint.slice(0, 16)}...\``;
          }),
        ];

        if (result.warnings.length > 0) {
          lines.push("", "Notes:", ...result.warnings.map((w) => `* ${w}`));
        }

        return { content: [{ type: "text", text: lines.join("\n") }] };
      }

      case "localsend_send": {
        const to = String(args?.to || "").trim();
        if (!to) {
          throw new Error("Missing required parameter: 'to'");
        }

        const filesInput: string[] = Array.isArray(args?.files) ? args.files : [];
        const textInput: string | undefined = args?.text;

        if (filesInput.length === 0 && !textInput) {
          throw new Error("Nothing to send: specify 'files', 'text', or both.");
        }

        const payloads: Payload[] = collectPayloads(filesInput);
        if (textInput) {
          const buf = Buffer.from(textInput, "utf-8");
          payloads.push({
            fileName: args?.textFileName?.trim() || "note.txt",
            content: buf,
            size: buf.length,
            fileType: "text/plain",
          });
        }

        if (payloads.length > MAX_FILES) {
          throw new Error(`Exceeded max file limit of ${MAX_FILES}.`);
        }

        let peer: Peer;
        if (isHostAddress(to)) {
          peer = {
            alias: to,
            host: to,
            port: args?.port ?? DEFAULT_PORT,
            protocol: args?.protocol ?? "https",
            fingerprint: "",
          };
        } else {
          const outcome = await discoverPeers(config, {
            timeoutMs: 3000,
            listenPort: server.port,
          });
          const match = findPeer(outcome.peers, to);
          if (!match) {
            throw new PeerNotFoundError(to);
          }
          peer = match;
        }

        const result = await sendFiles(config, {
          peer,
          payloads,
          pin: args?.pin,
        });

        const totalBytes = payloads.reduce((acc, p) => acc + p.size, 0);
        const okFiles = result.files.filter((f) => f.ok);
        const failedFiles = result.files.filter((f) => !f.ok);

        const summary = [
          `Transfer Complete to **${peer.alias}** (\`${peer.host}:${peer.port}\`):`,
          `* Sent: ${okFiles.length}/${result.files.length} items (${formatBytes(result.bytesSent)} / ${formatBytes(totalBytes)})`,
          `* Session ID: \`${result.sessionId}\``,
        ];

        if (okFiles.length > 0) {
          summary.push("", "Files delivered:", ...okFiles.map((f) => `  - ${f.fileName} (${formatBytes(f.size)})`));
        }

        if (failedFiles.length > 0) {
          summary.push("", "Failed items:", ...failedFiles.map((f) => `  - ${f.fileName}: ${f.error}`));
        }

        return { content: [{ type: "text", text: summary.join("\n") }] };
      }

      case "localsend_status": {
        const ips = localAddresses();
        const historyCount = server.history.length;
        const text = [
          "**LocalSend MCP Server Status**",
          "",
          `* **Agent Alias**: "${config.alias}"`,
          `* **Active Listening Port**: ${server.port} [${config.protocol}]`,
          `* **Device Fingerprint**: \`${config.fingerprint}\``,
          `* **Auto-Save Inbox**: \`${config.downloadDir}\``,
          `* **Total Files Received**: ${historyCount}`,
          `* **Local LAN IP(s)**:`,
          ...ips.map((ip) => `  - \`${ip}\``),
          "",
          "LocalSend desktop apps can add this agent to Favorites without connection errors.",
        ].join("\n");

        return { content: [{ type: "text", text }] };
      }

      case "localsend_history": {
        const history = server.history;
        if (history.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: "No incoming files have been received by the MCP server yet.",
              },
            ],
          };
        }

        const lines = [
          `**Received Files (${history.length}):**`,
          "",
          ...history.map(
            (item, i) =>
              `${i + 1}. **${item.fileName}** (${formatBytes(item.size)}) from *${item.sender}*\n   Saved at: \`${item.savedPath}\`\n   Received: ${item.timestamp}`,
          ),
        ];

        return { content: [{ type: "text", text: lines.join("\n") }] };
      }

      case "localsend_setup": {
        const updates: Partial<LocalSendConfig> = {};
        if (args?.alias) updates.alias = String(args.alias).trim();
        if (args?.downloadDir) updates.downloadDir = expandPath(String(args.downloadDir));

        const updated = saveConfig(updates);
        return {
          content: [
            {
              type: "text",
              text: `Configuration updated successfully:\n* Alias: "${updated.alias}"\n* Download Directory: \`${updated.downloadDir}\``,
            },
          ],
        };
      }

      default:
        return {
          content: [{ type: "text", text: `Unknown tool: ${name}` }],
          isError: true,
        };
    }
  } catch (err: any) {
    return {
      content: [{ type: "text", text: `LocalSend Error: ${err.message}` }],
      isError: true,
    };
  }
}
