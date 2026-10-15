"""
Document Retriever module for AUTOSAR HLD Document Analysis Assistant.
Manages semantic search across indexed passages with configurable Top-K and score formatting.
"""

from typing import List, Tuple
from dataclasses import dataclass
from src.chunking import TextChunk
from src.embeddings import BaseEmbeddingEngine
from src.vector_store import FAISSVectorStore

@dataclass
class RetrievedPassage:
    """Represents a retrieved passage with ranking, relevance score, and source metadata."""
    chunk: TextChunk
    score: float
    rank: int

    @property
    def citation_str(self) -> str:
        return f"{self.chunk.doc_name} (Page {self.chunk.page_num})"

class DocumentRetriever:
    """Semantic retrieval coordinator over FAISS vector index."""

    def __init__(self, vector_store: FAISSVectorStore, embedding_engine: BaseEmbeddingEngine):
        self.vector_store = vector_store
        self.embedding_engine = embedding_engine

    def retrieve(self, query: str, top_k: int = 4) -> List[RetrievedPassage]:
        """
        Embeds the query and retrieves the top-K most semantically relevant chunks.
        """
        query_clean = query.strip()
        if not query_clean or self.vector_store.total_vectors == 0:
            return []

        query_vec = self.embedding_engine.embed_query(query_clean)
        raw_results = self.vector_store.search(query_vec, top_k=top_k)

        passages: List[RetrievedPassage] = []
        for rank, (chunk, score) in enumerate(raw_results, start=1):
            passages.append(RetrievedPassage(
                chunk=chunk,
                score=score,
                rank=rank
            ))
        return passages
