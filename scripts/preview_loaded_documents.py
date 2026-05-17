from auto_finance_rag_agent.services.ingestion import load_raw_documents


def main():
    docs = load_raw_documents()

    print(f"Total loaded document objects: {len(docs)}")

    if not docs:
        print(
            "No documents were loaded from data/raw/policy_docs "
            "or data/synthetic/company_policy_documents."
        )
        return

    print("-" * 80)

    for i, doc in enumerate(docs[:10], start=1):
        print(f"Document #{i}")
        print(f"Source file: {doc.metadata.get('source_file')}")
        print(f"Source type: {doc.metadata.get('source_type')}")
        print(f"Page: {doc.metadata.get('page')}")
        print("Text preview:")
        print(doc.page_content[:500].replace("\n", " "))
        print("-" * 80)


if __name__ == "__main__":
    main()