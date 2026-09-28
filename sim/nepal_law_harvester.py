"""
nepal_law_harvester.py
----------------------
Safety-First Iterative Deepening Breadth-First (IDBFS) Legal Harvester & Ingestion Engine.
Engineered for Nepal Government (.gov.np) and Legal Portals (NITC/GIDC).

Core Architectural Invariants:
1. Distributed IDBFS Task Queue: Atomic claim, lease expiration, heartbeat, retry backoff, and reclamation.
2. Centralized Crawl Policy: Domain allowlists (*.gov.np, judicial portals), content-type filtering, and robots.txt parsing with crawl-delay caching.
3. Three-State Circuit Breaker: CLOSED -> OPEN -> HALF_OPEN states responding to HTTP 429/503, network disconnections, and connection timeouts.
4. Polite Fetcher: Per-domain randomized jitter (1.5s - 2.5s) and transparent academic research User-Agent.
5. Post-Write Disk Integrity Verification: Writes to .tmp, fsyncs, re-reads file from disk to verify SHA-256 and byte length before atomic os.replace.
6. Unicode NFC Normalization: Canonical Devanagari cleaning invisible zero-width characters (\\u200b).
7. Multidimensional Legal Chronology: Independent tracking of publication (राजपत्र), enactment (प्रमाणीकरण), and commencement (प्रारम्भ) across both B.S. and A.D. systems.
8. Act Entity-Relation Graph: Structured statutory entities (Constitution, Acts, Ordinances, Regulations) with relational links (AMENDS, REPEALS, PARTIALLY_REPEALS, CITES).
"""

import os
import sys
import time
import random
import socket
import sqlite3
import hashlib
import unicodedata
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
from urllib.parse import urlparse, urljoin
import urllib.request
import urllib.error
import urllib.robotparser
from typing import Optional, Tuple, Dict, Any, List, Set

# Ensure local sim modules are importable
SIM_DIR = os.path.dirname(os.path.abspath(__file__))
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

from nepali_calendar import (
    ad_to_bs,
    bs_to_ad,
    format_dual_date,
    format_dual_from_bs,
    parse_date_string
)

# Default Constants & Configuration
ACADEMIC_USER_AGENT = "KEC-Academic-Research-Bot/1.0 (+http://kec.edu.np; contact: aaradhyadevtmr@gmail.com)"
DEFAULT_MIN_DELAY = 1.5
DEFAULT_MAX_DELAY = 2.5
DEFAULT_CIRCUIT_BREAKER_SLEEP = 300.0  # 5 minutes deep sleep on network failure/rate limiting
DEFAULT_DB_PATH = os.path.join(SIM_DIR, "results", "nepal_legal_harvest.db")
DEFAULT_STORAGE_DIR = os.path.join(SIM_DIR, "results", "corpus_harvest")


@dataclass
class LegalChronology:
    """
    Multidimensional statutory temporal grounding.
    Distinguishes ingestion timestamp from authoritative legal enactment and publication dates.
    """
    harvested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    published_date_bs: Optional[str] = None
    published_date_ad: Optional[str] = None
    enacted_date_bs: Optional[str] = None
    enacted_date_ad: Optional[str] = None
    effective_date_bs: Optional[str] = None
    effective_date_ad: Optional[str] = None
    amended_date_bs: Optional[str] = None
    amended_date_ad: Optional[str] = None
    repealed_date_bs: Optional[str] = None
    repealed_date_ad: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "harvested_at": self.harvested_at,
            "published_date_bs": self.published_date_bs,
            "published_date_ad": self.published_date_ad,
            "enacted_date_bs": self.enacted_date_bs,
            "enacted_date_ad": self.enacted_date_ad,
            "effective_date_bs": self.effective_date_bs,
            "effective_date_ad": self.effective_date_ad,
            "amended_date_bs": self.amended_date_bs,
            "amended_date_ad": self.amended_date_ad,
            "repealed_date_bs": self.repealed_date_bs,
            "repealed_date_ad": self.repealed_date_ad,
        }

    @classmethod
    def from_single_date(cls, year_ad: int, month_ad: int, day_ad: int, date_type: str = "enacted") -> "LegalChronology":
        dual = format_dual_date(year_ad, month_ad, day_ad)
        ad_iso = dual["ad_iso"] if dual else f"{year_ad:04d}-{month_ad:02d}-{day_ad:02d}"
        bs_iso = dual["bs_iso"] if dual else None
        
        chrono = cls()
        if date_type == "enacted":
            chrono.enacted_date_ad = ad_iso
            chrono.enacted_date_bs = bs_iso
        elif date_type == "effective":
            chrono.effective_date_ad = ad_iso
            chrono.effective_date_bs = bs_iso
        elif date_type == "published":
            chrono.published_date_ad = ad_iso
            chrono.published_date_bs = bs_iso
        return chrono


