import json

from auto_finance_rag_agent.agent.nodes import policy_qna_node


def main() -> None:
    state = {
        "user_query": "What documents are required for a salaried auto finance applicant?",
        "intent": "policy_qna",
    }

    update = policy_qna_node(state)

    final_state = {
        **state,
        **update,
    }

    print("Node update:")
    print(json.dumps(update, indent=2))

    print("=" * 80)

    print("Final answer from result:")
    print(final_state["result"]["answer"])


if __name__ == "__main__":
    main()