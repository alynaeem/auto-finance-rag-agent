from typing import Any

from auto_finance_rag_agent.retrieval.vector_store import load_vectorstore


def retrieve_policy_context(query: str, k: int = 5) -> list[dict[str, Any]]:
    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search_with_score(
        query=query,
        k=k,
    )

    contexts = []

    for document, score in results:
        contexts.append(
            {
                "content": document.page_content,
                "score": score,
                "source_file": document.metadata.get("source_file"),
                "source_type": document.metadata.get("source_type"),
                "page": document.metadata.get("page"),
                "section_path": document.metadata.get("section_path"),
                "chunk_id": document.metadata.get("chunk_id"),
                "chunk_strategy": document.metadata.get("chunk_strategy"),
            }
        )

    return contexts