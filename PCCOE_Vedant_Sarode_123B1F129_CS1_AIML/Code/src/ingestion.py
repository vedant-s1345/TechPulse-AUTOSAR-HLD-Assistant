"""
PDF Ingestion Engine for AUTOSAR HLD Document Analysis Assistant.
Handles text extraction, page-level preservation, scanned page detection, and error handling.
"""

import io
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from dataclasses import dataclass, field
import pypdf

@dataclass
class PageData:
    """Represents text and metadata for a single extracted PDF page."""
    doc_name: str
    page_num: int  # 1-indexed
    text: str
    char_count: int
    is_empty_or_scanned: bool = False
    warning: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IngestionResult:
    """Represents the complete result of ingesting one PDF document."""
    doc_name: str
    success: bool
    total_pages: int = 0
    pages: List[PageData] = field(default_factory=list)
    error_message: Optional[str] = None
    scanned_pages_count: int = 0

class PDFIngestionEngine:
    """Robust PDF document ingestion engine with OCR alert and error handling."""

    def __init__(self, min_chars_per_page: int = 20):
        self.min_chars_per_page = min_chars_per_page

    def ingest_file(self, file_source: Union[str, Path, io.BytesIO], filename: Optional[str] = None) -> IngestionResult:
        """
        Ingest a PDF from a filepath or file-like object (e.g. Streamlit UploadedFile).
        """
        if isinstance(file_source, (str, Path)):
            path = Path(file_source)
            doc_name = filename or path.name
            if not path.exists():
                return IngestionResult(doc_name=doc_name, success=False, error_message=f"File not found: {path}")
            try:
                with open(path, "rb") as f:
                    stream = io.BytesIO(f.read())
            except Exception as e:
                return IngestionResult(doc_name=doc_name, success=False, error_message=f"Could not open file: {str(e)}")
        elif hasattr(file_source, "read"):
            doc_name = filename or getattr(file_source, "name", "uploaded_document.pdf")
            try:
                stream = io.BytesIO(file_source.read())
            except Exception as e:
                return IngestionResult(doc_name=doc_name, success=False, error_message=f"Could not read upload buffer: {str(e)}")
        else:
            return IngestionResult(doc_name="unknown", success=False, error_message="Unsupported file source type.")

        try:
            reader = pypdf.PdfReader(stream)
            num_pages = len(reader.pages)
            if num_pages == 0:
                return IngestionResult(
                    doc_name=doc_name,
                    success=False,
                    total_pages=0,
                    error_message="Document has 0 pages or has invalid structure."
                )

            extracted_pages: List[PageData] = []
            scanned_count = 0

            for idx, page in enumerate(reader.pages):
                page_num = idx + 1
                try:
                    raw_text = page.extract_text() or ""
                    cleaned_text = self._clean_text(raw_text)
                    char_len = len(cleaned_text)

                    if char_len < self.min_chars_per_page:
                        scanned_count += 1
                        warning = (
                            f"Page {page_num} contains insufficient extractable text ({char_len} chars). "
                            "This page appears to be a scanned diagram/image requiring OCR."
                        )
                        extracted_pages.append(PageData(
                            doc_name=doc_name,
                            page_num=page_num,
                            text=cleaned_text,
                            char_count=char_len,
                            is_empty_or_scanned=True,
                            warning=warning
                        ))
                    else:
                        extracted_pages.append(PageData(
                            doc_name=doc_name,
                            page_num=page_num,
                            text=cleaned_text,
                            char_count=char_len,
                            is_empty_or_scanned=False,
                            warning=None
                        ))
                except Exception as page_err:
                    scanned_count += 1
                    extracted_pages.append(PageData(
                        doc_name=doc_name,
                        page_num=page_num,
                        text="",
                        char_count=0,
                        is_empty_or_scanned=True,
                        warning=f"Extraction failure on page {page_num}: {str(page_err)}"
                    ))

            return IngestionResult(
                doc_name=doc_name,
                success=True,
                total_pages=num_pages,
                pages=extracted_pages,
                scanned_pages_count=scanned_count
            )

        except pypdf.errors.PdfReadError as pe:
            return IngestionResult(
                doc_name=doc_name,
                success=False,
                error_message=f"PDF parsing error (corrupt or unreadable PDF): {str(pe)}"
            )
        except Exception as e:
            return IngestionResult(
                doc_name=doc_name,
                success=False,
                error_message=f"Unexpected error while ingesting PDF: {str(e)}"
            )

    def _clean_text(self, text: str) -> str:
        """Normalizes whitespace while preserving paragraph boundaries."""
        if not text:
            return ""
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        return cleaned
