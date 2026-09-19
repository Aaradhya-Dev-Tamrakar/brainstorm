# 📱 RESEARCH EXPERIMENT: EXP-LOCALSEND-MCP-001 (Live Empirical Verification of the LocalSend MCP Server)

```text
Artifact ID:          EXP-LOCALSEND-MCP-001
Title:                Live Empirical Verification of localsend-mcp against Physical Mobile Device (Vivo V2029) and Desktop (SFG16)
Version:              1.0.0
Status:               EMPIRICALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Ingestion & Actuation (P2P Mesh / LAN File Handoff)
Created Date:         2026-09-19
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED
Target Tool:          F:\Aaradhya-Dev-Tamrakar\localsend-mcp
Contract:             schemas/examples/localsend-mcp.contract.json
```

---

## 1. Objective & Hypothesis

* **Hypothesis (HYP-LSN-001):** The `localsend-mcp` server can execute local LAN peer discovery over UDP multicast and HTTP/HTTPS, negotiate in-process X.509 mutual TLS, and reliably deliver direct text snippets and filesystem artifacts to a physical mobile device running the LocalSend protocol (`Vivo V2029`).
* **Scope:** Full tool suite verification across `localsend_status`, `localsend_devices`, `localsend_send` (text payload and disk file payload), and `localsend_history`.

---

## 2. Experimental Setup & Environment

The test was executed live against the active local Wi-Fi subnet (`192.168.1.0/24`) connecting the host workstation (`SFG16`, `192.168.1.11`) and a physical Android smartphone (`Vivo V2029`, `192.168.1.4`).

| Parameter | Configuration |
| :--- | :--- |
| **Host Workstation** | Windows 11 (`192.168.1.11`), Node.js runtime |
| **Target Mobile Device** | Vivo V2029 (`192.168.1.4:53317`), LocalSend v2.2 |
| **MCP Server Transport** | FastMCP / Stdio JSON-RPC with background listener |
| **Protocol / Security** | LocalSend v2 REST, TLSv1.3 with pure ASN.1 DER X.509 client certificate |
| **Date of Run** | 2026-09-19 |
| **Verification Gate** | Deterministic live execution |

---

## 3. Execution & Results

### 3.1 Server Status (`localsend_status`)
* **Agent Alias:** `"Antigravity on SFG16"`
* **Listening Port:** `53319 [https]`
* **Device Fingerprint:** `5eb7d53649534c431b5609e8407f607495f76f70c270dd9ca6dfd5c48c0b461b`
* **Local LAN IP:** `192.168.1.11`
* **Result:** Initialized successfully with in-process TLS material generation.

### 3.2 LAN Peer Discovery (`localsend_devices`)
Broadcasted UDP multicast announcement (`224.0.0.167:53317`) and collected responding peers:
* **Peer 1 (Desktop):** `SFG16` (`192.168.1.11:53317` [https], Windows, Fingerprint: `2139EC8B4ACA91F7...`)
* **Peer 2 (Mobile):** `V2029` (`192.168.1.4:53317` [https], Vivo, Fingerprint: `B27ED88FAB1D77ED...`)
* **Discovery Latency:** < 1.2s.

### 3.3 Text Payload Transfer (`localsend_send`)
* **Target:** `V2029` (`192.168.1.4:53317`, HTTPS)
* **Payload:** Text snippet (`agent_verification.txt`, 86 B)
* **Protocol Exchange:** `/api/localsend/v2/prepare-upload` $\to$ `/api/localsend/v2/upload`
* **Session ID:** `ea6e15be-c9d2-4c36-82fd-d840d42e1e70`
* **Delivery Status:** `Sent: 1/1 items (86 B / 86 B)`, `ok: true`.

### 3.4 File Payload Transfer (`localsend_send`)
* **Target:** `V2029` (`192.168.1.4:53317`, HTTPS)
* **Payload:** Filesystem artifact (`test_e4_artifact.json`, 136 B)
* **Session ID:** `a7427e09-5347-4ddf-9fd1-57e4b92b8b6e`
* **Delivery Status:** `Sent: 1/1 items (136 B / 136 B)`, `ok: true`.

### 3.5 Inbox & History Query (`localsend_history`)
* Successfully queried persistent receiver state (0 incoming items pending).

---

## 4. Claim Reconciliation

| Claim in Registry / Spec | Measured Result | Epistemic Verdict |
| :--- | :--- | :--- |
| Zero-cloud local P2P transfer over LAN | End-to-end HTTPS transfer verified over Wi-Fi without cloud relay | **CONFIRMED** |
| Physical device handoff to Vivo V2029 | Delivered both text snippet and JSON artifact to V2029 | **CONFIRMED** |
| LocalSend protocol v2 compatibility | Negotiated prepare-upload/upload lifecycle with LocalSend v2.2 | **CONFIRMED** |
| In-process ASN.1 DER X.509 mutual TLS | Client certificate generated and validated during TLSv1.3 handshake | **CONFIRMED** |

---

## 5. Limitations & Boundary Conditions

1. **Subnet Isolation:** Both host and mobile peer must reside on the same broadcast domain (`192.168.1.0/24`) or have multicast routing enabled.
2. **Foreground App State:** Android battery saver policies may suspend the LocalSend background listener if the screen is locked for extended periods.

---

## 6. Provenance & Reproduction

* **Repository:** `F:\Aaradhya-Dev-Tamrakar\localsend-mcp`
* **Reproduction Command:**
  ```powershell
  cd F:\Aaradhya-Dev-Tamrakar\localsend-mcp
  node -e "
  import('./dist/tools.js').then(async ({ handleToolCall }) => {
    import('./dist/config.js').then(async ({ loadConfig }) => {
      import('./dist/server.js').then(async ({ LocalSendServer }) => {
        const config = loadConfig();
        const server = new LocalSendServer(config);
        await server.start(53319);
        const res = await handleToolCall('localsend_send', { to: 'V2029', text: 'Verification Ping' }, config, server);
        console.log(res.content[0].text);
        await server.stop();
      });
    });
  });"
  ```
