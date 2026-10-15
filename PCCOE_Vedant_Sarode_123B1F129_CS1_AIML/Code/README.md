# AUTOSAR HLD Document Analysis Assistant
**TechPulse FY-26 Applied AI/ML Capstone Project — Case Study 1 (CS1)**  
**Target Institute:** Pimpri Chinchwad College of Engineering (PCCOE)  
**Academic Year:** 2026  

---

## 1. Project Overview
The **AUTOSAR HLD Document Analysis Assistant** is an engineering-grade document analysis and retrieval system designed to ingest automotive technical documents (specifically AUTOSAR High-Level Design specifications), index their architectural knowledge into a local high-performance vector database, and provide evidence-grounded answers with precise document-name and page-number citations.

### Key Capabilities
- **Multi-Document PDF Ingestion:** Extracts digital text while preserving exact page numbers and document identities. Detects scanned bitmap pages and issues explicit OCR requirements.
- **Context-Aware Chunking:** Splits text with configurable chunk size (default: 500 chars) and overlap (default: 80 chars), enforcing page boundaries so citations never suffer from page-smearing.
- **Local Neural Semantic Search:** Uses `all-MiniLM-L6-v2` (384-dimensional normalized dense vectors running locally on CPU) paired with a persistent **FAISS** (`IndexFlatIP`) cosine similarity vector index.
- **Strict Grounding & Responsible AI Guardrails:** Enforces that all answers derive strictly from retrieved context passages. If evidence is absent, the system explicitly responds: *"The provided document does not provide enough information to answer this question."*
- **Zero-Cost Deterministic Fallback:** Features a deterministic, offline sentence-extraction fallback engine that operates with 100% precision when external LLM APIs are unconfigured or offline.
- **Interactive Streamlit Interface:** Features document upload, ingestion telemetry, interactive Q&A with clickable citation badges, expandable raw evidence inspection, automated architecture entity cataloging, and an evaluator test suite.

---

## 2. Directory Structure
```
Code/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Pinned Python package dependencies
├── .env.example                # Safe environment variable configuration template
├── .gitignore                  # Git ignore rules protecting secrets and caches
├── src/                        # Core application modules
│   ├── __init__.py
│   ├── config.py               # Application settings and environment management
│   ├── ingestion.py            # PDF text extraction and OCR warning engine
│   ├── chunking.py             # Page-preserving text chunker
│   ├── embeddings.py           # Local SentenceTransformers and TF-IDF engines
│   ├── vector_store.py         # FAISS vector database with persistence
│   ├── retriever.py            # Top-K semantic retriever
│   ├── prompts.py              # Strict grounding prompts and injection defense
│   ├── qa_engine.py            # Grounded QA engine (Gemini & Deterministic Fallback)
│   └── extractor.py            # AUTOSAR architecture entity extractor
└── tests/                      # Automated unit and evaluation suites
    ├── __init__.py
    ├── test_ingestion.py       # Unit tests for PDF parsing and OCR detection
    ├── test_chunking.py        # Unit tests for chunking and page metadata
    ├── test_vector_store.py    # Unit tests for FAISS and embeddings
    ├── test_qa_engine.py       # Unit tests for grounding and fallback
    └── run_evaluation.py       # Comprehensive 12-scenario evaluation runner
```

---

## 3. Quick Start & Execution Guide

### Prerequisites
- Python 3.12, 3.13, or 3.14 (Tested on Python 3.14.5 64-bit on Windows)
- Dedicated Python virtual environment (`.venv`)

### Step 1: Virtual Environment Activation
```powershell
# From the project root:
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r Code\requirements.txt
```

### Step 3: Configure Environment (Optional)
Copy `.env.example` to `.env`:
```powershell
Copy-Item Code\.env.example .env
```
*(Note: If no Gemini API key is provided, the system seamlessly defaults to the zero-cost Deterministic Retrieval Fallback mode).*

### Step 4: Run Automated Tests
```powershell
# Run unit tests:
python -m unittest discover -s Code/tests -p "test_*.py"

# Run full evaluation suite:
python Code/tests/run_evaluation.py
```

### Step 5: Launch the Streamlit Web UI
```powershell
streamlit run Code/app.py
```
Open your browser to `http://localhost:8501`.

---

## 4. Evaluator 5-Minute Demonstration Walkthrough
1. **Load Knowledge Base:** In the sidebar under **Knowledge Base Actions**, click **"Load Synthetic AUTOSAR HLD Base"**. This instantly indexes 3 multi-page automotive HLD specifications (Battery Management System, Brake-by-Wire, and ADAS Sensor Fusion).
2. **Execute Sample Queries:** Navigate to the **Architectural Q&A** tab and click any quick-query button (e.g., *⚡ BMS Over-Voltage Flow* or *🛑 Brake-by-Wire ASIL Level*).
3. **Inspect Grounded Answer & Citations:** Observe the verified source citations (e.g., `[SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf, Page 3]`).
4. **Expand Retrieved Evidence:** Open the accordion **"🔍 Inspect Retrieved Evidence Passages"** to view exact cosine similarity scores and raw source paragraphs.
5. **View Extracted Catalog:** Click the **Component & Interface Catalog** tab to view auto-extracted Software Components (`BmsCellSupervisor_SWC`, `PedalSensorReader_SWC`, etc.), Interfaces, and ASIL ratings.
6. **Run Evaluator Suite:** Click the **Evaluator Test Suite** tab and press **"Run Full Automated Evaluation Suite"** to verify all 12 benchmark test cases live in the browser.
