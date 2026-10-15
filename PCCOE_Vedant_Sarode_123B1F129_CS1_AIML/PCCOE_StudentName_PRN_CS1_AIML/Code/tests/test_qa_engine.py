"""
Unit tests for Grounded QA Engine and Fallback Mechanism.
Tests grounding, empty query validation, negative evidence response, and citation preservation.
"""

import unittest
from src.embeddings import get_embedding_engine
from src.vector_store import FAISSVectorStore
from src.retriever import DocumentRetriever
from src.qa_engine import GroundedQAEngine
from src.chunking import TextChunk

class TestQAEngine(unittest.TestCase):

    def setUp(self):
        self.embedding_engine = get_embedding_engine("tfidf_dense")
        self.vector_store = FAISSVectorStore(dimension=self.embedding_engine.get_dimension())
        self.retriever = DocumentRetriever(self.vector_store, self.embedding_engine)
        self.qa_engine = GroundedQAEngine(
            retriever=self.retriever,
            provider="offline_deterministic"
        )

        # Index known test chunk
        chunk = TextChunk(
            chunk_id="bms_test_c0",
            doc_name="SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf",
            page_num=2,
            chunk_index=0,
            text="Component Name: BmsCellSupervisor_SWC. Evaluates over-voltage (OV threshold: 4.25V). Interface If_CellVoltageArray.",
            char_start=0,
            char_end=120,
            token_estimate=15
        )
        emb = self.embedding_engine.embed_documents([chunk.text])
        self.vector_store.add_chunks([chunk], emb)

    def test_empty_query_boundary(self):
        resp = self.qa_engine.answer_question("   ")
        self.assertIn("Invalid input", resp.answer)
        self.assertFalse(resp.grounded)

    def test_grounded_answer_and_citation(self):
        resp = self.qa_engine.answer_question("What is the over-voltage threshold for BmsCellSupervisor_SWC?")
        self.assertTrue(resp.grounded)
        self.assertIn("4.25V", resp.answer)
        self.assertIn("SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf", resp.answer)
        self.assertIn("Page 2", resp.answer)

    def test_insufficient_evidence_negative_query(self):
        resp = self.qa_engine.answer_question("What is the tire inflation pressure of a Porsche 911 GT3?")
        self.assertTrue(resp.is_insufficient_evidence or "not provide enough information" in resp.answer.lower())

if __name__ == "__main__":
    unittest.main()
