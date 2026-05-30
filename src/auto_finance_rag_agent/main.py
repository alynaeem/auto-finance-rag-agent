from fastapi import FastAPI

from auto_finance_rag_agent.generation.rag_service import ask_policy_question
from auto_finance_rag_agent.schemas import RAGRequest, RAGResponse


app = FastAPI(
    title="Auto Finance RAG Agent",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=RAGResponse)
def ask(request: RAGRequest) -> RAGResponse:
    return ask_policy_question(
        query=request.question,
        k=request.top_k,
    )
