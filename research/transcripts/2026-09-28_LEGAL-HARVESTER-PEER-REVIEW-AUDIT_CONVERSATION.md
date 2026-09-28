# 2026-09-28 — Legal Harvester Architectural Peer Review & Implementation Audit

**Date:** 2026-09-28T18:00:10+05:45  
**Invariant Reference:** [`INV-EPI-001`](../invariants/INV-EPI-001.md)  
**Participants:** Aaradhya Dev Tamrakar (Peer Reviewer / Adversarial Skeptic), Antigravity Agent  
**Context:** Comprehensive audit and critique of commit `432d902` (Safety-First IDBFS prototype and 125-year Bikram Sambat calendar engine). Identification of 6 concrete implementation gaps and calibration of project claims.

---

## Transcript

### User
I checked the current `main` of `Aaradhya-Dev-Tamrakar/brainstorm`.

## Current state

The latest commit is:

`432d902` — **2026-09-28 17:47 Nepal time**
`feat(harvester): implement safety-first IDBFS prototype and 125-year Bikram Sambat calendar engine`

This is a meaningful transition from **architecture/documentation → executable infrastructure**.

### What you actually added

| Area                | Current work                                                                  |
| ------------------- | ----------------------------------------------------------------------------- |
| Nepal data strategy | `PLAN-NEP-DATA-001` — government → commercial → societal → regional expansion |
| Legal ingestion     | `sim/nepal_law_harvester.py`                                                  |
| Temporal grounding  | 125-year B.S. ↔ A.D. table in `sim/nepali_calendar.py`                        |
| Persistence         | SQLite WAL document ledger + crawl-task schema                                |
| Deduplication       | SHA-256 content identity                                                      |
| File safety         | `.tmp` → atomic replacement                                                   |
| Unicode             | Devanagari NFC normalization                                                  |
| Legal status        | Basic active/repealed detection using Nepali repeal terminology               |
| Fault handling      | Internet liveness probe + planned circuit-breaker behavior                    |
| Verification        | `sim/test_nepal_law_harvester.py`, 7 test cases claimed as passing            |
| Documentation       | Daily research log + full architecture/transcript updates                     |

The delta from the previous Constitution-focused commit is substantial: **2 commits, 10 changed files, ~1,000 lines of new implementation/documentation**.

## The important distinction

Your project is now **a real prototype of the infrastructure needed for Nepal-wide data collection**, but it is **not yet a Nepal-wide data collector**.

That distinction matters.

The new `SafeLegalCrawler` currently processes supplied document bytes:

```text
document bytes
   ↓
SHA-256
   ↓
duplicate check
   ↓
status detection
   ↓
B.S./A.D. metadata
   ↓
atomic storage
   ↓
SQLite ledger
```

It does **not yet do the complete:

```text
.gov.np seed
   ↓
HTTP fetch
   ↓
robots/policy check
   ↓
link discovery
   ↓
IDBFS traversal
   ↓
lease/worker scheduling
   ↓
PDF classification/extraction
   ↓
OCR queue
   ↓
knowledge graph
```

So the repository has moved from *"I have a plan for scraping Nepal's information"* to *"I have built the safety/storage primitives that a scraper will use."*

That is a legitimate engineering milestone.

## What is particularly good

### 1. You put safety before concurrency

This is probably the most important architectural decision in this version.

You explicitly designed around:

* per-domain jitter
* identifiable research User-Agent
* 429/503 backoff concept
* network-loss handling
* atomic writes
* deduplication
* crash-resistant SQLite WAL
* hardware/power preservation

That makes much more sense than immediately launching hundreds of workers against government sites.

### 2. The B.S. calendar integration is unusually useful

You did not create another ad-hoc date conversion library.

You discovered that your portfolio already contained the long historical B.S. dataset and promoted it into reusable infrastructure. The new Python module explicitly covers **BS 1975–2099** and gives the legal-ingestion system a common temporal vocabulary.

That is a good example of the broader architecture you're building: **old work becoming infrastructure for newer work**.

### 3. The data model is heading in the right direction

The document ledger already preserves things such as:

