import os
import shutil
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

if TYPE_CHECKING:
    from langchain_chroma import Chroma


load_dotenv()

CHROMA_DIR = Path(os.getenv("CHROMA_DIR", "vectorstore/chroma"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "auto_finance_policy_chunks")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
LOCAL_EMBEDDING_MODEL = os.getenv(
    "LOCAL_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)


@lru_cache(maxsize=1)
def get_embedding_model() -> Embeddings:
    if EMBEDDING_PROVIDER == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    if EMBEDDING_PROVIDER == "local":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=LOCAL_EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")


def reset_vectorstore() -> None:
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def build_vectorstore(chunks: list[Document], reset: bool = True) -> "Chroma":
    from langchain_chroma import Chroma

    if not chunks:
        raise ValueError("Cannot build vectorstore because no chunks were provided.")

    if reset:
        reset_vectorstore()
        load_vectorstore.cache_clear()

    embeddings = get_embedding_model()

    chunk_ids = [chunk.metadata["chunk_id"] for chunk in chunks]

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=chunk_ids,
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
    )


@lru_cache(maxsize=1)
def load_vectorstore() -> "Chroma":
    from langchain_chroma import Chroma

    embeddings = get_embedding_model()

    return Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )


def warm_up_vectorstore() -> None:
    vectorstore = load_vectorstore()
    vectorstore.similarity_search("warm up retrieval", k=1)
