"""
FAISS Vector Store with Local Persistence for AUTOSAR HLD Document Analysis Assistant.
Indexes normalized embeddings using FAISS IndexFlatIP (Cosine Similarity) and persists metadata.
"""

import json
import pickle
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
import faiss

from src.chunking import TextChunk

class FAISSVectorStore:
    """Local FAISS vector index with metadata persistence and cosine similarity search."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product on normalized vectors = Cosine Similarity
        self.chunks: List[TextChunk] = []

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal if self.index else 0

    def add_chunks(self, chunks: List[TextChunk], embeddings: np.ndarray) -> None:
        """Add text chunks and corresponding embedding vectors to the index."""
        if len(chunks) == 0:
            return
        if len(chunks) != embeddings.shape[0]:
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {embeddings.shape[0]} embeddings.")
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} does not match index dimension {self.dimension}.")

        # Ensure float32 and contiguous
        embeddings_np = np.ascontiguousarray(embeddings, dtype="float32")
        self.index.add(embeddings_np)
        self.chunks.extend(chunks)

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> List[Tuple[TextChunk, float]]:
        """
        Query the index and return top_k most similar chunks with cosine similarity score.
        """
        if self.total_vectors == 0:
            return []

        query_np = np.ascontiguousarray(query_vector, dtype="float32")
        k = min(top_k, self.total_vectors)
        scores, indices = self.index.search(query_np, k)

        results: List[Tuple[TextChunk, float]] = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1 and idx < len(self.chunks):
                results.append((self.chunks[idx], float(score)))

        return results

    def save(self, directory: Path) -> None:
        """Save FAISS index and chunk metadata to a local directory."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        index_file = directory / "faiss_index.bin"
        metadata_file = directory / "chunks_metadata.pkl"

        faiss.write_index(self.index, str(index_file))
        with open(metadata_file, "wb") as f:
            pickle.dump({
                "dimension": self.dimension,
                "chunks": self.chunks
            }, f)

    @classmethod
    def load(cls, directory: Path) -> Optional["FAISSVectorStore"]:
        """Load an existing FAISS index and metadata from disk."""
        directory = Path(directory)
        index_file = directory / "faiss_index.bin"
        metadata_file = directory / "chunks_metadata.pkl"

        if not index_file.exists() or not metadata_file.exists():
            return None

        index = faiss.read_index(str(index_file))
        with open(metadata_file, "rb") as f:
            data = pickle.load(f)

        store = cls(dimension=data["dimension"])
        store.index = index
        store.chunks = data["chunks"]
        return store

    def clear(self) -> None:
        """Reset the index and metadata."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunks = []
