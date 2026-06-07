import time

from auto_finance_rag_agent.generation.answer_generator import generate_grounded_answer
from auto_finance_rag_agent.retrieval.retriever import retrieve_policy_context
from auto_finance_rag_agent.schemas import RAGResponse, SourceInfo


def ask_policy_question(query: str, k: int = 3) -> RAGResponse:
    start = time.perf_counter()
    contexts = retrieve_policy_context(query, k=k)
    retrieval_time = time.perf_counter() - start

    start = time.perf_counter()
    answer = generate_grounded_answer(query, contexts)
    generation_time = time.perf_counter() - start

    print(f"Retrieval time: {retrieval_time:.2f}s")
    print(f"Generation time: {generation_time:.2f}s")

    sources = []

    for context in contexts:
        sources.append(
            SourceInfo(
                source_file=context.get("source_file"),
                source_type=context.get("source_type"),
                page=context.get("page"),
                section_path=context.get("section_path"),
                score=context.get("score"),
                chunk_id=context.get("chunk_id"),
            )
        )

    return RAGResponse(
        query=query,
        answer=answer,
        sources=sources,
        safety_note="Portfolio demo only. Not legal, financial, or credit approval advice.",
    )