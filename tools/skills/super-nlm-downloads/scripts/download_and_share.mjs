#!/usr/bin/env node
/**
 * Super-NLM Studio Artifact Downloader & LocalSend Dispatcher
 *
 * Automates:
 * 1. Extracting notebook ID from Google NotebookLM URLs.
 * 2. Downloading all Studio artifacts directly to the subject's downloads folder (outside any git repo).
 * 3. Sharing via LocalSend:
 *    - Entire folder transfer (preserving folder hierarchy)
 *    - "Files only" transfer (creates a dated subfolder <name>_YYYY-MM-DD and shares that folder)
 */

import { execSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";
import { pathToFileURL } from "node:url";

const DOWNLOADS_BASE = "C:\\Users\\Aaradhya\\Downloads";
const LOCALSEND_MCP_DIR = "F:\\Aaradhya-Dev-Tamrakar\\Utility-MCPs\\localsend-mcp";

// Known course code to folder name mappings
const COURSE_MAPPINGS = {
  EX725: "EX725 Exam",
  ME708: "ME708 Exam",
  CT653: "CT653 Exam",
  CT704: "CT704 Exam",
  EX751: "EX751 Exam",
  EX752: "EX752 Exam",
};

/**
 * Extracts UUID from URL or raw ID string.
 */
export function extractNotebookId(input) {
  if (!input) return null;
  const match = input.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
  return match ? match[0] : input.trim();
}

/**
 * Formats current date as YYYY-MM-DD.
 */
export function getFormattedDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/**
 * Resolves the destination subject folder under C:\Users\Aaradhya\Downloads
 */
export function resolveSubjectFolder(notebookId) {
  let title = "";
  try {
    const raw = execSync(`nlm notebook get ${notebookId} --json`, { encoding: "utf-8", stdio: ["ignore", "pipe", "ignore"] });
    const data = JSON.parse(raw);
    title = data.title || "";
  } catch (e) {
    // Fallback: try nlm studio status
    title = "";
  }

  // Look for course code
  for (const [code, folderName] of Object.entries(COURSE_MAPPINGS)) {
    if (title.toUpperCase().includes(code)) {
      const targetDir = path.join(DOWNLOADS_BASE, folderName);
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }
      return { targetDir, title, code, folderName };
    }
  }

  // Regex match any XX999 pattern
  const codeMatch = title.match(/([A-Z]{2}\d{3})/i);
  if (codeMatch) {
    const code = codeMatch[1].toUpperCase();
    const folderName = `${code} Exam`;
    const targetDir = path.join(DOWNLOADS_BASE, folderName);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    return { targetDir, title, code, folderName };
  }

  // Fallback to sanitized notebook title or ID
  const sanitized = (title || notebookId).replace(/[<>:"/\\|?*]/g, "_").trim();
  const targetDir = path.join(DOWNLOADS_BASE, sanitized);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }
  return { targetDir, title, code: null, folderName: sanitized };
}

/**
 * Checks whether a filename already has a numeric prefix (e.g. "1 - ", "0.2 - ").
 * Returns true if the name starts with a numbering pattern we would produce.
 */
function hasNumericPrefix(name) {
  return /^\d+(\.\d+)?\s*-\s/.test(name);
}

/**
 * Checks whether a folder name already has a numeric prefix (e.g. "0. ", "3. ").
 */
function hasFolderNumericPrefix(name) {
  return /^\d+\.\s/.test(name);
}

/**
 * Enumerates files in a directory with ascending numeric prefixes, oldest-generated first.
 *
 * Modes:
 * - Single-notebook (folderIndex === null): files get "1 - Title.ext", "2 - Title.ext", ...
 * - Multi-notebook  (folderIndex is a number): files get "N.1 - Title.ext", "N.2 - Title.ext", ...
 *
 * Already-numbered files (matching the prefix pattern) are skipped entirely when ALL files
 * in the directory already have prefixes. Otherwise all files are re-numbered cleanly.
 * Sorting uses birthtime (creation time) ascending so oldest-generated comes first.
 */
export function enumerateFiles(dir, folderIndex = null) {
  const entries = fs.readdirSync(dir, { withFileTypes: true }).filter((e) => e.isFile());
  if (entries.length === 0) return;

  // Skip if all files already have numeric prefixes
  const unnumbered = entries.filter((e) => !hasNumericPrefix(e.name));
  if (unnumbered.length === 0) {
    console.log(`[Enumerate] Skipping ${path.basename(dir)} — all files already numbered.`);
    return;
  }

  // Sort all files by creation time ascending (oldest first)
  const filesWithStats = entries.map((e) => {
    const fullPath = path.join(dir, e.name);
    const stat = fs.statSync(fullPath);
    return { name: e.name, fullPath, birthtime: stat.birthtime };
  });
  filesWithStats.sort((a, b) => a.birthtime - b.birthtime);

  // Rename each file with its ascending index
  // Two-pass rename to prevent collisions (e.g. "1 - X.mp4" being overwritten before it's renamed)
  const renames = [];
  for (let i = 0; i < filesWithStats.length; i++) {
    const file = filesWithStats[i];
    // Strip any existing numeric prefix before re-numbering
    const cleanName = file.name.replace(/^\d+(\.\d+)?\s*-\s*/, "");
    const seqNum = i + 1;
    const prefix = folderIndex !== null ? `${folderIndex}.${seqNum}` : `${seqNum}`;
    const newName = `${prefix} - ${cleanName}`;

    if (newName !== file.name) {
      // Pass 1: rename to a temp name to avoid mid-loop collisions
      const tmpName = `__enum_tmp_${i}_${Date.now()}${path.extname(file.name)}`;
      const tmpPath = path.join(dir, tmpName);
      fs.renameSync(file.fullPath, tmpPath);
      renames.push({ tmpPath, finalPath: path.join(dir, newName), oldName: file.name, newName });
    }
  }

  // Pass 2: rename temps to final names
  for (const { tmpPath, finalPath, oldName, newName } of renames) {
    fs.renameSync(tmpPath, finalPath);
    console.log(`[Enumerate] ${oldName} → ${newName}`);
  }
}

/**
 * Enumerates folders (and files within each) for multi-notebook batch downloads.
 *
 * Folders are numbered "0. FolderName", "1. FolderName", ... sorted by the oldest
 * file creation time within each folder (i.e., the notebook whose artifacts were
 * generated first gets index 0).
 *
 * Files inside each numbered folder get sub-indices: "0.1 - Title.ext", etc.
 *
 * If no subfolders exist (single-notebook download), falls back to flat file enumeration.
 */
export function enumerateFolders(rootDir) {
  const entries = fs.readdirSync(rootDir, { withFileTypes: true });
  const subDirs = entries.filter((e) => e.isDirectory());
  const topFiles = entries.filter((e) => e.isFile());

  if (subDirs.length === 0 && topFiles.length > 0) {
    // Single-notebook mode: only files at root level
    console.log(`[Enumerate] Single-notebook mode — numbering ${topFiles.length} file(s).`);
    enumerateFiles(rootDir, null);
    return;
  }

  if (subDirs.length === 0) return;

  // Multi-notebook mode: number folders, then files within each

  // For each subfolder, find the oldest file birthtime as the folder's sort key
  const foldersWithAge = subDirs.map((d) => {
    const dirPath = path.join(rootDir, d.name);
    const files = fs.readdirSync(dirPath, { withFileTypes: true }).filter((e) => e.isFile());
    let oldestBirth = new Date(); // fallback to now if empty
    for (const f of files) {
      const stat = fs.statSync(path.join(dirPath, f.name));
      if (stat.birthtime < oldestBirth) oldestBirth = stat.birthtime;
    }
    return { name: d.name, dirPath, oldestBirth };
  });

  // Sort folders by their oldest contained file (oldest-generated notebook first)
  foldersWithAge.sort((a, b) => a.oldestBirth - b.oldestBirth);

  // Two-pass rename to prevent collisions (e.g. "1. X" blocking "0. X" rename)
  const folderRenames = [];
  for (let i = 0; i < foldersWithAge.length; i++) {
    const folder = foldersWithAge[i];
    const cleanFolderName = folder.name.replace(/^\d+\.\s*/, "");
    const newFolderName = `${i}. ${cleanFolderName}`;

    if (newFolderName !== folder.name) {
      const tmpName = `__enum_dir_tmp_${i}_${Date.now()}`;
      const tmpPath = path.join(rootDir, tmpName);
      fs.renameSync(folder.dirPath, tmpPath);
      folderRenames.push({ tmpPath, finalPath: path.join(rootDir, newFolderName), oldName: folder.name, newName: newFolderName, index: i });
    } else {
      folderRenames.push({ tmpPath: null, finalPath: folder.dirPath, oldName: folder.name, newName: newFolderName, index: i });
    }
  }

  // Pass 2: rename temps to final folder names
  for (const r of folderRenames) {
    if (r.tmpPath) {
      fs.renameSync(r.tmpPath, r.finalPath);
      console.log(`[Enumerate] Folder: ${r.oldName} → ${r.newName}`);
    }
  }

  // Pass 3: enumerate files inside each (now-renamed) folder
  for (const r of folderRenames) {
    enumerateFiles(r.finalPath, r.index);
  }

  // Also number any loose files at the root level (rare, but handle gracefully)
  if (topFiles.length > 0) {
    enumerateFiles(rootDir, null);
  }
}

/**
 * Downloads all completed artifacts into the subject directory.
 * Guarantee: Downloads are staged outside of repository, then moved into target subject folder.
 * After download, files are auto-enumerated with ascending numeric prefixes (oldest first).
 */
export function downloadArtifacts(notebookId, targetDir, options = {}) {
  const { enumerate = true } = options;
  console.log(`[Super-NLM] Downloading artifacts for notebook ${notebookId}...`);
  console.log(`[Super-NLM] Target Subject Directory: ${targetDir}`);

  // Create isolated staging directory in Downloads (strictly outside git repos)
  const stagingDir = path.join(DOWNLOADS_BASE, `_nlm_staging_${Date.now()}`);
  fs.mkdirSync(stagingDir, { recursive: true });

  try {
    console.log(`[Super-NLM] Running: nlm download all ${notebookId}...`);
    execSync(`nlm download all ${notebookId} --output-dir "${stagingDir}" --skip-existing --interactive-format markdown`, {
      stdio: "inherit",
      encoding: "utf-8",
    });

    // Move all downloaded files from staging subdirectories into targetDir
    function copyRecursive(dir) {
      const items = fs.readdirSync(dir, { withFileTypes: true });
      for (const item of items) {
        const fullSource = path.join(dir, item.name);
        if (item.isDirectory()) {
          copyRecursive(fullSource);
        } else if (item.isFile()) {
          const destFile = path.join(targetDir, item.name);
          fs.copyFileSync(fullSource, destFile);
          console.log(`[Super-NLM] Saved: ${item.name}`);
        }
      }
    }

    copyRecursive(stagingDir);
    console.log(`[Super-NLM] All artifacts successfully moved to ${targetDir}`);
  } finally {
    // Cleanup staging folder
    if (fs.existsSync(stagingDir)) {
      fs.rmSync(stagingDir, { recursive: true, force: true });
    }
  }

  // Auto-enumerate files (single-notebook: flat file numbering)
  if (enumerate) {
    enumerateFiles(targetDir, null);
  }

  return targetDir;
}

/**
 * Collects payloads for LocalSend transfer preserving folder hierarchy.
 */
function collectPayloads(paths) {
  const payloads = [];
  function walkDir(currentDir, rootParentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walkDir(fullPath, rootParentDir);
      } else if (entry.isFile()) {
        const stat = fs.statSync(fullPath);
        const relPath = path.relative(rootParentDir, fullPath).replace(/\\/g, "/");
        payloads.push({
          fileName: relPath,
          path: fullPath,
          size: stat.size,
          modified: stat.mtime.toISOString(),
        });
      }
    }
  }
  for (const raw of paths) {
    const resolved = path.resolve(raw);
    const stat = fs.statSync(resolved);
    if (stat.isDirectory()) {
      walkDir(resolved, path.dirname(resolved));
    } else if (stat.isFile()) {
      payloads.push({
        fileName: path.basename(resolved),
        path: resolved,
        size: stat.size,
        modified: stat.mtime.toISOString(),
      });
    }
  }
  return payloads;
}

