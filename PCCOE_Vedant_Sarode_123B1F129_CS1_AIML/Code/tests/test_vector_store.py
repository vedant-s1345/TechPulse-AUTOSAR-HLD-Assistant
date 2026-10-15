"""
Unit tests for FAISS Vector Store and Embeddings.
Verifies embedding generation, FAISS indexing, persistence, and cosine similarity retrieval.
"""

import unittest
import shutil
from pathlib import Path
import numpy as np

from src.embeddings import get_embedding_engine
from src.vector_store import FAISSVectorStore
from src.chunking import TextChunk

class TestVectorStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path("tests/temp_vector_store")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.embedding_engine = get_embedding_engine("tfidf_dense")
        self.dim = self.embedding_engine.get_dimension()
        self.vector_store = FAISSVectorStore(dimension=self.dim)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_indexing_and_search(self):
        chunks = [
            TextChunk(
                chunk_id="doc1_p1_c0",
                doc_name="Doc1.pdf",
                page_num=1,
                chunk_index=0,
                text="BmsCellSupervisor_SWC monitors battery cell voltage and detects over-voltage faults.",
                char_start=0,
                char_end=80,
                token_estimate=12
            ),
            TextChunk(
                chunk_id="doc2_p1_c0",
                doc_name="Doc2.pdf",
                page_num=1,
                chunk_index=0,
                text="PedalSensorReader_SWC reads dual hall-effect sensors for the brake pedal.",
                char_start=0,
                char_end=75,
                token_estimate=11
            )
        ]
        embeddings = self.embedding_engine.embed_documents([c.text for c in chunks])
        self.vector_store.add_chunks(chunks, embeddings)
        self.assertEqual(self.vector_store.total_vectors, 2)

        # Query for battery voltage
        q_vec = self.embedding_engine.embed_query("battery cell over-voltage threshold")
        results = self.vector_store.search(q_vec, top_k=1)
        self.assertEqual(len(results), 1)
        top_chunk, score = results[0]
        self.assertEqual(top_chunk.chunk_id, "doc1_p1_c0")
        self.assertGreater(score, 0.0)

    def test_persistence_save_and_load(self):
        chunk = TextChunk(
            chunk_id="persist_test_c0",
            doc_name="Persist.pdf",
            page_num=3,
            chunk_index=0,
            text="Autonomous Emergency Braking requires ASIL D fail-silent transition.",
            char_start=0,
            char_end=70,
            token_estimate=10
        )
        emb = self.embedding_engine.embed_documents([chunk.text])
        self.vector_store.add_chunks([chunk], emb)
        
        # Save to disk
        self.vector_store.save(self.temp_dir)
        self.assertTrue((self.temp_dir / "faiss_index.bin").exists())
        self.assertTrue((self.temp_dir / "chunks_metadata.pkl").exists())

        # Load from disk
        loaded_store = FAISSVectorStore.load(self.temp_dir)
        self.assertIsNotNone(loaded_store)
        self.assertEqual(loaded_store.total_vectors, 1)
        self.assertEqual(loaded_store.chunks[0].chunk_id, "persist_test_c0")

if __name__ == "__main__":
    unittest.main()