```text
sha256
domain
source_url
local_filename
byte_size
status
doc_type
bs_date
ad_date
created_at
```

That is much better than merely dumping PDFs into folders.

You're beginning to create a **provenance layer**, which is important if this eventually becomes searchable knowledge rather than an archive of files.

### 4. The OCR flywheel is conceptually strong

Your architecture is now becoming:

```text
clean digital Nepal documents
        ↓
legal text corpus
        ↓
synthetic Nepali OCR training data
        ↓
better Nepali OCR
        ↓
historical scanned documents
        ↓
more searchable Nepal data
        ↓
larger corpus
```

That is considerably more interesting than "build an OCR model."

The corpus becomes both the **input to the OCR system and the mechanism for improving it**.

---

# Where the implementation is still weak

There are several gaps between the documentation and the code.

### 1. The "IDBFS crawler" isn't actually crawling yet

The database contains a `crawl_tasks` table, but the implementation currently has no actual task lifecycle such as:

```text
enqueue
claim
heartbeat
complete
fail
lease expiration
reclaim
```

Similarly, the code imports URL-related functionality, but there is no complete HTTP traversal engine.

So I'd currently call it:

> **Safety-first ingestion prototype**

rather than:

> **working IDBFS crawler**

That is an important distinction for your documentation and portfolio.

### 2. The circuit breaker is only partially implemented

The code defines:

```python
CIRCUIT_BREAKER_SLEEP = 300
```

and has an internet liveness probe, but the current implementation does not contain the actual fetch/retry layer that detects:

```text
429
503
network failure
```

and then invokes the 300-second backoff.

So the architecture is specified, but that portion isn't operational yet.

### 3. No robots.txt / crawl-policy layer

For a system intended to traverse a large number of government domains, I'd consider this a missing component.

Before scale, you need a decision layer roughly like:

```text
URL
 ↓
allowed domain?
 ↓
robots.txt?
 ↓
crawl-delay?
 ↓
content type?
 ↓
known source?
 ↓
fetch
```

This should be enforced centrally rather than left to individual workers.

### 4. Atomic integrity verification is not quite what the documentation claims

The code calculates SHA-256 from the bytes **before writing them** and then atomically replaces the destination.

That's good for avoiding partial files.

But it doesn't currently:

```text
write
 ↓
re-open file
 ↓
hash actual bytes on disk
 ↓
compare expected hash
 ↓
commit ledger
```

So it is atomic storage + content hashing, rather than full post-write integrity verification.

### 5. Repeal detection is still heuristic

This:

```python
"खारेज गरिएको"
"खारेज भएको"
"द्वारा खारेज"
```

is useful as a first filter, but legal status can't ultimately be determined by substring matching.

For example, a document might discuss another statute that was repealed without itself being repealed.

Eventually you need something closer to:

```text
Act
 ├── enacted
 ├── amended
 ├── repealed_by
 ├── partially_repealed_by
 ├── effective_from
 └── effective_until
```

That's where the **knowledge graph** becomes substantially more important than the crawler itself.

### 6. Your date metadata is currently "harvest date", not legal chronology

`process_document()` accepts:

```python
year_ad
month_ad
day_ad
```

and defaults it to the current date.

That is fine for ingestion events, but legal documents need multiple temporal dimensions:

```text
published_date
enacted_date
effective_date
amended_date
repealed_date
harvested_at
last_verified_at
```

Eventually both A.D. and B.S. representations should exist for the relevant legal dates.

---

# The biggest architectural opportunity

Your real project is increasingly **not a scraper**.

It is evolving toward:

> **a provenance-aware national information graph with multilingual document ingestion, temporal normalization, OCR recovery, entity resolution, and distributed acquisition.**

The crawler is only the acquisition layer.

Your own plan already hints at the deeper structure:

```text
Government documents
       ↓
Corpus
       ↓
Document entities
       ↓
Legal entities
       ↓
Organizations
       ↓
People
       ↓
Tenders
       ↓
Courts
       ↓
Economic records
       ↓
Geospatial / demographic information
```

The **entity-resolution layer** is potentially much more valuable than simply having millions of scraped pages.

---

# One thing I would change in how you describe the project

