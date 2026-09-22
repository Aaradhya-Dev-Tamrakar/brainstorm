#!/usr/bin/env node

/**
 * LocalSend MCP Server Entrypoint.
 *
 * Runs over standard input/output (StdioServerTransport) for Antigravity,
 * Claude Desktop, and other MCP clients while maintaining a persistent
 * background listener on port 53318 for LAN peer registration and transfers.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { loadConfig } from "./config.js";
import { LocalSendServer } from "./server.js";
import { handleToolCall, TOOLS } from "./tools.js";

async function main() {
  const config = loadConfig();
  const server = new LocalSendServer(config);

  // Start persistent background listener (handles /register and /info)
  try {
    const boundPort = await server.start(config.port);
    // Write diagnostics to stderr so stdout is purely JSON-RPC for MCP
    process.stderr.write(`[localsend-mcp] Background listener active on port ${boundPort} (${config.protocol})\n`);
  } catch (err) {
    process.stderr.write(`[localsend-mcp] Warning: Could not start background listener: ${err}\n`);
  }

  const mcp = new Server(
    {
      name: "localsend-mcp",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    },
  );

  // Handle tool listing
  mcp.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: TOOLS };
  });

  // Handle tool calls
  mcp.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    return await handleToolCall(name, args, config, server);
  });

  // Graceful cleanup
  const cleanup = async () => {
    try {
      await server.stop();
    } catch {}
    process.exit(0);
  };

  process.on("SIGINT", cleanup);
  process.on("SIGTERM", cleanup);

  // Connect via stdio transport
  const transport = new StdioServerTransport();
  await mcp.connect(transport);
  process.stderr.write("[localsend-mcp] Stdio transport connected and ready.\n");
}

main().catch((err) => {
  process.stderr.write(`[localsend-mcp] Fatal error: ${err}\n`);
  process.exit(1);
});
