# TATA TECHNOLOGIES LTD.
## TECH PULSE FY-26 | AI/ML Capstone Project
# PROJECT SYNOPSIS

---

### Student Details
- **Institute / University:** Pimpri Chinchwad College of Engineering (PCCOE), Pune
- **Programme / Batch:** B.Tech / M.Tech — Artificial Intelligence & Machine Learning (TechPulse FY-26)
- **Student Name:** `[Pending Student Name - Please Fill]`
- **PRN:** `[Pending PRN - Please Fill]`

---

### 1. Case Study ID and Project Title / Topic
- **Case Study ID (CS1 to CS5):** **CS1**
- **Project Title / Topic:** **AUTOSAR HLD Document Analysis Assistant**

---

### 2. Objectives
Define the specific objectives and focus areas of the allocated AIML case study:
- Develop an automated document-analysis and retrieval pipeline that ingests complex, multi-page automotive technical PDF documents (AUTOSAR High-Level Design specifications).
- Improve architectural traceability by extracting and indexing software components (SWCs), ports, interfaces (Sender-Receiver, Client-Server), dependencies, and functional flows.
- Implement a semantic vector search system using a local vector database (FAISS) and domain-compatible dense neural embeddings (`all-MiniLM-L6-v2`).
- Provide strictly grounded natural language question answering with mandatory document-name and page-number citations, eliminating hallucinations and ensuring auditability.
- Incorporate robust error handling for unextractable/scanned documents, an adversarial prompt injection defense layer, and a deterministic offline retrieval fallback engine.

---

### 3. Scope
Clearly state what will be implemented in the project and what will not be covered:

#### In Scope — To Be Implemented:
- Ingestion of single and multi-document technical PDFs with preservation of page boundaries, metadata, and document identities.
- Page-level context-aware chunking with configurable chunk sizes and overlaps to prevent cross-page citation degradation.
- Scanned PDF and non-extractable text page detection with explicit OCR error flagging.
- Local dense embedding generation using SentenceTransformers (`all-MiniLM-L6-v2`) and fallback TF-IDF + SVD.
- Local persistent vector storage using FAISS `IndexFlatIP` (Cosine Similarity) with save/load capability.
- Configurable Top-K semantic retrieval and relevance score reporting.
- Grounded question answering using Google Gemini API (`gemini-2.5-flash`) with strict grounding prompts.
- Deterministic retrieval fallback engine for 100% offline, zero-cost operation when external LLM APIs are absent.
- Standardized insufficient evidence response: *"The provided document does not provide enough information to answer this question."*
- Interactive engineering web application built in Streamlit.
- Automated architecture entity catalog extraction (SWCs, ports, interfaces, functional flows, ASIL ratings).
- Reproducible automated evaluation suite with 12 benchmark test scenarios.

#### Out of Scope — Will Not Be Implemented:
- Automatic, unreviewed approval of automotive safety or architecture decisions.
- Direct automated modification or rewriting of approved source HLD documents without qualified human engineering review.
- Replacement of formal engineering safety governance (ISO 26262 ASIL sign-offs) or certified toolchain qualifications.
- Optical Character Recognition (OCR) runtime rasterization of scanned images (detection and warning provided; external OCR engine out of pilot scope).
- Automated generation of production C/C++ ECU code from design documents.

---

### 4. Proposed Approach
- **Pre-trained Model (name, version, local/private hosting):**  
  Google Gemini 2.5 Flash (`gemini-2.5-flash`) via `google-genai` SDK, operating under temperature `0.0` with strict context-bounding system instructions; and a deterministic offline sentence-extraction fallback engine.
- **Embedding Model:**  
  `all-MiniLM-L6-v2` (HuggingFace SentenceTransformers, 384-dimensional dense vectors, L2-normalized for cosine similarity, executed locally on CPU) with an offline fallback using scikit-learn TF-IDF + SVD.
- **Vector Store (FAISS / ChromaDB):**  
  **FAISS** (`faiss-cpu` v1.15.1) utilizing `IndexFlatIP` (Inner Product on unit vectors = exact Cosine Similarity). Local filesystem persistence storing binary index vectors (`faiss_index.bin`) and chunk metadata (`chunks_metadata.pkl`).
