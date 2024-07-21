from typing import List
from typing import List
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.docstore.document import Document

from langchain_openai import ChatOpenAI
# from knowledge_gpt.core.debug import FakeChatModel
from langchain.chat_models.base import BaseChatModel


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
        return None# FakeChatModel()

    if "gpt" in model:
        return ChatOpenAI(model=model, **kwargs)  # type: ignore

    raise NotImplementedError(f"Model {model} not supported!")
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
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
from langchain.docstore.document import Document
# from knowledge_gpt.core.embedding import FolderIndex
from pydantic import BaseModel
from langchain.chat_models.base import BaseChatModel
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
    relevant_docs = folder_index.similarity_search(query, k=5)

    partial_prompt = STUFF_PROMPT.partial(context=relevant_docs, question=query)
    
    chain = create_stuff_documents_chain(llm, STUFF_PROMPT)
    
    result = chain.invoke({"context": relevant_docs,  "question":query})

    sources = relevant_docs

    answer = result.split("SOURCES:")[0]

    return {
            "answer":answer,
            "partial":partial_prompt,
            "sources":sources,
            "ai_references":result.split("SOURCES:")[1],
            }
