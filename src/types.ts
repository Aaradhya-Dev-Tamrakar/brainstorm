/**
 * LocalSend Protocol v2 / v2.1 Types and Constants
 */

export const PROTOCOL_VERSION = "2.1";
export const DEFAULT_PORT = 53317;
export const DEFAULT_MCP_PORT = 53318;
export const MULTICAST_ADDRESS = "224.0.0.167";
export const API_PREFIX = "/api/localsend/v2";

export interface DeviceInfo {
  alias: string;
  version: string;
  deviceModel?: string;
  deviceType?: string;
  fingerprint: string;
  port: number;
  protocol: "http" | "https";
  download?: boolean;
}

export interface Peer {
  alias: string;
  host: string;
  port: number;
  protocol: "http" | "https";
  fingerprint: string;
  deviceModel?: string;
  deviceType?: string;
  download?: boolean;
}

export interface FileDescriptor {
  id: string;
  fileName: string;
  size: number;
  fileType: string;
  sha256?: string;
  preview?: string;
  metadata?: {
    modified?: string;
    [key: string]: unknown;
  };
}

export interface PrepareUploadRequest {
  info: DeviceInfo;
  files: Record<string, FileDescriptor>;
}

export interface PrepareUploadResponse {
  sessionId: string;
  files: Record<string, string>; // fileId -> token
}

export interface Payload {
  fileName: string;
  path?: string;
  content?: Buffer;
  size: number;
  fileType?: string;
  modified?: string;
}

export interface SentFile {
  fileName: string;
  size: number;
  ok: boolean;
  error?: string;
}

export interface SendResult {
  peer: Peer;
  sessionId: string;
  files: SentFile[];
  bytesSent: number;
}

export interface LocalSendConfig {
  alias: string;
  deviceModel: string;
  deviceType: string;
  port: number;
  protocol: "http" | "https";
  fingerprint: string;
  downloadDir: string;
}

export class TransferRejectedError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = "TransferRejectedError";
  }
}

export class PeerNotFoundError extends Error {
  constructor(target: string) {
    super(`No LocalSend device named "${target}" was found on the local network.`);
    this.name = "PeerNotFoundError";
  }
}
