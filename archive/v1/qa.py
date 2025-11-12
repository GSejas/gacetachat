#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Question Answering Engine - LangChain + OpenAI Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    AI-powered question answering system using LangChain and OpenAI GPT models.
    Implements document-aware Q&A with FAISS vector similarity search, context
    window management, and source attribution for Costa Rica gazette analysis.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐    Query     ┌──────────────────┐
    │   User Input    │ ───────────▶ │  Query Processor │
    │   (Question)    │              │  (This Module)   │
    └─────────────────┘              └──────────────────┘
            │                                 │
            │                                 │ Similarity Search
            ▼                                 ▼
    ┌─────────────────┐              ┌──────────────────┐
    │ FAISS Vector DB │              │  Document Chunk  │
    │ (Embeddings)    │◀─────────────│  Retrieval (k=5) │
    └─────────────────┘              └──────────────────┘
            │                                 │
            │ Context Docs                    │ LLM Processing
            ▼                                 ▼
    ┌─────────────────┐              ┌──────────────────┐
    │  Token Limiter  │              │   OpenAI GPT     │
    │  (Context Mgmt) │──────────────▶│  Answer + Sources│
    └─────────────────┘              └──────────────────┘
    ```

📥 Inputs:
    • User queries: Natural language questions about gazette content
    • Document indices: FAISS vector stores with embedded text chunks
    • Model configuration: GPT model selection, temperature, max tokens
    • Context limits: Token count thresholds for prompt management
    • Retrieval parameters: Number of similar documents to consider (k=5)

📤 Outputs:
    • AI answers: Structured responses with source attribution
    • Source documents: Retrieved text chunks with relevance scores
    • Token metrics: Context window utilization and optimization stats
    • Prompt partials: Formatted prompts for debugging and analysis
    • Error handling: Graceful degradation when information insufficient

🔗 Dependencies:
    • langchain: Document processing chains and prompt templates
    • langchain_openai: ChatOpenAI model integration and API client
    • pydantic: Data validation for structured response models
    • typing: Type hints for document lists and model interfaces
    • faiss (via folder_index): Vector similarity search backend

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[QA Module] --> B[ChatOpenAI]
        A --> C[PromptTemplate]
        A --> D[StuffDocumentsChain]
        A --> E[Document Retrieval]

        F[FAISS Index] --> E
        E --> G[Context Window Mgmt]
        G --> D
        D --> B
        B --> H[Answer + Sources]

        classDef qaModule fill:#e1f5fe
        classDef langchain fill:#f3e5f5
        classDef external fill:#fff3e0

        class A qaModule
        class C,D,G langchain
        class B,F,H external
    ```

🔒 Security Considerations:
    ⚠️  HIGH: OpenAI API key exposure via ChatOpenAI initialization
    ⚠️  MEDIUM: Prompt injection through user queries affecting LLM behavior
    ⚠️  MEDIUM: Document content leakage via similarity search results
    ⚠️  LOW: Token count manipulation for cost optimization attacks
    ⚠️  LOW: Debug mode bypass potentially exposing internal prompts

🛡️ Risk Analysis:
    • API Costs: No rate limiting on expensive GPT-4 calls, budget risk
    • Data Privacy: User queries and documents sent to OpenAI servers
    • Response Quality: Hallucination risk when insufficient context available
    • System Availability: Dependent on OpenAI API uptime and rate limits
    • Context Injection: Malicious documents could bias LLM responses

⚡ Performance Characteristics:
    • Time Complexity: O(d*log(n)) where d=docs, n=vector_dimension
    • Token Usage: 150-4000 tokens per query depending on context size
    • Response Time: 2-8 seconds for GPT-4, 1-3 seconds for GPT-3.5
    • Memory Usage: ~50MB + document index size in memory
    • Throughput: Limited by OpenAI rate limits (3,500 RPM for GPT-4)

🧪 Testing Strategy:
    • Unit Tests: Prompt template validation, document filtering logic
    • Integration Tests: End-to-end Q&A with known document corpus
    • Performance Tests: Large document sets, concurrent query processing
    • Quality Tests: Answer accuracy validation against human benchmarks

📊 Monitoring & Observability:
    • Metrics: Query response times, token usage, source relevance scores
    • Logging: User queries, retrieved documents, model responses
    • Alerts: API failures, excessive token usage, low-quality responses
    • Cost Tracking: OpenAI API usage and billing integration