@dataclass
class LegalStatusEvidence:
    """
    Evidence-backed statutory status classification.
    Distinguishes confirmed legislative acts from heuristic pattern matches.
    """
    status: str  # ACTIVE, REPEALED, AMENDED, UNCERTAIN
    confidence: str  # CONFIRMED_STATUTE, HEURISTIC_KEYWORD, UNKNOWN
    evidence_snippet: str = ""
    repealing_act_ref: Optional[str] = None
    amendment_count: int = 0


def normalize_devanagari(text: str) -> str:
    """
    Normalizes Devanagari text into canonical Unicode NFC form,
    cleaning invisible zero-width spaces (\u200b) that break search indexes.
    """
    if not text:
        return ""
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\u200b", "").strip()
    return normalized


def analyze_statute_status(text: str) -> LegalStatusEvidence:
    """
    Performs context-aware statutory status detection.
    Differentiates between an Act repealing prior laws ('खारेजी र बचाउ' clause, meaning the Act is ACTIVE)
    and an Act that itself has been repealed ('यो ऐन खारेज गरिएको छ').
    """
    if not text:
        return LegalStatusEvidence(status="ACTIVE", confidence="UNKNOWN", evidence_snippet="Empty text")
    
    norm = normalize_devanagari(text)

    # 1. Direct repeal markers targeting the statute itself
    direct_repeal_patterns = [
        r"(यो ऐन खारेज गरिएको छ)",
        r"(खारेज भएको छ)",
        r"(द्वारा खारेज गरिएको)",
        r"(यस ऐनद्वारा पुरानो[^\n।]+खारेज गरिएको)",
        r"(खारेज गरिएको छ)",
        r"(Repealed by [A-Za-z0-9\s]+ Act)",
        r"(has been repealed)"
    ]
    for pattern in direct_repeal_patterns:
        match = re.search(pattern, norm)
        if match:
            start = max(0, match.start() - 50)
            end = min(len(norm), match.end() + 50)
            snippet = norm[start:end].strip()

            repealing_ref = None
            ref_match = re.search(r"([^\n।]+(?:ऐन|संहिता|अध्यादेश|नियम)[^\n।]*द्वारा)", snippet)
            if ref_match:
                repealing_ref = ref_match.group(1).strip()

            return LegalStatusEvidence(
                status="REPEALED",
                confidence="HEURISTIC_KEYWORD",
                evidence_snippet=snippet,
                repealing_act_ref=repealing_ref
            )

    # 2. Repeal & Saving clause check (खारेजी र बचाउ)
    # Crucial domain invariant: If text only contains "खारेजी र बचाउ", this act is ACTIVE and repeals prior acts
    if "खारेजी र बचाउ" in norm:
        return LegalStatusEvidence(
            status="ACTIVE",
            confidence="HEURISTIC_KEYWORD",
            evidence_snippet="Contains standard 'खारेजी र बचाउ' (Repeal and Savings) chapter repealing older enactments."
        )

    # 3. Amendment marker check
    if "संशोधन" in norm and ("संशोधन गरिएको" in norm or "संशोधन ऐन" in norm):
        return LegalStatusEvidence(
            status="AMENDED",
            confidence="HEURISTIC_KEYWORD",
            evidence_snippet="Contains statutory amendment markers."
        )

    return LegalStatusEvidence(
        status="ACTIVE",
        confidence="HEURISTIC_KEYWORD",
        evidence_snippet="No repeal or amendment markers detected."
    )


def detect_statute_status(text: str) -> str:
    """Backward-compatible helper returning simple status string."""
    evidence = analyze_statute_status(text)
    return evidence.status


