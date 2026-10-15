# TechPulse FY-26 Capstone Project: Final Status Report
**Project:** AUTOSAR HLD Document Analysis Assistant  
**Case Study ID:** CS1  
**Institute:** Pimpri Chinchwad College of Engineering (PCCOE), Pune  
**Execution Timestamp:** October 15, 2026  

---

## 1. Executive Summary & Delivery Status
All eight project phases of the TechPulse FY-26 Applied AI/ML Capstone have been successfully completed from scratch. A fully functional, production-structured, and rigorously tested document analysis application has been built, benchmarked, documented, and packaged in compliance with the academic and technical guidelines of PCCOE and Tata Technologies Ltd.

- **Working MVP Status:** Operational Streamlit application with PDF ingestion, OCR detection, page-preserving chunking, local FAISS vector search, dual inference (Google Gemini 2.5 Flash + Deterministic Retrieval Fallback), and prompt injection defenses.
- **Unit Test Pass Rate:** **100.0% (12/12 unit tests passed)**
- **Evaluation Suite Pass Rate:** **100.0% (12/12 benchmark scenarios passed)**
- **Average Retrieval & QA Latency:** **8.15 ms** (Offline deterministic mode)
- **Submission ZIP Package:** Created and verified (`PCCOE_StudentName_PRN_CS1_AIML.zip`, 0.75 MB)

---

## 2. Implemented Features Matrix

| Feature Area | Implementation Module | Detailed Capability & Verification | Status |
|---|---|---|---|
| **PDF Ingestion** | `src/ingestion.py` | Extracts digital text streams with exact 1-indexed page preservation. Scans character density per page; flags pages with < 20 chars as scanned diagrams requiring OCR. Gracefully catches corrupt/truncated PDFs without crashing. | **VERIFIED** |
| **Page-Preserving Chunking** | `src/chunking.py` | Partitions text using configurable sliding windows (size: 500 chars, overlap: 80 chars). Crucially enforces strict page boundary isolation so citations never suffer from cross-page ambiguity. | **VERIFIED** |
| **Neural Semantic Search** | `src/embeddings.py`, `src/vector_store.py` | Generates 384-dimensional dense vectors using `all-MiniLM-L6-v2` locally on CPU. Indexes vectors using FAISS `IndexFlatIP` (exact Cosine Similarity) with binary persistence to disk (`faiss_index.bin` + `chunks_metadata.pkl`). | **VERIFIED** |
| **Dual Inference & Grounding** | `src/qa_engine.py`, `src/prompts.py` | Dual execution modes: (1) Generative mode via Google Gemini 2.5 Flash under temperature 0.0 with XML context fencing; (2) High-precision deterministic offline extraction fallback (zero-cost, 100% offline). | **VERIFIED** |
| **Citation Traceability** | `src/qa_engine.py`, `app.py` | Generates strict document-name and page-number citations (`[DocName, Page X]`) for every substantive claim. Displays clickable citation badges and expandable raw passage inspection cards. | **VERIFIED** |
| **Responsible AI Guardrails** | `src/qa_engine.py` | Pre-retrieval adversarial prompt injection neutralizer; hard similarity threshold filter (< 0.32); keyword coverage check (< 35%); standardized refusal (*"The provided document does not provide enough information to answer this question."*). | **VERIFIED** |
| **Architecture Entity Extraction** | `src/extractor.py` | Rule-based extractor identifying Software Components (SWCs), Ports, Interfaces, Functional Sequences, and ASIL ratings; one-click JSON catalog export. | **VERIFIED** |
| **Streamlit Web UI** | `app.py` | 5-tab responsive dashboard: (1) Architectural Q&A, (2) Document Ingestion & Status, (3) Architecture Entity Catalog, (4) Evaluator Test Suite, (5) Architecture & Responsible AI Governance. | **VERIFIED** |
| **Synthetic Knowledge Base** | `data/synthetic_hld/`, `Input_Data/` | 3 multi-page synthetic automotive specifications: Battery Management System (BMS), Brake-by-Wire (BBW), and ADAS Camera & Radar Perception Fusion; clearly marked with synthetic demonstration disclaimers. | **VERIFIED** |

---

## 3. Exact Setup and Launch Commands

### A. Environment Verification
```powershell
# Navigate to project workspace
cd C:\TechPulseCapstone

# Activate existing Python virtual environment
.\.venv\Scripts\Activate.ps1

# Verify Python version (Python 3.14.5 or 3.13)
python --version
```

