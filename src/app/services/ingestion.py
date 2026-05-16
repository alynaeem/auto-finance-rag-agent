from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader

PDF_dir = Path("data/raw/policy_docs")
MD_dir = Path("data/synthetic/company_policy_documents")

def load_raw_documents():
    """
    Load public pdf documents and synthetic markdown policy documents

    Returns:
    list: Langchain document objects with metadata

    """

    docs = []

    # Load pdf policy documents
    for pdf_path in PDF_dir.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()

        for doc in pdf_docs:
            doc.metadata["source_file"] = pdf_path.name
            doc.metadata["source_type"] = "public_pdf"

        docs.extend(pdf_docs)

    # Load synthetic markdown policy documents

    for md_path in MD_dir.glob("*.md"):
        loader = TextLoader(str(md_path))
        md_docs = loader.load()

        for doc in md_docs:
            doc.metadata["source_file"] = md_path.name
            doc.metadata["source_type"] = "synthetic_policy"
            doc.metadata["page"] = None

        docs.extend(md_docs)

    return docs
