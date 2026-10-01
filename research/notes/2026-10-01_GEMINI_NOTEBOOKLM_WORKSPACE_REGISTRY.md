# Research Note: Gemini & NotebookLM Knowledge Base Registry

- **Date**: 2026-10-01
- **Author**: Aaradhya Dev Tamrakar (`@AaradhyaDT`)
- **Epistemic Classification**: `EMPIRICALLY_VERIFIED`
- **Related Documents**: `[[AARADHYA_MASTER_v165]]`, `[[PROFILE]]`, `[[ECOSYSTEM_ARCHITECTURAL_BRAINSTORM]]`, `[[drive-manifest.json]]`

---

## 1. Executive Summary

This registry catalogues the complete fleet of Google NotebookLM and Gemini workspaces utilized across Aaradhya's engineering ecosystem, personal research laboratory, and academic fellowship streams.

---

## 2. Personal & Ecosystem Core Workspaces

| Workspace Name | Notebook ID | Direct URL | Scope & Epistemic Role |
| :--- | :--- | :--- | :--- |
| **Aaradhya — Engineer's Personal Notebook** | `95a79d26-2f87-42cd-8cb9-8361a1e56059` | [Open Workspace](https://notebook.google.com/notebook/95a79d26-2f87-42cd-8cb9-8361a1e56059) | **Lead Engineer's Private Journal & Master Workspace**: Grounded in `drive-manifest.json`, personal dossiers, master specs, and active development streams. |
| **SPARK** | `2c00f5a4-98dc-4783-96d1-3682fa3cb516` | [Open Workspace](https://notebook.google.com/notebook/2c00f5a4-98dc-4783-96d1-3682fa3cb516) | **Cross-Project Synergy & Ideation Workspace**: Research ideation, foundational technology evaluations, and cross-repository patterns. |

---

## 3. Project-Specific Workspaces: BiasAperture (Fuse AI Fellowship)

The **BiasAperture** research and validation corpus is indexed across four dedicated NotebookLM workspaces:

| Workspace Name | Notebook ID | Direct URL | Grounding Scope & Inventory |
| :--- | :--- | :--- | :--- |
| **BiasAperture — Strategy & Foundations** | `99bee3c6-07ed-4ff0-8ac8-0027b18ad06a` | [Open Workspace](https://notebook.google.com/notebook/99bee3c6-07ed-4ff0-8ac8-0027b18ad06a) | **Master Conceptual Layer (37 sources)**: Research sprint tracks 01–20, fellowship rubrics, overarching system architecture, and trade-off analyses. |
| **BiasAperture — References** | `bbac9235-404b-4c39-a2a4-1f30069af30b` | [Open Workspace](https://notebook.google.com/notebook/bbac9235-404b-4c39-a2a4-1f30069af30b) | **Academic Foundations (21 sources)**: Full-text peer-reviewed papers (*Gender Shades*, *FairFace*, *Model Cards*, *Datasheets*, Hardt et al. Equal Opportunity, four-fifths rule, SHAP theory) and EU AI Act regulatory documentation. |
| **BiasAperture — Source & Specs** | `928b5ed7-1353-4cb3-a1ce-b215e80b7db4` | [Open Workspace](https://notebook.google.com/notebook/928b5ed7-1353-4cb3-a1ce-b215e80b7db4) | **Ground-Truth Technical Layer (50 sources)**: Technical specifications (`specs/00`–`11`), production implementation (`src/bias_aperture/`), and test suites. |
| **BiasAperture — Repo State** | `6e9505f0-2d5c-4655-8bc7-9f97cf9620b9` | [Open Workspace](https://notebook.google.com/notebook/6e9505f0-2d5c-4655-8bc7-9f97cf9620b9) | **Synthesis & Defense Layer (39 sources)**: Developer logs, weekly milestone reports (WK1–WK5), proposal defense master dossier, and discrepancy audit trails. |

---

## 4. MCP & Super-NLM Tooling Integration

All workspaces listed above are accessible to automated coding agents and subagents via the local `super-nlm` and `notebooklm` MCP tools for source-grounded querying, batch synthesis, and citation verification:

```bash
# Querying via Super-NLM MCP
use super-nlm -> query_notebook(notebook_id="95a79d26-2f87-42cd-8cb9-8361a1e56059", query="...")
```

---

## 5. Privacy & Repository Boundaries

In accordance with `github-workflow` Rule #7, personal workspace IDs (`95a79d26...` and `2c00f5a4...`) must remain strictly within personal repositories (such as `brainstorm`) and must **never** be committed to public or collaborative team repositories (such as `BiasAperture`).
