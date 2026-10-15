# System Architecture and Processing Workflow
**TechPulse FY-26 Applied AI/ML Capstone — Case Study 1 (CS1)**  
**Project:** AUTOSAR HLD Document Analysis Assistant  

---

## 1. High-Level Logical Architecture

```mermaid
flowchart TD
    User["Engineering User<br/>(Architect / Developer / Assessor)"]
    
    subgraph UI_Layer ["User Interface Layer"]
        StreamlitApp["Streamlit Web Application (app.py)<br/>• Document Ingestion Panel<br/>• Architectural Q&A Dashboard<br/>• Entity Catalog & JSON Export<br/>• Automated Evaluation Suite"]
    end
    
    subgraph Ingestion_Layer ["Ingestion & Preprocessing Layer"]
        Parser["PDFIngestionEngine (src/ingestion.py)<br/>• pypdf Page Extraction<br/>• Scanned Page & OCR Detector<br/>• Corrupt File Resilience"]
        Chunker["TextChunker (src/chunking.py)<br/>• Chunk Size: 500 chars<br/>• Overlap: 80 chars<br/>• Strict Page Boundary Isolation"]
    end
    
    subgraph Storage_Layer ["Local Indexing & Vector Storage Layer"]
        EmbeddingEngine["EmbeddingEngine (src/embeddings.py)<br/>• all-MiniLM-L6-v2 (384-d normalized)<br/>• Fallback: TF-IDF + SVD (128-d)"]
        FAISSStore["FAISSVectorStore (src/vector_store.py)<br/>• IndexFlatIP (Cosine Similarity)<br/>• Disk Persistence: faiss_index.bin<br/>• Metadata Store: chunks_metadata.pkl"]
    end
    
    subgraph QA_Layer ["Grounded QA & Guardrails Layer"]
        Retriever["DocumentRetriever (src/retriever.py)<br/>• Top-K Semantic Passages<br/>• Cosine Similarity Scoring"]
        Guardrails["Responsible AI Guardrails (src/qa_engine.py)<br/>• Adversarial Injection Neutralizer<br/>• Relevance Threshold Filter (< 0.32)<br/>• Keyword Coverage Filter (< 35%)"]
        QAEngine["GroundedQAEngine (src/qa_engine.py)<br/>• Mode A: Google Gemini 2.5 Flash<br/>• Mode B: Deterministic Fallback"]
    end

    User -->|Queries & PDFs| StreamlitApp
    StreamlitApp --> Parser
    Parser --> Chunker
    Chunker --> EmbeddingEngine
    EmbeddingEngine --> FAISSStore
    
    StreamlitApp --> Retriever
    Retriever --> FAISSStore
    FAISSStore --> Retriever
    Retriever --> Guardrails
    Guardrails --> QAEngine
    QAEngine -->|Grounded Answers + Citations| StreamlitApp
```

---

## 2. Ingestion & Retrieval Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Engineer as Automotive Engineer
    participant UI as Streamlit UI (app.py)
    participant Ingest as PDF Ingestion (ingestion.py)
    participant Chunk as Text Chunker (chunking.py)
    participant Embed as Embeddings (embeddings.py)
    participant FAISS as FAISS Store (vector_store.py)
    participant QA as QA Engine (qa_engine.py)

    Note over Engineer,FAISS: Step 1: Knowledge Ingestion
    Engineer->>UI: Uploads AUTOSAR HLD PDFs
    UI->>Ingest: ingest_file(pdf_stream)
    Ingest-->>UI: PageData list (Page num, text, OCR warnings)
    UI->>Chunk: chunk_pages(pages, size=500, overlap=80)
    Chunk-->>UI: TextChunk list with page metadata
    UI->>Embed: embed_documents(chunk_texts)
    Embed-->>UI: 384-dimensional normalized vectors
    UI->>FAISS: add_chunks(chunks, vectors)
    FAISS->>FAISS: Persist to local disk

    Note over Engineer,QA: Step 2: Query & Grounded Answer
    Engineer->>UI: Enters query ("What is over-voltage threshold?")
    UI->>QA: answer_question(query, top_k=4)
    QA->>QA: Check prompt injection patterns
    QA->>Embed: embed_query(query)
    Embed-->>QA: Query vector
    QA->>FAISS: search(query_vector, top_k=4)
    FAISS-->>QA: Top-K passages with similarity scores
    QA->>QA: Verify similarity threshold (score >= 0.32)
    alt Gemini Mode Available
        QA->>QA: Format <retrieved_context> & invoke Gemini 2.5 Flash
    else Offline Fallback Mode
        QA->>QA: Deterministic extraction of salient sentences
    end
    QA-->>UI: QAResponse (Answer, verified citations, latency)
    UI-->>Engineer: Renders answer card, citation badges & raw passages
```

---

## 3. Data Flow and Entity Relations

```mermaid
erDiagram
    DOCUMENT {
        string doc_name PK
        int total_pages
        int scanned_pages_count
        boolean success
    }
    PAGE {
        string doc_name FK
        int page_num PK
        string text
        int char_count
        boolean is_empty_or_scanned
    }
    TEXT_CHUNK {
        string chunk_id PK
        string doc_name FK
        int page_num
        int chunk_index
        string text
        int char_start
        int char_end
    }
    EMBEDDING_VECTOR {
        string chunk_id FK
        float vector_384d
        string model_name
    }
    QA_CITATION {
        string query
        string doc_name FK
        int page_num
        float similarity_score
    }

    DOCUMENT ||--o{ PAGE : contains
    PAGE ||--o{ TEXT_CHUNK : partitioned_into
    TEXT_CHUNK ||--|| EMBEDDING_VECTOR : encoded_as
    TEXT_CHUNK ||--o{ QA_CITATION : referenced_by
```
