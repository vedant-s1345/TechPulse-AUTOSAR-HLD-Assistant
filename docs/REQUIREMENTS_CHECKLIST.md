# Requirements Traceability Checklist
**Project:** TechPulse FY-26 Applied AI/ML Capstone  
**Case Study:** CS1 — AUTOSAR HLD Document Analysis Assistant  
**Student Details:** PCCOE Candidate [Student Name: Pending User Input | PRN: Pending User Input]  
**Date:** October 15, 2026  

---

## 1. Compliance Matrix: Case Study 1 Specification vs Implementation

| Req ID | Requirement Description | Source Document & Section | Implementation File / Artifact | Verification Evidence | Status |
|---|---|---|---|---|---|
| **REQ-CS1-01** | Multi-PDF Ingestion with metadata extraction | CS1 §6, §7; User Prompt Phase 3.A | `src/ingestion.py`, `app.py` | Unit tests in `tests/test_ingestion.py`; UI upload | Planned / In Progress |
| **REQ-CS1-02** | Page-level text preservation & citation traceability | CS1 §7, §12; User Prompt Phase 3.A, 3.B | `src/ingestion.py`, `src/chunking.py` | Verification in `tests/test_chunking.py` | Planned / In Progress |
| **REQ-CS1-03** | Handling invalid PDFs, empty pages, and OCR error signaling | CS1 §3, §6; User Prompt Phase 3.A | `src/ingestion.py` | Test cases with corrupt/empty files in `tests/test_ingestion.py` | Planned / In Progress |
| **REQ-CS1-04** | Context-aware chunking with configurable overlap & metadata | CS1 §7; User Prompt Phase 3.B | `src/chunking.py` | Metadata retention unit tests | Planned / In Progress |
| **REQ-CS1-05** | Semantic embedding generation (compatible local model) | CS1 §9; Arch p.24; Prompt Phase 3.C | `src/embeddings.py` | Embedding generation benchmark | Planned / In Progress |
| **REQ-CS1-06** | Local vector store (FAISS or compatible local index) with persistence | CS1 §9; Arch p.25; Prompt Phase 3.C | `src/vector_store.py` | Local index save/load verification | Planned / In Progress |
| **REQ-CS1-07** | Configurable Top-k semantic passage retrieval | CS1 §7; Prompt Phase 3.C | `src/retriever.py`, `app.py` | Retrieval hit rate tests in `tests/test_retriever.py` | Planned / In Progress |
| **REQ-CS1-08** | Grounded question answering strictly using retrieved context | CS1 §5, §12; Prompt Phase 3.D | `src/qa_engine.py` | Evaluation suite question set (10+ tests) | Planned / In Progress |
| **REQ-CS1-09** | Document name and page number citations for every substantive answer | CS1 §7, §11, §12; Prompt Phase 3.D | `src/qa_engine.py`, `app.py` | Citation validation in `Evaluation_Results/` | Planned / In Progress |
| **REQ-CS1-10** | Explicit handling of insufficient evidence ("does not provide enough information") | CS1 §12; Prompt Phase 3.D | `src/qa_engine.py`, `src/prompts.py` | Out-of-domain and negative test cases | Planned / In Progress |
| **REQ-CS1-11** | Deterministic fallback retrieval response when LLM/API key is offline | Prompt Phase 3.D | `src/qa_engine.py` | Offline mode execution in test suite | Planned / In Progress |
| **REQ-CS1-12** | Untrusted document defense (prompt injection isolation, no code execution) | Prompt Phase 3.F | `src/prompts.py`, `src/qa_engine.py` | Adversarial injection evaluation test | Planned / In Progress |
| **REQ-CS1-13** | Engineering UI with upload, status, Q&A, citation viewer, raw passage inspect | CS1 §9; Arch p.24; Prompt Phase 3.E | `app.py` | Streamlit interactive smoke test & screenshots | Planned / In Progress |
| **REQ-CS1-14** | Evaluator sample workflow & preloaded synthetic knowledge base | CS1 §8; Prompt Phase 3.E, Phase 4 | `data/synthetic_hld/`, `app.py` | Pre-built automotive HLD documents | Planned / In Progress |
| **REQ-CS1-15** | Synthetic Automotive Knowledge Base (SWCs, interfaces, dependencies, flows) | Prompt Phase 4 | `data/synthetic_hld/*.pdf` | Clearly labelled synthetic AUTOSAR HLD docs | Planned / In Progress |
| **REQ-CS1-16** | Reproducible evaluation suite (10+ scenarios covering all test categories) | Report Template §5; Prompt Phase 5 | `tests/run_evaluation.py` | `Evaluation_Results/evaluation_report.md`, `.json` | Planned / In Progress |
| **REQ-CS1-17** | PCCOE Standard Submission Folder structure | Prompt Phase 6 | `PCCOE_StudentName_PRN_CS1_AIML/` | Verified directory tree & ZIP validation | Planned / In Progress |
| **REQ-CS1-18** | Technical Report Draft following PCCOE Template | Technical Report Template | `Documentation/PCCOE_AIML_Technical_Report_CS1.md` | Complete 11 sections matching template | Planned / In Progress |
| **REQ-CS1-19** | Project Synopsis Draft following PCCOE Template | Synopsis Template | `Synopsis/AIML_Project_Case_Study_Synopsis_CS1.md` | Complete 7 sections matching template | Planned / In Progress |
| **REQ-CS1-20** | Responsible AI, Human Oversight, and Ethical Declarations | Case Studies p.7; Report §6, §10, §11 | `Declarations/`, Report §6 | Governance & Declarations artifacts | Planned / In Progress |
| **REQ-CS1-21** | Demonstration Script (5-10 min) & Video Guide | Prompt Phase 6 | `Video/DEMO_SCRIPT.md` | Step-by-step evaluation guide | Planned / In Progress |
| **REQ-CS1-22** | Final Verification & Status Report | Prompt Phase 8 | `docs/FINAL_STATUS.md` | Comprehensive status with exact commands | Planned / In Progress |

---

## 2. Requirement Verification Tracking

This document will be updated during development as each module passes verification.
