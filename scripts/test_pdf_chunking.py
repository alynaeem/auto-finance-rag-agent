from auto_finance_rag_agent.ingestion.loader import load_pdf_documents
from auto_finance_rag_agent.ingestion.chunkers import chunk_pdf_pages


def main() -> None:
    pdf_pages = load_pdf_documents()
    chunks = chunk_pdf_pages(pdf_pages)

    print(f"PDF pages loaded: {len(pdf_pages)}")
    print(f"PDF chunks created: {len(chunks)}")
    print("-" * 80)

    first_chunk = chunks[0]

    print("First chunk metadata:")
    print(first_chunk.metadata)

    print("-" * 80)
    print("First chunk text preview:")
    print(first_chunk.page_content[:700].replace("\n", " "))


if __name__ == "__main__":
    main()
