from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

PDF_dir = Path("data/raw/policy_docs")
MD_dir = Path("data/synthetic/company_policy_documents")


def load_pdf_documents(pdf_dir: Path = PDF_dir) -> list[Document]:

    """
    Load public policy PDFs page by page.

    Each PDF page becomes one LangChain Document.

    Why page by page?
    - PDFs naturally have page numbers.
    - Page metadata is useful for citations.
    - Later, answers can cite the source file and page.
    """
    documents: list[Document] = []

    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()

        for doc in pdf_docs:
            doc.metadata["source_file"] = pdf_path.name
            doc.metadata["source_type"] = "public_pdf"

        documents.extend(pdf_docs)

    return documents

def load_markdown_policy_files(markdown_dir: Path = MD_dir) -> list[Document]:

    """
    Load synthetic markdown company policy files.

    Each markdown file becomes one LangChain Document for now.

    We are not splitting by headings yet. That will happen in chunkers.py.
    """

    documents: list[Document] = []

    for markdown_path in sorted(markdown_dir.glob("*.md")):
        loader = TextLoader(str(markdown_path), encoding="utf-8")
        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source_file"] = markdown_path.name
            doc.metadata["source_type"] = "synthetic_policy"
            doc.metadata["page"] = None

        documents.extend(loaded_docs)

    return documents

def load_all_raw_documents() -> list[Document]:

    """
    Load all raw documents before chunking.

    This function combines:
    - public PDF pages
    - synthetic markdown policy files
    """

    pdf_documents = load_pdf_documents()
    markdown_documents = load_markdown_policy_files()

    return pdf_documents + markdown_documents
