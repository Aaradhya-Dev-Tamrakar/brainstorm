/**
 * UDP Multicast & HTTP Peer Discovery for LocalSend.
 *
 * LocalSend discovery protocol:
 * 1. Sender opens an HTTP(S) listener.
 * 2. Sender broadcasts UDP multicast announcement to 224.0.0.167:53317 with `announce: true`.
 * 3. Each peer that hears the broadcast sends an HTTP POST to /api/localsend/v2/register
 *    on the sender's announced port with its DeviceInfo.
 * 4. The sender collects all responses and resolves peers.
 */

import * as dgram from "node:dgram";
import * as http from "node:http";
import * as https from "node:https";
import type { AddressInfo } from "node:net";
import type { DeviceInfo, LocalSendConfig, Peer } from "./types.js";
import { API_PREFIX, DEFAULT_PORT, MULTICAST_ADDRESS, PROTOCOL_VERSION } from "./types.js";
import { ensureTlsMaterial } from "./tls.js";

export interface DiscoveryOptions {
  timeoutMs?: number;
  listenPort?: number;
  signal?: AbortSignal;
}

export interface DiscoveryResult {
  peers: Peer[];
  warnings: string[];
}

export class PeerCollector {
  private peersMap = new Map<string, Peer>();

  constructor(private ownFingerprint: string) {}

  public add(info: any, host: string): void {
    if (!info || typeof info !== "object" || !host) return;
    if (info.fingerprint && info.fingerprint === this.ownFingerprint) return;

    const alias = typeof info.alias === "string" ? info.alias : host;
    const port = typeof info.port === "number" && info.port > 0 ? info.port : DEFAULT_PORT;
    const protocol = info.protocol === "http" ? "http" : "https";

    const peer: Peer = {
      alias,
      host,
      port,
      protocol,
      fingerprint: String(info.fingerprint || ""),
      deviceModel: info.deviceModel,
      deviceType: info.deviceType,
      download: info.download,
    };

    this.peersMap.set(`${host}:${port}`, peer);
  }

  public list(): Peer[] {
    return [...this.peersMap.values()].sort((a, b) => a.alias.localeCompare(b.alias));
  }
}

function delay(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve) => {
    const timer = setTimeout(resolve, ms);
    signal?.addEventListener("abort", () => {
      clearTimeout(timer);
      resolve();
    }, { once: true });
  });
}

function normalizeRemoteAddress(address?: string | null): string {
  if (!address) return "";
  return address.startsWith("::ffff:") ? address.slice(7) : address;
}

function readJsonBody(req: http.IncomingMessage): Promise<any> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf-8")));
      } catch (e) {
        resolve(null);
      }
    });
    req.on("error", reject);
  });
}

function sendJson(res: http.ServerResponse, status: number, data: unknown): void {
  const json = JSON.stringify(data ?? {});
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(json),
    "Connection": "close",
  });
  res.end(json);
}

export async function discoverPeers(
  config: LocalSendConfig,
  options: DiscoveryOptions = {},
): Promise<DiscoveryResult> {
  const timeoutMs = options.timeoutMs ?? 3500;
  const tls = config.protocol === "https" ? ensureTlsMaterial() : null;
  const ownFingerprint = tls?.fingerprint || config.fingerprint;

  const collector = new PeerCollector(ownFingerprint);
  const warnings: string[] = [];

  let listenPort = 0;

  // 1. Temporary HTTP(S) receiver to catch /register responses
  const handler = async (req: http.IncomingMessage, res: http.ServerResponse) => {
    const url = req.url || "";
    const host = normalizeRemoteAddress(req.socket.remoteAddress);

    if (req.method === "POST" && url.startsWith(`${API_PREFIX}/register`)) {
      try {
        const body = await readJsonBody(req);
        if (body) {
          collector.add(body, host);
        }
      } catch {}
      sendJson(res, 200, {
        alias: config.alias,
        version: PROTOCOL_VERSION,
        deviceModel: config.deviceModel,
        deviceType: config.deviceType,
        fingerprint: ownFingerprint,
        port: listenPort,
        protocol: config.protocol,
        download: false,
      });
      return;
    }

    if (req.method === "GET" && url.startsWith(`${API_PREFIX}/info`)) {
      sendJson(res, 200, {
        alias: config.alias,
        version: PROTOCOL_VERSION,
        deviceModel: config.deviceModel,
        deviceType: config.deviceType,
        fingerprint: ownFingerprint,
        port: listenPort,
        protocol: config.protocol,
        download: false,
      });
      return;
    }

    sendJson(res, 404, { error: "Not found" });
  };

  const server = tls
    ? https.createServer({ cert: tls.cert, key: tls.key }, handler)
    : http.createServer(handler);

  const sockets = new Set<import("node:net").Socket>();
  server.on("connection", (socket) => {
    sockets.add(socket);
    socket.on("close", () => sockets.delete(socket));
  });

  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, () => {
      listenPort = (server.address() as AddressInfo).port;
      resolve();
    });
  });

  // 2. UDP Multicast Sender
  const sender = dgram.createSocket({ type: "udp4", reuseAddr: true });
  let multicastListener: dgram.Socket | null = null;

  const cleanup = async () => {
    try { sender.close(); } catch {}
    if (multicastListener) {
      try { multicastListener.close(); } catch {}
    }
    for (const socket of sockets) socket.destroy();
    await new Promise<void>((done) => server.close(() => done()));
  };

  try {
    await new Promise<void>((resolve, reject) => {
      sender.once("error", reject);
      sender.bind(0, () => {
        try {
          sender.setBroadcast(true);
          sender.setMulticastTTL(1);
        } catch {}
        resolve();
      });
    });

    // 3. Optional Multicast Listener on 53317 (catches multicast peer replies if free)
    multicastListener = await new Promise<dgram.Socket | null>((resolve) => {
      const socket = dgram.createSocket({ type: "udp4", reuseAddr: true });
      let settled = false;

      socket.on("error", () => {
        if (!settled) {
          settled = true;
          try { socket.close(); } catch {}
          resolve(null);
        }
      });

      socket.on("message", (msg, rinfo) => {
        try {
          const parsed = JSON.parse(msg.toString("utf-8"));
          collector.add(parsed, rinfo.address);
        } catch {}
      });

      socket.bind(DEFAULT_PORT, () => {
        try { socket.addMembership(MULTICAST_ADDRESS); } catch {}
        if (!settled) {
          settled = true;
          resolve(socket);
        }
      });
    });

    const announcement = {
      alias: config.alias,
      version: PROTOCOL_VERSION,
      deviceModel: config.deviceModel,
      deviceType: config.deviceType,
      fingerprint: ownFingerprint,
      port: listenPort,
      protocol: config.protocol,
      download: false,
      announce: true,
    };

    const packet = Buffer.from(JSON.stringify(announcement), "utf-8");

    // 4. Send bursts
    const bursts = [0, 300, 800].filter((t) => t < timeoutMs);
    for (const t of bursts) {
      void delay(t, options.signal).then(() => {
        try {
          sender.send(packet, DEFAULT_PORT, MULTICAST_ADDRESS);
        } catch {}
      });
    }

    await delay(timeoutMs, options.signal);
  } finally {
    await cleanup();
  }

  return {
    peers: collector.list(),
    warnings,
  };
}

export function findPeer(peers: ReadonlyArray<Peer>, query: string): Peer | undefined {
  const target = query.trim().toLowerCase();
  return (
    peers.find((p) => p.alias.toLowerCase() === target) ??
    peers.find((p) => p.fingerprint.toLowerCase() === target) ??
    peers.find((p) => p.host === query.trim()) ??
    peers.find((p) => p.alias.toLowerCase().includes(target))
  );
}
