# faiss_helper.py
import os

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from config import config


class FAISSHelper:
    def __init__(
        self, model_name=None, max_tokens=None, temperature=None, openai_api_key=None
    ):
        self.model_name = model_name or config.OPENAI_MODEL_NAME
        self.max_tokens = max_tokens or config.OPENAI_MAX_TOKENS
        self.temperature = temperature or config.OPENAI_TEMPERATURE
        self.openai_api_key = openai_api_key or config.OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(
            # model=self.model_name,
            # max_tokens=self.max_tokens,
            # temperature=self.temperature,
            openai_api_key=self.openai_api_key
        )

    def save_faiss_index(self, db: FAISS, directory):
        os.makedirs(directory, exist_ok=True)
        db.save_local(directory)

    def load_faiss_index(self, directory):
        return FAISS.load_local(
            directory, self.embeddings, allow_dangerous_deserialization=True
        )

    def create_faiss_index(self, documents):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        db = FAISS.from_documents(docs, self.embeddings)
        return db