/**
 * Shares folder or files via LocalSend.
 */
export async function shareViaLocalSend({ targetDir, peerAlias = "V2029", filesOnly = false, specificFiles = [], subfolderPrefix = null }) {
  console.log(`[LocalSend] Preparing transfer to ${peerAlias}...`);

  // Dynamically import localsend-mcp modules
  const configModule = await import(pathToFileURL(path.join(LOCALSEND_MCP_DIR, "dist", "config.js")).href);
  const discoveryModule = await import(pathToFileURL(path.join(LOCALSEND_MCP_DIR, "dist", "discovery.js")).href);
  const clientModule = await import(pathToFileURL(path.join(LOCALSEND_MCP_DIR, "dist", "client.js")).href);

  const config = configModule.loadConfig();
  const outcome = await discoveryModule.discoverPeers(config, { timeoutMs: 4000 });
  const peer = discoveryModule.findPeer(outcome.peers, peerAlias);

  if (!peer) {
    throw new Error(`Peer "${peerAlias}" not found on LAN. Ensure LocalSend is open on ${peerAlias}.`);
  }
  console.log(`[LocalSend] Found peer ${peer.alias} at ${peer.host}:${peer.port}`);

  let pathToShare = targetDir;

  if (filesOnly) {
    // Requirement 2: "if asked to share the files only, then create a subfolder with those files, append date to the folder name, and share the folder"
    const dateStr = getFormattedDate();
    const baseName = subfolderPrefix || path.basename(targetDir);
    const subfolderName = `${baseName}_${dateStr}`;
    const subfolderPath = path.join(targetDir, subfolderName);

    if (!fs.existsSync(subfolderPath)) {
      fs.mkdirSync(subfolderPath, { recursive: true });
    }

    const availableFiles = fs.readdirSync(targetDir, { withFileTypes: true })
      .filter((d) => d.isFile())
      .map((d) => d.name);

    let filesToCopy = [];
    if (specificFiles && specificFiles.length > 0) {
      filesToCopy = availableFiles.filter((f) =>
        specificFiles.some((pattern) => f.toLowerCase().includes(pattern.toLowerCase()))
      );
    } else {
      filesToCopy = availableFiles;
    }

    if (filesToCopy.length === 0) {
      throw new Error(`No matching files found in ${targetDir} to share.`);
    }

    console.log(`[LocalSend] Creating dated subfolder: ${subfolderName} (${filesToCopy.length} files)`);
    for (const f of filesToCopy) {
      fs.copyFileSync(path.join(targetDir, f), path.join(subfolderPath, f));
    }

    pathToShare = subfolderPath;
  }

  const payloads = collectPayloads([pathToShare]);
  console.log(`[LocalSend] Dispatching ${payloads.length} item(s) to ${peer.alias}...`);
  for (const p of payloads) {
    console.log(` - ${p.fileName} (${(p.size / (1024 * 1024)).toFixed(2)} MB)`);
  }

  const result = await clientModule.sendFiles(config, { peer, payloads });
  console.log(`[LocalSend] Transfer completed successfully!`);
  return { result, pathToShare, payloadsCount: payloads.length };
}

