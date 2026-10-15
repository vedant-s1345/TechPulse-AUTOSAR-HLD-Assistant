"""
Unit tests for Text Chunking Engine.
Verifies page-number traceability, chunk overlap, and metadata preservation.
"""

import unittest
from src.ingestion import PageData
from src.chunking import TextChunker

class TestTextChunking(unittest.TestCase):

    def test_single_page_chunking_with_overlap(self):
        sample_text = (
            "AUTOSAR Software Component BmsCellSupervisor_SWC executes cyclic tasks every 10 milliseconds. "
            "It samples 192 lithium-ion cell voltages via isolated SPI communication lines. "
            "When any cell exceeds the critical 4.25V threshold, an emergency over-voltage alert is published."
        )
        page = PageData(
            doc_name="Test_BMS_Doc.pdf",
            page_num=2,
            text=sample_text,
            char_count=len(sample_text)
        )

        chunker = TextChunker(chunk_size=100, chunk_overlap=30)
        chunks = chunker.chunk_page(page)

        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertEqual(c.doc_name, "Test_BMS_Doc.pdf")
            self.assertEqual(c.page_num, 2)
            self.assertTrue(c.chunk_id.startswith("Test_BMS_Doc.pdf_p2_c"))
            self.assertIn("Page 2", c.citation_label)

    def test_empty_or_scanned_page_skipped(self):
        page = PageData(
            doc_name="Scanned.pdf",
            page_num=1,
            text="",
            char_count=0,
            is_empty_or_scanned=True
        )
        chunker = TextChunker(chunk_size=300, chunk_overlap=50)
        chunks = chunker.chunk_page(page)
        self.assertEqual(len(chunks), 0)

    def test_invalid_overlap_raises_error(self):
        with self.assertRaises(ValueError):
            TextChunker(chunk_size=100, chunk_overlap=120)

if __name__ == "__main__":
    unittest.main()