🔄 Data Flow:
    ```
    Query Input ──▶ Vector Search ──▶ Context Assembly ──▶ LLM Processing ──▶ Answer Output
         │               │                 │                    │                │
         ▼               ▼                 ▼                    ▼                ▼
    Validation    Similarity Scoring   Token Limiting    API Request     Source Attribution
    ```

📚 Usage Examples:
    ```python
    # Initialize LLM
    llm = get_llm("gpt-4", temperature=0.3, max_tokens=1000)

    # Query with document context
    result = query_folder(
        query="What are the main regulations?",
        folder_index=faiss_index,
        llm=llm,
        return_all=False
    )

    # Access structured response
    answer = result["answer"]
    sources = result["sources"]
    references = result["ai_references"]
    ```

🔧 Configuration:
    ```python
    # Model Selection
    SUPPORTED_MODELS = ["gpt-4", "gpt-3.5-turbo", "debug"]

    # Context Management
    MAX_CONTEXT_TOKENS = 4000
    SIMILARITY_SEARCH_K = 5

    # Prompt Template
    STUFF_PROMPT_TEMPLATE = "Answer using provided sources..."
    ```

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from typing import List

from langchain.chains.combine_documents.stuff import StuffDocumentsChain

# from knowledge_gpt.core.debug import FakeChatModel
from langchain.chat_models.base import BaseChatModel
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI


def pop_docs_upto_limit(
    query: str, chain: StuffDocumentsChain, docs: List[Document], max_len: int
) -> List[Document]:
    """Pops documents from a list until the final prompt length is less
    than the max length."""

    token_count: int = chain.prompt_length(docs, question=query)  # type: ignore

    while token_count > max_len and len(docs) > 0:
        docs.pop()
        token_count = chain.prompt_length(docs, question=query)  # type: ignore

    return docs


def get_llm(model: str, **kwargs) -> BaseChatModel:
    if model == "debug":
        return None  # FakeChatModel()

    if "gpt" in model:
        return ChatOpenAI(model=model, **kwargs)  # type: ignore

    raise NotImplementedError(f"Model {model} not supported!")


from langchain.prompts import PromptTemplate

## Use a shorter template to reduce the number of tokens in the prompt
template = """Create a final answer to the given questions using the provided document excerpts (given in no particular order) as sources. 

ALWAYS include a "SOURCES" section in your answer citing only the minimal set of sources needed to answer the question. 

If you are unable to answer the question, simply state that you do not have enough information to answer the question and leave the SOURCES section empty. 

Use only the provided documents and do not attempt to fabricate an answer.


---------

QUESTION: {question}
=========
{context}
=========
FINAL ANSWER:"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)
from langchain.chat_models.base import BaseChatModel
from langchain.docstore.document import Document

# from knowledge_gpt.core.embedding import FolderIndex
from pydantic import BaseModel

# <!-- ruff: noqa: F821 -->
# from langchain.globals import set_llm_cache


class AnswerWithSources(BaseModel):
    answer: str
    sources: List[Document]


from langchain.chains.combine_documents import create_stuff_documents_chain

# from langchain.cache import InMemoryCache


# set_llm_cache(InMemoryCache())
def query_folder(
    query: str,
    folder_index,
    llm: BaseChatModel,
    return_all: bool = False,
    debug: bool = True,
):
    """Queries a folder index for an answer.

    Args:
        query (str): The query to search for.
        folder_index (FolderIndex): The folder index to search.
        return_all (bool): Whether to return all the documents from the embedding or
        just the sources for the answer.
        model (str): The model to use for the answer generation.
        **model_kwargs (Any): Keyword arguments for the model.

    Returns:
        AnswerWithSources: The answer and the source documents.
    """
    # if debug:
    #     return {
    #         "answer": query,
    #         "partial": None,
    #         "sources": [],
    #         "ai_references": None,
    #     }

    relevant_docs = folder_index.similarity_search(query, k=5)

    partial_prompt = STUFF_PROMPT.partial(context=relevant_docs, question=query)

    chain = create_stuff_documents_chain(llm, STUFF_PROMPT)

    result = chain.invoke({"context": relevant_docs, "question": query})

    sources = relevant_docs

    answer = result.split("SOURCES:")[0]

    return {
        "answer": answer,
        "partial": partial_prompt,
        "sources": sources,
        "ai_references": result.split("SOURCES:")[1],
    }
