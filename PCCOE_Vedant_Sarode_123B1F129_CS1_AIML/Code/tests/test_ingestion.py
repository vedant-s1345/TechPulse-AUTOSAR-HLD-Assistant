"""
Unit tests for PDF Ingestion Engine.
Verifies valid extraction, scanned page OCR warnings, corrupt file resilience, and page metadata.
"""

import unittest
from pathlib import Path
from src.ingestion import PDFIngestionEngine
from src.config import SYNTHETIC_DATA_DIR

class TestPDFIngestion(unittest.TestCase):

    def setUp(self):
        self.engine = PDFIngestionEngine(min_chars_per_page=20)

    def test_ingest_valid_bms_pdf(self):
        pdf_path = SYNTHETIC_DATA_DIR / "SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf"
        result = self.engine.ingest_file(pdf_path)
        
        self.assertTrue(result.success, f"Ingestion failed: {result.error_message}")
        self.assertEqual(result.total_pages, 3)
        self.assertEqual(len(result.pages), 3)
        self.assertEqual(result.scanned_pages_count, 0)
        
        # Verify page 1 text preservation
        page1 = result.pages[0]
        self.assertEqual(page1.page_num, 1)
        self.assertIn("BATTERY MANAGEMENT SYSTEM", page1.text)
        
        # Verify page 2 SWC text
        page2 = result.pages[1]
        self.assertEqual(page2.page_num, 2)
        self.assertIn("BmsCellSupervisor_SWC", page2.text)

    def test_scanned_dummy_ocr_warning(self):
        pdf_path = SYNTHETIC_DATA_DIR / "SYNTHETIC_SCANNED_DUMMY_OCR_REQUIRED.pdf"
        result = self.engine.ingest_file(pdf_path)
        
        self.assertTrue(result.success)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.scanned_pages_count, 1)
        self.assertTrue(result.pages[0].is_empty_or_scanned)
        self.assertIn("OCR", result.pages[0].warning)

    def test_corrupt_file_handling(self):
        pdf_path = SYNTHETIC_DATA_DIR / "SYNTHETIC_CORRUPTED_FILE.pdf"
        result = self.engine.ingest_file(pdf_path)
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertIn("PDF parsing error", result.error_message)

    def test_nonexistent_file(self):
        result = self.engine.ingest_file("non_existent_file_path.pdf")
        self.assertFalse(result.success)
        self.assertIn("File not found", result.error_message)

if __name__ == "__main__":
    unittest.main()
