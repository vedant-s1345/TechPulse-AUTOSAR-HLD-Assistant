# Video Recording & Presentation Checklist
**Project:** AUTOSAR HLD Document Analysis Assistant (CS1)  
**Academic Program:** TechPulse FY-26 Applied AI/ML Capstone  

---

## 1. Pre-Recording Preparation
- [ ] Ensure Python virtual environment is active: `.\.venv\Scripts\Activate.ps1`
- [ ] Ensure dependencies are installed: `pip install -r Code/requirements.txt`
- [ ] Run unit tests to confirm green status: `python -m unittest discover -s Code/tests -p "test_*.py"`
- [ ] Run evaluation runner to verify 100% pass rate: `python Code/tests/run_evaluation.py`
- [ ] Start Streamlit application in a separate terminal: `streamlit run Code/app.py`
- [ ] Open browser at `http://localhost:8501` and verify full screen view (F11 or maximize).
- [ ] Check microphone audio levels and set screen resolution to 1080p (1920x1080).

---

## 2. Recommended Screen Capture Flow
1. **Slide 1 (0:00 - 1:30):** Title slide with Student Name, PRN, PCCOE affiliation, and Case Study 1 objective.
2. **Slide 2 (1:30 - 3:00):** Architecture and Sequence Diagram showing local FAISS vector store, page-preserving chunking, and dual-mode inference.
3. **Live App (3:00 - 4:30):** Click "Load Synthetic AUTOSAR HLD Base" -> Run "⚡ BMS Over-Voltage Flow" -> Highlight citations and expandable passage scores.
4. **Live App (4:30 - 6:00):** Show Tab 3 (Extracted Architecture Catalog) -> Demonstrate discovered SWCs, Interfaces, and JSON download.
5. **Live App (6:00 - 7:30):** Demonstrate Responsible AI guardrails -> Run "❓ Out-of-Scope (Negative)" (Tesla tire pressure) -> Demonstrate refusal without hallucination -> Demonstrate prompt injection neutralization.
6. **Live App (7:30 - 9:00):** Show Tab 4 (Evaluator Test Suite) -> Click "Run Full Automated Evaluation Suite" -> Show 12/12 PASS results table with sub-10ms latencies.
7. **Slide 3 (9:00 - 10:00):** Summary of achievements, limitations, and future work.

---

## 3. Video Submission Requirements
- Format: MP4 / MKV (H.264 video, AAC audio).
- Target Duration: 5 to 10 minutes (strictly enforced by academic evaluation guidelines).
- Save completed video file as: `Video/PCCOE_StudentName_PRN_CS1_Demo.mp4`
