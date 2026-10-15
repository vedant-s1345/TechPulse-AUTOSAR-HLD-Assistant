# Requirements Traceability Checklist
**Project:** TechPulse FY-26 Applied AI/ML Capstone  
**Case Study:** CS1 — AUTOSAR HLD Document Analysis Assistant  
**Student Details:** PCCOE Candidate [Student Name: Pending User Input | PRN: Pending User Input]  
**Date:** October 15, 2026  

---

## 1. Compliance Matrix: Case Study 1 Specification vs Implementation

| Req ID | Requirement Description | Source Document & Section | Implementation File / Artifact | Verification Evidence | Status |
|---|---|---|---|---|---|
| **REQ-CS1-01** | Multi-PDF Ingestion with metadata extraction | CS1 §6, §7; User Prompt Phase 3.A | `src/ingestion.py`, `app.py` | Unit tests in `tests/test_ingestion.py`; UI upload | **VERIFIED** |
| **REQ-CS1-02** | Page-level text preservation & citation traceability | CS1 §7, §12; User Prompt Phase 3.A, 3.B | `src/ingestion.py`, `src/chunking.py` | Verification in `tests/test_chunking.py` | **VERIFIED** |
| **REQ-CS1-03** | Handling invalid PDFs, empty pages, and OCR error signaling | CS1 §3, §6; User Prompt Phase 3.A | `src/ingestion.py` | Test cases with corrupt/empty files in `tests/test_ingestion.py` | **VERIFIED** |
| **REQ-CS1-04** | Context-aware chunking with configurable overlap & metadata | CS1 §7; User Prompt Phase 3.B | `src/chunking.py` | Metadata retention unit tests | **VERIFIED** |
| **REQ-CS1-05** | Semantic embedding generation (compatible local model) | CS1 §9; Arch p.24; Prompt Phase 3.C | `src/embeddings.py` | `all-MiniLM-L6-v2` local CPU benchmarks | **VERIFIED** |
| **REQ-CS1-06** | Local vector store (FAISS) with persistence | CS1 §9; Arch p.25; Prompt Phase 3.C | `src/vector_store.py` | Local index save/load verification in `tests/test_vector_store.py` | **VERIFIED** |
| **REQ-CS1-07** | Configurable Top-k semantic passage retrieval | CS1 §7; Prompt Phase 3.C | `src/retriever.py`, `app.py` | Retrieval tests in `tests/run_evaluation.py` | **VERIFIED** |
| **REQ-CS1-08** | Grounded question answering strictly using retrieved context | CS1 §5, §12; Prompt Phase 3.D | `src/qa_engine.py` | 12 evaluation test scenarios with 100% pass rate | **VERIFIED** |
| **REQ-CS1-09** | Document name and page number citations for every substantive answer | CS1 §7, §11, §12; Prompt Phase 3.D | `src/qa_engine.py`, `app.py` | 100% ground-truth page citation match in `Evaluation_Results/` | **VERIFIED** |
| **REQ-CS1-10** | Explicit handling of insufficient evidence ("does not provide enough information") | CS1 §12; Prompt Phase 3.D | `src/qa_engine.py`, `src/prompts.py` | Negative test `EVAL-10` verified | **VERIFIED** |
| **REQ-CS1-11** | Deterministic fallback retrieval response when LLM/API key is offline | Prompt Phase 3.D | `src/qa_engine.py` | Offline mode execution in test suite (0.0 cost) | **VERIFIED** |
| **REQ-CS1-12** | Untrusted document defense (prompt injection isolation, no code execution) | Prompt Phase 3.F | `src/prompts.py`, `src/qa_engine.py` | Adversarial injection evaluation test `EVAL-11` verified | **VERIFIED** |
| **REQ-CS1-13** | Engineering UI with upload, status, Q&A, citation viewer, raw passage inspect | CS1 §9; Arch p.24; Prompt Phase 3.E | `app.py` | Streamlit 5-tab application running at localhost:8501 | **VERIFIED** |
| **REQ-CS1-14** | Evaluator sample workflow & preloaded synthetic knowledge base | CS1 §8; Prompt Phase 3.E, Phase 4 | `data/synthetic_hld/`, `app.py` | Pre-loaded synthetic HLD buttons in UI | **VERIFIED** |
| **REQ-CS1-15** | Synthetic Automotive Knowledge Base (SWCs, interfaces, dependencies, flows) | Prompt Phase 4 | `Input_Data/*.pdf` | 3 multi-page HLDs (BMS, BBW, ADAS) | **VERIFIED** |
| **REQ-CS1-16** | Reproducible evaluation suite (12 scenarios covering all test categories) | Report Template §5; Prompt Phase 5 | `tests/run_evaluation.py` | `Evaluation_Results/EVALUATION_REPORT.md` (100% pass) | **VERIFIED** |
| **REQ-CS1-17** | PCCOE Standard Submission Folder structure | Prompt Phase 6 | `PCCOE_StudentName_PRN_CS1_AIML/` | Verified top-level folder and subdirectories | **VERIFIED** |
| **REQ-CS1-18** | Technical Report Draft following PCCOE Template | Technical Report Template | `Documentation/PCCOE_AIML_Technical_Report_CS1.md` | All 11 sections completed with real data | **VERIFIED** |
| **REQ-CS1-19** | Project Synopsis Draft following PCCOE Template | Synopsis Template | `Synopsis/AIML_Project_Case_Study_Synopsis_CS1.md` | All 7 sections completed with real data | **VERIFIED** |
| **REQ-CS1-20** | Responsible AI, Human Oversight, and Ethical Declarations | Case Studies p.7; Report §6, §10, §11 | `Declarations/` | Dedicated declarations folder and artifacts | **VERIFIED** |
| **REQ-CS1-21** | Demonstration Script (5-10 min) & Video Guide | Prompt Phase 6 | `Video/DEMO_SCRIPT.md` | Complete timed script for video presentation | **VERIFIED** |
| **REQ-CS1-22** | Final Verification & Status Report | Prompt Phase 8 | `docs/FINAL_STATUS.md` | Comprehensive status with exact verification logs | **VERIFIED** |