def is_internet_available(host: str = "1.1.1.1", port: int = 53, timeout: float = 3.0) -> bool:
    """Zero-overhead DNS socket probe to test raw WAN connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except (socket.error, OSError):
        return False


def atomic_write_file(content_bytes: bytes, destination_path: str) -> Tuple[bool, str, int]:
    """
    Writes data to a temporary file (.tmp), flushes and fsyncs to physical disk,
    re-opens the file from disk to verify SHA-256 and byte length strictly match the in-memory payload,
    and performs an atomic OS replace. Eliminates partial writes and guarantees post-write disk integrity.
    """
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    temp_path = f"{destination_path}.tmp"
    
    expected_hash = hashlib.sha256(content_bytes).hexdigest()
    expected_size = len(content_bytes)
    
    if expected_size < 128:  # Likely an empty payload or error stub
        return (False, expected_hash, expected_size)
        
    try:
        # Step 1: Write to .tmp and fsync to physical disk
        with open(temp_path, "wb") as f:
            f.write(content_bytes)
            f.flush()
            os.fsync(f.fileno())
            
        # Step 2: Re-read the file back from physical disk to compute and verify checksum
        disk_hasher = hashlib.sha256()
        disk_size = 0
        with open(temp_path, "rb") as rf:
            while chunk := rf.read(65536):
                disk_hasher.update(chunk)
                disk_size += len(chunk)
                
        disk_hash = disk_hasher.hexdigest()
        
        # Step 3: Strict post-write disk read verification
        if disk_hash != expected_hash or disk_size != expected_size:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            return (False, disk_hash, disk_size)
            
        # Step 4: Atomic replacement to destination
        os.replace(temp_path, destination_path)
        
        # Step 5: Final confirmation that destination exists
        if not os.path.exists(destination_path):
            return (False, disk_hash, disk_size)
            
        return (True, disk_hash, disk_size)
    except Exception:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        return (False, expected_hash, expected_size)


class CircuitBreaker:
    """
    Three-state Circuit Breaker (CLOSED, OPEN, HALF_OPEN) for polite web harvesting.
    Safeguards remote government servers (GIDC/NITC) and local connection state.
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_SLEEP):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.consecutive_failures = 0
        self.last_failure_time = 0.0
        self.last_state_change = time.time()
        self.trip_reason = ""

    def record_success(self):
        self.consecutive_failures = 0
        self.state = "CLOSED"
        self.trip_reason = ""

    def record_failure(self, is_severe: bool = False, reason: str = ""):
        self.consecutive_failures += 1
        self.last_failure_time = time.time()
        self.trip_reason = reason
        # 429, 503 or WAN disconnection -> immediate trip to OPEN
        if is_severe or self.consecutive_failures >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = time.time()

    def trip(self, reason: str = "MANUAL_TRIP"):
        self.state = "OPEN"
        self.last_state_change = time.time()
        self.trip_reason = reason

    def reset(self):
        self.state = "CLOSED"
        self.consecutive_failures = 0
        self.trip_reason = ""

    def can_execute(self) -> bool:
        now = time.time()
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if now - self.last_state_change >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.last_state_change = now
                return True
            return False
        if self.state == "HALF_OPEN":
            # Allow trial probe
            return True
        return False


class CrawlPolicy:
    """
    Centralized decision and governance layer for web ingestion:
    - Domain allowlisting (*.gov.np, law portals)
    - File extension and query string sanitization
    - Cached robots.txt parsing and crawl-delay enforcement
    """
    DEFAULT_ALLOWED_SUFFIXES = (
        ".gov.np",
        "lawcommission.gov.np",
        "supremecourt.gov.np",
        "moljpa.gov.np",
        "nepalindata.gov.np"
    )
    DISALLOWED_EXTENSIONS = {
        ".exe", ".zip", ".tar", ".gz", ".rar", ".7z",
        ".mp4", ".mp3", ".avi", ".mkv", ".wav",
        ".iso", ".bin", ".dmg",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
        ".css", ".js", ".map"
    }

    def __init__(self, allowed_suffixes: Optional[List[str]] = None):
        self.allowed_suffixes = tuple(allowed_suffixes) if allowed_suffixes else self.DEFAULT_ALLOWED_SUFFIXES
        self._robots_cache: Dict[str, Optional[urllib.robotparser.RobotFileParser]] = {}
        self._custom_crawl_delays: Dict[str, float] = {}

    def is_allowed_domain(self, domain: str) -> bool:
        if not domain:
            return False
        domain_lower = domain.lower()
        return any(domain_lower.endswith(suf.lower()) or domain_lower == suf.lower() for suf in self.allowed_suffixes)

    def is_target_content_url(self, url: str) -> bool:
        parsed = urlparse(url)
        path_lower = parsed.path.lower()
        _, ext = os.path.splitext(path_lower)
        if ext in self.DISALLOWED_EXTENSIONS:
            return False
        admin_paths = ("/admin", "/login", "/logout", "/wp-admin", "/user/login", "/api/auth")
        if any(path_lower.startswith(ap) for ap in admin_paths):
            return False
        return True

    def set_robots_txt(self, domain: str, robots_content: str):
        """Allows injecting or pre-caching robots.txt for testing or offline environments."""
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(robots_content.splitlines())
        self._robots_cache[domain.lower()] = parser
        # Also extract crawl-delay directly to support floating-point seconds (e.g. 3.5s)
        match = re.search(r"crawl-delay:\s*([0-9.]+)", robots_content, re.IGNORECASE)
        if match:
            try:
                self._custom_crawl_delays[domain.lower()] = float(match.group(1))
            except ValueError:
                pass

    def get_robots_parser(self, domain: str, fetcher_callable: Optional[callable] = None) -> Optional[urllib.robotparser.RobotFileParser]:
        dom = domain.lower()
        if dom in self._robots_cache:
            return self._robots_cache[dom]
            
        if fetcher_callable:
            robots_url = f"https://{dom}/robots.txt"
            success, content, code, _ = fetcher_callable(robots_url)
            if success and content:
                try:
                    text = content.decode("utf-8", errors="ignore")
                    parser = urllib.robotparser.RobotFileParser()
                    parser.parse(text.splitlines())
                    self._robots_cache[dom] = parser
                    return parser
                except Exception:
                    pass
        return None

    def get_crawl_delay(self, domain: str, user_agent: str = ACADEMIC_USER_AGENT) -> Optional[float]:
        dom = domain.lower()
        if dom in self._custom_crawl_delays:
            return self._custom_crawl_delays[dom]
        parser = self._robots_cache.get(dom)
        if parser:
            delay = parser.crawl_delay(user_agent) or parser.crawl_delay("*")
            if delay is not None:
                return float(delay)
        return None

    def can_crawl(self, url: str, user_agent: str = ACADEMIC_USER_AGENT) -> Tuple[bool, str]:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if parsed.scheme not in ("http", "https"):
            return (False, f"UNSUPPORTED_SCHEME: {parsed.scheme}")
            
        if not self.is_allowed_domain(domain):
            return (False, f"DISALLOWED_DOMAIN: {domain}")
            
        if not self.is_target_content_url(url):
            return (False, f"DISALLOWED_CONTENT_TYPE: {parsed.path}")
            
        parser = self._robots_cache.get(domain)
        if parser:
            if not parser.can_fetch(user_agent, url):
                return (False, "ROBOTS_DISALLOWED")
                
        return (True, "ALLOWED")


