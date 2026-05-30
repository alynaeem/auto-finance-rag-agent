import json

from auto_finance_rag_agent.retrieval.retriever import retrieve_policy_context


def main() -> None:
    query = "What documents are required for a salaried auto finance applicant?"

    contexts = retrieve_policy_context(query, k=3)

    print(f"Query: {query}")
    print(f"Contexts returned: {len(contexts)}")
    print("-" * 80)

    for index, context in enumerate(contexts, start=1):
        print(f"Context #{index}")
        print(json.dumps(context, indent=2))
        print("-" * 80)


if __name__ == "__main__":
    main()