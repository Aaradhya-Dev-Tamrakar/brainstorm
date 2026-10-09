# Executive Data Manifest: Auxiliary Suites, MCP Servers & Presentation Hubs

**Observer**: Commander 2 (Auxiliary & AEC) | **Status**: 100% Deterministically Verified

---

## 1. AEC-MCP Suite (`F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite`)

| ID | Name | Absolute Path | Tech Stack | Execution Context | Core Superpower | CLI / Launch Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AEC-01** | `fusion360-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\fusion360-mcp` | Python 3.10+, `http.server`, `CustomEvent` UI thread | Fusion 360 Add-In / HTTP (:8000) | Parametric CAD modeling, B-Rep inspection, script execution, viewport capture | Fusion Add-Ins / `.\install.ps1` |
| **AEC-02** | `Autodesk-Fusion-360-MCP-Server` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\Autodesk-Fusion-360-MCP-Server` | Python 3.10+, FastMCP, Fusion API Add-In | Stdio FastMCP & Fusion Add-In Bridge | Headless MCP server relay connecting agents to Fusion socket | `python Server/MCP_Server.py` |
| **AEC-03** | `revit-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\revit-mcp` | Python 3.10+, .NET, Revit API, pyRevit | Stdio MCP & Revit ExternalCommand | Parametric BIM authoring, family placement, schedule queries, IFC export | `python -m revit_mcp` |
| **AEC-04** | `autocad-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\autocad-mcp` | Python 3.10+, COM (`pywin32`), AutoCAD ActiveX | Stdio MCP & AutoCAD COM Client | 2D drafting automation, layer/entity generation, AutoLISP execution | `python -m autocad_mcp` |
| **AEC-05** | `rhino-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\rhino-mcp` | Python 3.9+, RhinoCompute, Grasshopper Headless | Stdio MCP & Rhino 7/8 IPC Bridge | NURBS modeling, Grasshopper solving, mesh subdivision, geometry bake | `rhino-mcp` or `python -m rhino_mcp` |
| **AEC-06** | `etabs-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\etabs-mcp` | Python 3.10+, CSI OAPI, `comtypes` | Stdio MCP & CSI ETABS OAPI Client | Structural framing, response spectrum analysis, seismic drift validation | `etabs-mcp` or `python -m etabs_mcp` |
| **AEC-07** | `sap2000-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\sap2000-mcp` | Python 3.10+, CSI SAP2000 OAPI, `comtypes` | Stdio MCP & SAP2000 OAPI Client | 2D/3D truss/bridge analysis, FE shell mesh generation, joint reactions | `python -m sap2000_mcp` |
| **AEC-08** | `staad-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\staad-mcp` | Python 3.10+, OpenSTAAD COM, `pywin32` | Stdio MCP & OpenSTAAD COM Client | Space frame modeling, member assignment, load combos, steel design | `python -m staad_mcp` |
| **AEC-09** | `epanet-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\epanet-mcp` | Python 3.10+, EPANET 2.2 DLL, `.inp` parser | Stdio MCP & EPANET Engine | Water network simulation, head loss calculation, pressure junction analysis | `python -m epanet_mcp` |
| **AEC-10** | `qgis-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\qgis-mcp` | Python 3.10+, PyQGIS, GDAL/OGR | Stdio MCP & Headless QGIS Subprocess | DEM elevation modeling, slope/contour generation, DXF boundary export | `python -m qgis_mcp` |
| **AEC-11** | `sketchup-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\sketchup-mcp` | Python 3.10+, Ruby Bridge, TCP Socket (:9876) | Stdio MCP & SketchUp Ruby Extension | Conceptual massing, solar shadow studies, extrusion, component insertion | `sketchup-mcp` or `python -m sketchup_mcp` |
| **AEC-12** | `3dsmax-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\3dsmax-mcp` | Python 3.10+, pymxs, MAXScript socket | Stdio MCP & 3ds Max Engine | Modifier stack automation, procedural meshes, Arnold rendering control | `python -m max_mcp` |
| **AEC-13** | `maya-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\maya-mcp` | Python 3.9+, `maya.cmds`, TCP Socket (:9877) | Stdio MCP & Maya Runtime | DAG scene queries, polygon meshes, animation keyframes, playblasts | Maya `userSetup.py` / `python -m maya_mcp.bridge` |
| **AEC-14** | `autodesk-mcp` | `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite\autodesk-mcp` | Python 3.10+, FastMCP, Shared Registry | Stdio MCP Router & Fleet Gateway | Central router dispatching tool calls across active Autodesk bridges | `autodesk-mcp` or `python -m autodesk_mcp` |

---

## 2. Utility Suite (`F:\Aaradhya-Dev-Tamrakar\Utility`)

| ID | Name | Absolute Path | Tech Stack | Execution Context | Core Superpower | CLI / Launch Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UTL-01** | `github-pilot` | `F:\Aaradhya-Dev-Tamrakar\Utility\github-pilot` | Python 3.10+, Typer, Rich, PyGithub | Macro CLI & Stdio MCP | Multi-account GitHub profile orchestrator, fleet audit, CI monitoring | `pilot` or `python -m pilot.cli` |
| **UTL-02** | `nepali-ocr-ai` | `F:\Aaradhya-Dev-Tamrakar\Utility\nepali-ocr-ai` | Python 3.11+, FastMCP, `google-genai`, `python-docx` | CLI & FastMCP (stdio JSON-RPC) | Devanagari vision OCR, Varnavinyas grammar checks, Preeti-Unicode transcoding | `nepali-ocr-ai` or `python -m nepali_ocr_ai.cli` |
| **UTL-03** | `md2pdf-desktop` | `F:\Aaradhya-Dev-Tamrakar\Utility\md2pdf-desktop` | Python 3.10+, Tkinter, FastMCP, `pypdf`, KaTeX | Desktop GUI, CLI, FastMCP | Technical Markdown-to-PDF conversion with math, Mermaid, GFM alerts | `python md2pdf_app.py` or `md2pdf` |
| **UTL-04** | `screen-qa-extension` | `F:\Aaradhya-Dev-Tamrakar\Utility\screen-qa-extension` | JavaScript, Chrome MV3, Gemini Flash API | Chrome Extension (Content & Worker) | DOM mutation observation detecting questions and rendering ambient overlays | Unpacked via `chrome://extensions` |
| **UTL-05** | `downloader-scripts` | `F:\Aaradhya-Dev-Tamrakar\Utility\downloader-scripts` | Windows Batch, PowerShell, `yt-dlp.exe`, ffmpeg | Desktop Batch & PowerShell Automation | Batch audio/video extraction via `yt-dlp` with metadata tags and auto-routing | `.\download.bat` or `.\yt-dlp.exe -a downloads.txt` |
| **UTL-06** | `windows-pilot` | `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot` | Python 3.10+, `pywin32`, `comtypes`, MS UIA, Typer | CLI & Windows Desktop MCP | Desktop UI automation, window perception, screenshot capture, UIA inspection | `winpilot` or `winpilot-mcp` |

