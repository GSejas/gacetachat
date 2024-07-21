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
            
            import os

            file_path = latest_gaceta.file_path
            absolute_path = os.path.abspath(file_path)

            if os.path.exists(absolute_path):
                print(f"File exists at: {absolute_path}")
            else:
                print(f"File does not exist at: {absolute_path}")
            
            loader = PyPDFLoader(absolute_path)
            documents = loader.load()
            db = self.faiss_helper.create_faiss_index(documents)
            directory = os.path.dirname(latest_gaceta.file_path)
            self.faiss_helper.save_faiss_index(db, directory)
            session.close()
            return db, documents
        session.close()
        return None, None

