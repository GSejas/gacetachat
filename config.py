# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FAISS_INDEX_DIR = "faiss_indexes"
    GACETA_PDFS_DIR = "gaceta_pdfs"
    OPENAI_MODEL_NAME = "gpt-4o"  # or any other model you prefer
    OPENAI_MAX_TOKENS = 1500
    OPENAI_TEMPERATURE = 0.7

config = Config()