---

## 3. Utility MCPs (`F:\Aaradhya-Dev-Tamrakar\Utility-MCPs`)

| ID | Name | Absolute Path | Tech Stack | Execution Context | Core Superpower | CLI / Launch Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MCP-01** | `google-classroom-mcp` | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\google-classroom-mcp` | Node.js 20+ (ESM), `@modelcontextprotocol/sdk`, `googleapis` | Stdio MCP (Node.js) | Google Classroom stream inspection, assignment queries, student submissions | `node index.mjs` (or `npm start`) |
| **MCP-02** | `localsend-mcp` | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\localsend-mcp` | TypeScript, Node.js 22+, `@modelcontextprotocol/sdk` | Stdio MCP & CLI (Node.js) | Zero-cloud LAN peer-to-peer file/text transfer and discovery via LocalSend | `node dist/index.js` or `npm start` |
| **MCP-03** | `typora-mcp` | `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\typora-mcp` | TypeScript, Node.js 22+, `@modelcontextprotocol/sdk` | Stdio MCP & CLI (Node.js) | Typora editor automation, draft recovery, real-time status inspection, HTML export | `node dist/index.js` or `npm start` |

---

## 4. Presentation & Educational Hubs

| ID | Name | Absolute Path | Tech Stack | Execution Context | Core Superpower | CLI / Launch Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HUB-01** | `AaradhyaDT.github.io` | `F:\AaradhyaDT\AaradhyaDT.github.io` | Vanilla HTML5/CSS3/JS, Web Crypto (AES-256-GCM), PWA | Static Web App / PWA (Canonical) | Authoritative portfolio with client AES-256-GCM encryption, 26-test gate | `python scripts/verify.py` / `.\sync.bat` |
| **HUB-02** | `Aaradhya-Dev-Tamrakar.github.io` | `F:\Aaradhya-Dev-Tamrakar\Aaradhya-Dev-Tamrakar.github.io` | Vanilla HTML5/CSS3/JS, Web Crypto, PWA | Static Web App / Mirror (GitHub Pages) | Secondary organization mirror providing multi-tenant redundancy and failover | `python -m http.server 8000` / `.\sync.bat` |
| **HUB-03** | `makerspace` | `F:\Aaradhya-Dev-Tamrakar\makerspace` | Static HTML5/CSS3/JS, Jekyll / GitHub Pages | Static Educational Web Portal | Equipment catalogue and portal for KEC Makerspace (3D printing, lasers, tools) | `bundle exec jekyll serve` or `python -m http.server 8000` |
| **HUB-04** | `react-workshop-ieeekecktm` | `F:\AaradhyaDT\react-workshop-ieeekecktm` | React 18+, Vite, Tailwind / CSS, ESLint | Interactive SPA / Vite Dev Server | Interactive educational curriculum and lab app for IEEE KEC React Workshop | `npm run dev` / `npm run build` |
| **HUB-05** | `IEEE-Xtreme-Archive` | `F:\Aaradhya-Dev-Tamrakar\IEEE-Xtreme-Archive` | Python 3.11+, CDP, SQLite (`corpus.db`), HF Hub | Autonomous Harvester CLI & Warehouse | Competitive programming statements/solutions harvesting, LaTeX math parsing | `python harvesters/cdp_engine.py` / `python scripts/verify.py` |