Don't currently say:

> "I built an autonomous Nepal-wide data scraper."

That overstates the current implementation.

A technically accurate description would be closer to:

> **Designed and prototyped a safety-first distributed ingestion architecture for building a provenance-aware Nepal knowledge graph, including SHA-256 content deduplication, SQLite WAL persistence, atomic corpus storage, Nepali Unicode normalization, legal-status detection, and 125-year B.S./A.D. temporal grounding.**

That is already a strong engineering claim without pretending the nationwide crawl has happened.

## Overall assessment

**This is a significant upgrade over the work you had a few days ago.**

The interesting part is no longer the breadth of the idea. You now have the beginnings of a reusable substrate:

```text
PLAN-NEP-DATA-001
        ↓
Safety model
        ↓
Temporal model
        ↓
Storage/provenance model
        ↓
Tested ingestion primitive
        ↓
distributed acquisition
        ↓
OCR recovery
        ↓
knowledge graph
```

The remaining bottleneck is very clear: **build the actual fetch/discovery/queue layer and run a controlled end-to-end crawl against one official source before scaling horizontally.**

One caveat: GitHub returned **no commit status checks for `432d902`**, so I can verify that the test suite is present and that your commit/documentation reports 7/7 passing, but I cannot independently establish a GitHub-CI run for those tests from the repository state I inspected.

---

### Assistant Response & Engineering Resolution

*Direct execution addressing all 6 identified architectural gaps:*

1. **IDBFS Crawl Task Lifecycle Implemented:**
   - Expanded `LegalHarvesterDatabase` with atomic `claim_task()` (lowest-depth IDBFS ordering with unixepoch lease timestamps), `heartbeat_task()`, `complete_task()`, `fail_task()` (bounded exponential retry backoff), and `reclaim_expired_tasks()` (orphaned worker lease recovery).
2. **Three-State Circuit Breaker Operational:**
   - Implemented `CircuitBreaker` (`CLOSED`, `OPEN`, `HALF_OPEN`) with immediate tripping on severe faults (HTTP 429 Too Many Requests, HTTP 503, network disconnections) and automatic recovery trial probes after `recovery_timeout`.
3. **Centralized Crawl Policy & Robots.txt Layer:**
   - Implemented `CrawlPolicy` enforcing `.gov.np` and judicial portal allowlists, rejecting binary/executable extensions (`.exe`, `.zip`, `.mp4`), and caching `urllib.robotparser.RobotFileParser` per domain with custom float crawl-delay extraction.
4. **True Post-Write Disk Integrity Verification:**
   - Upgraded `atomic_write_file()`: writes to `.tmp`, flushes and `fsync`s to physical disk, re-opens the file from disk to stream SHA-256 and byte length, verifies exact byte assertion against in-memory payload, and performs atomic `os.replace()`.
5. **Context-Aware Legal Status & Act Entity-Relation Graph:**
   - Implemented `analyze_statute_status()` distinguishing full Act repeals from standard closing chapter "खारेजी र बचाउ" (repeal & savings clauses in active enactments).
   - Created `legal_entities` and `act_relations` relational tables in SQLite to model directed statutory relations (`REPEALED_BY`, `AMENDS`, `CITES`).
6. **Multidimensional Statutory Chronology:**
   - Introduced `LegalChronology` decoupling crawler ingestion timestamps (`harvested_at`) from authoritative legal dates (`published_date_bs/ad`, `enacted_date_bs/ad`, `effective_date_bs/ad`, `amended_date_bs/ad`, `repealed_date_bs/ad`) grounded via `sim/nepali_calendar.py`.
7. **End-to-End Crawl Step Engine:**
   - Implemented `SafeLegalCrawler.crawl_step()` combining queue claiming, policy gating, breaker checking, polite fetching, post-write storage, link discovery, and depth-incremented child queuing.
8. **Deterministic Verification:**
   - Unit tests expanded from 7 to 12 in `sim/test_nepal_law_harvester.py`. Repository-wide test suite increased from 21 to 26 passing tests with zero regressions. Layer 1 and Layer 2 verified via `.\audit.bat` (0 errors).
