"""
test_nepal_law_harvester.py
---------------------------
Comprehensive unit test suite verifying the Safety-First Nepal Law Harvester:
1. Dual-calendar Bikram Sambat (BS) <-> Gregorian (AD) 125-year accuracy.
2. Devanagari Unicode NFC canonical normalization and ZWSP cleaning.
3. Post-write disk read integrity verification and SHA-256 deduplication.
4. Statutory status analysis (Repeal vs. Repeal & Savings clause vs. Active).
5. Multidimensional legal chronology (published, enacted, effective across BS/AD).
6. Act entity-relation graph persistence.
7. IDBFS distributed task queue lifecycle (enqueue, claim, lease timeout, reclaim, retry, complete).
8. Three-state circuit breaker transitions (CLOSED, OPEN, HALF_OPEN on 429/503/network drop).
9. Centralized crawl policy & robots.txt compliance.
10. End-to-end controlled crawl step with link discovery.
"""

import os
import sys
import shutil
import tempfile
import unittest
import time

SIM_DIR = os.path.dirname(os.path.abspath(__file__))
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

from nepali_calendar import ad_to_bs, bs_to_ad, format_dual_date, format_dual_from_bs
from nepal_law_harvester import (
    normalize_devanagari,
    detect_statute_status,
    analyze_statute_status,
    atomic_write_file,
    CircuitBreaker,
    CrawlPolicy,
    LegalChronology,
    LegalHarvesterDatabase,
    SafeLegalCrawler
)


class NepalLawHarvesterTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_harvest.db")
        self.storage_dir = os.path.join(self.temp_dir, "corpus")
        self.db = LegalHarvesterDatabase(self.db_path)
        self.crawler = SafeLegalCrawler(self.db, storage_dir=self.storage_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # 1. Temporal Engine Tests
    def test_ad_to_bs_exact_historical_milestones(self):
        # Constitution of Nepal Promulgation Date (2015-09-20 AD -> 2072-06-03 BS)
        res_const = ad_to_bs(2015, 9, 20)
        self.assertIsNotNone(res_const)
        self.assertEqual(res_const[0], 2072)
        self.assertEqual(res_const[1], 6)
        self.assertEqual(res_const[2], 3)
        self.assertEqual(res_const[3], "Ashwin")
        self.assertEqual(res_const[4], "असोज")

        # Portfolio Live Screenshot Date (2026-09-28 AD -> 2083-06-12 BS)
        res_today = ad_to_bs(2026, 9, 28)
        self.assertIsNotNone(res_today)
        self.assertEqual(res_today[0], 2083)
        self.assertEqual(res_today[1], 6)
        self.assertEqual(res_today[2], 12)
        self.assertEqual(res_today[3], "Ashwin")

    def test_bs_to_ad_bi_directional_reversibility(self):
        # 2072 Ashwin 3 -> 2015 September 20
        ad_const = bs_to_ad(2072, 6, 3)
        self.assertEqual(ad_const, (2015, 9, 20))

        # 2083 Ashwin 12 -> 2026 September 28
        ad_today = bs_to_ad(2083, 6, 12)
        self.assertEqual(ad_today, (2026, 9, 28))

    def test_format_dual_date_structure(self):
        formatted = format_dual_date(2015, 9, 20)
        self.assertEqual(formatted["ad_iso"], "2015-09-20")
        self.assertEqual(formatted["bs_iso"], "2072-06-03")
        self.assertIn("Ashwin", formatted["bs_formatted_en"])
        self.assertIn("असोज", formatted["bs_formatted_nep"])
        self.assertGreater(formatted["epoch_timestamp"], 0)

        # Reverse from BS
        dual_from_bs = format_dual_from_bs(2072, 6, 3)
        self.assertEqual(dual_from_bs["ad_iso"], "2015-09-20")

    # 2. Devanagari Normalization
    def test_devanagari_unicode_normalization(self):
        messy_str = "नेपालको\u200b \u200bसंविधान\u200b २०७२"
        clean = normalize_devanagari(messy_str)
        self.assertNotIn("\u200b", clean)
        self.assertEqual(clean, "नेपालको संविधान २०७२")

    # 3. Legal Status Analysis & Repeal vs Savings Distinction
    def test_statute_status_detection(self):
        active_text = "नेपालको संविधान (२०७२) प्रारम्भ मिति २०७२ असोज ३ गते ।"
        repealed_text = "यस ऐनद्वारा पुरानो मुलुकी ऐन, २०२० खारेज गरिएको छ ।"
        savings_text = "परिच्छेद १०: खारेजी र बचाउ । यस ऐन प्रारम्भ हुनु अघिका नियमहरू बमोजिम भएका काम यसै ऐन बमोजिम भएको मानिनेछ ।"
        
        self.assertEqual(detect_statute_status(active_text), "ACTIVE")
        self.assertEqual(detect_statute_status(repealed_text), "REPEALED")
        
        # Savings clause in an act indicates the act is ACTIVE and repeals earlier acts
        savings_evidence = analyze_statute_status(savings_text)
        self.assertEqual(savings_evidence.status, "ACTIVE")
        self.assertIn("खारेजी र बचाउ", savings_evidence.evidence_snippet)

    # 4. Post-Write Disk Integrity Verification
    def test_atomic_file_swapping(self):
        test_payload = b"NEPAL_LEGAL_STATUTE_OFFICIAL_CONTENT_" * 10
        dest_file = os.path.join(self.storage_dir, "test_act.pdf")
        
        success, sha_hash, size = atomic_write_file(test_payload, dest_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(dest_file))
        self.assertFalse(os.path.exists(dest_file + ".tmp"))  # Temp file cleanly replaced
        self.assertEqual(size, len(test_payload))

        # Re-read from disk to confirm exact byte match
        with open(dest_file, "rb") as f:
            disk_content = f.read()
        self.assertEqual(disk_content, test_payload)

    # 5. Crawler Deduplication
    def test_crawler_end_to_end_deduplication(self):
        test_payload = b"OFFICIAL_GAZETTE_CONTENT_BREADTH_FIRST" * 10
        test_url = "https://lawcommission.gov.np/acts/test_act.pdf"
        
        # 1. First Ingestion
        res1 = self.crawler.process_document(
            url=test_url,
            content_bytes=test_payload,
            extracted_text="यो ऐन सक्रिय छ ।",
            year_ad=2026, month_ad=9, day_ad=28
        )
        self.assertEqual(res1["status"], "INGESTED")
        self.assertEqual(res1["bs_date"], "2083-06-12")
        self.assertEqual(self.db.get_document_count(), 1)
        
        # 2. Duplicate Ingestion Attempt (Detected via SHA-256 and skipped)
        res2 = self.crawler.process_document(
            url=test_url,
            content_bytes=test_payload,
            extracted_text="यो ऐन सक्रिय छ ।",
            year_ad=2026, month_ad=9, day_ad=28
        )
        self.assertEqual(res2["status"], "SKIPPED_DUPLICATE")
        self.assertEqual(self.db.get_document_count(), 1)

    # 6. IDBFS Task Queue Lifecycle & Lease Reclamation
    def test_idbfs_task_lifecycle_and_reclamation(self):
        # Enqueue tasks at depth 1 and depth 0
        self.db.enqueue_task("lawcommission.gov.np", "https://lawcommission.gov.np/depth1", depth=1)
        self.db.enqueue_task("lawcommission.gov.np", "https://lawcommission.gov.np/depth0", depth=0)
        
        stats = self.db.get_queue_stats()
        self.assertEqual(stats.get("QUEUED"), 2)

        # IDBFS check: depth 0 must be claimed before depth 1
        t1 = self.db.claim_task(worker_id="worker-A", lease_seconds=1)
        self.assertIsNotNone(t1)
        self.assertEqual(t1["depth"], 0)
        self.assertEqual(t1["url"], "https://lawcommission.gov.np/depth0")

        # Worker heartbeat
        hb = self.db.heartbeat_task(t1["task_id"], worker_id="worker-A", lease_seconds=1)
        self.assertTrue(hb)

        # Wait for 1-second lease to expire
        time.sleep(1.2)
        
        # Reclaim expired leases
        reclaimed = self.db.reclaim_expired_tasks()
        self.assertEqual(reclaimed, 1)

        # Re-claimed by worker-B, then marked complete
        t1_reclaim = self.db.claim_task(worker_id="worker-B", lease_seconds=60)
        self.assertEqual(t1_reclaim["task_id"], t1["task_id"])
        
        comp = self.db.complete_task(t1_reclaim["task_id"], worker_id="worker-B")
        self.assertTrue(comp)

        # Next claimed task should now be depth 1
        t2 = self.db.claim_task(worker_id="worker-B", lease_seconds=60)
        self.assertEqual(t2["depth"], 1)

        # Failure backoff test: fail twice with max_retries=2
        self.db.fail_task(t2["task_id"], worker_id="worker-B", error_message="HTTP 500", max_retries=2)
        # Should be re-queued with retry_count=1
        t2_retry = self.db.claim_task(worker_id="worker-B", lease_seconds=60)
        self.assertEqual(t2_retry["retry_count"], 1)
        # Fail again -> exceeds max_retries, becomes FAILED
        self.db.fail_task(t2_retry["task_id"], worker_id="worker-B", error_message="Fatal error", max_retries=2)
        
        final_stats = self.db.get_queue_stats()
        self.assertEqual(final_stats.get("COMPLETED"), 1)
        self.assertEqual(final_stats.get("FAILED"), 1)

    # 7. Three-State Circuit Breaker Transitions
    def test_circuit_breaker_transitions(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.2)
        self.assertEqual(cb.state, "CLOSED")
        self.assertTrue(cb.can_execute())

        # Mild failure 1
        cb.record_failure(is_severe=False, reason="HTTP_500")
        self.assertEqual(cb.state, "CLOSED")

        # Severe failure (e.g. HTTP 429 Too Many Requests) immediately trips breaker to OPEN
        cb.record_failure(is_severe=True, reason="HTTP_429_RATE_LIMIT")
        self.assertEqual(cb.state, "OPEN")
        self.assertFalse(cb.can_execute())

        # Wait for recovery timeout (0.2s)
        time.sleep(0.25)
        # Transition to HALF_OPEN probe
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, "HALF_OPEN")

        # Probe succeeds -> resets to CLOSED
        cb.record_success()
        self.assertEqual(cb.state, "CLOSED")
        self.assertEqual(cb.consecutive_failures, 0)

    # 8. Centralized Crawl Policy & Robots.txt Compliance
    def test_crawl_policy_and_robots_rules(self):
        policy = CrawlPolicy()

        # Allowed .gov.np domain
        self.assertTrue(policy.is_allowed_domain("lawcommission.gov.np"))
        self.assertTrue(policy.is_allowed_domain("supremecourt.gov.np"))
        self.assertFalse(policy.is_allowed_domain("randomcommercialscraper.com"))

        # Allowed vs Disallowed Content Types
        self.assertTrue(policy.is_target_content_url("https://lawcommission.gov.np/acts/act_123.pdf"))
        self.assertTrue(policy.is_target_content_url("https://lawcommission.gov.np/acts/index.html"))
        self.assertFalse(policy.is_target_content_url("https://lawcommission.gov.np/downloads/setup.exe"))
        self.assertFalse(policy.is_target_content_url("https://lawcommission.gov.np/admin/login"))

        # Inject Robots.txt rules
        mock_robots = """
        User-agent: *
        Disallow: /restricted/
        Crawl-delay: 3.5
        """
        policy.set_robots_txt("lawcommission.gov.np", mock_robots)

        can_crawl_allowed, reason1 = policy.can_crawl("https://lawcommission.gov.np/public/act.pdf")
        self.assertTrue(can_crawl_allowed)
        self.assertEqual(reason1, "ALLOWED")

        can_crawl_disallowed, reason2 = policy.can_crawl("https://lawcommission.gov.np/restricted/draft.pdf")
        self.assertFalse(can_crawl_disallowed)
        self.assertEqual(reason2, "ROBOTS_DISALLOWED")

        # Crawl delay extraction
        delay = policy.get_crawl_delay("lawcommission.gov.np")
        self.assertEqual(delay, 3.5)

    # 9. Multidimensional Statutory Chronology & Entity Graph
    def test_multidimensional_chronology_and_entity_graph(self):
        chrono = LegalChronology(
            published_date_bs="2072-06-03",
            published_date_ad="2015-09-20",
            enacted_date_bs="2072-06-03",
            enacted_date_ad="2015-09-20",
            effective_date_bs="2072-06-03",
            effective_date_ad="2015-09-20"
        )
        
        test_payload = b"NEPAL_CONSTITUTION_2072_MULTIDIMENSIONAL_TEMPORAL_ENTITY" * 5
        res = self.crawler.process_document(
            url="https://lawcommission.gov.np/constitution_2072.pdf",
            content_bytes=test_payload,
            extracted_text="नेपालको संविधान २०७२ । यस ऐनद्वारा पुरानो अन्तरिम संविधान खारेज गरिएको छ ।",
            doc_type="PDF",
            chronology=chrono
        )
        self.assertEqual(res["status"], "INGESTED")
        self.assertEqual(res["legal_status"], "REPEALED")
        entity_id = res["entity_id"]

        # Record a directed Act relation (Constitutional succession / repeal)
        self.db.record_act_relation(
            source_entity_id=entity_id,
            target_title_nep="नेपालको अन्तरिम संविधान, २०६३",
            relation_type="REPEALS",
            section_ref="धारा ३०७"
        )

        relations = self.db.get_entity_relations(entity_id)
        self.assertEqual(len(relations), 2)  # 1 from automated evidence extractor + 1 explicitly added
        self.assertTrue(any(r["target_title_nep"] == "नेपालको अन्तरिम संविधान, २०६३" for r in relations))

    # 10. End-to-End Crawl Step with Link Discovery
    def test_crawl_step_end_to_end_with_link_discovery(self):
        root_url = "https://lawcommission.gov.np/index.html"
        self.db.enqueue_task("lawcommission.gov.np", root_url, depth=0)

        # Mock content provider supplying HTML with child act links
        def mock_provider(url: str):
            if "index.html" in url:
                html = """
                <html>
                <body>
                    <h1>Nepal Acts Portal</h1>
                    <a href="/acts/environment_act.pdf">Environment Protection Act</a>
                    <a href="https://lawcommission.gov.np/acts/companies_act.pdf">Companies Act</a>
                    <a href="/restricted/secret.pdf">Secret Draft</a>
                </body>
                </html>
                """
                return (True, html.encode("utf-8"), 200, "OK")
            elif "environment_act.pdf" in url:
                pdf_bytes = b"ENVIRONMENT_ACT_OFFICIAL_CONTENT_" * 10
                return (True, pdf_bytes, 200, "OK")
            return (False, None, 404, "Not Found")

        # Step 1: Process root page
        step1 = self.crawler.crawl_step(worker_id="worker-crawl-1", max_depth=2, content_provider=mock_provider)
        self.assertEqual(step1["status"], "STEP_COMPLETED")
        self.assertEqual(step1["depth"], 0)
        self.assertGreater(step1["discovered_links"], 0)

        # Check queue stats: root is completed, child links should be queued at depth 1
        stats = self.db.get_queue_stats()
        self.assertEqual(stats.get("COMPLETED"), 1)
        self.assertGreater(stats.get("QUEUED"), 0)

        # Step 2: Process child act at depth 1
        step2 = self.crawler.crawl_step(worker_id="worker-crawl-1", max_depth=2, content_provider=mock_provider)
        self.assertEqual(step2["status"], "STEP_COMPLETED")
        self.assertEqual(step2["depth"], 1)
        self.assertEqual(step2["ingest_result"]["status"], "INGESTED")


if __name__ == "__main__":
    unittest.main()
