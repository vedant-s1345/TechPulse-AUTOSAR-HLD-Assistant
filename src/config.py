"""
Configuration module for AUTOSAR HLD Document Analysis Assistant.
Manages environment variables, model defaults, and vector storage paths.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if available
load_dotenv(override=True)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Resolve synthetic data directory across root or Code/ deployment
if (WORKSPACE_ROOT / "data" / "synthetic_hld").exists():
    SYNTHETIC_DATA_DIR = WORKSPACE_ROOT / "data" / "synthetic_hld"
elif (WORKSPACE_ROOT.parent / "Input_Data").exists():
    SYNTHETIC_DATA_DIR = WORKSPACE_ROOT.parent / "Input_Data"
elif (WORKSPACE_ROOT / "Input_Data").exists():
    SYNTHETIC_DATA_DIR = WORKSPACE_ROOT / "Input_Data"
else:
    SYNTHETIC_DATA_DIR = WORKSPACE_ROOT / "data" / "synthetic_hld"

DATA_DIR = SYNTHETIC_DATA_DIR.parent if SYNTHETIC_DATA_DIR.exists() else WORKSPACE_ROOT / "data"
REFERENCE_DOCS_DIR = (
    WORKSPACE_ROOT / "reference_docs"
    if (WORKSPACE_ROOT / "reference_docs").exists()
    else WORKSPACE_ROOT.parent / "Documentation" / "Reference_Documents"
)
VECTOR_STORE_DIR = WORKSPACE_ROOT / "vector_store_data"

VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

# Embeddings & Vector Store Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "500"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "80"))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "4"))

# Grounding Safeguards
MAX_CONTEXT_CHUNKS = 6
STRICT_GROUNDING = True
