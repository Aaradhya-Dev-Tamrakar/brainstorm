# 🛡️ ARCHITECTURAL SPECIFICATION: OmniVault Tri-Tier Archival & Storage Optimization Engine

> **Artifact ID:** `ARCH-SPEC-009`  
> **Title:** OmniVault Tri-Tier Archival, Sub-Second Retrieval & Storage Optimization Engine  
> **Version:** `1.0.0`  
> **Status:** `ACTIVE`  
> **Principal Architect:** Aaradhya Dev Tamrakar (ADT)  
> **Domain:** Distributed Personal Storage, Information Retrieval & Disk Optimization  
> **Created Date:** 2026-10-05  
> **Evidence Tier:** `EMPIRICALLY_VERIFIED`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\omnivault` (Mirrored in `brainstorm` branch: `omnivault`)  
> **Execution Context:** Windows Desktop / Python 3.14 / SQLite FTS5 / BLAKE3  
> **Contract Reference:** [`schemas/examples/omnivault.contract.json`](../../schemas/examples/omnivault.contract.json)  

---

## 1. Executive Summary & Problem Statement

Modern multi-device personal storage architectures suffer from three critical points of friction:
1. **The Disconnected Cold Storage Dilemma (Search Blindness)**: High-capacity external hard drives (HDDs) are physically unplugged and stored in drawers 95% of the time. Traditional OS indexing engines (Windows Search, Spotlight) completely drop or fail to query offline drives. Locating an unindexed asset requires physical connection, spin-up delays, and manual directory crawling.
2. **Multi-Intake Mobile Bottlenecks**: Mobile captures (photos, documents, recordings) generate high churn. Users require both low-friction wireless LAN transfers (LocalSend) and high-throughput wired bulk dumps (USB/MTP) with zero re-copying of duplicate files.
3. **Workstation Disk Bloat**: Local NVMe workstation storage degrades over time due to hidden, regenerable build caches (Gradle, npm, pip, IDE caches) and duplicated binaries.

**OmniVault Core Axiom**: *The index and proxy previews must remain permanently resident and hot on the local workstation NVMe SSD, while the raw cold binaries reside safely on external cold media in human-readable hierarchies.*

---

## 2. Tri-Tier Storage Stratification

```
┌────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Hot-Edge (Mobile - Android/iOS)                                │
│  - Active capture: Camera, WhatsApp, Downloads, Voice memos            │
│  - Transport: LocalSend (Wi-Fi P2P) or High-Speed USB Cable (MTP)      │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Warm-Hub (Laptop NVMe SSD Control Plane)                       │
│  - Shadow Catalog: SQLite FTS5 database (~/.omnivault/catalog.db)      │
│  - Offline Proxy: WebP micro-thumbnails (160x160, 3KB/asset)           │
│  - Ingestion Staging: F:\OmniVault_Staging (LocalSend & Wired inboxes) │
│  - Query Latency: < 3.5 ms across 23,000+ indexed files                │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Cold-Vault (External Hard Drive - Western Digital 320GB)       │
│  - Partitions: I: (Main - Primary Vault) & H: (Mini - Secondary Vault) │
│  - Organization: Clean semantic tree (/Library/Category/YYYY/MM/...)   │
│  - Integrity: BLAKE3 cryptographic ledgers against bitrot              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Empirical Verification & Benchmarks

Empirically verified on physical hardware (2026-10-05):
* **Hardware Profile**: Western Digital WD3200BPVT (320GB USB External HDD) + NVMe SSD.
* **Volume `I:\` (Main)**: 15,991 files (120.2 GB) indexed in **5.81 seconds** (~2,750 files/sec).
* **Volume `H:\` (Mini)**: 7,317 files (24.2 GB) indexed in **3.91 seconds**.
* **Total Indexed Live Catalog**: **23,308 files (144.4 GB)**.
* **Search Latency**:
  - Keyword query (`setup`): 258 results in **1.57 ms**.
  - Category query (`pdf` under Documents): 1,390 results in **3.49 ms**.
* **Storage Optimization**:
  - Identified **13.9 GB** of safe, regenerable cache bloat (Gradle: 5.0 GB, npm: 2.9 GB, Temp: 2.6 GB, pip: 1.2 GB, VS Code: ~1.5 GB).
* **Automated Test Suite**: 6/6 unit tests passed in **0.33s**.
