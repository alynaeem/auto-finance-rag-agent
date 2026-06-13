from auto_finance_rag_agent.agent.intent import classify_intent


def main() -> None:
    test_queries = [
        "What documents are required for a salaried applicant?",
        "Calculate monthly payment for 20000 at 8% APR for 60 months.",
        "Compare 48 month and 60 month loan offers.",
        "The applicant submitted ID and salary slip. What documents are missing?",
        "Show refund complaint trends for auto loans.",
        "Predict credit risk for this applicant.",
        "Hello, how are you?",
    ]

    for query in test_queries:
        intent = classify_intent(query)

        print(f"Query: {query}")
        print(f"Intent: {intent}")
        print("-" * 80)


if __name__ == "__main__":
    main()