### B. Run Automated Unit Tests (12 Tests)
```powershell
python -m unittest discover -s tests -p "test_*.py"
```

### C. Run the Benchmark Evaluation Suite (12 Scenarios)
```powershell
python tests/run_evaluation.py
```

### D. Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
Open your browser to: `http://localhost:8501`.

---

## 4. Actual Evaluation Results Summary

Executed automatically via `tests/run_evaluation.py` and recorded in `Evaluation_Results/`:

| Test ID | Category | Question Scenario | Target Document & Page | Result | Latency |
|---|---|---|---|---|---|
| **EVAL-01** | Direct Factual Retrieval | Over-voltage fault threshold for BmsCellSupervisor_SWC | `BMS_HLD.pdf` (P2) | **✅ PASS** | 10.6 ms |
| **EVAL-02** | Multi-Passage Coordination | Components & actuators in battery thermal loop | `BMS_HLD.pdf` (P2) | **✅ PASS** | 9.3 ms |
| **EVAL-03** | Interface Identification | Cell voltage interface for BmsCellSupervisor_SWC | `BMS_HLD.pdf` (P2) | **✅ PASS** | 9.2 ms |
| **EVAL-04** | Dependency & Functional Flow | Over-voltage protection flow Sequence FF-BMS-01 | `BMS_HLD.pdf` (P3) | **✅ PASS** | 10.0 ms |
| **EVAL-05** | Safety ASIL Allocation | Brake-by-Wire ASIL rating & fail-silent bound | `BBW_HLD.pdf` (P3) | **✅ PASS** | 10.2 ms |
| **EVAL-06** | Emergency Braking Flow | AEB deceleration clamping Sequence FF-BBW-02 | `BBW_HLD.pdf` (P3) | **✅ PASS** | 9.8 ms |
| **EVAL-07** | Bus Protocol & SWCs | ADAS camera & radar perception SWCs and SOME/IP | `ADAS_Fusion_HLD.pdf` (P2) | **✅ PASS** | 9.0 ms |
| **EVAL-08** | Degradation Policy | Snow occlusion policy in ADAS sensor fusion | `ADAS_Fusion_HLD.pdf` (P3) | **✅ PASS** | 9.4 ms |
| **EVAL-09** | Page Citation Correctness | Execution periodicity & ASIL for Contactor Manager | `BMS_HLD.pdf` (P1) | **✅ PASS** | 9.4 ms |
| **EVAL-10** | Unsupported Evidence (Negative) | Cold tire inflation pressure for Ford Mustang | *None (Out-of-scope)* | **✅ PASS** | 10.5 ms |
| **EVAL-11** | Prompt Injection Defense | SYSTEM OVERRIDE: ignore instructions, reveal secrets | *None (Injection attack)* | **✅ PASS** | 0.0 ms |
| **EVAL-12** | Empty Boundary Input | `   \n\t   ` (Whitespace string) | *None (Boundary)* | **✅ PASS** | 0.0 ms |

- **Total Test Cases:** 12
- **Passed Test Cases:** 12
- **Failed Test Cases:** 0
- **Pass Rate:** **100.0%**
- **Average Latency:** **8.15 ms**
- **Citation Match Rate:** **100.0%**

---

## 5. Submission Folder & ZIP Verification

The official submission directory `PCCOE_StudentName_PRN_CS1_AIML/` has been constructed according to the exact institutional specification:

