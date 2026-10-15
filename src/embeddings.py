"""
Embedding Engine for AUTOSAR HLD Document Analysis Assistant.
Generates dense vector embeddings using SentenceTransformers (local CPU) or TF-IDF dense projection.
"""

import os
from typing import List, Union
import numpy as np

class BaseEmbeddingEngine:
    """Base interface for embedding models."""
    def get_dimension(self) -> int:
        raise NotImplementedError
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        raise NotImplementedError

    def embed_query(self, text: str) -> np.ndarray:
        raise NotImplementedError

class SentenceTransformerEngine(BaseEmbeddingEngine):
    """Local neural semantic embedding engine using HuggingFace SentenceTransformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        # Disable symlink warnings on Windows
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = (
            self.model.get_embedding_dimension()
            if hasattr(self.model, "get_embedding_dimension")
            else self.model.get_sentence_embedding_dimension()
        )

    def get_dimension(self) -> int:
        return self.dimension

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimension), dtype="float32")
        # Normalize embeddings for direct cosine similarity calculation via inner product
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.astype("float32")

    def embed_query(self, text: str) -> np.ndarray:
        emb = self.model.encode([text], convert_to_numpy=True, normalize_embeddings=True)
        return emb.astype("float32")

class TfidfDenseEngine(BaseEmbeddingEngine):
    """
    Lightweight deterministic offline fallback embedding using TF-IDF + SVD dense projection.
    Zero external downloads required; instantaneous execution.
    """
    def __init__(self, dimension: int = 128):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD
        from sklearn.preprocessing import normalize
        
        self.dimension = dimension
        self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
        self.svd = TruncatedSVD(n_components=dimension, random_state=42)
        self.is_fitted = False

    def get_dimension(self) -> int:
        return self.dimension

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        from sklearn.preprocessing import normalize
        if not texts:
            return np.empty((0, self.dimension), dtype="float32")
        
        tfidf = self.vectorizer.fit_transform(texts)
        n_features = tfidf.shape[1]
        n_comp = min(self.dimension, n_features, len(texts))
        
        if n_comp < self.dimension:
            # Pad with zeros if corpus is very small
            self.svd.n_components = n_comp
            dense = self.svd.fit_transform(tfidf)
            padded = np.zeros((len(texts), self.dimension), dtype="float32")
            padded[:, :n_comp] = dense
            result = normalize(padded, axis=1)
        else:
            self.svd.n_components = self.dimension
            dense = self.svd.fit_transform(tfidf)
            result = normalize(dense, axis=1)
            
        self.is_fitted = True
        return result.astype("float32")

    def embed_query(self, text: str) -> np.ndarray:
        from sklearn.preprocessing import normalize
        if not self.is_fitted:
            # Return dummy normalized vector if not yet fitted
            v = np.ones((1, self.dimension), dtype="float32")
            return normalize(v, axis=1).astype("float32")
        
        tfidf = self.vectorizer.transform([text])
        dense = self.svd.transform(tfidf)
        padded = np.zeros((1, self.dimension), dtype="float32")
        padded[0, :dense.shape[1]] = dense[0]
        return normalize(padded, axis=1).astype("float32")

def get_embedding_engine(model_type: str = "all-MiniLM-L6-v2") -> BaseEmbeddingEngine:
    """Factory to instantiate the appropriate embedding engine."""
    if model_type == "tfidf_dense":
        return TfidfDenseEngine(dimension=128)
    try:
        return SentenceTransformerEngine(model_name=model_type)
    except Exception as e:
        print(f"[Warning] Failed to initialize SentenceTransformer ({e}). Falling back to TfidfDenseEngine.")
        return TfidfDenseEngine(dimension=128)
