/**
 * LocalSend Client for outbound file/text transfers.
 */

import * as fs from "node:fs";
import * as http from "node:http";
import * as https from "node:https";
import type {
  DeviceInfo,
  FileDescriptor,
  LocalSendConfig,
  Peer,
  SendResult,
  SentFile,
  Payload,
} from "./types.js";
import {
  API_PREFIX,
  DEFAULT_PORT,
  PROTOCOL_VERSION,
  TransferRejectedError,
} from "./types.js";
import { guessFileType, randomId } from "./net.js";
import { ensureTlsMaterial, type TlsMaterial } from "./tls.js";

const REQUEST_TIMEOUT_MS = 60_000;
const UPLOAD_TIMEOUT_MS = 15 * 60 * 1000;

function requestOptions(
  peer: Peer,
  path: string,
  method: string,
  headers: http.OutgoingHttpHeaders,
  clientTls?: TlsMaterial | null,
): https.RequestOptions {
  return {
    hostname: peer.host,
    port: peer.port,
    path,
    method,
    headers,
    ...(peer.protocol === "https"
      ? {
          rejectUnauthorized: false,
          ...(clientTls && { key: clientTls.key, cert: clientTls.cert }),
        }
      : {}),
  };
}

interface RawResponse {
  status: number;
  body: string;
}

function sendRequest(
  peer: Peer,
  path: string,
  method: string,
  body: Buffer | fs.ReadStream | undefined,
  headers: http.OutgoingHttpHeaders,
  timeoutMs: number,
  signal?: AbortSignal,
  clientTls?: TlsMaterial | null,
): Promise<RawResponse> {
  const transport = peer.protocol === "https" ? https : http;

  return new Promise((resolve, reject) => {
    const req = transport.request(
      requestOptions(peer, path, method, headers, clientTls),
      (res) => {
        const chunks: Buffer[] = [];
        res.on("data", (chunk: Buffer) => chunks.push(chunk));
        res.on("end", () =>
          resolve({
            status: res.statusCode ?? 0,
            body: Buffer.concat(chunks).toString("utf-8"),
          }),
        );
        res.on("error", reject);
      },
    );

    req.setTimeout(timeoutMs, () => {
      req.destroy(
        new Error(
          `${peer.alias} did not respond within ${Math.round(timeoutMs / 1000)}s.`,
        ),
      );
    });

    req.on("error", (err: NodeJS.ErrnoException) => {
      if (err.code === "ECONNREFUSED") {
        reject(
          new Error(
            `${peer.alias} (${peer.host}:${peer.port}) refused connection. Is LocalSend open on that device?`,
          ),
        );
        return;
      }
      reject(err);
    });

    signal?.addEventListener("abort", () => req.destroy(), { once: true });

    if (!body) {
      req.end();
    } else if (Buffer.isBuffer(body)) {
      req.end(body);
    } else {
      body.on("error", (err) => req.destroy(err));
      body.pipe(req);
    }
  });
}

function explainPrepareFailure(status: number, alias: string, body: string): TransferRejectedError {
  switch (status) {
    case 400:
      return new TransferRejectedError(status, `${alias} rejected file list as invalid (400). ${body}`.trim());
    case 401:
      return new TransferRejectedError(
        status,
        `${alias} requires a PIN, or the PIN was wrong. Ask for the PIN and retry.`,
      );
    case 403:
      return new TransferRejectedError(status, `${alias} declined the transfer.`);
    case 409:
      return new TransferRejectedError(
        status,
        `${alias} is busy with another transfer. Wait a moment and retry.`,
      );
    case 429:
      return new TransferRejectedError(status, `${alias} is rate limiting requests. Wait a moment and retry.`);
    default:
      return new TransferRejectedError(
        status,
        `${alias} could not accept transfer (HTTP ${status}). ${body}`.trim(),
      );
  }
}

export function buildSenderInfo(
  config: LocalSendConfig,
  peer: Peer,
  clientTls?: TlsMaterial | null,
): DeviceInfo {
  return {
    alias: config.alias,
    version: PROTOCOL_VERSION,
    deviceModel: config.deviceModel,
    deviceType: config.deviceType,
    fingerprint: clientTls ? clientTls.fingerprint : config.fingerprint,
    port: config.port,
    protocol: peer.protocol,
    download: false,
  };
}

