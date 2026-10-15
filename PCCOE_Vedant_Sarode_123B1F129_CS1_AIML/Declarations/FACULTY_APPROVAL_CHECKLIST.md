# Faculty Approval & Capstone Evaluation Checklist
**TechPulse FY-26 Applied AI/ML Capstone — Case Study 1 (CS1)**  
**Institute:** Pimpri Chinchwad College of Engineering (PCCOE), Pune  
**Project Title:** AUTOSAR HLD Document Analysis Assistant  

---

### Student Submission Identification
- **Student Name:** `[Pending Student Name - To Be Filled by Candidate]`
- **PRN:** `[Pending PRN - To Be Filled by Candidate]`
- **Evaluation Panel / Guide:** `[Faculty Guide Name]`
- **Review Date:** `[Review Date]`

---

## 1. Compliance & Deliverables Verification Checklist

| Deliverable / Requirement | Faculty Criteria | Evaluation Status | Remarks / Faculty Notes |
|---|---|---|---|
| **1. Project Synopsis** | Synopsis matches official PCCOE template; defines 7 required sections; scope matches Case Study 1. | ☐ Approved<br/>☐ Needs Revision | |
| **2. Technical Report** | 11 complete sections following official template; includes architecture diagram, measured metrics, responsible AI measures. | ☐ Approved<br/>☐ Needs Revision | |
| **3. Working Codebase** | Modular architecture in `src/`; runnable Streamlit app; reproducible `requirements.txt` and `.env.example`. | ☐ Approved<br/>☐ Needs Revision | |
| **4. Ingestion & OCR Detection** | Extracts text with page retention; flags scanned pages and corrupt files gracefully. | ☐ Approved<br/>☐ Needs Revision | |
| **5. Chunking & Traceability** | Chunking preserves source page boundaries without cross-page citation degradation. | ☐ Approved<br/>☐ Needs Revision | |
| **6. Semantic Retrieval & FAISS** | Local vector store (FAISS) with dense embeddings (`all-MiniLM-L6-v2`); local persistence verified. | ☐ Approved<br/>☐ Needs Revision | |
| **7. Grounding & Citations** | Explicit citations `[DocName, Page X]`; refuses out-of-scope queries; zero hallucinations. | ☐ Approved<br/>☐ Needs Revision | |
| **8. Offline Deterministic Fallback** | Runs without external API keys or paid services; verified deterministic extraction mode. | ☐ Approved<br/>☐ Needs Revision | |
| **9. Synthetic Knowledge Base** | Cleanly labeled synthetic HLDs (BMS, Brake-by-Wire, ADAS); non-proprietary data used. | ☐ Approved<br/>☐ Needs Revision | |
| **10. Evaluation Suite** | 12 reproducible test cases; genuine measured results; JSON/CSV/Markdown reports present. | ☐ Approved<br/>☐ Needs Revision | |
| **11. Demonstration Script & Video** | 5 to 10-minute structured presentation script and recording checklist. | ☐ Approved<br/>☐ Needs Revision | |
| **12. AI-Tool Usage Declaration** | Transparent declaration of coding assistants and prompt usage. | ☐ Approved<br/>☐ Needs Revision | |

---

## 2. Final Faculty Decision & Endorsement

### Assessment Decision
- [ ] **Accepted with Full Endorsement** (Meets or exceeds all capstone technical requirements).
- [ ] **Provisional Acceptance** (Minor documentation or formatting adjustments required by date: ___________).
- [ ] **Resubmission Required** (Major technical or scope deficiencies identified).

---

### Evaluator Comments & Feedback
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  

---

### Faculty Signatures

**Faculty Guide / Mentor:**  
Name: _____________________________________________  
Signature: ________________________________________  
Date: _____________________________________________  

**Head of Department / Program Chair:**  
Name: _____________________________________________  
Signature: ________________________________________  
Date: _____________________________________________  
