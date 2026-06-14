from auto_finance_rag_agent.agent.graph import agent_graph, run_agent


THREAD_ID = "test-user-001"


def print_messages(thread_id: str) -> None:
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    state = agent_graph.get_state(config)

    print("Stored messages:")
    for message in state.values.get("messages", []):
        print(f"{message.type}: {message.content[:120]}")
    print("=" * 80)


def main() -> None:
    first = run_agent(
        user_query="Compare 48 and 60 month loan offers.",
        input_data={
            "amount_financed": 20000,
            "annual_apr": 8,
            "terms_months": [48, 60],
        },
        thread_id=THREAD_ID,
    )

    print("FIRST ANSWER")
    print(first["final_answer"])
    print("=" * 80)

    second = run_agent(
        user_query="Which one has lower total interest?",
        input_data={
            "amount_financed": 20000,
            "annual_apr": 8,
            "terms_months": [48, 60],
        },
        thread_id=THREAD_ID,
    )

    print("SECOND ANSWER")
    print(second["final_answer"])
    print("=" * 80)

    print_messages(THREAD_ID)


if __name__ == "__main__":
    main()