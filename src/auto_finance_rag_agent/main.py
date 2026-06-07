from contextlib import asynccontextmanager

from fastapi import FastAPI

from auto_finance_rag_agent.api.routes import router
from auto_finance_rag_agent.retrieval.vector_store import warm_up_vectorstore


@asynccontextmanager
async def lifespan(app: FastAPI):
    warm_up_vectorstore()
    yield


app = FastAPI(
    title="Auto Finance RAG Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)