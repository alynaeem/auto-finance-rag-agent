import json

from auto_finance_rag_agent.retrieval.vector_store import load_vectorstore


def main() -> None:
    query = "What documents are required for a salaried auto finance applicant?"

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search_with_score(
        query=query,
        k=5,
    )

    print(f"Query: {query}")
    print(f"Results returned: {len(results)}")
    print("-" * 80)

    for index, (document, score) in enumerate(results, start=1):
        print(f"Result #{index}")
        print(f"Score: {score}")
        print("Metadata:")
        print(json.dumps(document.metadata, indent=2))
        print("Text preview:")
        print(document.page_content[:700].replace("\n", " "))
        print("-" * 80)


if __name__ == "__main__":
    main()