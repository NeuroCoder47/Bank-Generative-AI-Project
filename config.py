import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-pro"
EMBEDDING_MODEL = "models/embedding-001"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

VECTOR_DB_PATH = "vector_db"
DATA_PATH = "data/policies"

RETRIEVAL_TOP_K = 3
