---
name: google-stitch-integration
description: Connects Google Antigravity with external UI layout generators via Model Context Protocol (MCP) to ingest production-ready design files, color tokens, and asset configurations directly from Google Stitch.
category: frontend
---

# Google Stitch MCP Integration Guide

This skill enables Antigravity to interface with **Google Stitch** (https://stitch.withgoogle.com/) via the Model Context Protocol (MCP). It defines the workflow for extracting design tokens, component hierarchies, wireframes, and production layouts generated in Google Stitch and translating them into robust frontend code.

---

## 1. Overview & Architectural Role

Google Stitch acts as an AI-powered design layout and design-system generation engine. By integrating Stitch into Antigravity via MCP:
1. **Design Tokens Synchronization**: Imports semantic color tokens, typography scales, spacing grids, and elevation layers defined in Stitch directly into project Tailwind/CSS variables.
2. **Wireframe & Artboard Ingestion**: Ingests structured layout trees and exported screen JSON directly into Antigravity context.
3. **Component Transpilation**: Converts high-level Stitch component specifications into accessible, responsive React/HTML components adhering to `ui-ux-pro-max` and `design-taste-frontend` standards.

---

## 2. MCP Server Configuration

To configure the Google Stitch MCP server in your Antigravity environment, add the server definition to your `mcp_config.json` (located in `~/.gemini/antigravity/mcp_config.json` or project workspace):

```json
{
  "mcpServers": {
    "google-stitch": {
      "command": "npx",
      "args": ["-y", "@google/stitch-mcp"],
      "env": {
        "STITCH_API_KEY": "<YOUR_STITCH_API_KEY>"
      }
    }
  }
}
```

---

## 3. Stitch MCP Tool Call Patterns

When the Stitch MCP server is connected, use the following tools:

### 1. `stitch_get_project`
Retrieves project metadata, artboards, and layout components for a given project ID.
- **Input**: `{ "projectId": "string" }`
- **Output**: Artboard names, canvas dimensions, screen hierarchy, and component manifest.

### 2. `stitch_get_tokens`
Extracts design tokens defined in the Stitch design system.
- **Input**: `{ "projectId": "string", "format": "tailwind" | "css-variables" | "json" }`
- **Usage**: Use returned tokens to populate `tailwind.config.js` or `globals.css`.

### 3. `stitch_export_component`
Exports a specific artboard or component into production code.
- **Input**: `{ "projectId": "string", "componentId": "string", "targetFramework": "react-tailwind" }`
- **Output**: Clean JSX/TSX layout structure with layout hierarchy preserved.

---

## 4. Code Synthesis & Refinement Pipeline

When ingesting designs from Google Stitch:
1. **Token Mapping**: Verify and reconcile incoming colors against the project's existing color palette to prevent visual fragmentation.
2. **Responsive Hardening**: Convert fixed artboard pixel coordinates into fluid CSS Grid, Flexbox, and Tailwind responsive breakpoints (`sm:`, `md:`, `lg:`, `xl:`).
3. **Micro-Interaction Enrichment**: Augment raw Stitch layouts with spring transitions, hover lifts, and accessibility attributes specified by `antigravity-ui-motion-design-expert`.
