# Research Note: LocalSend Zero-Router Direct Transport & AirDrop Parity Architecture

**Date:** 2026-09-27  
**Author:** Aaradhya Dev Tamrakar  
**Topic:** Architectural Evaluation of Upgrading LocalSend to Zero-Router Direct P2P Transfer  
**Cross-References:** [PLAN-P2P-001](../plans/PLAN-P2P-001_OFFLINE_DIRECT_TRANSPORT_ENGINE.md), [HYP-006](../hypotheses/HYP-006-DIRECT-L2-TRANSPORT-PARITY.yaml)

---

## 1. Problem Statement & Motivation

LocalSend is an outstanding, open-source, cross-platform file sharing solution. However, because it operates at the Application Layer (L7) via mDNS broadcasts (`:5353`) and standard HTTP/REST over a local subnet, it requires both the sender and receiver to be connected to the exact same Wi-Fi network.

In scenarios where:
* Users are outdoors or in transit with no Wi-Fi access point,
* Enterprise or public networks enable **Client Isolation** (AP isolation blocking direct peer communication),
* Users need ad-hoc point-to-point transfers between Windows laptops and Android devices,

LocalSend fails unless a user manually configures a personal hotspot and re-associates both devices.

---

## 2. Technical Feasibility & Platform Scope

### 2.1 Scope Decision: Excluding Apple iOS Native AWDL
Apple’s AirDrop relies on **Apple Wireless Direct Link (AWDL)** operating on 802.11 Action Frames. Because iOS sandboxing strictly forbids third-party apps from low-level AWDL frame injection or programmatic silent hotspot joining (which prompts the user with system dialogs on every attempt), targeting zero-click AirDrop parity on iOS is non-viable.

### 2.2 Scope Decision: Android $\leftrightarrow$ Windows $\leftrightarrow$ Linux Focus
On Android, Windows 10/11, and Linux:
1. **BLE Advertising & Scanning** are fully accessible via native OS APIs.
2. **Wi-Fi Direct (P2P Group Owner / Client)** and **Local-Only Hotspot (LOHS)** APIs allow zero-interaction high-speed Wi-Fi mesh creation.
3. Once the direct L2 link is negotiated, LocalSend's core file chunking, TLS certificate exchange, and streaming HTTP pipeline execute without requiring any external router.

---

## 3. Core Architectural Strategy

```
[LocalSend Flutter UI & File Engine]
                 │
                 ▼
    [DirectTransportPlugin (FFI)]
    ├── Android: Kotlin (WifiP2pManager + BLE)
    ├── Windows: C++/WinRT (WiFiDirectConnectionListener + BLE Watcher)
    └── Linux: Rust / D-Bus (wpa_supplicant + BlueZ)
                 │
                 ▼
[Link-Local Subnet: 192.168.49.0/24 @ 50-100+ MB/s]
```

### 3.1 Next Actions
1. Prototype BLE advertisement handshake schema.
2. Test Windows `WiFiDirectConnectionListener` interop against Android `WifiP2pManager.createGroup()`.
3. Wrap connection orchestration into a clean Flutter Platform Channel plugin for integration into a LocalSend fork.