export interface SendOptions {
  peer: Peer;
  payloads: ReadonlyArray<Payload>;
  pin?: string;
  signal?: AbortSignal;
}

export async function sendFiles(
  config: LocalSendConfig,
  options: SendOptions,
): Promise<SendResult> {
  const { peer, payloads } = options;
  if (payloads.length === 0) {
    throw new Error("Nothing to send.");
  }

  let clientTls: TlsMaterial | null = null;
  if (peer.protocol === "https") {
    clientTls = ensureTlsMaterial();
    if (!clientTls) {
      throw new Error(
        `${peer.alias} uses HTTPS which requires a local client certificate. Could not generate TLS material.`,
      );
    }
  }

  const files: Record<string, FileDescriptor> = {};
  const byId = new Map<string, Payload>();

  for (const payload of payloads) {
    const id = randomId();
    files[id] = {
      id,
      fileName: payload.fileName,
      size: payload.size,
      fileType: payload.fileType ?? guessFileType(payload.fileName),
      ...(payload.modified && { metadata: { modified: payload.modified } }),
    };
    byId.set(id, payload);
  }

  const prepareBody = Buffer.from(
    JSON.stringify({ info: buildSenderInfo(config, peer, clientTls), files }),
    "utf-8",
  );

  const pinQuery = options.pin ? `?pin=${encodeURIComponent(options.pin)}` : "";
  const prepared = await sendRequest(
    peer,
    `${API_PREFIX}/prepare-upload${pinQuery}`,
    "POST",
    prepareBody,
    { "Content-Type": "application/json", "Content-Length": prepareBody.length },
    REQUEST_TIMEOUT_MS,
    options.signal,
    clientTls,
  );

  if (prepared.status === 204) {
    return { peer, sessionId: "", files: [], bytesSent: 0 };
  }
  if (prepared.status !== 200) {
    throw explainPrepareFailure(prepared.status, peer.alias, prepared.body);
  }

  let sessionId = "";
  let tokens: Record<string, string> = {};
  try {
    const parsed = JSON.parse(prepared.body);
    sessionId = String(parsed.sessionId ?? "");
    tokens = parsed.files ?? {};
  } catch {
    throw new Error(`${peer.alias} sent an invalid prepare-upload response.`);
  }

  const results: SentFile[] = [];
  let bytesSent = 0;

  for (const [fileId, token] of Object.entries(tokens)) {
    const payload = byId.get(fileId);
    if (!payload) continue;

    const query = `?sessionId=${encodeURIComponent(sessionId)}&fileId=${encodeURIComponent(fileId)}&token=${encodeURIComponent(token)}`;
    const body = payload.content ?? fs.createReadStream(payload.path!);

    const uploaded = await sendRequest(
      peer,
      `${API_PREFIX}/upload${query}`,
      "POST",
      body,
      {
        "Content-Type": payload.fileType ?? "application/octet-stream",
        "Content-Length": payload.size,
      },
      UPLOAD_TIMEOUT_MS,
      options.signal,
      clientTls,
    );

    if (uploaded.status === 200) {
      results.push({ fileName: payload.fileName, size: payload.size, ok: true });
      bytesSent += payload.size;
    } else {
      results.push({
        fileName: payload.fileName,
        size: payload.size,
        ok: false,
        error: `HTTP ${uploaded.status}: ${uploaded.body}`,
      });
    }
  }

  return { peer, sessionId, files: results, bytesSent };
}

export async function fetchPeerInfo(
  host: string,
  port: number = DEFAULT_PORT,
  protocol: "http" | "https" = "https",
): Promise<DeviceInfo> {
  const peer: Peer = {
    alias: host,
    host,
    port,
    protocol,
    fingerprint: "",
  };

  const clientTls = protocol === "https" ? ensureTlsMaterial() : null;
  const res = await sendRequest(
    peer,
    `${API_PREFIX}/info`,
    "GET",
    undefined,
    {},
    5000,
    undefined,
    clientTls,
  );

  if (res.status !== 200) {
    throw new Error(`Failed to query ${host}:${port} (HTTP ${res.status}): ${res.body}`);
  }

  return JSON.parse(res.body) as DeviceInfo;
}
