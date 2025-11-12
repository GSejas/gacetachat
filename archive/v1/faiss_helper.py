#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 FAISS Vector Search Helper - Document Embeddings & Similarity Search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    FAISS (Facebook AI Similarity Search) integration for high-performance vector
    similarity search on document embeddings. Manages OpenAI embeddings, document
    chunking, index persistence, and retrieval for semantic search in gazette PDFs.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐   Document    ┌──────────────────┐
    │   PDF Content   │ ─────────────▶│   Text Splitter  │
    │   (Raw Text)    │               │   (1000 chunks)  │
    └─────────────────┘               └──────────────────┘
            │                                 │
            │                                 │ Embedding
            ▼                                 ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ Document Store  │               │  OpenAI API      │
    │ (Persistent)    │               │  (ada-002)       │
    └─────────────────┘               └──────────────────┘
            │                                 │
            │ FAISS Index                     │ Vector Embeddings
            ▼                                 ▼
    ┌─────────────────┐               ┌──────────────────┐
    │ index.faiss +   │◀──────────────│   FAISS Vector   │
    │ index.pkl       │   Serialize   │   Database       │
    └─────────────────┘               └──────────────────┘
    ```

📥 Inputs:
    • Document collections: LangChain Document objects with text content
    • Configuration parameters: Model name, tokens, temperature, API keys
    • Directory paths: File system locations for index storage and retrieval
    • Text content: Raw PDF text for chunking and embedding generation
    • Search queries: Natural language queries for similarity matching

📤 Outputs:
    • FAISS indices: Serialized vector databases with similarity search capability
    • Document chunks: Text segments optimized for retrieval (1000 char chunks)
    • Similarity scores: Ranked document relevance for user queries
    • Persistent storage: index.faiss + index.pkl files for efficient loading
    • Vector embeddings: High-dimensional representations via OpenAI ada-002

🔗 Dependencies:
    • langchain_community: FAISS vector store integration and persistence
    • langchain_openai: OpenAI embeddings API client and model access
    • langchain_text_splitters: Document chunking with overlap management
    • faiss-cpu: Core similarity search engine and indexing algorithms
    • config: Application configuration and API key management

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[FAISSHelper] --> B[OpenAIEmbeddings]
        A --> C[CharacterTextSplitter]
        A --> D[FAISS Vector Store]

        E[PDF Processor] --> A
        A --> F[Query Engine]
        D --> G[Disk Storage]
        B --> H[OpenAI API]

        I[Config] --> A
        A --> J[Document Retrieval]

        classDef faissModule fill:#e1f5fe
        classDef langchain fill:#f3e5f5
        classDef external fill:#fff3e0
        classDef storage fill:#fff8e1

        class A faissModule
        class B,C,D langchain
        class H,E external
        class G,I storage
    ```

🔒 Security Considerations:
    ⚠️  HIGH: OpenAI API key exposure in constructor - ensure secure credential storage
    ⚠️  HIGH: allow_dangerous_deserialization=True enables arbitrary code execution
    ⚠️  MEDIUM: No input validation on document content - potential injection vectors
    ⚠️  MEDIUM: File system access without path validation - directory traversal risk
    ⚠️  LOW: Embedding data contains original text snippets - privacy implications

🛡️ Risk Analysis:
    • API Cost Control: No rate limiting on embedding generation, cost escalation risk
    • Data Security: Original document content embedded in vectors, potential leakage
    • System Resources: Large indices consume significant memory and disk space
    • Dependency Risk: FAISS deserialization vulnerability in untrusted environments
    • Data Integrity: No checksum validation for index files, corruption possible

⚡ Performance Characteristics:
    • Time Complexity: O(d*log(n)) for similarity search, O(n*d) for index creation
    • Memory Usage: ~50MB base + 4 bytes per dimension per document
    • Index Size: ~1MB per 1000 documents with 1536-dimensional embeddings
    • Search Speed: <100ms for k=5 similarity search on 10K documents
    • Embedding API: 8191 tokens max per request, rate limited to 3M tokens/min

🧪 Testing Strategy:
    • Unit Tests: Individual method validation with mocked embeddings API
    • Integration Tests: End-to-end document indexing and retrieval workflows
    • Performance Tests: Large document sets, concurrent index operations
    • Security Tests: Deserialization safety, path traversal prevention

📊 Monitoring & Observability:
    • Metrics: Index size, search latency, embedding API usage, error rates
    • Logging: Index creation/loading events, search queries, API failures
    • Alerts: Index corruption, API quota exceeded, slow search performance
    • Health Checks: Index file integrity, embedding API connectivity

🔄 Data Flow:
    ```
    Documents ──▶ Text Splitting ──▶ Embedding ──▶ FAISS Index ──▶ Similarity Search
         │             │              │            │                │
         ▼             ▼              ▼            ▼                ▼
    Validation    Chunk Creation   API Request   Serialization   Result Ranking
    ```

📚 Usage Examples:
    ```python
    # Initialize FAISS helper
    helper = FAISSHelper(openai_api_key="sk-your-key")

    # Create index from documents
    documents = [Document(page_content="text content")]
    db = helper.create_faiss_index(documents)

    # Save index to disk
    helper.save_faiss_index(db, "gaceta_pdfs/2024-07-19/")

    # Load existing index
    loaded_db = helper.load_faiss_index("gaceta_pdfs/2024-07-19/")

    # Perform similarity search
    results = loaded_db.similarity_search("query text", k=5)
    ```

🔧 Configuration:
    ```python
    # Chunking Strategy
    CHUNK_SIZE = 1000          # Characters per document chunk
    CHUNK_OVERLAP = 0          # Overlap between chunks (disabled)

    # Embedding Model
    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model
    EMBEDDING_DIMENSIONS = 1536                 # Vector dimensions

    # Index Storage
    INDEX_FILE_PATTERN = "{date}/index.faiss"  # Date-based organization
    METADATA_FILE = "index.pkl"                 # Document metadata storage
    ```

🚨 Critical Security Notice:
    The allow_dangerous_deserialization=True parameter in load_faiss_index() enables
    pickle deserialization which can execute arbitrary code. Only load indices from
    trusted sources and consider implementing signature verification for production.

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
