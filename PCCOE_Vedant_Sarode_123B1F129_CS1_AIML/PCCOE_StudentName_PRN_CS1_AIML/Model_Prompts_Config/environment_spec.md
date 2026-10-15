# Environment Specification and Model Deployment Notes
**TechPulse FY-26 Applied AI/ML Capstone — Case Study 1 (CS1)**  

---

## 1. Runtime Environment
- **Host Operating System:** Microsoft Windows 11 / Windows Server (x86_64)
- **Primary Python Runtime:** Python 3.14.5 (64-bit)
- **Secondary Compatible Python Runtimes:** Python 3.12, Python 3.13
- **Virtual Environment Path:** `C:\TechPulseCapstone\.venv`
- **Package Manager:** `pip 26.1.1`

---

## 2. Core Library Stack & Hardware Utilization

| Component | Library & Version | Hardware Target | Memory Footprint | Network Dependency |
|---|---|---|---|---|
| **User Interface** | `streamlit 1.66.0` | CPU / Localhost (Port 8501) | ~120 MB | None (Local browser) |
| **PDF Ingestion** | `pypdf 6.20.1` | CPU (Pure Python) | ~30 MB | None |
| **PDF Generation (Synthetic)** | `reportlab 5.0.1` | CPU | ~40 MB | None |
| **Neural Embeddings** | `sentence-transformers 6.1.0` (`all-MiniLM-L6-v2`) | CPU / PyTorch 2.14.1 | ~250 MB | Initial model download (~80MB), then 100% offline |
| **Fallback Embeddings** | `scikit-learn 1.9.1` (TF-IDF + SVD) | CPU | ~40 MB | None (Zero download) |
| **Vector Index** | `faiss-cpu 1.15.1` | CPU (AVX2 / Multi-threaded) | < 15 MB for demo index | None (Local filesystem) |
| **Generative LLM SDK** | `google-genai 2.31.0` | Cloud (Google Gemini 2.5 Flash) | Minimal client footprint | HTTPS outbound to Google API |
| **Deterministic Fallback** | Custom Python Engine | CPU | < 5 MB | None (100% offline) |

---

## 3. Network Isolation and Zero-Cost Guarantee
- When operated without setting `GEMINI_API_KEY`, the application performs **zero network calls** during query processing.
- All embedding generation (`all-MiniLM-L6-v2`), FAISS vector calculations, document parsing, and answer extraction execute locally on CPU.
- The user cannot incur paid API charges unless they explicitly supply their own private API credentials in `.env` or the Streamlit sidebar.
