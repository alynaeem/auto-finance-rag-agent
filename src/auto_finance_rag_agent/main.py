from contextlib import asynccontextmanager
import os

import gradio as gr
from fastapi import FastAPI

from auto_finance_rag_agent.api.routes import router
from auto_finance_rag_agent.retrieval.vector_store import warm_up_vectorstore
from auto_finance_rag_agent.ui.gradio_app import create_gradio_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("WARM_UP_VECTORSTORE", "false").lower() == "true":
        warm_up_vectorstore()

    yield


app = FastAPI(
    title="Auto Finance RAG Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)

gradio_app = create_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/demo")
