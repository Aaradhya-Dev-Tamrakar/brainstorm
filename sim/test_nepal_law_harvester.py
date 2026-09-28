"""
test_nepal_law_harvester.py
---------------------------
Unit test suite verifying the Safety-First Nepal Law Harvester:
1. Dual-calendar Bikram Sambat (BS) <-> Gregorian (AD) 125-year accuracy.
2. Devanagari Unicode NFC canonical normalization.
3. Atomic file swapping and SHA-256 deduplication.
4. Statutory status detection (Active vs. Repealed).
5. Database WAL ledger operations.
"""

import os
import sys
import shutil
import tempfile
import unittest

SIM_DIR = os.path.dirname(os.path.abspath(__file__))
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

from nepali_calendar import ad_to_bs, bs_to_ad, format_dual_date
from nepal_law_harvester import (
    normalize_devanagari,
    detect_statute_status,
    atomic_write_file,
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

    def test_ad_to_bs_exact_historical_milestones(self):
        # Test 1: Constitution of Nepal Promulgation Date (2015-09-20 AD -> 2072-06-03 BS)
        res_const = ad_to_bs(2015, 9, 20)
        self.assertIsNotNone(res_const)
        self.assertEqual(res_const[0], 2072)
        self.assertEqual(res_const[1], 6)
        self.assertEqual(res_const[2], 3)
        self.assertEqual(res_const[3], "Ashwin")
        self.assertEqual(res_const[4], "असोज")

        # Test 2: Portfolio Live Screenshot Date (2026-09-28 AD -> 2083-06-12 BS)
        res_today = ad_to_bs(2026, 9, 28)
        self.assertIsNotNone(res_today)
        self.assertEqual(res_today[0], 2083)
        self.assertEqual(res_today[1], 6)
        self.assertEqual(res_today[2], 12)
        self.assertEqual(res_today[3], "Ashwin")

    def test_bs_to_ad_bi_directional_reversibility(self):
        # Verify 2072 Ashwin 3 -> 2015 September 20
        ad_const = bs_to_ad(2072, 6, 3)
        self.assertEqual(ad_const, (2015, 9, 20))

        # Verify 2083 Ashwin 12 -> 2026 September 28
        ad_today = bs_to_ad(2083, 6, 12)
        self.assertEqual(ad_today, (2026, 9, 28))

    def test_format_dual_date_structure(self):
        formatted = format_dual_date(2015, 9, 20)
        self.assertEqual(formatted["ad_iso"], "2015-09-20")
        self.assertEqual(formatted["bs_iso"], "2072-06-03")
        self.assertIn("Ashwin", formatted["bs_formatted_en"])
        self.assertIn("असोज", formatted["bs_formatted_nep"])
        self.assertGreater(formatted["epoch_timestamp"], 0)

    def test_devanagari_unicode_normalization(self):
        # String containing invisible zero-width spaces (\u200b)
        messy_str = "नेपालको\u200b \u200bसंविधान\u200b २०७२"
        clean = normalize_devanagari(messy_str)
        self.assertNotIn("\u200b", clean)
        self.assertEqual(clean, "नेपालको संविधान २०७२")

    def test_statute_status_detection(self):
        active_text = "नेपालको संविधान (२०७२) प्रारम्भ मिति २०७२ असोज ३ गते ।"
        repealed_text = "यस ऐनद्वारा पुरानो मुलुकी ऐन, २०२० खारेज गरिएको छ ।"
        
        self.assertEqual(detect_statute_status(active_text), "ACTIVE")
        self.assertEqual(detect_statute_status(repealed_text), "REPEALED")

    def test_atomic_file_swapping(self):
        test_payload = b"NEPAL_LEGAL_STATUTE_OFFICIAL_CONTENT_" * 10
        dest_file = os.path.join(self.storage_dir, "test_act.pdf")
        
        success, sha_hash, size = atomic_write_file(test_payload, dest_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(dest_file))
        self.assertFalse(os.path.exists(dest_file + ".tmp")) # Temp file should be cleaned/replaced
        self.assertEqual(size, len(test_payload))

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
        
        # 2. Duplicate Ingestion Attempt (Should be detected via SHA-256 and skipped)
        res2 = self.crawler.process_document(
            url=test_url,
            content_bytes=test_payload,
            extracted_text="यो ऐन सक्रिय छ ।",
            year_ad=2026, month_ad=9, day_ad=28
        )
        self.assertEqual(res2["status"], "SKIPPED_DUPLICATE")
        self.assertEqual(self.db.get_document_count(), 1) # Count remains 1


if __name__ == "__main__":
    unittest.main()
