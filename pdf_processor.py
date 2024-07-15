# pdf_processor.py
import os
from langchain_community.document_loaders import PyPDFLoader
from models import GacetaPDF
from db import Session
from faiss_helper import FAISSHelper

class PDFProcessor:
    def __init__(self, faiss_helper:FAISSHelper):
        self.faiss_helper = faiss_helper

    def process_latest_pdf(self):
        session = Session()
        latest_gaceta = session.query(GacetaPDF).order_by(GacetaPDF.date.desc()).first()
        if latest_gaceta:
            loader = PyPDFLoader(latest_gaceta.file_path)
            documents = loader.load()
            db = self.faiss_helper.create_faiss_index(documents)
            directory = os.path.dirname(latest_gaceta.file_path)
            self.faiss_helper.save_faiss_index(db, directory)
            session.close()
            return db, documents
        session.close()
        return None, None

    def search_in_pdf(self, query, index, documents):
        # query_vector = self.faiss_helper.embeddings.embed(query).reshape(1, -1)
        relevant_docs = index.similarity_search(query, k=5)#
        # return documents[I[0][0]].text
        return relevant_docs
