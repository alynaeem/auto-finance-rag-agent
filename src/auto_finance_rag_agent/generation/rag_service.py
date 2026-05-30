from auto_finance_rag_agent.generation.answer_generator import generate_grounded_answer
from auto_finance_rag_agent.retrieval.retriever import retrieve_policy_context
from auto_finance_rag_agent.schemas import RAGResponse, SourceInfo


def ask_policy_question(query: str, k: int = 3) -> RAGResponse:
    contexts = retrieve_policy_context(query, k=k)

    answer = generate_grounded_answer(query, contexts)

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