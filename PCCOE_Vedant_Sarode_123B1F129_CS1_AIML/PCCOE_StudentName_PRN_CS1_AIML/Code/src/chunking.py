"""
Text Chunking Engine for AUTOSAR HLD Document Analysis Assistant.
Splits page text into configurable chunks with overlap while preserving strict page-level citation traceability.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import re
from src.ingestion import PageData

@dataclass
class TextChunk:
    """Represents an individual text chunk with strict citation metadata."""
    chunk_id: str
    doc_name: str
    page_num: int
    chunk_index: int
    text: str
    char_start: int
    char_end: int
    token_estimate: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def citation_label(self) -> str:
        """Formatted human-readable citation label."""
        return f"{self.doc_name} (Page {self.page_num})"

class TextChunker:
    """
    Context-aware text chunker with configurable size and overlap.
    Crucially, operates on a per-page basis to guarantee that every retrieved passage
    points to an exact, verifiable source page number without page-smearing.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 80):
        if chunk_overlap >= chunk_size:
            raise ValueError(f"Chunk overlap ({chunk_overlap}) cannot be >= chunk size ({chunk_size})")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_page(self, page: PageData) -> List[TextChunk]:
        """Split a single page into overlapping chunks."""
        text = page.text.strip()
        if not text or page.is_empty_or_scanned:
            return []

        # If text is shorter than chunk size, return as a single chunk
        if len(text) <= self.chunk_size:
            return [TextChunk(
                chunk_id=f"{page.doc_name}_p{page.page_num}_c0",
                doc_name=page.doc_name,
                page_num=page.page_num,
                chunk_index=0,
                text=text,
                char_start=0,
                char_end=len(text),
                token_estimate=len(text.split())
            )]

        chunks: List[TextChunk] = []
        step = self.chunk_size - self.chunk_overlap
        start = 0
        chunk_idx = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # If not at the very end of text, attempt to break at a sentence or word boundary
            if end < len(text):
                # Look for sentence boundary (.!?) near end
                boundary_match = re.search(r'[\.\?\!\n]\s+', text[start:end])
                last_space = text[start:end].rfind(' ')
                if last_space > self.chunk_size * 0.7:
                    end = start + last_space

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(TextChunk(
                    chunk_id=f"{page.doc_name}_p{page.page_num}_c{chunk_idx}",
                    doc_name=page.doc_name,
                    page_num=page.page_num,
                    chunk_index=chunk_idx,
                    text=chunk_text,
                    char_start=start,
                    char_end=end,
                    token_estimate=len(chunk_text.split())
                ))
                chunk_idx += 1

            if end >= len(text):
                break
            start += step

        return chunks

    def chunk_pages(self, pages: List[PageData]) -> List[TextChunk]:
        """Process a list of pages across multiple documents."""
        all_chunks: List[TextChunk] = []
        for page in pages:
            all_chunks.extend(self.chunk_page(page))
        return all_chunks
