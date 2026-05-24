from langchain_core.documents import Document

from auto_finance_rag_agent.ingestion.chunkers import (
    chunk_markdown_documents,
    chunk_pdf_pages,
)
from auto_finance_rag_agent.ingestion.loader import (
    load_markdown_policy_files,
    load_pdf_documents,
)


def build_document_chunks() -> list[Document]:
    pdf_pages = load_pdf_documents()
    markdown_documents = load_markdown_policy_files()

    pdf_chunks = chunk_pdf_pages(pdf_pages)
    markdown_chunks = chunk_markdown_documents(markdown_documents)

    return pdf_chunks + markdown_chunks
