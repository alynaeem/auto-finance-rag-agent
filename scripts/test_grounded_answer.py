import json

from auto_finance_rag_agent.generation.answer_generator import generate_grounded_answer
from auto_finance_rag_agent.retrieval.retriever import retrieve_policy_context


def main() -> None:
    query = "What documents are required for a salaried auto finance applicant?"

    contexts = retrieve_policy_context(query, k=3)

    print("Question:")
    print(query)

    print("=" * 80)
    print("Retrieved contexts:")

    for index, context in enumerate(contexts, start=1):
        print("-" * 80)
        print(f"Context #{index}")
        print("Metadata:")
        print(
            json.dumps(
                {
                    "source_file": context.get("source_file"),
                    "source_type": context.get("source_type"),
                    "page": context.get("page"),
                    "section_path": context.get("section_path"),
                    "score": context.get("score"),
                },
                indent=2,
            )
        )
        print("Content preview:")
        print(context.get("content", "")[:500].replace("\n", " "))

    print("=" * 80)
    print("Gemini answer:")

    answer = generate_grounded_answer(query, contexts)

    print(answer)


if __name__ == "__main__":
    main()