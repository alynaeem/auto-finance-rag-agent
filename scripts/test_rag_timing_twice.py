from auto_finance_rag_agent.generation.rag_service import ask_policy_question


def main() -> None:
    query = "What documents are required for a salaried auto finance applicant?"

    print("First call")
    ask_policy_question(query, k=3)

    print("-" * 80)

    print("Second call")
    ask_policy_question(query, k=3)


if __name__ == "__main__":
    main()