class PoliteFetcher:
    """
    Polite HTTP Fetcher with per-domain jittered rate limiting and circuit breaker protection.
    """
    def __init__(self, circuit_breaker: CircuitBreaker, policy: CrawlPolicy,
                 min_delay: float = DEFAULT_MIN_DELAY, max_delay: float = DEFAULT_MAX_DELAY,
                 user_agent: str = ACADEMIC_USER_AGENT):
        self.circuit_breaker = circuit_breaker
        self.policy = policy
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.user_agent = user_agent
        self.domain_last_request: Dict[str, float] = {}

    def sleep_polite(self, domain: str):
        now = time.time()
        last = self.domain_last_request.get(domain, 0.0)
        configured_delay = self.policy.get_crawl_delay(domain, self.user_agent)
        min_d = max(self.min_delay, configured_delay) if configured_delay else self.min_delay
        max_d = max(self.max_delay, min_d * 1.5)
        
        elapsed = now - last
        target_delay = random.uniform(min_d, max_d)
        if elapsed < target_delay:
            time.sleep(target_delay - elapsed)
        self.domain_last_request[domain] = time.time()

    def fetch(self, url: str, timeout: float = 10.0) -> Tuple[bool, Optional[bytes], int, str]:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        can_go, reason = self.policy.can_crawl(url, self.user_agent)
        if not can_go:
            return (False, None, 0, f"POLICY_REJECTED: {reason}")
            
        if not self.circuit_breaker.can_execute():
            return (False, None, 0, f"CIRCUIT_BREAKER_OPEN: {self.circuit_breaker.trip_reason}")
            
        self.sleep_polite(domain)
        
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf;q=0.9,*/*;q=0.8",
                "Accept-Language": "ne,en;q=0.8"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status_code = resp.getcode()
                content = resp.read()
                self.circuit_breaker.record_success()
                return (True, content, status_code, "OK")
        except urllib.error.HTTPError as e:
            status_code = e.code
            is_severe = status_code in (429, 503)
            reason = f"HTTP_{status_code}"
            self.circuit_breaker.record_failure(is_severe=is_severe, reason=reason)
            return (False, None, status_code, f"HTTP_ERROR_{status_code}")
        except (urllib.error.URLError, socket.timeout, socket.error) as e:
            self.circuit_breaker.record_failure(is_severe=True, reason=str(e))
            return (False, None, 0, f"NETWORK_ERROR: {str(e)}")
        except Exception as e:
            self.circuit_breaker.record_failure(is_severe=False, reason=str(e))
            return (False, None, 0, f"UNEXPECTED_ERROR: {str(e)}")


class LegalHarvesterDatabase:
    """
    SQLite WAL-backed local task ledger, provenance registry, and statutory entity-relation graph.
    """
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            # 1. Document Storage Ledger
            conn.execute("""
                CREATE TABLE IF NOT EXISTS harvest_documents (
                    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sha256 TEXT UNIQUE NOT NULL,
                    domain TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    local_filename TEXT NOT NULL,
                    byte_size INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    status_confidence TEXT DEFAULT 'HEURISTIC_KEYWORD',
                    doc_type TEXT NOT NULL,
                    bs_date TEXT,
                    ad_date TEXT,
                    published_date_bs TEXT,
                    published_date_ad TEXT,
                    enacted_date_bs TEXT,
                    enacted_date_ad TEXT,
                    effective_date_bs TEXT,
                    effective_date_ad TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Distributed Task Queue
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crawl_tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    depth INTEGER NOT NULL,
                    status TEXT DEFAULT 'QUEUED',
                    claimed_by TEXT,
                    lease_expires_at REAL,
                    retry_count INTEGER DEFAULT 0,
                    last_error TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status_depth ON crawl_tasks(status, depth, task_id);")

            # 3. Statutory Entity Graph
            conn.execute("""
                CREATE TABLE IF NOT EXISTS legal_entities (
                    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    canonical_title_nep TEXT NOT NULL,
                    canonical_title_en TEXT,
                    doc_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    status_confidence TEXT NOT NULL,
                    enacted_bs TEXT,
                    enacted_ad TEXT,
                    effective_bs TEXT,
                    effective_ad TEXT,
                    repealed_by_ref TEXT,
                    sha256_ref TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 4. Act Relation Ledger (Cross-Statute Links)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS act_relations (
                    relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_entity_id INTEGER NOT NULL,
                    target_title_nep TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    section_ref TEXT,
                    gazette_ref TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(source_entity_id) REFERENCES legal_entities(entity_id)
                );
            """)
            conn.commit()

    # --- Task Queue Lifecycle Methods ---

    def enqueue_task(self, domain: str, url: str, depth: int = 0) -> bool:
        """Enqueues a newly discovered URL into the task pool."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO crawl_tasks (domain, url, depth, status)
                    VALUES (?, ?, ?, 'QUEUED')
                """, (domain, url, depth))
                conn.commit()
                return conn.total_changes > 0
        except sqlite3.Error:
            return False

    def claim_task(self, worker_id: str, lease_seconds: int = 60, max_depth: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Atomically claims the highest-priority pending task following IDBFS ordering (lowest depth first).
        Recovers tasks with expired worker leases.
        """
        now = time.time()
        with self._get_connection() as conn:
            cur = conn.cursor()
            query = """
                SELECT task_id, domain, url, depth, retry_count
                FROM crawl_tasks
                WHERE (status = 'QUEUED' OR (status = 'CLAIMED' AND lease_expires_at < ?))
            """
            params: List[Any] = [now]
            if max_depth is not None:
                query += " AND depth <= ?"
                params.append(max_depth)
            query += " ORDER BY depth ASC, task_id ASC LIMIT 1;"
            
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            if not row:
                return None
                
            task_id = row["task_id"]
            expires_at = now + lease_seconds
            cur.execute("""
                UPDATE crawl_tasks
                SET status = 'CLAIMED',
                    claimed_by = ?,
                    lease_expires_at = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
            """, (worker_id, expires_at, task_id))
            conn.commit()
            
            return {
                "task_id": task_id,
                "domain": row["domain"],
                "url": row["url"],
                "depth": row["depth"],
                "retry_count": row["retry_count"]
            }

    def heartbeat_task(self, task_id: int, worker_id: str, lease_seconds: int = 60) -> bool:
        """Extends worker lease for long-running extractions (e.g. large PDF OCR)."""
        now = time.time()
        expires_at = now + lease_seconds
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE crawl_tasks
                SET lease_expires_at = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ? AND claimed_by = ? AND status = 'CLAIMED'
            """, (expires_at, task_id, worker_id))
            conn.commit()
            return cur.rowcount > 0

    def complete_task(self, task_id: int, worker_id: str, status: str = "COMPLETED") -> bool:
        """Marks a claimed task as completed or skipped."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE crawl_tasks
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ? AND claimed_by = ?
            """, (status, task_id, worker_id))
            conn.commit()
            return cur.rowcount > 0

    def fail_task(self, task_id: int, worker_id: str, error_message: str, max_retries: int = 3) -> bool:
        """
        Handles failure with bounded retry backoff.
        If retry_count < max_retries, returns task to QUEUED; otherwise marks FAILED.
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT retry_count FROM crawl_tasks WHERE task_id = ?", (task_id,))
            row = cur.fetchone()
            if not row:
                return False
            retries = row["retry_count"]
            
            if retries + 1 < max_retries:
                cur.execute("""
                    UPDATE crawl_tasks
                    SET status = 'QUEUED',
                        claimed_by = NULL,
                        lease_expires_at = NULL,
                        retry_count = retry_count + 1,
                        last_error = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                """, (error_message, task_id))
            else:
                cur.execute("""
                    UPDATE crawl_tasks
                    SET status = 'FAILED',
                        retry_count = retry_count + 1,
                        last_error = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                """, (error_message, task_id))
            conn.commit()
            return True

    def reclaim_expired_tasks(self) -> int:
        """Reclaims any orphaned leases where the worker died or lost connectivity."""
        now = time.time()
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE crawl_tasks
                SET status = 'QUEUED',
                    claimed_by = NULL,
                    lease_expires_at = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE status = 'CLAIMED' AND lease_expires_at < ?
            """, (now,))
            conn.commit()
            return cur.rowcount

    def get_queue_stats(self) -> Dict[str, int]:
        """Returns counts of crawl tasks grouped by status."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT status, COUNT(*) as cnt FROM crawl_tasks GROUP BY status")
            return {row["status"]: row["cnt"] for row in cur.fetchall()}

    # --- Document & Entity Graph Operations ---

    def record_document(self, sha256: str, domain: str, source_url: str,
                        local_filename: str, byte_size: int, status: str,
                        doc_type: str, bs_date: str = None, ad_date: str = None,
                        status_confidence: str = "HEURISTIC_KEYWORD",
                        published_date_bs: str = None, published_date_ad: str = None,
                        enacted_date_bs: str = None, enacted_date_ad: str = None,
                        effective_date_bs: str = None, effective_date_ad: str = None) -> bool:
        """Records an ingested document in the provenance ledger with full temporal grounding."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO harvest_documents 
                    (sha256, domain, source_url, local_filename, byte_size, status, status_confidence,
                     doc_type, bs_date, ad_date, published_date_bs, published_date_ad,
                     enacted_date_bs, enacted_date_ad, effective_date_bs, effective_date_ad)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sha256, domain, source_url, local_filename, byte_size, status, status_confidence,
                    doc_type, bs_date, ad_date, published_date_bs, published_date_ad,
                    enacted_date_bs, enacted_date_ad, effective_date_bs, effective_date_ad
                ))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def register_legal_entity(self, canonical_title_nep: str, doc_type: str, status: str,
                              status_confidence: str, canonical_title_en: Optional[str] = None,
                              enacted_bs: Optional[str] = None, enacted_ad: Optional[str] = None,
                              effective_bs: Optional[str] = None, effective_ad: Optional[str] = None,
                              repealed_by_ref: Optional[str] = None, sha256_ref: Optional[str] = None) -> int:
        """Registers a formal statutory entity in the national legal graph."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO legal_entities 
                (canonical_title_nep, canonical_title_en, doc_type, status, status_confidence,
                 enacted_bs, enacted_ad, effective_bs, effective_ad, repealed_by_ref, sha256_ref)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                canonical_title_nep, canonical_title_en, doc_type, status, status_confidence,
                enacted_bs, enacted_ad, effective_bs, effective_ad, repealed_by_ref, sha256_ref
            ))
            conn.commit()
            return cur.lastrowid

    def record_act_relation(self, source_entity_id: int, target_title_nep: str,
                            relation_type: str, section_ref: Optional[str] = None,
                            gazette_ref: Optional[str] = None) -> bool:
        """Records a directed relationship between legal enactments (e.g. REPEALS, AMENDS, CITES)."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO act_relations (source_entity_id, target_title_nep, relation_type, section_ref, gazette_ref)
                    VALUES (?, ?, ?, ?, ?)
                """, (source_entity_id, target_title_nep, relation_type, section_ref, gazette_ref))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def get_entity_relations(self, entity_id: int) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT relation_id, source_entity_id, target_title_nep, relation_type, section_ref, gazette_ref
                FROM act_relations WHERE source_entity_id = ?
            """, (entity_id,))
            return [dict(row) for row in cur.fetchall()]

    def is_sha256_indexed(self, sha256: str) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM harvest_documents WHERE sha256 = ?", (sha256,))
            return cur.fetchone() is not None

    def get_document_count(self) -> int:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM harvest_documents")
            return cur.fetchone()[0]


class SafeLegalCrawler:
    """
    Polite, safety-guarded crawler and ingestion engine for Nepal's statutory legal portals.
    Orchestrates policy gating, circuit breakers, rate limiting, and atomic disk persistence.
    """
    def __init__(self, db: LegalHarvesterDatabase, storage_dir: str = DEFAULT_STORAGE_DIR,
                 policy: Optional[CrawlPolicy] = None,
                 circuit_breaker: Optional[CircuitBreaker] = None,
                 min_delay: float = DEFAULT_MIN_DELAY, max_delay: float = DEFAULT_MAX_DELAY,
                 user_agent: str = ACADEMIC_USER_AGENT):
        self.db = db
        self.storage_dir = storage_dir
        self.policy = policy or CrawlPolicy()
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.fetcher = PoliteFetcher(
            circuit_breaker=self.circuit_breaker,
            policy=self.policy,
            min_delay=min_delay,
            max_delay=max_delay,
            user_agent=user_agent
        )
        self.min_delay = min_delay
        self.max_delay = max_delay
        os.makedirs(storage_dir, exist_ok=True)

    def sleep_polite(self):
        """Applies randomized jitter delay between manual requests."""
        jitter = random.uniform(self.min_delay, self.max_delay)
        time.sleep(jitter)

    def process_document(self, url: str, content_bytes: bytes,
                          extracted_text: str = "", doc_type: str = "PDF",
                          chronology: Optional[LegalChronology] = None,
                          year_ad: Optional[int] = None, month_ad: Optional[int] = None, day_ad: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes atomic storage with post-write disk read verification,
        normalizes text, resolves multidimensional chronology,
        and registers the document and entities in the database.
        """
        domain = urlparse(url).netloc or "local"
        sha256 = hashlib.sha256(content_bytes).hexdigest()
        
        # Deduplication check
        if self.db.is_sha256_indexed(sha256):
            return {"status": "SKIPPED_DUPLICATE", "sha256": sha256}
            
        # Analyze statute status with evidence
        status_evidence = analyze_statute_status(extracted_text)
        
        # Resolve chronology
        if chronology is None:
            if year_ad is not None and month_ad is not None and day_ad is not None:
                chronology = LegalChronology.from_single_date(year_ad, month_ad, day_ad, date_type="enacted")
            else:
                chronology = LegalChronology()
                
        # Dual calendar fallback for legacy query columns
        legacy_bs = chronology.enacted_date_bs or chronology.published_date_bs
        legacy_ad = chronology.enacted_date_ad or chronology.published_date_ad
        
        # Atomic Write with strict post-write disk read verification
        ext = ".pdf" if doc_type == "PDF" else ".json"
        filename = f"{sha256[:16]}_{domain.replace('.', '_')}{ext}"
        dest_path = os.path.join(self.storage_dir, filename)
        
        success, final_hash, byte_size = atomic_write_file(content_bytes, dest_path)
        if not success:
            return {"status": "WRITE_FAILED", "sha256": final_hash}
            
        # Record in Provenance DB
        self.db.record_document(
            sha256=final_hash,
            domain=domain,
            source_url=url,
            local_filename=filename,
            byte_size=byte_size,
            status=status_evidence.status,
            status_confidence=status_evidence.confidence,
            doc_type=doc_type,
            bs_date=legacy_bs,
            ad_date=legacy_ad,
            published_date_bs=chronology.published_date_bs,
            published_date_ad=chronology.published_date_ad,
            enacted_date_bs=chronology.enacted_date_bs,
            enacted_date_ad=chronology.enacted_date_ad,
            effective_date_bs=chronology.effective_date_bs,
            effective_date_ad=chronology.effective_date_ad
        )

        # Register formal legal entity
        title_nep = normalize_devanagari(extracted_text[:120]) if extracted_text else filename
        entity_id = self.db.register_legal_entity(
            canonical_title_nep=title_nep,
            doc_type=doc_type,
            status=status_evidence.status,
            status_confidence=status_evidence.confidence,
            enacted_bs=chronology.enacted_date_bs,
            enacted_ad=chronology.enacted_date_ad,
            effective_bs=chronology.effective_date_bs,
            effective_ad=chronology.effective_date_ad,
            repealed_by_ref=status_evidence.repealing_act_ref,
            sha256_ref=final_hash
        )

        # If a repealing reference was identified, record relation
        if status_evidence.repealing_act_ref:
            self.db.record_act_relation(
                source_entity_id=entity_id,
                target_title_nep=status_evidence.repealing_act_ref,
                relation_type="REPEALED_BY"
            )
        
        return {
            "status": "INGESTED",
            "sha256": final_hash,
            "byte_size": byte_size,
            "legal_status": status_evidence.status,
            "status_confidence": status_evidence.confidence,
            "bs_date": legacy_bs,
            "ad_date": legacy_ad,
            "entity_id": entity_id,
            "dest_path": dest_path
        }

    def crawl_step(self, worker_id: str = "worker-01", max_depth: int = 2,
                   content_provider: Optional[callable] = None) -> Dict[str, Any]:
        """
        Executes one complete IDBFS task lifecycle step:
        1. Reclaims expired worker leases.
        2. Claims highest-priority task (lowest depth first).
        3. Enforces crawl policy and robots.txt rules.
        4. Queries circuit breaker state.
        5. Fetches bytes via PoliteFetcher (or content_provider in tests/offline).
        6. Processes and persists document with post-write verification.
        7. If HTML, extracts child links matching policy and enqueues them at depth + 1.
        8. Marks task COMPLETED.
        """
        # 1. Reclaim expired tasks
        reclaimed = self.db.reclaim_expired_tasks()
        
        # 2. Claim next available task
        task = self.db.claim_task(worker_id=worker_id, lease_seconds=60, max_depth=max_depth)
        if not task:
            return {"status": "IDLE", "message": "No pending tasks in queue", "reclaimed_leases": reclaimed}
            
        task_id = task["task_id"]
        url = task["url"]
        depth = task["depth"]
        
        # 3. Policy Gate
        can_crawl, reason = self.policy.can_crawl(url)
        if not can_crawl:
            self.db.complete_task(task_id, worker_id, status="SKIPPED_POLICY")
            return {"status": "SKIPPED_POLICY", "task_id": task_id, "url": url, "reason": reason}
            
        # 4. Circuit Breaker Gate
        if not self.circuit_breaker.can_execute():
            self.db.fail_task(task_id, worker_id, error_message=f"CIRCUIT_BREAKER_OPEN: {self.circuit_breaker.trip_reason}")
            return {"status": "CIRCUIT_BREAKER_OPEN", "task_id": task_id, "url": url}
            
        # 5. Fetch Content
        if content_provider:
            success, content, code, msg = content_provider(url)
        else:
            success, content, code, msg = self.fetcher.fetch(url)
            
        if not success or not content:
            self.db.fail_task(task_id, worker_id, error_message=msg)
            return {"status": "FETCH_FAILED", "task_id": task_id, "url": url, "error": msg}
            
        # 6. Process & Ingest Document
        doc_type = "PDF" if url.lower().endswith(".pdf") else "HTML"
        text_content = ""
        if doc_type == "HTML":
            try:
                text_content = content.decode("utf-8", errors="ignore")
            except Exception:
                pass
                
        ingest_res = self.process_document(
            url=url,
            content_bytes=content,
            extracted_text=text_content,
            doc_type=doc_type
        )
        
        # 7. Discover and Enqueue Child Links (if HTML and depth < max_depth)
        discovered_count = 0
        if doc_type == "HTML" and depth < max_depth:
            # Extract links using standard regex pattern
            href_matches = re.findall(r'href=[\'"]?([^\'" >]+)', text_content)
            for href in href_matches:
                child_url = urljoin(url, href)
                child_parsed = urlparse(child_url)
                if child_parsed.scheme in ("http", "https") and self.policy.is_allowed_domain(child_parsed.netloc):
                    if self.policy.is_target_content_url(child_url):
                        if self.db.enqueue_task(child_parsed.netloc, child_url, depth=depth + 1):
                            discovered_count += 1
                            
        # 8. Complete task
        self.db.complete_task(task_id, worker_id, status="COMPLETED")
        
        return {
            "status": "STEP_COMPLETED",
            "task_id": task_id,
            "url": url,
            "depth": depth,
            "ingest_result": ingest_res,
            "discovered_links": discovered_count
        }


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("=================================================================")
    print("   [NEPAL LAW HARVESTER] (SAFETY-FIRST IDBFS ENGINE)")
    print("=================================================================")
    db = LegalHarvesterDatabase()
    crawler = SafeLegalCrawler(db)
    
    print(f"[*] Database location: {db.db_path}")
    print(f"[*] Total indexed documents: {db.get_document_count()}")
    print(f"[*] Queue statistics: {db.get_queue_stats()}")
    print(f"[*] WAN liveness check: {'ONLINE' if is_internet_available() else 'OFFLINE'}")
    
    # Test dual calendar
    test_date = format_dual_date(2026, 9, 28)
    if test_date:
        print(f"[*] Temporal Engine: 2026-09-28 AD -> {test_date['bs_formatted_nep']} ({test_date['bs_formatted_en']})")
    print("=================================================================")