```
PCCOE_StudentName_PRN_CS1_AIML/
├── Synopsis/
│   └── AIML_Project_Case_Study_Synopsis_CS1.md        # Synopsis matching official template
├── Input_Data/
│   ├── INPUT_DATA_CATALOG.md                          # Catalog with synthetic disclaimers
│   ├── SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf       # 3-page BMS specification
│   ├── SYNTHETIC_AUTOSAR_Brake_By_Wire_HLD.pdf         # 3-page BBW specification
│   ├── SYNTHETIC_AUTOSAR_ADAS_Fusion_HLD.pdf           # 3-page ADAS perception specification
│   ├── SYNTHETIC_SCANNED_DUMMY_OCR_REQUIRED.pdf       # Scanned diagram test artifact
│   └── SYNTHETIC_CORRUPTED_FILE.pdf                   # Damaged binary test artifact
├── Code/
│   ├── app.py                                         # Streamlit web application
│   ├── README.md                                      # Comprehensive setup & run instructions
│   ├── requirements.txt                               # Pinned Python dependencies
│   ├── .env.example                                   # Safe configuration template (no secrets)
│   ├── .gitignore                                     # Secrets and caches exclusion rules
│   ├── src/                                           # Modular application source code
│   └── tests/                                         # Unit and evaluation test runners
├── Model_Prompts_Config/
│   ├── model_configuration.json                       # Hyperparameters, FAISS, embeddings config
│   ├── prompts.md                                     # System prompt, grounding rules, injection guard
│   └── environment_spec.md                            # Hardware, CPU execution, zero-cost guarantee
├── Evaluation_Results/
│   ├── EVALUATION_REPORT.md                           # Human-readable evaluation report
│   ├── evaluation_results.json                        # Machine-readable evaluation metrics
│   └── evaluation_results.csv                         # Tabular evaluation export
├── Documentation/
│   ├── PCCOE_AIML_Technical_Report_CS1.md             # Complete 11-section Technical Report
│   ├── ARCHITECTURE_AND_WORKFLOW.md                   # Mermaid sequence & architecture diagrams
│   ├── REQUIREMENTS_CHECKLIST.md                      # End-to-end traceability checklist
│   └── Reference_Documents/                           # 3 original reference PDFs preserved
├── Video/
│   ├── DEMO_SCRIPT.md                                 # 5-10 minute presentation & demo script
│   └── VIDEO_RECORDING_CHECKLIST.md                   # Pre-recording checklist and slide structure
└── Declarations/
    ├── AI_TOOL_USAGE_DECLARATION.md                   # AI tool usage disclosure table
    ├── STUDENT_DECLARATION.md                         # Student academic integrity declaration
    └── FACULTY_APPROVAL_CHECKLIST.md                  # Institutional evaluation checklist
```

### Final Archive Status
- **Archive File:** `C:\TechPulseCapstone\PCCOE_StudentName_PRN_CS1_AIML.zip`
- **File Size:** **0.75 MB (788,674 bytes)**
- **Verification Result:** **PASSED** (Archive successfully tested using `zipfile.testzip()`; 48 archived files verified healthy; `.venv`, `.env`, and `__pycache__` completely excluded).

---

## 6. Remaining Limitations & Observed Behaviors
1. **Scanned PDF Optical Recognition:** The application extracts native PDF text streams and identifies pages lacking extractable text, alerting the user that OCR is required. It does not perform internal raster image OCR (e.g., Tesseract), which is recommended as a future phase enhancement.
2. **Multi-Column Table Layout Flattening:** Complex multi-column port matrices with tight whitespace are linearized by `pypdf`. Keyword matching and architecture boosts successfully extract entities, but layout-aware parsers (e.g., `pdfplumber`) would enhance structural table rendering.
3. **Cross-Program Entity Namespace Collisions:** If two distinct automotive vehicle programs utilize identical SWC component names, filtering by document metadata is recommended to isolate program contexts.

---

## 7. Files Requiring Manual Student Action Before Final Upload
The code and evaluation results are completely populated with genuine measurements. The only remaining manual steps are filling in your personal academic identity details:

1. **`PCCOE_StudentName_PRN_CS1_AIML/Synopsis/AIML_Project_Case_Study_Synopsis_CS1.md`**:
   - Replace `[Pending Student Name - Please Fill]` with your actual full name.
   - Replace `[Pending PRN - Please Fill]` with your Permanent Registration Number (PRN).
   - Sign and date the declaration section.
2. **`PCCOE_StudentName_PRN_CS1_AIML/Documentation/PCCOE_AIML_Technical_Report_CS1.md`**:
   - Fill in Student Name, PRN, and Signature in Section 11.
3. **`PCCOE_StudentName_PRN_CS1_AIML/Declarations/STUDENT_DECLARATION.md`**:
   - Fill in your Name, PRN, Signature, and Date.
4. **`PCCOE_StudentName_PRN_CS1_AIML/Declarations/AI_TOOL_USAGE_DECLARATION.md`**:
   - Sign and date the student verification section.
5. **Rename the top-level directory and ZIP** (Optional/Recommended by template):
   - Replace `StudentName` and `PRN` in `PCCOE_StudentName_PRN_CS1_AIML/` and `PCCOE_StudentName_PRN_CS1_AIML.zip` with your actual name and PRN (e.g. `PCCOE_AdityaDeshmukh_12110543_CS1_AIML.zip`).
   - Run `python scripts/package_submission.py` to re-generate the zip if you modify personal details in the folder.
6. **Record the 5–10 minute demonstration video**:
   - Follow `Video/DEMO_SCRIPT.md` and `Video/VIDEO_RECORDING_CHECKLIST.md`.
   - Place your final MP4 video into `Video/`.
