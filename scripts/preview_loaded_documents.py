from auto_finance_rag_agent.ingestion.loader import load_all_raw_documents


def main() -> None:
    documents = load_all_raw_documents()

    print(f"Loaded documents: {len(documents)}")

    if not documents:
        print("No documents were loaded.")
        return

    print("-" * 80)

    for index, document in enumerate(documents[:10], start=1):
        print(f"Document #{index}")
        print(f"Source file: {document.metadata.get('source_file')}")
        print(f"Source type: {document.metadata.get('source_type')}")
        print(f"Page: {document.metadata.get('page')}")
        print("Text preview:")
        print(document.page_content[:500].replace("\n", " "))
        print("-" * 80)


if __name__ == "__main__":
    main()