- **RAG Pipeline and/or AI-Agent Design:**  
  Custom modular Python pipeline: PDF Ingestion -> Page Data Normalization -> Page-Preserving Text Chunking -> FAISS Indexing -> Query Vectorization -> Top-K Semantic Retrieval -> Prompt Injection Guard -> Strict Grounded QA Generation -> Citation Verification.
- **Service Layer and UI:**  
  Streamlit 1.66.0 web user interface providing interactive document upload, sidebar configuration, grounded Q&A, citation badges, expandable retrieved evidence inspection, architectural entity catalog, and an evaluator test runner.
- **Tools / Deterministic Rules:**  
  Deterministic keyword coverage and similarity thresholding (< 0.32), prompt injection regex pattern neutralizing, and rule-based AUTOSAR regex extractor for SWCs, ports, interfaces, and ASIL ratings.
- **Proposed System / Architecture Diagram:**  
  *(See detailed diagram in `Documentation/ARCHITECTURE_AND_WORKFLOW.md`)*

---

### 5. Input Data / Knowledge Base
- **Data / Knowledge Sources:**  
  Curated synthetic automotive engineering High-Level Design (HLD) specifications specifically authored for evaluation:
  1. `SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf` (Battery Management System)
  2. `SYNTHETIC_AUTOSAR_Brake_By_Wire_HLD.pdf` (Brake-by-Wire Electronic System)
  3. `SYNTHETIC_AUTOSAR_ADAS_Fusion_HLD.pdf` (Camera & Radar Sensor Fusion)
  4. `SYNTHETIC_SCANNED_DUMMY_OCR_REQUIRED.pdf` (Scanned page test artifact)
  5. `SYNTHETIC_CORRUPTED_FILE.pdf` (Malformed file test artifact)
- **Approximate Size and Format:**  
  Vector and text-layer PDFs, 1 to 3 pages each, totaling ~15 KB to 30 KB per document; ~25 total text chunks indexed.
- **Preprocessing and EDA Planned:**  
  Text extraction via `pypdf`, string normalization, paragraph boundary detection, empty page screening, character length threshold checks (< 20 chars flagged for OCR), and per-page chunking with overlap.

---

### 6. Expected Outcomes and Evaluation Plan
- **Expected Outputs (aligned to the case study):**  
  - Functional Streamlit engineering web application.
  - Evidence-grounded answers citing exact document names and page numbers.
  - Auto-extracted architecture catalog in structured table and JSON format.
  - Verified evaluation results report covering 12 test cases with 100% pass rate.
- **Evaluation Method:**  
  Automated test suite (`tests/run_evaluation.py`) executing 12 test cases across 8 categories: Direct Factual Retrieval, Multi-Passage Synthesis, Component Identification, Functional Flow Sequence, Safety ASIL Allocation, Degradation Policy, Unsupported Queries (Negative testing), Adversarial Injection Defense, and Empty Input Handling. Metrics recorded: Pass/Fail status, ground-truth page citation validity, and response latency.
- **Responsible AI Measures:**  
  - Mandatory source citations: `[Document, Page X]`.
  - Refusal to guess or hallucinate when evidence is absent.
  - Adversarial prompt injection defense treating document content as untrusted plain text data.
  - Zero private data transmission; local vector database and offline execution capability.
- **MLOps / Deployment Elements Planned:**  
  Dependency pinning via `requirements.txt`, safe configuration via `.env.example`, git secret protection via `.gitignore`, modular test harness via `unittest`, and standalone portability.

---

### 7. Planned AI-Tool Usage
- **AI Tool / Model:** Claude / Gemini / GitHub Copilot
- **Purpose:** Accelerated drafting of boilerplate code, test harness scaffolding, and Markdown documentation formatting.
- **Artifact Affected:** Source code modules in `src/`, unit tests in `tests/`, and report drafts.

---

### Student Declaration
- [X] I will not change the approved case-study scope, major methodology, or implementation approach without prior faculty approval.
- [X] I confirm that the work submitted under this synopsis represents my own understanding and contribution, and I will be responsible for explaining every significant part of the selected case study and its implementation.

**Name:** `[Pending Student Name]`  
**PRN:** `[Pending PRN]`  
**Signature:** ______________________________  
**Date:** `[Pending Date, e.g. October 15, 2026]`  

---

### Faculty Approval
- [ ] Approved as submitted
- [ ] Approved with modifications noted below
- [ ] Resubmission required

**Faculty Reviewer Name:** ______________________________  
**Faculty Signature:** ______________________________  
**Date:** ______________________________  
