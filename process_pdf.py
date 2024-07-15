# process_pdf.py
import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
# from langchain.loaders import PyPDFLoader
from models import GacetaPDF
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from db import Session

def ingest_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    return db

def query_vectorstore(db, query):
    docs = db.similarity_search(query)
    for doc in docs:
        print(doc.page_content)

def save_vectorstore(db, path="faiss_index"):
    db.save_local(path)

def load_vectorstore(path="faiss_index", embeddings=None):
    if embeddings is None:
        embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(path, embeddings)
    return db

def process_latest_pdf():
    session = Session()
    latest_gaceta = session.query(GacetaPDF).order_by(GacetaPDF.date.desc()).first()
    if latest_gaceta:
        loader = PyPDFLoader(latest_gaceta.file_path)
        documents = loader.load()
        embeddings = OpenAIEmbeddings()

        # Generate embeddings
        vectors = [embeddings.embed(doc.text) for doc in documents]

        # Create FAISS index
        dimension = len(vectors[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(vectors))

        return index, documents
    session.close()
    return None, None

def search_in_pdf(query, index, documents, embeddings):
    query_vector = embeddings.embed(query).reshape(1, -1)
    _, I = index.search(query_vector, k=1)
    return documents[I[0][0]].text