// CLI Execution entrypoint
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(`
Usage: node download_and_share.mjs <notebook_url_or_id> [options]
       node download_and_share.mjs --enumerate-output <path>

Options:
  --to <alias>               Target LocalSend peer (default: V2029)
  --share                    Share the entire subject folder after download
  --share-only               Do not download, only share existing subject folder
  --files-only               Bundle requested/downloaded files into a dated subfolder (<name>_YYYY-MM-DD) and share
  --filter <keyword>         Filter specific files (can specify multiple times)
  --subfolder-name <name>    Custom prefix for the dated subfolder
  --no-enumerate             Skip automatic file numbering after download
  --enumerate-output <path>  Number files/folders in an existing output directory
                             (auto-detects single vs multi-notebook layout)
    `);
    process.exit(0);
  }

  // Standalone enumerate mode: number an existing folder without downloading
  if (args.includes("--enumerate-output")) {
    const outputPath = args[args.indexOf("--enumerate-output") + 1];
    if (!outputPath || !fs.existsSync(outputPath)) {
      console.error(`[Enumerate] Directory not found: ${outputPath}`);
      process.exit(1);
    }
    console.log(`[Enumerate] Numbering files in: ${outputPath}`);
    enumerateFolders(outputPath);
    console.log(`[Enumerate] Done.`);
    return;
  }

  const inputUrl = args[0];
  const notebookId = extractNotebookId(inputUrl);
  if (!notebookId) {
    console.error("Invalid notebook URL or ID provided.");
    process.exit(1);
  }

  const peerAlias = args.includes("--to") ? args[args.indexOf("--to") + 1] : "V2029";
  const shouldShare = args.includes("--share") || args.includes("--share-only");
  const filesOnly = args.includes("--files-only");
  const noEnumerate = args.includes("--no-enumerate");
  const subfolderPrefix = args.includes("--subfolder-name") ? args[args.indexOf("--subfolder-name") + 1] : null;

  const filters = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--filter" && args[i + 1]) {
      filters.push(args[i + 1]);
    }
  }

  const { targetDir } = resolveSubjectFolder(notebookId);

  if (!args.includes("--share-only")) {
    downloadArtifacts(notebookId, targetDir, { enumerate: !noEnumerate });
  }

  if (shouldShare || filesOnly) {
    await shareViaLocalSend({
      targetDir,
      peerAlias,
      filesOnly,
      specificFiles: filters,
      subfolderPrefix,
    });
  }
}

if (process.argv[1] && process.argv[1].endsWith("download_and_share.mjs")) {
  main().catch((err) => {
    console.error("[Fatal Error]", err);
    process.exit(1);
  });
}
