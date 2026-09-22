/**
 * LocalSend MCP HTTP/HTTPS Listener.
 *
 * Runs a persistent server on port 53318 (or next free port) that:
 * 1. Responds to GET /api/localsend/v2/info
 * 2. Responds to POST /api/localsend/v2/register with 200 OK (enabling LocalSend favorites)
 * 3. Handles incoming file transfers (POST prepare-upload & upload) into config.downloadDir
 */

import * as fs from "node:fs";
import * as http from "node:http";
import * as https from "node:https";
import type { AddressInfo } from "node:net";
import * as path from "node:path";
import type {
  DeviceInfo,
  FileDescriptor,
  LocalSendConfig,
  PrepareUploadRequest,
  PrepareUploadResponse,
} from "./types.js";
import { API_PREFIX, PROTOCOL_VERSION } from "./types.js";
import { ensureTlsMaterial, type TlsMaterial } from "./tls.js";
import { randomId, uniquePath } from "./net.js";

export interface ReceivedFileRecord {
  fileName: string;
  savedPath: string;
  size: number;
  sender: string;
  timestamp: string;
}

interface IncomingSession {
  id: string;
  sender: DeviceInfo;
  files: Record<string, FileDescriptor>;
  tokens: Record<string, string>; // fileId -> token
}

export class LocalSendServer {
  private server: http.Server | https.Server | null = null;
  private activePort: number = 0;
  private tls: TlsMaterial | null = null;
  private sessions = new Map<string, IncomingSession>();
  private receivedHistory: ReceivedFileRecord[] = [];

  constructor(private config: LocalSendConfig) {}

  public get port(): number {
    return this.activePort;
  }

  public get history(): ReadonlyArray<ReceivedFileRecord> {
    return this.receivedHistory;
  }

  public async start(desiredPort: number = this.config.port): Promise<number> {
    if (this.server) {
      return this.activePort;
    }

    if (this.config.protocol === "https") {
      this.tls = ensureTlsMaterial();
    }

    let portToTry = desiredPort;
    const maxPort = desiredPort + 10;

    while (portToTry <= maxPort) {
      try {
        const boundPort = await this.tryListen(portToTry);
        this.activePort = boundPort;
        this.config.port = boundPort;
        return boundPort;
      } catch (err: any) {
        if (err.code === "EADDRINUSE") {
          portToTry += 1;
        } else {
          throw err;
        }
      }
    }

    throw new Error(`Unable to find an open port between ${desiredPort} and ${maxPort}`);
  }

  private tryListen(port: number): Promise<number> {
    return new Promise((resolve, reject) => {
      const handler = (req: http.IncomingMessage, res: http.ServerResponse) => {
        this.handleRequest(req, res);
      };

      const srv = this.tls
        ? https.createServer({ cert: this.tls.cert, key: this.tls.key }, handler)
        : http.createServer(handler);

      srv.once("error", (err) => {
        reject(err);
      });

      srv.listen(port, () => {
        const addr = srv.address() as AddressInfo;
        this.server = srv;
        resolve(addr.port);
      });
    });
  }

  public async stop(): Promise<void> {
    if (!this.server) return;
    return new Promise((resolve) => {
      this.server!.close(() => {
        this.server = null;
        resolve();
      });
    });
  }

