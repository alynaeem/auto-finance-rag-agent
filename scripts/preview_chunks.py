from collections import Counter

from auto_finance_rag_agent.services.ingestion import load_document_chunks


def main() -> None:
    chunks = load_document_chunks()

    print(f"Total chunks: {len(chunks)}")
    if not chunks:
        print(
            "No chunks were created from data/raw/policy_docs "
            "or data/synthetic/company_policy_documents."
        )
        return

    counts_by_type = Counter(chunk.metadata.get("source_type") for chunk in chunks)
    print(f"Chunks by source type: {dict(counts_by_type)}")
    print("-" * 80)

    for i, chunk in enumerate(chunks[:10], start=1):
        metadata = chunk.metadata
        print(f"Chunk #{i}")
        print(f"Chunk ID: {metadata.get('chunk_id')}")
        print(f"Source file: {metadata.get('source_file')}")
        print(f"Source type: {metadata.get('source_type')}")
        print(f"Page: {metadata.get('page')}")
        print(f"Section: {metadata.get('section_path')}")
        print("Text preview:")
        print(chunk.page_content[:500].replace("\n", " "))
        print("-" * 80)


if __name__ == "__main__":
    main()
