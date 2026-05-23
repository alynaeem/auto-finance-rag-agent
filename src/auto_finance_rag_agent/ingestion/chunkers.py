import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


PDF_CHUNK_SIZE = 800
PDF_CHUNK_OVERLAP = 120

MARKDOWN_CHUNK_SIZE = 800
MARKDOWN_CHUNK_OVERLAP = 120

MARKDOWN_HEADERS = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
    ("####", "h4"),
]


def create_content_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def add_chunk_ids(chunks: list[Document]) -> list[Document]:
    for index, chunk in enumerate(chunks):
        source_type = chunk.metadata.get("source_type", "unknown_source")
        source_file = chunk.metadata.get("source_file", "unknown_file")
        page = chunk.metadata.get("page")

        page_label = "no_page" if page is None else f"page_{page}"
        text_hash = create_content_hash(chunk.page_content)

        chunk.metadata["chunk_index"] = index
        chunk.metadata["chunk_id"] = (
            f"{source_type}::{source_file}::{page_label}::{index}::{text_hash}"
        )

    return chunks


def has_body_text(document: Document) -> bool:
    lines = [
        line.strip()
        for line in document.page_content.splitlines()
        if line.strip()
    ]

    return any(not line.startswith("#") for line in lines)


def chunk_pdf_pages(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=PDF_CHUNK_SIZE,
        chunk_overlap=PDF_CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["chunk_strategy"] = "pdf_page_recursive_token"

    return add_chunk_ids(chunks)


def chunk_markdown_documents(markdown_documents: list[Document]) -> list[Document]:
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False,
    )

    token_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=MARKDOWN_CHUNK_SIZE,
        chunk_overlap=MARKDOWN_CHUNK_OVERLAP,
    )

    section_documents: list[Document] = []

    for document in markdown_documents:
        sections = markdown_splitter.split_text(document.page_content)

        for section in sections:
            if not has_body_text(section):
                continue

            section.metadata.update(document.metadata)

            heading_values = [
                section.metadata[metadata_key]
                for _, metadata_key in MARKDOWN_HEADERS
                if metadata_key in section.metadata
            ]

            section_path = " > ".join(heading_values)

            section.metadata["section_path"] = section_path
            section.metadata["heading"] = section_path
            section.metadata["chunk_strategy"] = "markdown_header_then_token"

            section_documents.append(section)

    chunks = token_splitter.split_documents(section_documents)

    return add_chunk_ids(chunks)