  private async handleRequest(req: http.IncomingMessage, res: http.ServerResponse): Promise<void> {
    const rawUrl = req.url || "";
    const parsedUrl = new URL(rawUrl, `http://localhost:${this.activePort}`);
    const pathname = parsedUrl.pathname;
    const method = req.method?.toUpperCase();

    // 1. GET /api/localsend/v2/info
    if (method === "GET" && pathname === `${API_PREFIX}/info`) {
      this.sendJson(res, 200, this.getDeviceInfo());
      return;
    }

    // 2. POST /api/localsend/v2/register (Peer registration & LocalSend favoriting callback)
    if (method === "POST" && pathname === `${API_PREFIX}/register`) {
      // LocalSend app POSTs here when registering or adding to favorites
      this.sendJson(res, 200, this.getDeviceInfo());
      return;
    }

    // 3. POST /api/localsend/v2/prepare-upload
    if (method === "POST" && pathname === `${API_PREFIX}/prepare-upload`) {
      try {
        const bodyText = await this.readBody(req);
        const data: PrepareUploadRequest = JSON.parse(bodyText);

        const sessionId = randomId();
        const tokens: Record<string, string> = {};
        for (const fileId of Object.keys(data.files)) {
          tokens[fileId] = randomId();
        }

        this.sessions.set(sessionId, {
          id: sessionId,
          sender: data.info,
          files: data.files,
          tokens,
        });

        const response: PrepareUploadResponse = {
          sessionId,
          files: tokens,
        };
        this.sendJson(res, 200, response);
      } catch (err: any) {
        this.sendJson(res, 400, { error: err.message });
      }
      return;
    }

    // 4. POST /api/localsend/v2/upload?sessionId=...&fileId=...&token=...
    if (method === "POST" && pathname === `${API_PREFIX}/upload`) {
      const sessionId = parsedUrl.searchParams.get("sessionId") || "";
      const fileId = parsedUrl.searchParams.get("fileId") || "";
      const token = parsedUrl.searchParams.get("token") || "";

      const session = this.sessions.get(sessionId);
      if (!session || session.tokens[fileId] !== token) {
        this.sendJson(res, 403, { error: "Invalid session or token" });
        return;
      }

      const fileDesc = session.files[fileId];
      if (!fileDesc) {
        this.sendJson(res, 400, { error: "File ID not in session" });
        return;
      }

      try {
        const downloadDir = this.config.downloadDir;
        if (!fs.existsSync(downloadDir)) {
          fs.mkdirSync(downloadDir, { recursive: true });
        }

        const targetPath = uniquePath(downloadDir, fileDesc.fileName);
        const partPath = `${targetPath}.part`;
        const writeStream = fs.createWriteStream(partPath);

        let receivedBytes = 0;
        req.on("data", (chunk: Buffer) => {
          receivedBytes += chunk.length;
          writeStream.write(chunk);
        });

        req.on("end", () => {
          writeStream.end(() => {
            fs.renameSync(partPath, targetPath);
            this.receivedHistory.push({
              fileName: fileDesc.fileName,
              savedPath: targetPath,
              size: receivedBytes,
              sender: session.sender.alias,
              timestamp: new Date().toISOString(),
            });
            this.sendJson(res, 200, { status: "ok" });
          });
        });

        req.on("error", (err) => {
          writeStream.destroy();
          if (fs.existsSync(partPath)) fs.unlinkSync(partPath);
          this.sendJson(res, 500, { error: err.message });
        });
      } catch (err: any) {
        this.sendJson(res, 500, { error: err.message });
      }
      return;
    }

    // 5. POST /api/localsend/v2/cancel
    if (method === "POST" && pathname === `${API_PREFIX}/cancel`) {
      const sessionId = parsedUrl.searchParams.get("sessionId") || "";
      this.sessions.delete(sessionId);
      this.sendJson(res, 200, { status: "cancelled" });
      return;
    }

    this.sendJson(res, 404, { error: "Not found" });
  }

  private getDeviceInfo(): DeviceInfo {
    return {
      alias: this.config.alias,
      version: PROTOCOL_VERSION,
      deviceModel: this.config.deviceModel,
      deviceType: this.config.deviceType,
      fingerprint: this.tls?.fingerprint || this.config.fingerprint,
      port: this.activePort,
      protocol: this.config.protocol,
      download: true,
    };
  }

  private readBody(req: http.IncomingMessage): Promise<string> {
    return new Promise((resolve, reject) => {
      const chunks: Buffer[] = [];
      req.on("data", (chunk: Buffer) => chunks.push(chunk));
      req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
      req.on("error", reject);
    });
  }

  private sendJson(res: http.ServerResponse, status: number, data: unknown): void {
    const json = JSON.stringify(data);
    res.writeHead(status, {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(json),
      "Connection": "close",
    });
    res.end(json);
  }
}
