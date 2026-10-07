# Experiment Dossier: Empirical Security Audit of Embedded Broadcom CPE Firmware

**ID:** `EXP-011`  
**Date:** 2026-10-07  
**Status:** Completed / Empirically Verified  
**Principal Investigator:** Aaradhya Dev Tamrakar  
**Epistemic Tier:** `EMPIRICALLY_VERIFIED` (`ARCH-RFC-001`)  
**Target Hardware:** Broadcom BCM6848 GPON ONT (CPE Architecture)  
**Daemon Stack:** Embedded `micro_httpd` / Broadcom CPE Web Server  

---

## 1. Executive Summary & Objective

Embedded Customer Premises Equipment (CPE) deployed by national telecommunications providers frequently suffers from architectural decoupling between the presentation layer (`frameset` web interface) and the underlying HTTP daemon. 

This experiment empirically analyzes access-control invariants on a standard GPON ONT deployment (Broadcom BCM6848 series). We sought to determine whether read-only status and binary backup endpoints enforce session tokens and privilege boundaries prior to serving data across the local subnet.

---

## 2. Empirical Findings & Vulnerability Surface

### Finding 1: Unauthenticated Binary Configuration Disclosure
* **Endpoint:** `GET /backupsettings.conf`
* **Observed Behavior:** The web daemon (`micro_httpd`) returns `HTTP/200 OK` directly without validating cookie headers, basic authentication, or session nonces.
* **Payload Scope:** The response consists of the full XML data tree (`DslCpeConfig v3.0`, ~88 KB), which includes:
  - Plaintext / Base64 administrative account hashes (`<AdminPassword>`, `<SupportPassword>`).
  - 390 TLV-encoded WLAN NVRAM variables, including the active WPA passphrase (`wl0_wpa_psk`) and SSID parameters.
  - ISP WAN PPPoE credentials and SIP VoIP telephony registration strings (`<SIP>`, `<WANPPPConnection>`).
  - TR-069 Auto-Configuration Server (ACS) URLs and periodic inform credentials.

### Finding 2: Unauthenticated Telemetry & Subnet Topology Bleed
* **Endpoints:** `GET /info.html`, `GET /dhcpinfo.html`, `GET /wlstationlist.cmd`, `GET /arpview.cmd`
* **Observed Behavior:**
  - Real-time optical transceiver telemetry (laser Tx/Rx power, bias current, operating temperature) is exposed without authentication.
  - Active DHCP lease tables and ARP mappings disclose the complete hostname, MAC address, and IP distribution of all connected personal devices across the local subnet.
  - Active wireless station lists expose real-time BSSID association states.

---

## 3. Root Cause Analysis

The vulnerability originates from a common embedded firmware design flaw:
1. **Client-Side Security Illusion:** The router's navigation tree (`menu.html` / `menuBcm.js`) dynamically renders visible menu links based on an in-memory JavaScript role check (`var options = new Array('user', ...)`).
2. **Missing Server-Side Path Interceptor:** While form submission handlers (`*.cgi` and `*.cmd` POST endpoints) require active authentication, the static and generated file handlers (`/backupsettings.conf`, `/info.html`) lack request authentication wrappers in the underlying C-based `micro_httpd` routing loop.

---

## 4. Defense-in-Depth & Remediation Architecture

Because ISP-provisioned ONT firmware cannot easily be recompiled by end-users, the following mitigation layers were designed and verified:

```
┌──────────────────────────────────────────────────────────────────┐
│                  REMEDIATION ARCHITECTURE                        │
├────────────────────────────┬─────────────────────────────────────┤
│ LAYER                      │ MITIGATION ACTION                   │
├────────────────────────────┼─────────────────────────────────────┤
│ 1. RF Isolation            │ Migrate from overlapping Ch 8 to    │
│                            │ non-overlapping Channel 1/6/11.     │
│ 2. Cryptographic Modern    │ Enforce pure WPA2-AES (CCMP).       │
│                            │ Eliminate legacy TKIP cipher caps.  │
│ 3. Perimeter Decoupling    │ Introduce a dual-band 5 GHz router   │
│                            │ in AP/Router mode to terminate      │
│                            │ all client Wi-Fi; disable ONT WLAN. │
│ 4. Service Invariant       │ Enforce WANAccess = FALSE on HTTP,  │
│                            │ SSH, Telnet, and FTP daemons.       │
└────────────────────────────┴─────────────────────────────────────┘
```

1. **Spectrum & Cipher Hardening:**
   - Retuning the 2.4 GHz spectrum from overlapping Channel 8 to clean Channel 6 eliminates adjacent-channel collision rates.
   - Upgrading from mixed `tkip+aes` to pure `aes` removes the 802.11n 54 Mbps bandwidth cap.
2. **Hybrid Upstream DNS:**
   - Setting Primary DNS to `1.1.1.1` provides DNSSEC validation and low-latency resolution, while preserving the ISP secondary (`202.70.95.248`) for local peering caches.
3. **Future 5 GHz Gateway Segmentation:**
   - Connecting a secondary dual-band Wi-Fi router to LAN Port 1 allows terminating all consumer client traffic on isolated modern hardware, turning the ONT into a passive optical bridge and VoIP terminator.

---

## 5. Artifact Provenance & Sanitization Notice

* **Redaction Invariant:** In accordance with institutional confidentiality guidelines, all real MAC addresses, customer phone numbers, and physical coordinates have been purged from this document.
* **Associated Automated Tool:** [`tools/router_cdp/cdp_router_manager.js`](../../tools/router_cdp/cdp_router_manager.js) provides the automated verification and configuration harness for this target class.
