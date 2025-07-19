# config.py
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "test-api-key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///gaceta1.db")
    FAISS_INDEX_DIR = "faiss_indexes"
    GACETA_PDFS_DIR = "gaceta_pdfs"
    OPENAI_MODEL_NAME = "gpt-4o"  # or any other model you prefer
    OPENAI_MAX_TOKENS = 2000
    OPENAI_TEMPERATURE = 0.3


config = Config()
