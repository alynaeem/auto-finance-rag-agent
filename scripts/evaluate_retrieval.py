
from auto_finance_rag_agent.retrieval.vector_store import load_vectorstore

EVAL_QUESTIONS = [
    {
        "question": "What documents are required for a salaried auto finance applicant?",
        "expected_source": "required_documents_policy.md",
    },
    {
        "question": "When should an auto finance application be sent to manual review?",
        "expected_source": "eligibility_policy.md",
    },
    {
        "question": "How should add-on product cancellation complaints be handled?",
        "expected_source": "add_on_products_policy.md",
    },
    {
        "question": "What should a borrower compare before choosing an auto loan?",
        "expected_source": "cfpb_auto_loan_guide.pdf",
    },
    {
        "question": "How should complaints be escalated when they involve repossession or credit reporting?",
        "expected_source": "complaint_handling_policy.md",
    },
]


def main() -> None:
    vectorstore = load_vectorstore()

    total = len(EVAL_QUESTIONS)
    passed = 0

    for item in EVAL_QUESTIONS:
        question = item["question"]
        expected_source = item["expected_source"]

        results = vectorstore.similarity_search_with_score(
            query=question,
            k=5,
        )

        returned_sources = [
            document.metadata.get("source_file")
            for document, _score in results
        ]

        is_pass = expected_source in returned_sources

        if is_pass:
            passed += 1

        status = "PASS" if is_pass else "FAIL"

        print("=" * 100)
        print(f"Question: {question}")
        print(f"Expected source: {expected_source}")
        print(f"Returned sources: {returned_sources}")
        print(f"Status: {status}")

    hit_rate = passed / total

    print("=" * 100)
    print(f"Passed: {passed}/{total}")
    print(f"Top-5 retrieval hit rate: {hit_rate:.2%}")


if __name__ == "__main__":
    main()